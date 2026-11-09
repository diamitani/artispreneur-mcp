---
name: assistant-ui
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to act as the overview and router for assistant-ui, the React library for building AI chat interfaces from composable primitives: the layered model (primitives -> context hooks -> runtime -> adapters), a runtime-picker decision tree (useChatRuntime, external store, LangGraph, AG-UI, A2A, local), the six core packages, and a quick-start chat wired to an API route - always checking assistant-ui.com/llms.txt for the latest API. Use when high-level, cross-cutting, or architecture-overview questions arise: choosing packages, picking a runtime, or understanding the layered model (RuntimeCore, Runtime, context)."
---

# assistant-ui

**Always consult [assistant-ui.com/llms.txt](https://www.assistant-ui.com/llms.txt) for the latest API.**

React library for building AI chat interfaces with composable primitives.

## References

- [./references/architecture.md](./references/architecture.md) -- Core architecture and layered system
- [./references/packages.md](./references/packages.md) -- Package overview and selection guide

## When to Use

| Use Case | Best For |
|----------|----------|
| Chat UI from scratch | Full control over UX |
| Existing AI backend | Connects to any streaming backend |
| Custom message types | Tools, images, files, custom parts |
| Multi-thread apps | Built-in thread list management |
| Production apps | Cloud persistence, auth, analytics |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  UI Components (Primitives)             │
│    ThreadPrimitive, MessagePrimitive, ComposerPrimitive │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Context Hooks                         │
│   useAui, useAuiState, useAuiEvent │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Runtime Layer                        │
│  AssistantRuntime → ThreadRuntime → MessageRuntime      │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Adapters/Backend                      │
│   AI SDK · LangGraph · Custom · Cloud Persistence       │
└─────────────────────────────────────────────────────────┘
```

## Pick a Runtime

```
Using AI SDK?
├─ Yes → useChatRuntime (recommended)
└─ No
   ├─ External state (Redux/Zustand)? → useExternalStoreRuntime
   ├─ LangGraph agent? → useLangGraphRuntime
   ├─ AG-UI protocol? → useAgUiRuntime
   ├─ A2A protocol? → useA2ARuntime
   └─ Custom API → useLocalRuntime
```

## Core Packages

| Package | Purpose |
|---------|---------|
| `@assistant-ui/react` | UI primitives & hooks |
| `@assistant-ui/react-ai-sdk` | Vercel AI SDK v6 adapter |
| `@assistant-ui/react-langgraph` | LangGraph adapter |
| `@assistant-ui/react-markdown` | Markdown rendering |
| `assistant-stream` | Streaming protocol |
| `assistant-cloud` | Cloud persistence |

## Quick Start

```tsx
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { Thread } from "@/components/assistant-ui/thread";
import { useChatRuntime, AssistantChatTransport } from "@assistant-ui/react-ai-sdk";

function App() {
  const runtime = useChatRuntime({
    transport: new AssistantChatTransport({ api: "/api/chat" }),
  });
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  );
}
```

## State Access

```tsx
import { useAui, useAuiState } from "@assistant-ui/react";

const api = useAui();
api.thread().append({ role: "user", content: [{ type: "text", text: "Hi" }] });
api.thread().cancelRun();

const messages = useAuiState(s => s.thread.messages);
const isRunning = useAuiState(s => s.thread.isRunning);
```

## Related Skills

- `/setup` - Installation and configuration
- `/primitives` - UI component customization
- `/runtime` - State management deep dive
- `/tools` - Tool registration and UI
- `/streaming` - Streaming protocols
- `/cloud` - Persistence and auth
- `/thread-list` - Multi-thread management
- `/update` - Version updates and migrations

## Inputs
- `question_type` (enum: package-choice / runtime-choice / architecture-overview / quick-start, required)
- `backend` (string) - AI SDK, LangGraph, custom API, external store (Redux/Zustand)...
- `needs` (list) - threads, custom message types, cloud persistence, auth...

## Outputs
- Recommended package set from the core packages table with rationale
- Runtime pick from the decision tree with the wiring snippet
- Pointers to references/architecture.md and references/packages.md for depth

## Example
Input: "I have a Vercel AI SDK backend and want a multi-thread chat UI."
1. Backend = AI SDK -> useChatRuntime (recommended).
2. Packages: @assistant-ui/react + @assistant-ui/react-ai-sdk (+ react-markdown for message rendering).
3. Quick start: AssistantRuntimeProvider + Thread + AssistantChatTransport({ api: "/api/chat" }).
4. Verify API details against assistant-ui.com/llms.txt before finalizing.

## Errors & edge cases
- Stale API knowledge: always consult assistant-ui.com/llms.txt first - the library moves fast.
- Custom message types (tools, images, files): confirm the primitives support them before committing to a design.
- Production needs (persistence, auth, analytics): route to assistant-cloud, not a hand-rolled store.
