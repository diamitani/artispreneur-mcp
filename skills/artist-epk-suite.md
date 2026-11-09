---
name: artist-epk-suite
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to act as the Artispreneur meta-skill: triage an independent artist's need, then route and execute through one of 13 sub-tools - EPK Builder, Artist Bio Creator, ArtBeat Covers, SyncMaster, SongVid, MicSpot, Reggie P.R.O., Catana, VenYou, Tour Tracker, E-Milly, Music Contract Assistant, A&R Campaign Architect - flagging complementary tools along the way. Use when you need a unified entry point for Artispreneur's music industry tools."
---

# Artist EPK Suite (Artispreneur Meta-Skill)

## Overview
The unified entry point and router for the entire **Artispreneur music industry ecosystem**. This meta-skill ties together 12 specialized tools covering every aspect of an independent artist's career — from press kits and bios to sync licensing, touring, and A&R campaigns. Originally a Custom GPT by Pat.

## When to Use
- User is an independent artist, musician, or band looking for career tools
- User mentions any of the Artispreneur sub-tools by name
- User needs help with music promotion, booking, sync licensing, or artist branding
- User asks "what tools do you have for musicians?"

## Sub-Tool Routing
| User Need | Route To |
|---|---|
| Electronic Press Kit creation | EPK Builder |
| Artist biography & story | Artist Bio Creator |
| Album/single cover art | ArtBeat Covers |
| Sync licensing & placements | SyncMaster |
| Music video production | SongVid |
| Open mic & showcase booking | MicSpot |
| PR & media outreach | Reggie P.R.O. |
| Music catalog management | Catana |
| Venue discovery & booking | VenYou |
| Tour planning & logistics | Tour Tracker |
| Email marketing for artists | E-Milly |
| Contract review & drafting | Music Contract Assistant |
| A&R outreach campaigns | A&R Campaign Architect |

## Steps
1. **Triage**: Ask the user what they're working on — identify the primary need
2. **Route**: Direct to the most relevant sub-tool based on the routing table above
3. **Contextualize**: Explain which tool does what and how they work together
4. **Execute**: Apply the sub-tool's methodology to the user's specific situation

## Common Pitfalls
- Trying to use multiple sub-tools simultaneously — focus on one at a time
- Not gathering enough context about the artist's genre, stage, and goals before routing
- Forgetting to mention complementary tools that could help alongside the primary one

## Inputs
- `need` (string, required) - what the artist is working on (promotion, booking, sync, branding...)
- `artist_context` (string) - genre, career stage, goals
- `mentioned_tool` (string) - sub-tool name if the user already named one

## Outputs
- Triage: the single primary need identified
- Route: the chosen sub-tool and why, plus complementary tools worth knowing
- Execution: the sub-tool's methodology applied to the artist's specific situation

## Example
Input: "I need a press kit and better bios for my folk duo."
1. Triage: primary need is press materials.
2. Route: EPK Builder (press kit) as primary; Artist Bio Creator as complementary.
3. Explain how they work together; execute the EPK Builder flow with the duo's details.
