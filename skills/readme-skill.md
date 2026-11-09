---
name: readme-skill
description: "Turns any messy contact/company spreadsheet into the official HubSpot import files -- template-matched XLSX plus CSVs, dedupe-safe upserts by Email/Domain, NAICS industry mapping, and a local KPI ledger; optional direct upload to HubSpot with batch-ID attribution. Use when formatting a contact or company list for HubSpot import."
---

# HubSpot Import Formatter

Turn **any** spreadsheet of contacts or companies into {{COMPANY_NAME}}'s official HubSpot import
files — automatically. No more hand-mapping columns, re-saving as CSV, or accidentally
creating duplicate records.

> **The problem this fixes:** HubSpot filled up with duplicate Contacts and Companies
> because everyone imported files in their own format. This standardizes every import to
> the two official templates so HubSpot can dedupe properly.

---

## What you get back

Hand it one messy file, get back:

| File | What it is |
|---|---|
| `<name>_HubSpot_Import.xlsx` | A workbook with a clean **Contacts** and/or **Companies** tab (exactly the template), plus an **Extended** tab showing everything + a flag on incomplete rows. |
| `<name>_Contacts_HubSpot.csv` | The contacts template as a CSV — drop straight into HubSpot. |
| `<name>_Companies_HubSpot.csv` | The companies template as a CSV — drop straight into HubSpot. |

You only get the file types that are actually in your data (contacts, companies, or both).

---

## How to use it (end users)

You don't need to touch the command line. Just ask Claude:

- *"Format this list for HubSpot"* (with your file attached or its path)
- *"Prep this Apollo export for import"*
- *"Clean up this contact list and dedupe it before I upload"*
- *"Get this ready to upload to HubSpot"*

Claude runs the skill and hands back the files above, plus a plain-English summary:
how many contacts/companies, how many rows need attention, and which columns it mapped.

### Then in HubSpot
1. Go to **Contacts → Import** (or **Companies → Import**) → **Start an import** → file.
2. Upload the CSV (or the matching tab of the XLSX).
3. **Map your Email column to the `Email` property** — this is the #1 cause of mis-imports.
4. **Name the import using the Batch ID** the skill gives you (e.g. `{{COMPANY_NAME}}-IMP-20260614-...`).
   This is what lets us later see which deals came from which import.

---

## The rules it enforces

- **Required fields** (can't be blank):
  - Contacts → `Email`, `First Name`, `Last Name`
  - Companies → `Company Name`, `Company Domain Name`
- **Unique identifiers** (how HubSpot dedupes): `Email` for contacts, `Company Domain
  Name` for companies.
- **Nothing is dropped.** Rows missing a required field still appear, but they're
  highlighted on the *Extended* tab with a reason in the `Issues` column. Fix them and
  re-run, or import as-is knowing those rows won't match cleanly. Columns the engine
  doesn't recognize are preserved verbatim on the *Extended* tab (never in the
  HubSpot-ready files), so no source data is silently lost.
- **It auto-splits.** A typical export has one row per *person* that also carries their
  *company's* info — you'll get both a contacts file and a deduped companies file.
