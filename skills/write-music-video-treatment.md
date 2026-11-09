---
name: write-music-video-treatment
description: "Writes a scene-by-scene music video treatment -- concept, 3-act structure, shot list, and budget bands ($1.5k/$8k/$25k) -- delivering treatment.md. Use when the user wants to write a music video treatment."
---

# Write a music video treatment

- **Subagent:** @social-media-agent
- **Category:** Content
- **NPAO:** P
- **List price:** $25
- **Source:** Content Creation

## When to use
Scene-by-scene treatment with budget bands.

## Steps
1. Concept
2. 3 acts
3. shot list
4. budgets $1.5k/$8k/$25k

## Outputs
treatment.md

## Reference tools
- reference/templates/treatment.md

## Guardrails
No celebrity cameo promises.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `song` + `concept` -- the track and the creative concept
- `budget_band` -- $1.5k, $8k, or $25k (drives the shot list scale)

## Example

An indie single at the $8k band: concept -> 3-act structure -> shot list scoped to budget -> treatment.md from the reference template.

## Errors & edge cases

- **Celebrity cameo promises** -- never (guardrail: no celebrity cameo promises).
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
