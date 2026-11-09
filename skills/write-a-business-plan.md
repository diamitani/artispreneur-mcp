---
name: write-a-business-plan
description: "Writes a 12-month business plan with revenue mix -- Q1-Q4 milestones, a KPI table, and revenue mix drawn from the finance context -- delivering business-plan.md. Use when the user wants to write a business plan."
---

# Write a business plan

- **Subagent:** @finance-manager
- **Category:** Finance
- **NPAO:** P
- **List price:** $39
- **Source:** Finance

## When to use
12-month plan with revenue mix.

## Steps
1. Q1-Q4 milestones
2. KPI table
3. revenue mix from mcp__finance context

## Outputs
business-plan.md

## Reference tools
- reference/templates/business-plan.md
- mcp__finance

## Guardrails
No guaranteed numbers.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `business_context` -- finance context via mcp__finance (drives the revenue mix)
- `horizon` -- 12-month plan (Q1-Q4 milestones)

## Example

An early-stage SaaS: Q1-Q4 milestones set -> KPI table built -> revenue mix pulled from the finance context -> business-plan.md delivered from the reference template.

## Errors & edge cases

- **Guaranteed numbers** -- never (guardrail: no guaranteed numbers).
- **Dependent capability missing** (e.g. no finance context) -- name it and stop; the parent handoff summarizes artifacts + blockers.