- **Owners** are only filled if your file has an owner/rep column; otherwise left blank.
- **Industry is mapped semantically.** HubSpot's industry is a fixed dropdown, so messy
  values like "SaaS", "Fintech", or "Information Technology & Services" are auto-converted
  to the correct HubSpot industry (using {{COMPANY_NAME}}'s NAICS-based industry map), and each
  company is enriched with its **NAICS sector + code** (shown on the Extended tab). Values
  that can't be matched are kept and flagged so you can fix them.

---

## Running it directly (collaborators / power users)

```bash
# Basic
python3 scripts/format_import.py "/path/to/your_file.xlsx"

# Force a single object type
python3 scripts/format_import.py "list.csv" --only contacts

# Choose where outputs go, and tag who ran it (for KPIs)
python3 scripts/format_import.py "list.xlsx" --outdir ~/Desktop --operator "Jane Smith"

# Skip KPI logging
python3 scripts/format_import.py "list.csv" --no-log
```

Accepts CSV, XLSX, XLS, and multi-sheet workbooks.

---

## Optional: push straight to HubSpot + auto-build a list

Don't want to touch the import wizard at all? The skill can upload for you and hand back a
HubSpot **list** link:

> *"Format this and upload it to HubSpot, then send me the list link."*

What it does:
- **Contacts** are upserted by **Email**, **Companies** matched by **Domain** — so
  re-running never creates duplicates (it updates the existing record).
- **Enriches companies with NAICS** sector + code, and normalizes dropdowns (industry,
  lifecycle, country).
- **Asks you a short questionnaire** before building the list — name, description, static
  vs active, and (for active lists) the filter. The exact flow is documented in
  [`references/list_questionnaire.md`](references/list_questionnaire.md).
- Returns links like `https://app.hubspot.com/contacts/<portal>/objectLists/<id>`.

Run it directly:

```bash
python3 scripts/hubspot_upload.py "<name>_HubSpot_Import.xlsx" --batch-id {{COMPANY_NAME}}-IMP-...
python3 scripts/hubspot_upload.py "<file>" --dry-run        # validate, upload nothing
python3 scripts/hubspot_upload.py "<file>" --only contacts  # limit scope
```

**Credentials:** upload auth is the operator's own token — resolution order:
`HUBSPOT_PAT` env → `~/.atlas/hubspot.env`. The skill ships **no** bundled or
shared token (see `config/README.md`). To rotate, replace your own token;
nothing in the repo changes. Scopes: contacts/companies read+write, lists
read+write. **All uploads run as the token owner's user.** See
`references/hubspot_upload.md` for the full property map and details.

When HubSpot's dropdown options change (new lifecycle stage, lead status, industry),
refresh the validation snapshot: `scripts/refresh_hubspot_props.py`.

> ⚠️ This writes to production HubSpot. The skill will confirm before uploading.

## KPIs — measuring adoption & impact

Every run logs one row to a local ledger (`~/.{{COMPANY_NAME}}/hubspot_import_ledger.csv`). See the
running totals any time:

```bash
python3 scripts/kpi_report.py          # human-readable
python3 scripts/kpi_report.py --json   # machine-readable
```

You'll see: imports run, total contacts & companies prepared, data-quality (clean) rate,
and a breakdown by operator and month.

### "How many deals came through these imports?"
That answer lives in **HubSpot**, not in this tool. The mechanism:
1. Each run prints a **Batch ID**. Reps use it as the HubSpot **import name**.
2. In HubSpot, build a **Deals report** filtered to deals whose associated contact/company
   came from those import batches (HubSpot tracks the import each record came from).
3. The {{COMPANY_NAME}} GTM agent can pull this automatically via the HubSpot connection — ask it:
   *"How many deals trace back to imports tagged {{COMPANY_NAME}}-IMP-* this quarter?"*

This keeps the loop closed: volume + quality from the ledger, revenue impact from HubSpot.

---

## Requirements

Python 3 with `pandas` and `openpyxl`. Formatting runs locally — no data
leaves your machine, no credentials required. Uploading to HubSpot requires
your own `HUBSPOT_PAT` (see `config/README.md`); the skill bundles no token.

## Files

- `SKILL.md` — how Claude uses this.
- `scripts/format_import.py` — the engine (messy spreadsheet → HubSpot files).
- `scripts/hubspot_upload.py` — opt-in uploader (dry-run default, `--live` to write).
- `scripts/kpi_report.py` — KPI reporting from the local ledger.
- `scripts/refresh_hubspot_props.py` — refresh the HubSpot dropdown snapshot.
- `references/templates.md` — exact template specs & matching rules.
- `references/hubspot_upload.md` — upload property map & details.
- `references/list_questionnaire.md` — the short questionnaire before list builds.
- `config/README.md` — credential resolution (no token ships with the skill).
- `ARCHITECTURE.md` — how it's built.
- `EXEC_OVERVIEW.md` — the leadership one-pager.

## Questions / file reviews

Reach out to the GTM team ({{USER_NAME}}) or Sales Coordination (Rocco Orazio
Paradiso) before importing if you want a file double-checked.

## Inputs

- `file` (path) -- CSV, XLSX, XLS, or multi-sheet workbook of contacts/companies
- CLI flags -- `--only contacts|companies`, `--outdir`, `--operator "Name"` (for KPIs), `--no-log`
- For direct upload: the operator's own `HUBSPOT_PAT` (resolution order: `HUBSPOT_PAT` env -> `~/.atlas/hubspot.env`; scopes: contacts/companies read+write, lists read+write) and `--batch-id` (e.g. IMP-YYYYMMDD-...); `--dry-run` validates without writing

## Outputs

- `<name>_HubSpot_Import.xlsx` -- clean Contacts and/or Companies tabs matching the official template, plus an Extended tab flagging incomplete rows with reasons in the Issues column
- `<name>_Contacts_HubSpot.csv` and `<name>_Companies_HubSpot.csv` -- drop straight into HubSpot's import wizard
- A plain-English summary: how many contacts/companies, how many rows need attention, which columns were mapped; every run logs one row to the local KPI ledger (`~/.<company>/hubspot_import_ledger.csv`)

## Example

"Prep this Apollo export for import": the engine maps columns to the official templates, auto-splits person-rows into a deduped companies file (matched by Company Domain Name), converts messy industries ("SaaS", "Fintech") to HubSpot's fixed dropdown values with NAICS sector + code, flags 12 rows missing Email on the Extended tab, and reports "340 contacts, 210 companies, 12 rows need attention".

## Errors & edge cases

- **Rows missing required fields** (Contacts: Email, First Name, Last Name; Companies: Company Name, Company Domain Name) -- never dropped; highlighted on the Extended tab with a reason so you can fix and re-run, or import as-is knowing they won't match cleanly.
- **Unrecognized columns** -- preserved verbatim on the Extended tab, never in the HubSpot-ready files; no source data is silently lost.
- **The #1 mis-import cause** -- map your Email column to HubSpot's `Email` property at import time, and name the import with the Batch ID the skill prints.
- **Uploads write to production HubSpot** -- the skill confirms before uploading; the skill ships no bundled token, and all uploads run as the token owner's user.
