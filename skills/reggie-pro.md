---
name: reggie-pro
description: "PRO registration guide (ASCAP/BMI/SESAC): walks artists through enrollment, song metadata organization (ISRC/IPI/splits), royalty monitoring, and portfolio maintenance. Use when helping artists register for Performance Rights Organizations (ASCAP, BMI, SESAC) and manage music portfolios."
---

# Reggie Pro

Guide independent artists through Performance Rights Organization (PRO) registration and portfolio management. Covers ASCAP, BMI, and SESAC — the three major U.S. PROs that collect and distribute performance royalties.

## Workflow

1. Identify the artist's needs: new registration, catalog management, or PRO comparison.
2. Walk through the selected PRO's registration process step by step.
3. Help organize song metadata: ISRCs, IPI numbers, publisher splits, and co-writer info.
4. Advise on royalty collection setup and monitoring.
5. Provide guidance on portfolio maintenance — adding new works, updating splits, and tracking payments.

## Key Considerations

- ASCAP and BMI are open-enrollment; SESAC is invitation-only.
- Artists can only join one PRO as a writer but can have publisher affiliations with others.
- Accurate metadata is critical for proper royalty collection.
- International royalty collection may require additional steps with foreign PROs.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `need` | enum | required | `register` (first-time) | `compare` (which PRO) | `manage` (catalog upkeep) |
| `catalog` | string | -- | Works with ISRCs, co-writer splits, publisher info. |
| `publisher_status` | enum | `none` | `none` | `self-published` | `has-publisher` |

## Outputs

- **Deliverable:** a step-by-step registration walkthrough, a PRO comparison, or a portfolio action list (add works, update splits, track payments).
- **Format:** numbered steps with the exact info to have on hand.

## Example

> "First-time songwriter, 6 songs, no publisher -- ASCAP or BMI?"

1. Compare: both open-enrollment; BMI free for songwriters, ASCAP has a one-time fee; both collect the same performance royalties.
2. Walk through the chosen PRO's signup: writer profile, then register each work (title, ISRC, writers + split %, publisher or self-published).
3. Set up royalty monitoring: quarterly statements, cue-sheet follow-ups for any TV/film placements.

## Errors & edge cases

- Already affiliated as a writer with one PRO -> cannot join a second as a writer (publisher affiliations are separate).
- SESAC is invitation-only -> don't promise access; compare ASCAP/BMI honestly.
- Foreign performances -> international collection needs extra steps with foreign PROs; flag it.
- Inaccurate metadata = unpaid royalties; verify ISRCs, IPIs, and splits before filing.
