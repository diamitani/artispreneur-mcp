---
name: observability
description: "Adds tracing, telemetry, and observability to an assistant-ui backend — per-call `experimental_telemetry` on `streamText`/`generateText`, provider routing (Langfuse via OpenTelemetry span processor in `instrumentation.ts`, LangSmith via `wrapAISDK`, Helicone via proxy baseURL with no OTel), and renders collected spans as a trace waterfall with the `@assistant-ui/react-o11y` headless primitives (`SpanResource`, `SpanPrimitive`). Consult assistant-ui.com/llms.txt for the latest API. Use when wiring an AI SDK route handler to a tracing backend or rendering collected spans with react-o11y."
---

# assistant-ui Observability

**Always consult [assistant-ui.com/llms.txt](https://www.assistant-ui.com/llms.txt) for the latest API.**

Tracing and telemetry for an assistant-ui backend. Most of this is generic AI SDK telemetry; the assistant-ui specific part is the route handler and the `@assistant-ui/react-o11y` client primitives for rendering spans.

## Contents

- [References](#references)
- [Where it plugs in](#where-it-plugs-in)
- [Provider routing](#provider-routing)
- [AI SDK telemetry (shared)](#ai-sdk-telemetry-shared)
- [Helicone (proxy, no OTel)](#helicone-proxy-no-otel)
- [Visualizing spans with react-o11y](#visualizing-spans-with-react-o11y)
- [Common Gotchas](#common-gotchas)
- [Related Skills](#related-skills)

## References

- [./references/langfuse.md](./references/langfuse.md) -- Langfuse tracing
- [./references/langsmith.md](./references/langsmith.md) -- LangSmith tracing
- [./references/helicone.md](./references/helicone.md) -- Helicone proxy
- [./references/react-o11y.md](./references/react-o11y.md) -- @assistant-ui/react-o11y client primitives

## Where it plugs in

Telemetry attaches to the **server route** that calls `streamText`/`generateText`, not to the React runtime. The frontend (`useChatRuntime`, `Thread`) is unchanged. `react-o11y` is a separate, optional client layer for drawing the trace waterfall in your own UI.

```
Thread (frontend) ──> /api/chat (streamText) ──> tracing backend
                                              └─> react-o11y (optional UI)
```

## Provider routing

```
Langfuse   → OTel span processor + experimental_telemetry, propagateAttributes
LangSmith  → wrapAISDK(ai) wrapper, no OTel setup
Helicone   → proxy baseURL on the provider, no telemetry flag
react-o11y → client primitives to render spans you collected
```

## AI SDK telemetry (shared)

Langfuse and any OTel backend reuse the AI SDK `experimental_telemetry` flag. Enable it per call:

```ts
import { openai } from "@ai-sdk/openai";
import { streamText, convertToModelMessages } from "ai";
import type { UIMessage } from "ai";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const result = streamText({
    model: openai("gpt-5.4-nano"),
    messages: await convertToModelMessages(messages),
    experimental_telemetry: { isEnabled: true },
  });
  return result.toUIMessageStreamResponse();
}
```

For Langfuse, register an OTel span processor in `instrumentation.ts` and wrap the call so traces carry `userId`/`sessionId`:

```ts
import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor } from "@langfuse/otel";

export const langfuseSpanProcessor = new LangfuseSpanProcessor();

export async function register() {
  if (process.env.NEXT_RUNTIME !== "nodejs") return;
  const sdk = new NodeSDK({ spanProcessors: [langfuseSpanProcessor] });
  sdk.start();
}
```

```ts
import { propagateAttributes } from "@langfuse/tracing";

const result = await propagateAttributes(
  { traceName: "chat-completion", userId, sessionId },
  async () =>
    streamText({
      model: openai("gpt-5.4-nano"),
      messages: await convertToModelMessages(messages),
      experimental_telemetry: { isEnabled: true },
    }),
);
```

LangSmith skips OTel entirely; wrap the `ai` module instead. `convertToModelMessages` is not wrapped, so import it from `ai` directly:

```ts
import * as ai from "ai";
import { wrapAISDK } from "langsmith/experimental/vercel";
import { openai } from "@ai-sdk/openai";

const { streamText } = wrapAISDK(ai);

const result = streamText({
  model: openai("gpt-5.4-nano"),
  messages: await ai.convertToModelMessages(messages),
});
return result.toUIMessageStreamResponse();
```

See the per provider reference files for env vars, metadata tagging, and serverless flushing.

## Helicone (proxy, no OTel)

Helicone needs no telemetry flag. Point the provider at the proxy `baseURL` and pass the auth header:

```ts
import { createOpenAI } from "@ai-sdk/openai";

const openai = createOpenAI({
  baseURL: "https://oai.helicone.ai/v1",
  headers: { "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}` },
});
```

Use this `openai` instance with `streamText` as usual; streaming, tools, and attachments are unchanged.

## Visualizing spans with react-o11y

`@assistant-ui/react-o11y` gives headless primitives to render collected spans as a trace waterfall. Feed it `SpanData[]` (id, parentSpanId, name, type, status, startedAt, endedAt, latencyMs) via `SpanResource`, mount with `useAui`, and render `SpanPrimitive` parts.

```bash
npm install @assistant-ui/react-o11y
```

```tsx
import {
  SpanResource,
  SpanPrimitive,
  type SpanData,
} from "@assistant-ui/react-o11y";
import { AuiProvider, useAui } from "@assistant-ui/store";

function SpanRow() {
  return (
    <SpanPrimitive.Root>
      <SpanPrimitive.Indent />
      <SpanPrimitive.CollapseToggle />
      <SpanPrimitive.StatusIndicator />
      <SpanPrimitive.TypeBadge />
      <SpanPrimitive.Name />
    </SpanPrimitive.Root>
  );
}

export function TraceView({ spans }: { spans: SpanData[] }) {
  const aui = useAui({ resource: SpanResource({ spans }) });
  return (
    <AuiProvider value={aui}>
      <SpanPrimitive.Children components={{ Span: SpanRow }} />
    </AuiProvider>
  );
}
```

`SpanPrimitive.Children` flattens the tree to a visible list and wraps each item in `SpanByIndexProvider`. `Root` exposes `data-span-status`, `data-span-type`, `data-span-depth`, and `data-collapsed` for styling. See [react-o11y.md](./references/react-o11y.md) for the full part list and `SpanState` shape.

## Common Gotchas

**No traces on Vercel/Lambda**
- The function exits before OTel flushes its buffer. Langfuse: `await langfuseSpanProcessor.forceFlush()` before responding. LangSmith: `await new Client().awaitPendingTraceBatches()`.

**Langfuse traces empty**
- `experimental_telemetry: { isEnabled: true }` must be set on each `streamText`/`generateText` call.
- The span processor only registers when `process.env.NEXT_RUNTIME === "nodejs"`; OTel does not run on the edge runtime.

**LangSmith not tracing**
- Use the destructured methods from `wrapAISDK(ai)`, not the originals from `ai`. `LANGSMITH_TRACING=true` must be set.

**Helicone requests still hit OpenAI directly**
- Confirm requests go to `oai.helicone.ai`, not `api.openai.com`, and carry both `Helicone-Auth` and `Authorization` headers.

**react-o11y renders nothing**
- Primitives must render inside `AuiProvider`; the resource mounts through `useAui({ resource: SpanResource({ spans }) })`.

## Related Skills

- `/streaming` - The route handler and stream response telemetry attaches to
- `/setup` - Backend wiring (`ai-sdk`, `custom-backend`) where the route lives
- `/cloud` - Persistence; pair `userId`/`sessionId`/`threadId` with trace attributes

## Inputs

- Backend route (required) — the server route calling `streamText`/`generateText` → `toUIMessageStreamResponse` (telemetry attaches to the route, not the React runtime; the frontend `Thread`/`useChatRuntime` is unchanged)
- `provider` — Langfuse (OTel span processor) | LangSmith (`wrapAISDK(ai)` wrapper, no OTel) | Helicone (proxy baseURL, no telemetry flag) | react-o11y (client primitives to render spans you collected)
- Provider credentials/env vars and metadata tagging per the reference files: `./references/langfuse.md`, `./references/langsmith.md`, `./references/helicone.md`, `./references/react-o11y.md`
- `userId`/`sessionId` (and `threadId`) to propagate as trace attributes

## Outputs

- An instrumented route handler emitting traces to the chosen backend: Langfuse via `LangfuseSpanProcessor` registered in `instrumentation.ts` + `propagateAttributes`; LangSmith via destructured methods from `wrapAISDK(ai)` (`LANGSMITH_TRACING=true`); Helicone via proxy baseURL + `Helicone-Auth` header
- Serverless flush handling (Langfuse `forceFlush()`, LangSmith `awaitPendingTraceBatches()`)
- Optional span waterfall UI: feed `SpanData[]` (id, parentSpanId, name, type, status, startedAt, endedAt, latencyMs) into `SpanResource` via `useAui`, mount `AuiProvider`, render `SpanPrimitive` parts (`Root`, `Indent`, `CollapseToggle`, `StatusIndicator`, `TypeBadge`, `Name`) with `data-span-*` styling hooks
- Format: wired route code + per-provider reference notes

## Example

Wire Langfuse: add `experimental_telemetry: { isEnabled: true }` to the `streamText` call in `/api/chat` → register `LangfuseSpanProcessor` in `instrumentation.ts` (NodeSDK; only when `process.env.NEXT_RUNTIME === 'nodejs'` — OTel doesn't run on edge) → wrap the call in `propagateAttributes({ traceName: 'chat-completion', userId, sessionId }, ...)` → on Vercel/Lambda, `await langfuseSpanProcessor.forceFlush()` before responding (the function exits before OTel flushes otherwise) → traces appear in Langfuse tagged by user/session. Helicone needs no telemetry flag: point the provider at `https://oai.helicone.ai/v1` with `Helicone-Auth`.
