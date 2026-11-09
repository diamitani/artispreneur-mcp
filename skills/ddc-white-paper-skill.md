---
name: ddc-white-paper-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to present the Delali Development Cycle public framework paper: the problem (prompts are fragile, sprints without fences), the four-layer answer (Cycle + PAL + ROSTR + Runtime), who it is for (operators who should not be asked for Kubernetes; agents that must not free-style), and the cycle taught-then-delivered stage by stage under PAL, ROSTR, AWS Well-Architected, and SDLC governance. Use when working with the Delali Development Cycle white paper."
---

# The Delali Development Cycle

**A planning harness and product-operating system for building premium websites and software with non-technical operators in the loop**

**Version:** 1.0  
**Classification:** Public framework paper  
**Authors:** Diamitani Industries / Site Empire OS lineage  
**Governing methods:** PAL · ROSTR · AWS Well-Architected Framework · Software Development Life Cycle  
**Companion runtime:** DDC Planning Harness v1.0 (`ddc-planning-harness.md`)

---

## Abstract

Most AI site builders skip the road and paint the storefront. The Delali Development Cycle (DDC) is a **planning harness**: a fixed sequence of stages that turns a plain-language goal into executive documents, then into a payable, accessible, observable product. Operators speak at a middle-school reading level. The system writes at a board level. Education is on by default. Go-to-market, taste, and Well-Architected questions are gates, not decorations.

DDC does not replace an engine such as Claude, Codex, or Hermes. It is the car around the engine: steering, brakes, and a map that does not change until an architecture decision record says the factors changed.

---

## 1. The problem

Non-technical founders are told to “just prompt.” Prompts are fragile. They forget payments, tenancy, backups, SEO, and the job the customer hired the site to do. Technical teams are told to “just agile.” Sprints without a fence produce malls when the brief was a shop.

Three failures repeat:

1. **No immutable intake.** Tomorrow’s chat invents a different product.
2. **No ordered artifacts.** Intent, jobs, Now/Next/Later, and a PRD never exist as versioned files.
3. **No lock on build.** Code starts before quality, legal, or architecture can say no.

DDC exists so a studio, agency, or product company can run the same cycle by hand in Asana or by agent in Cursor, Claude, Codex, Hermes, OpenClaw, or Perplexity — and get the same shape of output.

---

## 2. What DDC is

DDC is four things that must stay together:

| Layer | Role |
|---|---|
| **Cycle** | Nine operator stages: Intake → Documentation → Scaffolding → Scripts → Connecting → Deploying → Testing → Refining → Maintaining |
| **PAL** | Parse, Ambiguity Scan, Latent Intent, Expand, Compile — thinking before typing |
| **ROSTR** | Orchestrated artifacts: intent → evidence → JTBD → NPAO → instruction pack → PRD → quality |
| **Runtime** | A state machine that will not advance if a gate fails |

**What it does:** takes type (ecommerce, SaaS, gallery, …), files, links, and a goal, then compiles a product plan **and** a GTM plan, then unlocks build.

**How it works:** one stage, one artifact, one question if blocked, education strip on, executive document under it.

**Why it matters:** best-in-class is a checklist plus taste plus a scale path, not a lucky generation.

---

## 3. Who it is for

- Operators who can describe a business but should not be asked for Kubernetes.
- Agents that must not free-style order.
- Educators who want the “thinking node” visible so the operator learns.

Intake language target: roughly grade 7. Output language target: investment memo / staff-engineer.

---

## 4. The cycle, taught then delivered

Education mode defaults **on**. It may be turned off. Each stage below is written twice in the product: a short teach block, then the artifact.

### 4.1 Intake

**Teach:** We write down what you asked so we do not invent a new product tomorrow.

**Deliver:** an immutable intake record (intake version 1). Site type (or auto). Goal, mission, keys, value proposition (or we help write them). Uploads and reference links. Payments inferred. One to five questions maximum, never a forty-field form.

### 4.2 Documentation (PAL + ROSTR inside)

**Teach:** Blueprints before bricks.

**Deliver, in order:**

1. PAL Parse / Ambiguity / Latent / Expand / Compile
2. Intent spec (fence and non-goals)
3. Evidence ledger and **resource map** (three category leaders; visual, IA, SEO, trust, speed scores — “is this Upwork-level?” becomes a number)
4. JTBD
5. NPAO (Now / Next / Later / Out)
6. Stories, IA, sitemap, flows
7. PRD and specifications
8. Architecture + six Well-Architected answers
9. GTM pack (ICP, persona, AIDA messaging, channels, campaigns, inbound SLA, brand, design system)
10. Quality scorecard on the **plan**

Build is locked until quality dimensions are ≥ 4/5 or a written waiver exists.

### 4.3 Scaffolding

**Teach:** Empty houses with the right rooms.

**Deliver:** Repo tree, a project AGENTS.md file (generated in the scaffolded user repo, not bundled here), skills, env example without values, CI stub.

### 4.4 Scripts

**Teach:** The working parts: accounts, pay, the one job the site exists for.

**Deliver:** Domain code, schema with row-level security, webhook idempotency, tests.

### 4.5 Connecting

**Teach:** Plugs: login, email, payments. Keys never live on the page or in git.

**Deliver:** OAuth redirect matrix, secret names, MCP allowlist. Approval required.

### 4.6 Deploying

**Teach:** Preview, then the real site. We must be able to undo.

**Deliver:** Preview URL, production promotion, `/health` and `/ready`. Approval required.

### 4.7 Testing

**Teach:** We click what a customer clicks.

