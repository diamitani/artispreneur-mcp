---
name: director-readiness-framework-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to coach director readiness through the six director muscles: Strategic Clarity, Organizational Influence, Communication at Scale, Talent and Leverage, Decision Velocity, External Orientation - each with manager-vs-director behavior pairs and watch-for prompts, plus positive readiness signals to reinforce and common blind spots for AI managers going to director. Use when coaching Patrick on director readiness."
---

# Director Readiness Framework

## What "Director-Ready" Looks Like at Patrick's Level

This framework helps you coach Patrick when he's operating below his target altitude, and recognize when he's operating above it.

---

## The Six Director Muscles

### 1. Strategic Clarity
**Manager behavior**: Executes on projects assigned to them. Asks "what should I build?"
**Director behavior**: Sets direction. Asks "what *should* we be building, and why?"

Watch for: Patrick taking on work without questioning whether it's the right work. Prompt: *"Before diving in — is this the highest-leverage thing right now, or is there a more strategic angle?"*

### 2. Organizational Influence
**Manager behavior**: Works within their team and immediate stakeholders.
**Director behavior**: Builds relationships across functions. Gets invited to conversations they're not formally part of.

Watch for: Patrick executing in a silo. Prompt: *"Who outside your immediate team should know about this? Could be a good touchpoint opportunity."*

### 3. Communication at Scale
**Manager behavior**: Updates their manager when asked.
**Director behavior**: Proactively controls the narrative — brief leadership before they ask, surface risks early, celebrate wins publicly.

Watch for: Patrick going quiet for more than 3-4 days. Prompt: *"Quick visibility check — when did you last update [manager] on what you're working on?"*

### 4. Talent and Leverage
**Manager behavior**: Does the work.
**Director behavior**: Multiplies through others. Delegates deliberately. Develops people.

Watch for: Patrick bottlenecking things on himself. Prompt: *"Is there someone on the team who could own this? What would it take to hand it off?"*

### 5. Decision Velocity
**Manager behavior**: Escalates decisions upward frequently.
**Director behavior**: Makes decisions at the right altitude — escalates strategically, not reflexively.

Watch for: Patrick asking for permission on things he should decide. Prompt: *"This feels like a decision you can make — do you have the context you need to just call it?"*

### 6. External Orientation
**Manager behavior**: Focused on internal execution.
**Director behavior**: Aware of market trends, competitor moves, customer signals — brings external context into internal decisions.

Watch for: Patrick only talking about internal projects. Prompt: *"Is there an external angle here — what are other companies doing with AI in this space?"*

---

## Director Readiness Signals (Positive)

When you see Patrick doing these things, call it out — positive reinforcement matters:
- Proactively briefs leadership without being asked
- Delegates work rather than doing it himself
- Comes to meetings with a recommendation, not just a status
- Connects cross-functional dots ("This intersects with what Sales is working on...")
- Sets boundaries on low-leverage work
- Advocates for his team publicly

---

## Common Blind Spots for AI Managers Going to Director

1. **Over-indexing on building**: AI managers often love to build. Directors need to know when *not* to build, and when to leverage others' builds.
2. **Underestimating the politics**: Director roles require navigating organizational dynamics. Encourage Patrick to invest in relationships, not just output.
3. **Measuring by output, not outcome**: Did the thing you built actually change behavior? Directors are accountable to outcomes, not deliverables.
4. **Not developing a successor**: Directors think about who will backfill them. Who is Patrick developing to take over his current responsibilities?
5. **Staying in tactical mode**: Easy to get pulled into execution. Director meetings should be about strategy, not status.

## Inputs
- `situation` (string, required) - what Patrick is doing or deciding
- `muscle` (enum: strategic-clarity / influence / communication / talent / decision-velocity / external) - inferred from the situation

## Outputs
- Altitude check: manager behavior vs director behavior for the situation, with the specific prompt to use
- Positive signals called out when present; blind spots named when they appear

## Example
Input: Patrick is deep in building a feature nobody asked for.
1. Muscle: Strategic Clarity - manager asks "what should I build?", director asks "what should we be building, and why?"
2. Prompt: "Before diving in - is this the highest-leverage thing right now, or is there a more strategic angle?"
3. Blind spot flagged: over-indexing on building; measuring by output, not outcome.

## Errors & edge cases
- Quiet for 3-4+ days: trigger the Communication-at-Scale visibility check.
- Bottlenecking on himself: trigger the Talent-and-Leverage handoff prompt.
- Permission-seeking on decidable calls: trigger the Decision-Velocity prompt instead of answering for him.
