---
name: maia-chatbot-analyst
description: "Maia chatbot performance analyst: answers 'is the chatbot generating pipeline, and at what quality?' with real HubSpot/n8n data -- PAL intent routing, pull recipes for conversations, contacts, MQLs, meetings, and deals, audience-calibrated report templates (exec one-pager vs. ops detail), and read-only, no-fabrication guardrails. Use when working with maia chatbot analyst."
---

# Maia Chatbot Analyst

Answers any stakeholder question about Maia's results with real data, and produces
audience-ready reports. Companion to `hubspot-chatbot-manager` (which *configures* Maia —
this skill *measures* her).

**Core question this skill exists to answer:** *Is Maia generating pipeline, and at what quality?*

---

## Known Resources

| Resource | Value |
|---|---|
| HubSpot Portal | `$HUBSPOT_PORTAL_ID` (env) |
| Chatflow (Maia) | `86381848` (UI-only — no public chatflows API, verified 404 on 2026-07-15) |
| Inbox | `1736871815` ("Hubspot Marketing Chatbot" — verified live 2026-07-15; older docs cite `10607506765`, which no longer exists) |
| HubSpot workflows | Update Contact `1843970484` · MQL Classification `1842490003` |
| MQL Classification workflow (n8n) | `SKUv0NlJUsWyNB4Z` → https://$N8N_BASE_URL/workflow/SKUv0NlJUsWyNB4Z |
| Segments (lists) | Contacts `31302` · Companies `31489` · Deals `31488` · MQLs `31487` |
| Master dashboard | https://app.hubspot.com/reports-dashboard/$HUBSPOT_PORTAL_ID/view/21114973 — full registry in `references/reporting-framework.md` |
| n8n instance | `$N8N_BASE_URL` (env) |
| Pilot page | `https://www.$COMPANY_SITE` (env) |
| Project dir | `$MAIA_PROJECT_DIR` (env -- your local project folder) |

Credentials (env) -- self-contained; no other skill required:

```bash
: "${HUBSPOT_PAT:?Set HUBSPOT_PAT -- your HubSpot private app token}"
: "${N8N_API_KEY:?Set N8N_API_KEY -- from n8n -> Settings -> n8n API}"
: "${N8N_BASE_URL:?Set N8N_BASE_URL -- your n8n instance}"
: "${HUBSPOT_PORTAL_ID:?Set HUBSPOT_PORTAL_ID -- your HubSpot portal ID}"
hs_get()  { curl -s -H "Authorization: Bearer $HUBSPOT_PAT" "https://api.hubapi.com$1" "${@:2}"; }
hs_post() { curl -s -X POST -H "Authorization: Bearer $HUBSPOT_PAT" -H "Content-Type: application/json" "https://api.hubapi.com$1" -d "$2" "${@:3}"; }
```

