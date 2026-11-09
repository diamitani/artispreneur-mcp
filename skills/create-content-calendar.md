---
name: create-content-calendar
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build a 30-day content calendar around an anchor release date: D-21 announce, D-14 visualizer, D0 premiere, D+3 follow-ups - scheduled in the artist's timezone, producing calendar.md from the content-calendar template. Use when the user wants to create a content calendar."
---

# create content calendar

- **Subagent:** @social-media-agent
- **Category:** Content
- **NPAO:** P
- **List price:** $15
- **Source:** Content Scheduling and Posting

## When to use
30-day calendar for Scheduling and Posting.

## Steps
1. Anchor store date
2. D-21 announce
3. D-14 visualizer
4. D0 premiere
5. D+3 follow-ups

## Outputs
calendar.md

## Reference tools
- reference/templates/content-calendar.md

## Guardrails
Respect artist timezone.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `anchor_date` (date, required) - the release/premiere date everything keys off
- `timezone` (string, required) - the artist's timezone; respected throughout
- `assets` (list) - announce creative, visualizer, premiere assets, follow-up content

## Example
Input: single premieres June 20, artist in America/Chicago.
1. Anchor: D0 = June 20.
2. D-21 (May 30): announce post; D-14 (June 6): visualizer drop; D0: premiere; D+3 (June 23): follow-ups.
3. All times in the artist's timezone; calendar.md from the template.

## Errors & edge cases
- Anchor date missing: stop - the whole calendar is computed from D0.
- Timezone unknown: ask once; never assume the artist's timezone.
- Assets missing for a beat: note it as a blocker in the parent handoff, keep the slot on the calendar.
