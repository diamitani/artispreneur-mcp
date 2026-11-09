---
name: n8n-engineer
version: "1.1.0"
description: "Builds, debugs, scales, and architects n8n workflows like a systems engineer — official patterns for instance-level MCP, MCP Server Trigger, MCP Client Tool, Call-n8n-Workflow, HTTP Request, and AI agents; an architecture decision order; build patterns (native node → HTTP Request → community node); a revenue-focused GTM mode; and five node-by-node Salesgency build templates (outreach, prospect mining, CRM hygiene, inbound responder, deliverability/DNS) as follow-me build contracts. Use when the user wants to build, debug, scale, or architect n8n workflows, ai agents, mcp server/client setups, http/api integrations, community nodes, or gtm automations."
---

# n8n Engineer

Use this skill when the task is about building or operating n8n like a systems engineer, not just sketching ideas. Treat n8n as both an automation fabric and an agent runtime. Optimize for revenue impact, operator clarity, and safe execution.

Read these references only when relevant:
- `references/architecture.md` for deciding between instance-level MCP, MCP Server Trigger, MCP Client Tool, sub-workflows, native nodes, HTTP Request, and custom nodes
- `references/agents.md` for AI Agent patterns, tool design, human review, fallbacks, and evaluations
- `references/http-api.md` for REST/API integrations, auth, pagination, batching, and the n8n API
- `references/hard-nodes.md` for common traps in Loop Over Items, Merge, Code, AI sub-nodes, and sub-workflows
- `references/gtm.md` for sales and GTM workflow patterns that create pipeline movement instead of busywork
- `references/ops.md` for scaling, error workflows, monitoring, rollout, and rollback
- `references/starter-pack.md` for the bundled workflow starter pack and how to use it
- `references/sources.md` for the official source index and URLs

## Operating stance

1. Prefer official n8n capabilities before workarounds.
2. Design from the business event backward: trigger, data contract, transformations, decisions, actions, observability.
3. Default to reusable sub-workflows for repeated business capabilities.
4. Never invent node parameters, API endpoints, or MCP behavior.
5. Never hardcode secrets in workflows or skill files.
6. For GTM automation, bias toward precision, enrichment quality, routing discipline, and human review before high-impact outbound actions.
7. Be explicit about what is implemented live, what is a JSON or workflow spec, and what still needs credentials, environment access, or human approval.

## Architecture decision order

1. Decide if the user needs:
- external AI clients to discover and run workflows
- a single workflow exposed as a crafted tool server
- n8n agents consuming external MCP tools
- ordinary automation without MCP
2. Choose the integration surface:
- instance-level MCP for one secure connection to many approved workflows
- MCP Server Trigger for a purpose-built MCP server inside one workflow
- MCP Client Tool when an n8n AI Agent should call external MCP tools
- Call n8n Workflow Tool or Execute Sub-workflow for reusable internal capabilities
- native app node when it supports the needed operation cleanly
- HTTP Request when the API operation exists but the node is incomplete or absent
- a custom community node only when reuse, auth complexity, or UX justify the investment
3. Define the contract:
- trigger and input schema
- normalization layer
- business logic
- tool and action layer
- logging and error path
- operator escalation path
4. For agentic workflows, define:
- system goal
- tool descriptions
- allowed write actions
- human review gates
- evaluation dataset
- rollback plan

## MCP rules

- Recommend instance-level MCP as the default control plane when the user wants Claude, Cursor, ChatGPT, Lovable, or similar clients to search and run multiple approved workflows across one n8n instance.
- Recommend MCP Server Trigger when the user wants a narrow, intentionally designed MCP surface from one workflow.
- Tell users that instance-level MCP is for discovering and running enabled workflows, not authoring or editing workflows.
- Remember that instance-level MCP is not per-client scoped: any connected client can see every workflow enabled for MCP access.
- For MCP Server Trigger, expose the smallest useful tool set. Prefer custom workflow tools and purpose-built sub-workflows over giant do-everything tools.
- When building AI inside n8n, use MCP Client Tool to reach external MCP servers and choose only the tools the agent actually needs.

