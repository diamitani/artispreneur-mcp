---
name: architecture-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to scaffold a fully local hubspot-import-formatter project: a five-stage engine (map -> normalize -> dedup -> validate -> write) that turns messy rep spreadsheets into import-ready workbooks, with hubspot_props.py as the single source of truth, semantic industry->NAICS resolution, optional direct upload with static lists, and a KPI ledger - no servers, no data leaves the machine. Use when formatting spreadsheets for HubSpot import."
---

# Architecture — HubSpot Import Formatter

A lightweight, fully local skill. No servers, no API keys, no data leaves the machine.
Everything runs as Python over the files the rep already has.

## What the skill sets up

When invoked, the skill scaffolds a `hubspot-import-formatter/` project
directory **in the user's workspace** (these are generated outputs, not
files bundled with this skill):

```
hubspot-import-formatter/
├── SKILL.md                    # Trigger + workflow instructions
├── README.md                   # Human guide for collaborators & end users
├── ARCHITECTURE.md             # System architecture
├── EXEC_OVERVIEW.md            # ELT / leadership one-pager
├── scripts/
│   ├── format_import.py        # The engine: map → normalize → dedup → validate → write
│   ├── hubspot_upload.py       # Optional: upsert to HubSpot + build a static list
│   ├── hubspot_props.py        # Shared template→internal map + enum validation (1 source)
│   ├── industry_resolver.py    # Semantic free-text industry → valid HubSpot value + NAICS
│   ├── refresh_hubspot_props.py# Refresh the live dropdown-option snapshot
│   └── kpi_report.py           # Reads the run ledger, prints adoption/volume KPIs
└── references/
    ├── templates.md            # Canonical template specs + alias/normalization rules
    ├── hubspot_upload.md       # Property map, dedupe strategy, token scopes
    ├── hubspot_lists.md        # Static vs active lists + filterBranch format
    ├── list_questionnaire.md   # Exact list-creation question flow + answer→flag mapping
    ├── hubspot_properties.json # Live snapshot: valid props + dropdown options
    ├── industry_mapping.md     # Semantic industry resolver docs
    └── industry_mapping.json   # 184 HubSpot industries → NAICS + synonyms (from Make.com)
```

The skill writes these files from the specifications below (the engine's
five stages, the design decisions, and the KPI layer). Nothing is
pre-built — the value is the documented pipeline, which the skill
implements fresh for each user's portal.

In the generated project, `hubspot_props.py` is the single source of truth
both the formatter and uploader import,
so they can never disagree on property names or valid values — that's what guarantees
no mis-mapping errors on import. `industry_resolver.py` layers semantic industry matching
on top of it.

Secrets live **outside** this folder at `~/.{{COMPANY_NAME}}/hubspot.env` (git-ignored) so a packaged
skill never ships a token.

## Data flow

```mermaid
flowchart TD
    A[Rep has a messy spreadsheet<br/>CSV / XLSX / multi-sheet] --> B[format_import.py]
    B --> C{Detect per sheet}
    C -->|person fields| D[Contacts pipeline]
    C -->|company identity| E[Companies pipeline]

    subgraph PIPE[For each object type]
      F[Map source cols → template fields<br/>exact-normalized, then substring]
      G[Normalize<br/>lowercase email · clean domain · derive domain from email]
      H[Dedup by unique ID<br/>Email / Company Domain Name]
      I[Validate required fields → Issues flag]
    end
    D --> PIPE
    E --> PIPE

    PIPE --> J[Exact-template sheet + CSV<br/>pristine, import-ready]
    PIPE --> K[Extended sheet<br/>+ leftover cols + Issues, flagged rows highlighted]
    PIPE --> L[Append run to KPI ledger<br/>~/.{{COMPANY_NAME}}/hubspot_import_ledger.csv]

    J --> M[HubSpot import wizard<br/>imported under Batch ID name]
    J --> U[hubspot_upload.py<br/>optional direct push]
    L --> N[kpi_report.py<br/>adoption & volume KPIs]
    M -.deal attribution via Batch ID.-> N
    U --> H1[Upsert: contacts by email,<br/>companies by domain]
    H1 --> H2[Create static list per type<br/>+ add members]
    H2 --> H3[Return list link]
```

### Upload path (generated `hubspot_upload.py`)

Optional. Reads the formatted workbook, sends only properties that exist in the portal,
validates enum/numeric fields, then writes via the dedupe-correct path per object:
**contacts upsert by email** (email is a HubSpot-unique property); **companies
search-then-update/create by domain** (domain usually isn't flagged unique, so direct
upsert is rejected). It then creates a static MANUAL list per type, adds the records, and
returns the link. Batches of 100 with per-record fallback so one bad row can't fail the
import. Token comes from `~/.{{COMPANY_NAME}}/hubspot.env`; uploads run as the token owner.

