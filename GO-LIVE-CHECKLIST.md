# GO-LIVE CHECKLIST -- Artispreneur MCP + REST API

Patrick's taps. Nothing here charges or submits anything until he says so.

## Status 2026-11-08 ~00:15 CT — REDEPLOYED, fix is LIVE

- [x] Redeployed: **https://artispreneur-mcp.vercel.app** (project
      `artispreneur-mcp`, scope `gptpat` Hobby, deployment
      `dpl_HUuKmSy1sMpwNpWYJQSCX3XfZy9e`, READY production). Deployed
      via the Vercel MCP connector (connected as gptpat123) — no Drive
      sheet token, no CLI token, no `.ops` script. `MCP_AUTH_TOKEN`
      rotated fresh at redeploy (production, sensitive, via
      `create_project_env` upsert); the token file was shredded after
      verification and the value lives only in the Vercel dashboard.
- [x] Live verification 20/20 PASS (`/tmp/verify_live.py`, run
      2026-11-08): `/health` library 385 / artispreneur 1 active /
      87 draft / agents 7 / packs 4, entitlements `admin-only`;
      no-auth `POST /mcp` 401; demo-free and demo-all-access 401;
      initialize 200 + session; tools/list exactly 6 tools;
      list_agents 7; get_agent booking-manager 13 skills; free-taste
      get_skill works; draft skill draft-gated even for admin;
      REST `/api/skills`, `/api/agents`, `/api/packs` 200 with auth,
      401 without. Demo keys are DEAD on the live URL.
- [x] Muse listing refreshed: `~/workspace/artispreneur-muse-listing/`
      `mcp-config.json` + `manifest.yaml` + INTEGRATION.md + README.md
      now point at `https://artispreneur-mcp.vercel.app/mcp`.
      No muse.ai/platform submission (still Patrick's tap).
- [ ] **STILL OPEN — rotate the exposed Vercel token:** the `vercel - all`
      token (user gptpat123-3709) appeared in full in a `ps` listing
      captured in tool output during a hung `vercel env pull`. Revoke /
      rotate it in the Vercel dashboard. Never use `vercel env pull`
      in this VM again (it prompts interactively and hangs).

## His taps (in order)

0. **Fresh Vercel token (was the BLOCKER — RESOLVED 2026-11-08)** --
   the Drive api-keys sheet (`1fExgj11...`) is gone (404, not in
   trash). Patrick connected the Vercel MCP (OAuth) as gptpat123
   instead; the redeploy ran through the connector with Patrick
   present to approve the env/deploy cards. Do NOT use the
   `~/workspace/.ops/redeploy-and-verify.sh` Drive-sheet path again.
0b. **Vercel billing (artispreneur team)** -- the `artispreneur` Pro
   team is suspended ("add a valid payment method"). The deploy went
   to `gptpat` (Hobby) instead. If Artispreneur hosting should live
   under the artispreneur team, reactivate billing there first.

## His taps (in order)

1. **Real `MCP_AUTH_TOKEN`** -- DONE, rotated at the 2026-11-08
   redeploy: generated fresh (`openssl rand -hex 32`), set via the
   Vercel connector (production, sensitive), never printed or
   committed. Patrick can copy it from Vercel dashboard >
   artispreneur-mcp > Settings > Environment Variables to paste into
   Muse's Secure Credentials Store. (The token generated for the
   failed 23:14 CT rotation appeared in a timeout traceback, was
   shredded, never set, and must NEVER be used.)
2. **Vercel deploy** -- DONE (fix redeployed 2026-11-08, deployment
   `dpl_HUuKmSy1sMpwNpWYJQSCX3XfZy9e`, READY). Live verified 20/20:
   `GET /health` library 385 / artispreneur 1 active / 87 draft /
   agents 7 / packs 4 with entitlements `admin-only`, demo keys 401,
   admin token returns the 6 tools.
3. **Supabase `has_access()` replacing demo entitlements** -- before ANY
   per-customer key is issued: replace the `entitlements.json` lookup in
   `api/_core.py` with `public.has_access(uid, product_id)` + the Supabase
   `usage_ledger` table (mirror
   `~/workspace/salesgency-platform-backend/supabase/schema.sql`). The demo
   file must never be deployed as-shipped; it is excluded from
   `vercel.json` includeFiles, the Dockerfile, `.dockerignore` and
   `.gitignore` on purpose.
4. **Stripe prices + webhook** -- create the 4 Artispreneur prices
   (Free $0 / All-Access $20/mo / Pro $200/mo / Label $25/seat/mo) and the
   webhook that grants/revokes entitlements on checkout/cancel. Until then
   every pack carries `stripe_status: "not_live_in_this_package"` and no
   customer is charged by this server.
5. **License text** -- confirm the license for the served skill content
   (same open question as the skill-co / Muse listing packs: 'Proprietary -
   Diamitani Industries' unconfirmed).
6. **Directory submission (NOT done)** -- `muse.ai` / platform directory
   listing for this MCP server, after 1-5 are live and the 87 draft music
   skills question is settled (draft bodies are never served; a listing
   should say so plainly).

## Pre-launch re-checks (agent runs, no tap needed)

- Re-run `python3 test_smoke.py` (expect 78/78, SMOKE PASS) and
  `python3 scripts/build_music_catalog.py` (expect 88 / 1 active / 87 draft)
  after any data change.
- The smoke suite now includes a Vercel-simulation block (boots with
  `VERCEL=1` and the demo file present): admin-only auth must hold and
  demo keys must 401. The old copy-without-the-file simulation is
  superseded — it missed the real failure mode.
- Docker build (not run yet -- no docker in this VM) before any container
  deploy: `docker build -t artispreneur-mcp .` then run with an admin token
  and hit `/health`.

## Known gaps (do not paper over)

- The 87 draft music skills are metadata-only by design; only
  `pro-registration` is active. Activating more is a content-review
  decision, not a code change.
- Free-tier metering on Vercel is best-effort (`/tmp` ledger, ephemeral)
  until the Supabase ledger lands (tap 3).
- `grok-social-cleanup` (#385) was audited 2026-11-07 (frontmatter valid, no
  secrets, keys are `{{XAI_API_KEY}}` / `{{OPENROUTER_API_KEY}}`
  placeholders). Removals require Patrick's explicit approval.
