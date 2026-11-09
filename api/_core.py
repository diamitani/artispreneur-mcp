#!/usr/bin/env python3
"""
Artispreneur MCP + REST API -- shared core (v1).

ONE core, TWO runtimes: the local runner (server.py, http.server) and the
Vercel serverless functions (api/*.py) both import this module. It is pure
functions with NO http.server dependency at import time, so either runtime
can use it -- and so it can be unit-tested without a socket.

Scope is Artispreneur ONLY. No salesgency tenant, no skill-co tenant.

  - library      : the 385-skill library (384 audited + grok-social-cleanup
                   as #385; full bodies for entitled tiers)
  - artispreneur : the 88-skill music layer (only pro-registration is ACTIVE;
                   the other 87 are draft: metadata only, bodies never served)

Tools -- exactly 6, constant no matter how large the catalog grows:
  list_skills, search_skills, get_skill, list_agents, get_agent, list_packs.

REST -- the same auth + gating as MCP, on /api/* (see handle_rest):
  GET /health (public), GET /api/skills, GET /api/skills/:slug,
  GET /api/agents, GET /api/agents/:slug, GET /api/packs.

Buy-in-his-store model (no upload):
  A customer buys a pack in Patrick's store (Stripe checkout -> webhook ->
  entitlement). They then connect this ONE endpoint in Muse/Claude/etc. with
  their key. Every get_skill call checks that key's tier and serves only what
  the tier owns. Cancel -> key revoked -> 401. Improve a skill -> every
  customer gets it instantly. No zip, no upload, no copyable file.

Auth -- two layers, both Bearer, constant-time compare:
  1. MCP_AUTH_TOKEN env (admin key, full access, key_id "admin").
     Optional; unset = demo keys only. NEVER commit a real value; set it in
     the host dashboard.
  2. Per-key entitlements in entitlements.json (DEMO ONLY in this package).
     In production this file MUST be replaced by a Supabase lookup
     (public.has_access(uid, product_id) + usage_ledger, mirroring
     ~/workspace/salesgency-platform-backend/supabase/schema.sql).
     Unknown token -> 401. Revoked token -> 401.
     If the file is absent at runtime (it is, on Vercel -- excluded from
     the deploy on purpose), zero demo keys load and the admin token is the
     only auth. That is not an error; the server must NOT crash.

Metering: get_skill calls count as runs. Free tier: 50/month. Paid tiers:
unlimited skill reads in this server. Counts come from usage_ledger.jsonl
(append-only, key_id only, no tokens, no PII). On Vercel the ledger defaults
to /tmp/usage_ledger.jsonl (the serverless filesystem is ephemeral, so
metering there is best-effort); in production the ledger is the Supabase
usage_ledger table. Ledger writes never fail a call (OSError -> pass).

Sessions -- Vercel statelessness:
  Serverless functions cannot hold sessions or SSE across invocations, so
  this server runs in LENIENT/STATELESS mode: initialize returns a session
  id, but tools/call ACCEPTS a missing or unknown session id -- auth is the
  Bearer token, not the session. The one exception: a session id that was
  explicitly torn down with DELETE /mcp is remembered (in-process) and
  rejected with -32001, so teardown is still meaningful on the local
  runner. GET /mcp (SSE keep-alive) is NOT supported on Vercel -- the
  Vercel function returns 405; POST is the transport there. The local
  runner still serves the SSE keep-alive loop.

MCP protocol: Streamable HTTP (spec 2025-03-26 / 2025-06-18).
Python 3.9+ stdlib ONLY -- no pip installs, no requirements.txt.
"""
import hashlib
import hmac
import json
import os
import re
import threading
import uuid
from datetime import datetime, timezone

_CORE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_CORE_DIR)
SKILLS_DIR = os.environ.get("SKILLS_DIR", os.path.join(ROOT, "skills"))
INDEX_PATH = os.environ.get("INDEX_PATH", os.path.join(ROOT, "skills-index.json"))
MUSIC_SKILLS_DIR = os.environ.get(
    "MUSIC_SKILLS_DIR", os.path.join(ROOT, "skills-artispreneur"))
MUSIC_CATALOG_PATH = os.environ.get(
    "MUSIC_CATALOG_PATH", os.path.join(ROOT, "data", "music-catalog.json"))
PACKS_PATH = os.environ.get("PACKS_PATH", os.path.join(ROOT, "packs.json"))
ENTITLEMENTS_PATH = os.environ.get(
    "ENTITLEMENTS_PATH", os.path.join(ROOT, "entitlements.json"))
AGENTS_PATH = os.environ.get("AGENTS_PATH", os.path.join(ROOT, "agents.json"))
if os.environ.get("USAGE_LEDGER_PATH"):
    USAGE_LEDGER_PATH = os.environ["USAGE_LEDGER_PATH"]
elif os.environ.get("VERCEL"):
    # Serverless filesystem is ephemeral: ledger lives in /tmp and may
    # reset between invocations. Best-effort metering only; production
    # metering is the Supabase usage_ledger table.
    USAGE_LEDGER_PATH = "/tmp/usage_ledger.jsonl"
