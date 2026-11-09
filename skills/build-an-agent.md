---
name: build-an-agent
description: "LLM-agnostic developer tooling skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to compile a Claude Code subagent markdown file: name + description, tools allowlist, model selection, skills preload (skipping files missing name/description), committed via mcp__github PR - with artifacts and blockers summarized in the parent handoff. Use when the user wants to build an agent."
---

# Build an Agent

- **Subagent:** @agent-factory
- **Category:** Platform
- **NPAO:** P
- **List price:** $29
- **Source:** Claude Code subagent docs

## When to use
Compile a Claude Code subagent markdown file.

## Steps
1. name+description
2. tools allowlist
3. model
4. skills preload
5. commit via mcp__github PR

## Outputs
agent.md

## Reference tools
- reference/tools/claude-code-subagent-fields.md
- mcp__github

## Guardrails
Skip files missing name/description.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `name` (string, required) and `description` (string, required) - agent identity
- `tools` (list) - allowlisted tools
- `model` (string) - model selection
- `skills` (list) - skills to preload; files missing name/description are skipped per Guardrails

## Example
Input: build an outreach subagent.
1. name: outreach-agent; description: what it does + when to invoke.
2. Tools allowlist: hubspot, outlook, bitly connectors.
3. Model + skills preload; skip any skill file missing name/description.
4. Commit via mcp__github PR; parent handoff summarizes artifacts + blockers.

## Errors & edge cases
- Skill file missing name/description: skip it per Guardrails - do not preload a nameless skill.
- mcp__github unavailable: name the missing dependency in the parent handoff and stop.
