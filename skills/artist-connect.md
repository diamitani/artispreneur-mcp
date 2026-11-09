---
name: artist-connect
description: "Mentorship matchmaker for independent artists: diagnoses the support gap (technical, strategic, emotional), maps it to real artist journeys and peer networks, and builds accountability structures. Use when connecting artists with mentorship, coaching, and real advice from true artist journeys."
---

# Artist Connect

Connect independent artists with mentorship, coaching, and real-world advice drawn from authentic artist journeys. Bridge the gap between where artists are and where they want to be.

## Workflow

1. Understand the artist's goals, challenges, and current career stage.
2. Identify the type of support needed: technical mentorship (production, songwriting), career coaching (strategy, branding), or emotional guidance (creative blocks, burnout).
3. Draw from real artist journeys and case studies to provide relatable, actionable advice.
4. Recommend mentorship resources: online communities, coaching programs, industry workshops, and peer networks.
5. Facilitate peer connections where appropriate — artists learning from artists at similar stages.
6. Provide accountability structures: goal setting, check-in schedules, and milestone tracking.

## Key Considerations

- Shared experience builds trust — reference real journeys, not just theory.
- Different stages require different types of mentorship.
- Encourage artists to both seek and offer mentorship — teaching reinforces learning.
- Prioritize mental health and sustainable creative practices.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `goals` | string | required | What the artist is trying to achieve. |
| `challenges` | string | required | What's in the way (creative block, no strategy, burnout, isolation). |
| `career_stage` | enum | -- | `emerging` | `developing` | `breakthrough` | `established` |
| `support_type` | enum | auto | `technical` (production, songwriting) | `career` (strategy, branding) | `emotional` (blocks, burnout) |

## Outputs

- **Deliverable:** a mentorship plan -- the right support type, resource recommendations (communities, coaching, workshops, peer networks), and an accountability structure (goals, check-in cadence, milestones).
- **Format:** chat brief with concrete next steps.

## Example

> Producer, developing stage: "I'm burned out and haven't finished anything in 4 months."

1. Diagnose: emotional-guidance track (burnout), not a technical gap.
2. Map to real journeys: artists who rebuilt output through rest + small-ship cadence, not grind.
3. Plan: peer community for co-working, sustainable creative practices, 30-day check-in milestones; revisit career coaching once output stabilizes.

## Errors & edge cases

- Asks for a manager, not a mentor -> clarify the difference before matching; managers take commission, mentors don't.
- No local scene -> route to online communities and remote coaching programs.
- Wants only "industry connects" -> reframe: peer mentorship at a similar stage often moves faster than access-chasing.
- Encourage giving back: artists should both seek and offer mentorship.
