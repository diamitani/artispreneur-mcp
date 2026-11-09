---
name: enably
description: "LLM-agnostic sales prospecting and go-to-market skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to architect sales enablement that bridges marketing content and field execution: needs assessment, content audit, content roadmap, 30/60/90 onboarding design, manager coaching framework, tooling recommendations (Seismic/Highspot/Showpad or lightweight alternatives), and ROI measurement - with the content-graveyard, no-rep-involvement, and coaching-over-content pitfalls front and center. Use when building advanced sales enablement strategies."
---

# Enably — Sales Enablement Architect

## Overview
Builds advanced sales enablement strategies that bridge the gap between marketing content and field execution. Focuses on equipping sales teams with the right content, training, tools, and coaching to win more deals.

## When to Use
- Designing a sales enablement function from scratch (team, tools, content strategy)
- Building sales playbooks, battle cards, talk tracks, and competitive intelligence docs
- Creating onboarding and ramp-up programs for new sales hires
- Developing ongoing coaching and certification programs
- Aligning marketing content production with sales team needs (case studies, one-pagers, ROI calculators)
- Implementing sales content management systems (Seismic, Highspot, Showpad) or lightweight alternatives
- Measuring enablement ROI: content usage, time-to-productivity, win-rate improvement

## How It Works
1. Audit current state: What content exists? What do reps actually use? Where are the gaps?
2. Define the enablement pillars: content, training, coaching, tools, analytics.
3. Build content aligned to the buyer's journey and sales stages.
4. Implement training cadence: onboarding, ongoing, just-in-time.
5. Measure impact and iterate.

## Steps
1. **Needs assessment** — Interview reps and managers: "What content do you wish you had in your last deal?"
2. **Content audit** — Inventory existing assets, tag by stage, persona, and format. Identify gaps.
3. **Content roadmap** — Prioritize high-impact assets: battle cards, competitive one-pagers, discovery questions, ROI models.
4. **Training design** — Build onboarding curriculum (30/60/90), ongoing skills workshops, and certification tracks.
5. **Coaching framework** — Define manager coaching cadence, call review process, and deal review templates.
6. **Tooling** — Recommend enablement platforms or a lightweight shared drive structure with clear taxonomy.
7. **Measurement** — Track content usage, time-to-first-deal, win rate by content engagement, rep ramp time.

## Common Pitfalls
- **Content graveyard**: Producing content nobody uses because reps can't find it or don't know it exists. Focus on discoverability and training.
- **No rep involvement**: Building enablement in a vacuum without frontline input creates irrelevant assets.
- **Over-indexing on content vs. coaching**: Content alone doesn't change behavior. Coaching and practice do.
- **Ignoring manager enablement**: Frontline managers need enablement too — how to coach, forecast, and run deal reviews.
- **No feedback loop**: Without tracking what content correlates with won deals, you can't improve.

## Inputs
- `team` (string, required) - sales team size, segments, current state
- `goal` (enum: new-function / playbooks / onboarding / coaching / alignment / tooling / measurement, required)
- `content_inventory` (list) - existing assets for the audit

## Outputs
- Needs assessment findings + enablement pillars (content, training, coaching, tools, analytics)
- Content roadmap: prioritized assets (battle cards, one-pagers, discovery questions, ROI models) mapped to buyer journey stages
- Training curriculum (30/60/90), coaching framework, tooling recommendation, measurement plan

## Example
Input: 15-rep SaaS team, no enablement function, win rate slipping.
1. Needs assessment: interview reps - "what content did you wish you had in your last deal?"
2. Audit: 200 assets exist, 12 used; gaps at late-stage (no ROI model, no security one-pager).
3. Roadmap: battle card + ROI model first; 30/60/90 onboarding; manager call-review cadence.
4. Measure: content usage vs win rate, time-to-first-deal, rep ramp time.
