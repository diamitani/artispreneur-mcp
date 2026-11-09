---
name: epk-builder-gpt
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to craft professional Electronic Press Kits - the digital resume for pitching venues, festivals, blogs, labels, and sync supervisors: three bio lengths (100/250/500 words), curated highlights (3-5 press quotes, notable shows, streaming numbers), and a clean 1-2 page one-sheet formatted for PDF export - story-first bios, gatekeeper-length discipline, always with clear booking contact. Use when creating Electronic Press Kits for musicians."
---

# EPK Builder GPT

## Overview
Crafts professional Electronic Press Kits (EPKs) for musicians. An EPK is a digital resume for artists — used to pitch to venues, festivals, blogs, labels, and sync supervisors. This skill produces all EPK components: artist bio, press photos guidance, music links, press quotes, tour history, and contact info.

## When to Use
- An artist needs an EPK to submit to venues or festivals
- Pitching to music blogs, playlist curators, or record labels
- Preparing for a release campaign (EPK is often the first thing gatekeepers see)
- Updating an outdated EPK with new music, press, and assets

## How It Works
1. **Gather assets**: Collect bio info, music links, press quotes, photos, tour dates, accolades.
2. **Write the bio**: Short (100 words), medium (250 words), and long (500 words) versions.
3. **Curate highlights**: Select top 3-5 press quotes, notable shows, and streaming numbers.
4. **Structure the EPK**: One-sheet format — everything on 1-2 pages.
5. **Deliver**: Clean, formatted EPK ready for PDF export.

## Steps
1. Ask for the artist's name, genre, location, and primary links (Spotify, website, socials).
2. Gather career highlights: notable shows, press coverage, awards, streaming milestones.
3. Write three bio lengths:
   - **Short bio** (100 words): One paragraph, elevator pitch.
   - **Standard bio** (250 words): For EPK main page, 2-3 paragraphs.
   - **Long bio** (500 words): Full story for website/about page.
4. Compile press quotes (with publication names and dates).
5. List discography with streaming links.
6. Include high-res photo guidance (what to include, specs).
7. Add contact/booking information.
8. Format into a clean one-sheet layout.

## Common Pitfalls
- **Bio reads like a resume**: Tell a story, not a timeline. Focus on what makes the artist unique.
- **Too long**: Gatekeepers skim. Lead with the strongest hook.
- **Missing contact info**: An EPK without clear booking contact is useless.
- **Outdated assets**: Always use current streaming numbers and recent press.

## Source
Originally from the Artispreneur Custom GPT portfolio. Consolidates the EPK Builder and EPK Creator GPTs.

## Inputs
- `artist` (string, required): name, genre, location, primary links
- `highlights` (list): notable shows, press coverage, awards, streaming milestones
- `press_quotes` (list) - with publication names and dates
- `photos` (list) - high-res photo guidance; `contact` (string) - booking info

## Outputs
- Three bio lengths: short (100 words, elevator pitch), standard (250), long (500, full story)
- Discography with streaming links; curated top 3-5 press quotes
- Clean one-sheet layout ready for PDF export

## Example
Input: EPK for a soul singer ahead of festival season.
1. Gather: name, genre, location, links; highlights (2 festival slots, 1.2M streams on the single).
2. Bios: 100-word elevator pitch, 250-word main, 500-word full story - story, not timeline.
3. Curate 4 press quotes with publications/dates; discography with links; booking contact prominent.
4. One-sheet, 1-2 pages, PDF-ready.
