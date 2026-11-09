---
name: extract-metadata-from-track
description: "LLM-agnostic data engineering and analytics skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to produce a clean ISRC/writers/BPM/key JSON record for a track, ready for distribution: read audio-file tags, session notes, or split sheets; normalize the ISRC (uppercase, 12 chars, never invented); copy writers/PRO/publisher/shares exactly from the signed split sheet (flagging non-100% totals); validate the filled metadata.json template before handoff. Use when the user wants to extract metadata from a track."
---

# Extract Metadata from Track

- **Subagent:** @distribution-agent
- **Category:** Catalogue
- **NPAO:** N
- **List price:** $9
- **Source:** Catalogue

## When to use
Produce a clean ISRC/writers/BPM/key JSON record for a track, ready for
distribution. Use when the user wants metadata extracted from a track —
from audio-file tags, a split sheet, or session notes.

## Steps
1. Read tags/input: pull whatever the audio file, session notes, or user
   message already states (title, artist, BPM, key, duration, existing ISRC).
2. Normalize ISRC: uppercase, strip spaces and dashes, expect 12 characters
   (country code + registrant + year + designation). If no ISRC exists yet,
   leave the field empty and flag it — do not invent one.
3. Writers from split sheet: copy each writer's name, PRO affiliation,
   publisher, and share percent exactly as the signed split sheet states.
   Shares should total 100%; if they do not, flag the discrepancy instead of
   adjusting numbers.
4. Fill the template at `reference/templates/metadata.json` and validate
   that it parses as JSON before handing it off.

## Outputs
A filled metadata.json following `reference/templates/metadata.json`.

## Reference tools
- reference/templates/metadata.json

## Guardrails
Never invent ISRC.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `source` (file/string, required) - audio file, session notes, or user message with tags
- `split_sheet` (file) - signed split sheet for writers, PRO affiliations, publishers, shares
- `template` (path, default: reference/templates/metadata.json)

## Outputs
- Filled metadata.json: title, artist, ISRC, writers, BPM, key, duration - validated to parse as JSON

## Example
Input: extract metadata for a single from the WAV tags + split sheet.
1. Read tags: title, artist, BPM 118, key Am, duration 3:24; existing ISRC present -> normalize to uppercase 12 chars.
2. Writers from the split sheet copied exactly (names, PRO, publisher, shares); shares total 100.
3. Fill reference/templates/metadata.json; validate it parses; hand off with the parent summary.

## Errors & edge cases
- Never invent ISRC: if none exists, leave the field empty and flag it.
- Shares don't total 100%: flag the discrepancy - never adjust numbers yourself.
- mcp__supabase/mcp__google_drive unavailable: name the missing dependency in the parent handoff and stop.
