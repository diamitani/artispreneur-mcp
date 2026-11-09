---
name: modular-react-framework
description: "Scaffolds and builds modular React+TypeScript dashboards, directories, and data tools in a strict layered architecture — core/types → core/schema → data → features → ui, with Zod validation and quarantine-never-discard data quality — on Vite + Tailwind v4 + React Router + TanStack Table, with taste-skill dial adaptations for data-dense UIs. Use when any data-rich React application, not just landing pages."
---

# Modular React Framework

Scaffold and build modular React+TypeScript dashboards, directories, and data tools with a layered architecture designed for data quality and expandability.

## Trigger conditions

Use this skill when:
- Building a React dashboard, data directory, admin panel, or any data-rich tool
- Setting up a new React+TypeScript+Tailwind project from scratch
- User mentions "modular", "data quality first", "expandable", "ward-agnostic", or "framework"
- The brief calls for tables, filters, search, data cards — NOT a marketing landing page

Do NOT use this skill for:
- Landing pages / marketing sites → use `landing-page-build`
- Python/FastAPI backends → use `backend-dev`
- Throwaway experiments → use `spike`

## Architecture layers (build in this order)

```
src/
├── core/types/         ← Interfaces — framework-agnostic, pure data shapes
├── core/schema/        ← Zod validation + data quality engine
├── data/sources/       ← API clients (fetch, retry, pagination)
├── data/transform/     ← Raw API records → validated domain models
├── data/seed/          ← Fallback seed data + React context provider
├── features/           ← Feature modules (directory, dashboard, etc.)
├── ui/layout/          ← App shell (nav, footer, Outlet)
├── ui/data/            ← Reusable: DataTable, StatCard, Badge, SearchInput, FilterPills
├── lib/                ← Pure utilities (search, geo, format)
├── router/             ← React Router config
├── App.tsx             ← Provider wrapping + RouterProvider
└── main.tsx            ← StrictMode + createRoot
```

**Rule:** Build top-down by layer. Never skip a layer — each depends on the one above. core/types has zero imports from the rest of the project. data/transform imports only core. `features` import `core` + `data`. `ui` imports nothing from `features`. This prevents circular dependencies.

## Scaffold steps

All paths in this section (e.g. src/index.css, core/types/models.ts) refer to
files you create in the **user's project directory** — they are not bundled with
this skill.

### 1. Create Vite project

```bash
npm create vite@latest . -- --template react-ts
# If directory not empty: scaffold into a subdirectory of the user's workspace,
# then move the files into place (never /tmp as the only copy — temp storage
# can be wiped without warning)
npm install
npm install react-router-dom @tanstack/react-table zod fuse.js @phosphor-icons/react
npm install -D tailwindcss@4 @tailwindcss/vite@4
```

### 2. Configure vite.config.ts

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@core': resolve(__dirname, 'src/core'),
      '@data': resolve(__dirname, 'src/data'),
      '@features': resolve(__dirname, 'src/features'),
      '@ui': resolve(__dirname, 'src/ui'),
    },
  },
})
```

### 3. Configure tsconfig.app.json

Add `baseUrl: "."` and matching `paths` for all aliases. Use the same @/, @core/, etc. prefixes so imports read cleanly.

### 4. Set up Tailwind v4 CSS

In src/index.css, use `@import 'tailwindcss'` (NOT the old `@tailwind base` directives). Define a `@theme` block with the project's color tokens. Tailwind v4 does NOT need a tailwind.config.js or postcss.config.js file.

### 5. Type system (core/types/models.ts in the user project)

Design all interfaces as framework-agnostic. Use `ward: number` instead of hardcoded ward values — this is what makes the system expandable. Key entities for a directory/dashboard:
- Business (with license status, category, address, geo)
- Institution (religious, school, community, etc.)
- Precinct + PrecinctCaptain + PollingLocation
- ServiceTicket (constituent intake)
- CommunityEvent
- WardMeta + WardMetrics + Initiative

### 6. Validation layer (core/schema/validation.ts in the user project)

```ts
import { z } from 'zod';

// Every entity gets a Zod schema
export const businessSchema = z.object({ ... });

// Validation engine:
export function validateRecord<T>(schema, data) → { valid, data?, errors[], warnings[] }
export function validateBatch<T>(schema, records[]) → { valid[], invalid[] }

