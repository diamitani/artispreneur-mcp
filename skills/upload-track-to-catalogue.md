---
name: upload-track-to-catalogue
description: "Adds a track to the catalogue as a vault master with provenance -- attaches file + metadata, sets Ready/Pending status, writes the Supabase catalogue row -- delivering catalogue-row.md. Use when the user wants to upload track to catalogue."
---

# Upload Track to Catalogue

- **Subagent:** @distribution-agent
- **Category:** Catalogue
- **NPAO:** N
- **List price:** $9
- **Source:** Catalogue

## When to use
Vault master with provenance.

## Steps
1. Attach file+metadata
2. status Ready/Pending
3. write mcp__supabase catalogue row

## Outputs
catalogue-row.md

## Reference tools
- mcp__supabase

## Guardrails
Version bump, no silent overwrite.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `track` + `metadata` -- the audio file and its metadata
- `status` -- Ready or Pending

## Example

A final master + metadata -> status Ready -> catalogue row written to mcp__supabase -> catalogue-row.md records the vault master with provenance.

## Errors & edge cases

- **Silent overwrites** -- version bump instead (guardrail); never silently replace a catalogue entry.
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
