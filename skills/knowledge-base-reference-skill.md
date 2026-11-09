---
name: knowledge-base-reference-skill
description: "Reference guide to a 582-fact, five-tab master knowledge base — company-wide knowledge, 436 country-specific facts across 51 countries, the Onspring-confirmed high-confidence subset, a country index, and a 226-document index — with retrieval priority rules (Tab 3 first), a fact-adding workflow, owner/review-status distributions, and known gaps. Use when working with [company name] master knowledge base."
---

# [Your Company Name] Master Knowledge Base — Reference Guide

Last updated: 2026-03-26
Version: 1.0 (post-ingestion, 582 facts)

---

## Active Knowledge Base File

**File name:** the user-supplied RFP workbook (a dated .xlsx such as the March 2026 export — not bundled with this skill; the user provides their copy)
**Location:** the user's workspace folder, in their RFP Builder Skill folder
**Total facts:** 582 (per the user's workbook — not a universal figure)
**Countries covered:** 51 (per the user's workbook)
**Source documents ingested:** 226 (per the user's workbook)

When a user does not provide their own KB file, reference this as the current master KB. Ask the user to upload it, or confirm it is already in the workspace.

---

## KB Structure — Five Tabs

### Tab 1: [Your Company Name] Knowledge (146 facts)
General [Your Company Name]-wide facts that apply across all geographies. Covers:
- EOR model and direct-entity structure (no third-party aggregators)
- Platform capabilities (HXM platform, integrations, APIs)
- Security and compliance certifications (SOC 2, ISO 27001, GDPR)
- Service offering breadth (EOR, payroll, benefits, HCM, VGM, HR outsourcing)
- Onboarding and implementation timelines
- SLA commitments
- Pricing and billing model

### Tab 2: Country-Specific Knowledge (436 facts, 51 countries)
Facts scoped to a specific country or region. Each row includes:
- `Country` column — the applicable country name
- `Knowledge Type` = "Country-Specific Knowledge"
- Full Q/A pair, source, owner, review status

Countries with the most facts: Bangladesh, Germany, Philippines, Brazil, India, UK, France, Canada, Australia, Mexico.

### Tab 3: Onspring-Confirmed (213 facts)
Subset of all facts where `Review Status = confirmed` and `Onspring Ready = TRUE`. These are the highest-confidence facts in the KB — verified through Onspring, Azure Blob approved sources, or formal RFP responses. Use these as the authoritative reference when a HIGH confidence answer is needed.

Source collections that feed this tab:
- Azure Blob Storage (approved facts from UniFirst, Citi, Sophos, Pinnacle Group RFPs)
- Onspring country data export (28 countries, full entity + benefits data)

### Tab 4: Country Index (51 countries)
Quick reference table — one row per country. Columns:
- Country name
- Entity name (e.g., "[Your Company Name] Bangladesh Pvt Ltd.")
- Operates as EOR (Y/N)
- Can sponsor work permits (Y/N)
- General and country-specific fact counts

### Tab 5: Document Index (226 documents)
Full catalog of all source documents ingested into the KB. Columns:
- Document name, category, format, country (or "Global"), source collection

---

## Source Collections — What Was Ingested

| Collection | Doc Count | Description |
|---|---|---|
| RFP Source Documents | 32 | Formal RFP/questionnaire files: Schaeffler, IPPF, Bangladesh, UniFirst, Citi, Sophos, Pinnacle Group |
| Country Summaries | 18 | Country-level PDF summaries — EOR terms, payroll, benefits, local law |
| Policies & Certifications | 24 | SOC 2, ISO 27001, SLA docs, privacy policies, DPAs |
| Case Studies & Reports | 19 | Customer stories, EOR market reports |
| Benefits Documentation | 14 | [Your Company Name] benefit plan docs, flex benefit guides by country |
| Approved Facts (Azure Blob) | 66 | Onspring-approved Q/A facts from live RFP responses (ptsalesgtmstorage / sales-enablement) |
| Country Data (Onspring) | 53 | Structured entity records for 28 countries from Onspring system |

---

## Fact Distribution by Owner

| Owner | Count | Topics |
|---|---|---|
| HRSD | 262 | HR processes, employment terms, benefits, offboarding, local compliance |
| Finance | 134 | Payroll, billing, FX, deposit requirements, invoicing, fees |
| Product | 97 | Platform capabilities, integrations, APIs, certifications, security |
| Implementation | 46 | Onboarding timelines, go-live, CSM model |
| Other | 40 | Legal/contract terms, cross-functional |
| VGM | 3 | Visa, work permits, immigration (expand with dedicated VGM sources) |

---

## Review Status Distribution

| Status | Count | Meaning |
|---|---|---|
| confirmed | 213 | Verified against Onspring or approved source — highest confidence |
| new | 350 | Extracted from RFP/source, not yet formally verified |
| unreviewed | 19 | Flagged for review — potential conflict or ambiguity |

---

## How to Reference the KB in Skill Workflows

### Skill #1 — Adding new facts:
1. Compare new extractions against Tab 1 and Tab 2 first
2. Check Tab 3 (Onspring-Confirmed) for authoritative confirmed answers on the same topic
3. Record the exact source document name matching Tab 5 entries where possible
4. When saving new facts, merge into the master KB and update the date stamp

### Skill #2 — Retrieving answers:
1. **Prioritize Tab 3 (Onspring-Confirmed)** — highest confidence, use for HIGH confidence answers
2. Fall back to **Tab 2** (Country-Specific Knowledge) for geographic questions
3. Fall back to **Tab 1** ([Your Company Name] Knowledge) for general questions
4. Skip any fact with `Review Status = unreviewed` or `Conflict Flag ≠ ""` — create HubSpot ticket instead

---

## Known Gaps / Areas for Expansion

- **VGM:** Only 3 facts — significantly underrepresented. Ingest [Your Company Name] visa/immigration policy documents.
- **Country name normalization:** Minor variant spellings exist (Côte d'Ivoire variants, Trinidad & Tobago). Tab 4 uses canonical forms.
- **Phase 2 — Onspring write-back:** Facts with `onspring_ready = TRUE` are ready for Onspring API upload (not yet implemented in v1 skill).
- **Azure Blob live sync:** Currently ingested via manual zip download. Phase 2 will add direct Blob SDK integration.

## Inputs

- `kb_file` (required, user-supplied) — the RFP workbook (a dated .xlsx, e.g. the March 2026 export); not bundled with this skill — ask the user to upload it or confirm it is in their workspace/RFP Builder Skill folder
- `question` + geography scope — routes retrieval: HIGH-confidence needs → Tab 3; country questions → Tab 2; general → Tab 1
- `new_facts` (when adding) — compared against Tabs 1–2 first, checked against Tab 3 for authoritative conflicts, source document matched to Tab 5 entries

## Outputs

- Answers with retrieval priority: **Tab 3 (Onspring-Confirmed, 213 facts)** first for HIGH confidence → Tab 2 (country-specific, 436 facts / 51 countries) → Tab 1 (company-wide, 146 facts); Tab 4 (country index: entity, EOR Y/N, work-permit sponsorship) for quick reference; Tab 5 (226 source documents) for provenance
- New facts merged into the master KB with the date stamp updated
- Format: cited answers naming the source document; facts carry owner (HRSD 262, Finance 134, Product 97, Implementation 46, Other 40, VGM 3) and review status (confirmed 213 / new 350 / unreviewed 19)

## Example

Q: ‘Does [Company] sponsor work permits in Germany?’ → check Tab 3 (Onspring-Confirmed) first for a HIGH-confidence answer with source; fall back to Tab 2 Germany rows; Tab 4 gives the entity name and EOR flag. Adding a fact: a new Sophos RFP extraction is compared against Tabs 1–2, checked against Tab 3 for conflicts on the same topic, its source document matched to a Tab 5 entry, then merged into the master KB with the date stamp updated.

## Errors & edge cases

- **No KB file provided:** the workbook is user-supplied, not bundled — ask the user to upload it or confirm it is already in the workspace before answering from it.
- **Skip unreviewed or conflict-flagged facts** (`Review Status = unreviewed`, `Conflict Flag ≠ ""`) — create a HubSpot ticket instead of answering from them.
- **VGM questions:** only 3 facts exist — flag the gap rather than answering thinly; ingest visa/immigration policy docs to expand.
- **Country-name variants** (Côte d'Ivoire spellings, Trinidad & Tobago) — use the Tab 4 canonical forms.
- **Phase 2 items are not implemented** (Onspring write-back of `onspring_ready` facts, Azure Blob live sync) — don't promise them; current ingestion is manual zip download.
