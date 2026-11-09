---
name: n8n-engineer-skill
description: "Designs, compiles, and validates production-ready n8n workflow JSON for B2B GTM and revenue automation — deterministic native-node logic, zero hardcoded secrets (`$env`/credential references only), a mandatory CRM dedupe shield before any outbound action, and error-trigger observability wired to RevOps Slack. Use when generating, modifying, or auditing n8n workflow JSON graphs for B2B GTM and revenue automation."
---

# n8n Systems Engineer Master Skill

Use this skill when generating, modifying, or auditing n8n workflow JSON graphs for B2B GTM and revenue automation.

---

## 📐 Core Engineering Principles

1. **Deterministic Logic Over Flaky Scripts**:
   - Use native n8n node types (`n8n-nodes-base.httpRequest`, `n8n-nodes-base.code`, `n8n-nodes-base.if`, `n8n-nodes-base.switch`) for predictable pipeline operations.
   - Restrict LLM / Agent nodes strictly to unstructured analysis, entity extraction, and dynamic Problem-Agitate-Solve copy generation.

2. **Zero Hardcoded Secrets**:
   - Never embed raw API keys, tokens, or webhook secrets in JSON node parameters.
   - Always reference environment variables (`={{ $env.SECRET_KEY }}`) or n8n credential objects (`genericAuthType`, `httpHeaderAuth`).

3. **CRM Dedupe Shield Mandatory**:
   - Before executing any outbound action (Smartlead, Instantly, Email, Slack dispatch), query the primary CRM (HubSpot, Salesforce, Attio) to verify:
     - Is the domain or contact an existing active customer?
     - Is there an open deal in progress with another rep?
     - Is the contact marked `Do Not Contact`?

4. **Error Handling & Observability**:
   - Configure retry on failure (3 retries with exponential backoff for external APIs).
   - Wire error triggers (`n8n-nodes-base.errorTrigger`) to route failure payloads (`runData[node][0].error`) directly to RevOps Slack channels.

---

## 🛠️ Canonical JSON Node Schema (v1.x Engine)

```json
{
  "name": "Production GTM Workflow",
  "nodes": [
    {
      "parameters": {},
      "id": "unique-uuid-01",
      "name": "Trigger Node",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300]
    }
  ],
  "connections": {},
  "settings": {
    "executionOrder": "v1"
  }
}
```

## Inputs

- `workflow_spec` — the trigger, node sequence, and connections to generate, modify, or audit
- `credentials` — referenced only via `={{ $env.* }}` or n8n credential objects; never raw values in JSON
- `crm` (HubSpot / Salesforce / Attio) — the dedupe shield queries it before any outbound action
- Scope: B2B GTM and revenue automation workflow JSON graphs (v1.x engine schema)

## Outputs

- Production-ready n8n workflow JSON: `{name, nodes[], connections{}, settings: {executionOrder: "v1"}}` with native node types, credential references, 3-retry exponential backoff, and `errorTrigger` → RevOps Slack wiring
- Audit verdicts against the four core principles (deterministic logic, zero secrets, dedupe shield, observability)
- Format: workflow JSON graph, ready to import

## Example

Outbound workflow JSON: `webhook` trigger → `code` normalize → `httpRequest` HubSpot company search (dedupe shield: existing customer? open deal? DNC?) → `if` clear → Smartlead dispatch; `errorTrigger` routes failures to #revops-alerts. Every secret is `={{ $env.HUBSPOT_KEY }}` — nothing raw. Canonical v1.x schema: `{name, nodes[] (parameters, id, name, type, typeVersion, position), connections{}, settings: {executionOrder: "v1"}}`.

## Errors & edge cases

- **Hardcoded secrets are a build failure.** Never embed raw API keys, tokens, or webhook secrets in JSON node parameters — always `={{ $env.SECRET_KEY }}` or n8n credential objects (`genericAuthType`, `httpHeaderAuth`).
- **The CRM dedupe shield is mandatory** before any outbound action (Smartlead, Instantly, email, Slack dispatch): is the domain/contact an existing active customer? An open deal with another rep? Marked Do Not Contact? Skip the shield and you spam customers.
- **LLM/Agent nodes are restricted** to unstructured analysis, entity extraction, and dynamic PAS copy generation — deterministic pipeline operations stay on native nodes (`httpRequest`, `code`, `if`, `switch`).
- **Observability is not optional**: 3 retries with exponential backoff on external APIs, and `n8n-nodes-base.errorTrigger` routing failure payloads (`runData[node][0].error`) to RevOps Slack.