else:
    USAGE_LEDGER_PATH = os.path.join(ROOT, "usage_ledger.jsonl")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8787"))
# Public base URL shown on the landing page (e.g. https://artispreneur-mcp.onrender.com).
# Empty = relative links; never include a token here.
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")
MCP_AUTH_TOKEN = os.environ.get("MCP_AUTH_TOKEN", "").strip()

SERVER_NAME = "artispreneur-mcp"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26")

# Free taste: the 5 library skills any valid key may read, no purchase.
# Verified present in skills-index.json (385). Change only in packs.json
# + here together; the smoke test asserts all 5 exist.
FREE_TASTE_SKILLS = {
    "business-model-canvas-builder",
    "create-content-calendar",
    "email-architect",
    "technical-writing-pro",
    "write-a-business-plan",
}

# Which tiers may read full bodies. Artispreneur tiers read the library and
# the active music skill; free reads free taste only.
LIBRARY_FULL_TIERS = {
    "artispreneur-all-access", "artispreneur-pro", "artispreneur-label",
    "admin",
}
ARTISPRENEUR_ACTIVE_TIERS = {
    "artispreneur-all-access", "artispreneur-pro", "artispreneur-label",
    "admin",
}

# ------------------------------------------------------------------ data load
_index = []          # unified entries: {slug,name,description,category,tenant,status,tier_required,sha256}
_by_key = {}         # (tenant, slug) -> entry
_packs = []
_agents = []
_entitlements = []   # demo keys
_body_cache = {}
_body_lock = threading.Lock()
_ledger_lock = threading.Lock()


def _load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def load_all():
    global _packs, _agents, _entitlements
    lib = _load_json(INDEX_PATH, [])
    if isinstance(lib, dict):
        lib = lib.get("skills", [])
    for e in lib:
        slug = e["slug"]
        _index.append({
            "slug": slug, "name": e.get("name") or slug,
            "description": e.get("description") or "",
            "category": e.get("category") or "other",
            "tenant": "library",
            "status": "active",
            "tier_required": ("free-taste" if slug in FREE_TASTE_SKILLS
                              else "artispreneur-all-access"),
            "sha256": e.get("sha256"),
        })
    music = _load_json(MUSIC_CATALOG_PATH, {})
    for s in music.get("skills", []):
        _index.append({
            "slug": s["slug"], "name": s.get("name") or s["slug"],
            "description": s.get("description") or "",
            "category": s.get("category") or "music",
            "tenant": "artispreneur",
            "status": s.get("status") or "draft",
            "tier_required": ("artispreneur-all-access"
                              if s.get("status") == "active" else "draft-blocked"),
            "agent": s.get("agent"),
            "sha256": None,
        })
    _packs_data = _load_json(PACKS_PATH, [])
    _packs = (_packs_data.get("packs", []) if isinstance(_packs_data, dict)
              else _packs_data)
    _agents = _load_json(AGENTS_PATH, {}).get("agents", [])
    # Absent file -> zero demo keys, admin token only. NOT an error; never
    # crash here.
    # PRODUCTION GUARD (fix 2026-11-08, found on first live deploy): Vercel
    # uploads the whole project dir, so entitlements.json ships even though
    # vercel.json includeFiles omits it. .vercelignore is the first line of
    # defence; this is the second: on Vercel, demo entitlements are NEVER
    # loaded even if the file is present. Only MCP_AUTH_TOKEN authenticates.
    if os.environ.get("VERCEL"):
        _entitlements = []
    else:
        _entitlements = _load_json(ENTITLEMENTS_PATH, {}).get("keys", [])
    for e in _index:
        _by_key[(e["tenant"], e["slug"])] = e
    return {
        "library": sum(1 for e in _index if e["tenant"] == "library"),
        "artispreneur_active": sum(
            1 for e in _index
            if e["tenant"] == "artispreneur" and e["status"] == "active"),
        "artispreneur_draft": sum(
            1 for e in _index
            if e["tenant"] == "artispreneur" and e["status"] == "draft"),
        "packs": len(_packs),
        "agents": len(_agents),
    }


COUNTS = load_all()


def skill_body(tenant, slug):
    """Full SKILL.md text, or None. Draft music skills have no body file
    in this package (only pro-registration.md ships under
    skills-artispreneur/), so a draft body lookup returns None -- but
    _readable() blocks drafts before the body is ever read."""
    base = SKILLS_DIR if tenant == "library" else MUSIC_SKILLS_DIR
    key = (tenant, slug)
    with _body_lock:
        if key in _body_cache:
            return _body_cache[key]
    path = os.path.join(base, slug + ".md")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    with _body_lock:
        _body_cache[key] = text
    return text


def health_payload():
    return {
        "ok": True, "service": SERVER_NAME, "version": SERVER_VERSION,
        "tenants": {
            "library": {"skills": COUNTS["library"]},
            "artispreneur": {"active": COUNTS["artispreneur_active"],
                             "draft": COUNTS["artispreneur_draft"]},
        },
        "packs": COUNTS["packs"], "agents": COUNTS["agents"],
        "auth": "enabled" if (MCP_AUTH_TOKEN or _entitlements) else "disabled",
        "entitlements": ("demo-file (DEMO ONLY -- NOT production, see README)"
                         if _entitlements else
                         "admin-only (no demo entitlements file present)"),
    }


