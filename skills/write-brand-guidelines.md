---
name: write-brand-guidelines
description: "Writes brand guidelines -- voice, hex palette, typography, and merch do's/don'ts -- enforced across marketing and published to Notion, delivering brand-guidelines.md. Use when the user wants to write brand guidelines."
---

# write brand guidelines

- **Subagent:** @marketing-agent
- **Category:** Brand
- **NPAO:** P
- **List price:** $29
- **Source:** Branding Kit + Marketing

## When to use
Voice/palette/type/merch rules enforced across marketing.

## Steps
1. Voice
2. hex palette
3. type
4. merch do/don't
5. publish to Notion

## Outputs
brand-guidelines.md

## Reference tools
- reference/templates/brand-guidelines.md
- mcp__notion

## Guardrails
Keep accessible contrast.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `brand_inputs` -- voice samples, logo/palette source, type preferences, merch line

## Example

A startup rebrand: voice defined -> hex palette locked -> type scale set -> merch do's/don'ts -> published to Notion via mcp__notion -> brand-guidelines.md.

## Errors & edge cases

- **Inaccessible contrast** -- keep accessible contrast (guardrail); check palette pairs.
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
