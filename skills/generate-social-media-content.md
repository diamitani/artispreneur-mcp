---
name: generate-social-media-content
description: "LLM-agnostic developer tooling skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to generate hooks, captions, CTAs, and story frames - one idea adapted per platform from the social-pack template: 3 true specific hooks (curiosity, value, identity - each provably true), per-platform captions (IG/TikTok, X/Threads, Shorts, Facebook), exactly one CTA per pack, 3-5 story frames with 5-word-max overlays, and the template's guardrails check before delivery - no engagement-bait lies. Use when the user wants to generate social media content."
---

# generate social media content

- **Subagent:** @social-media-agent
- **Category:** Content
- **NPAO:** P
- **List price:** $15
- **Source:** Content Creation

## When to use
Hooks, captions, CTAs, and story frames for Content Creation — one idea
adapted per platform from the social pack template.

## Steps
1. 3 hooks: write three true, specific hooks (curiosity, value, identity) —
   each must be provably true of the thing being promoted.
2. Captions: adapt the winning hook per platform (IG/TikTok, X/Threads,
   YouTube Shorts, Facebook) using `reference/templates/social-pack.md`.
3. CTA: exactly one call to action per pack; link goes in the designated
   slot, not buried in prose.
4. Story frames: 3-5 frames with a visual idea and a ≤5-word text overlay
   each.
5. Run the guardrails check at the bottom of the template before delivery.

## Outputs
content-pack.md

## Reference tools
- reference/templates/social-pack.md

## Guardrails
No engagement-bait lies.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `idea` (string, required) - the one idea being promoted
- `platforms` (list, default: IG/TikTok, X/Threads, YouTube Shorts, Facebook)
- `cta` (string, required) - exactly one call to action; link goes in the designated slot

## Example
Input: promote a new single on IG + TikTok + X.
1. 3 hooks: curiosity ("the song I almost deleted"), value ("the 4-chord trick"), identity ("for 2am drivers") - each provably true.
2. Captions: adapt the winning hook per platform from reference/templates/social-pack.md.
3. One CTA: pre-save link in the slot, not buried in prose.
4. 3-5 story frames with visual ideas and <=5-word overlays; guardrails check; content-pack.md.

## Errors & edge cases
- Hook not provably true: rewrite it - engagement-bait lies are a hard guardrail.
- More than one CTA requested: refuse - one CTA per pack.
- Template's guardrails check fails: fix and re-run before delivery.
