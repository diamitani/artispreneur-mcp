---
name: songvid
description: "Stock-footage music video conceptor: analyzes tempo, mood, lyrics, and structure, then delivers shot-by-shot treatments with clip references and timestamps, ready for editing. Use when creating music video concepts using stock footage based on song uploads."
---

# SongVid

Create compelling music video concepts using stock footage synchronized to uploaded songs. This skill helps independent artists visualize their music through curated stock clips matched to tempo, mood, and lyrical themes.

## Workflow

1. Receive the artist's song upload (audio file or link).
2. Analyze the track: tempo, mood, lyrical themes, and song structure.
3. Curate matching stock footage from royalty-free sources (Pexels, Pixabay, Artgrid, Storyblocks).
4. Develop a shot-by-shot concept treatment aligned with the song's dynamics.
5. Deliver a storyboard or concept brief ready for video editing.

## Key Considerations

- Match visual pacing to the song's BPM and energy shifts.
- Prioritize royalty-free or licensed footage to avoid copyright issues.
- Tailor concepts to the artist's brand and genre.
- Keep treatments actionable — clip references, timestamps, and transition notes.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `audio` | string | required | Audio file or link to the song. |
| `brand_notes` | string | -- | Artist's visual identity, genre cues, references. |
| `footage_sources` | string[] | `pexels,pixabay,artgrid,storyblocks` | Royalty-free sources to pull from. |
| `aspect` | enum | `16:9` | `16:9` | `9:16` | `1:1` |

## Outputs

- **Deliverable:** a shot-by-shot concept treatment -- clip references, timestamps aligned to the song's dynamics, transition notes.
- **Format:** treatment document ready to hand to an editor.

## Example

> 98 BPM melancholy indie track, 3:40, artist brand: "midnight city".

1. Analyze: verse (sparse, intimate) -> pre-chorus (build) -> chorus (wide, cathartic) -> bridge (stripped) -> final chorus.
2. Treatment: verse = slow urban night clips, shallow focus; chorus = wide landscape/cityscape, motion; timestamps at each section change; transitions: match-cut on beat drops.
3. Clip refs from royalty-free sources with search terms per shot; note which shots need the artist's own footage for identity.

## Errors & edge cases

- Song has no clear structure -> map shots to the energy curve instead of sections.
- Suggested footage is copyrighted -> royalty-free or properly licensed only; re-source the shot.
- Visual pacing fights the BPM -> re-cut the treatment; pacing follows the song, not the clips.
- Keep it actionable: every shot needs a clip reference, timestamp, and transition note.
