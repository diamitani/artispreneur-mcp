---
name: deadline-tracker
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to extract, ledger, and nag about legal case deadlines: one DEADLINES.md per case with Deadline / Days left / Source / Action required / If missed columns, extraction rules (notices, statutes, correspondence, personal hard dates), tickler discipline (weekly review, 7-day rule, resolved-not-deleted, conflict flags), and guardrails against invented deadlines and invented urgency. Use when tracking legal case deadlines."
---

# Deadline Tracker

Deadlines are the one thing in a legal case that doesn't negotiate. This skill extracts them, ledgers them, and nags about them.

## The ledger

One file per case: `<Case>/05 Deadlines/DEADLINES.md`.

```markdown
# Deadlines — <Case Name>

| # | Deadline | Days left | Source | Action required | If missed |
|---|----------|-----------|--------|-----------------|-----------|
| 1 | 2026-09-25 | 12 | Reconsideration sent 2026-09-11; 2-week follow-up | Follow up with Progressive if no response | Momentum loss; no legal penalty |
| 2 | ~2026-09-29 | 16 | Personal (DACA/EAD expiry) | Work authorization gap planning | Cannot work lawfully until renewed |
```

Fields:
- **Deadline** — the date. Prefix `~` when approximate; never present a guess as exact.
- **Days left** — computed from *today's* date at the time of writing. Recompute whenever the ledger is reviewed.
- **Source** — the document, statute, or rule that creates it, with citation to the manifest entry.
- **Action required** — the concrete next step, with an owner (Patrick, counsel, Lex-drafted).
- **If missed** — the honest consequence. "Nothing, legally" is a valid entry and better than invented urgency.

## Extraction rules

Pull deadlines from:
1. **Notices and letters** — "call us by August 3," "payment due," "you have 15 days to request a hearing." Quote the exact language in the ledger's source note.
2. **Statutes and rules** — appeal windows, statutes of limitation, regulatory response timelines (e.g., IID's 30–45 day complaint process). Cite the provision; mark "verify current law" when the date math matters.
3. **Correspondence Patrick sends** — a reconsideration letter creates its own follow-up deadline ("if no response in 2 weeks, escalate").
4. **Personal hard dates** — DACA/EAD expiry, move-out dates, court dates. They don't come from the case but they constrain it; keep them in the ledger with source "personal."

## Tickler discipline

- **Review cadence:** the ledger gets re-read and re-dated at least weekly while a case is active.
- **7-day rule:** any deadline inside 7 days gets flagged loudly, every time, until it's resolved or Patrick acknowledges it.
- **Resolved, not deleted:** when a deadline passes or is satisfied, move it to a "Closed" section with the outcome — the history of what was met is evidence of diligence.
- **Contradictory deadlines** (two documents, two dates) get a `⚠️ CONFLICT` flag and a note explaining the discrepancy — this is often case-winning material (see `insurance-coverage-playbook` §3.4).

## Guardrails

- Never invent a deadline. If a notice is ambiguous about whether a date is a deadline, quote the language and mark it `POSSIBLE — verify`.
- Countdown math uses the calendar date in Patrick's timezone (America/Chicago).
- The ledger is a planning tool, not legal advice about limitations periods — when a statute of limitations is in play, the entry says "CONFIRM WITH COUNSEL" in the action column.

## Inputs
- `case` (string, required) - case name; ledger lives at <Case>/05 Deadlines/DEADLINES.md
- `sources` (list) - notices, letters, statutes, correspondence, personal hard dates to mine

## Outputs
- DEADLINES.md ledger: one row per deadline with source, action required (with owner), and honest consequence if missed
- Closed section for resolved deadlines (moved, never deleted)
- Contradictory deadlines flagged with a conflict note explaining the discrepancy

## Example
Input: extract deadlines for the Progressive policy dispute.
1. Mine the reconsideration letter: "if no response in 2 weeks, escalate" -> follow-up deadline.
2. Statute: 2-year limitations window -> entry marked CONFIRM WITH COUNSEL.
3. Personal: EAD expiry -> source "personal", action "work authorization gap planning".
4. Days left computed from today in America/Chicago; the 7-day rule flags anything inside a week.

## Errors & edge cases
- Never invent a deadline: ambiguous language gets quoted and marked POSSIBLE - verify.
- "Nothing, legally" is a valid If-missed entry - better than invented urgency.
- Contradictory deadlines (two documents, two dates): flag CONFLICT with a discrepancy note - this is often case-winning material.
- Statute-of-limitations entries always carry CONFIRM WITH COUNSEL in the action column.