## Design decisions (and why)

| Decision | Choice | Why |
|---|---|---|
| Object detection | **Auto-detect & split** | One Sales Nav/Apollo export usually = people *and* their companies. Splitting produces both clean imports from one file, deduped independently. |
| Bad rows | **Keep but flag** | Reps must *see* what's missing, not have rows vanish. Flags live only on the Extended tab so the import tab/CSV stay pristine. |
| Owner field | **Map if present, else blank** | Never invent CRM ownership; let HubSpot assign on import if no source column exists. |
| Unique identifiers | Email (contacts) / Company Domain Name (companies) | Exactly what HubSpot dedupes on — the root cause of the duplicate problem this solves. |
| Logic location | **One bundled script, not ad-hoc per run** | Consistency is the entire point. A script guarantees every rep's output is byte-identical in structure. |

## The engine, in five stages (generated `format_import.py`)

1. **Load** — reads CSV or every sheet of an XLSX as strings (no silent type coercion).
2. **Detect** — per sheet, decides contacts / companies / both from which fields match.
3. **Map** — normalizes headers (lowercase, strip non-alphanumerics), matches against
   alias lists; exact match first, then substring; each source column used once.
4. **Normalize & dedup** — lowercases emails, strips URLs to bare domains, derives a
   company domain from a work email when no website column exists (free-mail ignored),
   drops duplicate unique IDs keeping the first.
5. **Validate & write** — flags rows missing required fields, writes the workbook
   (exact + extended tabs with template header styling) and the CSV(s), then appends one
   row to the KPI ledger.

## KPI layer

- **Local ledger** (`~/.{{COMPANY_NAME}}/hubspot_import_ledger.csv`, override via `{{COMPANY_PREFIX}}_IMPORT_LEDGER`):
  append-only, one row per run — batch ID, timestamp, operator, counts, flagged counts.
- The generated **`kpi_report.py`** aggregates it: total imports, rows prepared, data-quality rate,
  breakdown by operator and month.
- **Deal attribution** is intentionally *not* computed here (the script can't see the
  CRM). Each run emits a **Batch ID** meant to be used as the HubSpot import name;
  HubSpot/the GTM agent then reports deals traced to those import batches.

## Dependencies

Python 3 with `pandas` and `openpyxl` (standard in most data-tooling
environments). `xlrd` is used only for legacy `.xls`. No network calls.

## Extending it

Templates or aliases change? Edit the constants at the top of the generated
`format_import.py` (`CONTACT_TEMPLATE`, `COMPANY_TEMPLATE`, `*_REQUIRED`,
`*_ALIASES`) and mirror the change in the generated `references/templates.md`.
Adding a new object type = add a template/required/alias set and a detection rule.

## Inputs
- `spreadsheet` (file: CSV / XLSX, multi-sheet ok, required) - the messy rep data
- `template` (enum: contacts / companies, auto-detected per sheet) - target HubSpot object
- `portal_snapshot` (file) - hubspot_properties.json with valid props + dropdown options
- `upload` (boolean, default: false) - also run hubspot_upload.py for direct push

## Outputs
- hubspot-import-formatter/ project: SKILL.md, README, ARCHITECTURE.md, scripts (format_import.py, hubspot_upload.py, hubspot_props.py, industry_resolver.py, kpi_report.py), references/
- Exact-template workbook + CSV (pristine, import-ready) and an extended sheet with flagged rows highlighted
- Run appended to the KPI ledger; kpi_report.py prints adoption/volume KPIs

## Example
Input: a 2-sheet XLSX (contacts + companies) from a rep's trade-show list.
1. Detect per sheet: person fields -> Contacts pipeline; company identity -> Companies pipeline.
2. Map source columns -> template fields; normalize (lowercase email, clean domain); dedup by email/domain.
3. Industry free text "SaaS" -> semantic resolver -> valid HubSpot industry + NAICS.
4. Output: pristine import workbook + flagged extended sheet; ledger appended. Upload only if the user opts in.

## Errors & edge cases
- Required-field validation failures: rows get the Issues flag and highlighting - never silently dropped or invented.
- Ambiguous column mapping (exact-normalized then substring): surface the mapping for confirmation before writing.
- Token scope wrong on upload: hubspot_upload.md documents required scopes; secrets live at ~/.{{COMPANY_NAME}}/hubspot.env, never in the project folder.
- Template drift: refresh via refresh_hubspot_props.py against the live dropdown snapshot.
