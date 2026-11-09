---
name: popular-web-designs
description: "Real-world design vocabularies for generating HTML/CSS — templates capturing a site's visual language (Stripe's signature purple gradients and weight-300 elegance, Linear's ultra-minimal dark mode, Apple's premium whitespace): color palette as CSS custom properties, typography hierarchy, component styles, spacing system, shadows, plus copy-paste agent prompts and CDN font substitutes for proprietary typefaces. Pair with `claude-design` for taste and process. Use when working with real design systems."
---

# Popular Web Designs

Real-world design vocabularies for generating HTML/CSS. Each template captures a site's
visual language: color palette, typography hierarchy, component styles, spacing system,
shadows, and practical agent prompts with CSS values. The catalog is extensible — 3
templates ship with the skill (below); add more by following the template format in
"Extending the catalog.

## Related design skills

- **`claude-design`** — use for the design *process and taste* (scoping a brief,
  producing variants, verifying a local HTML artifact, avoiding AI-design slop).
  Pair it with this skill when the user wants a thoughtfully-designed page styled
  after a known brand: `claude-design` drives the workflow, this skill supplies
  the visual vocabulary.
- **`design-md`** — use when the deliverable is a formal DESIGN.md token spec
  file, not a rendered artifact.

## How to Use

1. Pick a design from the catalog below
2. Load it: `skill_view(name="popular-web-designs", file_path="templates/<site>.md")`
3. Use the design tokens and component specs when generating HTML
4. Pair with the `generative-widgets` skill to serve the result via cloudflared tunnel

Each template includes a **Hermes Implementation Notes** block at the top with:
- CDN font substitute and Google Fonts `<link>` tag (ready to paste)
- CSS font-family stacks for primary and monospace
- Reminders to use `write_file` for HTML creation and `browser_vision` for verification

## HTML Generation Pattern

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <!-- Paste the Google Fonts <link> from the template's Hermes notes -->
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
  <style>
    /* Apply the template's color palette as CSS custom properties */
    :root {
      --color-bg: #ffffff;
      --color-text: #171717;
      --color-accent: #533afd;
      /* ... more from template Section 2 */
    }
    /* Apply typography from template Section 3 */
    body {
      font-family: 'Inter', system-ui, sans-serif;
      color: var(--color-text);
      background: var(--color-bg);
    }
    /* Apply component styles from template Section 4 */
    /* Apply layout from template Section 5 */
    /* Apply shadows from template Section 6 */
  </style>
</head>
<body>
  <!-- Build using component specs from the template -->
