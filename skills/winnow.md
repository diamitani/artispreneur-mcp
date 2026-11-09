---
name: winnow
description: "Sits between the agent's tools and its context, pruning low-relevance tool-result blocks into short stubs ('[winnow] ... hidden' + summary + recall key) via a per-block yes/no relevance judgment -- with winnow_recall to restore hidden text and winnow_stats for tokens saved and regret rate. Use when a tool result contains '[winnow]' lines or winnow tools are available."
category: ai-agents
---

# winnow

winnow sits between Claude Code's tools and your context. After `Read`, `Bash`, or `Grep` returns a large result, winnow splits it into blocks, asks a System One model (TypeSafe's Jev, or an LLM-backed adapter) one yes/no question per block ("is this block needed for the current task?"), and replaces the low-probability blocks with a stub.

## What a stub looks like

```
[winnow] Lines 41-188 (148 lines) hidden: judged unlikely to matter for the current task (relevance <= 0.22).
[winnow] Summary: Boilerplate license header and the argparse setup for flags that are not part of this task.
[winnow] Full text cached as key a1b2c3d4e5f6. Call winnow_recall(key="a1b2c3d4e5f6", start=41, end=188) if you need it.
```

## How to treat it

- The summary is written by a cheap model and preserves identifiers, paths, numbers and error text. Trust it for orientation, not for exact values.
- If the hidden lines might matter after all, call the `winnow_recall` tool with the key. Add `start` and `end` to fetch only part of the cached text. Do not re-run the original command just to see the hidden part; recall is cheaper and does not re-trigger side effects.
- Outputs that show an error are never pruned. If you see a stub, the judge believed the output was clean.
- Line numbers in a stub refer to the original file or output. Claude Code renumbers the rewritten result from 1, so the numbers you see in the margin of a pruned `Read` do not match the file; use the stub's range with `Read` `offset`/`limit` or `winnow_recall` to reach the original lines. `Edit` is unaffected because it matches on text, not line numbers.

## Tools

- `winnow_recall(key, start?, end?)`: return the cached full text for a key.
- `winnow_stats()`: tokens saved, outputs rewritten, and the regret rate (how often a pruned key was later recalled).

## Inputs

- `tool_result` -- a large Read/Bash/Grep result to judge block by block ("is this block needed for the current task?")
- `recall_request` -- a recall key, with optional `start`/`end` to fetch only part of the cached text

## Outputs

- Pruned results: low-probability blocks replaced with stubs (`[winnow] Lines A-B (N lines) hidden: judged unlikely to matter (relevance <= x)`, a cheap-model summary preserving identifiers/paths/numbers/error text, and the full text cached under a recall key)
- `winnow_recall(key, start?, end?)` restores cached text; `winnow_stats()` reports tokens saved, outputs rewritten, and the regret rate (how often a pruned key was later recalled)

## Example

A 200-line Read: blocks judged -> lines 41-188 stubbed ("boilerplate license header and argparse setup", relevance <= 0.22, key a1b2c3d4e5f6) -> the flags turn out to matter -> `winnow_recall(key="a1b2c3d4e5f6", start=41, end=188)` restores them without re-running the command.

## Errors & edge cases

- **Summary treated as exact values** -- trust the stub summary for orientation, not exact values; recall for precision.
- **Re-running the command instead of recalling** -- recall is cheaper and doesn't re-trigger side effects.
- **Stub line numbers vs. renumbered margins** -- stub ranges refer to the original file/output; use them with Read offset/limit or winnow_recall.
- **Pruned error outputs** -- never happen; outputs showing an error are never pruned, so a stub means the judge believed the output was clean.