## Build patterns

- Native node first: best when the operation already exists and credential UX matters.
- HTTP Request second: best for unsupported operations on a known API, or when a credential type already exists in n8n.
- Custom community node third: best when the same integration pattern will be reused heavily, needs better ergonomics, or requires a true trigger or non-REST behavior.
- Sub-workflow by default for shared business capabilities such as enrichment, account research, outbound drafting, CRM writeback, approvals, or meeting prep.
- AI Agent only when tool selection, reasoning, or adaptive paths create real value. Use deterministic branches for straightforward routing and CRUD.

## GTM mode

- Focus on workflows that create meetings, unblock deals, shorten rep research time, improve follow-up speed, and preserve CRM truth.
- Separate read-heavy research from write-heavy execution.
- Gate writes to CRM, email, sequencing, billing, or legal systems with confidence thresholds or human review.
- Prefer this shape for revenue workflows:
  `signal -> enrich -> qualify -> personalize -> approve -> send or route -> log -> follow-up -> feedback loop`
- If a workflow cannot clearly improve speed, conversion, coverage, or data quality, trim it.

## Per-product build templates

Five Salesgency products ship as canonical n8n build patterns. Each spec is a build
contract: follow it node-for-node before adding flair. Parameter names shown are real
n8n node parameters; never invent parameters a node type does not expose.

### Template 1 — Outreach automation (multi-channel cold outreach engine)

- **Objective:** turn an approved prospect signal into a reviewed, send-ready cold
  email without ever auto-sending on first touch.
- **Trigger:** Webhook POST `prospect-intake` (`responseMode: onReceived`) with a
  prospect payload, or a Schedule trigger sweeping a qualified list.
- **Node-by-node plan:**
  1. `n8n-nodes-base.webhook` — ingest prospect payload (`httpMethod: POST`, `path`,
     `responseMode`).
  2. `n8n-nodes-base.code` — normalize to the data contract below; lowercase/trim
     domains, default `target_titles`, derive `trigger_type`.
  3. `n8n-nodes-base.httpRequest` — HubSpot `/crm/v3/objects/companies/search` on
     `domain`; dedupe shield (`authentication: genericCredentialType`,
     `genericAuthType: httpHeaderAuth`, `sendHeaders: true`).
  4. `n8n-nodes-base.if` — collision gate: proceed only when `total == 0`.
  5. `n8n-nodes-base.httpRequest` — Apollo `mixed_people/search` for contact reveal
     on `q_organization_domains`.
  6. `n8n-nodes-base.code` — deliverability pre-flight: deterministic email-format
     checks, role-address flag, bounce-risk heuristics. Fails closed (skip if unsure).
  7. `@n8n/n8n-nodes-langchain.agent` — PAS draft generator (problem-agitate-solve,
     < 65 words). Human-review gate downstream; the agent never sends.
  8. `n8n-nodes-base.httpRequest` — Slack webhook approval card with To/Company/Copy.
- **Data contract (in):** `{ email, name, company, domain?, target_titles?[] }`.
- **Data contract (out):** `{ contact_email, company_domain, collision_free: bool,
  preflight: pass|skip, draft, approval_url? }`.
- **Credentials needed:** HubSpot private-app token, Apollo API key (via `$env`
  placeholders), Slack incoming-webhook URL, LLM credential for the Agent node.
- **Guardrails:** no auto-send ever; every draft requires an approval action before
  sequence enrollment; suppression list check before step 3; rate-limit enrichment
  calls; error workflow attached.
- **Test plan:** (a) known-good prospect → draft + approval card posted;
  (b) duplicate-domain prospect → halted at gate, no enrichment spend;
  (c) malformed email → pre-flight skip, logged; (d) pinned replay of all three
  after any prompt or model change.

### Template 2 — Prospect automation (intent signal mining)

- **Objective:** convert raw intent signals (hiring posts, ATS boards, tech installs)
  into ICP-qualified prospects routed to CRM within minutes.
