---
name: auctopilot
description: "LLM-agnostic sales prospecting and go-to-market skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to discover local buying opportunities - real estate auctions, foreclosures, estate sales, vehicle and equipment auctions, tax liens and sheriff's sales - aggregated from auction platforms, government sites, and classifieds, structured by location, asset type, date, and value range with bidding tips and due-diligence guidance. Use when finding auctions, foreclosures, and estate sales near any location."
---

# AuctoPilot

## Overview
Finds auctions, foreclosures, and estate sales near any location. Discovers local buying opportunities across real estate, vehicles, equipment, collectibles, and general estate items. Helps users identify undervalued assets and bidding opportunities.

## When to Use
- Searching for local real estate auctions or foreclosures
- Finding estate sales, garage sales, or liquidation events
- Locating vehicle auctions (government surplus, repossessions, classic cars)
- Discovering equipment or industrial auctions
- Researching property tax liens or sheriff's sales
- Comparing auction platforms and listing sources

## How It Works
Aggregates and filters listing data from auction platforms, government sites, estate sale directories, and local classifieds. Structures information by location, asset type, auction date, and estimated value range.

## Steps
1. Clarify asset type and location (city, zip, radius)
2. Identify relevant platforms and sources
3. Search and filter listings by date, budget, and condition
4. Structure results: title, date, location, current bid/estimate, link
5. Flag high-potential opportunities based on user criteria
6. Provide bidding tips, inspection checklists, or due diligence guidance

## Common Pitfalls
- Not verifying auction terms (buyer's premium, deposit, payment deadlines)
- Skipping property/asset inspection before bidding
- Underestimating repair or renovation costs
- Ignoring title issues or liens on real estate
- Bidding emotionally without a firm maximum price

## Inputs
- `location` (string, required) - city, zip, or area plus search radius
- `asset_type` (enum: real-estate / vehicle / equipment / collectibles / estate-items, required)
- `budget` (number) - maximum price
- `date_range` (string) - when the auction/sale must occur

## Outputs
- Structured listings: title, date, location, current bid/estimate, link
- High-potential flags against the user's criteria
- Bidding tips, inspection checklists, and due-diligence guidance

## Example
Input: estate sales with vintage furniture near Chicago, 60613, 10-mile radius, under $500.
1. Clarify: estate-items, this weekend.
2. Search estate-sale directories and local classifieds in the radius.
3. Structure results with dates, addresses, and estimated value ranges; flag the two sales with furniture-heavy listings.
4. Add tips: arrive early, bring cash, inspect before bidding.
