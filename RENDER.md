# Render deploy — Artispreneur MCP (primary host)

## Why Render, not Vercel

Root cause: `GET /mcp` returned 405 on Vercel serverless because a
serverless function cannot hold the long-lived SSE stream (or the session)
that strict MCP clients open first. Vercel Python streaming is documented
for ASGI/WSGI apps, not for this stdlib `BaseHTTPRequestHandler` package,
and sessions are in-process so a GET in a fresh invocation cannot see the
POST's session anyway. The Vercel function now returns a bounded SSE
stream (200, pings every 5s for up to 20s, then clean close) instead of
405, but that is best-effort: whether Vercel flushes the stream live is
unproven without a deploy, and the stream still ends after 20s. A
long-running Docker service on Render holds the stream open indefinitely
(`server.py`: 25s ping loop, real sessions) — that is what Muse and other
strict clients need. Evidence: real MCP client handshake 16/16 PASS
locally against `server.py`, including GET /mcp SSE 200 + ping.

Vercel (https://artispreneur-mcp.vercel.app) stays live as a fallback;
its POST /mcp still works and its GET /mcp is no longer a 405.

## What to do in the Render dashboard (Patrick's tap)

1. **Create the GitHub repo first** (does not exist yet, checked
   2026-11-08 via the GitHub connector, signed in as diamitani):
   `diamitani/artispreneur-mcp`, private. Push this directory as the repo
   root (`git init`, add, commit, `git remote add origin
   git@github.com:diamitani/artispreneur-mcp.git`, `git push -u origin main`).
   Do NOT push to any other repo, and never move another repo's main.
2. Render dashboard (https://dashboard.render.com) > **New > Blueprint** >
   connect the `diamitani/artispreneur-mcp` repo. Render reads
   `render.yaml` from the repo root: service `artispreneur-mcp`, Docker,
   health check `/health`.
3. When prompted for environment variables, set:
   - `MCP_AUTH_TOKEN` — generate a fresh random token (32+ chars, e.g.
     `openssl rand -hex 32`). This is the ONLY credential the production
     server trusts. Never reuse the Vercel token or any demo key.
     Never commit it; set it in the dashboard only.
   - `BASE_URL` — leave blank on the first deploy, then set it to the
     Render URL (expected `https://artispreneur-mcp.onrender.com`) and
     redeploy once, so the landing page links correctly.
   - `HOST` is already `0.0.0.0` in render.yaml. `PORT` is injected by
     Render; do not set it.
4. Deploy. First deploy takes a few minutes (python:3.12-slim, no pip
   installs — stdlib only).
5. Verify (from any terminal):
   - `curl https://artispreneur-mcp.onrender.com/` → HTML landing page.
   - `curl https://artispreneur-mcp.onrender.com/health` → JSON, 385 / 1
     active / 87 draft / 7 agents / 4 packs.
   - `curl -i https://artispreneur-mcp.onrender.com/mcp` (no auth) → 401.
   - `curl -N -H "Authorization: Bearer <MCP_AUTH_TOKEN>" \
     https://artispreneur-mcp.onrender.com/mcp` → `text/event-stream`
     with `: ping` lines (note: this opens a stream with no session, so
     the server mints one and returns it in the `Mcp-Session-Id` header).
6. **Rotate the Vercel token afterwards? No** — the Vercel deployment
   keeps its own `MCP_AUTH_TOKEN` env var; the Render token is separate.
   Keep both secret. The old exposed Vercel token
   (user gptpat123-3709, captured in a `ps` listing) still needs revoking
   in the Vercel dashboard — unrelated to this deploy.

## What is NOT in the image

- `entitlements.json` (demo keys) is excluded by `.dockerignore` and by
  `vercel.json`. Production auth is `MCP_AUTH_TOKEN` only, until the
  Supabase `has_access()` lookup replaces demo entitlements at go-live
  (see GO-LIVE-CHECKLIST.md).
- No secrets are committed anywhere in this repo. Check with
  `git grep -i token` before pushing; the only token-shaped strings
  should be the words `MCP_AUTH_TOKEN` (the env var name) and test
  fixtures in `test_smoke.py` that are generated fresh per run.

## Free-tier note

Render's free web service spins down after inactivity and takes ~30–60s
to wake on the first request. That is a cold-start delay, not an error —
Muse will retry or the user waits once. If wake latency becomes a
problem, the fix is Render's paid instance type, not a code change.
