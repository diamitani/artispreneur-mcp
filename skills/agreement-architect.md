---
name: agreement-architect
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to draft tailored partnership agreements and contract templates: collecting parties, terms, scope, duration, and compensation, then producing a structured Word/doc document with standard clauses and an explicit not-legal-advice disclaimer. Use when crafting custom partnership agreements, contracts, and legal document templates in Word format."
---

# Agreement Architect

## Overview

Generates custom general partnership agreements and other contractual documents in structured formats. Crafts agreements tailored to specific business relationships, terms, and requirements.

## When to Use

- User needs a partnership agreement drafted
- Creating contract templates for business relationships
- Generating structured legal documents in Word/doc format
- Defining terms, responsibilities, and provisions between parties

## How It Works

Guides users through providing the necessary information (parties, terms, scope, duration, compensation) and generates a structured, professional agreement document.

## Steps

1. **Gather requirements** — Identify parties, business type, scope, and key terms
2. **Determine agreement type** — Partnership, service, NDA, licensing, or other
3. **Draft structure** — Build the agreement framework with standard clauses
4. **Customize terms** — Tailor specific provisions to the user's situation
5. **Output document** — Generate in requested format (Word doc, markdown, text)
6. **Disclaimer** — Always note this is not legal advice; recommend attorney review

## Common Pitfalls

1. **Over-customization** — Don't add clauses that contradict standard legal frameworks
2. **Missing jurisdiction** — Agreements should specify governing law and venue
3. **Vague terms** — Payment terms, deliverables, and timelines must be specific
4. **Not recommending legal review** — Always advise users to have an attorney review

## Source

Originally deployed as a custom GPT: [Agreement Architect](https://chatgpt.com/g/g-U53E2wyFn-agreement-architect)

## Inputs
- `parties` (list, required) - full legal names and roles of each party
- `agreement_type` (enum: partnership / service / NDA / licensing / other, required)
- `terms` (object) - scope, duration, compensation, responsibilities, termination
- `jurisdiction` (string, required) - governing law and venue
- `format` (enum: docx / markdown / text, default: docx)

## Outputs
- Structured agreement document with standard clauses customized to the terms
- Clause-by-clause rationale for non-standard provisions
- Disclaimer block: not legal advice; attorney review recommended

## Example
Input: two founders forming a general partnership, 50/50 profit split, California jurisdiction, 2-year initial term.
1. Confirm parties, the 50/50 split, vesting, and decision-making rules.
2. Select partnership type; set governing law to California.
3. Draft: parties, scope, capital contributions, profit/loss allocation, management, term/termination, dispute resolution.
4. Output .docx with the not-legal-advice disclaimer and a recommendation for attorney review.
