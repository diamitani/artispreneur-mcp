---
name: response-structure-skill
description: "Turns RFP or questionnaire answers into a complete, submission-ready proposal -- cover page, the RFP's own section order preserved for evaluator scoring, direct-answer-first drafting pattern, consistency rules, and a gap list of every not-met/partial/assumed requirement. Use when working with rfp response structure."
---

# RFP Response Structure

## When to use

Use this skill whenever you must turn RFP or questionnaire answers into a
complete, submission-ready proposal response: single-question answers,
full RFP workbooks, security questionnaires, and vendor assessments.

## Common Sections

1. Company overview
2. Product capability answers
3. Security and compliance
4. Implementation and support
5. Commercial or procurement notes

## Drafting Pattern

- Short answer first
- Supporting detail second
- Caveat or assumption last when needed

## How to structure a full response

Start with a cover page (respondent name, RFP title, date, contact) and a
table of contents. Then follow the RFP's own section order — never reorder
sections, because evaluators score by matching your answers to their numbered
requirements. For every numbered requirement, give the direct answer first in
one or two sentences, then add the evidence or detail that supports it
(screenshots, architecture notes, references), then close with any caveat or
assumption the answer depends on. If a requirement cannot be met, say so
plainly in the same slot and propose the closest alternative — a missing
answer discovered by the evaluator scores worse than an honest partial one.

## Consistency rules

- Use the same product and company names everywhere; never invent variant names.
- Keep tense and voice consistent (present tense, active voice).
- Mirror the RFP's terminology for key concepts so keyword matching works.
- Mark every figure and attachment with the section number it supports.

## Handoff

Deliver the draft as an editable document (Word or the RFP's workbook
format), plus a gap list: every requirement marked not-met, partial, or
answered-with-assumption, so the owner can review before submission.

## Inputs

- `rfp_document` -- the RFP or questionnaire: single-question answers, full RFP workbooks, security questionnaires, vendor assessments
- `answers` -- draft answers keyed to the RFP's numbered requirements

## Outputs

- An editable draft (Word or the RFP's workbook format) following the RFP's own section order -- cover page, table of contents, then direct answers with supporting evidence -- plus a **gap list**: every requirement marked not-met, partial, or answered-with-assumption, for owner review before submission

## Example

A 40-question security questionnaire: each numbered requirement gets a 1-2 sentence direct answer first, supporting evidence (screenshots, architecture notes) second, and any caveat last. Requirement 17 (SOC 2 Type II) is honestly marked not-met with the closest alternative proposed -- and appears on the gap list for the owner.

## Errors & edge cases

- **Reordered sections** -- never reorder; evaluators score by matching answers to numbered requirements.
- **Unmeetable requirement** -- say so plainly in the same slot and propose the closest alternative; a missing answer scores worse than an honest partial one.
- **Inconsistent naming** -- same product and company names everywhere; mirror the RFP's terminology so keyword matching works; mark every figure/attachment with the section number it supports.
