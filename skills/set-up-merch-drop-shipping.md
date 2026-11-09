---
name: set-up-merch-drop-shipping
description: "Stands up merch fulfillment -- print-on-demand (Printful/Printify) vs. warehouse above 200 units, USPS Ground shipping, and insert cards -- delivering merch-ops.md. Use when the user wants to set up merch drop shipping."
---

# set up merch drop shipping

- **Subagent:** @website-agent
- **Category:** Merch
- **NPAO:** O
- **List price:** $25
- **Source:** E-Commerce/Merch

## When to use
POD vs warehouse for E-Commerce/Merch.

## Steps
1. Printful/Printify test
2. warehouse if >200
3. USPS ground
4. insert card

## Outputs
merch-ops.md

## Reference tools
- reference/templates/merch-ops.md

## Guardrails
No fake carrier accounts.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `fulfillment_model` -- POD (Printful/Printify test run) vs. warehouse (above ~200 units)
- `product_line` -- the merch items to fulfill

## Example

A 50-unit test run: Printful POD -> USPS Ground shipping -> branded insert card -> merch-ops.md documents the ops setup from the reference template.

## Errors & edge cases

- **No fake carrier accounts** -- real carrier setup only (guardrail).
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
