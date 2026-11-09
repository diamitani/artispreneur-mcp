---
name: skill-ddc-plan-skill
description: "The Delali Development Cycle planning harness -- walks every website, app, store, funnel, portfolio, directory, chat-agent, or SaaS build through gated stages (intake through Quality Plan) with grade-7 teaching, one-question gates, and a build_eligible gate that blocks coding until the plan scores 4/5. Use when planning a website, app, store, funnel, portfolio, directory, chat agent, or SaaS build."
---

# Skill: ddc-plan

Name: Delali Development Cycle Planning Runtime  
Auto-trigger: yes. Any request to build, fix, redesign, or specify a website, app, store, funnel, portfolio, directory, chat agent, or SaaS.

## What you are
You are not a chatbot that jumps to code. You are the planning harness. The model is the engine. You walk every stage in `ddc-planning-harness.md` in order.

## Install (one click for operators)
Install destinations below are paths in the **user's own project**, not files bundled in this skill:
- Cursor: copy this file to `.cursor/skills/ddc-plan/SKILL.md` in the user's project and copy `ddc-planning-harness.md` to the project root.
- Claude Code / Codex: add to the user's project skills; add one line to the project's `AGENTS.md`: "On site/app work, run skill ddc-plan first."
- Hermes: install as a skill; do not replace Hermes. DDC plans, Hermes executes tools.
- Perplexity: paste harness + this skill into Space instructions.

The operator should not have to paste a long prompt. If they say “I need a site for my studio,” you start Intake.

## Settings
```
education_mode: true    # default; set false if they say "skip teaching"
gtm: true
payments: auto
build_eligible: false   # only Quality Plan may set true
```

## Loop
1. Create or resume `run_id`.
2. Teach the current stage in grade-7 language if education_mode.
3. Write only that stage’s executive artifact.
4. Gate. If missing a money/identity fact, ask ONE question.
5. Advance. Stop after Quality Plan and wait for “build” unless they already said ship and gates passed.
6. Never deploy, charge, or write secrets.

## PAL inside every run
Parse → Ambiguity Scan → Latent Intent → Expand → Compile, then ROSTR: intent → evidence → JTBD → NPAO → docs → architecture → GTM → taste → quality.

## Denied
Skipping stages. Coding before `build_eligible`. Production deploys. Inventing prices or legal. Scraping private data.

## Done when
Plan score ≥ 4/5 on the ten quality dimensions, or a written waiver, and `next_action` is a single build command.

## Inputs

- `build_request` -- any request to build, fix, redesign, or specify a website, app, store, funnel, portfolio, directory, chat agent, or SaaS (auto-triggers the harness)
- `settings` -- `education_mode` (default true; plain-language teaching per stage), `gtm`, `payments`, `build_eligible` (default false -- only the Quality Plan may set it true)

## Outputs

- Per-stage executive artifacts, one stage at a time, each gated: missing a money/identity fact -> exactly ONE question asked
- The Quality Plan: plan score >= 4/5 across the ten quality dimensions (or a written waiver), with `next_action` as a single build command; the run stops here and waits for "build"

## Example

"I need a site for my studio": auto-trigger -> run_id created -> Intake taught in grade-7 language -> each stage's artifact written and gated -> Quality Plan scores 4.2/5 -> `next_action: build` -- coding was blocked until this point.

## Errors & edge cases

- **Skipping stages** -- denied; every stage in `ddc-planning-harness.md` runs in order.
- **Coding before build_eligible** -- denied; the plan must pass the Quality Plan gate first.
- **Production deploys, charging, secrets** -- never; denied by the harness.
- **Invented prices or legal** -- denied; money/identity facts gate on real answers.
- **Scraping private data** -- denied.
- **PAL inside every run** -- Parse -> Ambiguity Scan -> Latent Intent -> Expand -> Compile, then ROSTR (intent -> evidence -> JTBD -> NPAO -> docs -> architecture -> GTM -> taste -> quality).
