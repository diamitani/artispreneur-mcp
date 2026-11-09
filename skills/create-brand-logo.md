---
name: create-brand-logo
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to produce the written logo brief a designer or image model works from - never the art itself: lock 3 brand adjectives first, specify the wordmark as a typeface category, define primary/stacked/monochrome lockups with minimum sizes, foil-on-black minimums, clear-space rules, and a never-do list - delivering logo-brief.md with no invented visual style. Use when the user wants to create a brand logo."
---

# create brand logo

- **Subagent:** @epk-agent
- **Category:** Brand
- **NPAO:** P
- **List price:** $19
- **Source:** Branding Kit

## When to use
Wordmark/lockup brief.

## Steps
1. Wordmark
2. lockup
3. foil-on-black notes
4. clear space/min size

## Outputs
logo-brief.md

## Reference tools
- reference/templates/logo-brief.md

## Guardrails
Brief only, not fake art. This skill produces the written brief a
designer or image model works from — it never renders the logo itself.
Never invent a visual style the artist hasn't approved.

## How to run it
1. Lock the 3 brand adjectives first — every later decision refers back
   to them.
2. Specify the wordmark direction as a typeface category (condensed
   grotesque, hand-drawn serif), not a specific font unless it's
   licensed for the project.
3. Define the primary lockup plus stacked and monochrome variants, with
   minimum sizes for digital and print.
4. If the brand uses foil-on-black, note foil-safe minimums: no hairlines
   under 1pt, no reversed small type under 8pt.
5. Close with clear-space rules and a never-do list (stretch, recolor,
   drop shadows, busy backgrounds without a scrim).

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `brand_adjectives` (list of 3, required) - locked first; every later decision refers back
- `wordmark_direction` (string) - typeface category (condensed grotesque, hand-drawn serif), not a specific font unless licensed
- `variants` (list) - primary, stacked, monochrome lockups with digital/print minimum sizes
- `foil_on_black` (boolean) - if true, note foil-safe minimums

## Example
Input: logo brief for a lo-fi beat label.
1. Lock adjectives: warm, dusty, understated.
2. Wordmark: hand-drawn serif category; primary + stacked + monochrome lockups.
3. Minimums: 120px digital, 1in print; foil-safe: no hairlines under 1pt, no reversed type under 8pt.
4. Clear-space rules + never-do list (stretch, recolor, drop shadows); write logo-brief.md.

## Errors & edge cases
- Brief only, not fake art: never render the logo itself.
- Unapproved visual style: never invent one the artist hasn't approved - brief from their direction.
- Missing adjectives: stop and lock them first; nothing else in the brief is decidable without them.
