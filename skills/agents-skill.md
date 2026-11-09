---
name: agents-skill
description: "Delali Development Cycle planning harness: a gated, stage-by-stage runtime for website/app/store/funnel builds -- PAL intake, one artifact per turn, education mode on by default, and a hard build_eligible gate before any scaffolding or deploys. Use when working with agents.md."
---

# AGENTS.md — Delali Planning Runtime

You are running inside the Delali Development Cycle Planning Harness.

On any request to build, redesign, or specify a website, app, store, funnel, portfolio, directory, chat product, or SaaS:

1. Do not wait for a special prompt.
2. Load the bundled `ddc-planning-harness.md`. If the `skill-ddc-plan-skill`
   skill is installed in your skill library, load it too.
3. Create or resume a run following the runtime rules in `ddc-planning-harness.md`.
4. Walk stages in order. One artifact per turn. One question if blocked.
5. `education_mode` defaults true: teach in simple language, then write the executive doc.
6. Do not scaffold or deploy until `build_eligible` is true.
7. PAL: Parse, Ambiguity Scan, Latent Intent, Expand, Compile.
8. ROSTR: intent → evidence → JTBD → NPAO → documentation → architecture → GTM → taste → quality.

Forbidden: secrets in git, skipping gates, production side effects without approval.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `request` | string | required | The build/redesign/specify request (website, app, store, funnel, portfolio, directory, chat product, or SaaS). |
| `harness_doc` | path | bundled `ddc-planning-harness.md` | The runtime rules document to load. |
| `companion_skill` | string | -- | `skill-ddc-plan-skill`, loaded too when installed in the skill library. |

## Outputs

- **Deliverable:** staged planning artifacts, one per turn, ending in an executive document -- code/scaffolding only after `build_eligible` is true.
- **Format:** chat walkthrough following the harness stage order.

## Example

> "Redesign my portfolio site."

1. Load the bundled `ddc-planning-harness.md` (plus `skill-ddc-plan-skill` if installed).
2. Create or resume a run; walk stages in order -- PAL intake, then one artifact per turn, one clarifying question max when blocked.
3. `education_mode` on: teach the concept in simple language, then write the executive doc. No scaffolding until the `build_eligible` gate passes.

## Errors & edge cases

- Harness doc missing -> cannot run the runtime; say so instead of improvising stages.
- Companion skill not installed -> continue with the bundled harness doc alone.
- Asked to scaffold/deploy before `build_eligible` -> refuse and keep walking the stages; production side effects always need approval.
- Secrets in git or skipped gates -> forbidden by the runtime, no exceptions.
