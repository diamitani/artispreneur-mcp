---
name: outreach-automator
description: "Generates personalized outreach sequences at scale — from list preparation through sequence design (touches, channels, timing, triggers) to CRM automation (HubSpot sequences, Salesforce cadences, Outreach.io) — bridging manual high-touch outreach and mass email blasts, with A/B testing and reply/meeting-rate tracking. Use when automating email outreach tasks and CRM workflows."
---

# Outreach Automator

## Overview
Generates personalized outreach sequences at scale, handling the full cycle from list preparation to sequence design to CRM automation. Bridges the gap between manual high-touch outreach and mass email blasts.

## When to Use
- Designing multi-touch outreach sequences (email + LinkedIn + call)
- Generating personalized email copy for a list of prospects at scale
- Setting up CRM-based outreach automation (HubSpot sequences, Salesforce cadences, Outreach.io)
- Creating prospect list segments with personalization tokens
- Writing A/B test variants for subject lines, body copy, and CTAs
- Building re-engagement sequences for cold or stalled leads

## How It Works
1. Define target audience segments and personalization variables.
2. Design the outreach sequence: number of touches, channels, timing, triggers.
3. Generate copy for each touch with personalization hooks.
4. Configure automation rules: enrollment triggers, step delays, exit conditions.
5. Define success metrics and tracking.

## Steps
1. **Audience definition** — Define ICP, segment by persona/industry/stage, identify personalization data points (name, company, recent trigger, pain point).
2. **Sequence design** — Map touchpoints: Day 1 (email), Day 3 (LinkedIn), Day 7 (email + call), Day 14 (breakup email). Include exit conditions (reply, meeting booked, bounce).
3. **Copy generation** — Write each touch with: hook, value prop, social proof, CTA. Vary angle across touches — don't repeat the same message.
4. **Personalization at scale** — Use merge tokens ({{first_name}}, {{company}}, {{pain_point}}) and conditional logic (if industry=X, insert Y angle).
5. **CRM setup** — Configure enrollment triggers, step delays, task creation, and tracking in the CRM or outreach tool of choice.
6. **Testing** — Set up A/B tests on subject lines, opening hooks, and CTAs. Define sample sizes and success criteria.
7. **Monitoring** — Track open rates, reply rates, meeting booked rate, and sequence drop-off points.

## Common Pitfalls
- **Stale lists**: Sending to unverified or outdated lists kills deliverability. Always validate before launching.
- **Spray-and-pray**: Even automated outreach needs personalization. Generic blasts get flagged as spam.
- **No exit conditions**: Prospects stuck in sequences after replying or booking a meeting create a terrible experience.
- **Ignoring cadence fatigue**: Too many touches too fast burns lists. Space touches at least 2-3 days apart.
- **Poor tracking**: Without UTM parameters and CRM tracking, you can't measure what's working.

## Inputs

- `audience` — ICP, segments by persona/industry/stage, and personalization data points per segment (name, company, recent trigger, pain point)
- `sequence_spec` — number of touches, channels (email + LinkedIn + call), timing (at least 2–3 days apart), triggers, exit conditions (reply, meeting booked, bounce)
- `crm` — HubSpot sequences, Salesforce cadences, Outreach.io, or tool of choice (enrollment triggers, step delays, task creation, tracking configured there)
- `tests` — A/B variants for subject lines, opening hooks, CTAs, with sample sizes and success criteria
- Validated prospect lists (stale/unverified lists kill deliverability — validate before launching)

## Outputs

- A multi-touch outreach sequence: touchpoint map with timing, per-touch copy (hook, value prop, social proof, CTA, varied angle per touch), merge tokens and conditional logic for personalization at scale
- CRM automation config: enrollment triggers, step delays, task creation, tracking (UTM parameters + CRM tracking)
- A/B test plan and success metrics: open rates, reply rates, meeting-booked rate, sequence drop-off points
- Format: sequence design + copy + automation configuration — personalized, never spray-and-pray

## Example

50 Series-A CTOs: Day 1 email (hook: their recent funding announcement, value prop, CTA: 15-min call) → Day 3 LinkedIn touch → Day 7 email + call → Day 14 breakup email · exit conditions: reply, meeting booked, bounce · copy per touch with hook, value prop, social proof, CTA — varied angles, never the same message twice · merge tokens `{{first_name}}`, `{{company}}`, `{{pain_point}}` + conditional logic (if industry=fintech, insert the compliance angle) · A/B test subject lines with defined sample sizes · track open rate, reply rate, meeting-booked rate, and sequence drop-off points.