- **Trigger:** Webhook POST `intent-signal` (factors/signal platform push) or
  Schedule polling Greenhouse/Lever board APIs (`GET
  https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs`).
- **Node-by-node plan:**
  1. `n8n-nodes-base.webhook` (or `n8n-nodes-base.scheduleTrigger`) — ingest signal.
  2. `n8n-nodes-base.code` — normalize signal: company domain, signal type
     (`hiring_spike`, `tech_install`, `funding`), strength.
  3. `n8n-nodes-base.httpRequest` — Apollo `organizations/search` for firmographics
     (headcount, industry, revenue).
  4. `n8n-nodes-base.if` — ICP gate: deterministic thresholds only (no agent here):
     e.g. `employees >= 50`, allowed industries, excluded existing customers.
  5. `n8n-nodes-base.httpRequest` — contact waterfall: Apollo/Prospeo people search
     on qualified domains.
  6. `n8n-nodes-base.httpRequest` — HubSpot create/update company + associate
     signal note (`/crm/v3/objects/companies`).
  7. `n8n-nodes-base.httpRequest` — Slack route alert to `#outbound-signals` with
     rep mention.
- **Data contract (in):** `{ signal_type, company_domain, company_name?, evidence_url?,
  strength? }`.
- **Data contract (out):** `{ qualified: bool, firmographics, contacts_revealed: n,
  crm_object_id?, routed_at }`.
- **Credentials needed:** Apollo API key, HubSpot token, Slack webhook URL.
- **Guardrails:** ICP thresholds are code, not agent judgment; cap waterfall spend
  per run; suppress existing opportunities; idempotency key = domain + signal_type.
- **Test plan:** (a) hiring-spike signal → qualified + routed; (b) below-threshold
  firmographics → dropped with reason; (c) same signal twice → single CRM write
  (idempotency check).

### Template 3 — CRM hygiene (bidirectional dedupe & scorer)

- **Objective:** weekly autonomous pass that finds duplicate contacts/companies,
  scores ghosting risk on open deals, and reports — merges are proposed, never
  auto-executed.
- **Trigger:** `n8n-nodes-base.scheduleTrigger` weekly (read-only until a human
  approves merges).
- **Node-by-node plan:**
  1. `n8n-nodes-base.scheduleTrigger` — weekly cadence.
  2. `n8n-nodes-base.httpRequest` — HubSpot `/crm/v3/objects/companies/search`,
     `limit: 100`, paginate with `after` cursor.
  3. `n8n-nodes-base.code` — duplicate detector: group by normalized domain;
     secondary records ranked by field completeness.
  4. `n8n-nodes-base.set` — build merge-proposal payload (primary + candidates,
     master deal IDs preserved).
  5. `n8n-nodes-base.httpRequest` — Slack `#revops-alerts` report with merge
     candidates and one-click approval links.
  6. `n8n-nodes-base.httpRequest` — HubSpot `/crm/v3/objects/deals/search` for open
     deals older than threshold.
  7. `n8n-nodes-base.code` — ghosting-risk scorer: days-since-last-activity,
     stage stall, missing next step → score 0–100.
  8. `n8n-nodes-base.if` — gate: route deals with score ≥ 70 to owner alerts.
  9. `n8n-nodes-base.httpRequest` — Slack owner alerts with recommended next action.
- **Data contract (in):** none (scheduled pull).
- **Data contract (out):** `{ run_id, duplicates_found: n, merge_proposals: [...],
  high_risk_deals: [...], report_url }`.
- **Credentials needed:** HubSpot token (read; write only via a separate approved
  merge workflow), Slack webhook URL.
- **Guardrails:** never auto-merge — merges require explicit human approval;
  preserve master deal ID; pagination + rate limits on HubSpot reads; dry-run flag
  for the first execution.
- **Test plan:** (a) seeded duplicate → appears in report, no CRM change;
  (b) stalled deal fixture → score ≥ 70 and owner alerted; (c) clean CRM →
  zero-alert run with green report.

### Template 4 — Inbound responder (sub-minute AI lead responder)

