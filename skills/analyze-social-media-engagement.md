---
name: analyze-social-media-engagement
description: "LLM-agnostic developer tooling skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to turn social metrics into a paid-media decision brief: hook rate, save/share rate, and best local posting windows feeding paid media - logged to HubSpot, never scraping login-gated sources without a connected tool. Use when the user wants to analyze social media engagement."
---

# Analyze social media engagement skill

- **Subagent:** @marketing-agent
- **Category:** Growth
- **NPAO:** A
- **List price:** $19
- **Source:** Paid Media research

## When to use
Hook rate, saves, posting windows feeding paid media decisions.

## Steps
1. Collect metrics
2. save/share rate
3. best local window
4. feed paid media brief
5. log in mcp__hubspot

## Outputs
engagement-brief.md

## Reference tools
- mcp__hubspot

## Guardrails
No login-gated scraping without connected tool.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `accounts` (list, required) - social accounts/handles to analyze
- `window` (string, default: last 30 days) - reporting period
- `metrics` (list, default: hook rate, save/share rate, posting times) - what to measure
- `paid_brief_target` (string) - the paid-media decision this feeds

## Example
Input: analyze @brand TikTok + IG, last 30 days, to decide creative for a paid push.
1. Collect hook rate (3-sec views/impressions), saves, shares per post.
2. Identify top-quartile posts; extract best local posting windows.
3. Write engagement-brief.md: winning hooks, creative patterns, recommended posting windows.
4. Log the brief in mcp__hubspot for the paid media team.

## Errors & edge cases
- Metrics behind a login wall: stop and request the connected tool - no scraping per Guardrails.
- Sparse data (<10 posts in window): widen the window before drawing conclusions.
- No clear winner: report "no signal" honestly instead of inventing a pattern.
