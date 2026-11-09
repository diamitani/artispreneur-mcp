---
name: create-lyric-video
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build a timed lyric storyboard from a verbatim transcription: play the track and mark each line's start time, apply the drop rules (hook always in caps, beat-synced emphasis, one accent color for the hook, max two lines on screen during the chorus), export CSV/SRT alongside the video for accessibility - never guessing timings, producing lyric-timing.md. Use when the user wants to create a lyric video."
---

# create lyric video

- **Subagent:** @social-media-agent
- **Category:** Content
- **NPAO:** O
- **List price:** $19
- **Source:** Content Creation

## When to use
Timed lyric storyboard.

## Steps
1. Transcribe first
2. timestamps
3. caps on drop

## Outputs
lyric-timing.md

## Reference tools
- reference/templates/lyric-timing.md

## Guardrails
Needs transcript first. Never guess timings — every row in the timing
sheet comes from listening to the actual track. Lyrics are transcribed
verbatim, no paraphrasing.

## How to run it
1. Transcribe the full lyric verbatim before opening the timing sheet.
2. Play the track and mark each line's start time; mark the drop/hook
   sections for visual emphasis.
3. Apply the drop rules: hook always in caps, beat-synced emphasis, one
   accent color reserved for the hook, max two lines on screen during
   the chorus.
4. Export the sheet as CSV/SRT alongside the video for accessibility,
   and keep a copy with the project files — the next single reuses the
   timing structure.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `track` (audio file, required) - the actual track; timings come from listening, never guessed
- `lyrics` (string) - full lyric transcribed verbatim, no paraphrasing

## Example
Input: lyric video for a 3:20 single.
1. Transcribe the full lyric verbatim before opening the timing sheet.
2. Play the track; mark each line's start time; mark drop/hook sections for emphasis.
3. Drop rules: hook in caps, beat-synced emphasis, one accent color for the hook, max two lines on screen in the chorus.
4. Export lyric-timing.md + CSV/SRT for accessibility; keep a copy with the project files for the next single.

## Errors & edge cases
- No transcript available: transcribe first - the guardrail forbids starting timing without one.
- Timing row without a listened timestamp: never guess; every row comes from the actual track.
- Paraphrased lyrics: forbidden - transcribe verbatim.
