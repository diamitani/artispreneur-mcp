---
name: create-llc
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to produce the state LLC formation brief and operating agreement draft: choose LLC vs S-Corp vs C-Corp, pick the state, walk the Department of State filing, articles checklist, operating agreement draft, and the $50-$250 fee - delivering articles-checklist.md and operating-agreement-draft.md via Drive, marked not legal advice. Use when the user wants to create an llc."
---

# Create an LLC

- **Subagent:** @legal-setup
- **Category:** Legal
- **NPAO:** N
- **List price:** $49
- **Source:** How To Incorporate Your Brand.docx

## When to use
State LLC formation brief and operating agreement draft.

## Steps
1. Choose LLC vs S-Corp vs C-Corp
2. Choose state
3. Dept of State site
4. Articles checklist
5. Operating agreement draft
6. Pay $50-$250 fee

## Outputs
articles-checklist.md, operating-agreement-draft.md

## Reference tools
- reference/templates/operating-agreement-stub.md
- mcp__google_drive upload

## Guardrails
Not legal advice.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `entity_choice` (enum: LLC / S-Corp / C-Corp, required) - confirmed with the user in step 1
- `state` (string, required) - formation state
- `members` (list) - members and ownership splits for the operating agreement

## Example
Input: single-member LLC in Illinois for a music brand.
1. Confirm LLC vs S-Corp vs C-Corp: LLC chosen.
2. State: Illinois; pull the Department of State filing steps.
3. Articles checklist completed; operating agreement drafted from the stub template.
4. Fee range ($50-$250) noted; both documents uploaded via mcp__google_drive.

## Errors & edge cases
- Entity choice unclear: confirm before drafting - the documents differ.
- Not legal advice: the guardrail applies to every output; recommend counsel for edge cases.
- mcp__google_drive unavailable: name the missing dependency in the parent handoff and stop.
