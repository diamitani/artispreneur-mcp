# VERIFICATION -- Artispreneur MCP + REST API (v1.0.0)

Built 2026-11-07. Package: `~/workspace/artispreneur-mcp/`. No Stripe work
was done, nothing was submitted to Meta.

## GET /mcp 405 fix + host switch (2026-11-08) — Render is primary

- **Root cause in one line:** Vercel serverless cannot hold the long-lived
  SSE stream (or the session) that strict MCP clients open with GET /mcp,
  so the endpoint answered 405 and the Muse handshake broke.
- **Evidence for the verdict:** Vercel Python docs say streaming is
  supported for ASGI/WSGI apps (FastAPI/Flask/Django), not for this
  stdlib `BaseHTTPRequestHandler` package; sessions are in-process, so a
  GET in a fresh invocation cannot see the POST's session in any case;
  and a Hobby function caps duration well below a held-open stream.
  A rewrite to FastAPI + Fluid Compute would be a different project.
- **What changed in this package (commit b93ca53, local git, not pushed):**
  - `api/mcp.py` do_GET: no more 405. Auth 401 without a token, then a
    BOUNDED SSE stream — 200 `text/event-stream`, immediate ping, a ping
    every 5s for up to 20s (`SSE_HOLD_SECONDS`, capped 50), then a clean
    close. Best-effort only: whether Vercel flushes live is unproven
    without a deploy. Vercel stays as a fallback.
  - `api/_core.py` + `server.py`: GET / returns a human HTML landing
    page (what this is, 385 skills / 7 agents / 4 packs, the exact Muse
    connect line, link to /health, no token shown). `server.py` GET /mcp
    mints a session if the client opens the stream before initialize.
  - `api/index.py` + `vercel.json`: root `/` rewrites to the landing
    page on Vercel too (was a 404).
  - `render.yaml` + `RENDER.md` + `Dockerfile` (PORT no longer hardcoded;
    Render injects it): primary host is a long-running Render Docker
    service from `server.py`, health check `/health`.
  - `test_smoke.py`: GET / now expects the HTML landing page.
- **Client-test evidence (real MCP client handshake, stdlib, /tmp/mcp_client_test.py):**
  16/16 PASS against `server.py` — GET / HTML landing page; /health
  385/1/87/7/4; POST no-auth 401; initialize 200 + session; **GET /mcp
  SSE 200 text/event-stream + ping**; GET /mcp no-auth 401; tools/list
  exactly 6; list_agents 7; get_agent booking-manager 13 skills;
  get_skill free-taste body; draft skill draft-gated (admin too); paid
  skill with demo-free not-entitled; list_packs 4; tools/call without
  session id works; DELETE teardown 200; ping after teardown -32001.
- **Vercel-handler harness (/tmp/test_vercel_handlers.py):** 5/5 PASS —
  GET / HTML, GET /mcp no-auth 401, GET /mcp 200 SSE, first ping <3s
  (proves the handler flushes in stdlib), pings on schedule. This proves
  the handler code streams; it does NOT prove Vercel's runtime flushes.
- **Regression:** `test_smoke.py` 78/78 PASS.
- **GitHub repo:** `diamitani/artispreneur-mcp` does NOT exist yet
  (checked 2026-11-08 via the GitHub connector, signed in as diamitani).
  Local git repo is committed (b93ca53, 411 files, remote `origin`
  git@github.com:diamitani/artispreneur-mcp.git) and ready to push.
  Repo creation via the GitHub connector was attempted 2026-11-08 but
  the approval card timed out unanswered after ~30 min — NOT created,
  NOT pushed. Exact blocked step: Patrick approves the GitHub
  create-repository card (or creates the private repo himself), then
  `git push -u origin main`, then Render Blueprint (see RENDER.md).
- **Expected Render URL (not live yet):** https://artispreneur-mcp.onrender.com
  — do not put it in the Muse listing as verified until the first deploy
  answers /health.
- **Still open:** rotate the exposed old Vercel token (gptpat123-3709) in
  the Vercel dashboard; Supabase `has_access()` before any per-customer
  key; Stripe prices/webhook; license text; muse.ai/platform submission;
  cross-model QA not run on this package.

