---
name: upload-music-video-to-youtube
description: "Publishes a music video to YouTube with the full packet -- title formula, description with credits + shortened link, chapters, end screens -- published via the YouTube Data API with the upload confirmed via API, never merely claimed. Use when the user wants to upload music video to youtube."
---

# upload music video to youtube

- **Subagent:** @social-media-agent
- **Category:** Content
- **NPAO:** P
- **List price:** $12
- **Source:** Content Creation

## When to use
YouTube packet: title/desc/chapters, confirmed via API.

## Steps
1. Title formula
2. desc credits+mcp__bitly link
3. chapters
4. end screens
5. publish via mcp__youtube_data_api

## Outputs
youtube-packet.md

## Reference tools
- mcp__youtube_data_api
- mcp__bitly

## Guardrails
Don't claim upload without API confirmation.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `video` + `metadata` -- the video file; title elements, credits, chapter timestamps for the packet

## Example

A finished video: title formula applied -> description with credits + mcp__bitly link -> chapters -> end screens -> published via mcp__youtube_data_api -> youtube-packet.md records the API-confirmed upload.

## Errors & edge cases

- **Claiming upload without API confirmation** -- don't (guardrail); the packet is only done when the API confirms.
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
