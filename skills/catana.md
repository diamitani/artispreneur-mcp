---
name: catana
description: "Music catalogue organizer: audits masters, stems, artwork, and metadata, enforces naming conventions, cross-references streaming platforms for gaps, and preps catalogues for playlisting and sync. Use when managing and enhancing music catalogues."
---

# Catana

Manage and enhance music catalogues for independent artists. Organize files, metadata, and assets across distribution platforms, streaming services, and local storage.

## Workflow

1. Audit the artist's current catalogue: master recordings, stems, artwork, metadata, distribution status.
2. Organize files with a consistent naming convention and folder structure (by release, by session, or by project).
3. Ensure metadata completeness: ISRCs, UPCs, credits, genre tags, and release dates.
4. Cross-reference catalogue across platforms (Spotify, Apple Music, YouTube, Bandcamp, SoundCloud) to identify missing or inconsistent entries.
5. Advise on catalogue optimization: playlisting pitch prep, featured artist tagging, and version cleanup.
6. Recommend archival and backup strategies to prevent data loss.

## Key Considerations

- Consistent metadata is essential for royalty tracking and discovery algorithms.
- Remove duplicate or outdated versions to avoid listener confusion.
- Keep stems and project files backed up — hard drive failures are common.
- Consider catalogue valuation for artists exploring publishing deals or sync licensing.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `catalog_scope` | string | required | Which releases to audit (e.g. "all singles 2023-2026", "the EP + loosies"). |
| `platforms` | string[] | `spotify,apple,youtube` | Also: `bandcamp`, `soundcloud`, distributor dashboards. |
| `storage_locations` | string[] | -- | Local drives, cloud folders where masters/stems/artwork live. |

## Outputs

- **Deliverable:** a catalogue audit report -- inventory gaps, metadata fixes (ISRCs, UPCs, credits, splits), a naming convention, and a backup/archival plan.
- **Format:** structured report (table per release) + the convention doc.

## Example

> "Audit my 12 singles across DistroKid and SoundCloud."

1. Inventory: 12 masters, 9 with stems, 11 with artwork; 2 missing ISRCs, 1 duplicate version live on SoundCloud.
2. Cross-reference: one single missing from Apple Music; featured-artist tag inconsistent on 3 tracks.
3. Convention: `Artist_Title_Version_YYYY` (e.g. `Nova_Midnight_RadioEdit_2026`); folders by release.
4. Backup: 3-2-1 rule for stems + project files; catalogue valuation note for a pending publishing conversation.

## Errors & edge cases

- Distributor won't correct metadata -> takedown-and-redeliver is the reliable path; document before pulling.
- Lost stems / dead hard drive -> recovery options first, then a going-forward backup rule.
- Duplicate/outdated versions confusing listeners -> consolidate to canonical versions.
- Metadata wrong at the distributor -> royalties misroute; fix ISRC/credits before playlist pitching.
