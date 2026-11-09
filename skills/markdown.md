---
name: markdown
description: "Renders assistant message text as markdown in assistant-ui via `MarkdownTextPrimitive` (wired into the `MessagePrimitive.Parts` text branch) — GFM, code-block syntax highlighting (react-shiki), KaTeX math, Mermaid diagrams, and a batteries-included Streamdown alternative; always consult assistant-ui.com/llms.txt for the latest API. Use when displaying model output as formatted markdown in assistant-ui chat interfaces."
---

# assistant-ui Markdown

**Always consult [assistant-ui.com/llms.txt](https://www.assistant-ui.com/llms.txt) for the latest API.**

Render and customize assistant message text as markdown with `MarkdownTextPrimitive` from `@assistant-ui/react-markdown`, wired into the `MessagePrimitive.Parts` text branch.

## References

- [./references/markdown-text.md](./references/markdown-text.md) -- MarkdownTextPrimitive setup
- [./references/syntax-highlighting.md](./references/syntax-highlighting.md) -- code highlighting (react-shiki / react-syntax-highlighter)
- [./references/latex-mermaid.md](./references/latex-mermaid.md) -- LaTeX and Mermaid
- [./references/streamdown.md](./references/streamdown.md) -- StreamdownTextPrimitive alternative

## Orientation

`MarkdownTextPrimitive` renders one text part as markdown. The registry component (`npx assistant-ui@latest add markdown-text`) generates `components/assistant-ui/markdown-text.tsx`, which exports a memoized `MarkdownText` built on the primitive plus a `defaultComponents` map from `unstable_memoizeMarkdownComponents`. Render `MarkdownText` from the `text` branch of `MessagePrimitive.Parts`.

```tsx
import "@assistant-ui/react-markdown/styles/dot.css";
import { MarkdownTextPrimitive } from "@assistant-ui/react-markdown";
import { MessagePrimitive } from "@assistant-ui/react";
import remarkGfm from "remark-gfm";
import { memo } from "react";

const MarkdownTextImpl = () => (
  <MarkdownTextPrimitive
    remarkPlugins={[remarkGfm]}
    className="aui-md"
    components={defaultComponents}
  />
);

export const MarkdownText = memo(MarkdownTextImpl);

<MessagePrimitive.Parts>
  {({ part }) => (part.type === "text" ? <MarkdownText /> : null)}
</MessagePrimitive.Parts>;
```

Add highlighting, math, or diagrams by extending the same primitive: `rehypePlugins` for KaTeX, `componentsByLanguage` for a per-language `SyntaxHighlighter` (Mermaid, diff), and `preprocess` to normalize raw text before parsing. See the references for each. For a batteries-included alternative with built-in Shiki, KaTeX, Mermaid, and block streaming, swap in `StreamdownTextPrimitive` from `@assistant-ui/react-streamdown`.

## Common Gotchas

- **Nothing renders / plain text shows.** The `text` branch must return `MarkdownText`; returning `<p>{part.text}</p>` bypasses markdown entirely.
- **No syntax highlighting.** Highlighting is not bundled. Register a `SyntaxHighlighter` in `defaultComponents` (react-shiki recommended) per the syntax-highlighting reference.
- **KaTeX has no styling.** Import `katex/dist/katex.min.css` once at the app root; `rehypeKatex` only emits markup.
- **Mermaid parses partial diagrams while streaming.** Gate rendering on stream completion (the reference uses `useAuiState` to detect the closing fence) instead of rendering every delta.
- **Memoization export name.** The package exports `unstable_memoizeMarkdownComponents`; the generated file aliases it to `memoizeMarkdownComponents`.
- **Unstyled by default.** The `aui-md` class and `styles/dot.css` provide base styling; add your own Tailwind/CSS otherwise.

## Related Skills

- **primitives** -- general UI composition (`ThreadPrimitive`, `ComposerPrimitive`, `MessagePrimitive.Parts`) for assembling the message and the rest of the chat surface around the markdown text branch.

## Inputs

- The `text` part from `MessagePrimitive.Parts` — the `text` branch must return `<MarkdownText />` (returning `<p>{part.text}</p>` bypasses markdown entirely)
- `remarkPlugins` (e.g. `remarkGfm`), `rehypePlugins` (e.g. KaTeX), `components` / `componentsByLanguage` (a `SyntaxHighlighter` per language — react-shiki recommended; highlighting is not bundled), `preprocess` (normalize raw text before parsing)
- Primitive choice: `MarkdownTextPrimitive` from `@assistant-ui/react-markdown` vs `StreamdownTextPrimitive` from `@assistant-ui/react-streamdown`
- References: `references/markdown-text.md` (setup), `syntax-highlighting.md`, `latex-mermaid.md`, `streamdown.md`

## Outputs

- A memoized `MarkdownText` component rendering GFM markdown, highlighted code blocks, math, and diagrams inside the chat thread
- Styling: `aui-md` class + `styles/dot.css` base (add your own Tailwind/CSS otherwise); `katex.min.css` imported once at the app root for math
- Format: TSX component (`components/assistant-ui/markdown-text.tsx`) + style imports; related: the `primitives` skill for composing the surrounding thread/composer surface

## Example

Wire markdown into a chat thread: `npx assistant-ui@latest add markdown-text` generates `components/assistant-ui/markdown-text.tsx` (memoized `MarkdownText` on the primitive + `defaultComponents` map) → import `@assistant-ui/react-markdown/styles/dot.css` → render `<MarkdownText />` in the `text` branch with `remarkPlugins={[remarkGfm]}`. Then: register react-shiki in `componentsByLanguage` for per-language highlighting, add `rehypeKatex` + `katex/dist/katex.min.css` for math, gate Mermaid on stream completion via `useAuiState` (partial fences mis-parse mid-stream) — or swap in `StreamdownTextPrimitive` for Shiki + KaTeX + Mermaid + block streaming built in.
