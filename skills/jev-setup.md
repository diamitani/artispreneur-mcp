---
name: jev-setup
description: "Connects Jev by getting a TypeSafe or OpenRouter API key into the OS secret store through a private browser page — the key never passes through the agent: never seen, asked for, read from disk, or placed in a command, URL, config, or log. Use when Jev is not working yet, a Jev tool reports no_key or auth_failed, or the person asks to connect or fix Jev."
version: 0.2.0
license: MIT
metadata:
  hermes:
    tags: [jev, typesafe, setup, credentials]
category: ai-agents
---

# Connect Jev (the key never passes through you)

Jev is TypeSafe's decision model. It needs one API key. **You must never see, ask for, or handle that key.**

The key can come from either of two places, and the same Jev answers either way:

- **TypeSafe** (`jev setup-key`, the default): a key from [console.typesafe.ai](https://console.typesafe.ai/settings/keys).
- **OpenRouter** (`jev setup-key --provider openrouter`): reaches Jev through OpenRouter's Decisions API. Worth offering when the person already has an OpenRouter key, because it is then one key instead of two and one bill instead of two.

If both keys exist, TypeSafe is used: an existing install never starts routing its decisions somewhere else because an OpenRouter key happened to be in the environment for a text model. `jev doctor` reports which one is in use under `key.provider`.

## Rules

- Never ask the person to paste the key into the chat. If they paste one anyway, do not store it, do not repeat it, tell them that key should be replaced, and start the flow below.
- Never read the secret store, `.env` files or `~/.config/jev/credentials` to "check" the key. Use `jev doctor`, which reports only presence and length.
- Never put the key in a command line, a URL, a config file you write, or a log.

## Flow

1. Check the state: `jev doctor`. If `key.present` is true and `jev.reachable` is true, you are done.
2. Start the private key page:

   ```bash
   jev setup-key
   ```

   It opens a page in the browser on the computer you are running on and prints one JSON line on stderr with a `url`. The URL holds no secret.
3. Tell the person, in one sentence, to paste their TypeSafe key into the page that just opened. If `browser_opened` is false, or they are talking to you from another device (Telegram, phone), send them the `url` and tell them it only opens **on the computer the agent runs on**. If they have no key yet, they create one at https://console.typesafe.ai/settings/keys.
4. Wait for the command to finish. It prints `{"status": "stored", "verified": true, ...}` when the key was saved and the provider accepted it. `rejected` means the key was wrong: run it again. `timed_out` means nobody used the page within ten minutes.
5. Run `jev doctor` once more and report the result in a sentence.

## When there is no browser

Headless server over SSH: the person runs `jev setup-key --tty` **themselves** in their own terminal. It is a hidden prompt. Do not run it for them through a tool that captures the terminal.

Remote machine on a private network (Tailscale, VPN): `jev setup-key --host <private-ip> --no-open` and send them the link. That traffic is plain HTTP, so use it only on a network you trust end to end. Never bind a public address.

## Where the key goes

The OS secret store (macOS Keychain service `Hermes TypeSafe API`, or `secret-tool` on Linux), falling back to `~/.config/jev/credentials` (mode 0600). On a Hermes machine it is also written as `TYPESAFE_API_KEY` into `~/.hermes/.env` and every `profiles/*/.env`, because each Hermes lane reads its own file. Running gateways pick it up on their next restart; do not restart one without being asked.

## Inputs

- State check: `jev doctor` — reports `key.present`, `jev.reachable`, and `key.provider`; presence and length only, never the key value
- `jev setup-key` (TypeSafe, default) or `jev setup-key --provider openrouter` — opens a private page in the browser on the computer the agent runs on; prints one JSON line on stderr with a `url`
- Variants: `--tty` (headless SSH — the person runs it themselves), `--host <private-ip> --no-open` (remote private network)
- The person, with a browser on the machine the agent runs on, and a key from console.typesafe.ai/settings/keys (or their existing OpenRouter key)

## Outputs

- `{"status": "stored", "verified": true, ...}` when the key was saved and the provider accepted it
- The key in the OS secret store: macOS Keychain service `Hermes TypeSafe API`, or `secret-tool` on Linux; fallback `~/.config/jev/credentials` (mode 0600). On Hermes also written as `TYPESAFE_API_KEY` into `~/.hermes/.env` and every `profiles/*/.env`
- A final `jev doctor` reported back in one sentence — done means `key.present` true and `jev.reachable` true

## Example

`jev doctor` → `key.present: false` → run `jev setup-key` → a page opens in the browser and one JSON line prints on stderr with a `url` (the URL holds no secret) → tell the person, in one sentence, to paste their TypeSafe key into the page (they create one at console.typesafe.ai/settings/keys if needed) → wait for `{"status": "stored", "verified": true, ...}` → `jev doctor` once more → report in a sentence: ‘Jev is connected via TypeSafe.’ Already has an OpenRouter key? Offer `jev setup-key --provider openrouter` — one key and one bill instead of two.

## Errors & edge cases

- **`rejected`** = the key was wrong: run `jev setup-key` again. **`timed_out`** = nobody used the page within ten minutes.
- If the person pastes a key into the chat anyway: do not store it, do not repeat it, tell them that key should be replaced, and start the flow below.
- **`browser_opened: false`**, or the person is on another device (Telegram, phone): send them the `url` — it only opens **on the computer the agent runs on**.
- **Headless server over SSH:** the person runs `jev setup-key --tty` **themselves** in their own terminal (hidden prompt) — never run it for them through a tool that captures the terminal.
- **Remote machine on a private network** (Tailscale, VPN): `jev setup-key --host <private-ip> --no-open`, plain HTTP — trusted networks only, never bind a public address.
- **If both keys exist, TypeSafe wins**: an existing install never starts routing its decisions somewhere else because an OpenRouter key happened to be in the environment (`jev doctor` reports the provider in use under `key.provider`).
- Gateways pick the key up on their next restart — do not restart one without being asked.