- **Objective:** every inbound lead enriched, scored, routed to the right AE, and
  answered in under 60 seconds.
- **Trigger:** Webhook POST `inbound-lead` from form/Typeform/Webflow/HubSpot.
- **Node-by-node plan:**
  1. `n8n-nodes-base.webhook` — ingest lead payload; verify `Authorization: Bearer
     {{ $env.WEBHOOK_SECRET }}` header in a first Code node.
  2. `n8n-nodes-base.code` — normalize + verify webhook secret (reject on mismatch
     via `n8n-nodes-base.stopAndError`).
  3. `n8n-nodes-base.httpRequest` — firmographic/persona enrichment (Apollo
     `mixed_people/search` by email, Brandfetch for logo/industry).
  4. `n8n-nodes-base.code` — deterministic ICP score 0–100 (title weight + company
     size weight + intent keywords; code, not agent).
  5. `n8n-nodes-base.if` — urgency gate: score ≥ 80 → hot path; else nurture path.
  6. Hot path `n8n-nodes-base.httpRequest` — Slack urgent alert + AE round-robin
     assignment (round-robin counter kept in a sub-workflow or Code state).
  7. `n8n-nodes-base.httpRequest` — HubSpot create contact + task for owner
     (`/crm/v3/objects/contacts`, `/crm/v3/objects/tasks`).
  8. `n8n-nodes-base.set` — response receipt payload (lead_id, score, owner,
     responded_at) for the log.
- **Data contract (in):** `{ email, first_name?, company, source? }` + `Authorization`
  header.
- **Data contract (out):** `{ lead_id, icp_score, path: hot|nurture, owner,
  sla_seconds }`.
- **Credentials needed:** Apollo API key, HubSpot token, Slack webhook URL,
  Calendly/Chili Piper link (static), optional Twilio for SMS.
- **Guardrails:** secret-verify every inbound call; scoring deterministic (agent
  only drafts the reply copy, never routing); hot-path alert + human owns the
  call; PII logged only in CRM, never in Slack copy.
- **Test plan:** (a) demo-form fixture → alert < 60s end-to-end; (b) score-90
  fixture → hot path + owner task; (c) score-30 fixture → nurture path, no urgent
  alert; (d) bad secret → rejected, no processing; (e) load: 50 concurrent
  webhooks → no dropped executions.

### Template 5 — Deliverability/DNS (cold email deliverability & DNS kit)

- **Objective:** pre-flight verification of every sending domain: SPF, DKIM, DMARC
  must pass before any campaign launches; fails loudly with remediation steps.
- **Trigger:** Webhook POST `domain-check` with `{ domains: [...], dkim_selector }`,
  or Schedule for weekly domain-health monitoring.
- **Node-by-node plan:**
  1. `n8n-nodes-base.webhook` (or `n8n-nodes-base.scheduleTrigger`) — ingest domain
     list and DKIM selector.
  2. `n8n-nodes-base.code` — normalize domains (strip protocol/www, lowercase,
     dedupe).
  3. `n8n-nodes-base.httpRequest` — fetch SPF via DNS-over-HTTPS
     (`https://dns.google/resolve?name={domain}&type=TXT`, no auth needed).
  4. `n8n-nodes-base.code` — parse SPF: require `v=spf1`, count lookups ≤ 10,
     flag `-all` vs `~all`.
  5. `n8n-nodes-base.httpRequest` — fetch DMARC TXT at `_dmarc.{domain}`.
  6. `n8n-nodes-base.httpRequest` — fetch DKIM TXT at
     `{selector}._domainkey.{domain}`.
  7. `n8n-nodes-base.code` — evaluator: pass/fail per record + overall verdict and
     remediation hints.
  8. `n8n-nodes-base.if` — gate: all-pass → report; any fail →
     `n8n-nodes-base.stopAndError` with the failing record + fix steps (routes to
     the error workflow).
  9. `n8n-nodes-base.set` / `n8n-nodes-base.httpRequest` — deliverability report
     (Slack or returned JSON).
