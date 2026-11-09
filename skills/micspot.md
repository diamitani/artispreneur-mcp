---
name: micspot
description: "Open-mic finder for musicians and comedians: venue, day/time, sign-up method, crowd vibe, backline, and cost -- filtered by genre and experience level. Use when finding open mics in any area for comedy and music."
---

# MicSpot

Help artists and comedians discover open mic opportunities in any location. Find venues, sign-up procedures, crowd vibes, and time slots so performers can get on stage.

## Workflow

1. Determine the user's location or target area.
2. Search for open mic listings across directories (Open Mic Finder, local event boards, social media, venue websites).
3. Compile relevant results with: venue name, address, day/time, sign-up process, genre focus, and any cost.
4. Highlight notable details: typical crowd size, backline provided, recording/performing rights, and community reputation.
5. Present organized results with recommendations based on the artist's genre and experience level.

## Key Considerations

- Open mics vary widely in quality and format — note whether it's music-only, comedy-friendly, or mixed.
- Sign-up methods differ: online pre-registration, first-come-first-served, or lottery.
- Encourage artists to visit as an audience member first to gauge fit.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `location` | string | required | City/neighborhood or "near <address>". |
| `art_type` | enum | `music` | `music` | `comedy` | `mixed` |
| `experience_level` | enum | `any` | `beginner` | `intermediate` | `pro` |
| `max_distance` | string | -- | e.g. "10 miles" / "30 min transit". |

## Outputs

- **Deliverable:** an organized venue list -- name, address, day/time, sign-up process, genre focus, cost, crowd vibe, backline -- with picks matched to genre + experience.
- **Format:** chat list, best fits first.

## Example

> "Open mics in Austin for a beginner folk singer."

1. Search open-mic directories, venue sites, local boards, socials.
2. Return 5: two music-only rooms with real listening crowds, one mixed room (comedy-heavy -- flagged), one lottery sign-up (arrive 1 hr early), one $5 cover with full backline.
3. Recommend: visit the top pick as an audience member first; bring a friend to the lottery one.

## Errors & edge cases

- No listings found -> widen the radius, check Instagram/Facebook event posts (many mics are social-only).
- Venue permanently closed -> verify day-of before publishing the list; mics die quietly.
- Music-only vs. comedy-friendly mismatch -> always label the format; a comic at a songwriter circle (or vice versa) is a wasted night.