def info_text():
    return (SERVER_NAME + " v" + SERVER_VERSION + "\n"
            "Artispreneur MCP: library (%d skills) + artispreneur "
            "(%d active / %d draft) + %d agents + %d packs\n"
            "MCP Streamable HTTP endpoint: POST /mcp (GET /mcp is the SSE stream)\n"
            "REST API: GET /api/skills, /api/skills/:slug, /api/agents, "
            "/api/agents/:slug, /api/packs\n"
            "Health: GET /health\n"
            "Auth: Bearer token on /mcp and /api/* (per-key entitlements; "
            "demo keys in entitlements.json, DEMO ONLY)\n"
            % (COUNTS["library"], COUNTS["artispreneur_active"],
               COUNTS["artispreneur_draft"], COUNTS["agents"],
               COUNTS["packs"]))


def landing_html(base_url="", host=""):
    """Human landing page for GET / (a browser tap must not see raw JSON).

    No token is ever shown. The MCP endpoint is POST /mcp; GET /mcp is the
    SSE stream and needs a Bearer token + session, so browsers are told
    to connect through Muse instead of tapping /mcp directly.
    The connect line uses BASE_URL when set, else the request Host, so it
    is correct on every host (Render, Vercel, localhost) without edits.
    """
    if base_url:
        mcp_url = base_url.rstrip("/") + "/mcp"
    elif host:
        mcp_url = "https://" + host + "/mcp" if ":" not in host \
            else "http://" + host + "/mcp"
    else:
        mcp_url = "/mcp"
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Artispreneur MCP — Skills &amp; Agents for Muse</title>
<style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:640px;margin:48px auto;padding:0 20px;color:#111;line-height:1.55}h1{font-size:28px;margin-bottom:4px}.sub{color:#555;margin-top:0}.card{border:1px solid #ddd;border-radius:12px;padding:16px 20px;margin:16px 0}.num{font-size:32px;font-weight:700}code{background:#f2f2f2;padding:2px 6px;border-radius:6px;word-break:break-all}a{color:#0b5fff}</style>
</head><body>
<h1>Artispreneur MCP</h1>
<p class="sub">The data and MCP layer for the music industry — skills and agents
your AI assistant can run on demand.</p>
<div class="card"><span class="num">%d</span> skills in the library<br>
<span class="num">%d</span> active music skills <span style="color:#555">(%d more in draft — bodies never served)</span><br>
<span class="num">%d</span> music agents &nbsp;·&nbsp; <span class="num">%d</span> packs</div>
<h2>Connect in Meta Muse</h2>
<p>Open a new chat in Muse (muse.ai or the Muse app) and send exactly:</p>
<p><code>Add Artispreneur Skill Library as a custom MCP connector: %s</code></p>
<p>Then ask: <code>List your Artispreneur skills</code></p>
<p>Muse will ask you to sign in with your Artispreneur key. Copy it from your
Artispreneur account — never paste a key into chat text.</p>
<h2>For developers</h2>
<ul>
<li>MCP endpoint: <code>POST %s</code> (Streamable HTTP, protocol 2025-06-18).
GET <code>/mcp</code> is the SSE stream and needs a Bearer token and session —
opening it in a browser will not work.</li>
<li>Health: <a href="/health">GET /health</a> (public, counts only).</li>
<li>REST API: <code>GET /api/skills</code>, <code>/api/skills/:slug</code>,
<code>/api/agents</code>, <code>/api/agents/:slug</code>, <code>/api/packs</code>
(Bearer token required).</li>
<li>Tools: <code>list_skills</code>, <code>search_skills</code>, <code>get_skill</code>,
<code>list_agents</code>, <code>get_agent</code>, <code>list_packs</code>.</li>
</ul>
<p><a href="https://artispreneur.com">artispreneur.com</a></p>
</body></html>
""" % (COUNTS["library"], COUNTS["artispreneur_active"],
       COUNTS["artispreneur_draft"], COUNTS["agents"], COUNTS["packs"],
       mcp_url, mcp_url)

# ------------------------------------------------------------- auth + metering
class GatedError(Exception):
    """A call the caller's tier may not make. Carries a machine code,
    a human message, and (when a purchase fixes it) an upgrade hint."""

    def __init__(self, code, message, upgrade_hint=None, pack_id=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.upgrade_hint = upgrade_hint
        self.pack_id = pack_id


# Preferred pack per tier wins over first-match (QA W-1 fix, carried over
# from skill-co-mcp: first-match returned the wrong pack for a tier).
# Artispreneur only here: a free key that hits a paid skill or exhausts its
# allowance is pointed at All-Access $20/mo, pack artispreneur-all-access.
_PREFERRED_PACK_FOR_TIER = {
    "artispreneur-all-access": "artispreneur-all-access",
    "artispreneur-pro": "artispreneur-pro",
    "artispreneur-label": "artispreneur-label",
    "free": "artispreneur-all-access",
}


def _pack_for_tier(tier):
    preferred = _PREFERRED_PACK_FOR_TIER.get(tier)
    if preferred:
        for p in _packs:
            if p.get("id") == preferred:
                return p
    for p in _packs:
        if p.get("tier_required") == tier:
            return p
    return None


def _upgrade_hint(tier_required):
    pack = _pack_for_tier(tier_required)
    if not pack:
        return None
    price = pack["price_cents"] / 100
    interval = (" / %s" % pack["interval"]) if pack.get("interval") else ""
    return ("Buy %s ($%.2f%s) at %s -- then reconnect with your key."
            % (pack["name"], price, interval, pack.get("buy_url", "")))


def _resolve_bearer(auth_header):
    """Return (entitlement_dict, reason) or (None, reason).

    Entitlement: {"key_id": str, "tier": str, "runs_allowance_per_month": int|None}
    reason is one of: ok / missing / unknown / revoked.
    """
    if not auth_header:
        return None, "missing"
    if MCP_AUTH_TOKEN and hmac.compare_digest(
            auth_header, "Bearer " + MCP_AUTH_TOKEN):
        return {"key_id": "admin", "tier": "admin",
                "runs_allowance_per_month": None}, "ok"
    for k in _entitlements:
        if hmac.compare_digest(auth_header, "Bearer " + k.get("token", "")):
            if k.get("revoked"):
                return None, "revoked"
            return {"key_id": k.get("key_id"), "tier": k.get("tier"),
                    "runs_allowance_per_month": k.get("runs_allowance_per_month")}, "ok"
    return None, "unknown"


def _unauthorized_body(reason):
    return json.dumps({
        "error": "unauthorized",
        "reason": reason,
        "message": "Missing, unknown or revoked Authorization: Bearer <token>. "
                   "Buy a pack in Patrick's store and use the key it issues; "
                   "demo keys are listed in entitlements.json (DEMO ONLY)."}
    ).encode()


def _log_usage(key_id, tool, tenant, slug, allowed, reason):
    rec = {"ts": datetime.now(timezone.utc).isoformat(),
           "key_id": key_id, "tool": tool, "tenant": tenant or "",
           "slug": slug or "", "allowed": bool(allowed),
           "reason": reason or ""}
    try:
        with _ledger_lock:
            with open(USAGE_LEDGER_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass  # metering degrades to unmetered rather than failing calls


def _runs_used_this_month(key_id):
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    try:
        used = 0
        with open(USAGE_LEDGER_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if (r.get("key_id") == key_id and r.get("tool") == "get_skill"
                        and r.get("allowed") is True
                        and str(r.get("ts", "")).startswith(month)):
                    used += 1
        return used
    except OSError:
        return 0


def _readable(entry, ent):
    """May this entitlement read the skill BODY?"""
    if entry["tenant"] == "library" and entry["slug"] in FREE_TASTE_SKILLS:
        return True
    if entry.get("status") == "draft":
        return False
    tier = ent["tier"]
    if entry["tenant"] == "library":
        return tier in LIBRARY_FULL_TIERS
    if entry["tenant"] == "artispreneur":
        return tier in ARTISPRENEUR_ACTIVE_TIERS
    return False


def _gated_error(entry, ent):
    if entry.get("status") == "draft":
        return GatedError(
            "draft-gated",
            "Skill '%s' is DRAFT (written, unreviewed) in the Artispreneur "
            "music layer and is not shippable yet. Its body is not served "
            "to any tier, including paid tiers. 87 of 88 music skills are "
            "in this state; only pro-registration is active."
            % entry["slug"])
    tier = entry.get("tier_required") or "artispreneur-all-access"
    return GatedError(
        "not-entitled",
        "Your tier '%s' does not include skill '%s' (tenant %s). "
        "Free keys read only the 5 free-taste skills; this skill needs "
        "tier '%s'." % (ent["tier"], entry["slug"], entry["tenant"], tier),
        upgrade_hint=_upgrade_hint(tier),
        pack_id=(_pack_for_tier(tier) or {}).get("id"))


def _check_allowance(ent, entry):
    allowance = ent.get("runs_allowance_per_month")
    if allowance is None:
        return
    used = _runs_used_this_month(ent["key_id"])
    if used >= allowance:
        # Free keys upgrade to All-Access $20/mo; any other metered tier
        # upgrades within its own lane.
        tier = ("artispreneur-all-access" if ent["tier"] == "free"
                else ent["tier"])
        raise GatedError(
            "allowance-exhausted",
            "Run allowance exhausted: %d/%d get_skill runs used this month "
            "on key '%s'." % (used, allowance, ent["key_id"]),
            upgrade_hint=_upgrade_hint(tier),
            pack_id=(_pack_for_tier(tier) or {}).get("id"))

# ------------------------------------------------------------------ tool logic
def _public_entry(e, ent):
    return {"slug": e["slug"], "name": e.get("name"),
            "description": e.get("description"),
            "category": e.get("category"), "tenant": e["tenant"],
            "status": e.get("status"),
            "readable": _readable(e, ent)}


def tool_list_skills(args, ent):
    tenant = (args.get("tenant") or "library").strip().lower()
    query = (args.get("query") or "").strip().lower()
    category = (args.get("category") or "").strip().lower()
    include_gated = bool(args.get("include_gated") or False)
    page = max(1, int(args.get("page") or 1))
    per_page = min(200, max(1, int(args.get("per_page") or 50)))
    if tenant not in ("library", "artispreneur", "all"):
        raise ValueError("tenant must be library, artispreneur or all")
    items = [e for e in _index
             if tenant == "all" or e["tenant"] == tenant]
    if category:
        items = [e for e in items
                 if (e.get("category") or "").lower() == category]
    if query:
        items = [e for e in items
                 if query in e["slug"].lower()
                 or query in (e.get("name") or "").lower()
                 or query in (e.get("description") or "").lower()]
    readable = [e for e in items if _readable(e, ent)]
    shown = items if include_gated else readable
    total = len(shown)
    start = (page - 1) * per_page
    return {"tenant": tenant, "total": total,
            "readable_count": len(readable),
            "page": page, "per_page": per_page,
            "note": ("Listing shows only skills your tier can read. "
                     "Pass include_gated=true to see gated/draft metadata.")
            if not include_gated else
            "Listing includes gated/draft metadata (readable=false). "
            "get_skill still enforces tier and draft status.",
            "skills": [_public_entry(e, ent)
                       for e in shown[start:start + per_page]]}


def _score(entry, body, terms):
    hay = ((entry.get("name") or "") + " " + (entry.get("description") or "")
           + " " + (entry.get("category") or "") + " "
           + (entry.get("slug") or "")).lower()
    body_l = (body or "")[:12000].lower()
    score, matched = 0.0, 0
    for t in terms:
        c_title = hay.count(t)
        c_body = body_l.count(t)
        if c_title or c_body:
            matched += 1
        score += 10.0 * c_title + 0.5 * c_body
    if matched < max(1, len(terms) // 2):
        return 0.0
    return score * (1.0 + 0.5 * matched / max(1, len(terms)))


def tool_search_skills(args, ent):
    q = (args.get("q") or "").strip()
    tenant = (args.get("tenant") or "all").strip().lower()
    include_gated = bool(args.get("include_gated") or False)
    limit = min(50, max(1, int(args.get("limit") or 20)))
    if not q:
        raise ValueError("q is required")
    if tenant not in ("library", "artispreneur", "all"):
        raise ValueError("tenant must be library, artispreneur or all")
    terms = [t for t in re.split(r"\s+", q.lower()) if t]
    hits = []
    for entry in _index:
        if tenant != "all" and entry["tenant"] != tenant:
            continue
        readable = _readable(entry, ent)
        if not readable and not include_gated:
            continue
        # Bodies of gated skills are never searched (no content leak via scores).
        body = skill_body(entry["tenant"], entry["slug"]) if readable else ""
        s = _score(entry, body, terms)
        if s > 0:
            hits.append((s, entry))
    hits.sort(key=lambda h: -h[0])
    return {"query": q, "tenant": tenant, "count": len(hits[:limit]),
            "results": [{**_public_entry(e, ent), "score": round(s, 2)}
                        for s, e in hits[:limit]]}


def tool_get_skill(args, ent):
    slug = (args.get("slug") or "").strip()
    tenant = (args.get("tenant") or "library").strip().lower()
    if not slug:
        raise ValueError("slug is required")
    if tenant not in ("library", "artispreneur"):
        raise ValueError("tenant must be library or artispreneur")
    entry = _by_key.get((tenant, slug))
    if entry is None:
        raise LookupError("unknown skill slug '%s' in tenant '%s'"
                          % (slug, tenant))
    if not _readable(entry, ent):
        raise _gated_error(entry, ent)
    _check_allowance(ent, entry)
    text = skill_body(tenant, slug)
    if text is None:
        raise LookupError("skill body missing for '%s' in tenant '%s'"
                          % (slug, tenant))
    return {"tenant": tenant, "slug": slug, "name": entry.get("name"),
            "description": entry.get("description"),
            "category": entry.get("category"),
            "status": entry.get("status"),
            "sha256": (entry.get("sha256") or hashlib.sha256(
                text.encode("utf-8")).hexdigest()),
            "skill_md": text}


def tool_list_packs(args, ent):
    tenant = (args.get("tenant") or "all").strip().lower()
    if tenant not in ("artispreneur", "all"):
        raise ValueError("tenant must be artispreneur or all")
    out = []
    for p in _packs:
        if tenant != "all" and p.get("tenant") != tenant:
            continue
        tier = p.get("tier_required")
        # "entitled" = this caller already owns this exact pack.
        # "readable_via_your_tier" = this caller's tier can read the
        # skills that pack unlocks.
        if tier == "free" or ent["tier"] == "admin":
            readable = True
        elif tier in ("artispreneur-all-access", "artispreneur-pro",
                      "artispreneur-label"):
            readable = ent["tier"] in LIBRARY_FULL_TIERS
        else:
            readable = False
        out.append({**p,
                    "entitled": ent["tier"] == tier or ent["tier"] == "admin",
                    "readable_via_your_tier": readable})
    return {"tenant": tenant, "count": len(out), "packs": out,
            "note": ("Stripe prices and the webhook that grants these packs "
                     "are NOT live in this package. Buying happens in "
                     "Patrick's store at go-live; this server only enforces "
                     "the entitlement a key already carries.")}


def tool_list_agents(args, ent):
    tenant = (args.get("tenant") or "all").strip().lower()
    if tenant not in ("artispreneur", "all"):
        raise ValueError("tenant must be artispreneur or all")
    items = [a for a in _agents if tenant == "all" or a["tenant"] == tenant]
    return {"tenant": tenant, "count": len(items),
            "note": ("Agent DIRECTORY only -- this server lists agents, it "
                     "does not run agent loops. The loop runs in Rostr / "
                     "Muse / Claude, using the skills this server serves."),
            "agents": [{"slug": a["slug"], "tenant": a["tenant"],
                        "name": a.get("name"), "status": a.get("status"),
                        "skill_count": a.get("skill_count"),
                        "skills": a.get("skills", [])} for a in items]}


def tool_get_agent(args, ent):
    slug = (args.get("slug") or "").strip()
    if not slug:
        raise ValueError("slug is required")
    for a in _agents:
        if a["slug"] == slug:
            return {"slug": a["slug"], "tenant": a.get("tenant"),
                    "name": a.get("name"), "status": a.get("status"),
                    "status_note": a.get("status_note"),
                    "skill_count": a.get("skill_count"),
                    "skills": a.get("skills", []),
                    "note": ("Agent DIRECTORY only -- this server lists "
                             "agents, it does not run agent loops.")}
    raise LookupError("unknown agent slug '%s'" % slug)


TOOL_DEFS = [
    {"name": "list_skills",
     "description": ("Browse skills in one tenant (library, artispreneur) "
                     "or all. By default shows only skills your tier can "
                     "read; pass include_gated=true to see gated / draft "
                     "metadata. Call get_skill to read the full SKILL.md."),
     "inputSchema": {"type": "object", "properties": {
         "tenant": {"type": "string", "default": "library"},
         "query": {"type": "string"},
         "category": {"type": "string"},
         "page": {"type": "integer", "default": 1, "minimum": 1},
         "per_page": {"type": "integer", "default": 50, "minimum": 1, "maximum": 200},
         "include_gated": {"type": "boolean", "default": False}}}},
    {"name": "search_skills",
     "description": ("Keyword search across skill names, descriptions and "
                     "(readable) bodies. Gated skill bodies are never "
                     "searched, so nothing leaks through scores."),
     "inputSchema": {"type": "object", "properties": {
         "q": {"type": "string"},
         "tenant": {"type": "string", "default": "all"},
         "limit": {"type": "integer", "default": 20, "minimum": 1, "maximum": 50},
         "include_gated": {"type": "boolean", "default": False}},
        "required": ["q"]}},
    {"name": "get_skill",
     "description": ("Return the complete SKILL.md for one skill by slug + "
                     "tenant. Enforces tier (not-entitled error with an "
                     "upgrade hint), draft status (never served), and the "
                     "monthly run allowance."),
     "inputSchema": {"type": "object", "properties": {
         "slug": {"type": "string"},
         "tenant": {"type": "string", "default": "library"}},
        "required": ["slug"]}},
    {"name": "list_agents",
     "description": ("Agent directory: the 7 Artispreneur music agents "
                     "(booking, brand, day-to-day, finance, legal, PR, "
                     "publishing managers). Lists agents; does not run them."),
     "inputSchema": {"type": "object", "properties": {
         "tenant": {"type": "string", "default": "all"}}}},
    {"name": "get_agent",
     "description": ("Return one agent by slug, with its skill list and "
                     "status. Directory only -- does not run the agent."),
     "inputSchema": {"type": "object", "properties": {
         "slug": {"type": "string"}},
        "required": ["slug"]}},
    {"name": "list_packs",
     "description": ("The storefront: the 4 Artispreneur packs (Free $0, "
                     "All-Access $20/mo, Pro $200/mo, Label $25/seat/mo), "
                     "with price, tier required, and whether your key "
                     "already owns it / can read it. Stripe is not live here."),
     "inputSchema": {"type": "object", "properties": {
         "tenant": {"type": "string", "default": "all"}}}},
]

TOOL_FUNCS = {
    "list_skills": tool_list_skills,
    "search_skills": tool_search_skills,
    "get_skill": tool_get_skill,
    "list_agents": tool_list_agents,
    "get_agent": tool_get_agent,
    "list_packs": tool_list_packs,
}


def call_tool(name, args, ent):
    """Run one tool with metering + error mapping.

    Returns (result_dict, None) on success or (None, error_dict) where
    error_dict is {"code": str, "message": str, "upgrade_hint": ...,
    "pack_id": ...} for gated errors, {"code": "not-found"|"bad-args"|...,
    "message": str} otherwise. Shared by the MCP dispatcher and the REST
    handlers so both runtimes enforce identical gating.
    """
    func = TOOL_FUNCS.get(name)
    if func is None:
        return None, {"code": "unknown-tool",
                      "message": "unknown tool: %s" % name}
    if not isinstance(args, dict):
        args = {}
    tenant = args.get("tenant") or ""
    slug = args.get("slug") or ""
    try:
        result = func(args, ent)
    except GatedError as e:
        _log_usage(ent["key_id"], name, tenant, slug, False, e.code)
        return None, {"code": e.code, "message": e.message,
                      "upgrade_hint": e.upgrade_hint, "pack_id": e.pack_id}
    except LookupError as e:
        _log_usage(ent["key_id"], name, tenant, slug, False, "not-found")
        return None, {"code": "not-found", "message": str(e)}
    except ValueError as e:
        _log_usage(ent["key_id"], name, tenant, slug, False, "bad-args")
        return None, {"code": "bad-args", "message": str(e)}
    except Exception as e:  # noqa: BLE001 - surface as a tool error
        _log_usage(ent["key_id"], name, tenant, slug, False, "tool-error")
        return None, {"code": "tool-error", "message": "tool error: %s" % e}
    # get_skill is the metered call; log allowed runs for allowance counting.
    _log_usage(ent["key_id"], name, tenant, slug, True, "ok")
    return result, None

# ------------------------------------------------------------- JSON-RPC / MCP
_sessions = set()
_torn_down = set()
_sessions_lock = threading.Lock()


def _new_session():
    sid = uuid.uuid4().hex
    with _sessions_lock:
        _sessions.add(sid)
        _torn_down.discard(sid)
    return sid


def _valid_session(sid):
    with _sessions_lock:
        return sid in _sessions


def _is_torn_down(sid):
    with _sessions_lock:
        return sid in _torn_down


def _drop_session(sid):
    with _sessions_lock:
        _sessions.discard(sid)
        if sid:
            _torn_down.add(sid)


def _err(code, message, data=None):
    e = {"code": code, "message": message}
    if data is not None:
        e["data"] = data
    return e


def handle_message(msg, proto_ver, session_id, ent):
    """One JSON-RPC message -> (response_dict_or_None, None).

    Stateless/lenient sessions (see module docstring): a missing or unknown
    session id is ACCEPTED for tools/call -- auth is the Bearer token, not
    the session. Only a session id explicitly torn down with DELETE /mcp
    is rejected (-32001). initialize still mints a session id for clients
    that want one.
    """
    if not isinstance(msg, dict):
        return {"jsonrpc": "2.0", "id": None,
                "error": _err(-32600, "invalid request")}, None
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}
    is_notification = mid is None and "method" in msg

    def resp(result=None, error=None):
        r = {"jsonrpc": "2.0", "id": mid}
        if error is not None:
            r["error"] = error
        else:
            r["result"] = result
        return r

    if is_notification:
        return None, None  # swallow notifications (incl. initialized)

    if method == "initialize":
        client_ver = (params or {}).get("protocolVersion")
        chosen = client_ver if client_ver in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0]
        return resp({
            "protocolVersion": chosen,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }), None

    if session_id and _is_torn_down(session_id):
        return resp(error=_err(
            -32001, "session torn down; call initialize again")), None

    if method == "ping":
        return resp({}), None
    if method == "tools/list":
        return resp({"tools": TOOL_DEFS}), None
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        result, err = call_tool(name, args, ent)
        if err is not None:
            code = -32002 if err["code"] in (
                "not-entitled", "draft-gated", "allowance-exhausted",
                "not-found") else -32602
            data = {"error": err["code"]}
            if err.get("upgrade_hint"):
                data["upgrade_hint"] = err["upgrade_hint"]
            if err.get("pack_id"):
                data["pack_id"] = err["pack_id"]
            return resp(error=_err(code, err["message"], data)), None
        return resp({"content": [{"type": "text",
                                  "text": json.dumps(result, ensure_ascii=False, indent=2)}]}), None

    return resp(error=_err(-32601, "method not found: %s" % method)), None


def handle_mcp_post(raw, headers):
    """POST /mcp. headers: dict-like (case-insensitive lookup not assumed;
    callers pass lower-cased keys or use .get with the exact names the
    runtime supplies -- server.py and api/mcp.py normalise first).

    Returns (status, headers_dict, body_bytes).
    """
    ent, reason = _resolve_bearer(headers.get("authorization") or "")
    if ent is None:
        return 401, {"Content-Type": "application/json"}, _unauthorized_body(reason)
    try:
        payload = json.loads((raw or b"").decode("utf-8") or "null")
    except (ValueError, UnicodeDecodeError):
        body = json.dumps({"jsonrpc": "2.0", "id": None,
                           "error": _err(-32700, "parse error")}).encode()
        return 400, {"Content-Type": "application/json"}, body
    proto_ver = headers.get("mcp-protocol-version", PROTOCOL_VERSIONS[0])
    session_id = headers.get("mcp-session-id")
    messages = payload if isinstance(payload, list) else [payload]
    responses = []
    new_session = None
    for m in messages:
        if isinstance(m, dict) and m.get("method") == "initialize" and not session_id:
            new_session = _new_session()
        r, _ = handle_message(m, proto_ver, new_session or session_id, ent)
        if r is not None:
            responses.append(r)
    out_headers = {"Content-Type": "application/json",
                   "MCP-Protocol-Version": proto_ver}
    if new_session:
        out_headers["Mcp-Session-Id"] = new_session
    if not responses:
        return 202, out_headers, b""
    out = responses if isinstance(payload, list) else responses[0]
    return 200, out_headers, json.dumps(out).encode()


def handle_mcp_delete(headers):
    """DELETE /mcp. Returns (status, headers_dict, body_bytes)."""
    ent, reason = _resolve_bearer(headers.get("authorization") or "")
    if ent is None:
        return 401, {"Content-Type": "application/json"}, _unauthorized_body(reason)
    sid = headers.get("mcp-session-id")
    if sid:
        _drop_session(sid)
    return 200, {}, b""


# ------------------------------------------------------------------ REST API
def _rest_error(status, err):
    body = {"error": err.get("code", "error"), "message": err.get("message", "")}
    if err.get("upgrade_hint"):
        body["upgrade_hint"] = err["upgrade_hint"]
    if err.get("pack_id"):
        body["pack_id"] = err["pack_id"]
    return status, "application/json", json.dumps(body).encode()


def handle_rest(method, path, query, auth_header, host=""):
    """REST dispatcher. method: "GET" etc. path: URL path without query
    string. query: dict of str -> str (first value wins). auth_header: the
    raw Authorization header value ("" if absent). host: request Host
    header (used only for the landing page's connect line).

    Returns (status, content_type, body_bytes). Auth: 401 without a valid
    Bearer token on every /api route except /health (public).
    """
    if method != "GET":
        return 405, "application/json", json.dumps(
            {"error": "method-not-allowed",
             "message": "only GET is supported on REST routes"}).encode()
    if path == "/health":
        return 200, "application/json", json.dumps(health_payload()).encode()
    if path == "/":
        # Human landing page: a browser tap must see HTML, never raw JSON.
        return 200, "text/html; charset=utf-8", \
            landing_html(BASE_URL, host).encode()
    if not path.startswith("/api/"):
        return 404, "application/json", json.dumps(
            {"error": "not-found", "message": "unknown route: %s" % path}).encode()

    ent, reason = _resolve_bearer(auth_header or "")
    if ent is None:
        return 401, "application/json", _unauthorized_body(reason)

    parts = [p for p in path.split("/") if p]
    # parts: ["api", "skills", ...] etc.
    resource = parts[1] if len(parts) > 1 else ""
    slug = parts[2] if len(parts) > 2 else (query.get("slug") or "")
    if len(parts) > 3:
        return 404, "application/json", json.dumps(
            {"error": "not-found", "message": "unknown route: %s" % path}).encode()

    def _bool(v):
        return str(v).lower() in ("1", "true", "yes")

    if resource == "skills":
        if slug:
            result, err = call_tool("get_skill", {
                "slug": slug,
                "tenant": (query.get("tenant") or "library").strip().lower(),
            }, ent)
            if err is not None:
                status = 403 if err["code"] in (
                    "not-entitled", "draft-gated", "allowance-exhausted") else (
                    404 if err["code"] == "not-found" else 400)
                return _rest_error(status, err)
            return 200, "application/json", json.dumps(result).encode()
        args = {
            "tenant": (query.get("tenant") or "library"),
            "query": query.get("query") or query.get("q") or "",
            "category": query.get("category") or "",
            "page": query.get("page") or 1,
            "per_page": query.get("per_page") or 50,
            "include_gated": _bool(query.get("include_gated") or False),
        }
        result, err = call_tool("list_skills", args, ent)
        if err is not None:
            return _rest_error(400, err)
        return 200, "application/json", json.dumps(result).encode()

    if resource == "agents":
        if slug:
            result, err = call_tool("get_agent", {"slug": slug}, ent)
            if err is not None:
                status = 404 if err["code"] == "not-found" else 400
                return _rest_error(status, err)
            return 200, "application/json", json.dumps(result).encode()
        result, err = call_tool("list_agents", {
            "tenant": (query.get("tenant") or "all")}, ent)
        if err is not None:
            return _rest_error(400, err)
        return 200, "application/json", json.dumps(result).encode()

    if resource == "packs":
        if slug:
            return 404, "application/json", json.dumps(
                {"error": "not-found",
                 "message": "no per-pack route; use GET /api/packs"}).encode()
        result, err = call_tool("list_packs", {
            "tenant": (query.get("tenant") or "all")}, ent)
        if err is not None:
            return _rest_error(400, err)
        return 200, "application/json", json.dumps(result).encode()

    return 404, "application/json", json.dumps(
        {"error": "not-found", "message": "unknown route: %s" % path}).encode()
