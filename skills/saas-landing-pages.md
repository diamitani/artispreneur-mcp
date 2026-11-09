---
name: saas-landing-pages
description: "Builds self-contained HTML landing pages for niche SaaS products by hybridizing 2-3 design templates (industry + interaction style) with the product's real brand identity -- a fixed 12-section page order, copy pulled from the product spec and never invented, verified in the browser before sign-off. Use when you need to build marketing/landing pages for niche SaaS."
---

# SaaS Landing Pages

Build self-contained HTML landing pages for niche SaaS products that sit at
industry intersections. Pull from the right template catalog (usually via the
popular-web-designs skill) and blend the templates with the product's actual
brand identity.

## Workflow

1. **Extract brand identity**:
   - Copy the user's logo into the project folder.
   - Extract dominant colors (Pillow, `sips` on macOS, or visual inspection).
   - If extraction tools are blocked (pip denied), fall back to `sips` or ask
     the user for the brand hex values.
   - NEVER fall back to a template's default color.

2. **Pick templates**: use the popular-web-designs catalog, matching by
   industry AND interaction style:
   - Pick one for the product's primary industry (e.g. Spotify for music).
   - Pick one for interaction style (e.g. Linear for AI workspaces).
   - Max 2–3 templates. More causes typography/spacing/shadow clashes.

3. **Hybridize the recipe**:
   - Surface colors from the dominant template (near-black, etc.).
   - Typography and layout rules from the interaction-style template.
   - Accent color from the actual user's logo — NEVER the template's green/orange.
   - Pick buttons/cards/shadows from whichever template feels more right.

4. **Build** as a single self-contained `.html` file (~40–80KB is fine):
   - All CSS in `<style>` tags in the head.
   - All JavaScript in one `<script>` tag at the bottom of the body.
   - Copy product copy from the user's product spec directly — never invent it.
   - Serve locally for preview: `python3 -m http.server 8765`.
   - Verify in the browser at `http://localhost:8765`: scroll through every
     section and confirm each one renders before calling it done.

## Sections (ordered)

1. **Announcement bar** — slim strip with a link to the CTA/early-access.
2. **Sticky nav** — logo + nav links + CTAs (Sign In / Get Started).
3. **Hero** — large headline (headline + gradient text), subheadline, dual CTA
   (primary + ghost), animated background (mesh gradient + grid overlay).
4. **Video section** — 16:9 container with play button, poster frame, and
   social-proof count (avatars + number).
5. **Agent/feature showcase** — tabbed or grid layout with split info panels.
6. **Feature cards** — benefit-first, one sentence each.
7. **Features grid** — 3-column grid; span-2 cards for the important features.
8. **Dashboard preview** — fake app chrome: sidebar + main area + stat cards.
9. **Platform pages** — pill switcher between app views.
10. **Signup CTA** — stat bar + email/waitlist form.
11. **Trust logos** — customer/genre logos in a muted row.
12. **Footer** — 4-column layout (Product / Resources / Company / Legal).

## Pitfalls

### Disk space — co-located projects [CRITICAL]
When building a new site in a monorepo with sibling Next.js/Docusaurus
projects, each sibling's `node_modules` can consume 400–500MB. Running
`npm install` on a third project will hit ENOSPC. **Before installing, clean
sibling artifacts:**
```bash
rm -rf ../dashboard/node_modules ../pal-site/node_modules ../deploy/.next
```
Check disk first: `df -h /`. If under 1GB free, aggressively clean before
installing.

### Video content integration (non-vision models)
When the user provides a video and the active model lacks vision, use
`whisper` for audio transcription to extract the narrative:
```bash
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 /tmp/audio.mp3
whisper /tmp/audio.mp3 --model tiny --language en --output_format txt
```
Then incorporate the transcript content into the page copy. For the video
element itself, keep the `<video>` tag with a poster fallback — the actual
mp4 can be served alongside the HTML if space permits.

### Design-source extraction
- 21st.dev community components are SPA-rendered — page-extract tools return
  empty. Use browser navigation + full-page snapshot to extract, and use
  category labels/scroll sidebars as design inspiration only.
