---
name: entity-readiness-baseline-analyst
description: "LLM-agnostic workflow automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to analyze the Entity Readiness Change Report baseline from two read-only sources - a CSV exported from the n8n Data Tables UI or an execution URL/ID - reporting row counts, unique countries, ready/not-ready counts, readiness-status counts, and timestamp coverage, with ready defined as exactly 'Ready to Hire Locals' or 'Ready to Hire All' and every answer stating its source. Use when analyzing the entity_readiness_baseline table, ready-country totals, status changes, or baseline coverage (read-only)."
---

# Entity Readiness Baseline Analyst

Use this skill only for the [Your Company Name] Entity Readiness Change Report, read-only. It supports two reliable sources:

1. A CSV downloaded from the n8n Data Tables UI.
2. An execution URL or ID containing the workflow's Data Table and normalization outputs.

Project scope: workflow `EirKWJBySSXugv3a`, table `entity_readiness_baseline` (`DWg0YxdKbQcNcwtv`), source Onspring Report 954. Do not edit a Data Table, create a workflow, or use undocumented internal n8n routes. This Cloud instance currently does not expose Data Table rows through its public API.

## Analyze a CSV

```bash
python3 scripts/analyze_baseline.py --csv "/absolute/path/entity_readiness_baseline.csv"
```

The CSV should contain `country`, `ready`, and optionally `status` and `updated_at`. The script reports row count, unique countries, ready/not-ready counts, readiness-status counts, and timestamp coverage.

## Analyze the latest execution

```bash
export N8N_ENTITY_REPORT_API_KEY="..."
python3 scripts/analyze_baseline.py --execution "<execution URL or ID>"
```

It rejects executions from other workflows, then calls only `GET /api/v1/executions/{id}?includeData=true` and summarizes the normalized output, baseline/diff state, report subject, and storage output count.

## Answer questions

Translate the JSON into direct answers. State the source used and any missing evidence. For Entity Readiness, define ready as exactly `Ready to Hire Locals` or `Ready to Hire All`; never infer readiness from another status. A seeded baseline means there was no prior comparison, so zero reported changes is expected.

## Inputs
- `source` (enum: csv / execution, required)
- `csv_path` (string) - absolute path; must contain `country`, `ready`, optionally `status`, `updated_at`
- `execution` (string) - execution URL or ID; must belong to workflow EirKWJBySSXugv3a

## Outputs
- CSV mode: row count, unique countries, ready/not-ready counts, readiness-status counts, timestamp coverage
- Execution mode: normalized output summary, baseline/diff state, report subject, storage output count
- Every answer states the source used and any missing evidence

## Example
Input: "How many countries are ready?" with the baseline CSV.
1. `python3 scripts/analyze_baseline.py --csv "/path/entity_readiness_baseline.csv"`.
2. Report: 142 rows, 138 unique countries, 96 ready ("Ready to Hire Locals" or "Ready to Hire All" only).
3. Note: a seeded baseline means zero reported changes is expected, not a failure.

## Errors & edge cases
- Never infer readiness from another status - ready is exactly the two defined statuses.
- Execution from another workflow: rejected - never mix sources.
- Do not edit a Data Table, create a workflow, or use undocumented internal n8n routes.
- This Cloud instance does not expose Data Table rows via the public API - use the CSV path instead.
