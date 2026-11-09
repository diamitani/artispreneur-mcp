---
name: jev-compaction
description: "Cuts a transcript to a fixed size by having Jev mark each turn keep/summarize/drop — 40 turns per request, judged on the first+last 350 redacted characters, nothing dropped below 0.7 confidence — the right tool when the size is fixed and something must go; measured evidence shows handing a handoff writer the whole dialogue beats any digest. Use when a transcript has to be cut to a fixed size and you must choose which turns go."
version: 0.2.0
license: MIT
metadata:
  hermes:
    tags: [jev, typesafe, compaction, handoff, context]
category: ai-agents
---

# Choosing turns with Jev, and what actually makes a handoff work

Jev cannot write a summary. It can mark each turn of a transcript:

- **keep**: carries a decision, a constraint, a preference, unfinished work, or an exact value, path, id, command or error that later work depends on.
- **summarize**: background whose gist matters. In the digest this is the turn's first 400 characters, nothing more. Jev writes no gist.
- **drop**: chatter, superseded attempts, repeated output.

It judges a long turn on its first 350 and last 350 characters, redacted, 40 turns per request, and sees no other turn while it does.

## Read this before you use it for a handoff

This skill used to say a handoff written from Jev's digest "stops losing the one line that mattered". We measured that on seven real sessions and 104 recall questions ([scorecard](reference/SCORECARD-2026-09-20.md)) and it was wrong:

| the writer reads | capsule | recall alone | with one search of the old session |
|---|---|---|---|
| Jev's digest | 400 words | 37.5% | 68.3% |
| the plain last 24,000 characters | 400 words | 48.1% | 68.3% |
| **the whole dialogue** | **1,200 words** | **58.7%** | **75.0%** |
| nothing: no handoff at all | | | 56.7% |

Jev's marks did beat the same marks handed out by recency (11 questions to 4), so the judgement is real. The digest built around it clips every other turn to 400 characters, and that cost more than the judgement earned. Nous Research found the same shape with a different Jev design ([hermes-agent PR 116246](https://github.com/NousResearch/hermes-agent/pull/116246)).

So, for a handoff:

1. **Give the writer the whole dialogue.** A current flash model reads 100,000 characters for about a cent. Do not pre-filter it.
2. **Ask for up to 1,200 words**, five headings: Working on, State, Decisions, Pointers, Next. At 400 words the capsule was full whatever the writer had read.
3. **Name the session in the handoff and say it is searchable.** One search was worth 16 to 33 points to every handoff we tried, and a session with no handoff and one search beat every handoff without one. On Hermes: `session_search(query="...")`, then `session_search(session_id=..., around_message_id=...)`. Passing `query` together with `session_id` ignores the query.
4. Do not append a list of "identifiers seen". It looked free and obvious; it changed nothing with a handoff and cost 13 points without one.

The `hermes-handoff` plugin does all four. `HANDOFF_JEV=1` puts the Jev pre-pass back if you want to compare on your own sessions with `evals/compaction/run_eval.py`.

## When this skill is still the right tool

When the size is fixed and something has to go: a small local writer, a context you cannot grow, a digest for a person to skim. There, choosing turns with Jev beat choosing them by recency.

1. Get the transcript as a list of `{role, content}` messages. On Hermes: `hermes sessions export --session-id <id> --format jsonl -`.
2. Select:
   - Hermes: call `jev_compact_select` with `messages`.
   - Anywhere else:

     ```bash
     jev compact-select --digest < transcript.json      # {"messages":[...]} or a bare list
     ```

3. Write from `digest`. `[KEEP VERBATIM]` lines go in unchanged. `[background]` lines are clipped already; treat them as context, not as the record.
4. The digest is cut to its last 24,000 characters by default, oldest first, keep lines included. Pass a larger `limit` if early keep lines matter.

## Guarantees

- The last six messages are always kept (`keep_last`); system messages are always kept.
- Nothing is dropped unless Jev was confident (0.7+). An unjudged turn is marked summarize, never drop. Summarize still means clipped to 400 characters.
- Turns that look like they hold a secret are not sent to Jev.
- Jev down: every turn comes back `summarize`. That is a worse input than the plain transcript, so on `status: "fail_open"` use the plain transcript instead.
- **`status: "partial"`** means some batches answered and some did not; the ids in `unjudged` sat at the `summarize` default with nobody judging them. Treat it like `fail_open` unless `unjudged` is short and you can see it does not cover the turns you care about. It used to report `ok` in this case, so one good batch hid every failed one.

## When to compact at all

`should_compact` is arithmetic, not a model call: compact at 60% of the window, urgently at 85%. Do not ask a model whether the window is full.

## Inputs

- `messages` (list of `{role, content}`, required) — the transcript; on Hermes: `hermes sessions export --session-id <id> --format jsonl -`; anywhere else: `jev compact-select --digest < transcript.json` (accepts `{"messages":[...]}` or a bare list)
- `limit` (int, default 24,000 chars) — the digest is cut to its last N characters, oldest first, keep lines included; raise it if early keep lines matter
- `keep_last` (default: last 6 messages always kept; system messages always kept)

## Outputs

- A digest: `[KEEP VERBATIM]` lines go into the handoff unchanged (decisions, constraints, exact values/paths/ids/commands/errors); `[background]` lines are pre-clipped to their first 400 characters — treat as context, not the record
- Status: `ok` / `partial` (check `unjudged`) / `fail_open` (use the plain transcript)
- Format: digest text; `HANDOFF_JEV=1` restores the Jev pre-pass in the `hermes-handoff` plugin for comparison via `evals/compaction/run_eval.py`

## Example

A 300-turn session needs a handoff: do NOT compact first — hand the writer the whole dialogue (a flash model reads 100k chars for ~a cent), ask for up to 1,200 words under Working on / State / Decisions / Pointers / Next, and name the session ID as searchable (`session_search`, then `session_search(session_id=..., around_message_id=...)`). Measured: whole-dialogue capsules recalled 58.7% vs 37.5% for Jev-digest capsules. Reserve `jev compact-select` for the fixed-size case: a small local writer, a context you cannot grow, a digest for a person to skim.

## Errors & edge cases

- **`status: "partial"`** means some batches answered and some did not; the `unjudged` ids sat at the `summarize` default with nobody judging them. Treat it like `fail_open` unless `unjudged` is short and visibly safe (it used to report `ok` here, hiding every failed batch).
- **Jev down:** every turn comes back `summarize` — a worse input than the plain transcript. On `status: "fail_open"`, use the plain transcript instead.
- **Turns that look like they hold a secret are never sent to Jev.**
- **`should_compact` is arithmetic, not a model call:** compact at 60% of the window, urgently at 85%. Do not ask a model whether the window is full.
