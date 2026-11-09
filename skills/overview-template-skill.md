---
name: overview-template-skill
description: "The template for the markdown walkthrough that ships with every diagram — At-a-glance table, a sub-120-word plain-English ‘How it works’ story, numbered step-by-step entries matching the diagram's badges (with in→out and failure paths), Components, Data & integration notes, Failure paths & safeguards, and Assumptions & open questions — written for a non-technical reader first, technical depth in the tables. Use when writing the overview document for a diagram."
---

# Overview Document Template

Every diagram ships with this markdown walkthrough. Step numbers MUST match the numbered badges in the diagram. Write for a non-technical reader first; put technical depth in the tables.

---

# {System / Workflow Name}

{One sentence: what this system does and for whom.}

## At a glance

| | |
|---|---|
| **Purpose** | {the job this system does} |
| **Trigger** | {what starts it} |
| **Actors** | {people + systems involved} |
| **Systems** | {tools/platforms touched} |
| **End state** | {what exists when it finishes} |
| **Owner** | {who runs/maintains it} |

## How it works

{One short paragraph telling the story of the diagram left-to-right or top-to-bottom. No jargon. This is the paragraph someone reads while looking at the image.}

## Step by step

### ① {Step name}
**What happens:** {plain-English description}
**System:** {which component from the diagram}
**In → Out:** {input} → {output}
**If it fails:** {retry / alert / human review path}

### ② {Step name}
{...repeat for each numbered badge in the diagram...}

## Components

| Component | Role | Type | Notes |
|---|---|---|---|
| {name as shown in diagram} | {what it does} | service / data store / external / human | {auth, limits, owner} |

## Data & integration notes

- {what data moves where, formats, sync vs async}
- {auth/keys required and where they live}
- {rate limits, batch sizes, schedules}

## Failure paths & safeguards

- {each dashed/red path in the diagram, what triggers it, who gets notified}
- {approvals or irreversible actions, called out plainly}

## Assumptions & open questions

- {every assumption made where the brief was thin}
- {decisions the owner still needs to make}

---

Rules:
- Keep "How it works" under 120 words.
- Every diagram node appears exactly once in the Components table.
- If there are no failure paths, say so explicitly — that's a finding, not an omission.
- Skip sections that genuinely don't apply (org charts have no failure paths); never skip Step by step or Components.

## Inputs

- The diagram (required) — its numbered badges drive the Step by step numbering 1:1
- `name` + one-sentence purpose (what the system does, for whom)
- At-a-glance facts: purpose, trigger, actors (people + systems), systems touched, end state, owner
- Data flows (what data moves where, formats, sync vs async), auth/keys and where they live, rate limits/batch sizes/schedules
- Failure paths (each dashed/red path: trigger, who gets notified), approvals or irreversible actions
- Assumptions where the brief was thin; decisions the owner still needs to make

## Outputs

- The overview document in template order: title · At a glance table · How it works (≤120 words, plain English, written while looking at the diagram) · Step by step (per badge: what happens, system, In → Out, if-it-fails path) · Components table (name as shown, role, type, notes) · Data & integration notes · Failure paths & safeguards · Assumptions & open questions
- Format: markdown walkthrough — non-technical reader first, technical depth in the tables

## Example

System: ‘Nightly inventory sync’ → At-a-glance: purpose, trigger (midnight cron), actors, systems, end state, owner → How it works: 98-word left-to-right story, no jargon → ① Extract (what happens, system, CSV → warehouse, if it fails: retry 3× then Slack alert) → ② Transform → ③ Load → Components table: cron, S3, warehouse, Slack alerter — each diagram node exactly once → Failure paths: warehouse timeout → Slack alert → Assumptions: sync window < 4h; open question: owner to confirm retention.

## Errors & edge cases

- **Step numbers don't match the diagram's numbered badges** → mismatch: renumber so every badge maps 1:1.
- **A diagram node missing from the Components table** → incomplete: every diagram node appears exactly once in the table.
- **No failure paths, unstated** → say so explicitly — that's a finding, not an omission.
- **Skipping Step by step or Components** → not allowed, ever. Skip other sections only when they genuinely don't apply (org charts have no failure paths).
