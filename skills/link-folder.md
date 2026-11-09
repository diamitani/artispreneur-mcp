---
name: link-folder
description: "Maintains a structured, searchable link repository — accepts URLs with metadata (title, category, tags, notes), normalizes categories on first use, dedupes against URL variations, and exports filtered sets to CSV, JSON, or spreadsheet. Use when adding web links to a running database or spreadsheet."
---

# Link Folder

## Overview
Adds web links to a running database or spreadsheet. Organizes and categorizes URLs for research and reference. Maintains a structured, searchable link repository for ongoing projects.

## When to Use
- Collecting research links during a project or investigation
- Building a reference library organized by topic or category
- Saving and tagging articles, tools, or resources for later review
- Maintaining a shared link database for a team
- Exporting categorized links to CSV, JSON, or spreadsheet format

## How It Works
Accepts URLs along with metadata (title, category, tags, notes). Organizes them into a structured format — typically a CSV file or spreadsheet-compatible output. Supports categorization, tagging, and duplicate detection.

## Steps
1. Accept one or more URLs from the user
2. For each URL, capture or infer: title, source domain, category, tags, brief description
3. Check for duplicates against existing entries
4. Append to the running database file (CSV or spreadsheet)
5. Confirm addition and display current category counts
6. On request: export, filter by category/tag, or generate a summary

## Common Pitfalls
- Adding dead or inaccessible links without verification
- Using inconsistent categories or tags — normalize on first use
- Duplicate entries due to URL variations (trailing slashes, www vs non-www)
- Not backing up the link database periodically
- Forgetting to capture the date added, making it hard to identify stale links

## Inputs

- `urls` (one or more, required) — links to file
- Per-URL metadata: `title`, `source_domain`, `category`, `tags[]`, `description` — captured or inferred per link; `date_added` recorded automatically
- `database_file` (the running CSV/spreadsheet) — checked for duplicates before appending

## Outputs

- The running link database (CSV or spreadsheet) with normalized categories/tags and duplicate-free entries
- Confirmation per add + current category counts
- On request: filter by category/tag, a summary of the collection, or an export to CSV, JSON, or spreadsheet format

## Example

Add five AI-music articles → each captured with title, source domain, category `research/ai-music`, tags, and a one-line description; ‘AI Music’ vs ‘ai-music’ normalized on first use; one trailing-slash duplicate of an existing entry caught and skipped; appended to the running CSV; confirmation: ‘5 added · research/ai-music now holds 23 links.’ Later: ‘export everything tagged tutorial as JSON.’
