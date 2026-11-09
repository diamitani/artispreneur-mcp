---
name: pro-registration
title: Register Music with a PRO
agent: publishing-manager
version: 1.0.0
category: publishing
status: active
tools: [ascap-api, bmi-api, sesac-portal, supabase]
inputs: [track_title, isrc, writers, ownership_splits, publisher_info, pro_affiliation]
outputs: [pro_work_registration, registration_receipt, catalogue_entry_update]
guardrails:
  allow: [prepare registration payloads, store drafts and receipts in the vault]
  require_approval: [submit registration to the PRO]
  never: [alter ownership splits without written approval from all writers, submit under a false publisher name]
supersedes: null
extends: null
---

# Register Music with a PRO

## What it does
Takes a finished track — title, ISRC, writers, and agreed splits — and gets it registered with the artist's performing rights organization (ASCAP, BMI, or SESAC) so performance royalties can be collected. Every registration is stored with its receipt in the artist vault and linked to the track's catalogue entry.

## When to use
- A new single, EP, or album is finished and has an ISRC.
- An older released track was never registered (found via the unclaimed-track audit).
- The artist switches PROs and the catalogue needs re-registration.
- A collaboration's split sheet is finalized and all writers have approved.

## Inputs
- `track_title` (required): official title exactly as released.
- `isrc` (required): valid ISRC, e.g. US-MR3-26-00001.
- `writers` (required): list of legal names +IPI/CAE numbers where known.
- `ownership_splits` (required): percentages summing to 100, matching the signed split sheet.
- `publisher_info` (optional): publisher name and affiliation; omit for self-published.
- `pro_affiliation` (required): ascAP | bmi | sesac — must match the artist's current affiliation.

## Procedure
1. Validate inputs: ISRC format, splits sum to 100, every writer has a legal name.
2. Pull the matching split sheet from the vault; if none exists or splits differ, STOP and route to `split-sheet-generator` first.
3. Check the catalogue entry for this ISRC; flag if a registration already exists (avoid duplicates).
4. Build the PRO-specific registration payload (each PRO's fields differ — use the field map in `docs/pro-field-maps.md`).
5. Present the completed registration to the artist for review with a plain-language summary: what is being claimed, by whom, at what splits.
6. On artist approval, submit via the PRO's API or guided portal flow.
7. Store the confirmation/receipt in the vault under `publishing/registrations/<isrc>/`.
8. Update the catalogue entry: set `pro_registered=true`, attach registration ID and date.

## Outputs
- `pro_work_registration`: the submitted registration record (PRO work ID).
- `registration_receipt`: confirmation PDF/screenshot stored in the vault.
- Updated catalogue entry with registration metadata.

## Guardrails
May prepare payloads and store drafts and receipts. May never submit to a PRO without the artist's explicit review and tap. May never alter ownership splits — any change requires a new signed split sheet from all writers. This skill handles administration only; it is not legal advice.

## Example
Artist: Maya Reyes (BMI-affiliated, self-published). Track: "Neon Static", ISRC US-MR3-26-00042, sole writer at 100%.
Input validated, no existing registration found, payload built for BMI's work registration, Maya reviews and taps approve. Submitted; BMI work ID 12345678 stored in `publishing/registrations/US-MR3-26-00042/`; catalogue entry updated. Royalties from radio, live performance, and streaming performance pools can now flow.
