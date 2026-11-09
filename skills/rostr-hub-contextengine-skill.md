---
name: rostr-hub-contextengine-skill
description: "Wires ROSTR Hub's runtime coordination layer -- the R-O-S-T-R layers (Runtime, Orchestration, State, Tools, Reference) -- with ContextEngine's zero-infrastructure flat-file memory, so an agent or multi-agent system coordinates steps, binds tools, and remembers projects across sessions. Use when wiring orchestration or persisting state across sessions."
---

# ROSTR Hub + ContextEngine

**Canonical source:** ROSTR Hub https://rostr-paper.vercel.app/#s7 · ContextEngine https://rostr-paper.vercel.app/#s8
*Read this file before wiring orchestration or persisting state. Fetch the live section only if a definition is still unclear.*

---

## ROSTR Hub — the coordination layer

ROSTR Hub is the runtime coordination layer for an agent or multi-agent system. Its five layers spell **R-O-S-T-R**.

### R — Runtime
The PAL-compiled config that actually runs.
- System prompt source: `SKILL.md` + `CLAUDE.md` ({{COMPANY_NAME}} context) + locked KB schema.
- Tool bindings: from the PAL L3 priority list.
- Version + scope (project vs. team).
- Model routing: lighter model for intake/formatting; stronger model for PRD/JTBD; reserve top tier for complex enrichment. Default to the latest Claude models.

### O — Orchestration
How steps and agents are sequenced.
- **Pattern:** sequential with conditional branching (default for the New Project System pipeline).
- **Pipeline:** Intake → DB write → KB agent → PAL engine → RAG/DAL → generation fan-out (PRD, diagram, reporting, tech stack) → JTBD plan (requires PRD) → artifact save.
- **Conditional branches:** no files/URLs → skip `web_fetch`; Asana ID present → pull task first; similar past project → surface prior KB; PRD quality gate fails → loop back to enrichment before JTBD.
- **Delegation:** the Planner (this skill, Agent 1) hands a self-contained Handoff Package to the Builder (Agent 2). No sub-agents needed for v1.
- **Trigger:** user prompt in chat (primary); n8n webhook from Asana (secondary).

### S — State
What is remembered.
- **Per-session:** raw inputs, project name/type, file paths (KB, PRD, JTBD), quality gate status, enrichment sources used.
- **Persistent (survives sessions):** all artifact paths in the project index, the domain taxonomy map (improves over time), quality feedback scores.
- **Shared:** the project index is readable by any teammate with directory access.

### T — Tools
The bound capabilities and their limits.
- `rag_dal.*`, `notion_api`, `asana_api`, `n8n_webhook`, `file_read_write`, `mermaid_renderer`, plus GTM tools (`hubspot_api`, `clay_table`, `amplemarket_api`).
- Track auth + rate limits per tool (e.g., Notion 3 req/sec → batch writes; Asana 1,500 req/min).

### R — Reference
The grounding knowledge.
- {{COMPANY_NAME}} org context (`CLAUDE.md`), locked templates (KB taxonomy, PRD template, JTBD format, naming convention), prior outputs (past KBs, past enrichment source lists).

---

## ContextEngine — persistent memory

ContextEngine gives the system memory across sessions with **zero infrastructure** — flat files on disk.

### Storage path (non-negotiable)
```
.context-engine/sessions/[project-name]/
```

### Modes
- **CACHE** (primary): store every project package run through the system.
- **RETRIEVE** (secondary): surface relevant past projects when a new intake is similar.
- **REPORT** (tertiary): generate the project index / activity digest on demand.

### What gets stored per session
```
project_id · project_name · project_type · submission_date
raw_input_summary (first 500 chars)
kb_file_path · prd_file_path · jtbd_plan_file_path
enrichment_sources_used · quality_gate_status · user_quality_score
tags (auto-extracted: tools, domain, team)
```

### Directory layout
```
.context-engine/
├── sessions/[project-name]/
│   └── [project-id]-session.md     (per-project context record)
└── CONTEXT.md                       (project index — all projects + metadata)

/New Project Automation/
├── projects/[YYYY-MM-DD]-[project-name]/   (the artifact package)
└── PROJECT_INDEX.md                         (master registry)
```

### Persistence scope
- Level: project (Patrick first; team-level on rollout).
- TTL: indefinite — projects don't expire; they are manually archived.

Use ContextEngine to (1) avoid rebuilding projects that already exist, (2) reuse prior enrichment to sharpen RAG queries, and (3) answer "show me every active GTM project" with confidence.

## Inputs

- `pal_config` -- the PAL-compiled runtime config (system prompt sources: SKILL.md + CLAUDE.md + locked KB schema; tool bindings from the PAL L3 priority list; model routing by step)
- `tool_bindings` -- `rag_dal.*`, `notion_api`, `asana_api`, `n8n_webhook`, `file_read_write`, `mermaid_renderer`, plus GTM tools (`hubspot_api`, `clay_table`, `amplemarket_api`); auth + rate limits tracked per tool
- `storage_path` -- `.context-engine/sessions/[project-name]/` (non-negotiable); the project index lives at `.context-engine/CONTEXT.md`

## Outputs

- A coordinated runtime: sequential-with-conditional-branching orchestration pipeline (Intake -> DB write -> KB agent -> PAL engine -> RAG/DAL -> generation fan-out -> JTBD plan -> artifact save), per-session + persistent + shared state, and ContextEngine memory in three modes: CACHE (store every run), RETRIEVE (surface similar past projects), REPORT (project index / activity digest)

## Example

The New Project System pipeline: user prompt triggers Intake -> Asana ID present? pull the task first -> KB agent -> PAL engine -> RAG/DAL enrichment (PRD quality gate fails? loop back before JTBD) -> generation fan-out (PRD, diagram, reporting, tech stack) -> JTBD plan -> artifact save. The run is stored under `.context-engine/sessions/[project]/` so a similar intake next week surfaces this KB and reuses its enrichment sources.

## Errors & edge cases

- **Unclear definition** -- this file is the working reference; fetch the live canonical sections (rostr-paper.vercel.app #s7/#s8) only if a definition is still unclear.
- **PRD quality gate fails** -- conditional branch loops back to enrichment before JTBD; never generate the plan from a failed PRD.
- **Projects never expire** -- TTL is indefinite; archive manually.
- **Conditional branches skipped** -- no files/URLs -> skip `web_fetch`; a similar past project exists -> surface its prior KB instead of re-enriching from zero.
