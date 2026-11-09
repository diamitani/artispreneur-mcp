---
name: value-proposition-architect
description: "Crafts value propositions, USPs, and positioning statements that connect product capabilities to audience pain points -- Moore's positioning, the Value Proposition Canvas, and a JTBD lens -- in multi-length variants (one-liner to full positioning doc), every claim backed by proof and stress-tested against objections. Use when crafting value propositions, USPs, and positioning statements."
---

# Value Proposition Architect

## Overview

Crafts compelling value propositions, unique selling propositions (USPs), and positioning statements that connect a product's capabilities to a specific audience's pain points and desired outcomes. Produces messaging frameworks that sales, marketing, and product teams can use directly — from one-line elevator pitches to full positioning docs.

## When to Use

- Launching a new product or feature and need the core messaging.
- Existing messaging is generic ("we save you time and money") and needs differentiation.
- Preparing for a pitch, fundraising deck, or website refresh.
- Building or refreshing a messaging house / brand hierarchy.
- A/B testing different value prop angles for different customer segments.
- Don't use for: purely creative brand copy (use a copywriting skill), or technical product specs.

## How It Works

1. **Input gathering** — Collects product details, target audience (from `buyer-persona-architect` if available), competitive alternatives, and GTM context.
2. **Framework application** — Applies proven value prop frameworks (Moore's positioning statement, Strategyzer's Value Proposition Canvas, Jobs-to-be-Done lens).
3. **Multi-variant output** — Generates value props at multiple lengths: one-liner, paragraph, and full positioning doc with proof points.
4. **Stress testing** — Tests each variant against common objections and competitive alternatives.

## Steps

1. **Gather inputs:** Ask for:
   - Product: What does it do? What's the core capability?
   - Audience: Who is it for? What's their pain point or desired outcome?
   - Alternatives: What do they do today instead? What are competitors saying?
   - GTM context: Is this for a website, sales deck, cold email, or investor pitch?
2. **Apply frameworks:** Produce value props using:
   - **Moore's Positioning:** For [target customer] who [need statement], [product name] is a [product category] that [key benefit]. Unlike [primary alternative], our product [key differentiation].
   - **Value Proposition Canvas:** Map customer jobs/pains/gains to product features/pain relievers/gain creators.
3. **Generate variants:** Produce at least three angles (e.g., emotional, functional, ROI-driven) and recommend which fits the GTM channel.
4. **Provide proof points:** For each claim in the value prop, list the evidence: case study, stat, testimonial, demo, or guarantee.
5. **Objection handling:** Anticipate the top 3-5 buyer objections and draft response messaging for each.

## Common Pitfalls

1. **Feature-dumping:** "We have AI, real-time analytics, and 50 integrations" is not a value proposition. Lead with the outcome, not the feature list.
2. **Same message for everyone:** A value prop that works for the CTO won't work for the end user. Tailor by persona.
3. **No proof:** "Best-in-class security" without SOC2 or a case study is empty marketing. Every claim needs backup.
4. **Ignoring the alternative:** If the customer's alternative is "do nothing" or "use Excel," your value prop must beat that specific alternative, not just competitors.
5. **Jargon and buzzwords:** "Leveraging AI to synergize workflows" alienates readers. Write like a human.

## Verification Checklist

- [ ] Moore's positioning statement is complete and specific
- [ ] At least three value prop variants are generated (by angle/length/channel)
- [ ] Every claim has a proof point
- [ ] Variants are tailored per persona if multiple audiences
- [ ] Competitive alternative is explicitly addressed
- [ ] Top objections have response messaging
- [ ] Output passes the "would a customer say this?" test

## Source

Originally a custom GPT: [Value Proposition Architect](https://chatgpt.com/g/g-68ae3f19816c8191bdc63ae43d37aae5-value-proposition-architect-gpt)

## Inputs

- `product` -- what it does, the core capability
- `audience` -- who it's for, their pain point or desired outcome (buyer personas from buyer-persona-architect if available)
- `alternatives` -- what they do today instead; what competitors are saying
- `gtm_context` -- website, sales deck, cold email, or investor pitch (drives length and angle)

## Outputs

- Moore's positioning statement ("For [target] who [need], [product] is a [category] that [benefit]. Unlike [alternative], [differentiation]"), 3+ variants by angle (emotional, functional, ROI) and length, proof points for every claim (case study, stat, testimonial, demo, guarantee), and top 3-5 objection responses -- passing the verification checklist and the "would a customer say this?" test

## Example

A deploy-automation launch: "For platform teams who lose hours to flaky deploys, DeploySafe is a release-automation platform that ships with zero-downtime guarantees. Unlike Jenkins plugins, it verifies every deploy." -> plus an ROI variant for CFOs, each claim backed by a case-study stat.

## Errors & edge cases

- **Feature-dumping** -- "AI, real-time analytics, 50 integrations" is not a value prop; lead with the outcome.
- **One message for everyone** -- a CTO value prop won't work for the end user; tailor by persona.
- **Proof-less claims** -- "best-in-class security" without SOC 2 or a case study is empty marketing.
- **Ignoring the real alternative** -- if it's "do nothing" or "Excel", beat that alternative, not just competitors.
- **Jargon and buzzwords** -- "leveraging AI to synergize workflows" alienates; write like a human.
