---
name: metering-and-billing
description: "Adds usage metering, monthly quotas, and Stripe subscription billing to any Next.js App Router app in ~30 minutes via a drop-in template — a usage-collector normalizing LLM calls to costed events, a Supabase (or in-memory) usage store, a per-customer monthly quota gate returning 402 + `upgrade_url`, and six Stripe routes (plans, checkout, webhook, portal, success). Use when you need to meter per-user LLM cost, enforce a paywalled free tier, or sell monthly subscriptions."
---

# Metering and Billing

Add usage metering, monthly quotas, and Stripe subscriptions to any
Next.js (App Router) app in about 30 minutes. The implementation lives in
a drop-in template so you never rewrite it per app:

```
https://github.com/diamitani/rostr-platform/tree/template/metering-billing/templates/metering-billing
```

## When to use this skill

- The app makes paid LLM or API calls on behalf of users and you need to
  know what each user costs you.
- You want a free tier with a hard monthly cap, and a paywall the moment
  it is hit.
- You want to sell a monthly subscription with Stripe and have customer
  plans upgrade/downgrade automatically.
- You run several apps and want the same billing pattern in all of them.

## Architecture

```
user action ──▶ quota gate ──▶ your LLM work ──▶ usage events ──▶ Supabase
   │                │                                        │
   │           over quota? ──▶ 402 { code:"quota_exceeded",  │
   │                           upgrade_url }                ▼
   │                                              GET /api/usage (dashboard)
   ▼
Stripe Checkout ──▶ webhook ──▶ plan: free → pro ──▶ quota raised
```

Four pieces, each independent:

1. **Meter** (usage-collector module) — `reportLlmCall()` normalizes one
   LLM call (model, tokens, USD cost). It prefers the provider's reported
   cost and falls back to a price table, marking the result estimated.
   `UsageCollector` gathers the calls for one unit of work and converts
   them into events: one `call` event per LLM call plus one aggregate
   `run` event that quota counting is based on.
2. **Store** (metering module) — `UsageStore` with a Supabase backend
   (two tables, service-role key, RLS on) and an in-memory fallback for
   local dev. `recordEvents()` never throws; store failures are swallowed
   with a warning so metering can never break the product.
3. **Quota** (`enforceQuota()`) — per customer per calendar month. Returns
   `null` when the customer may proceed, otherwise an HTTP **402**
   response with `{ code: "quota_exceeded", upgrade_url }` that the
   frontend turns into a paywall.
4. **Bill** (six API routes + Stripe) — Checkout sells the paid plan, the
   webhook flips the plan on `checkout.session.completed` and back on
   `customer.subscription.deleted`, the portal route manages the
   subscription. Without Stripe keys the billing routes answer 501 and
   the paywall stays open — the app keeps working.

Customer identity needs no auth framework: the host app passes its own
user id (`user:<id>`), or the request carries `Authorization: Bearer`,
which is hashed to `key:<sha256[:16]>`. Raw keys are never stored.

## Install from the template

### 1. Copy the files (5 min)

Copy the template into the app, keeping the relative layout:

```
billing.config.ts      →  lib/billing.config.ts
lib/metering.ts        →  lib/metering.ts
lib/usage-collector.ts →  lib/usage-collector.ts
app/api/usage          →  app/api/usage
app/api/billing        →  app/api/billing
```

All imports inside the template are relative, so the files work wherever
you put them (fix the one config import if you move things).
If the app already has `/api/usage` or `/api/billing/*` routes, relocate
the template's and update the upgrade URL builder in the metering module.

### 2. Install the Stripe SDK (2 min)

```
npm install stripe
```

### 3. Set env vars (5 min)

Minimum for local dev: nothing (memory store, open paywall). For
production:

```
SUPABASE_URL / SUPABASE_SERVICE_KEY   durable usage storage
STRIPE_SECRET_KEY / STRIPE_PRICE_ID   sell the plan
STRIPE_WEBHOOK_SECRET                 verify webhook signatures
BILLING_APP_NAME                      branding in plan responses
BILLING_FREE_RUNS / BILLING_PRO_RUNS  quotas per plan
BILLING_PRO_PRICE_USD                 display price (real charge = Stripe Price)
```

