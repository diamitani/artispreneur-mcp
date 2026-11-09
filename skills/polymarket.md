---
name: polymarket
description: "Queries Polymarket prediction-market data through three read-only public REST APIs (zero auth): Gamma (discovery/search), CLOB (real-time prices, orderbooks, history), and Data (trades, open interest) — parsing double-encoded fields, presenting prices as probabilities, with generous rate limits. Read-only: it does not place trades. Use when you need to query Polymarket markets, prices, orderbooks, and history."
---

# Polymarket — Prediction Market Data

Query prediction market data from Polymarket using their public REST APIs.
All endpoints are read-only and require zero authentication.

See `references/api-endpoints.md` for the full endpoint reference with curl examples.

## When to Use

- User asks about prediction markets, betting odds, or event probabilities
- User wants to know "what are the odds of X happening?"
- User asks about Polymarket specifically
- User wants market prices, orderbook data, or price history
- User asks to monitor or track prediction market movements

## Key Concepts

- **Events** contain one or more **Markets** (1:many relationship)
- **Markets** are binary outcomes with Yes/No prices between 0.00 and 1.00
- Prices ARE probabilities: price 0.65 means the market thinks 65% likely
- `outcomePrices` field: JSON-encoded array like `["0.80", "0.20"]`
- `clobTokenIds` field: JSON-encoded array of two token IDs [Yes, No] for price/book queries
- `conditionId` field: hex string identifying the market (used by the Data API `/trades` endpoint)
- For CLOB price history, pass the **token ID** from `clobTokenIds`, not the conditionId
- Volume is in USDC (US dollars)

## Three Public APIs

1. **Gamma API** at `gamma-api.polymarket.com` — Discovery, search, browsing
2. **CLOB API** at `clob.polymarket.com` — Real-time prices, orderbooks, history
3. **Data API** at `data-api.polymarket.com` — Trades, open interest

## Typical Workflow

When a user asks about prediction market odds:

1. **Search** using the Gamma API public-search endpoint with their query
2. **Parse** the response — extract events and their nested markets
3. **Present** market question, current prices as percentages, and volume
4. **Deep dive** if asked — use clobTokenIds for orderbook and price history (token ID, not conditionId)

## Presenting Results

Format prices as percentages for readability:
- outcomePrices `["0.652", "0.348"]` becomes "Yes: 65.2%, No: 34.8%"
- Always show the market question and probability
- Include volume when available

Example: `"Will X happen?" — 65.2% Yes ($1.2M volume)`

## Parsing Double-Encoded Fields

The Gamma API returns `outcomePrices`, `outcomes`, and `clobTokenIds` as JSON strings
inside JSON responses (double-encoded). When processing with Python, parse them with
`json.loads(market['outcomePrices'])` to get the actual array.

## Rate Limits

Generous — unlikely to hit for normal usage (verified against the official
rate-limits reference, https://docs.polymarket.com/api-reference/rate-limits,
on 2026-09-15):
- Gamma: 4,000 requests per 10 seconds (general)
- CLOB: 9,000 requests per 10 seconds (general)
- Data: 1,000 requests per 10 seconds (general)

## Limitations

- This skill is read-only — it does not support placing trades
- Trading requires wallet-based crypto authentication (EIP-712 signatures)
- Some new markets may have empty price history
- Geographic restrictions apply to trading but read-only data is globally accessible

## Inputs

- The question/event to look up (required) — ‘what are the odds of X happening?’ or a Polymarket-specific request
- API choice: **Gamma** (`gamma-api.polymarket.com`) for discovery/search/browsing · **CLOB** (`clob.polymarket.com`) for real-time prices, orderbooks, history — pass the **token ID** from `clobTokenIds` · **Data** (`data-api.polymarket.com`) for trades and open interest — pass `conditionId`
- Key concepts: Events contain 1:many Markets; markets are binary Yes/No with prices 0.00–1.00 = probabilities; volume is in USDC
- Full endpoint reference with curl examples: `references/api-endpoints.md`

## Outputs

- Market question, current Yes/No prices as percentages, and volume (e.g. ‘“Will X happen?” — 65.2% Yes ($1.2M volume)’)
- On deep dive: orderbook data and price history
- Rate limits (generous, verified 2026-09-15): Gamma 4,000 / CLOB 9,000 / Data 1,000 requests per 10 seconds
- Format: prices as percentages for readability; always show the market question and probability, include volume when available

## Example

‘What are the odds the Fed cuts rates in March?’ → search via the Gamma API public-search endpoint (`gamma-api.polymarket.com`) → parse the event and its nested markets → `outcomePrices` `["0.652", "0.348"]` (json.loads the double-encoded field) → present: ‘Will the Fed cut rates in March? — 65.2% Yes ($1.2M volume)’ → deep dive: orderbook and price history via the CLOB API (`clob.polymarket.com`) using the token ID from `clobTokenIds`.

## Errors & edge cases

- **Prices look like garbled strings** → `outcomePrices`, `outcomes`, and `clobTokenIds` are double-encoded JSON strings inside the JSON response — parse with `json.loads(market['outcomePrices'])` to get the actual array.
- **CLOB history query returns nothing** → pass the **token ID** from `clobTokenIds` (the [Yes, No] pair), not the `conditionId` hex — `conditionId` is for the Data API `/trades` endpoint.
- **Empty price history** → expected for some new markets; present the current price instead.
- **Trading requested** → not supported: this skill is read-only. Trading requires wallet-based crypto authentication (EIP-712 signatures); geographic restrictions apply to trading, but read-only data is globally accessible.
