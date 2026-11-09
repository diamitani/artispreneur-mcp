---
name: license-music
description: "Produces a filled sync/license brief (`license-brief.md`) from the user's ‘How To License Your Music’ document — defining the use, composition vs master rights, territory/term/fee, and credit line — via the @music-contract-agent subagent, saved to Google Drive. Use when the user wants to license your music."
---

# License your music

- **Subagent:** @music-contract-agent
- **Category:** Legal
- **NPAO:** O
- **List price:** $19
- **Source:** the user's "How To License Your Music" document (a user-supplied .docx — not bundled with this skill; the user provides their copy)

## When to use
Sync/license brief, licensing sub-capability.

## Steps
1. Define use
2. composition vs master
3. territory/term/fee
4. credit line
5. save to mcp__google_drive

## Outputs
A filled license brief (license-brief.md) — a generated artifact saved for the user, based on `reference/templates/license-brief.md`.

## Reference tools
- reference/templates/license-brief.md
- mcp__google_drive

## Guardrails
Not legal advice.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `use` (required) — the sync/license placement being briefed (film, ad, trailer, game…)
- `rights` (required) — composition vs master (or both)
- `territory` / `term` / `fee` (required) — e.g. worldwide, 5 years, $1,500
- `credit_line` (required) — e.g. ‘Song Title — Artist Name’
- Source: the user's ‘How To License Your Music’ .docx (user-supplied, not bundled); template: `reference/templates/license-brief.md`; subagent: @music-contract-agent

## Example

An indie film wants the song for its trailer → use: trailer sync; rights: master + composition; territory: worldwide, term 5 years, fee $1,500; credit line: ‘Song Title — Artist Name’ → filled `license-brief.md` generated from `reference/templates/license-brief.md` and saved via `mcp__google_drive`. List price $19 · Category: Legal · NPAO: O.

## Errors & edge cases

- **Not legal advice.** The brief is a deal artifact, not counsel — say so in the handoff.
- **Source document is user-supplied** (a .docx, not bundled) — if the user hasn't provided their copy, ask before drafting.
- **Dependent skill/capability missing** → name it and stop (per the parent handoff rule); summarize artifacts + blockers either way.
