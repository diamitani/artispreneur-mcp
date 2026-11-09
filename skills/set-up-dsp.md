---
name: set-up-dsp
description: "Claims the artist's profiles across Spotify, Apple Music, and YouTube -- distributor invite, Apple Music for Artists, and the YouTube Official Artist Channel via the YouTube Data API -- delivering dsp-claim-steps.md. Use when the user wants to set up dsp artist profiles."
---

# set up DSP

- **Subagent:** @distribution-agent
- **Category:** Release
- **NPAO:** N
- **List price:** $15
- **Source:** Distribution Account Setup

## When to use
Spotify/Apple/YouTube artist profile claim.

## Steps
1. Distributor invite
2. Apple Music for Artists
3. YouTube OAC via mcp__youtube_data_api

## Outputs
dsp-claim-steps.md

## Reference tools
- https://artists.spotify.com
- https://artists.apple.com
- mcp__youtube_data_api

## Guardrails
User completes identity OAuth.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `distributor_account` -- for the distributor invite step
- `artist_identity` -- the user completes identity OAuth themselves (guardrail)

## Example

A new single: distributor invite accepted -> Apple Music for Artists claimed -> YouTube Official Artist Channel requested via mcp__youtube_data_api -> dsp-claim-steps.md records the completed claims.

## Errors & edge cases

- **Identity OAuth** -- the user must complete it; the agent cannot claim profiles on their behalf.
- **Dependent capability missing** (e.g. no YouTube Data API access) -- name it and stop; the parent handoff summarizes artifacts + blockers.
