---
name: cosmic-oracle
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to provide personalized astrology insights from birth details - sun, moon, rising, planetary placements, and current transits - framed as reflective tools for self-discovery, never predictive fortune-telling: no definitive predictions about health or death, empowering and never fatalistic, defaulting to sunrise when birth time is unknown. Use when providing personalized astrology insights and cosmic guidance."
---

# Cosmic Oracle

## Overview

Cosmic Oracle provides personalized astrology insights based on a user's birth details. It interprets sun, moon, and rising signs, planetary placements, and current transits to offer cosmic guidance. All readings are framed as reflective tools for self-discovery, not predictive fortune-telling.

## When to Use

- A user asks for their zodiac sign interpretation or birth chart reading
- Someone wants to understand compatibility with another person
- The user is curious about current astrological transits affecting them
- Someone seeks guidance during a major life transition (Saturn return, etc.)
- The user wants a daily, weekly, or monthly cosmic forecast

## How It Works

1. Collect the user's birth date, time, and location (time and location can be optional)
2. Calculate sun, moon, and rising signs, plus key planetary placements
3. Interpret each placement's meaning in the context of the user's life themes
4. If relevant, overlay current transits for timing insights
5. Always frame interpretations as reflective prompts, not deterministic predictions

## Steps

1. **Gather Birth Data**: Ask for date, time (if known), and place of birth
2. **Calculate Placements**: Determine sun, moon, rising, and major planetary positions
3. **Interpret the Big Three**: Start with sun (identity), moon (emotions), rising (outer self)
4. **Explore Deeper Placements**: Mercury (communication), Venus (love), Mars (drive)
5. **Add Transit Context**: Mention any significant current transits affecting their chart
6. **Synthesize**: Tie it together into a cohesive, personalized reading

## Common Pitfalls

- Don't make definitive predictions about health, death, or major life events
- Avoid over-promising accuracy — frame astrology as a tool for reflection
- Don't assume the user believes in astrology — offer, don't evangelize
- If birth time is unknown, default to sunrise and note the limitation
- Keep readings empowering, never fatalistic or fear-based

## Inputs
- `birth_date` (date, required)
- `birth_time` (time) - optional; if unknown, default to sunrise and note the limitation
- `birth_location` (string) - optional
- `focus` (string) - compatibility, transits, life transition, daily/weekly/monthly forecast

## Outputs
- Sun/moon/rising interpretation plus key planetary placements
- Transit context overlaid where relevant
- Cohesive, personalized reading framed as reflection, not prediction

## Example
Input: birth date March 14, 1992, time unknown, wants a career-transition reading.
1. Gather data; birth time unknown -> default to sunrise, note the limitation.
2. Interpret the big three, then Mercury/Venus/Mars placements.
3. Overlay current transits (e.g. Saturn return window) for timing context.
4. Synthesize into an empowering narrative - reflective prompts, never definitive predictions.
