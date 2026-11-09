---
name: list-manager
description: "Organizes categorized listings — apartments, inventory, classifieds, any structured data — into a searchable, filterable collection: parses CSV/JSON/free text/links, normalizes fields, enables full-text and attribute search with sorting and comparison, flags duplicates, stale entries, and outliers, then exports filtered results. Use when organizing and managing categorized listings with search tools."
---

# List Manager

## Overview
Organizes and manages categorized listings with search tools. Handles apartment listings, inventory, classifieds, and any structured data that needs sorting, filtering, and searching.

## When to Use
- Managing apartment or rental property listings
- Organizing inventory, product catalogs, or asset registers
- Sorting and filtering classified ads or job postings
- Building a searchable directory of items with multiple attributes
- Comparing listings across multiple dimensions (price, location, specs)

## How It Works
Accepts listings in various formats (CSV, JSON, free text, links). Structures them into a searchable, filterable collection. Supports sorting by any field, full-text search, and exports.

## Steps
1. Accept listing data: paste, upload, or fetch from URLs
2. Parse and structure: identify columns/fields, normalize values
3. Index for search: enable full-text and attribute-based filtering
4. Present interactive options: sort, filter, search, compare
5. Flag duplicates, stale entries, or outliers
6. Export filtered results in CSV, markdown table, or spreadsheet format

## Common Pitfalls
- Inconsistent field names across sources — normalize during import
- Large datasets causing slow search — use indexing and pagination
- Losing sort/filter state between sessions
- Not handling missing or null values gracefully
- Forgetting to timestamp entries for staleness detection

## Inputs

- `listing_data` (required) — CSV, JSON, free text, or URLs to fetch; columns/fields identified and normalized on import (inconsistent field names unified then)
- `search` / `filter` / `sort` criteria — full-text plus attribute-based filtering, sortable by any field
- `export_format` (on request) — CSV, markdown table, or spreadsheet

## Outputs

- A structured, searchable, filterable collection with full-text + attribute search, sorting by any field, and side-by-side comparison
- Flags: duplicates, stale entries (timestamped for staleness detection), outliers, missing/null values handled gracefully
- Filtered results exported as CSV, markdown table, or spreadsheet — sort/filter state explicit so it survives between sessions

## Example

Twelve apartment listings pasted as free text → parsed into fields (price, beds, location, pet policy), ‘2br’ normalized to ‘2 bed’ across sources; full-text search ‘dog-friendly under $1500’; sorted by price; two entries flagged stale (timestamped >30 days); top 5 exported as a markdown table for comparison.
