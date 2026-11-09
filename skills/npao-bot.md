---
name: npao-bot
description: "Turns a messy task list into an executable action plan through the four-phase NPAO cycle — Navigate (full inventory, no filtering), Prioritize (impact × urgency scoring), Allocate (ownership + timeboxing), Orchestrate (review cadence) — outputting a clean NPAO card with the ranked list, assignments, and check-in plan. Use when helping users prioritize and analyze tasks using the NPAO framework (Navigate, Prioritize, Allocate, Orchestrate)."
---

# NPAO Bot — Task Prioritization & Orchestration

## Overview
NPAO Bot applies the NPAO framework — Navigate, Prioritize, Allocate, Orchestrate — to help users cut through task overwhelm, identify what matters most, and build an executable action plan. It turns a messy task list into a clear, growth-oriented roadmap.

## When to Use
- The user feels overwhelmed by too many tasks with no clear order.
- Prioritizing a backlog or sprint planning.
- Deciding what to delegate vs. own.
- Strategic weekly/monthly planning with a bias toward growth and impact.

## How It Works
The four-phase NPAO cycle:

| Phase | Question | Output |
|-------|----------|--------|
| **Navigate** | Where are we now? What's on the plate? | Full task inventory, current state |
| **Prioritize** | What moves the needle most? | Ranked list by impact/urgency matrix |
| **Allocate** | Who does what, by when? | Assignment + timeboxing |
| **Orchestrate** | How do we keep momentum? | Check-in cadence, blockers, adjustments |

## Steps
1. **Navigate** — Dump all tasks. No filtering yet. Capture everything: work, personal, pending decisions.
2. **Prioritize** — Score each task on Impact (1-5) and Urgency (1-5). Sort by product. Label top-3 "must-dos."
3. **Allocate** — Assign ownership (self vs. delegate) and rough time boxes. Flag dependencies.
4. **Orchestrate** — Set a review rhythm (daily standup, weekly retro). Define "done" for each task.
5. **Output NPAO card** — A clean markdown summary with the prioritized list, assignments, and check-in plan.

## Common Pitfalls
- **Skipping Navigate.** Jumping straight to prioritizing without a full inventory misses hidden tasks.
- **Fake urgency.** Not everything is urgent. Challenge "urgent" labels that lack consequences.
- **No follow-through.** Orchestrate is the most skipped phase. Without a review cadence, the plan dies.

## Inputs

- `task_list` (required) — dump everything first: work, personal, pending decisions; no filtering in the Navigate phase
- Impact (1–5) × Urgency (1–5) per task — sorted by product; challenge ‘urgent’ labels that lack consequences (fake urgency)
- `ownership` — self vs delegate per task, with rough timeboxes and flagged dependencies
- `review_rhythm` — daily standup, weekly retro; ‘done’ defined per task

## Outputs

- A clean **NPAO card** (markdown): the prioritized list ranked by impact × urgency (top-3 ‘must-dos’ labeled), ownership + timeboxing per task, dependencies flagged, and the check-in cadence with per-task done-definitions
- For: task overwhelm, backlog/sprint prioritization, delegate-vs-own decisions, strategic weekly/monthly planning with a growth/impact bias
- Format: markdown summary — the plan only lives if the Orchestrate phase sets the review rhythm

## Example

Overwhelmed Monday: Navigate — dump all 14 tasks (work, personal, pending decisions), no filtering → Prioritize — score each: ‘fix checkout bug’ 5×5=25, ‘plan Q1’ 4×2=8 → top-3 must-dos labeled → Allocate — ‘expense reports’ delegated to ops, ‘inbox zero’ timeboxed 30 min, dependencies flagged → Orchestrate — daily standup check-in; ‘done’ for the bug = fixed + test passing → NPAO card: ranked list, assignments, check-in plan.
