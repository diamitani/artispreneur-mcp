---
name: track-royalties-on-dsps
description: "Tracks DSP royalties against the key sheet -- ingests statements, computes week-over-week deltas, flags Content ID gaps, and notifies the Distribution Agent -- delivering royalty-brief.md. Use when the user wants to track your royalties on dsps."
---

# Track your royalties on DSPs

- **Subagent:** @pro-agent
- **Category:** Finance
- **NPAO:** A
- **List price:** $25
- **Source:** Account Management

## When to use
Key-sheet-linked royalty pulse and gap alerts.

## Steps
1. Ingest statements
2. WoW deltas
3. Flag Content ID gaps
4. Notify Distribution Agent

## Outputs
royalty-brief.md

## Reference tools
- mcp__supabase royalty_ledger

## Guardrails
Estimates aren't statements.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `statements` -- royalty statements to ingest
- `key_sheet` -- the key-sheet-linked ledger (mcp__supabase royalty_ledger)

## Example

Monthly statements ingested -> week-over-week deltas computed -> 2 Content ID gaps flagged -> Distribution Agent notified -> royalty-brief.md summarizes the pulse.

## Errors & edge cases

- **Estimates presented as statements** -- estimates aren't statements (guardrail); label them clearly.
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
