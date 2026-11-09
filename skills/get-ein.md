---
name: get-ein
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build the guided IRS EIN packet after entity choice: confirm legal name and entity, identify the responsible party (offline), draft the SS-4, file at IRS.gov EIN online, save the EIN letter to Drive - producing ss4-draft.md and ein-checklist.md with a never-store-SSN/ITIN guardrail and not-legal-advice framing. Use when the user wants to get an e.i.n."
---

# Get an E.I.N.

- **Subagent:** @legal-setup
- **Category:** Legal
- **NPAO:** N
- **List price:** $19
- **Source:** How To Incorporate Your Brand.docx

## When to use
Guided IRS EIN packet after entity choice.

## Steps
1. Confirm legal name and entity
2. Identify responsible party (offline)
3. Draft SS-4
4. File at IRS.gov EIN
5. Save EIN letter to Drive

## Outputs
ss4-draft.md, ein-checklist.md

## Reference tools
- WebFetch irs.gov EIN online
- mcp__google_drive upload

## Guardrails
Never store SSN/ITIN. Not legal advice.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `legal_name` (string, required) and `entity` (string, required) - confirmed in step 1
- `responsible_party` (string) - identified offline; never stored

## Example
Input: EIN for a new Illinois LLC.
1. Confirm legal name + entity (LLC).
2. Responsible party identified offline.
3. Draft SS-4 -> ss4-draft.md; checklist -> ein-checklist.md.
4. File at IRS.gov EIN online (WebFetch the current EIN page first); save the EIN letter via mcp__google_drive.

## Errors & edge cases
- Never store SSN/ITIN anywhere - draft the SS-4 without persisting sensitive identifiers.
- Entity not chosen yet: confirm it first - the packet keys off the entity type.
- mcp__google_drive unavailable: name the missing dependency in the parent handoff and stop.
