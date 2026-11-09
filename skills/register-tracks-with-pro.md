---
name: register-tracks-with-pro
description: "Batch-registers a music catalog with a P.R.O. -- exports the catalogue from Supabase, confirms splits, submits the works forms, and updates the PRO key sheet -- delivering works-registration.csv. Use when the user wants to register your tracks with a p.r.o."
---

# Register your tracks with a P.R.O.

- **Subagent:** @pro-agent
- **Category:** Publishing
- **NPAO:** N
- **List price:** $19
- **Source:** PRO guide

## When to use
Batch work registration + key sheet entry.

## Steps
1. Export catalogue from mcp__supabase
2. Confirm splits
3. Submit works form
4. Update key sheet table

## Outputs
works-registration.csv

## Reference tools
- mcp__supabase upsert pro_keysheet

## Guardrails
Composition vs recording IDs stay distinct.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `catalogue` -- exported from Supabase (`mcp__supabase`); composition vs. recording IDs stay distinct
- `splits` -- confirmed writer/publisher split percentages per work, verified before submission

## Example

A 12-track EP: export the catalogue -> confirm 50/50 writer splits -> submit the works registration forms -> update the key sheet table -> works-registration.csv listing all 12 registered works.

## Errors & edge cases

- **Composition vs. recording IDs conflated** -- keep them distinct or royalties misattribute.
- **Dependent capability missing** (e.g. no Supabase export available) -- name it and stop; the parent handoff summarizes artifacts + blockers.
