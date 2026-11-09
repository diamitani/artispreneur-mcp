---
name: ai-palmistry-guide
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to perform virtual palm readings from user-described palm features - heart, head, life, and fate lines plus mounts and finger shapes - synthesized into a reflective, empowering narrative explicitly framed as traditional art for self-reflection, not science. Use when providing AI-powered virtual palm readings."
---

# AI Palmistry Guide

## Overview

AI Palmistry Guide offers virtual palm readings based on user-provided descriptions or photos of their palms. It interprets major lines (heart, head, life, fate) along with mounts, finger shapes, and other features — delivering readings that are insightful, entertaining, and framed as self-reflection tools.

## When to Use

- A user requests a palm reading or asks about palmistry
- Someone shares a photo or description of their palm for interpretation
- The user is curious about what palm lines "mean"
- Someone wants a fun, reflective experience for entertainment or introspection
- The user asks specific questions about love, career, or health lines

## How It Works

1. Ask the user to describe their palm or share a photo (note: you cannot actually see images, so guide them to describe)
2. Walk through the major lines and features systematically
3. Interpret each feature using traditional palmistry symbolism
4. Synthesize into a cohesive, personalized reading
5. Always note that palmistry is a traditional art for reflection, not science

## Steps

1. **Get Palm Description**: Ask which hand is dominant, and have them describe the major lines
2. **Heart Line**: Interpret curvature, length, and breaks (emotional life)
3. **Head Line**: Interpret length and depth (intellect, decision-making style)
4. **Life Line**: Interpret length, depth, and branches (vitality, major life changes)
5. **Fate Line**: Interpret presence/absence (career path, sense of purpose)
6. **Mounts and Extras**: Note prominent mounts, finger shapes, or special markings
7. **Synthesize Reading**: Weave interpretations into a unified, empowering narrative

## Common Pitfalls

- Don't make alarming predictions (early death from a short life line — this is a myth anyway)
- Avoid medical or health diagnoses disguised as palmistry
- Don't claim scientific validity — be transparent this is traditional/interpretive
- If the user can't describe their palm well, offer general palmistry education instead
- Keep it light and fun unless the user brings serious emotional weight

## Inputs
- `hand` (enum: dominant / non-dominant, required)
- `line_descriptions` (object) - user-described heart, head, life, fate lines (length, curvature, depth, breaks)
- `extra_features` (string) - mounts, finger shapes, special markings
- `focus` (string) - love, career, or general reflection, if the user has one

## Outputs
- Line-by-line interpretation using traditional palmistry symbolism
- Synthesized reading woven into a unified, empowering narrative
- Framing note: traditional/interpretive art, not scientific

## Example
Input: dominant right hand; long curved heart line, deep straight head line, life line with one branch, faint fate line; focus on career.
1. Heart line: emotionally expressive, values deep connection.
2. Head line: analytical, decisive.
3. Life line: vitality with a major branch = one significant life change.
4. Fate line: faint = career path self-directed rather than predetermined.
5. Synthesize into an empowering narrative with the traditional-art framing; no alarming predictions.
