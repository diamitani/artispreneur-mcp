---
name: eor-topics-skill
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to answer from the EOR topics reference: a topic-to-search-terms map across nine areas (hiring, termination, payroll, employer costs, benefits, compliance, probation, visa, working hours) for building SharePoint search queries, the key EOR concepts reps encounter (direct EOR model, 13th/14th month, probation, notice periods, severance, employer tax burden), and frequently asked countries prioritized by region. Use when building SharePoint search queries for common EOR topics."
---

# Common EOR Topics & Search Keywords

Use this as a reference when building SharePoint search queries.

## Topic → Search Terms Mapping

| Rep's Question Type | Good SharePoint Search Terms |
|---|---|
| Hiring / onboarding | "onboarding timeline [country]", "new hire requirements [country]", "employment contract [country]" |
| Termination / severance | "termination [country]", "severance [country]", "notice period [country]", "redundancy [country]" |
| Payroll | "payroll [country]", "salary [country]", "pay frequency [country]", "13th month [country]" |
| Employer costs | "employer costs [country]", "social contributions [country]", "employer tax [country]" |
| Benefits | "statutory benefits [country]", "leave entitlement [country]", "health insurance [country]" |
| Compliance | "labor law [country]", "compliance [country]", "regulatory [country]" |
| Probation | "probation period [country]", "trial period [country]" |
| Visa & mobility | "work visa [country]", "work permit [country]", "right to work [country]" |
| Working hours | "working hours [country]", "overtime [country]", "hours regulations [country]" |

## Key EOR Concepts Reps Encounter

- **EOR (Employer of Record)**: {{COMPANY_NAME}} is the legal employer. {{COMPANY_NAME}} handles payroll, compliance, HR admin. Client is the day-to-day manager.
- **Direct EOR Model**: {{COMPANY_NAME}} owns entities in 160+ countries — no third-party aggregators. Faster, more compliant.
- **Onboarding SLA**: Typical 2–5 business days in most countries (varies).
- **13th / 14th month salary**: Required in many LATAM and European countries — common prospect question.
- **Probation periods**: Legally defined in most countries, can affect termination risk.
- **Notice periods**: Vary widely — Germany (up to 7 months), UK (1 week/year), US (at-will).
- **Severance**: Often legally mandated (e.g., France, Brazil, Mexico). {{COMPANY_NAME}} ensures compliant calculation.
- **Employer tax burden**: Often 20–35% on top of salary in EU; lower in APAC and parts of LATAM.

## Frequently Asked Countries

High-volume countries reps often ask about (prioritize finding docs for these):
- Germany, France, UK, Netherlands, Spain (Europe)
- Brazil, Mexico, Colombia, Argentina (LATAM)
- India, Singapore, Japan, Australia (APAC)
- Canada (North America)
- UAE (Middle East)

## Inputs
- `question_type` (enum: hiring / termination / payroll / employer-costs / benefits / compliance / probation / visa / working-hours, required)
- `country` (string) - fills the [country] slot in the search terms

## Outputs
- SharePoint-ready search terms with the country substituted
- Key-concept briefing for the topic (e.g. notice periods: Germany up to 7 months, UK 1 week/year, US at-will)

## Example
Input: a rep needs termination rules for Germany.
1. Type: termination; country: Germany.
2. Search terms: "termination Germany", "severance Germany", "notice period Germany", "redundancy Germany".
3. Concept briefing: notice up to 7 months, severance often mandated - Atlas ensures compliant calculation.

## Errors & edge cases
- Country omitted: give the general concept briefing and ask for the country before searching - EOR answers are jurisdiction-specific.
- Frequently asked countries (DE/FR/UK/Brazil/India...): prioritize those docs; others may need fresh sourcing.
