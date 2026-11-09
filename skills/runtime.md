---
name: runtime
description: "Guides the assistant-ui runtime system in @assistant-ui/react -- the Runtime -> ThreadList -> Thread -> Composer/Message hierarchy, the modern useAui / useAuiState / useAuiEvent API, thread and message operations, and capability checks. Use when creating a runtime or wiring AssistantRuntimeProvider."
---

# assistant-ui Runtime

**Always consult [assistant-ui.com/llms.txt](https://www.assistant-ui.com/llms.txt) for the latest API.**

## References

- [./references/local-runtime.md](./references/local-runtime.md) -- useLocalRuntime deep dive
- [./references/external-store.md](./references/external-store.md) -- useExternalStoreRuntime deep dive
- [./references/thread-list.md](./references/thread-list.md) -- Thread list management
- [./references/state-hooks.md](./references/state-hooks.md) -- State access hooks
- [./references/types.md](./references/types.md) -- Type definitions
- [./references/adapters.md](./references/adapters.md) -- Attachment, speech, dictation, suggestion, and history adapters
- [./references/voice.md](./references/voice.md) -- Realtime voice chat
- [./references/runtime-concepts.md](./references/runtime-concepts.md) -- Stability policy, transport runtime, message timing

## Runtime Hierarchy

```
AssistantRuntime
├── ThreadListRuntime (thread management)
│   ├── ThreadListItemRuntime (per-thread item)
│   └── ...
└── ThreadRuntime (current thread)
    ├── ComposerRuntime (input state)
    └── MessageRuntime[] (per-message)
        └── MessagePartRuntime[] (per-content-part)
```

## State Access (Modern API)

```tsx
import { useAui, useAuiState, useAuiEvent } from "@assistant-ui/react";

function ChatControls() {
  const api = useAui();
  const messages = useAuiState(s => s.thread.messages);
  const isRunning = useAuiState(s => s.thread.isRunning);

  useAuiEvent("composer.send", (e) => {
    console.log("Sent in thread:", e.threadId);
  });

  return (
    <div>
      <button onClick={() => api.thread().append({
        role: "user",
        content: [{ type: "text", text: "Hello!" }],
      })}>
        Send
      </button>
      {isRunning && (
        <button onClick={() => api.thread().cancelRun()}>Cancel</button>
      )}
    </div>
  );
}
```

## Thread Operations

```tsx
const api = useAui();
const thread = api.thread();

thread.append({ role: "user", content: [{ type: "text", text: "Hello" }] });

thread.cancelRun();

const state = thread.getState();  // { messages, isRunning, ... }
```

## Message Operations

```tsx
const message = api.thread().message(0);

message.edit({ role: "user", content: [{ type: "text", text: "Updated" }] });
message.reload();
```

## Events

```tsx
useAuiEvent("thread.runStart", () => {});
useAuiEvent("thread.runEnd", () => {});
useAuiEvent("composer.send", ({ threadId }) => {
  console.log("Sent in thread:", threadId);
});
useAuiEvent("thread.modelContextUpdate", () => {});
```

## Capabilities

```tsx
const caps = useAuiState(s => s.thread.capabilities);
// { cancel, edit, reload, copy, speak, attachments }
```

## Common Gotchas

**"Cannot read property of undefined"**
- Ensure hooks are called inside `AssistantRuntimeProvider`

**State not updating**
- Use selectors with `useAuiState` to prevent unnecessary re-renders

**Messages array empty**
- Check runtime is configured
- Verify API response format

## Inputs

- `runtime_type` -- `useLocalRuntime` + ChatModelAdapter (custom streaming API), `useExternalStoreRuntime` (existing Redux/Zustand state), `useRemoteThreadListRuntime` (thread list management), or a runtime hook per backend (`useChatRuntime`, `useLangGraphRuntime`, `useAgUiRuntime`, ...)
- `state_selectors` -- `useAuiState(s => ...)` selectors (e.g. `s.thread.messages`, `s.thread.isRunning`, `s.thread.capabilities`)
- `events` -- `useAuiEvent` subscriptions: `composer.send`, `thread.runStart`, `thread.runEnd`, `thread.modelContextUpdate`

## Outputs

- A working runtime wired to `AssistantRuntimeProvider`; thread operations (`append`, `cancelRun`, `getState`), message operations (`edit`, `reload`), and capability checks (`cancel`, `edit`, `reload`, `copy`, `speak`, `attachments`) -- always consult assistant-ui.com/llms.txt for the latest API

## Example

A chat controls component: `useAuiState(s => s.thread.messages)` to render messages, `s.thread.isRunning` to show a Cancel button that calls `api.thread().cancelRun()`, and a Send button calling `api.thread().append({ role: "user", content: [{ type: "text", text: "Hello!" }] })`.

## Errors & edge cases

- **"Cannot read property of undefined"** -- ensure hooks are called inside `AssistantRuntimeProvider`.
- **State not updating** -- use selectors with `useAuiState` to prevent unnecessary re-renders.
- **Messages array empty** -- check the runtime is configured and verify the API response format.
- **Deep dives** -- see the reference files: local-runtime, external-store, thread-list, state-hooks, types, adapters, voice, runtime-concepts.
