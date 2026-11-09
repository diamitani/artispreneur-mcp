---
name: templates-skill
description: "The source of truth for the two official HubSpot import templates -- exact Contacts and Companies column specs (order, required flags, unique identifiers Email and Company Domain Name), header styling, column-matching and normalization rules; the format_import.py script encodes all of this. Use when working with hubspot import templates."
---

# HubSpot Import Templates — Reference

Source of truth for the two official templates. The script `scripts/format_import.py`
encodes all of this; edit both together if HubSpot's templates change.

## Header styling

| Type | Hex fill | Meaning |
|------|----------|---------|
| Required | `EE4266` (red) | Cannot be blank |
| Optional | `222B40` (dark navy) | Fill if available |

Font: bold, white, left-aligned. Row 1 frozen.

## Contacts template

Sheet name: `Contacts`. **Unique identifier: `Email`.**

| # | Column | Required |
|---|--------|----------|
| 1 | Email | ✅ |
| 2 | First Name | ✅ |
| 3 | Last Name | ✅ |
| 4 | Phone Number | |
| 5 | Mobile Phone Number | |
| 6 | Job Title | |
| 7 | Company Name | |
| 8 | Lead Status | |
| 9 | Lifecycle Stage | |
| 10 | Contact Owner | |
| 11 | Country/Region | |
| 12 | State/Region | |
| 13 | City | |
| 14 | LinkedIn URL | |

## Companies template

Sheet name: `Companies`. **Unique identifier: `Company Domain Name`.**

| # | Column | Required |
|---|--------|----------|
| 1 | Company Name | ✅ |
| 2 | Company Domain Name | ✅ |
| 3 | Industry | |
| 4 | Number of Employees | |
| 5 | City | |
| 6 | State/Region | |
| 7 | Country/Region | |
| 8 | LinkedIn Company Page | |
| 9 | Company Owner | |

## Column matching

Matching is done on a normalized header (lowercased, all non-alphanumerics removed):
1. **Exact normalized match** against an alias list (e.g. `e-mail`, `Email Address`,
   `work_email` all normalize toward `email`).
2. **Substring fallback** — alias contained in the header or vice versa, longest aliases
   first, each source column used at most once.

Key alias groups (see script for the full lists):
- **Email** ← email, e-mail, work email, contact email, mail
- **Company Domain Name** ← domain, website, url, web address, homepage, company domain
- **Number of Employees** ← employees, headcount, company size, # employees
- **Contact/Company Owner** ← owner, rep, AE, SDR, BDR, assigned to, account owner

## Normalization rules

- **Domain cleanup**: `https://www.Acme.com/about?x=1` → `acme.com`.
- **Domain from email**: when a company has no website column, derive the domain from a
  work email; free-mail providers (gmail.com, yahoo.com, etc.) are ignored.
- **Email**: trimmed + lowercased.
- **Dedup**: by the unique identifier, keeping the first occurrence; rows with a blank
  unique id are kept (and flagged as incomplete).

## Outputs

- `<stem>_HubSpot_Import.xlsx` — `Contacts`/`Companies` (exact) + `*_Extended` tabs.
- `<stem>_Contacts_HubSpot.csv`, `<stem>_Companies_HubSpot.csv` — exact template, CSV.

## Inputs

- `template` -- Contacts (14 columns, unique identifier: Email; required: Email, First Name, Last Name) or Companies (9 columns, unique identifier: Company Domain Name; required: Company Name, Company Domain Name)
- `source_headers` -- your spreadsheet's headers, matched on normalized form (lowercased, non-alphanumerics removed) against the alias list: exact normalized match first, then alias, then fuzzy

## Example

A spreadsheet with "e-mail", "FirstName", "Co. Website": normalized matching maps them to Email, First Name, Company Domain Name; the required-column check flags the missing Last Name before import.

## Errors & edge cases

- **Template drift** -- `scripts/format_import.py` encodes this entire reference; edit both together whenever HubSpot's templates change, or the script and the doc disagree.
- **Ambiguous header matches** -- substring fallback can misassign (longest aliases first, each source column used once); verify the mapping on the Extended tab when headers are unusual.
- **Free-mail domains** -- deriving Company Domain Name from a work email ignores gmail.com/yahoo.com/etc.; companies with only free-mail contacts keep a blank domain and get flagged incomplete.
- **Blank unique identifiers** -- rows with a blank Email / Company Domain Name are kept (not dropped) and flagged as incomplete; they won't dedupe.
- **Required-column styling** -- red (`EE4266`) = cannot be blank; if a required column is missing from your source, the import will fail HubSpot-side.
