---
name: intake-map-skill
description: "Silent 6-section intake mapper — extracts Identity, Goals, Scope, Stakeholders, Tech & Data, and Current State from raw user input plus research, labels every field [Extracted]/[Inferred]/[Enrich]/[TBD], and surfaces only true blockers in the Gap Check (the user never fills out a form). Use when working with intake map."
---

# Intake Map (Reference)

> The 6 sections every input is silently mapped against. **The user never fills this out.** The system extracts from their input + research, labels each field, and surfaces only unresolved gaps in the Gap Check.
>
> Labels: `[Extracted]` — found in the input · `[Inferred]` — derived from context · `[Enrich]` — fill via web research · `[TBD]` — must ask the user.

---

## Section 1 — Identity & Problem

| Field | Required? | If missing |
|---|---|---|
| Project name | **Yes** | Ask (blocker) |
| One-sentence description | **Yes** | Ask (blocker) |
| Project type (automation, agent/skill, dashboard, content, enablement, RevOps, internal tool, EOR process, other) | Recommended | Infer |
| Problem this solves + who feels it | Recommended | Infer from description |
| How it's handled today + cost of doing nothing | No | Infer or `[TBD]` |
| Net-new vs. enhancement | No | Infer |

## Section 2 — Goals & Success

| Field | Required? | If missing |
|---|---|---|
| Primary goal | **Yes** | Ask (blocker) |
| Success criteria — how we'll know it worked | Recommended | Infer from project type (flag as friction) |
| KPIs (time saved, leads, meetings, pipeline $, adoption, data quality, cost savings, error reduction) | Recommended | Infer via research |
| Target numbers / benchmarks | No | `[TBD]` |
| Timeline to results | No | `[TBD]` |

## Section 3 — Scope & Constraints

| Field | Required? | If missing |
|---|---|---|
| In scope | Recommended | Infer (flag ambiguity as friction) |
| Out of scope | No | `[TBD]` |
| Hard deadlines / external dependencies | No | `[TBD]` |
| Constraints — budget, compliance, tools we can't use | No | `[TBD]` |
| Must-have integrations | Recommended | Infer from stack |
| Who approves / signs off | No | `[TBD]` |

## Section 4 — Users & Stakeholders

| Field | Required? | If missing |
|---|---|---|
| Primary end user + technical level | Recommended | Infer from project type |
| Number of users at ship | No | Infer |
| What makes them adopt it / abandon it | No | Infer |
| Executive sponsor | No | `[TBD]` |
| Other teams impacted | No | `[TBD]` |
| Similar projects that failed before — why | No | `[TBD]` |

## Section 5 — Tech & Data

| Field | Required? | If missing |
|---|---|---|
| Tools it must work with (HubSpot, Clay, Amplemarket, n8n, Asana, Factors.ai, Slack, M365, Salesforce, other) | Recommended | Infer from use case |
| Where input data comes from / where output goes | Recommended | Infer |
| **API keys / access confirmed today?** | Recommended | **Blocker if unconfirmed** → API Readiness |
| Privacy / security / compliance needs | No | `[TBD]` |
| Preferred AI model / platform / budget | No | Default to approved stack |

## Section 6 — Current State & Context

| Field | Required? | If missing |
|---|---|---|
| Does this already exist somewhere? (Asana, Slack, Notion, Drive, someone's head) | Recommended | Assume net-new |
| Asana URL / docs to import | No | Skip |
| Current state (not started, planning, in progress, stalled, done-needs-docs, abandoned) | No | Assume not started |
| Does leadership know it exists? | No | If no/unsure → Leadership Summary is doubly mandatory |
| Reference materials, links, competitor examples | No | `[Enrich]` |
| Brain dump — fears, 10/10 outcome, what to cut first | No | Skip |

---

## Gap → Priority Mapping

| Gap | Class | Effect |
|---|---|---|
| Missing name / description / primary goal | **Blocker** | Ask in Gap Check; can't proceed unnamed |
| Unconfirmed API or integration access | **Blocker** | API Readiness block per tool |
| Ambiguous scope, missing KPIs | **Friction** | Flag in Brief risk section; infer where possible |
| Missing optional context | **Enrich/skip** | Research if valuable, skip if not |

**Minimum viable submission:** one sentence. Quality: description only ≈ 60% · + Sections 1–2 ≈ 80% · + Sections 3–5 ≈ 95% · all six ≈ 100%. State the score in the Brief.

**Special behaviors:**
- Asana URL → import all tasks/comments/attachments as `[IMPORTED — Asana]` before generating anything.
- "Stalled" project → surface friction items first.
- Leadership unaware → Leadership Summary leads every conversation about the project, not just the doc.

## Inputs

- `raw_input` (string, required) — the user's brain dump or request; minimum viable submission is one sentence (~60% quality)
- `asana_url` (optional) — if provided, all tasks/comments/attachments are imported as `[IMPORTED — Asana]` before anything is generated
- Research context (web) fills `[Enrich]` fields; the system infers the rest and asks only about `[TBD]` blockers

## Outputs

- A 6-section intake map (Identity & Problem, Goals & Success, Scope & Constraints, Users & Stakeholders, Tech & Data, Current State & Context) with every field labeled `[Extracted]` / `[Inferred]` / `[Enrich]` / `[TBD]`
- Gap → Priority mapping: **Blockers** (missing name/description/goal, unconfirmed API access) vs **Friction** (ambiguous scope, missing KPIs) vs **Enrich/skip**
- A quality score stated in the Brief: description only ≈ 60%, + Sections 1–2 ≈ 80%, + Sections 3–5 ≈ 95%, all six ≈ 100%
- Format: internal reference — the user only ever sees the Gap Check questions, never the map itself

## Example

Input: one sentence — 'Build a dashboard tracking outbound replies.' Section 1: project name = `[TBD]` (blocker), type = dashboard `[Inferred]`. Section 5: tools HubSpot/Clay `[Inferred]`, API keys unconfirmed → **Blocker** → API Readiness. Score ≈ 60%. The Gap Check asks exactly two things: the project name and API access confirmation — everything else is inferred or enriched silently.

## Errors & edge cases

- **Unconfirmed API or integration access is a hard blocker** — do not proceed past intake until access is confirmed (API Readiness per tool).
- **One-sentence input is acceptable** (~60% quality) — run the Gap Check rather than demanding more upfront.
- **'Stalled' current state** → surface friction items first; don't re-run discovery the user already did.
- **Leadership unaware of the project** → the Leadership Summary becomes mandatory and leads every conversation about it.
