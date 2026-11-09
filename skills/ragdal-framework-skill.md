---
name: ragdal-framework-skill
description: "Runs pre-PRD knowledge enrichment through a unified RAG DAL query interface -- adapter-notated retrieval (rag_dal.web_search / web_fetch / knowledge_base / crm_query), domain-taxonomy query clusters per project type, and a tiered source-credibility strategy, written into the KB as '11. RAG Enrichment Layer'. Use when enriching a project knowledge base before PRD/JTBD generation."
---

# RAG DAL — Retrieval / Data Abstraction Layer

**Canonical source:** https://rostr-paper.vercel.app/#s5
*Read this file before running enrichment. Fetch the live section only if a definition is still unclear.*

RAG DAL is the **unified query interface** the system uses to enrich a project's knowledge base before the PRD and JTBD plan are generated — so every output reflects current standards, not just what the user already knew. Tools are referenced with **adapter notation**: `rag_dal.web_search`, `rag_dal.web_fetch`, `rag_dal.knowledge_base`, `rag_dal.crm_query`.

**Guiding principle: pursue completeness, not adequacy.** Stop when the topic is genuinely covered, not when you have "enough to write something."

---

## Adapters

| Adapter | Use for |
|---|---|
| `rag_dal.web_search` | Best-practice claims, tool comparisons, process standards, API docs |
| `rag_dal.web_fetch` | Scraping a specific user-supplied URL into the KB |
| `rag_dal.knowledge_base` | Querying past project KBs for reuse / similar prior work |
| `rag_dal.crm_query` | Pulling HubSpot deal/contact/company context when relevant |

---

## Domain taxonomy map (project type → precision search clusters)

Generic search returns noise; domain-specific queries return signal. Map the project type (Q1.2) to a query cluster:

| Project type | Primary queries | Fallback |
|---|---|---|
| Outbound / SDR system | "outbound SDR automation best practices 2026" · "AI SDR tech stack Clay HubSpot Amplemarket" | "B2B prospecting automation workflow" |
| EOR / global hiring | "Employer of Record compliance automation workflow" · "global payroll integration API best practices" | "HR tech automation EOR onboarding" |
| CRM / RevOps | "HubSpot workflow automation best practices RevOps" · "CRM data hygiene automation" | "RevOps tech stack automation 2026" |
| Content / marketing | "AI content generation workflow marketing automation" · "B2B content pipeline tools" | "marketing AI automation best practices" |
| Reporting / dashboard | "GTM reporting dashboard best practices KPI framework" · "sales pipeline reporting automation" | "revenue reporting automation tools" |
| AI agent / skill build | "[domain] AI agent design pattern" · "LLM agent tool use best practices" | "AI automation project best practices [domain]" |
| General / unknown | "AI automation project best practices [extracted_domain]" | "software project planning best practices [extracted_domain]" |

---

## Source tier strategy

| Tier | Sources | Trust weight | Use for |
|---|---|---|---|
| **Tier 1 — high credibility** (query first) | Industry reports (Gartner, Forrester), vendor official docs, G2 category guides, practitioner LinkedIn articles | 1.0 | Best-practice claims, tool comparisons, process standards |
| **Tier 2 — mid credibility** (cross-reference) | Tech blogs (HubSpot, Outreach, Clay, n8n docs), verified news, company case studies | 0.7 | Implementation detail, tool-specific guidance, workflow examples |
| **Tier 3 — user-generated** (trend signal only) | Reddit, LinkedIn posts, X threads, forums | 0.3 | Emerging trends, common pain points, tooling opinions — flag as "community signal, not verified" |

---

## Retrieval loop

- **Stop condition:** 3+ Tier 1/2 sources retrieved with relevant content, OR 5 search iterations completed (whichever first).
- **Max iterations:** 5.
- **Cache:** enrichment results cached per project-type for 30 days; same type reuses prior search, new types run fresh.

---

## Internal sources ({{COMPANY_NAME}}-specific — always include)

- `CLAUDE.md` — {{COMPANY_NAME}} ICP, value props, competitive positioning.
- Project instructions — PRD template, output schemas.
- Past project KBs via `rag_dal.knowledge_base` — surface similar prior projects as additional context (reuse detection).

---

## Output

Write enrichment into the KB under `## 11. RAG Enrichment Layer`:
```
## 11. RAG Enrichment Layer
### Best practices (3–5, relevant to this project type)
  - [practice] — [Tier 1 | Tier 2 | Community Signal] — [URL]
### Recommended tools/platforms not already in the user's stack
  - [tool] — [why it fits] — [Tier] — [URL]
### Common failure modes / what to avoid
  - [failure mode] — [source]
```

Every claim is labeled with its tier. This block is the difference between a generic plan and one that reflects how the best teams actually do this work.

## Inputs

- `project_type` (from Q1.2) -- mapped to a domain taxonomy query cluster: Outbound/SDR, EOR, CRM/RevOps, Content, Reporting, AI agent, or General/unknown
- `adapters` -- one or more of `rag_dal.web_search` (best-practice claims), `rag_dal.web_fetch` (user-supplied URL), `rag_dal.knowledge_base` (past project KBs), `rag_dal.crm_query` (HubSpot deal/contact/company context)
- `stop_condition` -- 3+ Tier 1/2 sources retrieved with relevant content, OR 5 search iterations, whichever first; enrichment results cached per project-type for 30 days

## Outputs

- A `## 11. RAG Enrichment Layer` KB block: 3-5 tier-labeled best practices with URLs, recommended tools/platforms not already in the user's stack, and common failure modes -- every claim labeled Tier 1 (1.0), Tier 2 (0.7), or Community Signal (0.3). This block is what separates a generic plan from one reflecting how the best teams actually do the work.

## Example

An Outbound/SDR-system project maps to the cluster "outbound SDR automation best practices 2026" / "AI SDR tech stack Clay HubSpot Amplemarket". After 3 Tier-1/2 hits the loop stops and the KB gains 4 best practices, 2 recommended tools, and 3 failure modes, each tier-labeled with its source URL.

## Errors & edge cases

- **Generic search returns noise** -- always map the project type to a domain cluster first; generic queries are the fallback, not the start.
- **Stop condition never met** -- hard cap at 5 iterations; the guiding principle is "pursue completeness, not adequacy".
- **Tier-3 sources treated as verified** -- Reddit/LinkedIn/X threads are trend signal only; flag them "community signal, not verified".
- **Stale internal context** -- always include company-specific sources: CLAUDE.md, project instructions (PRD template, output schemas), and past project KBs via `rag_dal.knowledge_base`.
