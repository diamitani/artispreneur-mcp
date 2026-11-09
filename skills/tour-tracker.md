---
name: tour-tracker
description: "Tour planner for independents: route building, venue research with deal structures, logistics (transport/lodging/backline/riders), budget templates, and local support plus promotion per market. Use when discovering live music tours, booking venues, and planning tour logistics."
---

# Tour Tracker

Help independent artists discover touring opportunities, book venues, and plan tour logistics. Cover everything from route planning to advancing shows and managing budgets.

## Workflow

1. Define the tour scope: geography, date range, budget, and band size.
2. Research suitable venues in target cities based on capacity, genre fit, and reputation.
3. Build a tour route with logical city ordering to minimize travel costs.
4. Provide venue contact information, booking procedures, and typical deal structures (door deal, guarantee, percentage).
5. Advise on logistics: transportation, lodging, load-in/load-out, backline, and hospitality riders.
6. Create a tour budget template covering guarantees, merch projections, travel, lodging, food, and emergency funds.
7. Suggest local support acts and promotional strategies for each market.

## Key Considerations

- Start with smaller regional runs before attempting national tours.
- Build relationships with local promoters and venue bookers — personal connections matter.
- Always have contracts or email confirmations before hitting the road.
- Factor in rest days to prevent burnout.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `region` | string | required | e.g. "Midwest", "Texas triangle", "West Coast". |
| `date_range` | string | required | e.g. "2026-11-01..2026-11-14". |
| `budget` | string | -- | Total tour budget. |
| `band_size` | integer | `1` | Traveling personnel count. |
| `draw_estimate` | string | -- | Expected draw per market (drives guarantee vs. door-deal calls). |

## Outputs

- **Deliverable:** a route (logical city order), venue shortlist with contacts + deal structures, logistics checklist, and a budget template.
- **Format:** structured plan: route map, per-city sheet, budget table.

## Example

> "5-city Midwest run, 3-piece, $3k budget, November."

1. Route: Chicago -> Milwaukee -> Madison -> Minneapolis -> Des Moines (no backtracking; rest day after night 3).
2. Venues: 100-200 cap rooms matching genre; booker contacts, typical deals (door vs. guarantee at this draw), load-in/backline notes.
3. Logistics: van rental vs. personal vehicles, lodging (band crash network + 2 hotel nights), hospitality rider minimums.
4. Budget: guarantees + merch projections vs. travel/lodging/food + 10% emergency fund.
5. Per market: 1-2 local support acts + a promo checklist (local press, posters, social geo-targeting).

## Errors & edge cases

- Routing zigzags across the map -> reorder by geography; drive time is money.
- No confirmed deals, only "maybes" -> don't hit the road on promises; get email confirmations first.
- Skipping rest days -> burnout by night 6; schedule them.
- Start with regional runs before attempting national tours.
