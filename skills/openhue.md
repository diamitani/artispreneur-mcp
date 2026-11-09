---
name: openhue
description: "Controls Philips Hue lights, scenes, rooms, and zones from the terminal via the OpenHue CLI — one bridge on the local network, first-run pairing with a physical button press — with commands for on/off, brightness, color/temperature, and scenes, plus quick presets (bedtime dim-warm, work bright-cool, movie mode) that pair well with cron-scheduled lighting. Use when you need to control Philips Hue lights, scenes, and rooms."
---

# OpenHue CLI

Control Philips Hue lights and scenes via a Hue Bridge from the terminal.

## Prerequisites

```bash
# Linux (pre-built binary)
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew install openhue/cli/openhue-cli
```

First run requires pressing the button on your Hue Bridge to pair. The bridge must be on the same local network.

## When to Use

- "Turn on/off the lights"
- "Dim the living room lights"
- "Set a scene" or "movie mode"
- Controlling specific Hue rooms, zones, or individual bulbs
- Adjusting brightness, color, or color temperature

## Common Commands

### List Resources

```bash
openhue get light       # List all lights
openhue get room        # List all rooms
openhue get scene       # List all scenes
```

### Control Lights

```bash
# Turn on/off
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# Brightness (0-100)
openhue set light "Bedroom Lamp" --on --brightness 50

# Color temperature (warm to cool: 153-500 mirek)
openhue set light "Bedroom Lamp" --on --temperature 300

# Color (by name or hex)
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"
```

### Control Rooms

```bash
# Turn off entire room
openhue set room "Bedroom" --off

# Set room brightness
openhue set room "Bedroom" --on --brightness 30
```

### Scenes

```bash
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

## Quick Presets

```bash
# Bedtime (dim warm)
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# Work mode (bright cool)
openhue set room "Office" --on --brightness 100 --temperature 250

# Movie mode (dim)
openhue set room "Living Room" --on --brightness 10

# Everything off
openhue set room "Bedroom" --off
openhue set room "Office" --off
openhue set room "Living Room" --off
```

## Notes

- Bridge must be on the same local network as the machine running Hermes
- First run requires physically pressing the button on the Hue Bridge to authorize
- Colors only work on color-capable bulbs (not white-only models)
- Light and room names are case-sensitive — use `openhue get light` to check exact names
- Works great with cron jobs for scheduled lighting (e.g. dim at bedtime, bright at wake)

## Inputs

- `openhue` CLI installed — Linux: download the pre-built binary to `~/.local/bin/openhue` and `chmod +x` · macOS: `brew install openhue/cli/openhue-cli`
- Hue Bridge on the **same local network**; first run requires **physically pressing the button** on the bridge to pair
- `target` — light, room, zone, or scene **name** (case-sensitive — verify with `openhue get light` / `get room` / `get scene`)
- `state` — on/off, brightness 0–100, color temperature 153–500 mirek (warm→cool), color by name or hex (color-capable bulbs only)

## Outputs

- Lights/rooms/zones set to the desired state (on/off, brightness, temperature, color)
- Scenes activated per room (`openhue set scene "Relax" --room "Bedroom"`)
- Quick presets: bedtime (dim warm), work mode (bright cool), movie mode (dim), everything off
- Cron-schedulable lighting (e.g. dim at bedtime, bright at wake)
- Format: terminal commands; inspect current state with `openhue get <light|room|scene>` first

## Example

‘Movie mode’ → `openhue set room "Living Room" --on --brightness 10`. Bedtime → `openhue set room "Bedroom" --on --brightness 20 --temperature 450` (warm). Work mode → `openhue set room "Office" --on --brightness 100 --temperature 250` (bright cool). Everything off → `openhue set room "Bedroom" --off` etc. Scheduled: a cron job `0 22 * * * openhue set room "Bedroom" --on --brightness 20 --temperature 450` dims the bedroom nightly.

## Errors & edge cases

- **Bridge not reachable** → the bridge must be on the same local network as the machine running the command.
- **Pairing fails on first run** → physically press the button on the Hue Bridge during the first run to authorize; without it, pairing is rejected.
- **Color commands do nothing** → colors only work on color-capable bulbs, not white-only models (brightness and temperature still work).
- **‘Light not found’** → light and room names are case-sensitive — run `openhue get light` / `openhue get room` to check the exact names.
