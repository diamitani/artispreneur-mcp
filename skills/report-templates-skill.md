---
name: report-templates-skill
description: "Six locked Maia marketing-chatbot report formats -- Executive Snapshot, Funnel Analysis, Daily Digest, Bad Conversations Review, Board One-Pager, and ad-hoc Q&A -- each with its KPI definitions and a strict sourcing rule: numbers only from this session's API responses; missing data stated as 'not available' with the reason. Use when working with maia report templates."
---

# Maia Report Templates

Every report header must state: **date range · data sources · pulled at (CT)**.
Numbers only from API responses received this session. Missing data → say "not available"
with the reason.

---

## 1. Executive Snapshot (VP Marketing / leadership)

One screen. KPIs (from MAIA_REPORTING_JTBD.md Job 1):

| KPI | Definition |
|---|---|
| Conversations handled | Threads in inbox 1736871815 in range |
| Leads created | Contacts with chatbot_session_id, createdate in range |
| MQLs | lifecyclestage=marketingqualifiedlead within cohort (chatbot_lead_temperature `hot` as secondary signal) |
| Meetings booked | Meetings associated to Maia cohort |
| Deals created / won | Association walk from cohort |
| Pipeline $ / Closed-won $ | Sum of deal `amount` |
| WSEs (closed) | WSE property on won deals |

Then conversion rates: lead-capture %, MQL %, meeting %, win %.
Close with **So what** — 2–3 bullets: what's working, what needs attention, next step.

## 2. Funnel Analysis

Conversations → Leads → MQLs → Meetings → Deals → Won → WSEs, with counts and stage-to-stage
conversion %. Flag the biggest drop-off stage and hypothesize why using conversation-level
evidence (temperatures, disqualification reasons, unanswered questions).

## 3. Daily Digest (the table the n8n workflow captures)

Header KPIs for the day (vs. prior day), then one row per conversation:

| Conversation (thread ID) | Contact | Company | Summary | Temp | MQL? | Meeting? | Recommended next step |
|---|---|---|---|---|---|---|---|

- Summary = `maia_chat_summary` (fallback: summarize `chatbot_transcript` and label it
  "generated summary").
- Append a **Gaps** section: conversations with no matched contact, contacts with no MQL
  verdict (possible n8n failure — check executions), and any n8n execution failures for
  `SKUv0NlJUsWyNB4Z` that day.

## 4. Bad Conversations Review

A conversation is flagged **bad** if any of:
1. Visitor asked for a human / expressed frustration or complaint (transcript scan)
2. Maia couldn't answer ≥2 questions (`chatbot_questions_asked` vs. transcript answers)
3. Qualified buying intent but **no** email captured (lost lead)
4. `chatbot_disqualification_reason` populated on a contact that looks ICP (misfire)
5. Contact matched but MQL classification never ran (n8n execution missing/failed)
6. Wrong/contradictory answer on compliance, pricing, or country capability (escalate to
   Patrick — this is a guidelines fix via hubspot-chatbot-manager)

Output: table (thread ID · date · contact/anon visitor · failure category · evidence quote
≤1 line · recommended fix) + count by category + trend vs. prior period.

## 5. Board One-Pager

Narrative, non-technical, ≤1 page:
- **Headline:** pipeline generated and stage (e.g., "Maia sourced $X in pipeline from N
  conversations this quarter").
- **Proof case:** one concrete story (chat → MQL → meeting → deal) with company name.
- **Quality:** MQL rate, meeting rate, bad-conversation rate with one-line interpretation.
- **Reliability:** scoring-automation success rate (from n8n executions), uptime issues if any.
- **Asks / next:** what's being improved next.
- Aggregates and company names only — no individual emails/phones. Attribution tiers stated
  honestly (sourced vs. influenced).

## 6. Ad-hoc Q&A

For one-off questions ("how many MQLs this week?"), answer in 1–3 sentences with the number,
range, and source — no template scaffolding. Offer the relevant full report as a follow-up.

## Inputs

- `report_type` -- one of the six formats: Executive Snapshot | Funnel Analysis | Daily Digest | Bad Conversations Review | Board One-Pager | ad-hoc Q&A
- `date_range` -- every report header states: date range, data sources, pulled at (CT)
- `data` -- KPIs computed from API responses received this session only (conversations handled, leads created, MQLs, meetings booked, deals created/won, pipeline/closed-won $, WSEs)

## Outputs

- **Executive Snapshot** -- one-screen KPI table + conversion rates + "So what" bullets (what's working, needs attention, next step)
- **Funnel Analysis** -- Conversations -> Leads -> MQLs -> Meetings -> Deals -> Won -> WSEs with stage-to-stage conversion % and the biggest drop-off flagged with a hypothesis
- **Daily Digest** -- header KPIs vs. prior day, one row per conversation (thread ID, contact, company, summary, temp, MQL?, meeting?, next step), plus a Gaps section
- **Bad Conversations Review** -- flagged-conversation table (thread ID, date, contact, failure category, evidence quote, recommended fix) + count by category + trend
- **Board One-Pager** -- narrative, non-technical, 1 page max: headline, proof case, quality, reliability, asks/next
- **ad-hoc Q&A** -- 1-3 sentence answer with the number, range, and source; offer the full report as follow-up

## Example

Daily Digest for yesterday: header KPIs vs. prior day; one row per conversation ("thread 88412, Acme Corp, pricing question, hot, MQL yes, meeting booked, next: AE follow-up"); Gaps section flags 2 conversations with no matched contact and 1 n8n execution failure for workflow SKUv0NlJUsWyNB4Z.

## Errors & edge cases

- **Missing data** -- never invent; state "not available" with the reason.
- **Bad-conversation false negatives** -- flag when: visitor asked for a human / expressed frustration; Maia couldn't answer 2+ questions; qualified buying intent but no email captured; disqualification misfire on an ICP contact; MQL classification never ran; wrong/contradictory compliance, pricing, or country answer (escalate guideline fixes via hubspot-chatbot-manager).
- **Board one-pager privacy** -- aggregates and company names only; no individual emails or phones; attribution tiers stated honestly (sourced vs. influenced).
