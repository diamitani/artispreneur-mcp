---
name: claim-tracks-with-pro
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to claim unmatched performances and digital uses with a PRO: open the unmatched queue, match ISRC/title, attach recordings, dispute hijacks - controlled works only - producing claim-queue.md with status updates via mcp__supabase. Use when the user wants to claim tracks with a P.R.O."
---

# Claim tracks with a P.R.O.

- **Subagent:** @pro-agent
- **Category:** Publishing
- **NPAO:** A
- **List price:** $15
- **Source:** PRO guide

## When to use
Claim unmatched performances/digital uses.

## Steps
1. Open unmatched queue
2. Match ISRC/title
3. Attach recordings
4. Dispute hijacks

## Outputs
claim-queue.md

## Reference tools
- mcp__supabase update status

## Guardrails
Only claim controlled works.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `works` (list, required) - controlled works to claim: title + ISRC per track
- `unmatched_queue` (string) - where the PRO's unmatched performances/digital uses live
- `recordings` (list) - recording files to attach as proof

## Example
Input: claim 3 controlled singles with unmatched Spotify uses.
1. Open the unmatched queue at the PRO.
2. Match each ISRC/title pair to its unmatched lines.
3. Attach the recordings; dispute any hijacked matches.
4. Update status in mcp__supabase; output claim-queue.md with claimed/pending/disputed.

## Errors & edge cases
- Work is not controlled by the user: do not claim it per Guardrails - flag it instead.
- Hijacked match found: dispute through the PRO's process; do not overwrite silently.
- mcp__supabase unavailable: name the missing dependency in the parent handoff and stop.
