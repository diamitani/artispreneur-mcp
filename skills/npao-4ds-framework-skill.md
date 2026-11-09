---
name: npao-4ds-framework-skill
description: "The NPAO priority framework + 4Ds lifecycle reference — classifies every task by felt urgency (N: Necessity ‘I MUST’ → A: Anxiety ‘I WON'T HAVE PEACE’ → P: Priority ‘I NEED’ → O: Opportunity ‘I CAN’), executed N→A→P→O with anxiety deliberately before priority, mapped onto the 4Ds phases (PreD/D1/D2/D3/D4) with hard phase gates. Use when classifying tasks or assigning phases with the NPAO priority framework."
---

# NPAO Priority Framework + 4Ds Lifecycle

**Canonical source:** NPAO https://rostr-paper.vercel.app/#s6 · 4Ds https://rostr-paper.vercel.app/#s6-7
*Read this file before classifying tasks or assigning phases. Fetch the live section only if a definition is still unclear.*

---

## NPAO — the four classes

NPAO classifies every task by the *felt urgency* behind it, not by topic. The class determines execution order **and** scheduling order.

```
N — NECESSITY: "I MUST"
  Hard blocker. Nothing downstream works without it.
  Examples: API auth, schema definition, database creation, tool registration,
            access provisioning.
  → Execute FIRST. Cannot be skipped. Cannot be pushed past today without a BLOCKED flag.

A — ANXIETY: "I WON'T HAVE PEACE"
  Persistent friction. An unresolved loop. Degrades the quality of P-class work.
  Examples: ambiguous scope, broken prior automation, undefined edge cases,
            stale data, missing owner.
  → Execute SECOND — before Priority. Open >3 days → auto-escalate to N-class.

P — PRIORITY: "I NEED"
  Mission-critical. Directly advances the objective.
  Examples: build the agent, write the workflow, create the output, run the test.
  → Execute THIRD — with full focus, all N and A cleared. Needs a Deep Work block.

O — OPPORTUNITY: "I CAN"
  Optional growth. Non-blocking. Compounding value.
  Examples: logging, dashboards, fallback enrichment, notifications.
  → Execute LAST — only when N, A, P are complete. If no slot, it waits. That is correct.

EXECUTION ORDER: N → A → P → O
CRITICAL RULE: Anxiety before Priority — unresolved loops degrade execution quality
               on core mission work.
```

### Why Anxiety runs before Priority

The single most important and most counter-intuitive NPAO rule. An open anxiety (an unresolved dependency, an ambiguous scope decision) silently taxes every priority task that follows it — the builder second-guesses, re-checks, and reworks. Clearing anxiety first is not procrastination; it is what makes priority execution clean.

---

## NPAO Canvas format

When producing a task plan, lay it out as a canvas with every task atomic (one owner, one done-state):

```
NPAO TASK CANVAS — [Project Name]
Mission: [one-line]
4Ds Phase: [current] | Dominant NPAO class: [per phase]

N — NECESSITY (resolve first) — nothing downstream proceeds without these
  N1. [Task] | Owner: [role] | Est: [duration] | Done when: [criterion]
      Build prompt: [instruction] | Subtasks: N1a / N1b | Blocks: [downstream IDs]

A — ANXIETY (clear before Priority) — friction that degrades P-class
  A1. [Task] | Owner | Est | Done when | Why anxiety (not priority): [rationale]
      Resolves: [what friction this eliminates]

P — PRIORITY (core mission work)
  P1. [Task] | Owner | Est | 4Ds: [phase] | Done when | Subtasks | Feeds: [downstream ID]

O — OPPORTUNITY (when bandwidth allows)
  O1. [Task] | Owner | Est | Done when | Value if completed: [what this adds]

Execution Queue: N1 → N2 → A1 → A2 → P1 → P2 → O1
```

---

## Scheduling rules (used by the Scheduler)

- **N:** earliest available slot; cannot be pushed past today without a BLOCKED flag.
- **A:** before any P-class task; prefer Focus or Quick Hit blocks; open >3 days → escalate to N.
- **P:** requires a Deep Work block (90+ min uninterrupted); never fragmented time; pushed >2 consecutive days → milestone-risk flag.
- **O:** fills remaining capacity only; never displaces N/A/P; waiting is correct.

