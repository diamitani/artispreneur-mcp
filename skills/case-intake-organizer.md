---
name: case-intake-organizer
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to turn a chaotic pile of case inputs into a chronologically perfect case file before any research or drafting: classify each input into six mirrored subdirectories (correspondence, filings, evidence, case-law research, deadlines, notes), rename to YYYY-MM-DD_Source_Brief-Description, maintain a verified manifest and a fact sheet with a quarantined PRIVATE counsel-only section, and extract deadlines to the deadline-tracker. Use when organizing legal case intake documents."
---

# Case Intake Organizer

Turn a chaotic pile of inputs into a chronologically perfect case file. Intake runs *before* research and drafting — a draft that cites "the July memo" instead of a filed document is sloppiness, and Lex is allergic to sloppiness.

## The six subdirectories (mirror in Drive and in the portal)

```
<Case Name> — <State> (<Year>)/
├── 01 Correspondence/         # insurer/agent/counsel letters, BOTH directions
├── 02 Filings and Complaints/ # regulator complaints, court filings (drafts marked DO-NOT-FILE)
├── 03 Evidence and Documents/ # dec pages, notices, memos, bills, photos, reports
├── 04 Case Law Research/      # memos from case-law-research + INDEX.md
├── 05 Deadlines/              # DEADLINES.md ledger
└── 06 Notes/                  # intake memos (PRIVATE), trackers, strategy notes
```

## Step 1 — Classify each input

For each raw input, decide its subdirectory:

| Input type | Goes to |
|---|---|
| Letter/email to or from insurer, agent, counsel, regulator | 01 Correspondence |
| Complaint filed (or draft), court filing, appeal letter | 02 Filings and Complaints |
| Policy docs, notices, bills, memos, photos, police reports, IDs | 03 Evidence and Documents |
| Opinion memos, research notes | 04 Case Law Research |
| Anything stating a date something must happen by | 05 Deadlines (+ also file the doc itself where it belongs) |
| Intake memos, trackers, internal strategy, meeting notes | 06 Notes |

When an input fits two places (a notice with a deadline), file the document in its primary home and log the deadline separately.

## Step 2 — Rename

Convention: `YYYY-MM-DD_Source_Brief-Description.ext`

- Date = the document's own date (mailing date, email date, memo date) — not the day you received it.
- Source = who made it (`Progressive`, `Diamitani`, `IID`, `Youkhana`, `Police`, `ComEd`…).
- Description = 2–5 words, hyphens, no spaces: `Cancellation-Notice`, `Final-Bill`, `Coverage-Denial`.
- Drafts get a suffix: `_DRAFT-DO-NOT-FILE`.

Examples:
- `2026-06-23_Progressive_Cancellation-Notice.pdf`
- `2026-09-11_Diamitani_Supplemental-Reconsideration.pdf`
- `2026-09-13_IID-Complaint_DRAFT-DO-NOT-FILE.docx`

## Step 3 — Manifest

Maintain `<Case>/MANIFEST.md` (or a manifest section per subdirectory). One row per document:

```markdown
| # | File | Date | From → To | Type | Summary (1 line) | Verified |
|---|------|------|-----------|------|------------------|----------|
| 1 | 2026-05-13_Progressive_Policy-Declarations.pdf | 2026-05-13 | Progressive → Diamitani | Dec page | Policy 874096430, 2020 BMW X5, $… premium | ✅ read |
```

"Verified" means someone actually opened it and confirmed the contents match the name — never mark verified on a file you haven't read.

## Step 4 — Fact sheet

Maintain `<Case>/FACT-SHEET.md`, updated on every intake:

```markdown
# Fact Sheet — <Case Name>
**Parties:** …
**Policy / claim / account numbers:** …
**Key dates (chronological):** …
**Amounts in dispute:** …
**Current posture:** (e.g., "reconsideration sent 2026-09-11; awaiting response; IID complaint drafted, not filed")
**Open deadlines:** (mirror of DEADLINES.md)
**Authorities:** (citations + one-line verdicts from case-law-research)
**PRIVATE — counsel only:** (facts that must never enter outbound drafts without explicit authorization)
```

The PRIVATE section exists so sensitive facts are *recorded* (memory is worse) but *quarantined*.

## Step 5 — Extract deadlines

Any date that is a "by" date, an effective date, a response window, or a statute-driven cutoff goes to `deadline-tracker` with its source document cited. Intake doesn't just file paper — it surfaces tripwires.

## Guardrails

- Never rename the only copy. Copy → verify → then (optionally) remove the original.
- Never guess a document's date from a filename — read the document.
- Duplicates: keep one canonical copy; note the duplicate's location in the manifest row.
- Counsel-only inputs (admissions, ID numbers, DOBs) get filed in 06 Notes with PRIVATE in the filename or Drive description — never in 01–03 where they could ride along into a filing.

## Inputs
- `case_name` (string, required), `state` (string), `year` (integer)
- `inputs` (list of files, required) - the raw pile: letters, filings, notices, photos, IDs, memos
- `dest` (string) - Drive folder and portal mirror target

## Outputs
- Six-subdirectory case tree with renamed, classified documents
- MANIFEST.md: one row per document with a Verified column (never verified unread)
- FACT-SHEET.md: parties, numbers, key dates, amounts, posture, deadlines, authorities, PRIVATE section
- Deadlines extracted to the deadline-tracker with source documents cited

## Example
Input: 8 files for the Progressive policy dispute (cancellation notice, final bill, denial letter, crash report).
1. Classify: notice -> 03 Evidence; bill -> 03; denial -> 01 Correspondence; crash report -> 03.
2. Rename: `2026-06-23_Progressive_Cancellation-Notice.pdf`, etc.
3. Manifest rows with Verified once opened; fact sheet updated; the Aug-3 deadline logged to the tracker.
4. Counsel-only facts (garaging admission, ID numbers) filed in 06 Notes with PRIVATE in the filename.

## Errors & edge cases
- Never rename the only copy: copy -> verify -> then optionally remove the original.
- Document's date: read it from the document itself, never guess from the filename.
- Input fits two places (a notice with a deadline): file in the primary home, log the deadline separately.
- Duplicates: keep one canonical copy; note the duplicate's location in the manifest row.
