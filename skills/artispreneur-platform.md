---
name: artispreneur-platform
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to build and maintain the Artispreneur multi-product music business platform in the single master repo (github.com/diamitani/artispreneur-v217): five product families (Pro Toolkit, Directory & Outreach, Academy, Core, Cataba Publishing) under one dark-gold design system, a unified signup flow, Stripe pricing tiers, and hard user preferences (verify before done, unified headers, plain language for artists). Use when you need to build and maintain the Artispreneur multi-product."
---

# Artispreneur Platform Builder

## Trigger

When the user asks to build, update, deploy, or maintain any part of the Artispreneur ecosystem — landing pages, agent workspace, academy, directory, pricing, signup flow, architecture docs, or investment materials.

## Master Repo (external — not bundled with this skill)

All work happens in the user's repository:

```
github.com/diamitani/artispreneur-v217
```

Everything lives in ONE master repo. Do not create separate repos for separate products. 5 product families coexist under one codebase:
- **Pro Toolkit** — Contract Agent + EPK Builder
- **Directory & Outreach** — Outreach Agent + CRM + contact directory
- **Academy** — Tutor Agent + courses
- **Core** — Master Agent + Business Registration + PAL onboarding
- **Cataba Publishing** — Catalog Agent + splitsheets + ISRC

File paths named below (e.g. `index.html`, `backend/`, `terraform/main.tf`)
are locations **inside that repository** — user-side project files, never
skill-bundled resources.

## Design System

```css
:root {
  --bg: #09090b;         /* Near-black */
  --surface: #111113;    /* Card backgrounds */
  --card: #18181b;       /* Elevated cards */
  --border: #252529;     /* Borders */
  --text: #fafafa;       /* Primary text */
  --text-muted: #a1a1aa; /* Secondary text */
  --text-dim: #63636b;   /* Dim text */
  --gold: #c9a227;       /* Brand gold */
  --gold-light: #e0b832; /* Hover gold */
  --gold-subtle: rgba(201,162,39,0.08);
}
```

**Fonts:** Inter (body), Playfair Display (headings), Geist Mono (code)
**Logo:** the repo's wordmark PNG — always use `<img>` with height 22px
**Header pattern:** Sticky navbar with logo + "Artispreneur" text (gold on "preneur") + nav links (Rostr Agent, Academy, Directory, Pricing, Login) + "Get Started Free" CTA button

## Architecture

**Unified signup flow (ALL products):**
```
Sign Up → PAL Onboarding → ROSTR Compiles Soul.md → Provision Workspace → Install Tools → Agent Dashboard
```

**Multi-tenant Hermes runtime** — NOT per-user EC2. Free/Artist/Pro share one Hermes instance with isolated namespaces. Only Label/Enterprise gets dedicated EC2.

**AWS backend:** Cognito (auth), RDS PostgreSQL (data), S3 (outputs/assets), Lambda (FastAPI), Bedrock (LLM), CloudFront (CDN), ElastiCache (sessions)

**Deploy:** GitHub push → Vercel auto-deploy → rostragent.com

## Stripe Pricing

| Tier | Monthly | Annual | Chats | Skills | PDFs | Storage |
|------|---------|--------|-------|--------|------|---------|
| Free | $0 | $0 | 10 + BYOK | — | — | — |
| Artist | $12 | $99 | 200 | 20 | 50 | 1GB |
| Pro | $25 | $199 | Unlimited | Unlimited | Unlimited | 5GB |
| Label | $59 | $499 | Unlimited | Unlimited | Unlimited | 10GB (5 seats) |

Stripe products and keys live in the user's own finance records — never
in this skill. When wiring checkout, ask the user for the price/product
IDs for the tier being built.

## User Preferences

- **After every deploy:** CONFIRM with the user AND send the fresh Vercel production URL (the hash URL, not just the alias). Never assume they'll find it.
- **Before claiming done:** verify all pages, cross-links, and end-to-end data flow (signup → login → workspace).
- **Headers must be unified** across ALL pages — same logo, nav, CTA. Check this on every build.
- **Design for the actual user** (indie artist who doesn't know jargon). Use plain language. "Register your songs" not "PRO registration".
- **Code quality:** modular, clean, short files, production-grade.
- **Frustration = fix immediately.** If the user says something doesn't work, stop and fix it — don't argue.

## Repo Layout (user's repository)

| Path in repo | Purpose |
|------|---------|
| `index.html` | Landing page with chat UI |
| `workspace.html` | Rostr Agent workspace (agents, sidebar, chat) |
| `signup.html` | PAL onboarding wizard |
| `login.html` | Email/password auth |
| `pricing.html` | Stripe checkout (annual toggle) |
| `success.html` | Post-checkout confirmation |
| `skills.html` | Skill Builder + PDF generation |
| `academy.html` | Courses listing |
| `directory.html` | Contacts with filters |
| `architecture.html` | Full system architecture visual |
| `investment.html` | One-pager for investors |
| `backend/` | Python modules, agents |
| `terraform/main.tf` | AWS infrastructure |

## Inputs
- `product` (enum: pro-toolkit / directory-outreach / academy / core / cataba-publishing, required)
- `task` (string, required) - build, update, deploy, or maintain
- `repo_path` (string) - local clone of artispreneur-v217 (never create separate repos per product)

## Outputs
- Changes inside the master repo following the repo layout (index.html, workspace.html, signup.html, pricing.html...)
- Dark-gold design system applied: CSS tokens, Inter/Playfair/Geist fonts, sticky navbar, "Get Started Free" CTA
- Post-deploy: fresh Vercel hash URL confirmed with the user; pages, cross-links, and signup->login->workspace flow verified

## Example
Input: add the Academy tutor agent page.
1. Work in artispreneur-v217 under Academy; no new repo.
2. Apply the design system tokens and unified header/footer.
3. Deploy via the ecosystem workflow; confirm the fresh hash URL with the user.
4. Verify: nav links, unified header across pages, end-to-end signup -> workspace flow.

## Errors & edge cases
- Stripe pricing needed: ask the user for price/product IDs - they live in the user's own finance records, never in the skill.
- "Frustration" signal from the user: stop and fix immediately, do not argue.
- Jargon in artist-facing copy: rewrite in plain language ("Register your songs", not "PRO registration").
