---
name: manage-business-expenses
description: "Maintains the studio/ads/travel expense ledger via the @finance-manager subagent — pulls transactions through Plaid, tags categories, totals monthly, and writes expense rows to Supabase, delivering `expense-ledger.md`. Use when the user wants to manage business expenses."
---

# manage business expenes

- **Subagent:** @finance-manager
- **Category:** Finance
- **NPAO:** A
- **List price:** $15
- **Source:** Finance

## When to use
Studio/ads/travel ledger.

## Steps
1. Pull via mcp__plaid
2. tag category
3. monthly total
4. write mcp__supabase expenses row

## Outputs
expense-ledger.md

## Reference tools
- mcp__plaid
- mcp__supabase

## Guardrails
Not tax advice.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `transactions` via `mcp__plaid` (required) — the pull source
- `categories` — studio, ads, travel (tagged per transaction)
- `month` — the period being totaled
- Destination: the `mcp__supabase` expenses table (row writes)

## Example

October close: pull transactions via `mcp__plaid` → tag 42 transactions (studio / ads / travel) → monthly total $5,089 → write rows to the `mcp__supabase` expenses table → deliver `expense-ledger.md`. (List price $15 · Category: Finance · NPAO: A · Subagent: @finance-manager.)

## Errors & edge cases

- **Not tax advice.** The ledger is a tracking artifact — say so in the handoff.
- **Dependent skill/capability missing** → name it and stop; summarize artifacts + blockers either way.
