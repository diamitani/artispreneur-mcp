---
name: register-with-pro
description: "Walks an artist or company through P.R.O. signup -- picks ONE compositional PRO (BMI/ASCAP/SESAC), creates the writer account, opens SoundExchange for the recording side, and adds the publisher after the LLC exists -- delivering pro-picker.md. Use when the user wants to register with a p.r.o."
---

# Register with a P.R.O.

- **Subagent:** @pro-agent
- **Category:** Publishing
- **NPAO:** N
- **List price:** $15
- **Source:** How To Register with a Performing Rights Organization.docx

## When to use
Artist/company PRO signup.

## Steps
1. Pick ONE compositional PRO
2. Create writer account
3. Open SoundExchange
4. Add publisher after LLC

## Outputs
pro-picker.md

## Reference tools
- https://www.bmi.com
- https://www.ascap.com
- https://www.sesac.com
- https://www.soundexchange.com
- mcp__supabase

## Guardrails
No dual-register.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs

- `entity` -- the artist or company signing up; the publisher entity requires an existing LLC
- `pro_choice` -- exactly one of BMI, ASCAP, or SESAC (compositional side); SoundExchange covers the recording side

## Example

A solo artist picks ASCAP -> writer account created -> SoundExchange opened for digital performance royalties -> publisher account added after the LLC is formed -> pro-picker.md records the choices.

## Errors & edge cases

- **Dual registration** -- never register with two compositional PROs; pick exactly one.
- **Publisher before LLC** -- add the publisher only after the legal entity exists.
- **Dependent capability missing** -- name it and stop; the parent handoff summarizes artifacts + blockers.
