---
name: gtm-architect-factors-api-reference-skill
description: "LLM-agnostic sales prospecting and go-to-market skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to use the Factors.ai API reference built for gtm-architect (see the standalone factors-api-skill for the full reference): core endpoints for accounts, workflows, alerts, events, and integrations; the canonical Factors -> HubSpot ABM date + n8n trigger workflow; backfill for historical accounts; and sync debugging - with domain as the join key and factors_abm__workflow_date as the key HubSpot field. Use when working with the Factors.ai API for the GTM Architect reference."
---

# Factors.ai API — GTM Architect Reference

> This is the Factors.ai reference for use within gtm-architect.
> For the full Factors.ai skill (standalone), see the `factors-ai` skill.
> Auth is in `references/credentials.md`.

**Base URL:** `https://api.factors.ai`
**Auth:** `Authorization: Bearer {{FACTORS_AI_KEY}}`
**Key HubSpot field:** `factors_abm__workflow_date` (Company, datetime) — join key: domain

---

## Core Endpoints

### Accounts
```
GET  /v1/accounts                    # list all (params: page, per_page, domain, segment)
GET  /v1/accounts/{id}               # get single account
POST /v1/accounts                    # create account
PATCH /v1/accounts/{id}              # update account
POST /v1/accounts/bulk               # bulk upsert by domain
```

### Workflows
```
GET  /v1/workflows                   # list all
GET  /v1/workflows/{id}              # get single
POST /v1/workflows                   # create workflow
PATCH /v1/workflows/{id}             # update (status, name, actions)
DELETE /v1/workflows/{id}            # delete
GET  /v1/workflows/{id}/executions   # history (params: start_date, end_date)
```

### Alerts
```
GET  /v1/alerts                      # list all
POST /v1/alerts                      # create alert
PATCH /v1/alerts/{id}                # update
DELETE /v1/alerts/{id}               # delete
```

### Events
```
GET  /v1/events                      # global events (params: account_domain, event_type, dates)
GET  /v1/accounts/{id}/events        # events for one account
POST /v1/events                      # track custom event
```

### Integrations
```
GET  /v1/integrations/hubspot        # check HubSpot connection
GET  /v1/integrations/hubspot/field_mapping   # see field mappings
PUT  /v1/integrations/hubspot/field_mapping   # set field mappings
```

---

## Canonical Workflow: Factors → HubSpot ABM Date + n8n Trigger

```python
workflow = {
    "name": "ABM Signal → HubSpot + n8n",
    "status": "active",
    "trigger": {
        "type": "event",
        "event_name": "$pageview",
        "frequency": "once_per_account_per_day",
        "conditions": [{"property": "page_url", "operator": "contains", "value": "/pricing"}]
    },
    "filters": [{"type": "segment", "segment_name": "ICP Tier 1"}],
    "actions": [
        {
            "type": "hubspot_update",
            "object": "company",
            "match_on": "domain",                          # ← join key
            "properties": {
                "factors_abm__workflow_date": "{{event.timestamp}}"
            }
        },
        {
            "type": "webhook",
            "url": "https://YOUR_N8N/webhook/factors-abm-trigger",
            "method": "POST",
            "payload": {
                "account_domain": "{{account.domain}}",
                "account_name": "{{account.name}}",
                "timestamp": "{{event.timestamp}}",
                "source": "factors_ai"
            }
        }
    ]
}
```

---

## Backfill: Populate `factors_abm__workflow_date` for Historical Accounts

```python
import requests

FACTORS_HEADERS = {"Authorization": "Bearer {{FACTORS_AI_KEY}}", "Content-Type": "application/json"}
HS_HEADERS = {"Authorization": "Bearer {{HUBSPOT_API_KEY}}", "Content-Type": "application/json"}

# 1. Get all past executions for a workflow
execs = requests.get(
    "https://api.factors.ai/v1/workflows/{WORKFLOW_ID}/executions",
    headers=FACTORS_HEADERS,
    params={"start_date": "2024-10-01"}
).json().get("executions", [])

# 2. Group by domain, keep most recent
domain_ts = {}
for ex in execs:
    d = ex.get("account", {}).get("domain")
    ts = ex.get("executed_at")
    if d and ts and (d not in domain_ts or ts > domain_ts[d]):
        domain_ts[d] = ts

# 3. Batch upsert to HubSpot
inputs = [{"idProperty": "domain", "id": d, "properties": {"factors_abm__workflow_date": ts}}
          for d, ts in domain_ts.items()]
for i in range(0, len(inputs), 100):
    requests.post(
        "https://api.hubapi.com/crm/v3/objects/companies/batch/upsert",
        headers=HS_HEADERS,
        json={"inputs": inputs[i:i+100]}
    )
print(f"Backfilled {len(inputs)} companies")
```

---

## Debugging the Sync

If `factors_abm__workflow_date` isn't updating on HubSpot companies:
1. Confirm account exists in Factors with domain set
2. Confirm HubSpot company exists with matching domain
3. Check workflow is `active` and has `hubspot_update` action with `match_on: "domain"`
4. Check the Factors → HubSpot integration is connected
5. Check field mapping includes `factors_abm__workflow_date`
6. Check workflow execution history for this account

Read-only API checks for steps 1, 4, 5, and 6:

```http
GET /v1/accounts?domain=EXAMPLE_DOMAIN
GET /v1/integrations/hubspot
GET /v1/integrations/hubspot/field_mapping
GET /v1/workflows/{id}/executions?account_domain=EXAMPLE_DOMAIN
```

## Inputs
- `need` (enum: endpoints / canonical-workflow / backfill / debug, required)
- `FACTORS_AI_KEY` (env, from references/credentials.md)

## Outputs
- Endpoint table (accounts/workflows/alerts/events/integrations) with methods and params
- Canonical workflow spec: ABM Signal -> HubSpot + n8n (event trigger, segment filter, hubspot_update on domain, webhook action)
- Backfill procedure: executions -> group by domain, keep most recent -> batch upsert to HubSpot

## Example
Input: backfill factors_abm__workflow_date for historical accounts.
1. GET /v1/workflows/{id}/executions with start/end dates.
2. Group by domain, keep the most recent execution per domain.
3. Batch upsert to HubSpot companies matched on domain.

## Errors & edge cases
- Need the full Factors reference: use the standalone factors-api-skill - this one is scoped to the gtm-architect use case.
- Sync not updating: run the debugging section (integration status -> field mapping -> domain join key).
- Auth: references/credentials.md first, always.
