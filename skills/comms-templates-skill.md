---
name: comms-templates-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to write from copy-paste stakeholder communication templates in Patrick's voice (direct, concise, no fluff): weekly status updates, executive briefings, cross-functional heads-ups, post-meeting follow-ups, escalations to leadership, and celebrating wins - each making the ask, the risk, and the timeline explicit. Use when working with stakeholder communication templates."
---

# Stakeholder Communication Templates

Use these as starting points. Adapt to Patrick's voice — direct, concise, no fluff.

---

## Weekly Status Update (async Slack or email to manager)

```
Hey [Manager] — quick weekly update:

✅ Done this week:
- [Item 1]
- [Item 2]

🔄 In flight:
- [Project A] — on track for [date]
- [Project B] — slight delay due to [reason], new ETA [date]

🚧 Blocked / needs input:
- [Item] — waiting on [person/decision]

📅 Next week focus:
- [Top 2-3 priorities]

🙋 Asks from you:
- [Any decisions or unblocks needed from manager]
```

---

## Executive Briefing (for skip-level or leadership)

```
[Project/Initiative Name] — Status Update

TL;DR: [One sentence on where things stand]

What's working:
- [Key win or progress]

What's at risk:
- [Any yellow/red flags — be direct]

Decision needed (if any):
- [Specific ask, framed as a choice]

Timeline: [Next milestone + date]
```

---

## Cross-functional Heads Up

Use when Patrick's work will impact another team, or when he wants to build visibility with a peer.

```
Hey [Name] — heads up on something that might be relevant to your team:

[1-2 sentences on what Patrick is working on and why it connects to them]

Happy to sync briefly if useful, or just wanted you to have the context. No action needed on your end right now.
```

---

## Post-Meeting Follow-Up

```
Thanks everyone for [meeting name] — quick recap:

Decisions made:
- [Decision 1]
- [Decision 2]

Action items:
- [Person]: [Task] by [Date]
- [Person]: [Task] by [Date]

Next meeting: [Date/time, or "to be scheduled"]

Anything I missed?
```

---

## Escalation to Leadership

Use when something is at risk and leadership needs to know before it becomes a crisis.

```
Heads up — flagging a risk on [project/initiative]:

Situation: [What's happening, factually]
Impact: [What happens if this isn't addressed — be specific]
What I need: [Clear, specific ask — a decision, a resource, an unblock]
Timeline: [When do you need a response to avoid the impact]

Happy to jump on a call if easier.
```

---

## Celebrating a Win (for manager or Slack channel)

Keep it brief — directors don't over-celebrate, but they do make wins visible.

```
Quick win worth sharing: [Project/person/outcome]

[1-2 sentences on what happened and why it matters]

Shoutout to [anyone who contributed].
```

## Inputs
- `template` (enum: weekly-status / exec-briefing / cross-functional / follow-up / escalation / win, required)
- `facts` (object) - done items, in-flight with ETAs, blockers, asks, decisions, risks

## Outputs
- Filled template adapted to Patrick's voice - direct, concise, no fluff
- Explicit ask, impact, and timeline in escalations; TL;DR-first in exec briefings

## Example
Input: weekly status update to the manager.
1. Template: weekly-status; facts: 2 done, Project A on track, Project B delayed 3 days (vendor), need headcount decision.
2. Fill: Done / In flight / Blocked / Next week / Asks sections.
3. Voice check: direct sentences, no filler; the headcount ask is explicit with its deadline.

## Errors & edge cases
- Missing facts: do not invent status - ask for the specific item or mark it TBD.
- Escalation without a clear ask: an escalation must name the decision, resource, or unblock needed plus its deadline.
- Wins: keep brief - visible, not over-celebrated.
