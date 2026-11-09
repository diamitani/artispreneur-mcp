---
name: output-spec-skill
description: "Defines the exact structure of the two-tab Excel knowledge workbook this pipeline produces — Tab 1: {{COMPANY_NAME}} General Knowledge, Tab 2: Country-Specific Knowledge — with an 11-column schema (Question, Answer, Knowledge Type, Owner, Country, Source, Review Status, Conflict Flag, Notes, Date Extracted, Onspring Ready), review-status and conflict-flag enums, auto-populated conflict notes, formatting rules, and an Onspring upload mapping. Use when producing the output-spec knowledge workbook."
---

# Output Specification

This document defines the exact structure of the two-tab Excel workbook produced by this skill.

---

## Workbook Structure

**File name:** `{{COMPANY_FILE}}

**Tab 1: {{COMPANY_NAME}} Knowledge**
All rows where `knowledge_type = "{{COMPANY_NAME}} General Knowledge"`

**Tab 2: Country-Specific Knowledge**
All rows where `knowledge_type = "Country-Specific Knowledge"`

---

## Column Schema (both tabs)

| # | Column Name | Type | Description |
|---|---|---|---|
| 1 | **Question** | Text | Neutral, reusable question phrasing. Should be answerable by the Answer in this row. |
| 2 | **Answer** | Text | Source-grounded answer. Include qualifiers. 1–4 sentences max. |
| 3 | **Knowledge Type** | Enum | `{{COMPANY_NAME}} General Knowledge` or `Country-Specific Knowledge` |
| 4 | **Owner** | Enum | `Product` / `HRSD` / `Finance` / `VGM` / `Implementation` / `Other` |
| 5 | **Country** | Text | Country name if Country-Specific. Leave blank for {{COMPANY_NAME}} General. |
| 6 | **Source** | Text | Name of the source document or ticket (e.g., "RFP - Schaeffler Group", "HubSpot Ticket #12345") |
| 7 | **Review Status** | Enum | See values below |
| 8 | **Conflict Flag** | Enum | See values below |
| 9 | **Notes / Reviewer Comment** | Text | Auto-populated context for conflicts. Also used for human reviewer comments post-delivery. |
| 10 | **Date Extracted** | Date | Date this row was generated (YYYY-MM-DD) |
| 11 | **Onspring Ready** | Boolean | `TRUE` once a human has reviewed and approved. Default: `FALSE` for needs_review, `TRUE` for confirmed/new facts that passed extraction. |

---

## Review Status Values

| Value | Meaning |
|---|---|
| `new` | No matching fact in the existing KB. Proposed for first-time addition. |
| `confirmed` | Matches an existing KB fact. Source confirmed the answer. No change needed. |
| `needs_review` | Ambiguous classification, uncertain owner, conditional answer, or weak source. Requires human judgment before acceptance. |

---

## Conflict Flag Values

| Value | Meaning |
|---|---|
| *(blank)* | No conflict detected |
| `enrichment` | New fact adds detail to an existing KB fact without contradicting it |
| `conflict` | New fact contradicts an existing KB fact |
| `scope_reduction` | New fact narrows the scope of an existing KB fact (e.g., General → Country-Specific) |

---

## Notes Field Format (auto-populated for conflicts)

When a conflict is detected, auto-populate the `Notes` field in this format:

```
[CONFLICT TYPE: conflict | enrichment | scope_reduction]

EXISTING KB ANSWER:
"[existing answer text]"
Source: [existing KB source]

NEW PROPOSED ANSWER:
"[new answer text]"
Source: [new source document]

REASON FOR FLAG:
[1–2 sentence explanation of why this was flagged]

