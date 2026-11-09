---
name: dropshipping-ai-assistant
description: "LLM-agnostic workflow automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to automate dropshipping workflows and optimize product strategy end-to-end: niche selection -> product research -> supplier vetting (AliExpress, CJ Dropshipping, Zendrop) -> store setup -> marketing -> scaling, with KPI tracking (CPA, ROAS, conversion rate, AOV, margin) and hard pitfalls (no saturated products without differentiation, never scale ads before unit economics). Use when automating dropshipping workflows and optimizing product strategy for e-commerce businesses."
---

# Dropshipping AI Assistant

## Overview
Automates dropshipping workflows and optimizes product strategy for e-commerce businesses. Helps with product research, supplier evaluation, store optimization, and marketing strategy for dropshipping operations.

## When to Use
- Researching winning products or trending niches
- Evaluating suppliers on AliExpress, CJ Dropshipping, Zendrop, or similar
- Optimizing Shopify/WooCommerce store pages and product listings
- Creating ad copy, product descriptions, or email sequences
- Analyzing competitor stores and pricing strategies
- Automating order fulfillment or inventory tracking workflows

## How It Works
Guides users through the dropshipping lifecycle: niche selection → product research → supplier vetting → store setup → marketing → scaling. Provides frameworks, checklists, and automation scripts where applicable.

## Steps
1. Clarify the user's dropshipping model (general store, one-product, niche, branded)
2. For product research: analyze criteria (demand, margin, competition, shipping)
3. For supplier evaluation: check ratings, shipping times, communication, samples
4. For store optimization: review product pages, pricing, upsells, trust signals
5. For marketing: recommend ad platforms, creative angles, targeting strategies
6. Track KPIs: CPA, ROAS, conversion rate, AOV, profit margin

## Common Pitfalls
- Chasing saturated products without differentiation
- Ignoring shipping times and supplier reliability
- Underpricing (not accounting for ad costs, returns, fees)
- Scaling ad spend before unit economics are proven
- Neglecting post-purchase experience and customer support

## Inputs
- `model` (enum: general-store / one-product / niche / branded, required)
- `stage` (enum: product-research / supplier-eval / store-optimization / marketing / scaling, required)
- `criteria` (object) - demand, margin, competition, shipping time

## Outputs
- Product research shortlist with criteria scores
- Supplier evaluation (ratings, shipping times, communication, samples)
- Store optimization review: product pages, pricing, upsells, trust signals
- Marketing plan: platforms, creative angles, targeting; KPI dashboard (CPA, ROAS, conversion, AOV, margin)

## Example
Input: one-product store, product-research stage, pet niche.
1. Clarify the model (one-product) and criteria (demand + margin + shippable).
2. Research: 5 candidates scored; the winner has demand, 3x margin headroom, low saturation.
3. Supplier eval: 2 AliExpress suppliers compared on rating/shipping/communication.
4. KPI targets set before any ad spend: CPA ceiling, ROAS floor.
