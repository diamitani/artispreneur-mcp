---
name: marketing-chatbot-execution-analyst-marketing-chatbot-execution-analyst
description: "Chatbot-scoped n8n + HubSpot execution analyst: server-side-filtered ingest of only the marketing chatbot's workflows (the MQL Classification n8n workflow + two HubSpot flows), with query recipes for success rates, failures, and streaks -- every number cited by execution ID. Use when working with marketing chatbot execution analyst."
---

# Marketing Chatbot Execution Analyst

Scoped fork of the n8n Execution Analyst that watches **only the Marketing Chatbot's
workflows**. Every ingest is server-side filtered to the chatbot's n8n workflow, so the
local store never mixes in other automations. Companion skills:
`maia-chatbot-analyst` (business results/reporting) · `hubspot-chatbot-manager` (config) ·
generic `n8n-execution-analyst` (everything else in the n8n instance).

## Scope — the ONLY workflows this skill covers

| System | Workflow | ID / Link |
|---|---|---|
| n8n | Marketing Chatbot \| MQL Classification (14 nodes, active) | `SKUv0NlJUsWyNB4Z` · https://$N8N_BASE_URL/workflow/SKUv0NlJUsWyNB4Z |
| HubSpot | Marketing Chatbot \| Update Contact | flow `1843970484` · https://app.hubspot.com/workflows/$HUBSPOT_PORTAL_ID/platform/flow/1843970484/edit |
| HubSpot | Marketing Chatbot \| MQL Classification | flow `1842490003` · https://app.hubspot.com/workflows/$HUBSPOT_PORTAL_ID/platform/flow/1842490003/edit |

If asked about any other workflow, say it's out of scope here and route to
`/n8n-execution-analyst`.

## Setup

```bash
# Self-contained env bootstrap -- inlined from maia-chatbot-analyst/scripts/env.sh
# (same pattern; that skill is an optional convenience, not a dependency)
: "${N8N_API_KEY:?Set N8N_API_KEY -- from n8n -> Settings -> n8n API}"
: "${N8N_BASE_URL:?Set N8N_BASE_URL -- your n8n instance}"
: "${HUBSPOT_PAT:?Set HUBSPOT_PAT -- your HubSpot private app token}"
cd into this skill's directory
python3 scripts/store.py    # one-time DB init (data/executions.db — chatbot-only store)
```

## Configuration

| Variable | What it is |
|---|---|
| `N8N_API_KEY` | n8n API key (n8n -> Settings -> n8n API). Never print or log it. |
| `N8N_BASE_URL` | n8n instance base URL |
| `HUBSPOT_PAT` | HubSpot private app token |
| `HUBSPOT_PORTAL_ID` | HubSpot portal ID (used in the flow links) |
| `N8N_WORKFLOW_FILTER` | Optional override -- comma-separated workflow IDs (defaults to the chatbot's `SKUv0NlJUsWyNB4Z`) |

Scoping is baked in: `scripts/ingest.py` defaults `N8N_WORKFLOW_FILTER=SKUv0NlJUsWyNB4Z`
and passes it as a server-side `workflowId` filter. Widen only by exporting a
comma-separated `N8N_WORKFLOW_FILTER` (rarely wanted — prefer the generic skill).

## Routing

| User says… | Do this |
|---|---|
| "pull / refresh chatbot executions" | `scripts/ingest.py` (`--limit N` pilot, `--workflow <id>` to target one) |
| "run the daily chatbot execution report" | `scripts/run_daily.py` (ingest → alert check → dashboard) |
| any question about chatbot runs, failures, rates, a specific execution | `scripts/query.py` --stats / `--failures N` / `--streaks` (`--days`, `--workflow`, `--json` flags) — cite execution IDs |
| "chatbot execution dashboard" | `scripts/dashboard/build.py` → present the generated dashboard/index.html |
| "did conversation/contact X get scored?" | ingest, then query executions around the conversation close time; cross-check the contact's property history via the HubSpot contacts API with property history for lifecyclestage |
| HubSpot workflow (1843970484 / 1842490003) questions | HubSpot exposes no execution-log API — check the flow definition via the HubSpot automation flows API and per-contact property history; for anything deeper, link to the flow's History tab in the UI and say so honestly |
| "create an artifact / report / table from execution data" | query the store, then build the artifact (markdown/xlsx/HTML dashboard) — every number from stored executions, cite execution IDs |

## Guardrails (inherited + scoped)

- **Read-only** n8n + HubSpot APIs. GET only. Never activate/deactivate/delete.
- **Chatbot scope only.** Never report on other workflows from this skill.
- **No fabrication.** Answers come from the store (`scripts/query.py`) or live API JSON —
  if data is absent, say so.
- **Secrets from env only** (`N8N_API_KEY`, `HUBSPOT_PAT`). Never print them.
- **Alerts dry-run by default** (`scripts/alert.py`).
- Store is idempotent (upsert on execution ID); safe to re-run anytime.

## What gets captured per execution

Workflow name + ID · start/stop time · status · duration · top-level error message ·
per-node errors (node name + message). See `docs/SCHEMA.md`.

## Scheduling

Wire `scripts/run_daily.py` daily 06:00 CT — it feeds the "Automation health" section of
the Maia Daily Digest (see the maia-chatbot-analyst skill's daily-report-workflow-spec reference, node 6).

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `command` | enum | required | `ingest` (pull/refresh executions) | `daily_report` (ingest -> alert check -> dashboard) | `query` (ask about runs/failures/rates) | `dashboard` (build the HTML dashboard) |
| `flags` | string | -- | `--limit N`, `--days N`, `--workflow <id>`, `--json` for `query.py` |
| `execution_id` | string | -- | Drill into one specific execution. |

## Outputs

- **Deliverable:** execution stats, failure lists, streaks, or the daily report -- every number from stored executions, cited by execution ID.
- **Format:** chat summary + `dashboard/index.html` for the dashboard command.

## Example

> "What was the chatbot's scoring success rate this week?"

1. `python3 scripts/ingest.py` (refreshes the chatbot-only store; server-side filtered to `SKUv0NlJUsWyNB4Z`).
2. `python3 scripts/query.py --stats --days 7`
3. Report: "The scoring automation ran N times, succeeded X%," with the failing execution IDs and their node errors listed.

## Errors & edge cases

- n8n 401/403 on ingest -> `N8N_API_KEY` missing/invalid or `N8N_BASE_URL` wrong.
- HubSpot workflow questions -> HubSpot exposes no execution-log API; check the flow definition via the automation flows API and per-contact property history, and link the flow's History tab honestly.
- Asked about a non-chatbot workflow -> out of scope here; route to the generic `n8n-execution-analyst`.
- Alerts are dry-run by default (`scripts/alert.py`); the store upserts on execution ID, so re-running ingest is always safe.
