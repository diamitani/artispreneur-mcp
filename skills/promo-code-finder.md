---
name: promo-code-finder
description: "Discovers new-user promo codes, signup discounts, and promotional offers before registering for online services — a consolidation of the ProMe and 1Promo GPTs: searches known promotion databases, company offer pages, and community-sourced deals, validates expiration and terms, ranks the best options by value with restrictions noted, and gives application instructions. Use when finding new user codes, promo codes, and signup discounts before registering for services."
---

# Promo Code Finder

## Overview

Helps users discover new user promo codes, signup discounts, and promotional offers before registering for online services. Consolidates the ProMe and 1Promo GPTs for finding company promotions.

## When to Use

- User wants to find discount codes before signing up for a service
- Searching for new user promotions or referral codes
- Comparing signup incentives across competing platforms
- Checking if a company offers first-time user discounts

## How It Works

Searches for and validates promo codes, referral links, and signup bonuses. Can check known promotion databases, company offer pages, and community-sourced deals.

## Steps

1. **Identify the service** — Determine which company or platform the user wants to sign up for
2. **Search for offers** — Look for active promo codes, signup bonuses, and referral programs
3. **Validate codes** — Check expiration dates and terms/conditions
4. **Present best options** — Rank by value with any restrictions noted
5. **Provide application instructions** — How to apply the code during signup

## Common Pitfalls

1. **Expired codes** — Always verify recency; promo codes expire frequently
2. **Region restrictions** — Many codes are geo-limited; confirm availability in user's region
3. **Stacking limits** — Most platforms don't allow combining multiple promo codes

## Source

Originally deployed as two custom GPTs:
- [ProMe](https://chatgpt.com/g/g-2so7aRjk7-prome)
- [1Promo](https://chatgpt.com/g/g-guHxZadWZ-1promo)

## Inputs

- The service/company to sign up for (required)
- The user's region (many codes are geo-limited) and plan preference (annual vs monthly affects which code wins)

## Outputs

- Validated promo codes, referral links, and signup bonuses: expiration dates, terms/conditions, region restrictions, stacking limits
- Ranked by value with restrictions noted
- Application instructions: how to apply the code during signup
- Format: ranked options + how-to-apply

## Example

‘Any deals for signing up to Notion?’ → identify the service → search promo databases, the company's offer pages, and community deals → validate: code X expires end of month, 20% off annual, new users only, US-only → present ranked: X (20% off annual) > referral link Y ($10 credit) — stacking not allowed → application: ‘enter X at checkout on the annual plan before creating the workspace.’
