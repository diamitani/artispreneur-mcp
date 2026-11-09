---
name: affli
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to design end-to-end affiliate marketing strategy: niche and program selection across Amazon Associates, ShareASale, CJ and Impact, content and traffic plans, conversion-rate optimization, and affiliate-ID/UTM tracking dashboards. Use when building and optimizing affiliate marketing strategies."
---

# Affli

## Overview
Builds and optimizes affiliate marketing strategies. Guides users through product selection, content strategy, traffic generation, and commission optimization across major affiliate networks and platforms.

## When to Use
- Choosing a niche and affiliate programs to promote
- Building a content strategy (blog, YouTube, social, email)
- Comparing affiliate networks (Amazon Associates, ShareASale, CJ, Impact, etc.)
- Optimizing existing affiliate content for higher conversions
- Analyzing commission structures and selecting high-EPC programs
- Scaling traffic through SEO, paid ads, or social media

## How It Works
Evaluates the affiliate landscape for a given niche, recommends programs and products, and designs content + traffic strategies. Applies conversion rate optimization principles to affiliate funnels.

## Steps
1. Understand the user's niche, audience, and existing assets
2. Research affiliate programs: commission rates, cookie duration, EPC, reputation
3. Recommend top 5–10 products/programs with rationale
4. Design content plan: review posts, comparison articles, tutorials, roundups
5. Map traffic sources: SEO keywords, Pinterest, YouTube topics, email sequences
6. Optimize conversions: CTAs, link placement, bonus offers, disclosure compliance
7. Set tracking: affiliate IDs, UTMs, dashboard for monitoring performance

## Common Pitfalls
- Promoting too many products instead of focusing on a few high-converting ones
- Ignoring FTC disclosure requirements for affiliate links
- Building content purely for commissions without genuine value
- Chasing high commission rates over product-audience fit
- Not tracking which links/content actually drive conversions

## Inputs
- `niche` (string, required) - the market/topic the affiliate strategy targets
- `audience` (string) - who buys: demographics, platforms, intent level
- `assets` (list) - existing blog, YouTube channel, email list, social following
- `constraints` (string) - networks already joined, geographic limits, preferred content formats

## Outputs
- Recommended program shortlist (5-10 programs) with commission rates, cookie duration, EPC, and rationale
- Content plan: review posts, comparison articles, tutorials, roundups mapped to funnel stages
- Traffic map: SEO keywords, Pinterest/YouTube topics, email sequences
- Conversion checklist: CTAs, link placement, bonus offers, FTC disclosure, UTM tracking setup

## Example
Input: niche "home espresso", audience of beginner home-baristas on YouTube (12k subs), no affiliate accounts yet.
1. Compare programs: Amazon Associates (4.5%, 24h cookie) vs a specialty roaster program (15%, 30-day cookie, higher EPC).
2. Recommend the specialty program for machines, Amazon for accessories - 6 programs total with rationale.
3. Content plan: "Best espresso machines under $500" comparison, grinder tutorial, monthly deal roundup.
4. Tracking: unique UTMs per video, affiliate IDs in a dashboard, FTC disclosure in descriptions.

## Errors & edge cases
- User has no audience or traffic yet: prioritize 2-3 low-competition SEO plays before scaling recommendations.
- High commission but poor audience fit: recommend fit over rate - chasing commissions over fit is a listed pitfall.
- No tracking in place: set up UTMs and affiliate IDs first; never recommend scaling without attribution.
- Missing FTC disclosure: add it before any affiliate link goes live.