</body>
</html>
```

Write the file with `write_file`, serve with the `generative-widgets` workflow (cloudflared tunnel),
and verify the result with `browser_vision` to confirm visual accuracy.

## Font Substitution Reference

Most sites use proprietary fonts unavailable via CDN. Each template maps to a Google Fonts
substitute that preserves the design's character. Common mappings:

| Proprietary Font | CDN Substitute | Character |
|---|---|---|
| Geist / Geist Sans | Geist (on Google Fonts) | Geometric, compressed tracking |
| Geist Mono | Geist Mono (on Google Fonts) | Clean monospace, ligatures |
| sohne-var (Stripe) | Source Sans 3 | Light weight elegance |
| Berkeley Mono | JetBrains Mono | Technical monospace |
| Airbnb Cereal VF | DM Sans | Rounded, friendly geometric |
| Circular (Spotify) | DM Sans | Geometric, warm |
| figmaSans | Inter | Clean humanist |
| Pin Sans (Pinterest) | DM Sans | Friendly, rounded |
| NVIDIA-EMEA | Inter (or Arial system) | Industrial, clean |
| CoinbaseDisplay/Sans | DM Sans | Geometric, trustworthy |
| UberMove | DM Sans | Bold, tight |
| HashiCorp Sans | Inter | Enterprise, neutral |
| waldenburgNormal (Sanity) | Space Grotesk | Geometric, slightly condensed |
| IBM Plex Sans/Mono | IBM Plex Sans/Mono | Available on Google Fonts |
| Rubik (Sentry) | Rubik | Available on Google Fonts |

When a template's CDN font matches the original (Inter, IBM Plex, Rubik, Geist), no
substitution loss occurs. When a substitute is used (DM Sans for Circular, Source Sans 3
for sohne-var), follow the template's weight, size, and letter-spacing values closely —
those carry more visual identity than the specific font face.

## Design Catalog

Shipped templates (in `templates/`):

| Template | Site | Style |
|---|---|---|
| `templates/stripe.md` | Stripe | Signature purple gradients, weight-300 elegance |
| `templates/apple.md` | Apple | Premium white space, SF Pro, cinematic imagery |
| `templates/linear.app.md` | Linear | Ultra-minimal dark-mode, precise, purple accent |

### Extending the catalog

To add a new site template, create `templates/<site>.md` following the shipped
examples. Every template must include:

1. **Hermes Implementation Notes** block at the top (CDN font substitute +
   Google Fonts `<link>`, font-family stacks, `write_file`/`browser_vision`
   reminders)
2. Character summary (what makes this design recognizable)
3. Color palette as CSS custom properties with real observed values
4. Typography: weights, sizes, tracking, scale
5. Component styles (buttons, cards, nav, code blocks…)
6. Layout rules (max-width, section rhythm, hero pattern)
7. Shadow treatment
8. Agent prompts — copy-paste instructions that reproduce the look

Planned additions (not yet written — contribute following the format above):
Claude, Vercel, Supabase, Figma, Notion, Airbnb, Spotify, Coinbase, Framer,
Raycast, Sentry, Mintlify, Cal.com, Webflow, Miro, Intercom, Zapier, Warp,
Cursor, PostHog, Resend, Replit-style docs sites, and others.

## Choosing a Design

Match the design to the content:

- **Developer tools / dashboards:** Linear, Vercel, Supabase, Raycast, Sentry
- **Documentation / content sites:** Mintlify, Notion, Sanity, MongoDB
- **Marketing / landing pages:** Stripe, Framer, Apple, SpaceX
- **Dark mode UIs:** Linear, Cursor, ElevenLabs, Warp, Superhuman
- **Light / clean UIs:** Vercel, Stripe, Notion, Cal.com, Replicate
- **Playful / friendly:** PostHog, Figma, Lovable, Zapier, Miro
- **Premium / luxury:** Apple, BMW, Stripe, Superhuman, Revolut
- **Data-dense / dashboards:** Sentry, Kraken, Cohere, ClickHouse
- **Monospace / terminal aesthetic:** Ollama, OpenCode, x.ai, VoltAgent

## Inputs

- Chosen design from the catalog (required) — shipped: `stripe`, `apple`, `linear.app`; extensible via `templates/<site>.md` (Hermes Implementation Notes block + 8 sections)
- The template loaded via `skill_view(name="popular-web-designs", file_path="templates/<site>.md")` — tokens, typography, component specs, layout rules, shadow treatment, agent prompts
- The content to style — matched to a design via the Choosing a Design table
- Related skills: `claude-design` (design process/taste) · `design-md` (formal DESIGN.md token spec) · `generative-widgets` (serve via cloudflared tunnel)

## Outputs

- A single self-contained HTML page: Google Fonts `<link>` from the template's Hermes notes, CSS custom properties for the palette, template typography, component styles (buttons, cards, nav, code blocks), layout rules, shadow treatment
- Served via the `generative-widgets` workflow (cloudflared tunnel) and verified with `browser_vision` for visual accuracy
- New catalog templates in the 8-section format (planned additions: Claude, Vercel, Supabase, Figma, Notion, Airbnb, Spotify, Coinbase, Framer, Raycast, Sentry, Mintlify, Cal.com, Webflow, Miro, Intercom, Zapier, Warp, Cursor, PostHog, Resend)
- Format: HTML/CSS — one design's vocabulary, applied faithfully

## Example

Landing page styled after Stripe → load `templates/stripe.md` via `skill_view` → tokens: `--color-accent: #533afd`, sohne-var → Source Sans 3 CDN substitute, weight-300 elegance → build single self-contained HTML (font `<link>`, `:root` custom properties, typography, component styles, layout, shadows) → `write_file` → serve via the `generative-widgets` cloudflared tunnel → verify with `browser_vision`. Extending: add `templates/<site>.md` with Hermes Implementation Notes + the 8-section format.

## Errors & edge cases

- **Proprietary font unavailable via CDN** → use the template's Google Fonts substitute (e.g. Source Sans 3 for Stripe's sohne-var, DM Sans for Circular/Airbnb Cereal) and follow the template's weight, size, and letter-spacing values closely — those carry more visual identity than the specific font face.
- **Substituted font but ignored tracking** → the design won't read as the original; weight, size, and letter-spacing matter more than the face.
- **Mixing design vocabularies** → pick one design and match it to the content via the Choosing a Design table (developer tools → Linear/Vercel, marketing → Stripe/Apple, dark mode → Linear/Cursor, premium → Apple/BMW, playful → PostHog/Figma).
