---
name: sales-process-assistant
description: "Automates and optimizes sales workflows end to end -- process mapping, bottleneck analysis, trigger/condition/action automation design, CRM configuration (HubSpot, Salesforce, Pipedrive), data hygiene, pipeline insights (forecasting, win/loss), and reporting dashboards. Use when automating sales workflows or integrating CRMs."
---

# Sales Process Assistant

## Overview
Automates and optimizes sales workflows with a focus on CRM integration, pipeline management, and actionable insights. Consolidates the capabilities of Sales Process Assistant and Prossley into one practical workflow engine.

## When to Use
- Designing automated sales workflows (lead routing, follow-up sequences, task creation)
- Integrating or migrating CRM data between platforms (HubSpot, Salesforce, Pipedrive, etc.)
- Generating sales insights from pipeline data: forecasting, bottleneck analysis, win/loss patterns
- Building prospecting workflows with enrichment, scoring, and sequencing
- Automating reporting: weekly pipeline reviews, activity summaries, deal health dashboards
- Cleaning and deduplicating CRM data for better accuracy

## How It Works
1. Map the current sales process end-to-end (lead → opportunity → close).
2. Identify manual bottlenecks and automation opportunities.
3. Design automated workflows: triggers, conditions, actions.
4. Configure CRM fields, pipelines, automations, and integrations.
5. Generate reports and insights from pipeline data.

## Steps
1. **Process mapping** — Document each stage, handoff, and tool in the current sales process.
2. **Bottleneck identification** — Find steps that are manual, error-prone, or slow.
3. **Automation design** — Specify triggers (e.g., form submission, deal stage change) → conditions → actions (task creation, email sequence, Slack notification).
4. **CRM configuration** — Guide setup of custom fields, pipelines, automation rules, and integrations.
5. **Data hygiene** — Deduplicate records, standardize fields, validate enrichment.
6. **Insights generation** — Pull pipeline metrics: conversion rates by stage, time-in-stage, win/loss by rep or segment.
7. **Reporting setup** — Build dashboards or scheduled reports for team and leadership visibility.

## Common Pitfalls
- **Automating a broken process**: Automate only after optimizing the underlying process. "Automating chaos" multiplies problems.
- **Over-automation**: Too many automated touches can feel spammy. Leave room for human judgment.
- **CRM spaghetti**: Poor field hygiene and inconsistent data entry make automations unreliable.
- **Ignoring user adoption**: If reps don't use the CRM correctly, no workflow automation saves you. Invest in training.
- **No error handling**: Automations need fallback paths — what happens when enrichment fails or a field is missing?

## Inputs

- `current_process` -- the sales process mapped end to end (lead -> opportunity -> close), with each stage, handoff, and tool documented
- `crm_platform` -- HubSpot, Salesforce, Pipedrive, or other (for integration/migration work)
- `pipeline_data` -- for insights: conversion rates by stage, time-in-stage, win/loss by rep or segment

## Outputs

- Automated workflows specified as triggers -> conditions -> actions (e.g. form submission -> enrichment -> round-robin lead routing -> follow-up sequence -> Slack notification)
- CRM configuration guide (custom fields, pipelines, automation rules, integrations)
- Cleaned, deduplicated CRM data with standardized fields
- Insight reports (forecasting, bottleneck analysis, win/loss patterns) and dashboards or scheduled reports for team and leadership

## Example

Inbound lead flow: website form submission triggers enrichment; qualified leads route round-robin to SDRs with an automatic 5-touch follow-up sequence; deal stage changes fire Slack notifications; a weekly pipeline review dashboard shows conversion-by-stage and flags deals stalled 14+ days.

## Errors & edge cases

- **Automating a broken process** -- optimize the underlying process first; "automating chaos" multiplies problems.
- **Over-automation** -- too many automated touches feel spammy; leave room for human judgment.
- **CRM spaghetti** -- poor field hygiene and inconsistent data entry make automations unreliable; fix data hygiene first.
- **Ignoring user adoption** -- if reps don't use the CRM correctly, no workflow automation saves you; invest in training.
- **No error handling** -- automations need fallback paths: what happens when enrichment fails or a field is missing?
