---
name: create-an-epk-rostr-core
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build a complete electronic press kit for an independent artist - bio in three lengths, press quotes, music links, photos, tour dates, contact - assembled into a publishable markdown page with strict guards: bio_facts required and never invented, real quotes with attribution or an exact placeholder, never publish or send (file produced and stopped). Use when building a complete electronic press kit for an independent artist."
---

# Skill: create-an-epk

**Price:** $29 one-time
**Version:** 1.0

## Description
Build a complete electronic press kit for an independent artist: bio,
press quotes, music links, photos, tour dates, and contact — assembled
into a publishable page.

## When to use
The user wants a press kit / EPK for an artist. Trigger phrases: "make an
EPK", "press kit", "one-sheet".

## Inputs
- artist_name (required)
- genre (required)
- bio_facts: 3–10 bullet facts about the artist (required — never invent these)
- music_links: streaming URLs (optional)
- press_quotes: real quotes with attribution (optional — see guardrails)
- photo_url: press photo URL (optional)
- contact_email (optional)

## Steps
1. **Collect.** Confirm artist_name, genre, and bio_facts. If any are
   missing, ask once, then proceed with what's given.
2. **Bio.** Write three lengths from the facts: short (50 words), standard
   (150 words), long (300 words). Same facts, different depth.
3. **Press quotes.** Use ONLY supplied quotes with real attribution. If
   none were supplied, insert exactly: `[PRESS QUOTE PLACEHOLDER — add real
   quotes before publishing]`. Never invent a quote or attribute one.
4. **Assemble.** Produce one markdown document with sections: header
   (name/genre/location), bio (three lengths), music links, press quotes,
   tour dates, contact.
5. **Save.** Write the finished press kit to a new markdown file you
   generate for this artist (for example in your working directory or the
   artist's press folder), using the write_file tool.

## Outputs
- The finished press kit document — a generated markdown file containing
  the header, three bio lengths, music links, press quotes, tour dates,
  and contact sections.

## Guardrails
- NEVER invent press quotes, stats, or achievements. Placeholder > fiction.
- NEVER publish or send anything — produce the file and stop. Publishing
  is a separate, human-approved step.
- Keep the artist's voice: read the bio_facts for tone before writing.

## Example
Input: EPK for an R&B singer, 6 bio facts, no press quotes yet.
1. Collect: artist_name, genre confirmed; bio_facts = 6 real bullets.
2. Bio: 50 / 150 / 300 words from the same facts.
3. Press quotes: none supplied -> insert exactly `[PRESS QUOTE PLACEHOLDER - add real quotes before publishing]`.
4. Assemble the markdown with header, bios, music links, tour dates, contact; write the file; stop - publishing is a separate human-approved step.

## Errors & edge cases
- bio_facts missing: ask once, then proceed with what is given - never invent facts.
- Invented quotes/stats/achievements: forbidden; the exact placeholder is the only substitute.
- Asked to publish or send: refuse - produce the file and stop.
