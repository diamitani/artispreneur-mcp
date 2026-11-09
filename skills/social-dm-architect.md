---
name: social-dm-architect
description: "Writes platform-aware social DMs -- LinkedIn (professional but warm, 2-3 short paragraphs), Twitter/X (ultra-concise), Instagram (casual, emoji-friendly) -- each with a hook tied to the recipient's recent activity, a low-friction CTA, and 2-3 hook variations for A/B testing. Use when generating LinkedIn, Twitter/X, and social media DMs for outreach, follow-ups, and networking."
---

# Social DM Architect

## Overview
Generates platform-aware direct messages for LinkedIn, Twitter/X, and other social platforms. Each platform has distinct norms — LinkedIn skews professional, Twitter rewards brevity, Instagram favors casual. This skill tailors messaging accordingly.

## When to Use
- Cold outreach DMs on LinkedIn to prospects, recruiters, or partners
- Follow-up DMs after connecting, events, or interactions
- Networking DMs for intros, mentorship requests, or collaboration
- Twitter/X DMs for quick outreach, feedback, or relationship building
- Multi-platform campaigns requiring platform-specific message variants

## How It Works
1. Identify the platform (LinkedIn, Twitter/X, Instagram, etc.) and the recipient's context.
2. Determine the goal: connection, meeting, pitch, feedback, or relationship.
3. Draft a message that respects platform character limits, tone, and norms.
4. Include a natural hook tied to the recipient's recent activity, content, or mutual connection.
5. Polish for brevity — DMs have lower attention spans than email.

## Steps
1. **Platform check** — Confirm platform (LinkedIn, Twitter/X, etc.) and any character limits.
2. **Context gathering** — Ask for: recipient name/role, recent trigger (post, event, mutual connection), and goal.
3. **Draft the message** — Lead with the hook, state intent clearly, add a low-friction CTA (e.g., "Would you be open to a 15-min chat?").
4. **Platform polish** — LinkedIn: professional but warm, 2-3 short paragraphs. Twitter/X: ultra-concise, 1-2 sentences max. Instagram: casual, emoji-friendly.
5. **Offer alternatives** — Provide 2-3 hook variations or CTAs for A/B testing.

## Common Pitfalls
- **Pitch-slapping**: Leading with a sales pitch in the first DM burns bridges. Build rapport first.
- **Ignoring platform norms**: A formal LinkedIn message on Twitter feels stiff; a casual tweet-style DM on LinkedIn feels unprofessional.
- **No hook**: "Hi, I'd like to connect" gets ignored. Reference a post, shared connection, or common interest.
- **Overly long**: LinkedIn accept 300-500 chars in first DM; Twitter/X only 140-280 chars. Anything longer loses impact.
- **Generic template feel**: Even with a template, insert one genuine personal detail.

## Inputs

- `platform` -- LinkedIn, Twitter/X, Instagram, etc. (determines character limits, tone, norms)
- `recipient` -- name, role, and context
- `trigger` -- recent post, event, or mutual connection to hook on
- `goal` -- connection, meeting, pitch, feedback, or relationship

## Outputs

- A drafted DM: hook (tied to the trigger) -> clear intent -> low-friction CTA (e.g. "Would you be open to a 15-min chat?")
- 2-3 hook or CTA variations for A/B testing, polished per platform

## Example

LinkedIn cold outreach to a VP of Engineering who just posted about scaling infra: hook references the post ("your thread on sharding resonated -- we hit the same wall at..."), 3 short paragraphs, CTA "open to a 15-min chat next week?", plus 2 alternate hooks.

## Errors & edge cases

- **Pitch-slapping** -- leading with a sales pitch in the first DM burns bridges; build rapport first.
- **Ignoring platform norms** -- a formal message on Twitter feels stiff; a tweet-style DM on LinkedIn feels unprofessional.
- **No hook** -- "Hi, I'd like to connect" gets ignored; reference a post, shared connection, or common interest.
- **Overly long** -- LinkedIn: 300-500 chars for the first DM; Twitter/X: 140-280. Longer loses impact.
- **Generic template feel** -- even with a template, insert one genuine personal detail.
