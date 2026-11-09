---
name: artist-business-plan
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to turn an artist's creative vision into a structured business plan: mission and brand identity, market analysis, diversified revenue streams (streaming, live, merch, sync, Patreon), quarterly SMART milestones with KPIs, and an aligned budget - grounded, never promising 1M streams in month one. Use when guiding artists through building tailored business plans and growth strategies."
---

# Artist Business Plan

## Overview
Transforms an artist's creative vision into a concrete, actionable business plan. Covers mission, brand identity, revenue streams, audience growth strategy, and measurable milestones — treating the artist's career as a sustainable business.

## When to Use
- An artist is serious about turning music into a career
- Building a 1-year or 3-year growth roadmap
- Preparing for investor pitches, grant applications, or label meetings
- Identifying and diversifying revenue streams

## How It Works
1. **Vision & mission**: Define the artist's unique value proposition and long-term goals.
2. **Market analysis**: Identify target audience, competitors, and genre landscape.
3. **Revenue model**: Map out income streams — streaming, live shows, merch, sync, teaching, Patreon, etc.
4. **Growth milestones**: Set quarterly SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound).
5. **Budget & resources**: Outline costs and needed investments.
6. **Deliverable**: A structured business plan document.

## Steps
1. Ask: "What does success look like for you in 1 year? In 3 years?"
2. Define the artist's brand: genre, values, visual identity, story.
3. Analyze the market: Who are comparable artists? What's working for them?
4. Map revenue streams with realistic projections.
5. Set quarterly milestones with KPIs (streams, followers, show attendance, revenue).
6. Create a budget that aligns with goals.
7. Compile into a formatted business plan document.

## Common Pitfalls
- **Unrealistic projections**: Don't promise 1M streams in month one. Be grounded.
- **Ignoring costs**: Factor in recording, mixing, mastering, artwork, promotion, touring.
- **No differentiation**: If the plan sounds like every other artist, it's not useful.

## Source
Originally from the Artispreneur Custom GPT portfolio.

## Inputs
- `vision` (string, required) - what success looks like in 1 year and 3 years
- `brand` (string) - genre, values, visual identity, story
- `comparables` (list) - similar artists and what's working for them
- `budget` (number) - available investment

## Outputs
- Structured business plan document: mission, brand identity, market analysis
- Revenue model with realistic projections across streaming, live, merch, sync, teaching, Patreon
- Quarterly SMART milestones with KPIs (streams, followers, show attendance, revenue)
- Aligned budget covering recording, mixing, mastering, artwork, promotion, touring

## Example
Input: bedroom-pop artist, goal is full-time music in 3 years.
1. Vision: 1yr - 50k monthly listeners + first 200-cap shows; 3yr - touring income covers rent.
2. Revenue map: streaming + live + merch + sync, projections grounded in current 8k monthly listeners.
3. Milestones: Q1 EP release + 15k listeners; Q2 first headline show; KPIs per quarter.
4. Budget aligned: recording and promo prioritized; compiled into the plan document.
