---
name: artispreneur-ecosystem
description: "LLM-agnostic skill for operating the Artispreneur multi-site web ecosystem - the shared dark-gold design DNA (tokens, sticky-navbar header, footer Ecosystem column), the five live Vercel sites, the deploy workflow (build locally first, npx vercel --prod, disable SSO protection), the mandatory verify-deploy.py loop, and the recipe for adding a new site. Use when building, deploying, or maintaining Artispreneur's sites."
---

# Artispreneur Ecosystem

Multi-site brand platform for Artispreneur. All sites share one design
system and deploy to Vercel. This skill is the operator's runbook:
design DNA, the deploy workflow, and the mandatory verification loop.

## Design DNA

Every Artispreneur site uses this design language:

| Token | Value |
|---|---|
| Background | near-black `#09090B` |
| Surface / card | `#111113` / `#18181B` |
| Border | `#252529` |
| Gold accent | `#C9A227` (hover `#E0B832`) |
| Text | `#FAFAFA`, muted `#A1A1AA`, dim `#63636B` |
| Sans | Inter |
| Serif | Playfair Display |
| Mono | Geist Mono |

Rules: dark backgrounds always; gold reserved for accents and CTAs;
headers use the sticky navbar pattern (logo + nav links + "Get Started
Free" CTA); footers carry an "Ecosystem" column linking all sites; no
emojis in UI; plain language for artists, not jargon.

## Live Sites (external — not bundled with this skill)

| Site | URL | Type |
|---|---|---|
| Platform Hub | `artispreneur-platform.vercel.app` | Static HTML |
| Landing + Workspace | `artispreneur-landing.vercel.app` | Static HTML |
| Academy | `academy-build.vercel.app` | Next.js |
| Directory | `directory-artispreneur.vercel.app` | Next.js |
| Rostr Contracts | `contractagent-artispreneur.vercel.app` | Next.js |

All deploy under the `artispreneur` Vercel team. Static HTML sites have
zero build step — Vercel serves them as static assets. Next.js sites
(academy, directory) build from their repos.

## Deploy Workflow

1. **Build locally first** (Next.js sites): `npm run build` must pass
   before anything is deployed. Never deploy with build failures.
2. **Deploy:** `npx -y vercel@latest --prod` from the site repo
   (the `vercel` binary is not on PATH; use npx).
3. **SSO check:** new Vercel projects have Deployment Protection enabled
   by default — hash URLs return HTTP 302 to the Vercel SSO page and the
   site is NOT publicly reachable. Disable right after first deploy or
   use a custom domain (custom domains bypass SSO).
4. **Verify:** run the bundled verification script against every page:

```bash
python3 scripts/verify-deploy.py \
  --site https://artispreneur-landing.vercel.app \
  --routes / /pricing.html /workspace.html /signup.html
```

The script checks HTTP 200 on each route and flags SSO-blocked sites.
It exits nonzero on any failure — a deploy is not done until it exits 0.

## Verification Loop (mandatory)

After every deploy, before telling the user it's done:

1. Run `scripts/verify-deploy.py` for the deployed site (all key routes).
2. Confirm the fresh **production hash URL** from the Vercel output
   (the `https://<name>-<hash>-<team>.vercel.app` line) — copy it
   verbatim and send it to the user along with the alias. Never assume
   they'll find it.
3. Spot-check cross-links: nav links, footer Ecosystem column, and any
   links between sites resolve.

## Adding a New Site to the Ecosystem

1. Clone the closest existing site repo (static HTML for landing-style
   pages, the academy repo for course-style sites).
2. Strip the old site's content thoroughly — copy, images, data files,
   and any backend references.
3. Apply the Design DNA tokens and the shared header/footer pattern.
4. Add the new site to the footer Ecosystem column of every other site.
5. Deploy, disable SSO protection, and run the verification loop.

## Domain Management

- Custom domains are added in the Vercel dashboard (project settings →
  domains), then DNS is pointed at Vercel (A record `76.76.21.21` or
  CNAME `cname.vercel-dns.com`).
- SSL provisions automatically after DNS propagates.
- Keep a record of which domain maps to which project — the alias alone
  is not enough when debugging.

## Scripts

- `scripts/verify-deploy.py` — HTTP-status verification for deployed
  sites. See `--help` for the multi-site JSON config format.

## Inputs
- `site` (string, required) - which ecosystem site (platform hub, landing, academy, directory, contracts, or a new site)
- `change` (string, required) - what to build, deploy, or maintain
- `repo_path` (string) - local clone of the site's repo

## Outputs
- Deployed site via `npx -y vercel@latest --prod` with SSO protection disabled
- verify-deploy.py exit 0 across all key routes (HTTP 200, no SSO blocks)
- Fresh production hash URL reported verbatim alongside the alias
- For new sites: ecosystem footer column updated on all sites

## Example
Input: deploy the landing site update.
1. `npm run build` locally - must pass before deploying (static HTML sites skip this).
2. `npx -y vercel@latest --prod` from the repo; disable SSO protection on the new deployment.
3. `python3 scripts/verify-deploy.py --site https://artispreneur-landing.vercel.app --routes / /pricing.html /workspace.html /signup.html`.
4. Report the fresh hash URL verbatim; spot-check nav and footer Ecosystem links.

## Errors & edge cases
- Deploy returns HTTP 302 to a Vercel SSO page: Deployment Protection is on - disable it or attach a custom domain (custom domains bypass SSO).
- verify-deploy.py exits nonzero: the deploy is not done - fix routes and re-verify before telling the user.
- Adding a new site: strip the cloned repo's old content thoroughly (copy, images, data, backend refs) before applying the Design DNA.
