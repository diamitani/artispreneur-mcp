---
name: create-an-epk
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to assemble a full electronic press kit: bio, focus track + links, press photos, tech rider stub, one-sheet - saved to Drive as EPK.md from the epk template, with a hard no-fake-press-quotes guardrail and a parent handoff summarizing artifacts and blockers. Use when the user wants to create an epk."
---

# Create an EPK

- **Subagent:** @epk-agent
- **Category:** Brand
- **NPAO:** P
- **List price:** $29
- **Source:** Media Kit

## When to use
Full media kit / EPK.

## Steps
1. Bio
2. focus track+links
3. press photos
4. tech rider stub
5. one-sheet
6. save to Drive

## Outputs
EPK.md

## Reference tools
- reference/templates/epk.md
- mcp__google_drive

## Guardrails
No fake press quotes.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `artist` (string, required) - artist name and context
- `bio` (string) - artist bio (use create-an-artist-bio for the three lengths)
- `focus_track` (string) + `links` (list) - streaming URLs
- `press_photos` (list), `tech_rider` (string), `one_sheet` (string)

## Example
Input: EPK for a folk duo with a new single.
1. Bio from create-an-artist-bio; focus track + Spotify/Apple links; 3 press photos.
2. Tech rider stub (stage plot needs, inputs); one-sheet summary.
3. Assemble EPK.md from reference/templates/epk.md; save via mcp__google_drive.
4. Parent handoff: artifacts + blockers.

## Errors & edge cases
- No fake press quotes: if none supplied, omit or mark clearly - never invent one.
- mcp__google_drive unavailable: name the missing dependency in the parent handoff and stop.
- Missing photos or rider details: note as blockers in the handoff rather than inventing them.
