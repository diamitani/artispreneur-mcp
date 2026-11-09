---
name: transcribe-lyrics
description: "Cleans lyrics with section tags -- from an audio file, video, or rough transcript -- in three passes: raw words line-by-line, [Verse]/[Chorus]/[Bridge] section labels, and an explicit-content flag; uncertain lines marked [?] for human verification. Use when the user wants to transcribe lyrics."
---

# transcribe lyrics

- **Subagent:** @social-media-agent
- **Category:** Catalogue
- **NPAO:** N
- **List price:** $9
- **Source:** Content Creation

## When to use
Clean lyrics with section tags — from an audio file, a video, or a rough
transcript — producing a tidy lyrics sheet ready for publishing, liner notes,
or sync licensing paperwork.

## Steps
1. Pass 1 words — transcribe the raw words line by line, in order, with no
   formatting. Keep ad-libs and backing vocals in parentheses.
2. Section tags — label each block in square brackets: [Verse 1], [Chorus],
   [Pre-Chorus], [Bridge], [Hook], [Outro], [Intro], [Interlude].
3. Explicit flag — if the song contains profanity, slurs, or sexual content,
   add an explicit-content flag at the top of the file.

## Transcription rules
- One line per lyric line; never merge two sung lines into one.
- Preserve the artist's wording — do not correct grammar or slang.
- Mark uncertain lines with [?] at the end of the line so a human can verify.
- Distinguish lead vs. backing vocals: backing vocals in (parentheses).
- Repeated choruses: transcribe the chorus in full the first time, then mark
  repeats as [Chorus — repeat] only when the wording is identical.

## Outputs
lyrics.txt

## Reference tools
- None beyond parent tools

## Guardrails
Mark uncertain lines [?].

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `source` -- an audio file, a video, or a rough transcript

## Example

A rough voice memo: Pass 1 transcribes raw words line by line (ad-libs and backing vocals in parentheses) -> section tags applied ([Verse 1], [Chorus], [Bridge]) -> two uncertain lines marked [?] -> explicit-content flag added -> lyrics.txt ready for liner notes.

## Errors & edge cases

- **Merged lyric lines** -- one line per sung line; never merge two sung lines.
- **"Corrected" wording** -- preserve the artist's wording; do not fix grammar or slang.
- **Unmarked uncertainty** -- mark uncertain lines with [?] so a human verifies (guardrail).
- **Repeated choruses fully re-transcribed** -- transcribe in full the first time, then mark repeats as [Chorus -- repeat] only when the wording is identical.
