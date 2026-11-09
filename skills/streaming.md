---
name: streaming
description: "Streams from custom (non-AI-SDK) backends in assistant-ui via the assistant-stream package -- createAssistantStreamResponse / createAssistantStreamController, emitting text and tool-call parts through the stream -- wired into useLocalRuntime as ChatModelRunResult chunks. Use when building a custom streaming endpoint or debugging stream wire issues."
---

# assistant-ui Streaming

**Always consult [assistant-ui.com/llms.txt](https://www.assistant-ui.com/llms.txt) for the latest API.**

The `assistant-stream` package handles streaming from AI backends.

## References

- [./references/data-stream.md](./references/data-stream.md) -- AI SDK data stream format
- [./references/assistant-transport.md](./references/assistant-transport.md) -- Native assistant-ui format
- [./references/encoders.md](./references/encoders.md) -- Encoders and decoders
- [./references/resumable.md](./references/resumable.md) -- Resumable streams

## When to Use

```
Using Vercel AI SDK?
├─ Yes → toUIMessageStreamResponse() (no assistant-stream needed)
└─ No → assistant-stream for custom backends
```

## Installation

```bash
npm install assistant-stream
```

## Custom Streaming Response

```ts
import { createAssistantStreamResponse } from "assistant-stream";

export async function POST(req: Request) {
  return createAssistantStreamResponse(async (stream) => {
    stream.appendText("Hello ");
    stream.appendText("world!");

    const tool = stream.addToolCallPart({ toolCallId: "1", toolName: "get_weather" });
    tool.argsText.append('{"city":"NYC"}');
    tool.argsText.close();
    tool.setResponse({ result: { temperature: 22 } });

    stream.close();
  });
}
```

## With useLocalRuntime

`useLocalRuntime` expects `ChatModelRunResult` chunks. Yield content parts for streaming:

```tsx
import { useLocalRuntime } from "@assistant-ui/react";

const runtime = useLocalRuntime({
  model: {
    async *run({ messages, abortSignal }) {
      const response = await fetch("/api/chat", {
        method: "POST",
        body: JSON.stringify({ messages }),
        signal: abortSignal,
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n");
        buffer = parts.pop() ?? "";

        for (const chunk of parts.filter(Boolean)) {
          yield { content: [{ type: "text", text: chunk }] };
        }
      }
    },
  },
});
```

## Debugging Streams

```ts
import { AssistantStream, DataStreamDecoder } from "assistant-stream";

const stream = AssistantStream.fromResponse(response, new DataStreamDecoder());
for await (const event of stream) {
  console.log("Event:", JSON.stringify(event, null, 2));
}
```

## Stream Event Types

- `part-start` with `part.type` = `"text" | "reasoning" | "tool-call" | "source" | "file"`
- `text-delta` with streamed text
- `result` with tool results
- `step-start`, `step-finish`, `message-finish`
- `error` strings

## Common Gotchas

**Stream not updating UI**
- Check Content-Type is `text/event-stream`
- Check for CORS errors

**Tool calls not rendering**
- `addToolCallPart` needs both `toolCallId` and `toolName`
- Register tool UI with `makeAssistantToolUI`

**Partial text not showing**
- Use `text-delta` events for streaming

## Inputs

- `backend_type` -- Vercel AI SDK -> use toUIMessageStreamResponse() (no assistant-stream needed); anything else -> the assistant-stream package (`npm install assistant-stream`)
- `stream_parts` -- text deltas, part-start/result events, tool-call parts (toolCallId, toolName, argsText, response)

## Outputs

- A working streaming endpoint (`createAssistantStreamResponse(async (stream) => { stream.appendText(...); const tool = stream.addToolCallPart({...}); ... stream.close(); })`) consumed by `useLocalRuntime`'s model `run()` as an async generator of `ChatModelRunResult` chunks

## Example

POST /api/chat returns `createAssistantStreamResponse`: appends "Hello " + "world!", adds a `get_weather` tool-call part with args `{"city":"NYC"}` and a result `{ temperature: 22 }`, then closes; `useLocalRuntime` reads the body via `getReader()` and yields content-part chunks.
