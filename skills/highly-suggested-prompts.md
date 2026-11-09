---
name: highly-suggested-prompts
description: "LLM-agnostic developer tooling skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to expertly optimize any prompt — for ChatGPT, Claude, coding assistants, or image generators — diagnosing it against a 7-dimension framework (clarity, specificity, structure, context, constraints, role, examples) and returning a refined version with change-by-change rationale. Use when refining prompts with precision for optimal AI performance and clarity."
---

# Highly Suggested Prompts — Prompt Engineering Expert

## Overview
An **expert prompt optimization and enhancement** system. Takes any prompt — whether for ChatGPT, Claude, coding assistants, or image generators — and refines it for maximum clarity, precision, and effectiveness. Originally a Custom GPT by Pat.

## When to Use
- User is writing or refining a prompt and wants it to be more effective
- User's AI responses are inconsistent or off-target and they need better prompts
- User wants to convert a vague idea into a precise, structured prompt
- User is building a library of reusable prompts (system prompts, templates)
- User asks "can you improve this prompt?" or "why isn't this prompt working?"

## How It Works
The system analyzes the user's original prompt against best practices in prompt engineering: clarity, specificity, structure, context, constraints, output format, and role assignment. It then produces an optimized version and explains what was changed and why.

## Prompt Optimization Framework
| Dimension | What to Check |
|---|---|
| **Clarity** | Is the intent unambiguous? Could it be misinterpreted? |
| **Specificity** | Are the boundaries clear? What's in scope vs out? |
| **Structure** | Is there a logical flow? Should this use sections or steps? |
| **Context** | Does the AI have enough background to respond well? |
| **Constraints** | Are there explicit do's and don'ts? Format requirements? |
| **Role** | Would a persona or role assignment improve output quality? |
| **Examples** | Would few-shot examples clarify the expected output? |

## Steps
1. **Collect**: Get the user's original prompt and understand what they want to achieve
2. **Diagnose**: Identify weaknesses across the 7 optimization dimensions
3. **Refine**: Rewrite the prompt with targeted improvements
4. **Explain**: Walk through what changed and why each change matters
5. **Test Guidance**: Suggest how to evaluate whether the refined prompt works better

## Common Pitfalls
- Over-engineering prompts that already work well — don't fix what isn't broken
- Adding too much structure to prompts that benefit from open-endedness
- Optimizing for one model's quirks at the expense of cross-model portability
- Making prompts longer without actually improving clarity

## Inputs
- The user's original prompt (inline, for any model or use case).
- What they want to achieve — and the symptom if one exists ("can you improve this prompt?", "why isn't this prompt working?", inconsistent/off-target responses, vague idea to structure, reusable prompt library to build).
- Optional: test criteria for evaluating whether the refined prompt works better.

## Outputs
- Diagnosis across the 7 optimization dimensions: clarity, specificity, structure, context, constraints, role, examples.
- The refined prompt with targeted improvements.
- An explanation of what changed and why each change matters.
- Test guidance for evaluating whether the refined prompt performs better.

## Example
A user asks: "can you improve this prompt?" with a vague image-generation prompt.

1. Collect the original prompt and the intended result.
2. Diagnose weaknesses across the 7 dimensions — e.g., missing context (subject detail), no constraints (aspect ratio, style), no output-format specification.
3. Rewrite with targeted fixes, keeping portability across models rather than optimizing for one model's quirks.
4. Walk through what changed and why, and suggest how to test the refined version against the original.
