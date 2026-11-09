---
name: archetypes-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to pick video archetypes from the quick-reference catalog of eight pre-wired Remotion compositions - social_ad (15s), sales_explainer (60s), country_spotlight (30s), product_demo (90s), event_promo (20s), testimonial (45s), thought_leadership (30s), internal_announce (45s) - each with structure, aspect ratio, placement, default voice persona, and script word budget. Use when picking a video archetype for a Remotion composition (social_ad, sales_explainer, country_spotlight, product_demo, event_promo, testimonial, thought_leadership, internal_announce)."
---

# Archetype deep dive

Each archetype is a pre-wired Remotion composition. This doc is the quick
reference the skill uses to pick defaults and the user can read to understand
what they're getting.

---

## social_ad — 15s · 1:1 (or 9:16) · LinkedIn feed
- **Structure:** headline (10s) → end card (5s)
- **Best for:** paid LinkedIn, organic feed posts, quick ICP hits
- **Voice persona default:** {{COMPANY_NAME}}-upbeat-rep
- **Script budget:** ≤ 38 words

## sales_explainer — 60s · 16:9 · website hero, first-touch outbound
- **Structure:** hook (13s) → problem (13s) → solution (13s) → stats (13s) → end (8s)
- **Best for:** "What does {{COMPANY_NAME}} do?" content
- **Voice persona default:** {{COMPANY_NAME}}-warm-brand
- **Script budget:** ≤ 150 words

## country_spotlight — 30s · 16:9 or 1:1 · ABM, country launches
- **Structure:** headline + country label (10s) → big stat (10s) → end (10s)
- **Best for:** highlighting new country launches or ABM campaigns
- **Voice persona default:** {{COMPANY_NAME}}-upbeat-rep
- **Script budget:** ≤ 75 words

## product_demo — 90s · 16:9 · mid-funnel enablement
- **Structure:** title (10s) → 3 feature beats (20s each) → end (10s)
- **Best for:** asynchronous walkthroughs, enablement
- **Voice persona default:** {{COMPANY_NAME}}-neutral-narrator
- **Script budget:** ≤ 225 words

## event_promo — 20s · 1:1 · webinar / conference teasers
- **Structure:** hook (7s) → event details (7s) → CTA (6s)
- **Best for:** "meet us at booth X" style promos
- **Voice persona default:** {{COMPANY_NAME}}-upbeat-rep
- **Script budget:** ≤ 50 words

## testimonial — 45s · 16:9 · customer stories
- **Structure:** pull quote + lower-third (27s) → outcome headline (10s) → end (8s)
- **Best for:** case-study pull quotes, customer social proof
- **Voice persona default:** {{COMPANY_NAME}}-warm-brand
- **Script budget:** ≤ 110 words

## thought_leadership — 30s · 1:1 · exec quotes, CEO insights
- **Structure:** quote + lower-third (20s) → end card (10s)
- **Best for:** Jim McCoy / exec content, industry commentary
- **Voice persona default:** {{COMPANY_NAME}}-confident-exec
- **Script budget:** ≤ 75 words

## internal_announce — 45s · 16:9 · team updates, all-hands
- **Structure:** title (10s) → headline (13s) → stat (13s) → next step (9s)
- **Best for:** internal wins, team communication
- **Voice persona default:** {{COMPANY_NAME}}-warm-brand
- **Script budget:** ≤ 110 words
- **Note:** Uses primary logo; internal audience, no external disclaimers.

## Inputs
- `goal` (enum: paid-social / hero / ABM / enablement / event / proof / exec-comms / internal, required)
- `placement` (string) - LinkedIn feed, website hero, outbound, all-hands...
- `duration_target` (string) - picks the closest archetype length
- `voice_persona` (string, default: archetype default) - override e.g. for exec tone

## Outputs
- Chosen archetype with its beat structure, aspect ratio, and word budget
- Default voice persona and placement guidance
- Script slot map (e.g. hook 13s -> problem 13s -> solution 13s -> stats 13s -> end 8s)

## Example
Input: first-touch outbound video explaining what the company does, website hero.
1. Goal "what does it do" + hero placement -> sales_explainer.
2. 60s, 16:9; voice default {{COMPANY_NAME}}-warm-brand.
3. Script slots: hook (13s) -> problem (13s) -> solution (13s) -> stats (13s) -> end (8s); budget <= 150 words.

## Errors & edge cases
- Word count over budget: trim to the archetype's script budget before composing - overruns break the beat timing.
- Wrong aspect for placement (e.g. 16:9 for a LinkedIn feed): social_ad and event_promo support 1:1 or 9:16 - pick one of those.
- No matching archetype: use the closest structure and adjust beats; do not invent a new archetype code.
