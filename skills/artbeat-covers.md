---
name: artbeat-covers
description: "LLM-agnostic music production and marketing skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to conceptualize album/single cover art for independent artists: genre-aware visual research, 3-5 distinct creative concepts with palettes and typography direction, refinement to one winner, and a DSP-ready design brief (3000x3000px) a designer or AI image tool can execute. Use when helping artists create visually stunning cover art tailored to their music."
---

# ArtBeat Covers

## Overview
Helps independent artists conceptualize and design compelling cover art that visually represents their music. Generates creative concepts, mood boards, color palettes, typography direction, and detailed visual briefs that can be handed to a designer or used with AI image generation tools.

## When to Use
- An artist needs cover art for a single, EP, or album release
- Brainstorming visual concepts that match the music's mood and genre
- Creating a design brief for a graphic designer
- Exploring different artistic styles (photography, illustration, abstract, typographic)
- Ensuring cover art meets DSP specifications (3000x3000px, etc.)

## How It Works
1. **Music intake**: Understand the song/album's genre, mood, themes, and title.
2. **Visual research**: Reference genre-appropriate cover art trends and iconic examples.
3. **Concept generation**: Propose 3-5 distinct visual directions.
4. **Refine**: Narrow to the strongest concept and detail color, typography, imagery.
5. **Deliver a design brief**: Ready for execution by a designer or AI tool.

## Steps
1. Ask for: album/single title, genre, mood, lyrical themes, and any visual preferences.
2. Ask about: existing brand colors, logo, or visual identity.
3. Research genre conventions (e.g., hip-hop covers vs. folk covers vs. electronic covers).
4. Propose 3-5 concepts with:
   - Visual description (imagery, composition, style)
   - Color palette (hex codes or descriptive)
   - Typography direction (font style, placement)
   - Mood/vibe alignment with the music
5. Get artist feedback and refine the chosen concept.
6. Provide DSP specs: 3000x3000px minimum, JPG/PNG, 72 DPI minimum, RGB color.
7. Deliver a final design brief document.

## Common Pitfalls
- **Text illegibility at small sizes**: Cover art must read as a tiny thumbnail on streaming platforms.
- **Genre mismatch**: A bubblegum pop cover on a dark ambient album confuses listeners.
- **Overcomplicated**: Simple, bold designs often outperform busy ones at thumbnail size.
- **Copyright issues**: Don't use unlicensed stock photos or artwork without permission.

## Source
Originally from the Artispreneur Custom GPT portfolio.

## Inputs
- `title` (string, required) - album/single title
- `genre` (string, required) - drives visual conventions research
- `mood` (string) and `themes` (string) - lyrical/visual direction
- `brand` (string) - existing brand colors, logo, visual identity
- `preferences` (string) - photography / illustration / abstract / typographic lean

## Outputs
- 3-5 visual concepts, each with imagery/composition description, color palette, typography direction, mood alignment
- One refined final concept after artist feedback
- DSP-ready design brief: 3000x3000px minimum, JPG/PNG, 72 DPI, RGB

## Example
Input: dark-folk EP "Hollow Pines", moody forest imagery, artist likes grainy photography.
1. Research: folk-cover conventions vs dark-ambient aesthetics.
2. Concepts: (a) foggy pine silhouette with serif type, (b) cracked-bark macro texture, (c) lone cabin at dusk - each with palette + type direction.
3. Artist picks (a); refine: thumbnail-legibility check, palette locked.
4. Final brief ready for the designer with DSP specs.
