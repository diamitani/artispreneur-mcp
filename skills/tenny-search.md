---
name: tenny-search
description: "Saves apartment listing links and parses them into organized, comparable CSVs -- extracts price, beds, baths, sqft, address, amenities, and contact info from Zillow, Apartments.com, Craigslist, or raw pasted text, normalizes the values, and highlights the best-value options. Use when saving apartment listing links and parsing them into organized CSV format."
---

# Tenny Search

## Overview
Saves apartment listing links and parses them into organized CSV format. Structures real estate data for easy comparison, helping renters and buyers evaluate properties side by side.

## When to Use
- Collecting apartment listings from Zillow, Apartments.com, Craigslist, etc.
- Parsing listing details into structured fields for comparison
- Exporting property data to CSV for spreadsheet analysis
- Tracking listing prices and availability over time
- Comparing rental properties by price, sqft, amenities, location

## How It Works
Accepts apartment listing URLs or raw listing text. Extracts structured data points (price, beds, baths, sqft, address, amenities, contact info). Outputs a clean CSV for sorting and comparison.

## Steps
1. Accept listing URLs or copy-pasted listing text
2. Parse each listing to extract: price, beds, baths, sqft, address, neighborhood, amenities, lease terms, contact info, source URL
3. Normalize values: consistent price format, standardized amenities, deduplication
4. Structure into CSV with consistent column headers
5. Highlight best value options based on user criteria
6. Export CSV file for further analysis

## Common Pitfalls
- Parsing errors from inconsistent listing formats across sites
- Missing critical fields like application fees or pet policies
- Not updating listings — prices and availability change quickly
- Mixing different property types (studio vs house) in the same dataset
- Assuming amenities are included when they're actually add-ons

## Inputs

- `listings` -- apartment listing URLs (Zillow, Apartments.com, Craigslist, etc.) or copy-pasted listing text
- `criteria` -- the renter's/buyer's priorities for best-value highlighting (price ceiling, beds, neighborhood, must-have amenities)

## Outputs

- A clean CSV with consistent column headers (price, beds, baths, sqft, address, neighborhood, amenities, lease terms, contact info, source URL), normalized values (consistent price format, standardized amenities, deduplicated), with best-value options highlighted against the criteria

## Example

12 listings across Zillow and Craigslist: parsed to price/beds/baths/sqft/address/amenities, normalized ($1,850/mo, "in-unit laundry" standardized), deduplicated (3 cross-posted), CSV exported -- the $1,650 2-bed near transit highlighted as best value under the $1,700 ceiling.

## Errors & edge cases

- **Inconsistent listing formats** -- parsing errors across sites; verify extracted fields per listing.
- **Missing critical fields** -- application fees and pet policies are often absent; flag them as unknown, don't assume.
- **Stale listings** -- prices and availability change quickly; re-check before acting.
- **Mixed property types** -- don't mix studios and houses in one comparison set.
- **Assumed amenities** -- verify inclusions; amenities are often add-ons, not included.