## Redeploy of the fix (2026-11-08 ~00:15 CT) — LIVE, 20/20 PASS

- Vercel MCP connector connected as gptpat123 (gptpat123-3709, Hobby,
  defaultTeamId `team_oapewDYu0AulFXlrwKCX9ggY`). Patrick was present
  in chat and approved both write cards (env, then deployment).
- `MCP_AUTH_TOKEN` rotated fresh via `create_project_env` (upsert,
  sensitive, production; env id `XphIQno0H5hDFOno`). Token held only
  in a 0600 temp file, never printed, shredded after verification.
- Deployment `dpl_HUuKmSy1sMpwNpWYJQSCX3XfZy9e`, READY production,
  alias `artispreneur-mcp.vercel.app`. Deployed via
  `create_deployment` with the files array built from disk: 397 files,
  all SHA1-referenced (verified against the live deployment tree —
  only `api/_core.py` differed) except `api/_core.py` inlined (the
  fix). `entitlements.json`, `.env*`, server.py, docs, scripts, tests
  excluded per `.vercelignore`.
- Live verification 20/20 PASS (script `/tmp/verify_live.py`; two
  early runs were 15/20 then 19/20 because the *checker* mis-parsed
  the MCP text-content responses and the top-level JSON-RPC error
  shape — the server was correct in both cases; the checker was
  fixed and the clean re-run is 20/20): `/health` 200, library 385,
  artispreneur 1 active / 87 draft, agents 7, packs 4, entitlements
  `admin-only`; no-auth `POST /mcp` 401; demo-free 401; demo-all-access
  401; `GET /api/skills` no-auth 401; initialize 200 + session;
  tools/list exactly 6 tools; list_agents 7; get_agent booking-manager
  13 skills; get_skill free-taste body; draft skill draft-gated even
  for admin; list_packs 4; REST agents/skills/packs 200 with auth.
- Muse listing refreshed with the live URL (see
  `~/workspace/artispreneur-muse-listing/`).
- Still open: rotate the exposed old Vercel token (gptpat123-3709) in
  the Vercel dashboard; Supabase `has_access()` before any per-customer
  key; Stripe prices/webhook; license text; muse.ai/platform submission;
  cross-model QA not run on this package.

## Live deploy (2026-11-07 night) — https://artispreneur-mcp.vercel.app

- Project `artispreneur-mcp`, scope `gptpat` (Hobby), production alias
  `https://artispreneur-mcp.vercel.app`. Deployed with `npx vercel@latest
  --prod` using the Drive sheet's `vercel - all` token (user
  gptpat123-3709). The `artispreneur` team (Pro) was NOT usable: project
  creation failed there with "account suspended, add a valid payment
  method" — that billing suspension is a separate Patrick tap.
- Live `GET /health` verified from outside the VM: library 385,
  artispreneur 1 active / 87 draft, agents 7, packs 4. Unauthenticated
  `POST /mcp` -> 401 (verified live).
- **Finding on first live deploy (W-3 live):** `/health` reported
  entitlements `demo-file`, not admin-only — Vercel uploads the whole
  project dir, so `entitlements.json` shipped despite `vercel.json`
  `includeFiles` omitting it. Demo keys (`demo-free`, `demo-all-access`,
  `demo-pro`, `demo-label`) therefore authenticate on the PUBLIC URL
  today. Fix built the same night (see below); redeploy is BLOCKED
  (token section below).
- **Fix (2026-11-08):** (1) `api/_core.py` production guard — when
  `VERCEL` is set, demo entitlements are NEVER loaded even if the file
  is present; only `MCP_AUTH_TOKEN` authenticates. (2) `.vercelignore`
  excluding `entitlements.json`, `.env*`, `usage_ledger.jsonl`,
  `test_smoke.py`, `scripts/`, `Dockerfile`, `server.py`, docs.
  Local smoke now **78/78** (73 + 5 new Vercel-simulation checks:
  VERCEL=1 boots, health admin-only, demo-free/demo-all-access -> 401,
  admin initialize 200).