(Attribution: same wrappers as `maia-chatbot-analyst/scripts/env.sh` and `hubspot-chatbot-manager`'s `hs-api.sh`. If either skill is installed, its env file/scripts are an optional convenience -- never a dependency. See Setup below if a credential is missing.)

## Configuration

| Variable | What it is |
|---|---|
| `HUBSPOT_PAT` | HubSpot private app token (never print or log it) |
| `HUBSPOT_PORTAL_ID` | Your HubSpot portal ID (dashboard/report links) |
| `N8N_BASE_URL` | Your n8n instance base URL |
| `N8N_API_KEY` | n8n API key |
| `COMPANY_SITE` | Company site host for the pilot-page link |
| `MAIA_PROJECT_DIR` | Your local project folder for artifacts (was the author's `~/Documents/Claude/Projects/Hubspot Chatbot Buildout`) |

---

## Step 0 — Understand intent with PAL

Before pulling anything, run the request through `/pal` (skill: `anthropic-skills:pal`) to
extract: **who is asking** (exec/board vs. ops), **what metric or object** they want
(conversations, contacts, MQLs, meetings, deals, bad conversations, workflow health),
**date range** (default: last 7 days if unstated), and **desired output** (number, table,
narrative report, dashboard, scheduled workflow). If PAL is unavailable, do the same
extraction inline. Never ask the user to clarify things you can default sensibly.

**Audience calibration:**
- **VP Marketing / board / stakeholders** → plain English, no jargon, lead with the headline
  number, funnel context, 1-page max, always state the date range and data source.
- **Patrick / ops** → include record IDs, property names, execution IDs, and anomalies.

## Step 1 — Route to the right data source

| Intent | Where to pull | How |
|---|---|---|
| Conversations, transcripts, inbox volume | HubSpot Conversations API (inbox `1736871815`) | the hs_get tool against the HubSpot Conversations API threads endpoint — see `references/data-sources.md` |
| Contacts created / MQLs / lead quality | HubSpot Contacts search on chatbot properties | recipes in `references/data-sources.md` §2 |
| Meetings booked | Meetings search + Maia meeting link | §3 |
| Deals / revenue / WSEs attributed | Deals search + associations walk | §4 |
| Lists, properties, HubSpot workflows | Lists v3 / Properties v3 / Flows v4 | §5 |
| Dashboards & reports | Link the existing assets first (`references/reporting-framework.md`), then live pulls | §6 |
| "Did the MQL workflow run / fail?", execution detail, scoring gaps | **/marketing-chatbot-execution-analyst** (chatbot-scoped) | Step 2 below |
| "Bad conversations" | Pull threads + chatbot_* props, apply the Bad Conversation rubric | `references/report-templates.md` §4 |
| "Daily report" (run one now) | Full daily digest pull | `references/report-templates.md` §3; existing script: the customer_agent_daily_report.py script in the project directory |
| "Build/automate the daily report" | **/n8n-engineer** with the bundled spec | Step 3 below |

If the HubSpot MCP connector is available in the session (tools like
`search_crm_objects`, `query_crm_data`), prefer it for CRM object queries; fall back to the
REST recipes otherwise. Conversations/inbox/chatflow data is REST-only.

## Step 2 — Workflow execution data (companion skill, optional)

For anything about the chatbot workflows' runs, the companion
**marketing-chatbot-execution-analyst** skill is pre-scoped to the chatbot's workflows
only (n8n `SKUv0NlJUsWyNB4Z` + HubSpot flows `1843970484`/`1842490003`) — use it when
installed. For non-chatbot workflows, use the generic `n8n-execution-analyst` instead.

Graceful degradation (companion skill unavailable) -- query n8n directly:

```bash
: "${N8N_BASE_URL:?Set N8N_BASE_URL}" ; : "${N8N_API_KEY:?Set N8N_API_KEY}"
curl -s "$N8N_BASE_URL/api/v1/executions?workflowId=SKUv0NlJUsWyNB4Z&limit=50" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | python3 -m json.tool | head -60
```

Typical stakeholder joins this enables:
- "Conversation closed but contact never got MQL-stamped" → find the execution for that
  conversation/session ID, report the failing node and error.
- "How reliable is chatbot scoring?" → execution success rate over the date range,
  presented as *"the scoring automation ran N times, succeeded X%"*.

Inherit that skill's guardrails: GET-only, no fabricated data, secrets from env.

## Step 3 — Building the automated daily report

When asked to **automate** reporting (vs. run one now), invoke **/n8n-engineer**
(skill: `anthropic-skills:n8n-engineer`) and hand it
`references/daily-report-workflow-spec.md`. Two starting assets already exist:
- the existing n8n_customer_agent_daily_reporter.json file in the project dir — prior daily reporter draft
- the existing customer_agent_daily_report.py script in the project dir — working Python pull logic to port

The target output is the daily digest table defined in the spec: every conversation of the
day with associated contact, conversation summary, temperature, MQL result, meeting/deal
status, and a header of day-over-day KPIs. Delivery per spec (email and/or Slack).
Alternatively, if the user wants it HubSpot-native, propose scheduled HubSpot reports/lists
per `references/data-sources.md` §6 — but n8n is the recommended path since HubSpot's
reports API can't compose this table.

## Step 4 — Construct the answer

1. Pull the data (Steps 1–2). **Every number must come from an API response you actually
   received.** If a pull fails or a field is empty, say so — never estimate silently.
2. Pick the matching template from `references/report-templates.md`:
   Executive Snapshot · Funnel · Daily Digest · Bad Conversations Review · Board One-Pager.
3. State date range, data source, and pull time on every report.
4. For exec/board output, close with 2–3 "So what" bullets (what's working, what needs
   attention, recommended next step).
5. If the user wants an artifact: markdown in the project dir; an xlsx file via the xlsx skill;
   PDF via `make-pdf`.

---

## Hard guardrails

- **Read-only.** GET/search only against HubSpot and n8n. Never create, update, or delete
  CRM records, workflows, or executions from this skill. (Config changes → route to
  `hubspot-chatbot-manager`.)
- **No fabrication.** No number, contact name, or quote that didn't come from an API
  response in this session. If data is unavailable, state exactly what's missing and why.
- **Secrets from env only.** Never print, log, or paste `HUBSPOT_PAT` or `N8N_API_KEY`.
- **PII discipline.** Board/stakeholder outputs use company names and aggregates; include
  individual contact emails only when the audience is Patrick/ops or the user explicitly asks.
- **Property gotchas** (verified against live data 2026-07-15 — do not "correct" these):
  the Maia cohort filter is `chatbot_session_id HAS_PROPERTY`; the booleans
  `chatbot_mql_status` / `ai_chatbot_processed` exist but are never populated (0 contacts);
  MQL = `lifecyclestage=marketingqualifiedlead`; temperature values are lowercase
  `hot`/`low`. Full map + counts in `references/data-sources.md` §2 and §7.

## Setup (one time, only if env is missing)

1. HubSpot: export `HUBSPOT_PAT` (HubSpot private app token). If the `hubspot-chatbot-manager` skill is installed, its `.env` holds the same token -- reuse it, but this skill never requires that skill.
2. n8n: export `N8N_API_KEY` (n8n → Settings → n8n API) and `N8N_BASE_URL` (your n8n instance). A local `.env` in this skill's folder works too if your shell loads it.
3. Export `HUBSPOT_PORTAL_ID`, `COMPANY_SITE`, and `MAIA_PROJECT_DIR` for dashboard links and artifacts.
4. Verify: `curl -s -H "Authorization: Bearer $HUBSPOT_PAT" https://api.hubapi.com/crm/v3/objects/contacts?limit=1 | head -c 200` should return JSON, not a 401.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `question` | string | required | The stakeholder question (run through PAL first: who is asking, what metric/object, date range, desired output). |
| `date_range` | string | last 7 days | e.g. `2026-10-01..2026-10-07`. Stated on every report. |
| `audience` | enum | auto | `exec` (plain English, headline number first, 1-page max) | `ops` (record IDs, property names, execution IDs, anomalies). |
| `output` | enum | `narrative` | `number` | `table` | `narrative` | `dashboard` | `scheduled workflow`. |

## Outputs

- **Deliverable:** the answer with date range, data source, and pull time stated; exec output closes with 2-3 "so what" bullets; artifacts on request (Markdown in the project dir, xlsx, PDF).
- **Format:** chat report + optional artifact file. Every number comes from an API response received in the session.

## Example

> "How many MQLs did Maia generate last week?"

1. PAL: asker = VP Marketing (exec) -> metric = MQLs, range = last 7 days, output = number + funnel context.
2. Route: contacts search on the chatbot cohort (`chatbot_session_id HAS_PROPERTY` + `createdate GTE $SINCE_MS`), filter `lifecyclestage = marketingqualifiedlead`.
3. Build the Executive Snapshot template: headline MQL count, funnel (conversations -> contacts -> MQLs), date range + source stated, 2-3 so-what bullets.

## Errors & edge cases

- 401 from HubSpot -> `HUBSPOT_PAT` missing/invalid; re-export it.
- Empty cohort -> verify the `chatbot_session_id HAS_PROPERTY` filter; never filter on `ai_chatbot_processed` / `chatbot_mql_status` (exist but are never populated).
- Temperature values are lowercase `hot`/`low`; MQL = `lifecyclestage=marketingqualifiedlead` -- do not "correct" these.
- HubSpot MCP connector absent -> fall back to the REST recipes; conversations/inbox data is REST-only anyway.
- No fabrication: if a pull fails or a field is empty, say exactly what's missing and why.