### 4. Run the SQL migration (3 min)

Run the SQL migration from the template once in the Supabase SQL editor.
It creates `billing_customers` and `usage_events` with RLS enabled. One
Supabase project serves many apps — pass a distinct `projectId` per app
when collecting (step 5).

### 5. Wire the two snippets (10 min)

Gate the expensive route, collect one report per LLM call, flush in a
`finally` block. Works with any LLM provider:

```ts
import { randomUUID } from "node:crypto";
import {
  customerIdForRequest,
  enforceQuota,
  usageStoreFromEnv,
} from "./lib/metering";
import { UsageCollector, reportLlmCall } from "./lib/usage-collector";

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));

  // Who is this? Your app's authenticated user id, or a Bearer API key.
  const customerId = customerIdForRequest(req, body.user_id);
  if (!customerId)
    return Response.json({ error: "unauthorized" }, { status: 401 });

  // Quota gate — over quota returns 402, the frontend shows the paywall.
  const blocked = await enforceQuota(req, customerId);
  if (blocked) return blocked;

  const collector = new UsageCollector({
    customerId,
    projectId: "my-app",
    runId: randomUUID(),
  });
  try {
    const res = await callYourLlm(/* ... */);
    collector.add(
      reportLlmCall({
        model: "anthropic/claude-sonnet-4-6",
        promptTokens: res.usage?.input_tokens,
        completionTokens: res.usage?.output_tokens,
        // Best: the real cost when the provider reports it.
        reportedCostUsd: res.providerMetadata?.gateway?.cost,
      })
    );
    return Response.json({ ok: true });
  } finally {
    await usageStoreFromEnv().recordEvents(collector.toEvents());
  }
}
```

### 6. Stripe dashboard (5 min)

1. Products → new product → recurring monthly price → copy the `price_…`
   id into `STRIPE_PRICE_ID`.
2. Developers → Webhooks → add endpoint
   `https://YOUR-APP.com/api/billing/webhook`, subscribe to
   `checkout.session.completed` and `customer.subscription.deleted` →
   copy the `whsec_…` secret into `STRIPE_WEBHOOK_SECRET`.
3. Settings → Billing → Customer portal → activate (needed for the
   portal route).

### 7. Test the quota block

Set `BILLING_FREE_RUNS=1` and hit the gated route twice: first call
returns 200, the second returns 402 with `code: "quota_exceeded"` and an
`upgrade_url`. Then check the readout:

```
GET /api/usage?user_id=test-user
→ { plan: "free", runs_this_month: 1, runs_quota: 1, spend_usd: 0.0123 }
```

Paid flow (Stripe test mode, card `4242 4242 4242 4242`): POST
`/api/billing/checkout` → open the returned URL → complete → webhook
fires → `/api/usage` shows `plan: "pro"` with the bigger quota. Cancel in
the dashboard → webhook → back to `free`.

## Adapting plans per app

Plans are env-driven — no code changes to rebrand:

- `BILLING_APP_NAME` — shown in plan and success responses.
- `BILLING_FREE_RUNS` / `BILLING_PRO_RUNS` — monthly run quotas.
- `BILLING_PRO_PRICE_USD` — display price; the real charge is the Stripe
  Price, so the number customers see always matches Stripe.