**Deliver:** Playwright path: sign up, pay (test mode), core job, a11y.

### 4.8 Refining

**Teach:** Compare to the best in your field. Close the gap.

**Deliver:** Taste pass, SEO pass, resource-map delta.

### 4.9 Maintaining

**Teach:** Launch is the start of the life cycle.

**Deliver:** Runbook, backups, learning loop, cost alert.

---

## 5. PAL and ROSTR, every step

PAL is not a kickoff workshop. It is a lens on every stage.

- **Parse:** what was said
- **Ambiguity:** what would wreck us if wrong (money, identity, tenancy)
- **Latent intent:** the job hired
- **Expand:** screens, data, threats, cost, scale topology
- **Compile:** the artifact the next agent is allowed to read

ROSTR is the control plane: the orchestrator owns run state; children write typed artifacts; RAG-DAL is the only research door; side effects need approval; learning is proposed then evaluated.

NPAO is the anti-mall rule. Now is always a vertical slice: landing + identity + pay-if-needed + core job.

---

## 6. GTM compiled on top of product

A beautiful unpaid site is a hobby. After architecture, DDC compiles:

- ICP and persona
- Positioning
- AIDA for hero, pricing, and first email (Attention, Interest, Desire, Action)
- Sales and marketing channels
- Three campaign plays
- Inbound SLA
- Brand playbook and design-system hooks
- Tech stack as an ADR, not a fashion list

Messaging psychology is bounded: clarity, proof, specific promise, one primary action. No dark patterns in v1.

---

## 7. Taste, UI library, resource map, SEO

- **Taste Skill** (`design-taste-frontend`) is the anti-slop gate.
- **UI template library:** landing, OAuth, pricing, checkout, app shell, chat, directory, gallery — same tokens, different adapters per `site_type`.
- **Resource map:** three live peers per type; scores for visual, information architecture, SEO (title, H1, intent match, speed), trust (legal, proof), and job completion.
- Quality question example: “Is my freelance site the same level as Upwork?” Answer with a scored gap, not a compliment.

---

## 8. One-click, no magic prompt

The skill auto-triggers on any site-shaped request. PAL extracts intent. Optional commands exist (`/ddc`, `/ddc educate off`, `/ddc build`) but are not required.

Install surfaces: Cursor skill folder, a Claude Code SKILL.md file, a project AGENTS.md file, Hermes skill, OpenClaw skill, Perplexity Space instructions, GitHub template repository.

The recommended **open-source host** for long-running execution is Nous **Hermes Agent** (skills, MCP, memory, provider-neutral). DDC does not fork it. DDC sits on top as the planner. This paper does not “fund” a harness; it standardizes the planning architecture those runtimes should obey.

---

## 9. Manual system (Asana) and machine system (GitHub)

**Asana** is the human DDC: one template project, sections = stages, tasks = artifacts and gates, description = teach + done-when.

**GitHub** is the machine DDC: scaffolding, skills, runtime TypeScript, white paper, install, UI library stubs, eval fixtures.

Both maps are the same nine stages. A person can walk Asana without an agent. An agent can walk the repo without Asana. Together they are the operating system.

---

## 10. Well-Architected and scale

Every architecture stage answers six pillars: operational excellence, security, reliability, performance efficiency, cost optimization, sustainability. Scale from one user to billions is a **topology** change (pooler, cells, regions), not a rewrite of org / user / entitlement.

---

## 11. Project 2 (separate product)

After DDC v1 is true in docs, Asana, and repo, Project 2 is a **builder portal** (web) and **desktop shell** (Electron) that compete on operator experience with Claude / Hermes / OpenAI desktops: intake, stage rail, education strip, artifact viewer, one-click install of the skill pack, local runtime. That product consumes DDC; it is not a substitute for the cycle.

---

## 12. Truth standard

DDC is “true” when:

1. A stranger can finish a plan from Asana without a hidden prompt.
2. An agent using only the project's AGENTS.md file does not skip to code.
3. Stripe test webhooks and RLS tests exist in the Now slice.
4. Education can be turned off without breaking gates.
5. Resource-map scoring is reproducible from the same three URLs.
6. A golden eval run validates stage order and one-question ambiguity.

Until those pass, claim **framework**, not miracle.

---

## 13. Closing

DDC is duty-shaped software process: love for the operator (simple intake), courage to stop at a gate, peace of a map that does not move every chat. The factors that may change (cloud vendor, design library, payment processor) live in ADRs. The cycle does not.

---

*Paper v1.0. Supersede, do not silently rewrite. Bundled companion file: `ddc-planning-harness.md`. Related but separate deliverables (not bundled with this skill): the ddc-plan skill, the DDC runtime implementation, the project AGENTS.md file, and the premium-site-build-os skill from the skill library.*

## Inputs
- `audience` (string) - operator, agent-builder, educator
- `depth` (enum: abstract / full, default: full)

## Outputs
- The white paper narrative: abstract -> problem -> what-DDC-is -> who-it-is-for -> the cycle taught-then-delivered
- Companion pointer: DDC Planning Harness v1.0

## Example
Input: explain DDC to a non-technical founder.
1. Problem: "Most AI site builders skip the road and paint the storefront."
2. What it is: nine stages with PAL and ROSTR inside every stage; the car around the engine.
3. How it works for her: she describes the business in plain words; the system teaches each step, then delivers board-level documents and only then unlocks build.

## Errors & edge cases
- Reader wants to skip to build: the paper's position is explicit - build is locked until the plan's quality gates pass.
- Confusing DDC with an engine: DDC does not replace Claude/Codex/Hermes - it is the harness around the engine.
