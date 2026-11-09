---
name: recalla
description: "Rebuilds forgotten information into structured recall cards -- memory triggers, context chains, and explicitly flagged gaps, each closed with concrete retrieval paths (emails, notes, calendars, teammates) -- for meeting prep, project handoffs, and learning reviews. Use when providing intuitive recall assistance."
---

# Recalla — Intuitive Recall Assistant

## Overview
Recalla helps users retrieve, organize, and synthesize information they've encountered but can't fully remember. It generates structured recall lists, memory triggers, and contextual prompts to surface forgotten details — useful for meeting prep, project handoffs, learning reviews, and daily planning.

## When to Use
- A user is trying to remember details from a past conversation, meeting, or document.
- Preparing for a discussion where recalling prior context is critical.
- Reviewing learned material and needing structured memory aids (spaced-repetition style prompts).
- Building a personal knowledge "recollection" for a topic or project.

## How It Works
Recalla structures recall into three layers:
1. **Triggers** — Key words, dates, names, or phrases that jog memory.
2. **Context chains** — How those triggers connect to broader topics or decisions.
3. **Gap flags** — Areas where memory is fuzzy and external sources may be needed.

## Steps
1. **Clarify the recall target.** Ask: "What are you trying to remember — a conversation, a document, a timeline, a decision?"
2. **Extract known fragments.** List everything the user does remember, no matter how small.
3. **Build trigger chains.** Connect fragments into logical sequences. Identify missing links.
4. **Surface gap flags.** Mark unknowns explicitly — dates, names, outcomes, rationales.
5. **Suggest retrieval paths.** Recommend where to find the missing info (emails, notes, calendars, teammates).
6. **Output structured recall card.** Present as a markdown table or bullet hierarchy with triggers, context, and gaps.

## Common Pitfalls
- **Over-fabricating details.** Never invent specifics the user hasn't confirmed. Flag uncertainty.
- **No action plan.** A recall list without a "how to verify" step is incomplete. Always close with retrieval suggestions.
- **Too broad.** Narrow the recall target before building triggers, or the list becomes overwhelming.

## Inputs

- `recall_target` (string) -- what the user is trying to remember: a conversation, document, timeline, or decision. Narrow this first; too broad a target makes the list overwhelming.
- `known_fragments` (list) -- everything the user does remember, no matter how small: words, dates, names, phrases

## Outputs

- A structured recall card (markdown table or bullet hierarchy) in three layers: **Triggers** (words/dates/names that jog memory), **Context chains** (how triggers connect to broader topics or decisions), **Gap flags** (areas where memory is fuzzy) -- each gap closed with a suggested retrieval path

## Example

Prepping for a call with a past client. Triggers: "Q2 pricing thread", "the renewal call in May". Context chain: pricing thread -> renewal call -> pending discount approval. Gap flag: the exact quoted number (fuzzy) -> retrieval path: search sent email for the proposal PDF.

## Errors & edge cases

- **Over-fabricating details** -- never invent specifics the user hasn't confirmed; flag uncertainty explicitly.
- **Recall target too broad** -- narrow the target before building triggers.
- **No verification step** -- a recall list without a "how to verify" step is incomplete; always close with retrieval suggestions.