- `BILLING_UPGRADE_URL` — override for the 402 upgrade link (defaults to
  the app's own `/api/billing/plans`).
- `BILLING_PAID_PLAN_ID` / `BILLING_FREE_PLAN_ID` — the plan ids the
  webhook flips between.

For three or more tiers, add entries to the plans map in
the billing config file, create the matching Stripe Prices, and pass
`price_id` in the checkout body to sell a specific tier.

## API reference

| Route | Method | Auth | Purpose |
|---|---|---|---|
| `/api/usage?user_id=` | GET | user id or Bearer | plan, runs used, quota, metered spend |
| `/api/billing/plans` | GET | none | public plan list (paywall target) |
| `/api/billing/checkout` | POST | user id or Bearer | `{ user_id?, price_id? }` → `{ url }` |
| `/api/billing/webhook` | POST | Stripe signature | plan flips; register in dashboard |
| `/api/billing/portal` | POST | user id or Bearer | `{ url }` billing-portal session |
| `/api/billing/success?session_id=` | GET | none | verifies session, reports plan |

## Rolling it out across apps

The same template drops into every app unchanged; only the env vars and
the `projectId` differ per app. Suggested order: the app with real users
first (it pays for itself immediately), then the rest. Each app gets its
own Stripe product/price and webhook endpoint, but they can all share one
Supabase project — usage stays separated by `project_id`, and customer
ids are namespaced by each app's own user ids or API keys.

## Inputs

- The drop-in template: `github.com/diamitani/rostr-platform/tree/template/metering-billing/templates/metering-billing` — copy 5 paths into the app keeping relative layout (all imports relative)
- Env: `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` (durable storage; omit for local-dev memory store) · `STRIPE_SECRET_KEY` / `STRIPE_PRICE_ID` / `STRIPE_WEBHOOK_SECRET` · `BILLING_APP_NAME` · `BILLING_FREE_RUNS` / `BILLING_PRO_RUNS` (monthly run quotas) · `BILLING_PRO_PRICE_USD` (display; the real charge is the Stripe Price)
- The expensive route to gate + the LLM call to meter (`reportLlmCall({model, promptTokens, completionTokens, reportedCostUsd})` — provider-reported cost preferred, price-table fallback marked estimated)
- `projectId` per app (one Supabase project serves many apps); webhook endpoint `https://YOUR-APP.com/api/billing/webhook` subscribed to `checkout.session.completed` + `customer.subscription.deleted`

## Outputs

- Four pieces: **Meter** (`reportLlmCall` + `UsageCollector` → one `call` event per LLM call + one aggregate `run` event for quota counting) · **Store** (`UsageStore`: Supabase two-table backend, RLS on, in-memory fallback) · **Quota** (`enforceQuota()`: per customer per calendar month — `null` = proceed, else HTTP **402** `{code: "quota_exceeded", upgrade_url}` → frontend paywall) · **Bill** (six routes: usage readout, plans, checkout, webhook, portal, success)
- `GET /api/usage?user_id=` → `{plan, runs_this_month, runs_quota, spend_usd}`; webhook flips `free ↔ pro` on checkout/session-completed and subscription-deleted; plans are env-driven (rebrand without code changes; 3+ tiers via the plans map + `price_id` in the checkout body)
- Format: installed template + 6 API routes + one SQL migration; roll out app by app, each with its own Stripe product/price/webhook

## Example

Wire the chat route: copy the template files (`billing.config.ts → lib/`, `lib/metering.ts`, `lib/usage-collector.ts`, `app/api/usage`, `app/api/billing`) → `npm install stripe` → set env (`BILLING_FREE_RUNS=10`, `STRIPE_PRICE_ID=price_…`, `STRIPE_WEBHOOK_SECRET=whsec_…`) → run the SQL migration (`billing_customers`, `usage_events`, RLS on) → gate `POST` with `enforceQuota` + `UsageCollector`/`reportLlmCall` in a try/finally → test: `BILLING_FREE_RUNS=1`, hit twice → 200 then **402** `{code: "quota_exceeded", upgrade_url}` → Stripe test mode (4242…) checkout → webhook flips plan to `pro` with the bigger quota.

## Errors & edge cases

- **Store failures are swallowed with a warning** — `recordEvents()` never throws, so metering can never break the product; check logs if usage looks under-counted.
- **Without Stripe keys**, the billing routes answer 501 and the paywall stays open — the app keeps working; this is the local-dev default (memory store, open paywall), not a bug.
- **Route collision**: if the app already has `/api/usage` or `/api/billing/*`, relocate the template's routes and update the upgrade-URL builder in the metering module.
- **Raw API keys are never stored** — a Bearer key is hashed to `key:<sha256[:16]>`; customer identity is the host app's own user id (`user:<id>`) with no auth framework required.
- **One Supabase project serves many apps** — pass a distinct `projectId` per app when collecting, or usage mixes across apps.
