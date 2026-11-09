---
name: ddc-announcements-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to post the ready-made Delali Development Cycle announcements for LinkedIn and Facebook: the nine-stage planning harness (Intake -> Documentation -> Scaffolding -> Scripts -> Connecting -> Deploying -> Testing -> Refining -> Maintaining) positioned as the car around the AI engine - used as-is, never with fake metrics or 'funded by' claims. Use when announcing the Delali Development Cycle on LinkedIn or Facebook."
---

# Delali Development Cycle — announcements

Use as-is. Do not add fake metrics or “funded by.” DDC is a framework and planning harness, not a priced round.

---

## LinkedIn

**The Delali Development Cycle (DDC)**

Most AI “website builders” skip the map and paint the storefront.

DDC is a planning harness for people who can describe a business but should not be asked for Kubernetes — and for agents that must not free-style the order of work.

**What it is**  
A nine-stage cycle — Intake, Documentation, Scaffolding, Scripts, Connecting, Deploying, Testing, Refining, Maintaining — with PAL and ROSTR inside every stage: intent, jobs-to-be-done, Now/Next/Later, PRD, architecture, then a GTM pack (ICP, AIDA messaging, channels, SLA, brand).

**What it does**  
You pick a type (SaaS, shop, gallery, directory, chat app…). You drop files and links. You say the goal in plain language. The system writes executive docs, scores you against category leaders (visual, IA, SEO, trust), and only then unlocks build.

**How it works**  
Education is on by default: each step is taught in simple language, then delivered at board level. One question if something about money, login, or data is unclear. No magic prompt. “I need a site for my studio” is enough.

**Why it matters**  
Best-in-class is not a lucky generation. It is a gate you cannot skip: taste, payments, accessibility, backups, and a path from one user to many without rewriting the product.

Manual path: Asana template.  
Machine path: GitHub skill pack for Cursor, Claude, Codex, Hermes, OpenClaw, Perplexity.

Launch is not the end of the life cycle. It is the start of Maintaining.

#ProductDevelopment #AIagents #WebDevelopment #GTM #WellArchitected

---

## Facebook

We built a way to make a serious website without needing a serious prompt.

It is called the **Delali Development Cycle**.

Think of the AI as an engine. DDC is the car: steering, brakes, and a map.

You say what you want in everyday words.  
The system teaches you each step (you can turn teaching off).  
Then it writes the grown-up documents: who it is for, what “done” means, how people pay, how it looks next to the best sites in your field, and how you will get customers (not just a pretty page).

Nine steps, always in order:

Intake → Docs → Folders → Code → Plug-ins (login, email, pay) → Put it live → Test → Improve → Keep it healthy.

If something about money or accounts is unclear, it asks **one** question. Not a homework packet.

This is for makers, shops, agencies, and anyone tired of tools that skip the boring stuff that actually makes a business real.

Peace. Courage. Success. Love — and a checklist that does not vanish when the chat does.

## Inputs
- `platform` (enum: linkedin / facebook, required)

## Outputs
- The platform's announcement text, ready to post as-is
- LinkedIn: the structured What-it-is / What-it-does / How-it-works / Why-it-matters version with hashtags
- Facebook: the plain-language engine-and-car version

## Example
Input: announce DDC on LinkedIn.
1. Platform: linkedin -> post the full structured announcement verbatim.
2. Do not add metrics, funding claims, or extra hashtags beyond the supplied set.

## Errors & edge cases
- Temptation to add metrics or "funded by": forbidden - DDC is a framework and planning harness, not a priced round.
- Platform not listed: use the closest variant's voice; do not invent a new format.