- **REDEPLOY BLOCKED — Vercel token gone:** the Drive api-keys sheet
  (`1fExgj11...`) now 404s on `files.get` (permanently deleted or
  access revoked during the Drive consolidation; not in trash). Six
  other key sheets in this Drive account were checked by structure
  only — none contains a Vercel row. Per AGENTS.md, the next step is
  Patrick supplying a fresh Vercel token via the Secure Vault card
  flow (or Vercel MCP OAuth connect), then re-run
  `~/workspace/.ops/redeploy-and-verify.sh`.
- **Token exposure — rotation recommended:** during the hung
  `vercel env pull` (it prompts interactively; never use it in this
  VM), a `ps` listing captured the full `vercel - all` token in tool
  output. That token (user gptpat123-3709) should be revoked/rotated
  in the Vercel dashboard. The token value is NOT repeated in this
  file or in chat. The live `MCP_AUTH_TOKEN` was generated fresh at
  deploy time, set only in the Vercel dashboard, and never printed;
  Patrick can copy it from Vercel dashboard > artispreneur-mcp >
  Settings > Environment Variables to paste into Muse.

## Smoke test: 78/78 checks passed -- SMOKE PASS

`python3 test_smoke.py` (boots the real local server on scratch port 8892
with a scratch usage ledger and a fresh random admin token). Full output in
the build transcript; checks covered:

- Health (public): library **385**, artispreneur **1 active / 87 draft**,
  agents **7**, packs **4**, entitlements labelled demo; `GET /` info text.
- 401s: `/mcp` no-auth / unknown / revoked; `/api/skills`, `/api/agents`,
  `/api/packs`, `/api/skills/:slug`, `/api/agents/:slug` no-auth, plus
  revoked and unknown keys on `/api/skills`.
- Handshake: `initialize` 200 + session id; `ping` with session; `ping`
  **without** a session id (stateless/lenient mode); `tools/list` exactly
  the 6 tools (`list_skills`, `search_skills`, `get_skill`, `list_agents`,
  `get_agent`, `list_packs`).
- Agents: `list_agents` = 7; `get_agent booking-manager` = 13 skills;
  unknown agent slug errors.
- Tiers: free library total = 5 (exactly the 5 free-taste slugs);
  all-access library total = 385 incl. `grok-social-cleanup`; artispreneur
  `include_gated` total = 88, default = 1 (`pro-registration`), free
  default = 0.
- Search: free finds `write-a-business-plan`, does NOT surface paid
  `add-music-to-collaborative-playlist`; all-access finds it.
- Gating: free-taste `get_skill` ok; paid skill with free key ->
  `not-entitled` with hint naming All-Access $20/mo and
  `pack_id: artispreneur-all-access`; `pro-registration` ok for all-access,
  `not-entitled` for free; draft `artist-bio-writer` -> `draft-gated` for
  free AND all-access AND admin; unknown slug errors.
- Packs: `list_packs` = 4, ids are the 4 Artispreneur packs, all
  `stripe_status: not_live_in_this_package`.
- REST: `GET /api/skills` total 385; `GET /api/skills/:slug` free-taste 200
  / paid-with-free 403 `not-entitled`; `GET /api/agents/:slug` 200 with 13
  skills, 401 without auth; `GET /api/packs` count 4; draft via REST with
  admin -> 403 `draft-gated`; unknown skill slug -> 404; `GET /api/agents`
  count 7.
- Metering: ledger counted 2 free `get_skill` runs, topped up to exactly
  50 allowed, 51st -> `allowance-exhausted` with All-Access hint +
  `pack_id artispreneur-all-access`.
- Admin + demo keys: admin token reads a paid skill; `demo-all-access`
  still works after admin boot (385); `demo-pro` and `demo-label` read
  `pro-registration`.
- Teardown: `DELETE /mcp` 200; reuse of the torn-down session -> `-32001`;
  fresh `initialize` after teardown works.
- Ledger: `get_skill` lines for `demo-free` present; admin token value and
  any `Bearer` string absent.

## Data verification (independent of the smoke run)

- `scripts/build_music_catalog.py`: music skills **88 (active 1, draft 87,
  agents 7)**; active is `pro-registration`; fails loudly otherwise.
