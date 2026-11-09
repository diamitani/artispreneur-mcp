---
name: release-music-with-dsp
description: "Builds a DSP release ticket on a 21-day store-date buffer -- confirms splits are signed, assembles WAV + artwork + metadata, picks the distributor, and writes the release_tickets row -- delivering release-ticket.md. Use when the user wants to release your music with a dsp."
---

# Release your music with a DSP

- **Subagent:** @distribution-agent
- **Category:** Release
- **NPAO:** P
- **List price:** $29
- **Source:** Streaming guide + Distribution Account Setup

## When to use
Release ticket, 21-day buffer.

## Steps
1. Confirm splits signed
2. WAV+art+metadata
3. pick distributor
4. set store date +21d
5. write release_tickets row

## Outputs
release-ticket.md

## Reference tools
- reference/templates/release-ticket.md
- mcp__supabase

## Guardrails
No release without signed splits.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `release_assets` -- final WAV(s), cover art, full metadata
- `distributor` -- the chosen distribution service
- `store_date` -- release date, set at least 21 days out (the buffer)

## Example

Single release: splits confirmed signed -> WAV + art + metadata assembled -> distributor picked -> store date set 21 days out -> release ticket written to the release_tickets table -> release-ticket.md.

## Errors & edge cases

- **Unsigned splits** -- no release without signed splits; the ticket is blocked until they are confirmed.
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