RECOMMENDED REVIEWER: [Owner]
```

For `new` facts with no conflict, leave `Notes` blank or include a brief extraction note.

---

## Formatting Rules

- Header row: bold, dark blue background (#1A2E5A), white text
- Tab 1 header accent: {{COMPANY_NAME}} blue (#0057B8)
- Tab 2 header accent: teal (#007C7C) to visually distinguish country-specific rows
- Row height: auto (wrap text enabled)
- Column widths:
  - Question: 45
  - Answer: 65
  - Knowledge Type: 25
  - Owner: 18
  - Country: 18
  - Source: 28
  - Review Status: 18
  - Conflict Flag: 18
  - Notes: 55
  - Date Extracted: 16
  - Onspring Ready: 16
- Freeze top row on both tabs
- Conflict rows (Conflict Flag != blank): light yellow fill (#FFFACD) for easy visual scanning
- needs_review rows: light orange fill (#FFF0D9)

---

## Onspring Compatibility Notes

When the operations team is ready to upload from Excel to Onspring:

- The `Question` column maps to the Onspring "Task Name" or fact title field
- The `Answer` column maps to the primary response body
- The `Owner` column maps to the Onspring owner/assignee field
- The `Country` column maps to the geography tag
- `Knowledge Type` maps to the category field
- `Onspring Ready = TRUE` is the filter criterion for the upload batch
- `Review Status` and `Conflict Flag` are internal workflow fields — they may not have direct Onspring equivalents in v1

This workbook is designed so that an ops team member can filter `Onspring Ready = TRUE` and paste/import the matching rows without additional transformation.

## Inputs

- Extracted knowledge rows: `Question` (neutral, reusable), `Answer` (source-grounded, 1–4 sentences, qualifiers), `Knowledge Type` ({{COMPANY_NAME}} General vs Country-Specific), `Owner` (Product/HRSD/Finance/VGM/Implementation/Other), `Country` (country-specific rows only), `Source` (document or ticket name)
- The existing KB for match checks → drives Review Status (`new` / `confirmed` / `needs_review`) and Conflict Flag (blank / `enrichment` / `conflict` / `scope_reduction`)
- File name: `{{COMPANY_FILE}}` — human reviewer approval flips `Onspring Ready` to `TRUE`

## Outputs

- A formatted two-tab Excel workbook: Tab 1 {{COMPANY_NAME}} Knowledge (General rows), Tab 2 Country-Specific Knowledge · 11-column schema with the specified widths · header row bold, dark blue (#1A2E5A), white text; tab accents {{COMPANY_NAME}} blue (#0057B8) / teal (#007C7C); frozen top rows; wrap text; conflict rows light yellow, `needs_review` rows light orange
- Conflict Notes auto-populated in the prescribed format (conflict type, existing answer + source, new answer + source, reason, recommended reviewer)
- Onspring upload mapping: Question → task name, Answer → response body, Owner → assignee, Country → geography tag; upload batch = rows with `Onspring Ready = TRUE`
- Format: Excel workbook — ops pastes/imports the filtered batch with no additional transformation

## Example

New fact: ‘What is the parental leave policy?’ / source-grounded answer (1–4 sentences, qualifiers included), Owner=HRSD, Review Status=`new`, Onspring Ready=`FALSE` → row lands in Tab 1 ({{COMPANY_NAME}} General Knowledge), unhighlighted. A contradicting update arrives → Conflict Flag=`conflict`, Notes auto-populated (‘EXISTING KB ANSWER’ vs ‘NEW PROPOSED ANSWER’ + reason + RECOMMENDED REVIEWER), row highlighted yellow (#FFFACD). Ops filters `Onspring Ready = TRUE` and imports the batch into Onspring without transformation.

## Errors & edge cases

- **Ambiguous classification, uncertain owner, conditional answer, or weak source** → Review Status `needs_review` — requires human judgment before acceptance (light orange fill).
- **New fact contradicts an existing KB fact** → Conflict Flag `conflict` — Notes auto-populated with existing vs new answer, sources, reason, and recommended reviewer (light yellow fill).
- **New fact narrows an existing fact's scope** (e.g. General → Country-Specific) → `scope_reduction`; adds detail without contradicting → `enrichment`.
- **No matching fact in the existing KB** → `new` — proposed for first-time addition; `Onspring Ready` stays `FALSE` until a human reviews and approves.
