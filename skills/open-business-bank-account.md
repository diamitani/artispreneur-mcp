---
name: open-business-bank-account
description: "Assembles a business bank account opening kit — gathers the EIN letter, Articles PDF, and ID, compares business accounts, and routes payouts — delivering a `bank-kit.md` and a parent handoff with artifacts and blockers. Category: Finance · NPAO: N · Subagent: @legal-setup · Source: Legal sequence. Use when the user wants to open a business bank account."
---

# open business bank account

- **Subagent:** @legal-setup
- **Category:** Finance
- **NPAO:** N
- **List price:** $12
- **Source:** Legal sequence

## When to use
Docs list + bank comparison.

## Steps
1. EIN letter
2. Articles PDF
3. ID
4. compare accounts
5. route payouts

## Outputs
bank-kit.md

## Reference tools
- mcp__google_drive

## Guardrails
Never mix personal rent.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- EIN letter
- Articles (PDF)
- Owner ID
- Payout routing preferences (where business income should route)
- Execution: Subagent @legal-setup · Reference tool: `mcp__google_drive`

## Example

New LLC needs an account: collect EIN letter + Articles PDF + owner ID → compare business accounts (fees, minimums, payout routing) → `bank-kit.md` with the docs list and the recommended account → parent handoff: artifacts complete, blockers none. Guardrail observed: business funds stay separate from personal rent.

## Errors & edge cases

- **Dependent skill/capability missing** (e.g. `mcp__google_drive`) → name it and stop; report it in the parent handoff as a blocker.
- **Missing EIN letter, Articles PDF, or ID** → blocker: surface in the parent handoff instead of proceeding without documentation.
- **Guardrail: never mix personal rent** — business banking stays separate from personal funds.
