---
name: troubleshooting-template-skill
description: "The Troubleshooting & Lessons Report template -- the second required deliverable, showing judgment under friction: per-issue blocks (symptom, severity, root cause, fix, prevention), a forward-looking guardrail checklist, and a candid 'overall work entailed' section -- in full + redacted versions, secrets always described never shown. Use when working with troubleshooting report."
---

# Troubleshooting Report — Template

The second required deliverable. Its job is to show **judgment under friction** — that the
builder hit real problems, diagnosed them, fixed them, and learned how to prevent them. To a
hiring decision-maker, this is often more convincing than the polished case study, because
anyone can describe a success; diagnosing failure is what seniority looks like.

Keep the same name-then-translate discipline and the same two rules (two versions, no secrets).

Title format: **[Project name] — Troubleshooting & Lessons Report**

---

## 1. Summary
3–4 lines: how many issues were hit, their general nature (integration, data, logic,
performance, auth), and the headline lesson. Frame it as competence, not chaos:
*"Five issues surfaced during the build; each was isolated, fixed, and turned into a
safeguard so it can't recur."*

## 2. Issues & resolutions
One block per issue. Use a consistent structure — a table works well for scanning, prose
works well for depth. Recommended per-issue fields:

> **Issue [n]: [short name]**
> - **Symptom** — what the builder actually saw (the error, the wrong output, the silence).
> - **Severity** — blocker / major / minor; whether it stopped the project or just slowed it.
> - **Root cause** — the real underlying reason, in plain English (name-then-translate the tech).
> - **The fix** — what was changed to resolve it.
> - **Prevention** — what someone should do to stop this happening again (config, test, guardrail, doc).

Cover the common categories explicitly if the evidence shows them:
- **Auth / credentials** — expired tokens, wrong scopes, keys in the wrong place. (Describe; never print the key.)
- **Integration / API** — rate limits, schema mismatches, breaking changes, timeouts.
- **Data** — duplicates, bad formats, missing fields, encoding, volume/scale surprises.
- **Logic / prompt** — the AI or code doing the wrong thing; ambiguous instructions.
- **Orchestration** — steps firing out of order, race conditions, silent failures, no retries.

## 3. What would prevent these next time (forward-looking)
A consolidated checklist of guardrails and practices the issues revealed — the kind a team
could adopt. e.g., *"Store all credentials in a secret manager and rotate on a schedule,"
"Add a dedupe/idempotency check before any write,"  "Test against the live API's rate limits
early,"  "Add a dead-letter path so failed records aren't lost."* This shows the builder
thinks about reliability and maintainability, not just getting it working once.

## 4. Overall work entailed
A candid, confident summary of the **effort and skill the project actually took** — the part
the user explicitly wants captured. Convey scope without padding:
- The range of problems solved and disciplines touched (integration, data, AI, automation, debugging).
- The iteration: how many passes, what was rebuilt, what was learned mid-flight.
- The judgment calls: where experience (not just effort) made the difference.

This is the section that answers an executive's unspoken question: *"How hard was this, really,
and is this person good?"* Answer it honestly and well.

---

## Rendering notes
- Same four formats as the case study; same two versions (full + redacted).
- In the **redacted** version, scrub any client-identifying detail from symptoms and root
  causes (e.g., a client's data quirk becomes "the source CRM contained duplicate records").
- Secrets are **always** described, never shown — even in the full version. An expired token
  is "an expired private-app token," not the token string.

## Inputs

- `project_name` -- for the title: "[Project name] -- Troubleshooting & Lessons Report"
- `build_evidence` -- the issues actually hit: symptoms seen (errors, wrong outputs, silences), severities, root causes, fixes applied

## Outputs

- The report: 1. Summary (3-4 lines framing competence: issues isolated, fixed, turned into safeguards) -> 2. Issues & resolutions (per-issue: symptom, severity blocker/major/minor, root cause in plain English, the fix, prevention) -> 3. Forward-looking prevention checklist (guardrails a team could adopt) -> 4. Overall work entailed (candid scope/effort/judgment summary) -- same four formats as the case study, full + redacted versions

## Example

Five build issues (expired token, rate limits, duplicate records, ambiguous prompt, race condition): each gets symptom/severity/root-cause/fix/prevention -> checklist gains "store credentials in a secret manager", "add a dedupe check before any write", "add a dead-letter path" -> the effort section answers "how hard was this, really?" honestly.

## Errors & edge cases

- **Chaos framing** -- frame as competence, not chaos: every issue isolated, fixed, and converted to a safeguard.
- **Client detail in the redacted version** -- scrub identifying detail from symptoms and root causes (a client's data quirk becomes "the source CRM contained duplicate records").
- **Printed secrets** -- secrets are always described, never shown, even in the full version ("an expired private-app token", not the token).
