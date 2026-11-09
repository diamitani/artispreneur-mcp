---
name: grok-social-cleanup
description: "LLM-agnostic social-media cleanup skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to audit a user's social profiles for offensive content and unwanted follows using xAI's Grok as the classifier, then present every flagged item for explicit user approval before removing it. Use when the user wants to delete offensive likes or comments, or unfollow porn, spam, or bot accounts, on X, Instagram, Threads, or Facebook."
---

# Grok Social Cleanup

A Grok-powered bot skill for cleaning up public social profiles. It reads your likes, replies, and follows, classifies each one for offensive content (homophobia, antisemitism, misogyny, racism, other hate) or unwanted account types (porn/NSFW, spam, bots), shows you the flagged list, and only removes what you confirm. Works on any social network: connector where one exists, live browser where one doesn't.

**Base URL:** `https://api.x.ai/v1`
**Auth:** `Authorization: Bearer {{XAI_API_KEY}}` — the user's own key from console.x.ai (user tap; never stored by the agent).

## When to use
- "Clean up my socials", "scrub my X profile", "delete my offensive likes"
- "Unfollow all porn accounts", "remove spam/bot follows"
- Works for X, Instagram, Threads, Facebook — any network with a connected tool or browser path.

## Steps
1. Collect (read-only). Pull the user's liked posts, replies/comments, and following list for each requested account. Use the connected tool where one exists (instagram, threads, facebook_cli connectors); use the live browser for networks without a connector (X). Do NOT unlike, delete, or unfollow anything in this pass.
2. Classify with Grok. Send each item's text (and display name + bio for followed accounts) to Grok with the fixed classifier prompt below. Return JSON per item: `{"verdict": "flag" | "review" | "clean", "class": "<policy class>", "reason": "<one line>"}`. Borderline items are `review`, never `flag`.
3. Report for approval. Present every `flag` and `review` item grouped by action (unlike / delete comment / unfollow), showing the exact text or handle, the post URL, and the policy class. WAIT for the user's explicit confirmation. Nothing is removed without the user's tap.
4. Execute confirmed removals. Unlike, delete, or unfollow ONLY the confirmed items, one by one, verifying each in the UI or via the connector response. Stop immediately on any 429 / rate-limit / bot-check and resume later — never retry aggressively.
5. Verify and report. Re-read the lists, confirm the flagged items are gone, and write `cleanup-report.md` with the flagged items, the user's decisions, and the verified removals.

## Classifier prompt (send to Grok verbatim, with the item text appended)
```
You are a content classifier for a social-profile cleanup tool. Classify the
item below for policy violations. Return ONLY valid JSON:
{"verdict": "flag" | "review" | "clean", "class": "<one of: homophobia, antisemitism, misogyny, racism, other-hate, nsfw-account, spam-bot, none>", "reason": "<one sentence>"}
Flag only clear violations: slurs, dehumanizing language, hate toward a
protected group, or accounts whose name/bio is explicitly sexual or spam.
Quotes, song lyrics, news discussion, and reclaimed language used by the
group itself are "review", not "flag". When in doubt, "review".
```

## Outputs
- `cleanup-report.md` — flagged items, user decisions, verified removals

## Reference tools
- xAI API: `POST https://api.x.ai/v1/chat/completions`, header `Authorization: Bearer {{XAI_API_KEY}}`, body `{"model": "grok-4-1-fast-non-reasoning", "messages": [...], "response_format": {"type": "json_object"}}` (chat-completions is documented-but-legacy; Responses API is xAI's newer primary — same auth)
- Fallback analyzer: OpenRouter `POST https://openrouter.ai/api/v1/chat/completions` with model `x-ai/grok-latest` and `Authorization: Bearer {{OPENROUTER_API_KEY}}` (env toggle; OpenRouter key comes from the user's Secure Vault, never a file)
- [Instagram](/opt/hatch/connectors/instagram/CONNECTOR.md), [Threads](/opt/hatch/connectors/threads/CONNECTOR.md), [Facebook](/opt/hatch/connectors/facebook_cli/CONNECTOR.md) — read + write where the connector supports it
- `browser.browse` for X and any network without a connector; the browser's login agent handles sign-in

## Guardrails
- Read-only until the user confirms the exact removal list. Unlikes, deletions, and unfollows are irreversible on most networks — NEVER auto-execute.
- No login-gated reads without a connected tool or the user's own live browser session.
- Never store `{{XAI_API_KEY}}` or `{{OPENROUTER_API_KEY}}` in files, memory, or chat. Env vars only; shred temp copies immediately.
- Borderline content is never auto-flagged; it goes to manual review.
- Rate limits and bot checks are stop conditions: 429 / challenge ends the run; report progress and resume later. Do not sleep, retry, or lower the rate to continue.
- Model unavailable: stop and say so; do not silently substitute a weaker judgment.

## Parent handoff
Summarize artifacts + blockers. If a dependent skill/capability is missing, name it and stop.

## Inputs
- `accounts` (list, required) - handles + networks to audit, e.g. `X @handle`, `Instagram @handle`
- `policy` (list, default: homophobia, antisemitism, misogyny, racism, other-hate) - violation classes to flag
- `unfollow_classes` (list, default: porn/NSFW accounts, spam, bots) - follow-list classes to flag
- `grok_model` (string, default: grok-4-1-fast-non-reasoning) - xAI model for classification; fast/cheap default. xAI's canonical IDs are the suffixed variants (`-reasoning` / `-non-reasoning`); if the API rejects the default, set this to the other variant.

## Example
Input: audit X @handle for hate-speech likes, unfollow porn accounts.
1. Browser: sign in as the user, export likes, replies, and following (handle + bio). Read-only.
2. Grok classifies each item: flags 3 homophobic likes, 1 misogynistic reply, 12 NSFW follows.
3. Report shows all 16 items with text, URLs, and classes. User confirms all 16.
4. Browser unlikes the 3, deletes the reply, unfollows the 12 — verifying each one.
5. `cleanup-report.md` written; re-check confirms all 16 removed.

## Errors & edge cases
- Login unavailable: stop and request the credential — no scraping per Guardrails.
- Rate-limited mid-run: stop immediately; report progress; resume later.
- xAI API down or key invalid: stop and report; do not substitute another model's judgment silently.
- Zero flags: report "clean" honestly instead of inventing violations.
- Porn-account detection is bio/name-based; a false-positive unfollow is irreversible — always user-confirm.
