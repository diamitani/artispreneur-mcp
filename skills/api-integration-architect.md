---
name: api-integration-architect
description: "LLM-agnostic developer tooling skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to design APIs end-to-end in six steps: requirements, RESTful routes, OpenAPI 3.1 specs, AI-friendly patterns (unique operationIds, structured errors, rate-limit headers), integration blueprints, and runnable Express/FastAPI/Hono/Next.js templates. Use when designing API schemas, building integrations, generating JSON schemas, or deploying API templates for AI assistants."
---

# API Integration Architect

## Overview

Designs API schemas, builds integration blueprints, generates JSON Schema / OpenAPI specs, and produces deployable API templates optimized for AI assistant consumption. Covers REST, webhooks, and AI-friendly API design patterns.

## When to Use

- Designing a new REST API from scratch
- Building integrations between third-party services
- Generating OpenAPI 3.1 specs for a GPT Action or MCP tool
- Creating JSON schemas for structured outputs
- Auditing an existing API for AI-friendliness
- Setting up webhook-based event-driven integrations
- Building an API gateway or middleware layer

## How It Works

1. **Requirements Elicitation** — Understand data models, operations, consumers.
2. **Schema Design** — Produce OpenAPI 3.1 + JSON Schema definitions.
3. **Integration Blueprint** — Map auth flows, error handling, rate limiting, retry logic.
4. **AI Optimization** — Ensure the API is consumable by AI agents (GPT Actions, MCP, function calling).
5. **Template Generation** — Produce runnable API templates (Express, FastAPI, Hono, Next.js Route Handlers).

## Steps

### Step 1: API Requirements
Document:
- **Resources**: What entities does the API manage? (users, orders, products, etc.)
- **Operations**: CRUD per resource + any custom actions
- **Consumers**: Who calls this API? (frontend, mobile, third-party, AI agent)
- **Auth model**: API keys, OAuth 2.0, JWT, session cookies
- **Rate limits**: What's the expected throughput?
- **Data formats**: JSON only, or multipart/form-data, SSE streaming?

### Step 2: RESTful Route Design
Follow REST conventions:
```
GET    /api/v1/products          → List products (paginated, filterable)
POST   /api/v1/products          → Create product
GET    /api/v1/products/:id      → Get product
PATCH  /api/v1/products/:id      → Update product (partial)
DELETE /api/v1/products/:id      → Delete product
POST   /api/v1/products/:id/clone → Custom action (use verb suffix)
```

### Step 3: OpenAPI 3.1 Specification
Generate a complete spec with:
```yaml
openapi: 3.1.0
info:
  title: [API Name]
  version: 1.0.0
  description: >
    [2-3 sentence description including primary use cases and consumers]
servers:
  - url: https://api.example.com/v1
    description: Production
paths:
  /products:
    get:
      operationId: listProducts
      summary: List all products
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        "200":
          description: Paginated product list
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ProductListResponse"
components:
  schemas:
    Product:
      type: object
      required: [id, name, price]
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 200
        price:
          type: number
          format: float
          minimum: 0
        created_at:
          type: string
          format: date-time
```

### Step 4: AI-Friendly API Design
For APIs consumed by AI agents, add these extras:
- **`x-ai-description`** extensions on endpoints explaining when/why an AI would call this
- **Structured error responses** with machine-parseable error codes
- **Idempotency keys** support for safe retries
- **Pagination cursors** over offset pagination (more reliable for agents)
- **Comprehensive `description` fields** on all schemas (AI reads these for context)
- **Minimal required fields** — AI agents may not have all data, prefer partial updates

### Step 5: Integration Blueprint
For third-party integrations, document:
```
Service: [Name]
Base URL: [https://...]
Authentication: [Type + token location]
Rate Limit: [X req / Y seconds]
Critical Endpoints:
  - POST /webhooks → Event ingestion
  - GET /sync → Full data sync
Error Strategy:
  - 429 → Exponential backoff (1s, 2s, 4s, 8s, max 60s)
  - 5xx → Retry up to 3 times with jitter
  - 4xx → Log, notify, do NOT retry
Webhook Verification: HMAC-SHA256 signature header
```

### Step 6: Generate API Template
Choose the framework and generate a runnable template:
- **Next.js**: Route Handlers in `app/api/` with Zod validation
- **Express**: Routes + middleware + error handler
- **FastAPI**: Path operations + Pydantic models
- **Hono**: Edge-compatible routes on Cloudflare Workers

## Common Pitfalls

- **Missing operationId**: AI agents and code generators rely on `operationId` to map to function names. Always include unique, descriptive operationIds.
- **Vague error responses**: `{ "error": "something went wrong" }` is useless. Return structured errors with codes, messages, and resolution hints.
- **No rate limit headers**: Always return `X-RateLimit-Remaining` and `Retry-After` headers so consumers can self-regulate.
- **Nested resources too deep**: `/users/:id/orders/:id/items/:id/notes` is a smell. Flatten or provide top-level endpoints with query filters.
- **Auth model mismatch**: Don't use API keys for user-specific data; don't use user sessions for service-to-service calls. Match auth to the consumer type.

## Source

Consolidates: API Integration Architect Pro GPT, API Guide GPT, Funky GPT.

## Inputs
- `resources` (list, required) - entities the API manages (users, orders, products...)
- `operations` (list) - CRUD per resource plus custom actions
- `consumers` (list) - frontend, mobile, third-party, AI agent
- `auth_model` (enum: api-key / oauth2 / jwt / session, required)
- `framework` (enum: express / fastapi / hono / nextjs) - for the template step

## Outputs
- RESTful route table following the six-step conventions
- Complete OpenAPI 3.1 spec with unique operationIds and structured error responses
- Integration blueprint: auth, rate limits, retry/backoff strategy, webhook verification
- Runnable API template in the chosen framework

## Example
Input: a products API for a Next.js storefront + a GPT Action consumer, JWT auth.
1. Resources: products; operations: list/get/create/update/delete/clone.
2. Routes: `GET /api/v1/products`, `POST /api/v1/products/:id/clone`, etc.
3. OpenAPI 3.1 with operationIds (listProducts...), structured errors, rate-limit headers.
4. Blueprint: JWT in Authorization header, 429 -> exponential backoff, HMAC webhook verification.
5. Next.js Route Handlers template with Zod validation.
