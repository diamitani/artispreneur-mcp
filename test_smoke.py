#!/usr/bin/env python3
"""Smoke test for the Artispreneur MCP + REST API (server.py + api/_core.py).

Boots the real local server as a subprocess on a scratch port with a
scratch usage ledger, then runs the full MCP handshake plus tier-gating,
REST, metering and teardown checks:

  - /health + / public, no auth (library 385, artispreneur 1 active /
    87 draft, agents 7, packs 4)
  - /mcp and /api/* without auth / unknown key / revoked key -> 401
  - initialize -> session, tools/list -> exactly the 6 tools, ping
  - tools/call with NO session id still works (stateless/lenient mode --
    Vercel cannot hold sessions; auth is the Bearer token)
  - list_agents = 7, get_agent booking-manager = 13 skills
  - list_skills per tier (free library = 5 free-taste; all-access = 385,
    incl. grok-social-cleanup #385; artispreneur 1 readable / 88 gated)
  - search free finds free-taste and does NOT surface paid skills
  - get_skill: free taste ok; paid skill with free key -> not-entitled
    with All-Access $20/mo hint + pack_id artispreneur-all-access;
    draft skill -> draft-gated for free AND all-access AND admin;
    active music skill (pro-registration) readable by all-access
  - free key exhausts its 50-run monthly allowance, 51st get_skill fails
    with allowance-exhausted
  - list_packs = 4, all stripe_status not_live_in_this_package
  - REST: GET /api/skills/:slug and /api/agents/:slug work with auth and
    401 without; draft via REST -> 403 draft-gated
  - DELETE /mcp tears the session down; reuse after teardown -> -32001;
    fresh initialize after teardown works again
  - admin token (MCP_AUTH_TOKEN) grants full access; demo keys keep working
  - usage ledger: calls logged with key_id, admin token value never appears

Run:  python3 test_smoke.py
Exit 0 only if every check passes. No real tokens are used; the admin
token below is generated fresh per run and never written to disk.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8892
BASE = "http://127.0.0.1:%d" % PORT

FREE_TASTE = {
    "business-model-canvas-builder", "create-content-calendar",
    "email-architect", "technical-writing-pro", "write-a-business-plan",
}
EXPECTED_TOOLS = {"list_skills", "search_skills", "get_skill",
                  "list_agents", "get_agent", "list_packs"}
EXPECTED_PACKS = {"artispreneur-free", "artispreneur-all-access",
                  "artispreneur-pro", "artispreneur-label"}
ADMIN_TOKEN = "admin-test-" + uuid.uuid4().hex

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name
          + ((" -- " + str(detail)) if detail and not ok else ""), flush=True)


def http(method, path, token=None, body=None, session=None):
    req = urllib.request.Request(BASE + path, method=method)
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if session:
        req.add_header("Mcp-Session-Id", session)
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")

    def _parse(raw):
        if not raw:
            return None
        try:
            return json.loads(raw)
        except ValueError:
            return raw.decode("utf-8", "replace")

    try:
        with urllib.request.urlopen(req, data=data, timeout=10) as r:
            return r.status, dict(r.headers), _parse(r.read())
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), _parse(e.read())
    except Exception as e:  # noqa: BLE001 - report as a failed check
        return None, {}, {"_transport_error": str(e)}


def mcp(token, method, params=None, session=None, mid=1):
    body = {"jsonrpc": "2.0", "id": mid, "method": method}
    if params is not None:
        body["params"] = params
    return http("POST", "/mcp", token=token, body=body, session=session)


def mcp_call(token, tool, args, session=None, mid=1):
    status, headers, resp = mcp(
        token, "tools/call",
        {"name": tool, "arguments": args}, session=session, mid=mid)
    return status, headers, resp


def tool_result(resp):
    """Unwrap a successful tools/call response -> result dict or None."""
    try:
        return json.loads(resp["result"]["content"][0]["text"])
    except (KeyError, TypeError, ValueError):
        return None


def tool_error(resp):
    try:
        return resp["error"]
    except (KeyError, TypeError):
        return None


def free_get_skill_used(ledger_path):
    month = time.strftime("%Y-%m", time.gmtime())
    used = 0
    try:
        with open(ledger_path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if (r.get("key_id") == "demo-free"
                        and r.get("tool") == "get_skill"
                        and r.get("allowed") is True
                        and str(r.get("ts", "")).startswith(month)):
                    used += 1
    except OSError:
        pass
    return used


def main():
    tmp = tempfile.mkdtemp(prefix="artispreneur-mcp-smoke-")
    ledger = os.path.join(tmp, "usage_ledger.jsonl")
    env = dict(os.environ)
    env["PORT"] = str(PORT)
    env["HOST"] = "127.0.0.1"
    env["USAGE_LEDGER_PATH"] = ledger
    env["MCP_AUTH_TOKEN"] = ADMIN_TOKEN
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "server.py")],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True)
    try:
        # --- wait for boot ---
        up = False
        for _ in range(50):
            try:
                s, _, _ = http("GET", "/health")
                if s == 200:
                    up = True
                    break
            except Exception:
                pass
            time.sleep(0.2)
        check("server boots and /health answers", up)
        if not up:
            return 1

        # --- health counts (public, no auth) ---
        s, _, h = http("GET", "/health")
        check("health 200 without auth", s == 200, s)
        check("health library = 385",
              isinstance(h, dict) and h.get("tenants", {}).get("library", {}).get("skills") == 385, h)
        check("health artispreneur active = 1",
              isinstance(h, dict) and h.get("tenants", {}).get("artispreneur", {}).get("active") == 1, h)
        check("health artispreneur draft = 87",
              isinstance(h, dict) and h.get("tenants", {}).get("artispreneur", {}).get("draft") == 87, h)
        check("health agents = 7",
              isinstance(h, dict) and h.get("agents") == 7, h)
        check("health packs = 4",
              isinstance(h, dict) and h.get("packs") == 4, h)
        check("health entitlements labelled demo",
              isinstance(h, dict) and "demo" in str(h.get("entitlements", "")).lower(), h)

        s, _, root = http("GET", "/")
        check("GET / 200 HTML landing page (not raw JSON)",
              s == 200 and isinstance(root, str) and "<html" in root.lower()
              and "Artispreneur" in root and "Add Artispreneur Skill Library" in root, s)

        # --- 401s ---
        s, _, _ = http("POST", "/mcp", body={"jsonrpc": "2.0", "id": 1, "method": "ping"})
        check("POST /mcp no auth -> 401", s == 401, s)
        s, _, _ = http("POST", "/mcp", token="no-such-key",
                       body={"jsonrpc": "2.0", "id": 1, "method": "ping"})
        check("POST /mcp unknown key -> 401", s == 401, s)
        s, _, _ = http("POST", "/mcp", token="demo-revoked",
                       body={"jsonrpc": "2.0", "id": 1, "method": "ping"})
        check("POST /mcp revoked key -> 401", s == 401, s)
        for path in ("/api/skills", "/api/agents", "/api/packs",
                     "/api/skills/email-architect", "/api/agents/booking-manager"):
            s, _, _ = http("GET", path)
            check("GET %s no auth -> 401" % path, s == 401, s)
        s, _, _ = http("GET", "/api/skills", token="demo-revoked")
        check("GET /api/skills revoked key -> 401", s == 401, s)
        s, _, _ = http("GET", "/api/skills", token="no-such-key")
        check("GET /api/skills unknown key -> 401", s == 401, s)

        # --- initialize + session ---
        s, headers, resp = mcp("demo-all-access", "initialize",
                               {"protocolVersion": "2025-06-18",
                                "capabilities": {},
                                "clientInfo": {"name": "smoke", "version": "1"}})
        session = None
        for k, v in headers.items():
            if k.lower() == "mcp-session-id":
                session = v
        check("initialize 200 + session id",
              s == 200 and bool(session)
              and isinstance(resp, dict)
              and resp.get("result", {}).get("serverInfo", {}).get("name") == "artispreneur-mcp",
              (s, resp))
        s, _, resp = mcp("demo-all-access", "ping", session=session)
        check("ping with session ok",
              s == 200 and isinstance(resp, dict) and resp.get("result") == {}, resp)
        # Stateless/lenient: no session id at all still works.
        s, _, resp = mcp("demo-all-access", "ping", session=None)
        check("ping WITHOUT session ok (stateless/lenient mode)",
              s == 200 and isinstance(resp, dict) and resp.get("result") == {}, resp)

        # --- tools/list: exactly 6 ---
        s, _, resp = mcp("demo-all-access", "tools/list", session=session)
        tools = []
        try:
            tools = [t["name"] for t in resp["result"]["tools"]]
        except (KeyError, TypeError):
            pass
        check("tools/list returns exactly 6 tools", len(tools) == 6, tools)
        check("tools/list names are the 6 expected tools",
              set(tools) == EXPECTED_TOOLS, tools)

        # --- agents ---
        s, _, resp = mcp_call("demo-all-access", "list_agents", {}, session=session)
        res = tool_result(resp)
        check("list_agents = 7",
              isinstance(res, dict) and res.get("count") == 7, res)
        s, _, resp = mcp_call("demo-all-access", "get_agent",
                              {"slug": "booking-manager"}, session=session)
        res = tool_result(resp)
        check("get_agent booking-manager returns 13 skills",
              isinstance(res, dict) and res.get("slug") == "booking-manager"
              and len(res.get("skills", [])) == 13, res)
        s, _, resp = mcp_call("demo-all-access", "get_agent",
                              {"slug": "no-such-agent"}, session=session)
        check("get_agent unknown slug -> error",
              tool_error(resp) is not None, resp)

        # --- list_skills per tier ---
        s, _, resp = mcp_call("demo-free", "list_skills",
                              {"tenant": "library", "per_page": 200}, session=session)
        res = tool_result(resp)
        check("list_skills free library total = 5",
              isinstance(res, dict) and res.get("total") == 5, res)
        free_slugs = {e["slug"] for e in (res or {}).get("skills", [])}
        check("list_skills free library slugs are exactly the 5 free-taste",
              free_slugs == FREE_TASTE, free_slugs)
        s, _, resp = mcp_call("demo-all-access", "list_skills",
                              {"tenant": "library", "per_page": 200}, session=session)
        res = tool_result(resp)
        check("list_skills all-access library total = 385",
              isinstance(res, dict) and res.get("total") == 385, res)
        aa_slugs = {e["slug"] for e in (res or {}).get("skills", [])}
        check("list_skills all-access includes grok-social-cleanup (#385)",
              "grok-social-cleanup" in aa_slugs, len(aa_slugs))
        s, _, resp = mcp_call("demo-all-access", "list_skills",
                              {"tenant": "artispreneur", "include_gated": True},
                              session=session)
        res = tool_result(resp)
        check("list_skills artispreneur include_gated total = 88",
              isinstance(res, dict) and res.get("total") == 88, res)
        s, _, resp = mcp_call("demo-all-access", "list_skills",
                              {"tenant": "artispreneur"}, session=session)
        res = tool_result(resp)
        check("list_skills artispreneur default total = 1 (only active readable)",
              isinstance(res, dict) and res.get("total") == 1
              and res["skills"][0]["slug"] == "pro-registration", res)
        s, _, resp = mcp_call("demo-free", "list_skills",
                              {"tenant": "artispreneur"}, session=session)
        res = tool_result(resp)
        check("list_skills artispreneur free default total = 0",
              isinstance(res, dict) and res.get("total") == 0, res)

        # --- search ---
        s, _, resp = mcp_call("demo-free", "search_skills",
                              {"q": "business plan", "tenant": "library"},
                              session=session)
        res = tool_result(resp)
        found = {r["slug"] for r in (res or {}).get("results", [])}
        check("search free finds free-taste write-a-business-plan",
              "write-a-business-plan" in found, found)
        s, _, resp = mcp_call("demo-free", "search_skills",
                              {"q": "collaborative playlist", "tenant": "library"},
                              session=session)
        res = tool_result(resp)
        found = {r["slug"] for r in (res or {}).get("results", [])}
        check("search free does NOT surface paid playlist skill",
              "add-music-to-collaborative-playlist" not in found, found)
        s, _, resp = mcp_call("demo-all-access", "search_skills",
                              {"q": "collaborative playlist", "tenant": "library"},
                              session=session)
        res = tool_result(resp)
        found = {r["slug"] for r in (res or {}).get("results", [])}
        check("search all-access finds paid playlist skill",
              "add-music-to-collaborative-playlist" in found, found)

        # --- get_skill gating ---
        s, _, resp = mcp_call("demo-free", "get_skill",
                              {"slug": "email-architect", "tenant": "library"},
                              session=session)
        res = tool_result(resp)
        check("get_skill free-taste ok with free key",
              isinstance(res, dict) and res.get("slug") == "email-architect"
              and bool(res.get("skill_md")), res)
        s, _, resp = mcp_call("demo-free", "get_skill",
                              {"slug": "add-music-to-collaborative-playlist",
                               "tenant": "library"}, session=session)
        err = tool_error(resp)
        check("get_skill paid skill with free key -> not-entitled",
              err is not None and err.get("data", {}).get("error") == "not-entitled",
              err)
        check("not-entitled hint names All-Access $20/mo",
              err is not None and "All-Access" in str(err.get("data", {}).get("upgrade_hint", ""))
              and "$20.00" in str(err.get("data", {}).get("upgrade_hint", "")), err)
        check("not-entitled pack_id is artispreneur-all-access",
              err is not None and err.get("data", {}).get("pack_id") == "artispreneur-all-access",
              err)
        s, _, resp = mcp_call("demo-all-access", "get_skill",
                              {"slug": "pro-registration", "tenant": "artispreneur"},
                              session=session)
        res = tool_result(resp)
        check("get_skill pro-registration ok with all-access",
              isinstance(res, dict) and res.get("slug") == "pro-registration"
              and bool(res.get("skill_md")), res)
        s, _, resp = mcp_call("demo-free", "get_skill",
                              {"slug": "pro-registration", "tenant": "artispreneur"},
                              session=session)
        err = tool_error(resp)
        check("get_skill pro-registration with free key -> not-entitled",
              err is not None and err.get("data", {}).get("error") == "not-entitled",
              err)
        for key, label in (("demo-free", "free"), ("demo-all-access", "all-access"),
                           (ADMIN_TOKEN, "admin")):
            s, _, resp = mcp_call(key, "get_skill",
                                  {"slug": "artist-bio-writer", "tenant": "artispreneur"},
                                  session=session)
            err = tool_error(resp)
            check("get_skill draft skill -> draft-gated for %s" % label,
                  err is not None and err.get("data", {}).get("error") == "draft-gated",
                  err)
        s, _, resp = mcp_call("demo-all-access", "get_skill",
                              {"slug": "no-such-skill", "tenant": "library"},
                              session=session)
        check("get_skill unknown slug -> error",
              tool_error(resp) is not None, resp)

        # --- list_packs ---
        s, _, resp = mcp_call("demo-free", "list_packs", {}, session=session)
        res = tool_result(resp)
        check("list_packs = 4",
              isinstance(res, dict) and res.get("count") == 4, res)
        pack_ids = {p["id"] for p in (res or {}).get("packs", [])}
        check("list_packs ids are the 4 Artispreneur packs",
              pack_ids == EXPECTED_PACKS, pack_ids)
        check("list_packs all stripe_status not_live_in_this_package",
              isinstance(res, dict) and all(
                  p.get("stripe_status") == "not_live_in_this_package"
                  for p in res.get("packs", [])), res)

        # --- REST ---
        s, _, body = http("GET", "/api/skills?tenant=library&per_page=1",
                          token="demo-all-access")
        check("REST GET /api/skills with auth 200, total 385",
              s == 200 and isinstance(body, dict) and body.get("total") == 385,
              (s, body))
        s, _, body = http("GET", "/api/skills/email-architect", token="demo-free")
        check("REST GET /api/skills/:slug free-taste with free key 200",
              s == 200 and isinstance(body, dict)
              and body.get("slug") == "email-architect" and bool(body.get("skill_md")),
              (s, body))
        s, _, body = http("GET", "/api/skills/add-music-to-collaborative-playlist",
                          token="demo-free")
        check("REST GET /api/skills/:slug paid with free key -> 403 not-entitled",
              s == 403 and isinstance(body, dict) and body.get("error") == "not-entitled",
              (s, body))
        s, _, body = http("GET", "/api/agents/booking-manager",
                          token="demo-all-access")
        check("REST GET /api/agents/:slug booking-manager 200, 13 skills",
              s == 200 and isinstance(body, dict)
              and len(body.get("skills", [])) == 13, (s, body))
        s, _, body = http("GET", "/api/agents/booking-manager")
        check("REST GET /api/agents/:slug no auth -> 401", s == 401, s)
        s, _, body = http("GET", "/api/packs", token="demo-free")
        check("REST GET /api/packs with free key 200, count 4",
              s == 200 and isinstance(body, dict) and body.get("count") == 4,
              (s, body))
        s, _, body = http("GET", "/api/skills/artist-bio-writer?tenant=artispreneur",
                          token=ADMIN_TOKEN)
        check("REST GET draft skill with admin -> 403 draft-gated",
              s == 403 and isinstance(body, dict) and body.get("error") == "draft-gated",
              (s, body))
        s, _, body = http("GET", "/api/skills/no-such-skill", token="demo-all-access")
        check("REST GET unknown skill slug -> 404", s == 404, s)
        s, _, body = http("GET", "/api/agents", token="demo-all-access")
        check("REST GET /api/agents 200, count 7",
              s == 200 and isinstance(body, dict) and body.get("count") == 7,
              (s, body))

        # --- metering: free key 50-run allowance ---
        used = free_get_skill_used(ledger)
        check("ledger counts free get_skill runs so far (%d)" % used, used >= 2, used)
        mid = 100
        ok = True
        while used < 50:
            mid += 1
            s, _, resp = mcp_call("demo-free", "get_skill",
                                  {"slug": "email-architect", "tenant": "library"},
                                  session=session, mid=mid)
            if tool_result(resp) is None:
                ok = False
                break
            used += 1
        check("free key reaches exactly 50 allowed get_skill runs", ok and used == 50, used)
        s, _, resp = mcp_call("demo-free", "get_skill",
                              {"slug": "email-architect", "tenant": "library"},
                              session=session, mid=999)
        err = tool_error(resp)
        check("free 51st get_skill -> allowance-exhausted",
              err is not None and err.get("data", {}).get("error") == "allowance-exhausted",
              err)
        check("allowance-exhausted hint names All-Access + pack_id",
              err is not None
              and "All-Access" in str(err.get("data", {}).get("upgrade_hint", ""))
              and err.get("data", {}).get("pack_id") == "artispreneur-all-access",
              err)

        # --- admin token + demo keys still work ---
        s, _, resp = mcp_call(ADMIN_TOKEN, "get_skill",
                              {"slug": "add-music-to-collaborative-playlist",
                               "tenant": "library"}, session=session)
        res = tool_result(resp)
        check("admin token get_skill paid skill ok",
              isinstance(res, dict) and bool(res.get("skill_md")), res)
        s, _, resp = mcp_call("demo-all-access", "list_skills",
                              {"tenant": "library"}, session=session)
        res = tool_result(resp)
        check("demo-all-access still works after admin boot (total 385)",
              isinstance(res, dict) and res.get("total") == 385, res)
        s, _, resp = mcp_call("demo-pro", "get_skill",
                              {"slug": "pro-registration", "tenant": "artispreneur"},
                              session=session)
        res = tool_result(resp)
        check("demo-pro reads active music skill",
              isinstance(res, dict) and bool(res.get("skill_md")), res)
        s, _, resp = mcp_call("demo-label", "get_skill",
                              {"slug": "pro-registration", "tenant": "artispreneur"},
                              session=session)
        res = tool_result(resp)
        check("demo-label reads active music skill",
              isinstance(res, dict) and bool(res.get("skill_md")), res)

        # --- DELETE teardown, then reuse -> error; fresh init works ---
        s, _, _ = http("DELETE", "/mcp", token="demo-all-access", session=session)
        check("DELETE /mcp teardown 200", s == 200, s)
        s, _, resp = mcp("demo-all-access", "ping", session=session)
        err = tool_error(resp)
        check("reuse after teardown -> -32001 error",
              err is not None and err.get("code") == -32001, resp)
        s, headers, resp = mcp("demo-all-access", "initialize",
                               {"protocolVersion": "2025-06-18",
                                "capabilities": {},
                                "clientInfo": {"name": "smoke", "version": "1"}})
        new_session = None
        for k, v in headers.items():
            if k.lower() == "mcp-session-id":
                new_session = v
        check("fresh initialize after teardown works",
              s == 200 and bool(new_session) and new_session != session,
              (s, new_session))

        # --- ledger: key_id only, admin token value never appears ---
        try:
            ledger_text = open(ledger, encoding="utf-8").read()
        except OSError:
            ledger_text = ""
        check("usage ledger has get_skill lines for demo-free",
              '"key_id": "demo-free"' in ledger_text
              and '"tool": "get_skill"' in ledger_text, ledger_text[:200])
        check("usage ledger never contains the admin token value",
              ADMIN_TOKEN not in ledger_text, "admin token leaked into ledger")
        check("usage ledger has no Bearer token values",
              "Bearer" not in ledger_text, "Bearer string in ledger")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    # --- Vercel simulation: VERCEL=1 must disable demo keys even though
    # entitlements.json is present on disk (first live deploy proved Vercel
    # uploads the whole project dir). Admin token still works. ---
    vport = PORT + 1
    vbase = "http://127.0.0.1:%d" % vport
    vledger = os.path.join(tmp, "vercel-ledger.jsonl")

    def vhttp(method, path, token=None, body=None):
        req = urllib.request.Request(vbase + path, method=method)
        if token:
            req.add_header("Authorization", "Bearer " + token)
        if body is not None:
            req.add_header("Content-Type", "application/json")
            data = json.dumps(body).encode()
        else:
            data = None
        try:
            with urllib.request.urlopen(req, data=data, timeout=10) as resp:
                raw = resp.read()
                try:
                    return resp.status, json.loads(raw)
                except ValueError:
                    return resp.status, raw.decode(errors="replace")
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                return e.code, json.loads(raw)
            except ValueError:
                return e.code, raw.decode(errors="replace")

    venv = dict(os.environ)
    venv["PORT"] = str(vport)
    venv["HOST"] = "127.0.0.1"
    venv["VERCEL"] = "1"
    venv["USAGE_LEDGER_PATH"] = vledger
    venv["MCP_AUTH_TOKEN"] = ADMIN_TOKEN
    vproc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "server.py")],
        env=venv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True)
    try:
        vup = False
        for _ in range(50):
            try:
                s, _ = vhttp("GET", "/health")
                if s == 200:
                    vup = True
                    break
            except Exception:
                pass
            time.sleep(0.2)
        check("vercel-sim server boots", vup)
        if vup:
            s, h = vhttp("GET", "/health")
            check("vercel-sim health entitlements admin-only",
                  isinstance(h, dict) and "admin-only" in str(h.get("entitlements", "")), h)
            s, _ = vhttp("POST", "/mcp", token="demo-free",
                         body={"jsonrpc": "2.0", "id": 1, "method": "ping"})
            check("vercel-sim demo-free -> 401", s == 401, s)
            s, _ = vhttp("POST", "/mcp", token="demo-all-access",
                         body={"jsonrpc": "2.0", "id": 1, "method": "ping"})
            check("vercel-sim demo-all-access -> 401", s == 401, s)
            s, h = vhttp("POST", "/mcp", token=ADMIN_TOKEN,
                         body={"jsonrpc": "2.0", "id": 1, "method": "initialize",
                               "params": {"protocolVersion": "2025-06-18",
                                          "capabilities": {},
                                          "clientInfo": {"name": "smoke", "version": "1"}}})
            check("vercel-sim admin initialize 200", s == 200, s)
    finally:
        vproc.terminate()
        try:
            vproc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            vproc.kill()

    failed = [c for c in CHECKS if not c[1]]
    print("\n%d/%d checks passed" % (len(CHECKS) - len(failed), len(CHECKS)))
    if failed:
        print("FAILED:")
        for name, _, detail in failed:
            print("  - %s -- %s" % (name, detail))
        print("SMOKE FAIL")
        return 1
    print("SMOKE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
