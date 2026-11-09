---
name: add-music-to-collaborative-playlist
description: "LLM-agnostic sales prospecting and go-to-market skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to run curated playlist-pitch outreach in Indie Bible tone: one personal line, a track+BPM+city subject, a single Bitly link, 3-10 targets logged in HubSpot and sent via Outlook only after human approval - delivering pitch-email.md and target-list.md. Use when the user wants to add music to collaborative playlist."
---

# add music to collaborative playlist

- **Subagent:** @outreach-agent
- **Category:** Outreach
- **NPAO:** O
- **List price:** $15
- **Source:** EMAIL TEMPLATES PLAYLISTS + Playlists cap

## When to use
Playlist pitch, Indie Bible tone, part of Messaging/Sequences.

## Steps
1. One personal line
2. subject track+BPM+city
3. one link (mcp__bitly)
4. 3-10 curated targets
5. log in mcp__hubspot
6. send via mcp__outlook after approval

## Outputs
pitch-email.md, target-list.md

## Reference tools
- reference/tools/directories.md
- mcp__hubspot
- mcp__outlook
- mcp__bitly

## Guardrails
Never dump full CSV. Max 10 targets/run. Human approves send.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `track` (string, required) - the song being pitched, title and artist name
- `bpm` (integer) and `city` (string) - feed the `track+BPM+city` subject format
- `targets` (list, 3-10) - curated playlist targets from reference/tools/directories.md
- `link` (URL) - exactly one shortened track link via mcp__bitly
- `approval` (human, required) - explicit go-ahead before any Outlook send

## Example
Input: pitching "Neon Waterfall" by Marina Vale (118 BPM, Chicago) to 6 indie-playlist curators.
1. Draft a one-line personal opener for each curator referencing their most recent playlist theme.
2. Subject: `Neon Waterfall - 118 BPM - Chicago`.
3. Shorten the streaming link with mcp__bitly; embed exactly one link.
4. Log all 6 targets in mcp__hubspot; send via mcp__outlook after the user approves.
Output: pitch-email.md (one personalized email) + target-list.md (6 targets with status).

## Errors & edge cases
- Missing dependency (no Bitly/HubSpot/Outlook connection): name it in the parent handoff and stop - do not improvise a different send path.
- More than 10 targets requested: run the first 10, queue the rest for a second run.
- No approval given: draft and log only; the send step stays blocked.
- Target list arrives as a full CSV dump: refuse - curate down to 10 max per Guardrails.
