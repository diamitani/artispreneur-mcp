---
name: image-scraper-pro
description: "Bulk website image extractor with relevance filtering — scrapes img tags, srcsets, and CSS backgrounds across pages or catalogs, filters by size/format/alt-text, downloads with proper naming (never hotlinks), and generates attribution docs. Use when scraping and extracting relevant images from websites for visual content enhancement."
---

# Image Scraper Pro

Extract relevant images from websites for visual content enhancement.

## Core Capabilities
- **Website Image Extraction**: Identify and extract images from target URLs
- **Relevance Filtering**: Filter by size, format, alt text, and contextual relevance
- **Bulk Collection**: Gather images across multiple pages or product catalogs
- **Format Optimization**: Convert and resize for target platforms
- **Metadata Extraction**: Capture alt text, captions, and source attribution

## Workflow
1. Define target URL(s) and image requirements (size, type, topic)
2. Scrape page for all image elements (img tags, background images, srcsets)
3. Filter by dimensions, file type, and contextual relevance
4. Download qualifying images with proper naming
5. Generate attribution and usage documentation

## Technical Approach
- Parse HTML for `<img>` tags, `<picture>` elements, and CSS backgrounds
- Check `srcset` for responsive image variants
- Filter by minimum dimensions (ignore icons, spacers, tracking pixels)
- Respect the target site's robots.txt and rate limiting
- Use headless browser for JavaScript-rendered images when needed

## Pitfalls
- Always respect copyright and licensing — check site terms of use
- Don't hotlink — download and host images properly
- Respect the target site's robots.txt and implement polite scraping delays
- Some sites use CDN image protection — may require alternative approaches
- Never scrape personal images or PII

## Inputs

- `urls` (string | string[], required) — target page(s) or catalog to scrape
- `min_dimensions` (string, optional, e.g. `1200x800`) — minimum width/height; icons, spacers, and tracking pixels are ignored by default
- `formats` (string[], optional, e.g. `jpeg`, `png`, `webp`) — allowed file types
- `topic_keywords` (string[], optional) — relevance filter applied to alt text and surrounding context
- `render_js` (boolean, default: auto) — use a headless browser when images are JavaScript-rendered

## Outputs

- Downloaded image files with proper naming (deliverable: files on disk, converted/resized for the target platform)
- Attribution and usage documentation (Markdown) capturing alt text, captions, and source URLs
- Format: local image files + `attribution.md`-style doc; nothing hotlinked

## Example

Target: `https://example-shop.com/catalog`. Requirements: product photos at least 1200px wide, JPEG or PNG, topic keyword `jacket`. The skill parses `<img>`, `<picture>`, and CSS backgrounds (checking `srcset` for the best variant), filters out icons and tracking pixels, downloads qualifiers to `./images/` with descriptive filenames, and writes an attribution doc with source URLs and license notes.
