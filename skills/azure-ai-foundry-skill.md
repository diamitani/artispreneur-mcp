---
name: azure-ai-foundry-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to guide model and prompt decisions for Azure AI Foundry workflows: current Anthropic Claude deployment references (claude-sonnet-4-6 for reasoning-heavy decomposition, 4-5 fallback, haiku-4-5 for rapid variants), a role split (reasoning vs rewriting), the three-step prompt orchestration chain (reasoning -> structured brief -> final prompt), and guardrails (secrets out of prompts, never invent unsupported tools). Use when working with Azure AI Foundry."
---

# Azure AI Foundry

Use this reference when the workflow-builder output needs a model recommendation, deployment note, or prompt orchestration plan through Azure AI Foundry.

Official doc:
- `https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-claude`

## Current Anthropic Claude Deployments To Reference

Based on the current Microsoft Learn Azure AI Foundry Claude guidance:

- `claude-sonnet-4-6`: strongest default for reasoning-heavy workflow decomposition, system planning, and design-direction generation
- `claude-sonnet-4-5`: acceptable fallback when 4.6 is unavailable
- `claude-haiku-4-5`: faster and lighter for rapid iterations, rewrites, variants, and prompt compression

Do not rename deployments in final outputs. If the environment-specific deployment name is unknown, call it out and refer to the model family plus the expected deployment alias.

## Recommended Role Split

- Use Sonnet 4.6 to:
  - unpack ambiguous briefs
  - identify actors, states, and exception paths
  - generate high-quality design direction
  - critique weak visual prompts

- Use Haiku 4.5 to:
  - spin multiple prompt variants
  - rewrite copy to fit frames or nodes
  - compress detailed briefs into concise image prompts
  - generate low-risk alternatives quickly

## Prompt Orchestration Pattern

Use a three-step chain:

1. reasoning
2. structured brief
3. final prompt

Example structure:

```text
Reasoning prompt:
Turn this rough request into a workflow specification, identify hidden constraints, and propose one bold but practical design direction.

Structured brief:
Return JSON with objective, audience, workflow_layers, visual_style, palette, constraints, and frame_plan.

Final prompt:
Generate one concise image prompt for a polished concept board using the structured brief only.
```

## Guardrails

- Keep secrets and endpoint details outside the prompt body.
- Avoid asking the model to invent unsupported tools or product features.
- Use the reasoning model to decide what to draw; use the lighter model to vary how it is phrased.

## Inputs
- `task` (string, required) - what the workflow needs: model recommendation, deployment note, or prompt orchestration plan
- `deployment_name` (string) - environment-specific deployment name if known; otherwise the model family + expected alias is used
- `complexity` (enum: reasoning-heavy / rapid-iteration, default: reasoning-heavy)

## Outputs
- Model recommendation: claude-sonnet-4-6 (reasoning, planning, design direction), 4-5 (fallback), or claude-haiku-4-5 (variants, rewrites, compression)
- Three-step orchestration: reasoning prompt -> structured JSON brief -> final concise prompt

## Example
Input: need a workflow that turns rough briefs into polished concept-board image prompts.
1. Task: prompt orchestration plan; complexity: reasoning-heavy -> claude-sonnet-4-6.
2. Reasoning prompt: unpack the brief, surface hidden constraints, propose one bold practical design direction.
3. Structured brief: JSON with objective, audience, workflow_layers, visual_style, palette, constraints, frame_plan.
4. Final prompt: one concise image prompt from the brief only (haiku-4-5 for variants).

## Errors & edge cases
- Deployment name unknown: do not invent one - call it out and refer to the model family plus expected alias.
- Never rename deployments in final outputs.
- Guardrails: secrets and endpoint details stay out of the prompt body; never ask the model to invent unsupported tools.