---

## 4Ds Lifecycle

Every project and task is tagged to a phase. The phase determines which NPAO class is dominant.

| Phase | Name | Dominant NPAO | What's happening | Gate rule |
|---|---|---|---|---|
| **PreD** | Drafting | N | Research, validate, prove the idea before building | — |
| **D1** | Design | P | Architecture, specs, schemas, agent behavior — lock decisions | Nothing moves to D2 until **all** D1 decisions are locked |
| **D2** | Develop | P + A | Build, implement, test; clear blockers in parallel | — |
| **D3** | Deploy | N | Release, credentials, config, health checks | **Hard gate** — explicit user approval required |
| **D4** | Debug | A + O | Monitor, fix, optimize | Fix first, then optimize |

**Phase gate rule (most-violated):** Never advance to D2 (Develop) until all D1 (Design) decisions are locked. Most wasted builds skip straight from PreD to D2. The NPAO canvas flags this explicitly.

---

## Classification heuristics

When unsure which class a task is, ask in order:
1. Does anything else literally fail to start without this? → **N**
2. Is this an unresolved question/loop that will make me re-do P-work if left open? → **A**
3. Does this directly produce the thing the project exists to make? → **P**
4. Is this nice-to-have, additive, non-blocking? → **O**

A task can only hold one class. If it feels like two, split it.

## Inputs

- `task_list` (required) — every task classified by felt urgency using the heuristics, in order: (1) does anything else literally fail to start without this? → N · (2) is this an unresolved question/loop causing P-work rework? → A · (3) does this directly produce the thing the project exists to make? → P · (4) nice-to-have, additive, non-blocking? → O
- `phase` per task/project — PreD (Drafting, N-dominant) · D1 (Design, P-dominant — lock decisions) · D2 (Develop, P+A) · D3 (Deploy, N-dominant — hard gate: explicit user approval) · D4 (Debug, A+O — fix first, then optimize)
- Canonical source: NPAO https://rostr-paper.vercel.app/#s6 · 4Ds https://rostr-paper.vercel.app/#s6-7 (fetch live only if a definition is unclear)

## Outputs

- An **NPAO task canvas**: Mission one-liner, 4Ds phase, dominant NPAO class; N/A/P/O sections with atomic tasks (one owner, one done-state, estimate, done-when criterion, build prompt, subtasks, blocks/feeds links); the execution queue (N1 → N2 → A1 → A2 → P1 → P2 → O1)
- Scheduling rules: **N** earliest slot, never past today w/o BLOCKED · **A** before any P (Focus/Quick-Hit blocks), >3 days open → N · **P** Deep Work 90+ min, never fragmented, >2 days pushed → milestone-risk · **O** fills remaining capacity only, never displaces N/A/P
- Format: canvas markdown — read this file before classifying tasks or assigning phases

## Example

Launch checklist: ‘Stripe keys’ → **N** (nothing downstream works without it — execute first, today or BLOCKED). ‘Ambiguous refund policy’ → **A** (unresolved loop that will degrade checkout work — clear before any P). ‘Build checkout’ → **P** (deep-work block, full focus). ‘Add analytics dashboard’ → **O** (waits for bandwidth — that is correct). Phase: D1 Design until refund-policy and pricing decisions are locked — never D2 with open D1 decisions. Execution queue: N1 → A1 → P1 → O1.

## Errors & edge cases

- **Most-violated rule: advancing to D2 (Develop) before all D1 (Design) decisions are locked.** Most wasted builds skip straight from PreD to D2 — the canvas flags this explicitly; nothing moves to D2 until D1 decisions are locked.
- **Anxiety misclassified as Priority** — an open anxiety silently taxes every P-task after it (second-guessing, re-checking, rework). Clearing anxiety first is not procrastination; it's what makes priority execution clean.
- **A task that feels like two classes** → split it. A task can only hold one class.
- **N pushed past today without a BLOCKED flag** — not allowed; N is earliest-available-slot, hard blocker.
- **P in fragmented time** — P requires a 90+ minute uninterrupted Deep Work block; pushed >2 consecutive days → milestone-risk flag. A open >3 days → auto-escalate to N.
