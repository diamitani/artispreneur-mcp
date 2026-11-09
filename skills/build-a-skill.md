---
name: build-a-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to package a SKILL.md for preload: name/description/when-to-use, inputs/outputs, NPAO + list price, guardrails (no disable-model-invocation preloads), committed via mcp__github PR - reporting artifacts and blockers in the parent handoff. Use when the user wants to build a skill."
---

# Build a Skill

- **Subagent:** @agent-factory
- **Category:** Platform
- **NPAO:** P
- **List price:** $19
- **Source:** Claude Code skills docs

## When to use
Package a SKILL.md for preload.

## Steps
1. name/description/when-to-use
2. inputs/outputs
3. NPAO+price
4. guardrails
5. commit via mcp__github PR

## Outputs
SKILL.md

## Reference tools
- reference/tools/claude-code-subagent-fields.md
- mcp__github

## Guardrails
No disable-model-invocation preloads.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `name` (string, required) - skill slug
- `description` (string, required) - what it does + when to use it
- `when_to_use` (string, required)
- `inputs` / `outputs` (lists) - parameters and deliverables
- `subagent` (enum: @agent-factory..., required), `category`, `npao`, `list_price`

## Example
Input: package a new outreach skill.
1. Draft SKILL.md: name, description, when-to-use; inputs (targets, approval); outputs (pitch-email.md).
2. Assign @agent-factory, NPAO=P, list price $19.
3. Guardrails check: no disable-model-invocation preload.
4. Commit via mcp__github PR; parent handoff summarizes the artifact.

## Errors & edge cases
- Missing name or description: refuse to package - both are required.
- A disable-model-invocation preload is requested: blocked by Guardrails - name it and stop.
- mcp__github unavailable: name the missing dependency in the parent handoff and stop.
