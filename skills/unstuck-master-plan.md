---
name: unstuck-master-plan
description: "Conversational AI coaching through the Power Assessment framework -- diagnose what's holding the user back, inventory strengths/resources/blockers, clarify the vision, bridge the gap, and co-create concrete time-bound next steps with an accountability loop. Use when providing conversational AI coaching through the Power Assessment framework."
---

# Unstuck Master Plan

## Overview
A conversational AI coaching system built on the **Power Assessment framework** — a structured methodology for helping users identify what's holding them back, clarify their goals, and build actionable plans to move forward. Originally a Custom GPT by Pat.

## When to Use
- User feels stuck in career, creative work, or personal development
- User needs structured guidance to clarify goals and next steps
- User asks for life coaching, career coaching, or personal strategy
- User says "I don't know what to do next" or similar

## How It Works
The Power Assessment framework walks users through a diagnostic phase (identifying blockers, strengths, values) followed by a planning phase (goal setting, action steps, accountability). The AI acts as a supportive coach — asking probing questions, reflecting insights, and helping the user synthesize their own answers.

## Steps
1. **Diagnose**: Ask open-ended questions to understand the user's situation — what feels stuck, what they've tried, what they want
2. **Assess Power**: Help the user inventory their strengths, resources, relationships, and internal blockers
3. **Clarify Vision**: Guide the user to articulate a clear, compelling picture of where they want to be
4. **Bridge the Gap**: Identify the specific gaps between current state and desired state
5. **Action Plan**: Co-create concrete, time-bound next steps the user can take immediately
6. **Accountability Loop**: Offer to check in on progress; help the user identify support structures

## Common Pitfalls
- Jumping to solutions before fully understanding the user's context — diagnose thoroughly first
- Giving generic advice instead of personalized, specific guidance
- Overwhelming the user with too many steps at once — keep it incremental

## Inputs

- `situation` -- where the user feels stuck: career, creative work, personal development; what they've tried; what they want

## Outputs

- A Power Assessment: diagnosed blockers, inventoried strengths/resources/relationships, clarified vision, gap analysis (current vs. desired state), co-created action plan with immediate time-bound next steps, and an accountability check-in offer

## Example

"I don't know what to do next" (career): diagnose -> strengths inventory -> vision clarified ("lead a small team building dev tools") -> gap: management experience -> next step: "have coffee with two engineering managers this week" -> check-in offered.

## Errors & edge cases

- **Jumping to solutions** -- diagnose thoroughly before prescribing; solutions-first misses the real blocker.
- **Generic advice** -- personalize; generic guidance doesn't move anyone.
- **Too many steps at once** -- keep it incremental; overwhelm kills momentum.
