---
name: neon-postgres
description: "Neon Serverless Postgres playbook — the pooled-vs-direct connection decision table, Drizzle-first schema-as-code guidance, driver picks per runtime (Vercel, Cloudflare, Netlify, edge), and branching, autoscaling, scale-to-zero, instant restore, read replicas, pooling, and logical replication recipes — self-contained, with the parent neon skill as an optional companion. Use when users ask about Neon Serverless Postgres: connections, drivers, branching, or scaling."
---

> **Optional companion:** the parent `neon` skill (platform overview, getting-started recipes, development best practices) complements this one. **This skill is fully self-contained** -- every section below works without it.

> **If the parent skill is unavailable:** select your org/project with the Neon CLI (`neon projects list`) or the Neon console, then continue at "Get the connection string" below. Fetch the parent skill anytime from https://neon.com/docs/ai/skills/neon/SKILL.md or install it with:
>
> ```bash
> npx skills add neondatabase/agent-skills --skill neon
> ```

# Neon Serverless Postgres

Serverless Postgres is the core of the Neon platform. It separates compute and storage to offer autoscaling, branching, instant restore, and scale-to-zero. It's fully compatible with Postgres and works with any language, framework, or ORM that supports Postgres.

## Setup Flow

### 1. Select the organization and project

Use the CLI (default) or MCP server to list organizations and projects. Let the user select an existing project or create a new one. Check the `.neon` file for an existing linked project or branch.

### 2. Get the connection string

Use the CLI (default), `neon env pull`, or the MCP server to get the connection string. Store it in `.env` as `DATABASE_URL`. Read the file first before modifying it, to avoid overwriting existing values.

#### When to use pooled vs direct connections

| Use case                                 | Connection type  |
| ---------------------------------------- | ---------------- |
| Web applications, serverless functions   | Pooled (-pooler) |
| Schema migrations                        | Direct           |
| pg_dump / pg_restore                     | Direct           |
| Logical replication                      | Direct           |
| Long-running analytics with temp tables  | Direct           |
| Admin tasks needing SET or session state | Direct           |
| LISTEN / NOTIFY                          | Direct           |

### 3. Pick the connection method and driver

Always pair Neon with an ORM such as **Drizzle** for easy schema management and migrations. Refer to the connection methods guide to pick the correct driver based on how the runtime treats your code: https://neon.com/docs/connect/choose-connection.md.

Recommendations:

