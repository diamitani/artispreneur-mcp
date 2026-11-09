---
name: context-engine-rostr-core
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to rely on the always-on agent memory loop (rostr-core): the runtime - not the agent - saves each session as markdown, compresses it into tiered storage (hot raw under 7 days, warm gzip under 30, cold auto-summary), indexes one row per session in the master brain library, and loads the last session back at session start - with fire-and-forget checkpoints that can never block the agent. Use when working with the agent's memory (the always-on session loop)."
---

# context-engine

> The agent's memory. A loop that runs on EVERY session, in the background:
> it saves the session as a compressed `.md`, stores it, indexes it — and
> the next session pulls the last one (or all of them) back.

**Price:** $15 · **Vertical:** developer · **Version:** 2.0.0

## Always-on, not called manually

The agent does **not** invoke this skill per session. The **runtime** runs
the loop automatically on two triggers:

1. **Length trigger** — when the context window approaches its end
   (default: 75% of the model's token limit) → distill the session so
   far → save → compress → index → continue with the distilled summary.
2. **Time trigger** — periodic checkpoint during long sessions (default:
   every 30 minutes) → plus a final save at session end.

The save/compress/index path runs in a **background thread**
(fire-and-forget). A checkpoint can never block or break the agent —
failures are logged, never raised.

Config (env):
- `CONTEXT_CHECKPOINT_TOKENS_PCT` — default `75`
- `CONTEXT_CHECKPOINT_MINUTES` — default `30`
- `CONTEXT_BACKGROUND` — default `true` (set `false` for synchronous
  checkpoints in tests/scripts)

## The procedure the runtime follows

### 1. Save

At session end (or on a trigger): the transcript becomes a markdown file.

### 2. Compress + store

The `.md` goes into the storage folder:

```
storage/sessions/<project_id>/<session_id>.md
```

The file path **is** the link — the index row points at it. Fresh
sessions stay raw (hot tier).

### 3. Index

One row goes into the **master brain library** — the single central index
of everything (sessions, ingested sources, links):

| column | meaning |
|---|---|
| `id` | row id |
| `kind` | `session` \| `source` \| `link` |
| `project_id` | knowledge never crosses projects |
| `path` | the link: storage path for sessions, URL for sources/links |
| `summary` | one-line description (keyword-searchable) |
| `bytes_raw` / `bytes_stored` | size before/after compression |
| `compression_level` | `raw` \| `gzip` \| `summary+gzip` |
| `created_at` / `last_accessed` | age drives the compression tiers |

Local backend: `storage/index.json`. Production: the `kb_items` table
in Supabase (schema in `supabase_schema.sql`).

### 4. Load (next session)

At session start the runtime pulls the **last** session item (or **all**
of them on request), decompressed on read, and injects them into the new
session's context. `load_last(project_id)` / `load_sessions(project_id,
limit)`.

## Continual compression (the library shrinks itself)

A maintenance pass (`compress_library(project_id)`) runs on a schedule
and re-tiers every session row by age:

- **Hot** (< 7 days) — stays raw `.md`. Recent work must be instantly
  readable.
- **Warm** (< 30 days) — gzipped. Full text kept, ~70–80% smaller.
- **Cold** (> 30 days) — auto-summarized (extractive: headings + opening,
  clearly labeled `AUTO-SUMMARY`), then gzipped. The gist survives; the
  bulk doesn't.

Every pass reports `{processed, gzipped, summarized, bytes_before,
bytes_after, bytes_saved}` so you can watch the library fit your data
limits.

## The two halves (don't mix them up)

- **Context Engine (this skill):** session memory — what the agent
  itself did and learned. `save_session` / `load_last` / `load_sessions`
  / `compress_library`.
- **RAG DAL (`ragdal.py`):** outside-world research — URL ingest,
  chunking, link graph, vector retrieval. Its sources and links land in
  the *same* master library as `source`/`link` rows.

## Outputs

- Checkpoint rows in the master index; decompressed session text on load.
- `pack_text` — the injectable session-memory string PAL stage 2 adds
  to every compiled prompt.

## Pairs well with

- Every skill: memory makes all of them smarter across sessions.
- `build-a-skill` — past sessions are the raw material for new skills.

## Inputs
- None for the agent - the runtime drives the loop on two triggers: length (context near 75% of the token limit) and time (every 30 minutes + session end)
- `project_id` (string) - knowledge never crosses projects
- Config env: CONTEXT_CHECKPOINT_TOKENS_PCT (75), CONTEXT_CHECKPOINT_MINUTES (30), CONTEXT_BACKGROUND (true)

## Example
Input: a long build session crosses 75% of the context window.
1. Runtime distills the session so far -> saves the .md to storage/sessions/<project_id>/<session_id>.md.
2. Indexes one row in the master brain library (kind=session, path=storage path, summary, compression level).
3. Continues with the distilled summary; failures log, never raise.
4. Next session: load_last(project_id) injects the last session; compress_library re-tiers by age on schedule.

## Errors & edge cases
- Never invoke the loop manually - it is runtime-driven; the agent must not duplicate it.
- Checkpoint failures: logged only, never raised; a checkpoint can never break the agent.
- Cold-tier summaries are extractive and labeled AUTO-SUMMARY - the gist survives, the bulk does not.
- Do not mix up the halves: this skill is session memory (save/load/compress); ragdal.py is outside-world research ingest.
