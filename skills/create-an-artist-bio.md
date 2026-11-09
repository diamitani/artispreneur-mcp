---
name: create-an-artist-bio
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to write 50/150/400-word artist bios from an interview-first flow: capture voice, hometown, genre, sonic references, and 3-5 real facts; draft the 50-word identity first, expand to 150 and 400 with the same facts and no new claims, end every version with momentum (current release or next move) - no fake awards, every claim from supplied facts, voice matched via the template checklist, producing bios.md. Use when the user wants to create an artist bio."
---

# Create an artist bio

- **Subagent:** @epk-agent
- **Category:** Brand
- **NPAO:** P
- **List price:** $12
- **Source:** Media Kit

## When to use
50/150/400 word bios.

## Steps
1. Capture voice/hometown/genre
2. 50w
3. 150w
4. 400w+CTA

## Outputs
bios.md

## Reference tools
- reference/templates/bio.md

## Guardrails
No fake awards. Every claim in the bio must come from supplied facts —
if the artist hasn't told you, it doesn't go in. Read the voice checklist
in the template before finalizing.

## How to run it
1. Interview first: hometown, genre, 2–3 sonic references, years active,
   and 3–5 real facts (releases, shows, press, story). Capture 1–2
   sentences in the artist's own words for voice matching.
2. Draft the 50-word version first — it forces the one-line identity.
3. Expand to 150 words for press, then 400 for features. Same facts,
   more depth; never new claims at longer lengths.
4. End every version with momentum: current release or next move plus
   where to hear it.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `interview` (object, required): hometown, genre, 2-3 sonic references, years active, 3-5 real facts (releases, shows, press, story), 1-2 sentences in the artist's own words for voice matching

## Example
Input: interview with a Chicago footwork producer, 3 releases, 6 years active.
1. Interview first: capture the facts and 2 sentences in her own words.
2. Draft the 50-word version - forces the one-line identity.
3. Expand to 150 (press) then 400 (features): same facts, more depth, never new claims.
4. Every version ends with momentum (current release + where to hear it); voice checklist read before finalizing; save bios.md.

## Errors & edge cases
- No fake awards: a claim not supplied by the artist does not go in - placeholder > fiction.
- Longer lengths tempting new claims: same facts at every length, only more depth.
- Voice mismatch: read the template's voice checklist before finalizing each version.
