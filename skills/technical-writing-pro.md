---
name: technical-writing-pro
description: "Professional technical writing -- refining technical copy for clarity and audience fit, documenting processes (SOPs, runbooks), writing API references and integration guides, and crafting goal-oriented documents (proposals, RFPs, specs, white papers) with consistent style-guide application. Use when refining technical copy, creating processes, and crafting goal-oriented documents."
---

# Technical Writing Pro

Professional technical writing: refine copy, document processes, and create goal-oriented materials.

## Core Capabilities
- **Technical Copy Refinement**: Edit for clarity, precision, and audience appropriateness
- **Process Documentation**: SOPs, workflows, onboarding guides, runbooks
- **API Documentation**: Endpoint references, integration guides, SDK docs
- **Goal-Oriented Documents**: Proposals, RFPs, technical specifications, white papers
- **Style Consistency**: Apply style guides (Google, Microsoft, Chicago Manual) consistently

## Workflow
1. Identify document type, audience, and goal
2. Audit existing content for gaps, jargon, and structural issues
3. Restructure for logical flow and scannability
4. Refine language for clarity while preserving technical accuracy
5. Add navigation aids (TOC, cross-references, callout boxes)

## Writing Principles
- **Audience First**: Match complexity to reader expertise
- **Concrete Over Abstract**: Use examples, not vague descriptions
- **Active Voice**: "Click the button" not "The button should be clicked"
- **Progressive Disclosure**: Overview → Details → Deep Dive

## Pitfalls
- Don't sacrifice accuracy for simplicity
- Verify all procedural steps with actual testing
- Maintain version tracking for living documents

## Inputs

- `document` -- the draft or source material; `document_type` (API reference, SOP/runbook, proposal, RFP, spec, white paper, onboarding guide); `audience` (expertise level to match); `goal` (what the document must achieve)
- `style_guide` -- Google, Microsoft, or Chicago Manual (applied consistently)

## Outputs

- Refined copy: audited for gaps/jargon/structure, restructured for flow and scannability, language clarified without losing technical accuracy, with navigation aids (TOC, cross-references, callout boxes); follows Audience-First, Concrete-Over-Abstract, Active-Voice, Progressive-Disclosure (Overview -> Details -> Deep Dive)

## Example

A draft API integration guide: audit finds missing auth section and passive-voice procedures -> restructured (Overview -> Authentication -> Endpoints -> Deep Dive) -> "The button should be clicked" becomes "Click the button" -> TOC + callout boxes added -> procedural steps verified by actual testing.

## Errors & edge cases

- **Accuracy sacrificed for simplicity** -- never; clarity must preserve technical precision.
- **Untested procedures** -- verify all procedural steps with actual testing before publishing.
- **No version tracking** -- living documents need version history.
- **Audience mismatch** -- match complexity to reader expertise; don't write a deep-dive for an overview audience.
