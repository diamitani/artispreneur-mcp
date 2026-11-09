---
name: create-split-sheet-agreement
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to document writer/producer splits before submission or distribution: list contributors, lock % composition and master points, sign, save to Drive, log in Notion - producing split-sheet.md from the split-sheet template, with a not-a-substitute-for-counsel-on-samples guardrail. Use when the user wants to create a split sheet agreement."
---

# create split sheet agreement

- **Subagent:** @music-contract-agent
- **Category:** Legal
- **NPAO:** N
- **List price:** $19
- **Source:** Submission gate

## When to use
Writer/producer splits before submission or distribution.

## Steps
1. List contributors
2. % composition
3. master points
4. sign
5. save to mcp__google_drive
6. log in mcp__notion

## Outputs
split-sheet.md

## Reference tools
- reference/templates/split-sheet.md
- mcp__google_drive
- mcp__notion

## Guardrails
Not a substitute for counsel on samples.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `contributors` (list, required) - writers/producers with roles
- `composition_pct` (object, required) - % splits summing to 100
- `master_points` (object) - master royalty points
- `signatures` (list) - all contributors sign

## Example
Input: split sheet for a 2-writer, 1-producer single.
1. List contributors: writer A (lyrics/melody), writer B (melody), producer C (beat).
2. Lock composition: 40/35/25; master points agreed.
3. All sign; save split-sheet.md to mcp__google_drive; log in mcp__notion.

## Errors & edge cases
- Splits don't sum to 100: stop - do not produce the sheet until the math closes.
- Samples involved: flag the not-a-substitute-for-counsel guardrail before proceeding.
- Missing signature: the sheet is a draft until every contributor signs.
