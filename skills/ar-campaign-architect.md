---
name: ar-campaign-architect
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to plan multi-channel A&R release campaigns for independent artists: artist intake, channel mapping (playlists, blogs, venues, radio, social, sync), a 4-8 week phased timeline (pre-release teasers -> release-week push -> post-release sustain), and an asset checklist with deadlines. Use when designing A&R strategies for artist campaigns across blogs, playlists, venues, and licensing platforms."
---

# A&R Campaign Architect

## Overview
Designs multi-channel A&R (Artist & Repertoire) campaign strategies for independent artists. Plans promotion across blogs, playlists, venues, radio, social media, and sync licensing platforms — all tailored to the artist's genre, budget, and career stage.

## When to Use
- An artist is planning a single or album release and needs a promo roadmap
- Building a multi-month campaign with phased rollouts
- Identifying which channels (Spotify playlists, blogs, TikTok, local venues) to target
- Creating a timeline with clear milestones and deliverables

## How It Works
1. **Artist intake**: Gather genre, release type, budget, timeline, and existing assets (press photos, music videos, etc.).
2. **Channel mapping**: Identify the most impactful channels for the artist's genre and audience.
3. **Timeline**: Build a phased campaign (pre-release teasers → release week push → post-release sustain).
4. **Asset checklist**: List all needed assets (press release, one-sheet, social content, playlist pitch).
5. **Action plan**: Deliver a week-by-week or day-by-day plan with specific tasks.

## Steps
1. Ask about the release: single, EP, or album? Release date?
2. Ask about budget range and any existing team (manager, PR, etc.).
3. Map channels: DSP playlists (Spotify/Apple), music blogs, social media (TikTok, Instagram, YouTube), local press, radio, sync.
4. Build a 4-8 week campaign timeline with phases:
   - **Pre-release** (4 weeks out): Teasers, pre-save campaigns, press outreach.
   - **Release week**: Full push — playlist pitching, social blitz, blog premieres.
   - **Post-release** (2-4 weeks): Sustained playlist push, live shows, sync submissions.
5. Create asset checklist and assign deadlines.
6. Deliver the plan in a clear, actionable format.

## Common Pitfalls
- **Starting too late**: Playlist pitching needs 2-4 weeks lead time. Press needs even more.
- **Spreading too thin**: Focus on 3-4 high-impact channels instead of trying everything.
- **No follow-through**: The post-release sustain phase is where most campaigns die.

## Source
Originally from the Artispreneur Custom GPT portfolio.

## Inputs
- `release_type` (enum: single / EP / album, required) and `release_date` (date, required)
- `genre` (string, required) - drives channel selection
- `budget` (string) - budget range; `team` (string) - existing manager/PR/help
- `assets` (list) - press photos, videos, EPK, existing audience numbers

## Outputs
- Channel map: 3-4 high-impact channels matched to genre and audience
- 4-8 week phased campaign timeline with milestones and deliverables
- Asset checklist with deadlines (press release, one-sheet, social content, playlist pitch)

## Example
Input: indie-rock single, release in 8 weeks, $800 budget, no PR team.
1. Intake: DIY artist, 3k monthly listeners, press photos on hand.
2. Channel map: Spotify editorial/user playlists, 5 genre blogs, TikTok, 3 local venues.
3. Timeline: weeks 8-5 pre-save + press outreach; release week playlist blitz + blog premieres; weeks +1..+4 sustain push + sync submissions.
4. Asset checklist: one-sheet, 30s teaser, playlist pitch email - deadlines set 2 weeks before each phase.