- If a tool fails (Pillow denied, binary missing), use `sips` on macOS or
  visually inspect the image and ask the user.

### Blending rules
- **Don't guess the accent color from the template.** Take it from the user's
  logo. Falling back to the template's default green or indigo makes a clone,
  not a blend.
- **Don't blend more than 3 templates.** Typography and shadows will clash.
  Two is almost always enough.
- **Don't make up product copy.** Pull copy directly from the user's spec.

## Copy voice patterns

- **Hero**: declarative short sentences. Speak to who the user already is,
  not who they should become. "Your Music. Your Business."
- **Section labels**: emoji + ALL-CAPS micro-label above each title
  (e.g. `⚡ AGENTIC WORKSPACE`).
- **Feature cards**: benefit-first, one sentence each.
- **CTA**: aspirational but grounded — not hype.

## Reference recipes

- `references/ethereal-glass-recipe.md` — OLED black, cyan accent,
  double-bezel cards, Geist typography. For AI/SaaS dark-mode-first products.
- `references/halftone-pulse-recipe.md` — Halftone dot textures, warm accent,
  bold display type. For creator/music tools with energy.
- `references/spotify-hybrid-recipe.md` — Spotify-industry + Linear-interaction
  hybrid: how to blend two templates without clashing.
- `references/hybrid.md` — The general hybridization method: picking,
  blending, and QA rules.
- `references/music-tech-saas-hybrid.md` — Worked example: Spotify + Linear
  hybrid for a music-tech SaaS.
- `references/rostr-saas-case-study.md` — Worked example: SaaS landing build
  using video transcript → problem grid → solution flow → bento features.
- `references/nextjs-route-group-pattern.md` — Integrating a landing page and
  an app dashboard into one Next.js project using route groups, instead of
  deploying two separate projects.

## Related

- **popular-web-designs** skill — design template catalog for typography and
  component specs. Load it first; pick the two templates that best match the
  product's industry AND interaction style.
- **claude-design** skill — design process workflow (scoping brief, verifying,
  avoiding AI slop).
- **shadcn-app-design** skill — for the app/dashboard portion of a SaaS
  platform. Use together with this skill when building a complete platform
  (landing page + app).
- **ocr-and-documents** skill — for extracting brand guidelines from PDFs.

## Inputs

- `product_spec` -- the source of all copy (never invent product copy)
- `logo` -- the user's logo file; dominant colors extracted (Pillow, `sips` on macOS, or visual inspection) -- NEVER fall back to a template's default color
- `templates` -- 1-3 picks from the popular-web-designs catalog: one for the product's industry (e.g. Spotify for music), one for interaction style (e.g. Linear for AI workspaces); more than 3 causes typography/spacing/shadow clashes

## Outputs

- A single self-contained `.html` file (~40-80KB): all CSS in head `<style>` tags, all JS in one bottom `<script>` tag; the 12 ordered sections (announcement bar, sticky nav, hero, video, showcase, feature cards, features grid, dashboard preview, platform pages, signup CTA, trust logos, footer); served locally (`python3 -m http.server 8765`) and verified section-by-section in the browser

## Example

A music-tech SaaS: Spotify (industry) + Linear (interaction-style) hybrid -- surface colors from the dominant template, typography/layout rules from Linear, accent color from the actual logo; the reference recipe `references/music-tech-saas-hybrid.md` shows the full blend.

## Errors & edge cases

- **Template default colors** -- guessing the accent from the template makes a clone, not a blend; always take it from the user's logo.
- **More than 3 templates** -- typography and shadows will clash; two is almost always enough.
- **Invented copy** -- pull copy directly from the user's spec.
- **Disk space (ENOSPC) in monorepos** -- sibling `node_modules` can eat 400-500MB each; check `df -h /` and clean sibling artifacts before `npm install`.
- **Video provided to a non-vision model** -- transcribe with whisper and fold the narrative into the copy; keep the `<video>` tag with a poster fallback.
- **21st.dev components** -- SPA-rendered; page-extract tools return empty; use browser navigation + full-page snapshot.
