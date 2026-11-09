---
name: rss-assist
description: "Turns RSS feeds into original SEO-optimized blog posts and curated roundups -- feed discovery and triage, blog transformation with original analysis (never verbatim reposts), SEO metadata, and RSS-to-publish pipeline setup. Use when transforming RSS feeds into engaging SEO-optimized blogs or aggregating feed content."
---

# RSS Assist

## Overview
Transforms RSS feed content into engaging, SEO-optimized blog posts and curated roundups. Also helps discover, organize, and manage RSS feed collections for content aggregation workflows. Consolidates RSS Assist and RSS Aggregator.

## When to Use
- Turning RSS feed items into original blog posts with SEO optimization
- Creating weekly/monthly content roundups from industry RSS feeds
- Discovering and curating RSS feed lists for a specific topic or niche
- Aggregating content from multiple feeds into a single digest or dashboard
- Setting up RSS-to-blog or RSS-to-newsletter pipelines
- Monitoring competitor or industry feeds for content inspiration

## How It Works
1. Source: Connect to RSS feeds (URLs, OPML files, or feed discovery).
2. Curate: Filter and prioritize items based on relevance, recency, and quality.
3. Transform: Convert feed items into original, value-added blog content — not just reposts.
4. Optimize: Apply SEO best practices to titles, headings, meta descriptions, and structure.
5. Aggregate: Combine multiple feed sources into unified outputs.

## Steps
1. **Feed discovery** — For a given topic/niche, suggest high-quality RSS feeds to follow. Or work with user-provided feed URLs.
2. **Content triage** — Review recent feed items and surface the most blog-worthy or roundup-worthy pieces.
3. **Blog transformation** — For each chosen item: extract the core insight, add original analysis/commentary, expand with context, structure as a proper blog post.
4. **SEO optimization** — Craft an SEO title (<60 chars), meta description (150-160 chars), H2/H3 structure, internal/external link suggestions, and keyword targets.
5. **Roundup assembly** — For digest-style outputs: group items by theme, write a unifying intro, short commentary per item, and a hook for the next edition.
6. **Pipeline setup** — Guide on automating: RSS → content curation → draft generation → publishing (via Zapier, Make, or custom scripts).

## Common Pitfalls
- **Thin content**: Reposting RSS summaries verbatim adds no value and hurts SEO. Always add original insight.
- **No feed triage**: Curating every feed item drowns readers. Curate the top 10-20% by relevance.
- **SEO stuffing**: Forcing keywords into unnatural places reads badly. Write for humans first, optimize second.
- **Stale feeds**: RSS feeds go dormant. Periodically audit feed lists and replace dead sources.
- **Copyright issues**: Republishing full articles without permission is infringement. Summarize, quote sparingly, and link to the source.

## Inputs

- `feeds` -- RSS feed URLs, OPML file, or a topic/niche for feed discovery
- `content_goal` -- blog post (single-item transformation), roundup/digest (multi-feed aggregation), or pipeline setup (RSS -> curation -> draft -> publish)

## Outputs

- SEO-optimized blog posts: SEO title (<60 chars), meta description (150-160 chars), H2/H3 structure, internal/external link suggestions, keyword targets -- built from extracted insight + original commentary, not reposts
- Themed roundups: items grouped by theme with a unifying intro, short per-item commentary, and a next-edition hook
- Pipeline setup guide (Zapier, Make, or custom scripts)

## Example

A weekly industry roundup from 5 feeds: triage surfaces the top 15% most blog-worthy items, grouped into 3 themes; each item gets a 2-3 sentence original take plus a link to the source; the edition closes with a hook for next week's roundup.

## Errors & edge cases

- **Thin content** -- reposting RSS summaries verbatim adds no value and hurts SEO; always add original insight.
- **No feed triage** -- curating every item drowns readers; curate the top 10-20% by relevance.
- **Stale feeds** -- RSS feeds go dormant; periodically audit the feed list and replace dead sources.
- **Copyright issues** -- republishing full articles without permission is infringement; summarize, quote sparingly, and link to the source.
- **SEO stuffing** -- write for humans first, optimize second.
