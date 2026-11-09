---
name: industry-mapping-skill
description: "Resolves messy free-text industry labels to valid HubSpot dropdown values through a 4-rung resolution ladder (exact → synonym → fuzzy → NAICS-sector default), enriching each company with NAICS sector + 2-digit code and returning 'unresolved' rather than guessing against the live portal. Use when working with semantic industry mapping."
---

# Semantic Industry Mapping — Reference

Source spreadsheets carry industry in countless forms ("Software", "SaaS", "Fintech",
"Computer Software", a NAICS sector, or already-valid HubSpot codes). HubSpot's `industry`
is a fixed dropdown, so anything that doesn't match exactly used to be dropped. The
resolver (`scripts/industry_resolver.py`) maps free text to a **valid HubSpot industry
value** and enriches each company with its **NAICS sector + 2-digit code**.

## Data source

`references/industry_mapping.json` holds three tables (59 HubSpot industries across
the NAICS sectors, plus 27 curated synonyms — an example mapping; if you have your
own Industry Mapping workbook, regenerate or extend the JSON from it):

- `hubspot_to_naics` — each HubSpot industry → `{naics, sector}` (used for enrichment).
- `sector_defaults` — a default HubSpot industry per NAICS sector (broad-input fallback).
- `synonyms` — curated GTM / data-provider terms → HubSpot industry (Software→
  COMPUTER_SOFTWARE, Fintech→FINANCIAL_SERVICES, etc.).

## Resolution ladder (first confident hit wins)

1. **exact** — already a HubSpot option (validated against the live portal snapshot in
   `hubspot_properties.json`).
2. **synonym** — a curated term match.
3. **fuzzy** — close string match against the canonical 184-industry list (cutoff 0.86;
   handles "Information Technology & Services" → `INFORMATION_TECHNOLOGY_AND_SERVICES`).
4. **sector / naics-code** — input names a NAICS sector label or a 2-digit code → that
   sector's default industry.

Every candidate is then checked against the **live portal options**. If it isn't a real
option there (exact or whitespace/punctuation-only difference), the resolver tries the
NAICS-sector default; if that also isn't a portal option, it returns **unresolved** rather
than guessing — no loose fuzzy guessing against the portal (that once mislabeled
"Manufacturing" as a junk option).

## Where it's applied

- **Formatter** (the external import formatter, companies only): rewrites the `Industry`
  column to the resolved HubSpot value, preserves the original in `Industry (source)`,
  and adds `NAICS Sector` + `NAICS Code` columns — all on the **extended tab** only (the
  exact template stays the 9 official columns). Unresolved values are kept as-is and
  flagged in `Issues` with their NAICS sector as a hint.
- **Uploader** (the companion uploader script in hubspot-upload-skill): resolves
  `industry` before sending; unmappable values are dropped so they can't error the
  batch (the company still uploads).

## Known portal gap

The example snapshot has **no generic "Manufacturing" option** — only specific types.
A bare "Manufacturing" input therefore falls through the ladder to the sector default
(in the bundled example map, the Manufacturing sector's default). If you want a
dedicated "Manufacturing" option, add it in HubSpot (Settings → Properties → industry),
then refresh the snapshot — it will resolve automatically afterward.

## Maintenance

- Refresh the **portal option snapshot** when HubSpot dropdowns change by running
  the bundled refresh script (`scripts/refresh_hubspot_props.py`).
- Regenerate the **industry map** if your source workbook changes: rebuild
  `references/industry_mapping.json` from it, or edit the JSON directly. Add new GTM
  synonyms to the `synonyms` table — they take effect immediately.

## Test it

```bash
python3 scripts/industry_resolver.py "SaaS" "Fintech" "oil & gas" "Manufacturing" "54"
```

## Inputs

- `industry_text` (string, required) — free-text industry label(s): `"SaaS"`, `"oil & gas"`, `"54"`, a NAICS sector, or an already-valid HubSpot code
- `references/industry_mapping.json` (reference file, default: bundled example with 59 HubSpot industries, 27 curated synonyms, sector defaults)
- `hubspot_properties.json` (live portal snapshot) — every candidate is validated against real portal options
- CLI: `python3 scripts/industry_resolver.py "SaaS" "Fintech" "oil & gas" "Manufacturing" "54"`

## Outputs

- Resolved HubSpot industry value per company + NAICS sector + 2-digit code
- Formatter: rewrites the `Industry` column, preserves the original in `Industry (source)`, adds `NAICS Sector` + `NAICS Code` columns — extended tab only (official 9-column template untouched); unresolved values kept as-is and flagged in `Issues` with their NAICS sector as a hint
- Uploader: resolves `industry` before sending; unmappable values are dropped so they can't error the batch (the company still uploads)

## Example

`python3 scripts/industry_resolver.py "SaaS" "Fintech" "oil & gas" "Manufacturing" "54"` → `SaaS`→`COMPUTER_SOFTWARE` (synonym), `Fintech`→`FINANCIAL_SERVICES` (synonym), `"54"`→ that NAICS sector's default industry, `Manufacturing`→ **unresolved** (the example snapshot has no generic Manufacturing option) flagged in `Issues` with its sector as a hint rather than force-mapped to a junk option.

## Errors & edge cases

- **Unresolved values are never guessed.** The resolver returns `unresolved` instead of fuzzy-matching against the portal (a past loose match mislabeled `Manufacturing` as a junk option).
- **Known portal gap:** bare `Manufacturing` input falls through the ladder — add a dedicated option in HubSpot (Settings → Properties → industry), then refresh the snapshot and it resolves automatically.
- **Stale dropdown options:** refresh the portal snapshot with `scripts/refresh_hubspot_props.py` whenever HubSpot dropdowns change.
- **Custom workbook:** regenerate `references/industry_mapping.json` from your own Industry Mapping workbook (or edit the JSON directly); new GTM synonyms take effect immediately.