- **Data contract (in):** `{ domains: string[], dkim_selector?: string }`
  (default selector `default`).
- **Data contract (out):** `{ domain, spf: pass|fail, dkim: pass|fail,
  dmarc: pass|fail, overall, remediation: [...] }` per domain.
- **Credentials needed:** none for DNS checks (public DNS-over-HTTPS); Slack
  webhook URL for reporting.
- **Guardrails:** checks are read-only (no DNS writes); evaluate each domain
  independently so one bad record does not block others; report remediation
  commands, never apply them.
- **Test plan:** (a) fully-configured domain → all pass; (b) missing DMARC →
  fail branch + stopAndError fires with remediation; (c) 10 domains → 10
  independent verdicts; (d) malformed domain input → normalize/drop, no crash.

## Output expectations

For build requests, return:
- objective
- recommended architecture
- node-by-node plan or workflow JSON
- credentials and secrets required
- input and output schema
- failure modes and guardrails
- test plan
- deploy and rollback notes

## Validation checklist

- The chosen surface is correct:
  instance MCP vs MCP Trigger vs MCP Client vs ordinary workflow
- The workflow separates deterministic logic from agentic logic
- Credentials are referenced through n8n credentials or approved secret stores
- Human review exists for high-impact writes
- Error handling and rollback are specified
- Pagination, batching, rate limits, and retries are addressed where relevant
- The user can tell what is reusable, what is environment-specific, and what remains to be wired up

## Inputs

- `task` — build, debug, scale, or architect (systems-engineer stance: optimize for revenue impact, operator clarity, safe execution)
- `integration_surface` — decide via the architecture order: instance-level MCP (one secure connection, many approved workflows) · MCP Server Trigger (one purpose-built tool server) · MCP Client Tool (n8n agent calling external MCP) · Call-n8n-Workflow/Execute Sub-workflow (reusable capabilities) · native node · HTTP Request · community node (last resort)
- `business_event` — design backward: trigger → data contract → normalization → business logic → tool/action layer → logging, error path, operator escalation
- `credentials` — referenced through n8n credentials or approved secret stores (`$env` placeholders), never hardcoded
- `template` (1–5, optional) — outreach automation · prospect/intent mining · CRM hygiene · inbound responder · deliverability/DNS kit; each is a build contract: follow it node-for-node before adding flair
- Load only the relevant `references/` file (architecture, agents, http-api, hard-nodes, gtm, ops, starter-pack, sources)

## Example

Template 1 — outreach automation: `webhook` (POST `prospect-intake`) → `code` normalize to the data contract → `httpRequest` HubSpot company search (dedupe shield) → `if` collision gate (`total == 0` only) → `httpRequest` Apollo contact reveal → `code` deliverability pre-flight (fails closed — skip if unsure) → `agent` PAS draft (<65 words; never sends) → `httpRequest` Slack approval card. Credentials: HubSpot private-app token, Apollo key, Slack webhook, LLM credential. Test plan: known-good prospect → draft + card; duplicate domain → halted at gate, no enrichment spend; malformed email → pre-flight skip, logged.

## Errors & edge cases

- **Never invent node parameters, API endpoints, or MCP behavior** — parameter names in the templates are real n8n node parameters; verify against `references/` before adding any.
- **Never hardcode secrets** in workflows or skill files — credentials go through n8n credentials or `$env` placeholders.
- **Instance-level MCP is not per-client scoped**: any connected client can see every workflow enabled for MCP access — it's for discovering/running enabled workflows, not authoring.
- **Human review before high-impact outbound**: no auto-send on first touch; gate writes to CRM, email, sequencing, billing, or legal systems with confidence thresholds or approval.
- **Deterministic logic stays out of the agent**: ICP thresholds, dedupe gates, and deliverability pre-flights are code (fail closed); the AI agent drafts copy and handles tool selection, never routing or sends.
- **Every build ships with**: an error workflow attached, a rollback plan, pagination/batching/rate-limit/retry handling, and explicit labeling of what's live vs JSON/spec vs still needing credentials, environment access, or human approval.
