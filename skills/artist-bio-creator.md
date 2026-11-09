---
name: artist-bio-creator
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to interview artists for their story hook, then write three platform-tuned bios - short (50-80 words, Spotify/social), standard (150-250, EPK/press), long (400-600, website) - polished for tone, cliche-free, and voiced to match the music. Use when guiding musicians through creating professional artist biographies."
---

# Artist Bio Creator

## Overview
Guides musicians through crafting professional artist biographies that tell a compelling story. Produces multiple versions optimized for different platforms (Spotify, Instagram, press kits, website) and lengths, each tailored to its audience.

## When to Use
- Writing a new artist bio from scratch
- Updating an existing bio for a new release or career milestone
- Creating platform-specific bios (short for social, long for website)
- Need a compelling narrative arc that goes beyond "I started making music at age 6"

## How It Works
1. **Interview the artist**: Dig into their story, influences, and what makes them unique.
2. **Find the hook**: Identify the most interesting angle — a unique background, a defining moment, a sound nobody else has.
3. **Write for the platform**: Different lengths and tones for different contexts.
4. **Polish**: Remove clichés, add vivid details, ensure the voice matches the music.

## Steps
1. Ask: "Tell me your story — how did you start? What drives you? What's your sound?"
2. Ask about: genre, influences, notable achievements, upcoming releases.
3. Draft the **short bio** (50-80 words): For Spotify, Instagram, Twitter. Punchy hook.
4. Draft the **standard bio** (150-250 words): For EPK, press releases, festival programs.
5. Draft the **long bio** (400-600 words): For website "About" page, full narrative with quotes and details.
6. Review with artist for tone, accuracy, and voice alignment.
7. Deliver final versions clearly labeled by platform/length.

## Common Pitfalls
- **Chronological laundry list**: "Born in X, moved to Y, released Z." Boring. Lead with the hook.
- **Vague influences**: "I'm influenced by everything." Name specific artists and what you took from them.
- **No story**: Every biography needs tension, growth, or transformation — not just facts.
- **Wrong tone**: A death metal bio shouldn't read like a folk singer's.

## Source
Originally from the Artispreneur Custom GPT portfolio.

## Inputs
- `story` (string, required) - how they started, what drives them, their sound
- `genre` (string) and `influences` (list) - specific artists and what was taken from them
- `achievements` (list) - releases, milestones, notable moments
- `tone_target` (string) - must match the music's mood

## Outputs
- Short bio (50-80 words): punchy hook for Spotify/Instagram
- Standard bio (150-250 words): EPK, press releases, festival programs
- Long bio (400-600 words): website About page, full narrative with quotes and details

## Example
Input: Detroit techno producer, started DJing warehouse parties, debut EP "Rust Belt Signal".
1. Interview surfaces the hook: a former auto-plant electrician wiring assembly-line rhythm into techno.
2. Short bio: hook-first, 60 words for Spotify.
3. Standard: adds influences (specific, not "everything") and the EP for EPK.
4. Long: full narrative arc with a quote; reviewed with the artist for voice alignment.
