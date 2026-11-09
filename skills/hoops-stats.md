---
name: hoops-stats
description: "LLM-agnostic developer tooling skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to deliver NBA analytics across five dimensions — raw stats, advanced metrics, situational trends, matchup analysis, and betting context — with every insight labeled by confidence level and caveated against sample size. Use when providing NBA stats, trends, betting analysis, and actionable basketball insights."
---

# Hoops Stats — NBA Analytics & Betting Insights

## Overview
Hoops Stats delivers NBA data analysis — player stats, team trends, matchup breakdowns, and betting-relevant insights. It processes game logs, advanced metrics, and situational data to surface actionable patterns for fans, fantasy players, and bettors.

## When to Use
- Comparing player performance across games or seasons.
- Analyzing team matchups, pace, and defensive schemes.
- Evaluating betting lines (spread, over/under, player props) against recent data.
- Fantasy basketball roster decisions (start/sit, waiver wire).
- Pre-game or post-game statistical breakdowns.

## How It Works
Hoops Stats analyzes basketball data across five dimensions:
1. **Raw stats** — Points, rebounds, assists, steals, blocks, turnovers, minutes.
2. **Advanced metrics** — PER, TS%, USG%, BPM, net rating, on/off splits.
3. **Situational trends** — Home/away splits, back-to-back performance, rest-advantage games.
4. **Matchup analysis** — Opponent defensive ratings, positional matchups, pace differentials.
5. **Betting context** — Line movement, public betting splits, injury impact modeling.

## Steps
1. **Clarify the question.** Player comp? Game prediction? Bet evaluation? Fantasy decision?
2. **Pull relevant data.** Use recent game logs (last 5-10 games for form, season-long for baselines).
3. **Apply context filters.** Home/away, rest days, opponent strength, injuries.
4. **Calculate insights.** Compare trends to baselines. Highlight outliers and regression candidates.
5. **Present with confidence levels.** Label each insight: High confidence (strong trend) / Medium / Low (small sample).
6. **Include caveats.** Sample size warnings, injury uncertainty, lineup changes.

## Common Pitfalls
- **Small sample theater.** Drawing conclusions from 2-3 games. Always compare against larger baselines.
- **Ignoring context.** A player's stats against the league-worst defense don't generalize.
- **Betting advice without disclaimers.** Always note that historical data doesn't guarantee future outcomes. Never present analysis as financial advice.

## Inputs
- The question type: player comparison, team matchup, betting-line evaluation (spread, over/under, player props), fantasy roster decision (start/sit, waiver wire), or pre/post-game statistical breakdown.
- Relevant data: recent game logs (last 5–10 games for form), season-long numbers for baselines.
- Context filters: home/away splits, rest days, back-to-back, opponent strength, injuries, pace differentials.

## Outputs
- Analysis across the five dimensions: raw stats, advanced metrics (PER, TS%, USG%, BPM, net rating, on/off splits), situational trends, matchup analysis, betting context (line movement, public splits, injury impact).
- Insights compared against baselines with outliers and regression candidates highlighted.
- Every insight labeled High / Medium / Low confidence, with caveats: sample-size warnings, injury uncertainty, lineup changes.

## Example
Evaluate a spread bet: "Is the -6.5 line justified for tonight's game?"

1. Clarify the question — bet evaluation against the spread.
2. Pull recent game logs (last 5–10) plus season baselines for both teams.
3. Apply context filters: home/away splits, rest advantage, opponent defensive ratings, injury reports.
4. Compare trends to baselines; highlight outliers (a player shooting 55% from three over 3 games vs a 36% season baseline is a regression candidate).
5. Present the line-vs-data verdict with a confidence label, sample-size caveats, and the disclaimer that historical data doesn't guarantee future outcomes — never framed as financial advice.
