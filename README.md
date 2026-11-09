# Artispreneur MCP + REST API

One endpoint for the Artispreneur skill library and music layer, served two
ways: as MCP tools (Muse / Claude / any Streamable-HTTP MCP client) and as a
plain REST API. **Artispreneur only** -- no salesgency tenant, no skill-co
tenant. Stdlib only, no `requirements.txt`, no pip installs.

## What is live / gated / draft

| Surface | State |
| --- | --- |
| 385-skill library (384 audited + `grok-social-cleanup` #385) | **Live** for entitled tiers; free keys read only the 5 free-taste skills |
| Music skill `pro-registration` | **Live** (the one active music skill) for All-Access / Pro / Label / admin |
| Other 87 music skills | **Draft** -- metadata only in list/search (`include_gated=true`); bodies are **never** served to any tier, including admin |
| 7 music agents (booking, brand, day-to-day, finance, legal, PR, publishing) | **Directory only** -- listed, never executed by this server |
| 4 packs: Free $0, All-Access $20/mo, Pro $200/mo, Label $25/seat/mo | **Metadata only** -- `stripe_status: "not_live_in_this_package"`; Stripe is not live here |
| Per-key entitlements | **Demo file only** (`entitlements.json`) for local smoke tests; production must replace it with the Supabase `has_access()` lookup (see GO-LIVE-CHECKLIST.md) |

Free taste (any valid key, no purchase): `business-model-canvas-builder`,
`create-content-calendar`, `email-architect`, `technical-writing-pro`,
`write-a-business-plan` -- plus 50 `get_skill` runs/month, then
`allowance-exhausted` with an upgrade hint naming **All-Access $20/mo**
(`pack_id: artispreneur-all-access`).

## Run locally

```bash
python3 server.py
# Serving Artispreneur MCP on http://127.0.0.1:8787/mcp
```

`HOST` defaults to `127.0.0.1` (never `0.0.0.0` by default); `PORT` env,
default `8787`. Copy `.env.example` to `.env` for local runs if you want an
admin token; never commit a real value.

Smoke test (boots the server on a scratch port with a scratch ledger):

```bash
python3 test_smoke.py   # 73/73 checks passed, SMOKE PASS (2026-11-07)
```

## MCP tools -- exactly 6, never one per skill

`list_skills`, `search_skills`, `get_skill`, `list_agents`, `get_agent`,
`list_packs`. `get_agent` returns one agent by slug with its skill list and
status.

Connect in Muse / Claude / any MCP client (Streamable HTTP):

- URL: `http://127.0.0.1:8787/mcp` (local) or your deployed `/mcp`
- Header: `Authorization: Bearer <your key>`
- `initialize` returns a `Mcp-Session-Id`; send it back on later calls.
  The server is **lenient/stateless**: `tools/call` also accepts a missing
  or unknown session id (auth is the Bearer token, not the session), so
  serverless deployments work. Only a session explicitly torn down with
  `DELETE /mcp` is rejected (`-32001`).

## REST API -- same auth + gating as MCP

401 without a valid Bearer token on every `/api` route except `/health`.

| Route | Notes |
| --- | --- |
| `GET /health` | Public. Counts only, no secrets |
| `GET /` | Public info text |
| `GET /api/skills?tenant=&query=&category=&page=&per_page=&include_gated=` | Same shape as `list_skills` |
| `GET /api/skills/:slug?tenant=` | One skill body; 403 gated, 404 unknown |
| `GET /api/agents` | The 7 music agents |
| `GET /api/agents/:slug` | One agent; 404 unknown |
| `GET /api/packs` | The 4 Artispreneur packs |

## Vercel deploy notes

- `vercel.json` rewrites `/mcp -> /api/mcp`, `/health -> /api/health`,
  `/api/skills/:slug -> /api/skills?slug=:slug`,
  `/api/agents/:slug -> /api/agents?slug=:slug`, and bundles the data files
  into each function via `includeFiles` (`skills/**`,
  `skills-artispreneur/**`, `data/**`, `skills-index.json`, `packs.json`,
  `agents.json`, `api/_core.py`). `entitlements.json` and
  `usage_ledger.jsonl` are **deliberately excluded**.
- Each `api/*.py` is a thin `class handler(BaseHTTPRequestHandler)` wrapper
  over `api/_core.py` (all logic lives there, shared with the local
  runner). No `requirements.txt` anywhere in the package.
- **Stateless sessions:** serverless functions cannot hold sessions or SSE
  across invocations. `initialize` returns a session id, but `tools/call`
  accepts a missing or unknown session id -- never 401 on session alone.
- **GET /mcp returns 405 on Vercel** (SSE keep-alive is not supported on
  serverless; POST is the transport). The local runner still serves the
  SSE keep-alive loop.
- **Usage ledger defaults to `/tmp/usage_ledger.jsonl` when `VERCEL` is
  set** (the serverless filesystem is ephemeral, so metering there is
  best-effort). Ledger writes never fail a call (`try/except OSError`).
- **If `entitlements.json` is absent at runtime** (it will be on Vercel),
  zero demo keys load and the server relies on the `MCP_AUTH_TOKEN` admin
  key only. It does **not** crash; `/health` still reports counts and its
  `entitlements` field reads `admin-only (no demo entitlements file
  present)`. Demo keys 401 on Vercel until the Supabase lookup lands.
- Set the real `MCP_AUTH_TOKEN` in the Vercel dashboard
  (Settings > Environment Variables). Never commit a token.

## Docker

```bash
docker build -t artispreneur-mcp .
docker run -p 8787:8787 -e MCP_AUTH_TOKEN=<admin-token> artispreneur-mcp
```

The Dockerfile sets `ENV HOST=0.0.0.0` explicitly inside the container
only, and never copies `entitlements.json` (also excluded in
`.dockerignore` / `.gitignore`, with `.env` and `usage_ledger.jsonl`).

## Layout

```
server.py                 local runner (http.server ThreadingHTTPServer)
api/_core.py              ALL logic: data load, auth, gating, metering,
                          MCP dispatch, REST handlers (no http.server import)
api/mcp.py api/health.py  Vercel functions (thin wrappers over _core)
api/skills.py api/agents.py api/packs.py
vercel.json               rewrites + includeFiles (NOT entitlements.json)
skills/                   385 SKILL.md bodies (skills/<slug>.md)
skills-index.json         rebuilt from disk (slug, name, description,
                          category, sha256) -- see scripts/build_skills_index.py
skills-artispreneur/      pro-registration.md ONLY (the one active skill)
data/music-catalog.json   regenerated from artispreneur-music-layer/catalog.yaml
                          (88 skills, 1 active, 87 draft) -- see scripts/
agents.json               the 7 music agents (directory only)
packs.json                the 4 Artispreneur packs
entitlements.json         DEMO ONLY keys -- local smoke only, never deployed
test_smoke.py             73-check smoke suite (local server, scratch ledger)
scripts/                  build_music_catalog.py, build_skills_index.py
```

Rebuild data from sources (both fail loudly on drift):

```bash
python3 scripts/build_music_catalog.py   # expects 88 skills, 1 active
python3 scripts/build_skills_index.py   # expects 385 skills, sha256-verified
```

## Auth model (summary)

Two Bearer layers, constant-time compare (`hmac.compare_digest`):
`MCP_AUTH_TOKEN` env = admin (`key_id "admin"`, full access), and per-key
entitlements in `entitlements.json` (demo only). Unknown or revoked token
-> 401. Metering: `get_skill` calls append `{key_id, tool, tenant, slug,
allowed, reason}` to `usage_ledger.jsonl` -- key_id only, no tokens, no
PII. Free tier: 50 runs/month.

## What this package does NOT do

No Stripe (prices/webhook not live), no deploy, no Meta/Muse directory
submission, no agent loops (agents are a directory), no real customer keys.
See `GO-LIVE-CHECKLIST.md` for Patrick's taps and `VERIFICATION.md` for
what was and was not run.
