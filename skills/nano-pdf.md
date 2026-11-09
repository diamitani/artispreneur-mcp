---
name: nano-pdf
description: "Edits PDF text via natural-language instructions — point it at a page and describe the change (`nano-pdf edit deck.pdf 1 'Change the title to 'Q3 Results''`); ideal for typos, titles, dates, and small content fixes, not complex layout surgery. Use when you need to edit PDF text/typos/titles via nano-pdf CLI."
---

# nano-pdf

Edit PDFs using natural-language instructions. Point it at a page and describe what to change.

## Prerequisites

```bash
# Install with uv (recommended — already available in Hermes)
uv pip install nano-pdf

# Or with pip
pip install nano-pdf
```

## Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## Examples

```bash
# Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"

# Update a date on a specific page
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"

# Fix content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

## Notes

- Page numbers may be 0-based or 1-based depending on version — if the edit hits the wrong page, retry with ±1
- Always verify the output PDF after editing (use `read_file` to check file size, or open it)
- The tool uses an LLM under the hood — requires an API key (check `nano-pdf --help` for config)
- Works well for text changes; complex layout modifications may need a different approach

## Inputs

- `file.pdf` (required) + `page_number` (required — 0- or 1-based depending on version) + `"instruction"` (required, natural language): `nano-pdf edit <file.pdf> <page_number> "<instruction>"`
- Install: `uv pip install nano-pdf` (recommended — uv already available in Hermes) or `pip install nano-pdf`
- An LLM API key (see `nano-pdf --help` for config)

## Outputs

- The edited PDF, written in place/by the tool — verified after editing (file size check or visual open)
- Format: PDF with the requested text change applied; best for titles, typos, dates, and small content fixes

## Errors & edge cases

- **Page numbers may be 0-based or 1-based** depending on version — if the edit hits the wrong page, retry with ±1.
- **Always verify the output PDF** after editing (check file size via `read_file`, or open it) — don't assume the edit landed.
- **Complex layout modifications** may need a different approach — this tool is for text changes.
- **Requires an API key** (it uses an LLM under the hood) — check `nano-pdf --help` for config.