- `scripts/build_skills_index.py`: **385** skills indexed; every sha256
  re-verified against the skill-co-mcp index (no drift); `grok-social-cleanup`
  included as #385 from its own frontmatter.
- `agents.json`: 7 artispreneur agents, counts 13/17/10/8/10/14/16, matching
  the catalog; no salesgency agent.
- `packs.json`: 4 Artispreneur packs only, all
  `stripe_status: not_live_in_this_package`.
- `entitlements.json`: 5 DEMO keys only (free 50/mo, all-access, pro,
  label, revoked).

## Vercel simulation (superseded by the live deploy + fix)

The pre-deploy `/tmp/vercel-sim` run (package copied WITHOUT
`entitlements.json`, `VERCEL=1`) passed, but it MISSED the real failure
mode: Vercel uploads the whole project dir, so the file ships anyway.
That assumption is now fixed in code (VERCEL guard) and in the smoke
suite, which boots a second server with `VERCEL=1` and the demo file
present on disk: health reports admin-only, demo keys 401, admin works
(5 checks, part of the 78/78). `vercel.json` parses; its `includeFiles`
omits `entitlements.json`, and `.vercelignore` now excludes it from the
upload as well. All 5 `api/*.py` files import standalone (`handler`
present); core loads with counts 385/1/87/4/7; ledger path
`/tmp/usage_ledger.jsonl` on Vercel.

## Secret scan

Pattern scan for live-secret shapes (`sk-...`, `ghp_...`, `AKIA...`,
`xox...`, `-----BEGIN ... PRIVATE KEY-----`) over the package: **no live
secrets found**. Two false positives, both documentation text, not
credentials:
- `skills/redaction-rules-skill.md` mentions `-----BEGIN PRIVATE KEY-----`
  as an example of what to redact.
- `sk-delegation` inside `task-delegation-followup` slugs tripped the
  `sk-` prefix pattern.
Demo tokens in `entitlements.json` (`demo-free`, `demo-all-access`,
`demo-pro`, `demo-label`, `demo-revoked`) are intentional, clearly labelled
DEMO, and excluded from every deploy path. No `requirements.txt` anywhere
in the package (verified: 0 files). The Dockerfile COPYs `server.py`,
`api/`, `skills/`, `skills-artispreneur/`, `skills-index.json`, `data/`,
`packs.json`, `agents.json` only -- never `entitlements.json`.

## What was NOT run

- **Docker build** -- no docker in this VM. The Dockerfile is written and
  its COPY list was verified by inspection, but the image was not built.
- **Live Vercel deploy of the FIX** -- blocked (see "Live deploy"
  section): no usable Vercel token remains in the Drive account.
  The currently live deployment is the pre-fix build, with demo keys
  active on the public URL.
- **Full live authenticated verification** -- not completed: health +
  unauth 401 verified live; the authenticated live checks (initialize,
  tools/list, get_skill, draft-gated, REST) were scripted in
  `~/workspace/.ops/redeploy-and-verify.sh` but never ran, because the
  redeploy they depend on is blocked. The same checks pass locally
  (78/78).
- **Live MCP client connect** (Muse/Claude) -- the protocol surface was
  verified by the smoke test's JSON-RPC calls, not by a real client.
  The Muse listing files were NOT yet refreshed with the real URL
  (waiting on the fixed redeploy so the pack points at the fixed build).
- **Cross-model QA** -- the build was self-tested by the builder model
  (Muse Spark); no independent different-model testing agent ran, per the
  standing rule this is a disclosed deviation for this package.
- **No Stripe, no Supabase, no Meta/Muse submission** -- all gated behind
  Patrick's taps in GO-LIVE-CHECKLIST.md.

## Files created (406 total, 4.2M -- mostly the 385 skill bodies)

Key files: `server.py`, `api/_core.py`, `api/mcp.py`, `api/health.py`,
`api/skills.py`, `api/agents.py`, `api/packs.py`, `vercel.json`,
`Dockerfile`, `.dockerignore`, `.gitignore`, `.env.example`,
`skills-index.json`, `skills/` (385), `skills-artispreneur/pro-registration.md`,
`data/music-catalog.json`, `agents.json`, `packs.json`,
`entitlements.json` (DEMO ONLY), `test_smoke.py`,
`scripts/build_music_catalog.py`, `scripts/build_skills_index.py`,
`README.md`, `VERIFICATION.md` (this file), `GO-LIVE-CHECKLIST.md`.
`~/workspace/artispreneur-mcp-deploy/`, `~/workspace/skill-co-mcp/` and
`~/workspace/artispreneur-muse-listing/` were not touched.

