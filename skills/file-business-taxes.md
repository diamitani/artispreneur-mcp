---
name: file-business-taxes
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to organize the quarterly-estimate + tax folder: pull the full-year ledger via connected accounting sources (Plaid/Supabase), collect and reconcile 1099s, work the Schedule C checklist from the tax-folder template, tally quarterly estimated payments against the due-date table with catch-up flags - then hand the completed folder to the CPA; the agent organizes, it does not file, and this is not tax advice. Use when the user wants to file business taxes."
---

# file business taxes

- **Subagent:** @legal-setup
- **Category:** Finance
- **NPAO:** A
- **List price:** $49
- **Source:** Finance

## When to use
Quarterly estimated payments plus an organized tax folder for the business:
income, expenses, receipts, Schedule C worksheet, and estimates tracking.

## Steps
1. Pull the full-year ledger via the connected accounting sources
   (Plaid / Supabase MCP tools or the user's own exports).
2. Collect 1099s (NEC, MISC, K) and reconcile income to the ledger.
3. Work the Schedule C checklist in `reference/templates/tax-folder.md`:
   gross receipts, COGS, categorized expenses, net profit sanity check.
4. Tally quarterly estimated payments against the due-date table in the
   template; flag any missed quarter for catch-up.
5. Hand the completed folder to the CPA for filing — the agent organizes,
   it does not file and this is not tax advice.

## Outputs
tax-folder-checklist.md

## Reference tools
- mcp__plaid
- mcp__supabase
- reference/templates/tax-folder.md

## Guardrails
Not tax advice; CPA files.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `year` (integer, required)
- `sources` (list) - Plaid / Supabase MCP tools or the user's own exports for the ledger
- `forms_1099` (list) - NEC, MISC, K forms to reconcile

## Example
Input: organize the 2026 tax folder.
1. Pull the full-year ledger via mcp__plaid; collect 1099s and reconcile income.
2. Work the Schedule C checklist in reference/templates/tax-folder.md: gross receipts, COGS, categorized expenses, net profit sanity check.
3. Tally quarterly estimates against the due-date table; flag the missed Q2 for catch-up.
4. tax-folder-checklist.md complete -> hand to the CPA for filing.

## Errors & edge cases
- Not tax advice; the agent never files - the CPA files.
- Ledger vs 1099 mismatch: reconcile before handing off; flag unresolved gaps.
- mcp__plaid/mcp__supabase unavailable: name the missing dependency in the parent handoff and stop.
