---
name: cloud
description: "LLM-agnostic productivity and task automation skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to wire assistant-ui Cloud persistence and authorization via the assistant-cloud package and AssistantCloud client: cloud.threads CRUD and per-thread message listing, presigned file uploads, three auth options (JWT recommended, API key server-side, anonymous), env-var config, and common gotchas - always consulting assistant-ui.com/llms.txt for the latest API. Use when adding cross-session thread/message persistence, multi-device chat history, file uploads, or auth to an assistant-ui app: passing the cloud option to useChatRuntime."
---

# assistant-ui Cloud

**Always consult [assistant-ui.com/llms.txt](https://www.assistant-ui.com/llms.txt) for the latest API.**

Cloud persistence for threads, messages, and files.

## References

- [./references/persistence.md](./references/persistence.md) -- Thread and message persistence
- [./references/authorization.md](./references/authorization.md) -- Authentication patterns
- [./references/custom-persistence.md](./references/custom-persistence.md) -- Self-hosted message persistence
- [./references/auth-integrations.md](./references/auth-integrations.md) -- better-auth and Clerk integrations

## Installation

```bash
npm install assistant-cloud
```

## Quick Start

```tsx
import { AssistantCloud } from "assistant-cloud";
import { useChatRuntime, AssistantChatTransport } from "@assistant-ui/react-ai-sdk";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { Thread } from "@/components/assistant-ui/thread";
import { ThreadList } from "@/components/assistant-ui/thread-list";

const cloud = new AssistantCloud({
  baseUrl: process.env.NEXT_PUBLIC_ASSISTANT_BASE_URL,
  authToken: async () => getAuthToken(),
});

function Chat() {
  const runtime = useChatRuntime({
    transport: new AssistantChatTransport({ api: "/api/chat" }),
    cloud,
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <ThreadList />
      <Thread />
    </AssistantRuntimeProvider>
  );
}
```

## Authentication Options

```tsx
// JWT Token (recommended)
const cloud = new AssistantCloud({
  baseUrl: process.env.NEXT_PUBLIC_ASSISTANT_BASE_URL,
  authToken: async () => session?.accessToken,
});

// API Key (server-side)
const cloud = new AssistantCloud({
  baseUrl: process.env.ASSISTANT_BASE_URL,
  apiKey: process.env.ASSISTANT_API_KEY,
  userId: user.id,
  workspaceId: user.workspaceId,
});

// Anonymous (public apps)
const cloud = new AssistantCloud({
  baseUrl: process.env.NEXT_PUBLIC_ASSISTANT_BASE_URL,
  anonymous: true,
});
```

## Cloud API

```tsx
const threads = await cloud.threads.list();
await cloud.threads.create({ title: "New Chat" });
await cloud.threads.update(threadId, { title: "Updated" });
await cloud.threads.delete(threadId);

const messages = await cloud.threads.messages(threadId).list();

const { signedUrl, publicUrl } = await cloud.files.generatePresignedUploadUrl({
  filename: "document.pdf",
});
await fetch(signedUrl, { method: "PUT", body: file });
```

## Environment Variables

```env
NEXT_PUBLIC_ASSISTANT_BASE_URL=https://api.assistant-ui.com
ASSISTANT_API_KEY=your-api-key  # Server-side only
```

## Common Gotchas

**Threads not persisting**
- Pass `cloud` to runtime
- Check authentication

**Auth errors**
- Verify `authToken` returns valid token
- Check `baseUrl` is correct

## Inputs
- `app` (string, required) - the assistant-ui app to extend
- `features` (list) - thread persistence, multi-device history, file uploads, auth
- `auth` (enum: jwt / api-key / anonymous, default: jwt)
- `base_url` / `api_key` / `user_id` / `workspace_id` (env) - per the chosen auth option

## Outputs
- AssistantCloud wired into useChatRuntime via the `cloud` option, with ThreadList + Thread rendered
- Working threads/messages API calls and presigned file-upload flow
- Environment variable configuration documented

## Example
Input: add cross-session chat history to a Next.js assistant-ui app with JWT auth.
1. `npm install assistant-cloud`; consult assistant-ui.com/llms.txt for the current API.
2. `new AssistantCloud({ baseUrl: process.env.NEXT_PUBLIC_ASSISTANT_BASE_URL, authToken: async () => session?.accessToken })`.
3. Pass `cloud` to useChatRuntime; render ThreadList + Thread.
4. File uploads: generatePresignedUploadUrl -> PUT the file -> use the public URL.

## Errors & edge cases
- Stale API knowledge: consult assistant-ui.com/llms.txt first - the Cloud API moves fast.
- API key on the client: use the server-side pattern (ASSISTANT_BASE_URL + userId/workspaceId), never expose keys in the browser.
- Anonymous mode: only for public apps; production user data needs JWT or API-key auth.
