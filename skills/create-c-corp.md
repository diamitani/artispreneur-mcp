---
name: create-c-corp
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build the C-Corp outline for scale or investors: confirm the need, define shareholders/board/officers, draft the bylaws outline, set stock classes, file articles - uploaded via mcp__google_drive as bylaws-outline.md, with a double-taxation warning. Use when the user wants to create a c-corp."
---

# Create a C-Corp

- **Subagent:** @legal-setup
- **Category:** Legal
- **NPAO:** O
- **List price:** $79
- **Source:** How To Incorporate Your Brand.docx

## When to use
C-Corp outline for scale or investors.

## Steps
1. Confirm need
2. Shareholders/board/officers
3. Bylaws outline
4. Stock classes
5. File articles

## Outputs
bylaws-outline.md

## Reference tools
- mcp__google_drive upload

## Guardrails
Warn double taxation.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `need` (string, required) - why a C-Corp: scale, investors...
- `shareholders` / `board` / `officers` (lists) - who holds what roles
- `stock_classes` (list) - classes and rights

## Example
Input: C-Corp outline for a two-founder startup raising a seed round.
1. Confirm the need: investor-ready entity.
2. Shareholders/board/officers defined; stock classes (common + authorized preferred).
3. Bylaws outline drafted; articles filing steps listed.
4. Upload bylaws-outline.md via mcp__google_drive with the double-taxation warning.

## Errors & edge cases
- C-Corp not actually needed (LLC would do): confirm the need first - say so if the facts point elsewhere.
- Double taxation: warn explicitly before any filing steps.
- mcp__google_drive unavailable: name the missing dependency in the parent handoff and stop.