// Data quality checks (post-validation):
// - Staleness: lastUpdated > 90 days → warning
// - Unverified: verifiedAt === null → warning
// - Missing geo: address.geo missing → warning
```

**CRITICAL PRINCIPLE:** Invalid records are quarantined, never discarded. The `validateBatch` function returns both `valid` and `invalid` arrays so nothing is silently lost.

### 7. Data layer

**API client** (data/sources/ in the user project): Fetch with retry (3 attempts, exponential backoff), pagination support, field selection. For Socrata APIs (Chicago Data Portal), use `$where`, `$select`, `$order`, `$limit`, `$offset` as query params.

**Transform** (data/transform/ in the user project): Map raw API field names to domain models. Infer categories from descriptions with a keyword map. Run through `validateBatch` before returning.

**Seed data** (data/seed/ in the user project): Create a React context provider that holds fallback data. In production this gets swapped for live API data. Always include enough seed data (5-10 records per entity) so the UI renders meaningfully without an API connection.

### 8. Shared UI components (ui/data/DataDisplay.tsx in the user project)

Build these once, use everywhere:
- **DataTable** — generic `<T>` table with columns config, empty state, row click
- **StatCard** — label + value + subtitle + trend indicator
- **Badge** — variant-driven (active/expired/pending/open/resolved/closed)
- **SearchInput** — search icon + controlled input
- **FilterPills** — mutually-exclusive pill buttons

### 9. Feature modules

Each feature is a self-contained directory with components that receive data as props (never fetch internally — this keeps them pure and testable):

- **BusinessDirectory**: search + filter pills + sort + table
- **PrecinctFinder**: search + card grid (captain profile, polling location)
- **Dashboard**: stat cards + meta stats + initiative tracker + pipeline status
- **EventsPage**: upcoming events in cards, past events in compact list
- **ReportIssue**: intake form with validation

### 10. Routing

Use `createBrowserRouter` with a Layout shell (nav header + `<Outlet />` + footer). Each page component wraps the feature component, pulling data from the seed context (or eventually an API hook).

## Taste-skill dial adaptation for data tools

The taste skills (design-taste-frontend, gpt-taste) are built for landing pages. When you're building a dashboard/directory instead, adapt the three dials:

| Dial | Landing Page | Dashboard/Data Tool |
|------|-------------|---------------------|
| DESIGN_VARIANCE | 7-9 | 4-5 (data needs consistency) |
| MOTION_INTENSITY | 6-8 | 2-3 (subtle state transitions only) |
| VISUAL_DENSITY | 3-5 | 6-8 (data density is the point) |

**Color:** Never default to AI-purple. For civic/public-sector: navy + sky blue + a restrained accent. For enterprise: the design system's own tokens. For data tools specifically: neutral grays with one accent for interactive elements.

**Typography:** Two profiles depending on audience:
- **Civic/public-sector:** Inter (body) + JetBrains Mono (data/labels). Inter is explicitly acceptable per taste-skill rules for "public-sector / accessibility-first" projects.
- **Developer tools / premium tools:** Geist Sans (body) + Geist Mono (code). Install the @fontsource/geist-sans and @fontsource/geist-mono npm packages. Import in the component (not global CSS) to scope it: import '@fontsource/geist-sans/400.css' etc., then apply with `style={{ fontFamily: "'Geist Sans', 'Geist', sans-serif" }}` on the root element. Inter is banned per taste-skill rules for non-civic projects.

**Never** apply landing-page patterns (centered hero, AIDA structure, GSAP scroll-triggers, cinematic spacing) to a data tool. The user is here to work with data, not to be marketed to.

## Data quality principles

1. **Validate at the boundary** — every external record passes through Zod before entering the system
2. **Quarantine, never discard** — invalid records are logged, not silently dropped
3. **Source tracking** — every record tagged with origin (`city_api | manual | import`)
4. **Verification flag** — `verifiedAt: null` means "needs human review"
5. **Staleness detection** — warn on records not updated in 90+ days
6. **Batch validation** — process in chunks, report valid/invalid counts

## Hazards

### node_modules copy breaks binaries
Copying `node_modules` between directories (e.g., from `/tmp/` to the project) breaks binary symlinks in the project's .bin/ directory (tsc, vite, etc.). **Always run `npm install` from the target directory after copying.** Better: never copy node_modules — install fresh.

### Vite build detected as server
Hermes may flag `npx vite build` as a long-running server and reject it in foreground mode. Two workarounds:

**Option A (direct node invocation — simpler):**
```bash
node ./node_modules/vite/bin/vite.js build
```
This bypasses the `npx` wrapper that Hermes misinterprets as a server starter.

**Option B (background + notify):**
```
terminal(command="npx vite build", background=true, notify_on_complete=true)
process(action="wait", session_id="...")
```
Prefers option A for speed; use B only when the direct path doesn't work.

### Socrata field names are case-sensitive
Chicago Data Portal (Socrata) field names use lowercase with underscores: `legal_name`, `doing_business_as_name`, `zip_code` — NOT `address_1`, `legalName`, etc. The original seed data in the reference files shows the wrong names that caused the failures. See `references/chicago-data-portal-fields.md` for the corrected field map.

## Verification

After scaffolding:
```bash
npx tsc --noEmit        # Must pass with zero errors
npx vite build          # Must produce dist/ with no warnings
```

Before shipping any feature: DataTable empty state renders, search returns results in <500ms, filters work independently and in combination, mobile layout doesn't break.

## References

- `references/chicago-data-portal-fields.md` — Correct Socrata field names for business licenses, 311 requests, and building permits
- `references/taste-skill-installation.md` — How to install and use the Leonxlnx/taste-skill package
- `references/dark-tool-page-pattern.md` — Dark-themed Ethereal Glass tool page pattern (fonts, layout, components, anti-patterns)

## Inputs

- `project_dir` (required) — the user's project; scaffold in place or a workspace subdirectory, then move files (never `/tmp` as the only copy — temp storage can be wiped)
- `entities` — framework-agnostic interfaces in `core/types`: Business, Institution, Precinct (+Captain, PollingLocation), ServiceTicket, CommunityEvent, WardMeta/WardMetrics/Initiative (adapt per domain)
- `data_sources` — Socrata/Chicago Data Portal clients (fetch, 3-attempt exponential-backoff retry, pagination; field names lowercase-underscore) or seed data (5–10 records per entity so the UI renders without an API)
- `design_tokens` + `audience` — civic/public-sector (Inter + JetBrains Mono, navy/sky/restrained accent) vs developer/premium tools (Geist Sans/Mono); data-dense dial settings (DESIGN_VARIANCE 4–5, MOTION 2–3, DENSITY 6–8); never AI-purple, never landing-page patterns on a data tool
- Not for: landing pages (`landing-page-build`), Python/FastAPI backends (`backend-dev`), throwaway experiments (`spike`)

## Outputs

- Layered `src/` tree built top-down (never skip a layer): `core/types` (zero project imports) → `core/schema` (Zod + validation engine) → `data/sources|transform|seed` → `features/` (self-contained, props-only, testable) → `ui/layout|data` → `lib/` → `router/` → `App.tsx`/`main.tsx`
- Data quality engine: `validateRecord`/`validateBatch` → `{valid[], invalid[]}`; staleness (>90d), unverified (`verifiedAt: null`), and missing-geo warnings; source tracking (`city_api | manual | import`)
- Reusable UI kit: generic `DataTable<T>`, `StatCard`, `Badge`, `SearchInput`, `FilterPills`; feature modules (directory, precinct finder, dashboard, events, intake form); `createBrowserRouter` shell
- Verification: `npx tsc --noEmit` zero errors, `npx vite build` clean `dist/`; per-feature: empty states render, search <500ms, filters compose, mobile holds
- Format: scaffolded project in the user's directory

## Example

Ward business directory: `npm create vite@latest . -- --template react-ts` → install `react-router-dom @tanstack/react-table zod fuse.js @phosphor-icons/react` + Tailwind v4 → `vite.config.ts` aliases (`@`, `@core`, `@data`, `@features`, `@ui`) → `core/types` (Business: license status, category, address, geo — `ward: number`, never hardcoded) → Zod schemas + `validateBatch` (invalid records quarantined, never silently dropped) → Socrata client (`$where`/`$select`, lowercase-underscore fields) → transform + validate → seed context provider (5–10 records/entity) → `DataTable`/`StatCard`/`SearchInput`/`FilterPills` → pure props-driven `BusinessDirectory` feature → router shell → `npx tsc --noEmit` zero errors, `npx vite build` clean.