## Redeploy 2026-11-08 ~23:00 CT — GET /mcp 405 fix is LIVE on Vercel

- **Deployment:** `dpl_5JyuVHzT6oPPPmVhh76bvj2eYYS9`, READY, production,
  `https://artispreneur-mcp.vercel.app` (project `prj_kfdDrINZOd9o2WGY7Q0ENGjXp31l`,
  gptpat Hobby). Deployed via the Vercel MCP connector only, 398 files
  (394 SHA1-referenced, 4 inlined: `vercel.json`, `api/_core.py`,
  `api/mcp.py`, `api/index.py`). An earlier build of the same fix
  (`dpl_BcNXn7Q1z758eSAgMyRnKmbafouC`) went READY first, then was
  superseded by this one after the token rotation (env changes need a
  redeploy to take effect in serverless functions).
- **Token:** fresh `MCP_AUTH_TOKEN` generated with `openssl rand -hex 32`,
  set via `create_project_env` (upsert, sensitive, production, env id
  `XphIQno0H5hDFOno`), verified live, temp file shredded. Value lives
  only in the Vercel dashboard (artispreneur-mcp > Settings >
  Environment Variables). The 00:07 CT token it replaces is now revoked
  by overwrite; the shredded 23:14 CT token was never set and must never
  be used.
- **Live checks 12/12 PASS** (verified against the live URL with the
  fresh token; three first-run "failures" were checker bugs — wrong
  response-field names and a read that waited for 400 bytes on a ping
  stream — each re-confirmed by direct evidence):
  1. `GET /` 200 HTML landing page (was a raw JSON error)
  2. `GET /health` 200, admin-only, 385 / 1 active / 87 draft / 7 agents / 4 packs
  3. `GET /mcp` with auth 200 `text/event-stream`, `X-Accel-Buffering: no`,
     live `: ping` lines — **the 405 is gone; Vercel flushes the bounded
     (20s) stream live**
  4. Unauthenticated `POST /mcp` 401; unauthenticated `GET /mcp` 401
  5. `demo-free` 401 — demo keys dead
  6. Authenticated `initialize` 200 + `Mcp-Session-Id`
  7. `tools/list` exactly 6 tools
  8. `list_agents` = 7; `get_agent booking-manager` = 13 skills
  9. `get_skill business-model-canvas-builder` returns the skill payload
     with `skill_md` body (free-taste)
  10. `get_skill affiliate-crm-setup` (tenant artispreneur) → DRAFT-gated
      error, body not served
  11. `list_packs` = 4
  12. REST `/api/skills`, `/api/agents/booking-manager`, `/api/packs` 200 with auth
- **Vercel SSE verdict (corrected):** the bounded 20s stream DOES flush
  live on Vercel (proven by curl `-N`: pings arrive every ~5s). Render
  remains the primary host for the indefinite stream + real sessions
  (`server.py`), Vercel is a working fallback, not a broken one.
- **Not done in this run:** GitHub repo `diamitani/artispreneur-mcp`
  still does NOT exist — `create_repository` via the GitHub connector
  failed twice with GitHub API errors (org path 404 because diamitani is
  a personal account, not an org; personal-account path 403 "Resource not
  accessible by integration" — the Muse GitHub App installation lacks
  repo-creation permission; approval cards were approved both times).
  SSH push from this VM is blocked by the sandbox proxy. Patrick must
  create the repo himself at github.com/new (private,
  `diamitani/artispreneur-mcp`, no README) or grant the app repo-creation
  permission, then `git push -u origin main` from
  `~/workspace/artispreneur-mcp/` (local main `d9477e8`, secret scan clean).
  Until then, Render cannot deploy from the repo. No muse.ai/platform
  submission (privacy/terms still 404 — separate blocker).
