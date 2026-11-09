---
name: sop-architect
description: "Turns raw process descriptions, interview notes, or existing docs into polished, team-ready SOPs -- the standard template (Purpose, Scope, Prerequisites, Step-by-Step, Expected Outcomes, Exception Handling, Roles), gap analysis for missing steps and edge cases, and formatting for wikis, Notion, training docs, or compliance records. Use when building or improving Standard Operating Procedures."
---

# SOP Architect

## Overview

Transforms raw process descriptions, interview notes, or existing documentation into polished, team-ready Standard Operating Procedures. The skill structures workflows, identifies missing steps and edge cases, and enforces clarity so every team member can follow the procedure with minimal ramp-up. Outputs are formatted for direct use in wikis, Notion, training docs, or compliance records.

## When to Use

- You have a process description (verbal, written, or in meeting notes) and need it turned into a formal SOP.
- An existing SOP is outdated, inconsistent, or missing critical steps — you need a gap analysis and rewrite.
- You are onboarding new team members and want clear, repeatable procedure docs.
- You need SOPs that satisfy compliance, audit, or ISO requirements.
- Don't use for: strategy docs, project plans, or one-off task lists that don't repeat.

## How It Works

1. **Ingest** — Accepts a process in any form: bullet points, transcript, rough notes, or an existing SOP draft.
2. **Structure** — Maps the process into a standard SOP template: Purpose, Scope, Prerequisites, Step-by-Step Procedure, Expected Outcomes, Exception Handling, and Roles.
3. **Gap Analysis** — Flags missing decision points, ambiguous steps, unhandled edge cases, and missing roles.
4. **Format** — Produces clean markdown or rich-text output with numbered steps, conditional branches, and clear role assignments.

## Steps

1. **Gather the process:** Ask the user to describe the workflow or paste existing notes. Prompt for: who does it, what triggers it, what tools are involved, and what the desired outcome is.
2. **Draft the SOP:** Produce a structured draft with all standard sections. Use numbered steps with clear actor (role) for each. Ask clarifying questions for any ambiguous steps.
3. **Gap check:** Review the draft against these questions:
   - Are there preconditions or approvals not mentioned?
   - What happens when a step fails — is there a fallback?
   - Are all roles, tools, and access requirements listed?
   - Are there time-sensitive or compliance-sensitive steps?
4. **Polish for adoption:** Simplify language for a new team member. Add brief "Why this step matters" notes where the rationale isn't obvious.
5. **Deliver:** Present the final SOP in the user's preferred format, with a summary of gaps identified and filled.

## Common Pitfalls

1. **Vague action verbs:** "Handle the request" is useless. Every step must have a concrete verb + object + destination (e.g., "Forward the ticket to `#eng-support` in Slack with the `urgent` tag").
2. **Missing role assignments:** Every step needs an explicit actor. "The request is approved" → ask: by whom? In what system?
3. **No exception paths:** Happy-path-only SOPs break in production. Always include "If X fails, then Y" branches.
4. **Over-engineering:** Not every process needs a 20-page SOP. Match the depth to the risk and frequency of the task.
5. **No verification criteria:** The SOP must define what "done" looks like — a checklist item, a status change, or a notification sent.

## Verification Checklist

- [ ] Every step has a concrete action verb and clear actor
- [ ] Purpose and Scope sections are present and correct
- [ ] Prerequisites (tools, access, approvals) are listed
- [ ] Exception/error paths are documented
- [ ] Expected outcome is measurable
- [ ] Output is formatted for the target platform (Notion, wiki, Confluence, etc.)
- [ ] User confirmed no missing steps

## Source

Originally a custom GPT: [SOP Architect](https://chatgpt.com/g/g-68ae5f21a1608191bd68ed88850d7ab1-sop-architect-gpt)

## Inputs

- `process_source` -- the process in any form: bullet points, transcript, rough notes, or an existing SOP draft (describe who does it, what triggers it, tools involved, desired outcome)
- `target_format` -- wiki, Notion, Confluence, training doc, or compliance record

## Outputs

- A structured SOP draft: Purpose, Scope, Prerequisites, numbered step-by-step procedure with an explicit actor per step, Expected Outcomes, Exception Handling, Roles -- simplified for a new team member, with "why this step matters" notes where rationale isn't obvious
- A gap-analysis summary: gaps identified and filled, plus the verification checklist (concrete verbs + actors, prerequisites listed, exception paths documented, measurable outcome, formatted for the target platform)

## Example

A verbal refund process becomes an SOP: Purpose/Scope/Prerequisites up top; numbered steps with actors ("Forward the ticket to #eng-support in Slack with the urgent tag"); "If the refund API fails, escalate to the on-call engineer" exception branch; outcome "customer refunded within 24h, ticket closed".

## Errors & edge cases

- **Vague action verbs** -- "handle the request" is useless; every step needs concrete verb + object + destination.
- **Missing role assignments** -- every step needs an explicit actor ("the request is approved" -> by whom? in what system?).
- **Happy-path-only SOPs** -- break in production; always include "If X fails, then Y" branches.
- **Over-engineering** -- not every process needs 20 pages; match depth to risk and frequency.
- **No verification criteria** -- define what "done" looks like: a checklist item, a status change, a notification sent.
- **Wrong job** -- strategy docs, project plans, and one-off task lists are out of scope.
