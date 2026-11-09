---
name: business-audit
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to perform dynamic business audits across six pillars - financials, operations, marketing/sales, product, team, market positioning - scoring each (1-5 or red/yellow/green), surfacing the top 3-5 risks and opportunities, and delivering a structured report with prioritized action items and an optional roadmap. Use when performing dynamic business audits and strategic planning assessments."
---

# Business Audit

## Overview
Performs dynamic business audits and strategic planning assessments. Analyzes business health across key dimensions and identifies growth opportunities. Helps entrepreneurs and managers understand their current state and prioritize actions.

## When to Use
- A user asks for a business health check, SWOT analysis, or strategic assessment
- Evaluating a company's strengths, weaknesses, opportunities, and threats
- Preparing for fundraising, pivots, or strategic planning sessions
- Benchmarking against industry standards or competitors
- Identifying operational gaps and growth levers

## How It Works
Systematically evaluates the business across core pillars: financials, operations, marketing/sales, product, team, and market positioning. Produces a structured audit report with findings, risks, and prioritized recommendations.

## Steps
1. Gather context: business model, industry, stage, team size, revenue
2. Assess each pillar with targeted questions and data review
3. Score each pillar on a simple scale (e.g., 1–5 or red/yellow/green)
4. Identify top 3–5 risks and top 3–5 opportunities
5. Produce a summary report with prioritized action items
6. Optionally generate a roadmap or next-step timeline

## Common Pitfalls
- Making recommendations without sufficient context — ask clarifying questions first
- Over-indexing on one pillar (e.g., only financials) while ignoring others
- Providing vague advice — always tie recommendations to specific metrics or actions
- Failing to prioritize — not everything can be fixed at once
- Assuming industry benchmarks without verifying them

## Inputs
- `business_model` (string, required), `industry` (string), `stage` (string), `team_size` (integer), `revenue` (string)
- `focus` (string) - fundraising, pivot, strategic planning, benchmarking
- `benchmarks` (string) - industry standards to compare against, verified not assumed

## Outputs
- Pillar-by-pillar assessment with scores and evidence
- Top 3-5 risks and top 3-5 opportunities
- Summary report with prioritized action items; optional roadmap/next-step timeline

## Example
Input: audit a 12-person SaaS at $40k MRR preparing for a seed round.
1. Gather context across all six pillars with targeted questions.
2. Score: financials yellow (burn 14 months), product green, marketing red (no repeatable channel).
3. Top risks: single-channel acquisition, key-person dependency; top opportunities: expansion revenue, pricing.
4. Report with prioritized actions and a 90-day roadmap.
