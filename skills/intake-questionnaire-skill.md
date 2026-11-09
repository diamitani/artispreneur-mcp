---
name: intake-questionnaire-skill
description: "Runs the 12-fact case-study intake against uploaded artifacts — extracts problem, client, actor, solution, stack, APIs, AI tools, automation platforms, data, timeline, blockers, and outcome from evidence first, tags each [E]videnced/[R]ecalled/[I]nferred for RAG/DAL provenance, and asks the user only about what can't be inferred, batched in one short message. Use when working with intake questionnaire."
---

# Intake Questionnaire — the 12 facts every case study needs

Run this against the uploaded artifacts in Stage 1. For each fact, try to **extract it from
the evidence first**. Only ask the user about facts you genuinely cannot infer. Batch all
questions into one short message — never interrogate one question at a time.

For each fact, internally tag the source as **[E]videnced** (stated in an artifact),
**[R]ecalled** (user told you directly), or **[I]nferred** (you reasoned it out). This tagging
feeds the RAG/DAL provenance step so you never overstate.

| # | Fact | What to look for | If missing |
|---|------|------------------|-----------|
| 1 | **Problem / trigger** | What pain or goal started this? A request, a broken process, a manual slog. | Ask: "What problem kicked this off?" |
| 2 | **Client / context** | Company, team, or internal stakeholder. Industry + rough size. | Ask: "Who was this for? Industry + size is enough." (needed for redaction) |
| 3 | **Actor / role** | Who did the work and in what capacity (you solo, a team, which hat). | Infer from threads; confirm if unclear. |
| 4 | **The solution** | What was actually built or done — in one sentence, then in detail. | Core — reconstruct from artifacts. |
| 5 | **Tech stack** | Languages, frameworks, no-code/low-code platforms, databases. | Scan configs, code, threads. |
| 6 | **APIs & integrations** | Which APIs/services were called; auth method (token/OAuth/key) — value NEVER captured. | Scan for endpoints, SDK names, key *names*. |
| 7 | **MCPs / agents / AI tools** | MCP servers, Claude skills, agents, models used (Opus/Sonnet, etc.). | Scan threads + tool names. |
| 8 | **Automation platforms** | n8n, Zapier, Make, Clay, HubSpot workflows, schedulers, webhooks. | Scan for workflow exports/screenshots. |
| 9 | **Data** | What data flowed through — sources, volume, shape, sensitivity. | Scan CSVs/schemas. Note PII presence. |
| 10 | **Timeline / effort** | How long, how many iterations, rough hours or sprints. | Infer from thread timestamps; confirm. |
| 11 | **Blockers & fixes** | What broke, what was tricky, how it got solved. → feeds Troubleshooting Report. | Scan for errors, retries, "didn't work", debugging. |
| 12 | **Outcome & impact** | Result. Metrics if any (time saved, $ , volume, accuracy, adoption). | Ask if no metric is evidenced — but never invent one. |

## Systems-thinking probes (surface these if the evidence supports them)

These are what separate a "I built a script" story from a "I architected a system" story.
Look for evidence that the project reasoned about:

- **Data flow** — how information moved end-to-end, transformations, sources of truth.
- **Failure modes** — retries, fallbacks, error handling, what happens when a step fails.
- **Scale** — designed for one run or for 50+ reps / thousands of records?
- **Handoffs** — human-in-the-loop gates, approvals, where control passes between systems.
- **Feedback loops** — logging, monitoring, learning from outputs, iteration based on results.
- **Tradeoffs** — choices made and why (cost vs speed, build vs buy, model selection).

If two or more of these are evidenced, the Case Study gets a dedicated **"Systems Thinking"**
section. If only one, fold it into the "How it worked" narrative.

## When to ask vs infer

**Ask** only when: a fact is critical to the narrative (problem, outcome, client/industry for
redaction) AND there is no reasonable basis to infer it. **Infer** (and tag [I]) for
everything reconstructable from the artifacts. The goal is a fast, low-friction intake — the
user dropped files because they want a document, not a survey.

## Inputs

- `artifacts` (files, required) — uploaded evidence scanned in Stage 1: repos, configs, threads, CSVs, screenshots, workflow exports
- The 12-fact table (problem, client, actor, solution, stack, APIs, AI tools, automation platforms, data, timeline, blockers, outcome) — each fact extracted from evidence first
- `question_batch` (one short message) — only facts with no reasonable inferable basis get asked

## Outputs

- All 12 facts with source tags: **[E]videnced** (stated in an artifact), **[R]ecalled** (user told you), **[I]nferred** (reasoned out) — feeding the RAG/DAL provenance step so nothing is overstated
- A dedicated **Systems Thinking** section when 2+ of the six probes (data flow, failure modes, scale, handoffs, feedback loops, tradeoffs) are evidenced; folded into narrative when only one
- Format: intake record ready for case-study drafting — fast, low-friction, never a survey

## Example

Artifacts: repo export + Slack thread. Extracted: problem = 'manual CSV cleanup slog' [E], stack = 'Python/pandas' [E from requirements.txt], APIs = 'Stripe (key name sk_live_…)' [E — name only], outcome = '$12k/yr saved' [R — user said it]. Not inferable: client industry (needed for redaction) → one batched ask: 'Who was this for? Industry + size is enough.' Systems probes: retries + logging evidenced → Case Study gets a dedicated 'Systems Thinking' section.

## Errors & edge cases

- **Never invent a metric.** If no outcome metric is evidenced, ask — do not fabricate one.
- **API key values are NEVER captured** — record key *names* and auth methods only.
- **Never interrogate one question at a time.** Batch all genuine gaps into a single short message.
- **Note PII presence** in the Data fact (fact 9) when scanning CSVs/schemas.
