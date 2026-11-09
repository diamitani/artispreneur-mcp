---
name: venyou
description: "Venue contact database builder: researches venues by market, captures booking contacts and submission preferences, and organizes them into a follow-up-ready tracker. Use when finding and organizing music venue contact information."
---

# VenYou

Find and organize music venue contact information for independent artists. Build venue databases with booking contacts, capacity details, and submission preferences.

## Workflow

1. Identify target cities, regions, or venue types the artist wants to play.
2. Research venues: capacity, genre focus, typical crowd, and reputation among artists.
3. Locate booking contact information: email, phone, contact person, and preferred submission method (email, form, EPK portal).
4. Note venue specifics: PA system quality, backline provided, stage dimensions, green room, and load-in access.
5. Organize findings in a structured format (spreadsheet, database, or CRM-ready export) with fields for contact date, follow-up status, and show history.

## Key Considerations

- Booking contacts change frequently — verify before reaching out.
- Respect submission preferences; unsolicited calls can hurt more than help.
- Organize by market so artists can quickly see who they know in each city.
- Track follow-ups: persistence pays off but don't be a nuisance.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `markets` | string[] | required | Cities/regions, e.g. `["Chicago", "Milwaukee"]`. |
| `venue_types` | string[] | -- | e.g. clubs, theaters, DIY spaces, festivals. |
| `capacity_range` | string | -- | e.g. "100-300". |
| `genre_fit` | string | -- | e.g. "indie rock", "hip-hop", "jazz". |

## Outputs

- **Deliverable:** a structured venue database -- name, market, capacity, genre focus, booking contact (name/email/phone), submission preference, PA/backline notes, plus follow-up tracking fields (contact date, status, show history).
- **Format:** table/CSV-ready; CRM-importable on request.

## Example

> "Indie rooms in Chicago, 100-300 cap."

1. Research 12 venues: capacity, genre focus, reputation among artists.
2. Capture booker emails + preferred submission method (email vs. EPK portal vs. form); note PA quality, backline, stage size, load-in access.
3. Organize by market with follow-up columns; flag the 3 with the warmest reputation for first outreach.

## Errors & edge cases

- Booking contacts change frequently -> verify every contact before a campaign goes out.
- Venue prefers portal submissions -> respect it; unsolicited calls hurt more than help.
- No booker listed -> call the venue's general line once, then log the result.
- Track follow-ups: persistent but not a nuisance; log every touch.
