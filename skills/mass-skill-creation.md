---
name: mass-skill-creation
description: "Converts catalogs, portfolios, or spreadsheets of 20+ items into Hermes skills in bulk via a 5-phase batch-delegation pattern — parse & cluster with aggressive consolidation (V1/V2/V3 → one skill), design the skill map, dispatch 5–6 parallel sub-agents at 8–12 skills each, run a straggler pass, build a master portfolio-index — proven on ~185 items → ~124 consolidated skills. Use when converting a catalog, portfolio, or spreadsheet of items into Hermes Agent skills in bulk (>20 items)."
---

# Mass Skill Creation from Portfolios & Catalogs

## Overview

When a user has a catalog of items (GPTs, tools, templates, configurations) and says "turn these all into skills," the naive approach of creating one skill per row fails. This skill encodes the proven batch-delegation pattern for converting ~185 items into ~124 consolidated skills across categories.

## When to Use

- User provides a spreadsheet, JSON, or list of >20 items to convert into skills
- Migrating a portfolio of tools/GPTs/configurations
- "Turn these all into skills" with a large dataset

Don't use for fewer than ~8 items — just create directly with `skill_manage`.

## How It Works

### Phase 1: Parse and Cluster

1. **Read the source data** — parse the spreadsheet/JSON to understand columns, descriptions, and relationships.
2. **Group by domain** — cluster items into categories (productivity, software-dev, music-industry, etc.).
3. **Identify consolidation candidates** — items that are iterative versions of the same idea get merged into one skill.

**Consolidation rule:** If PromptBuilder V1, V2, and V3 all exist, create ONE `prompt-builder-architect` skill. List the originals in a "Source" section.

### Phase 2: Design the Skill Map

For each cluster, produce:
- **Skill name** (lowercase, hyphens, ≤64 chars)
- **Category** (match existing: productivity, software-development, music-industry, lifestyle, creative, education)
- **Description** (≤1024 chars, start with "Use when…")
- **Which source items it consolidates**

Create a master index skill that maps every source item to its skill.

### Phase 3: Dispatch Parallel Sub-Agents

Use `delegate_task` with 5-6 parallel sub-agents, each handling 8-12 skills:

```
delegate_task(tasks=[
  {goal: "Create 10 GTM/business skills using skill_manage...",
   context: "Use skill_manage(action='create', category='productivity')...",
   toolsets: ["skills"]},
  {goal: "Create 10 music-industry skills...",
   toolsets: ["skills"]},
  ...
])
```

**Key settings:**
- `toolsets: ["skills"]` — sub-agents only need `skill_manage`
- Provide full descriptions inline in the goal — sub-agents have no conversation memory
- Spec file paths and structure expectations explicitly

### Phase 4: Straggler Pass

After all parallel agents return, scan for missing items:

```python
# In execute_code: walk ~/.hermes/skills/ and diff against expected names
import os
skills_dir = os.path.expanduser("~/.hermes/skills/")
existing = set()
for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" in files:
        existing.add(os.path.basename(root))
missing = [name for name in expected if name not in existing]
```

Create stragglers directly with `skill_manage(action='create')` — faster than re-dispatching for a handful of items.

### Phase 5: Create the Index

Build a `portfolio-index` skill with a table per category mapping source items to consolidated skills. This is the single entry point for the entire catalog.

## Common Pitfalls

1. **185 one-line skills are worse than 0.** The model pays for every loaded skill's description every turn. Consolidate aggressively — group iterative versions, merge near-duplicates, skip pure test/one-off items.
2. **Sub-agents can't see each other's creations.** If batch A creates skills that batch B should reference via `related_skills`, accept imperfect cross-referencing or do a post-hoc cleanup pass.
3. **Skill loader cache.** New skills won't appear in `skills_list` until a fresh session. Don't re-create skills that already exist — the sub-agents will report "already exists" and that's fine.
4. **Sub-agent batch size.** 10-12 skills per sub-agent works reliably. Larger batches risk hitting iteration limits. For 50+ skills, split into 5-6 parallel sub-agents.
5. **Category consistency.** Ensure all sub-agents use the same category names. Provide the exact category string in the goal — don't rely on sub-agent inference.
6. **Don't delegate skills needing tight cross-references.** If skills need `related_skills` pointing at each other, create them all in ONE batch (same sub-agent) or create first, then patch references.

## Verification Checklist

- [ ] All source items are accounted for in at least one skill or intentionally skipped
- [ ] Master index skill maps every source item → consolidated skill
- [ ] No two skills have the same name or cover identical territory
- [ ] Each skill has valid YAML frontmatter with name, description, tags
- [ ] Categories are consistent and match existing directory structure
- [ ] Consolidation is aggressive — iterative versions merged, test/one-off items skipped
- [ ] Sub-agent straggler pass confirmed no remaining missing skills

## Inputs

- `source_data` (required) — spreadsheet, JSON, or list of **>20 items** (fewer than ~8 → create directly with `skill_manage`, don't use this skill)
- Consolidation rule: iterative versions merged (V1/V2/V3 → one skill), near-duplicates merged, pure test/one-off items skipped — 185 one-line skills are worse than 0 (the model pays per loaded description every turn)
- Skill map per cluster: `name` (lowercase, hyphens, ≤64 chars), `category` (match existing: productivity, software-development, music-industry, lifestyle, creative, education — exact strings, no inference), `description` (≤1024 chars, starts with ‘Use when…’), which source items it consolidates
- Dispatch: `delegate_task` with 5–6 parallel sub-agents, 8–12 skills each, `toolsets: ["skills"]`, full descriptions + spec paths inline in each goal

## Outputs

- Consolidated skills created via `skill_manage(action='create', category=...)` — aggressive consolidation, no duplicate names or overlapping territory, valid YAML frontmatter (name, description, tags)
- Straggler pass: filesystem walk of `~/.hermes/skills/` diffed against expected names; missing items created directly
- A master `portfolio-index` skill: one table per category mapping every source item → its consolidated skill
- Verification checklist: all source items accounted for or intentionally skipped, categories consistent, consolidation aggressive
- Format: skills on disk + the index skill as the catalog's single entry point

## Example

185 GPTs in a spreadsheet → Phase 1: parse columns, cluster into productivity / software-dev / music-industry; PromptBuilder V1, V2, V3 → ONE `prompt-builder-architect` (originals listed in its Source section). Phase 2: skill map — names ≤64 chars, categories matched to existing, descriptions ≤1024 chars starting ‘Use when…’. Phase 3: 6 parallel sub-agents × ~10 skills via `delegate_task` (`toolsets: ["skills"]`, full descriptions inline — sub-agents have no conversation memory). Phase 4: walk `~/.hermes/skills/`, diff against expected names, create stragglers directly with `skill_manage`. Phase 5: `portfolio-index` skill with per-category source→skill tables — the single entry point.
