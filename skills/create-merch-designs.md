---
name: create-merch-designs
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to draft SKU concepts for e-commerce/merch: 3 SKUs with prices, print notes from the brand guide, 72-hour drop copy - following the artist's brand guidelines when owned, producing merch-brief.md from the merch-brief template. Use when the user wants to create merch designs."
---

# create merch designs

- **Subagent:** @website-agent
- **Category:** Merch
- **NPAO:** O
- **List price:** $25
- **Source:** E-Commerce/Merch

## When to use
SKU concepts for E-Commerce/Merch.

## Steps
1. 3 SKUs
2. prices
3. print notes from brand guide
4. 72h drop copy

## Outputs
merch-brief.md

## Reference tools
- reference/templates/merch-brief.md

## Guardrails
Follow brand guidelines if owned.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `brand` (string) - brand guide if owned; print notes derive from it
- `skus` (list, default: 3) - product concepts
- `drop_window` (string, default: 72h) - drop copy timeline

## Example
Input: merch for an EP drop.
1. 3 SKUs: heavyweight tee, embroidered hoodie, lyric-poster bundle; prices set.
2. Print notes from the brand guide (ink colors, placement).
3. 72-hour drop copy written; merch-brief.md saved from the template.

## Errors & edge cases
- No brand guide: proceed with neutral design notes and flag the gap - never invent brand rules.
- Pricing unknown: use placeholder ranges and mark them for the artist to confirm.