- Drizzle as ORM (see https://neon.com/docs/guides/drizzle.md)
- On Vercel, use `node-postgres` (`npm install pg`) with Vercel Fluid compute and `import { attachDatabasePool } from "@vercel/functions";`
- On Cloudflare, use `node-postgres` with Cloudflare Hyperdrive
- On Neon Functions, use `node-postgres`, as the functions are long-running and reuse the pool across requests.
- Use the `@neondatabase/serverless` driver for serverless and edge environments (for example, when using Netlify) — HTTP transport for one-shot queries, WebSocket for transaction support. Link: https://neon.com/docs/serverless/serverless-driver.md

### 4. Set up the schema

Manage schemas and migrations as code. Avoid running ad hoc schema migrations against your database, since they're hard to manage.

If you're using an ORM, follow your ORM's best practices to manage schemas and migrations. For example, if using Drizzle, only use Drizzle for schema and migration management unless instructed otherwise.

## Branching

Use this when the user is planning isolated environments, schema migration testing, preview deployments, or branch lifecycle automation.

Key points:

- Branches are instant, copy-on-write clones (no full data copy).
- Each branch has its own compute endpoint.
- Use the neon CLI or MCP server to create, inspect, and compare branches.

Link: https://neon.com/docs/introduction/branching.md

For detailed branch creation workflows (normal vs schema-only branches, reset-from-parent, CLI/MCP selection), the companion `neon-postgres-branches` skill adds step-by-step recipes -- optional, not required. If it isn't installed, fetch it from https://neon.com/docs/ai/skills/neon-postgres-branches/SKILL.md or install it with:

```bash
npx skills add neondatabase/agent-skills --skill neon-postgres-branches
```

**If that companion is unavailable:** the key points above plus the Neon CLI (`neon branches create --name <name>`) cover the same operations.

## Autoscaling

Use this when the user needs compute to scale automatically with workload and wants guidance on CU sizing and runtime behavior.

Link: https://neon.com/docs/introduction/autoscaling.md

## Scale to Zero

Use this when optimizing idle costs and discussing suspend/resume behavior, including cold-start trade-offs.

Key points:

- Idle computes suspend automatically after a default of 5 minutes; the timeout is configurable, and suspension can only be disabled on the Launch and Scale plans.
- First query after suspend typically has a cold-start penalty (around hundreds of ms)
- Storage remains active while compute is suspended.

Link: https://neon.com/docs/introduction/scale-to-zero.md

## Instant Restore

Use this when the user needs point-in-time recovery or wants to restore data state without traditional backup restore workflows.

Key points:

- History windows for instant restore depend on plan limits.
- Users can create branches from historical points-in-time.
- Time Travel queries can be used for historical inspection workflows.

Link: https://neon.com/docs/introduction/branch-restore.md

## Read Replicas

Use this for read-heavy workloads where the user needs dedicated read-only compute without duplicating storage.

Key points:

- Replicas are read-only compute endpoints sharing the same storage.
- Creation is fast and scaling is independent from primary compute.
- Typical use cases: analytics, reporting, and read-heavy APIs.

Link: https://neon.com/docs/introduction/read-replicas.md

## Connection Pooling

Use this when the user is in serverless or high-concurrency environments and needs safe, scalable Postgres connection management.

Key points:

- Neon pooling uses PgBouncer.
- Add `-pooler` to endpoint hostnames to use pooled connections.
- Pooling is especially important in serverless runtimes with bursty concurrency.

Link: https://neon.com/docs/connect/connection-pooling.md

## IP Allow Lists

Use this when the user needs to restrict database access by trusted networks, IPs, or CIDR ranges.

Link: https://neon.com/docs/introduction/ip-allow.md

## Logical Replication

Use this when integrating CDC pipelines, external Postgres sync, or replication-based data movement.

Key points:

- Neon supports native logical replication workflows.
- Useful for replicating to/from external Postgres systems.

Link: https://neon.com/docs/guides/logical-replication-guide.md

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `topic` | enum | required | `setup` | `connections` | `branching` | `autoscaling` | `scale_to_zero` | `restore` | `replicas` | `pooling` | `ip_allow` | `replication` |
| `runtime` | enum | -- | `vercel` | `cloudflare` | `netlify` | `node` -- picks the driver per the connection-methods guide. |
| `orm` | string | `drizzle` | ORM for schema-as-code (Drizzle recommended). |

## Outputs

- **Deliverable:** the connection setup (pooled vs. direct per the decision table), `DATABASE_URL` handling, and the topic's operational recipe.
- **Format:** chat walkthrough + code snippets + doc links.

## Example

> "Set up Neon for my new Vercel app."

1. Select (or create) the org/project -- Neon CLI by default; parent `neon` skill's recipes if installed.
2. Get the connection string -> store as `DATABASE_URL` in `.env` (read the file first; never overwrite existing values).
3. Vercel runtime -> pooled connection (`-pooler` hostname) + `node-postgres` with Vercel Fluid compute; Drizzle for schema/migrations as code.

## Errors & edge cases

- First query after idle is slow -> expected cold start from scale-to-zero (default 5-minute suspend); storage stays active.
- Connection storms from serverless -> use the pooled (`-pooler`) endpoint; direct connections are for migrations, pg_dump, replication, and LISTEN/NOTIFY.
- Ad-hoc schema changes -> manage schemas and migrations as code (Drizzle); avoid one-off migrations against the database.
- Parent `neon` skill missing -> everything above still works; use the CLI/console paths noted in the companion callout.
