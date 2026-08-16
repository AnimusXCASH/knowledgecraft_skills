# Research Library Registry Contract

Registry version: `2`

Default location:

`.knowledgecraft/research/registry.json`

The registry is runtime project state. It normally belongs in the consuming project's `.knowledgecraft/` workspace, not in the public skills repository.

## Top-Level Structure

```json
{
  "version": 2,
  "updated_at": "2026-08-16T07:00:00+00:00",
  "sources": {}
}
```

Fields:

- `version`: registry schema version;
- `updated_at`: UTC ISO-8601 timestamp of the most recent save;
- `sources`: object keyed by stable source ID.

## Source Identity

Each source record represents one exact byte-level content identity.

The canonical identity is the full SHA-256 digest.

Source IDs are deterministic SHA-256 prefixes:

`SRC-<hash-prefix>`

The default prefix length is 12 hexadecimal characters. If a different registered hash already owns that short ID, the implementation extends the prefix until the ID is unique.

Same full hash must resolve to the same existing source ID.

Filename, path, title, author, or metadata must never replace SHA-256 as the content identity.

## Source Record

Representative record:

```json
{
  "source_id": "SRC-a1b2c3d4e5f6",
  "sha256": "a1b2c3d4e5f6...",
  "filename": "paper.pdf",
  "primary_path": "D:/Research/paper.pdf",
  "paths": [
    "D:/Research/paper.pdf",
    "D:/Archive/paper-copy.pdf"
  ],
  "active_paths": [
    "D:/Research/paper.pdf",
    "D:/Archive/paper-copy.pdf"
  ],
  "missing_paths": [],
  "stale_paths": [],
  "extension": ".pdf",
  "size_bytes": 123456,
  "discovered_at": "2026-08-16T07:00:00+00:00",
  "last_seen_at": "2026-08-16T07:30:00+00:00",
  "status": "grounded",
  "revision_of": null,
  "revision_root": null,
  "revision_number": 1,
  "revised_by": [],
  "extracted_path": "D:/project/.knowledgecraft/research/extracted/SRC-a1b2c3d4e5f6.md",
  "artifacts": {
    "grounded": [
      "D:/project/.knowledgecraft/research/grounded/SRC-a1b2c3d4e5f6-source-card.yaml",
      "D:/project/.knowledgecraft/research/grounded/SRC-a1b2c3d4e5f6-claim-ledger.yaml"
    ]
  },
  "history": [],
  "error": null
}
```

## Required Identity Fields

### `source_id`

Stable deterministic source identifier.

Do not change once assigned.

### `sha256`

Full SHA-256 digest of registered content.

This is the authoritative content identity.

### `filename`

Filename observed when the source record was first created.

Filename is descriptive metadata, not identity.

### `extension`

Lowercase source-file extension used for extraction routing.

### `size_bytes`

File size observed when the source record was created.

This is descriptive and must not be used instead of SHA-256 for identity.

## Path Fields

### `primary_path`

Preferred currently valid path for the source.

May change when a previous primary path disappears, becomes stale, or another valid registered copy is selected.

May be `null` if no valid registered copy currently exists.

### `paths`

All paths historically registered for this exact source content.

A path can remain here even when it becomes unavailable or is reassigned to revised content.

### `active_paths`

Known existing paths that currently contain the registered SHA-256 content.

Extraction must hash-verify content before trusting a path.

### `missing_paths`

Known registered paths that do not currently exist.

A missing path does not delete source identity.

### `stale_paths`

Paths that no longer represent this source's registered content.

Typical case: the same filesystem path was overwritten with revised content and assigned to a new source record.

Do not use stale paths for extraction.

## Time Fields

### `discovered_at`

UTC ISO-8601 timestamp when this content identity was first registered.

### `last_seen_at`

UTC ISO-8601 timestamp when the same content was most recently encountered during scanning.

## Lifecycle

Allowed normal statuses:

1. `new`
2. `extracted`
3. `grounded`
4. `ideas_created`
5. `series_planned`
6. `drafted`
7. `qa_approved`
8. `scheduled`
9. `published`

Exceptional statuses:

- `failed`
- `ignored`

Normal `mark` transitions move one stage forward.

Non-standard transitions require explicit `--force`.

Extraction may recover `failed -> extracted` directly after successful extraction.

Re-extraction of a source already at `extracted` or later in the normal lifecycle refreshes the extraction artifact without downgrading the source status.

## Revision Fields

### `revision_of`

Source ID of the immediately prior content registered at the same path.

`null` when no prior revision is known.

### `revision_root`

Earliest known source ID in the revision lineage.

May be `null` for an original source with no predecessor.

### `revision_number`

Integer revision position.

Original source:

`1`

Next changed content at the same path:

`2`

and so on.

### `revised_by`

List of source IDs created as direct revisions of this source.

Revision lineage describes content history only. It does not mean the newer content is scientifically better, corrected, or authoritative.

## Extraction Field

### `extracted_path`

Path to the deterministic extracted-text artifact.

Default directory:

`.knowledgecraft/research/extracted/`

Extraction must fail when no registered path can be hash-verified against the source's `sha256`.

## Artifacts

### `artifacts`

Object keyed by lifecycle stage.

Each value is a list of existing artifact paths.

Example:

```json
{
  "artifacts": {
    "grounded": [
      "D:/project/.knowledgecraft/research/grounded/SRC-...-source-card.yaml",
      "D:/project/.knowledgecraft/research/grounded/SRC-...-claim-ledger.yaml"
    ],
    "ideas_created": [
      "D:/project/.knowledgecraft/research/insights/SRC-...-insights.yaml"
    ]
  }
}
```

Multiple artifacts may belong to the same stage.

Do not collapse multiple grounded files into one path field.

Older version-1 artifact strings are migrated to one-element lists.

## History

### `history`

Append-only list of important registry events.

Typical events:

```json
{
  "at": "2026-08-16T07:00:00+00:00",
  "event": "discovered",
  "path": "D:/Research/paper.pdf"
}
```

```json
{
  "at": "2026-08-16T07:10:00+00:00",
  "event": "status",
  "from": "extracted",
  "to": "grounded",
  "forced": false
}
```

```json
{
  "at": "2026-08-16T07:20:00+00:00",
  "event": "artifact_added",
  "stage": "grounded",
  "path": "D:/project/.knowledgecraft/research/grounded/SRC-...-claim-ledger.yaml"
}
```

Other valid implementation events may include:

- `path_added`
- `path_reassigned`
- `primary_path_changed`
- `revision_created`
- `extraction_refreshed`
- `failed`

History should not be rewritten solely for cosmetic cleanup.

## Error Field

### `error`

`null` when no current processing error is recorded.

Otherwise contains the latest relevant extraction/processing error string.

Successful extraction clears the prior extraction error.

## Duplicate Rules

### Same bytes, same path

Same source.

No duplicate source record.

### Same bytes, different filename

Same source.

Add the new path to the existing source.

### Same bytes, different folder

Same source.

Add the new path to the existing source.

### Different bytes, same path

New source content.

Create a new source record and revision link.

Preserve the previous source record.

## Registry Migration

Version-1 registries are migrated in memory when loaded and written as version 2 on save.

Migration is additive where practical.

Important compatibility behavior:

- old single-string artifact paths become one-element artifact lists;
- missing v2 path-state fields are created;
- missing revision metadata receives safe defaults;
- existing source IDs and hashes are preserved.

Do not allocate new source IDs merely because a version-1 registry is being migrated.

## Ownership Boundaries

The registry manages:

- source identity;
- paths;
- revisions;
- extraction state;
- workflow state;
- artifact references;
- audit history.

The registry does not determine:

- scientific findings;
- causal meaning;
- construct interpretation;
- study limitations not explicitly grounded;
- mechanisms;
- practical recommendations.

Those responsibilities belong to the scientific grounding and insight skills.
