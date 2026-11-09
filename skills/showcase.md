---
name: showcase
description: "Live-event producer for open mics, showcases, and release parties: venue, lineup, production, promotion, budget, and day-of run-of-show. Use when planning open mics, showcases, or release parties for artists."
---

# Showcase

Plan and execute open mics, showcases, and release parties for independent artists. Cover every detail from venue selection to promotion and day-of production.

## Workflow

1. Define the event type and goals: open mic (community building), showcase (industry exposure), or release party (fan celebration).
2. Select and secure a venue: capacity, sound system, stage setup, bar/payment terms, and date availability.
3. Curate the lineup: headliner, supporting acts, and host/MC. Balance genre, draw, and set lengths.
4. Plan production: sound engineer, backline, lighting, stage plot, load-in schedule, and soundcheck times.
5. Develop a promotional strategy: flyer design, social media campaign, press outreach, email blast, and ticket/RSVP setup.
6. Manage budget: venue cost, production expenses, artist compensation, and projected revenue (tickets, bar percentage, merch).
7. Execute day-of operations: run of show, stage management, door/guest list, merch table, and content capture.

## Key Considerations

- Start small — a packed 100-cap room beats an empty 300-cap room.
- Clear communication with venue staff and artists prevents day-of chaos.
- Capture content (photos, video) for future promotion.
- Build community around the event, not just attendance.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `event_type` | enum | required | `open_mic` (community) | `showcase` (industry exposure) | `release_party` (fan celebration) |
| `city` | string | required | Market for venue sourcing. |
| `date` | string | -- | Target date or window. |
| `capacity_target` | integer | -- | e.g. 100. |
| `budget` | string | -- | Total budget or range. |

## Outputs

- **Deliverable:** a full event plan -- venue shortlist, lineup, production checklist, promo plan, budget, and day-of run-of-show.
- **Format:** structured plan document in chat.

## Example

> "Release party, Chicago, 100-cap, $2k budget, November."

1. Venue: 100-150 cap rooms with in-house PA; negotiate bar percentage vs. rental.
2. Lineup: headliner (the artist), 2 supporting acts with complementary draw, host/MC; set lengths + changeovers mapped.
3. Production: sound engineer, backline, stage plot, load-in/soundcheck schedule.
4. Promo (4 weeks): flyer, social campaign, press outreach to local blogs, email blast, RSVP/ticket link.
5. Budget: venue, production, artist comp vs. projected tickets/bar/merch.
6. Day-of: run-of-show, door/guest list, merch table, content capture (photo/video for future promo).

## Errors & edge cases

- Budget too small for the room -> downsize capacity; a packed 100-cap beats an empty 300-cap.
- No sound engineer in budget -> only book venues with in-house engineers.
- Lineup overruns -> enforce set lengths in writing with every act.
- Capture content or the event never happened (for promo purposes).
