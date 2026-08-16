---
name: research-batch
description: Resume and batch-process only new or unfinished research sources from a local research registry. Use for requests such as process new papers, catch up the research folder, process everything not yet grounded, or continue where a previous research-to-content workflow stopped.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "research-orchestration"
  opencode/slash: "true"
---

# Research Batch

Use this skill to orchestrate multiple research sources through the existing KnowledgeCraft research pipeline.

This skill does not own source identity, scientific grounding, or insight interpretation.

It coordinates:

- `research-library` for source identity, registry state, extraction, artifacts, and lifecycle;
- `research-source-grounder` for strict source-faithful grounding;
- `research-insight-miner` for controlled interpretation and validated insight generation.

Load `research-library` first.

## Default Goal

When the user says only:

- `process new research`;
- `process new papers`;
- `catch up the research folder`;
- `continue unfinished research`;
- `process everything pending`;

the default terminal stage is:

`ideas_created`

Default flow:

`scan -> extract -> ground -> validate/register grounding artifacts -> mine insights -> validate/register insight artifact -> ideas_created`

Do not automatically continue into content planning, drafting, publishing, or scheduling unless the user explicitly requests downstream work.

## Core Batch Principle

Process sources **one complete source at a time** by default.

Preferred order:

1. determine current registry state;
2. determine the next valid action;
3. complete that action;
4. validate its required artifacts;
5. update the registry;
6. continue until the source reaches the requested terminal stage;
7. only then move to the next source.

Do not ground multiple sources simultaneously and then try to reconcile artifacts afterward unless cross-source synthesis is explicitly requested.

This reduces source mixing, artifact misregistration, and claim leakage between papers.

## Source Selection

Use the research-library registry as the source of truth for what is pending.

Do not decide that a source is new or complete from filenames or directory contents alone.

Typical eligible states for the default `ideas_created` target:

- `new`
- `failed`
- `extracted`
- `grounded`

Typical default stop states:

- `ideas_created`
- `series_planned`
- `drafted`
- `qa_approved`
- `scheduled`
- `published`
- `ignored`

Do not process `ignored` sources unless the user explicitly asks to restore or process them.

Do not downgrade sources already beyond the requested terminal stage.

## Resume Matrix

For the default terminal stage `ideas_created`:

### `new`

Next:

`extract`

Then continue to grounding and insight mining.

### `failed`

Inspect the current error and determine whether the failed operation can be retried safely.

For extraction failures, use the research-library extraction retry.

Do not silently clear or bypass the failure.

### `extracted`

Next:

`research-source-grounder`

After valid grounding artifacts exist:

`extracted -> grounded`

Then continue to insight mining.

### `grounded`

Verify the registered grounding artifacts exist and are usable.

Then use:

`research-insight-miner`

After validator PASS:

`grounded -> ideas_created`

### `ideas_created`

Default batch target already reached.

Stop for this source unless the user requested a later stage.

### Later lifecycle stages

Do not move backward.

If the requested terminal stage has already been reached or exceeded, leave the source unchanged.

## Artifact Completeness Rule

Registry status alone is not sufficient evidence that a stage is complete.

Before resuming from a stage that depends on artifacts, verify the required artifacts exist.

### Grounded stage requires

At minimum:

- source card;
- claim ledger.

Both must belong to the same source ID.

If the registry says `grounded` but one or both required artifacts are missing:

- treat the grounding stage as incomplete;
- do not proceed to insight mining;
- regenerate or repair grounding artifacts using `research-source-grounder`;
- register the repaired artifacts;
- preserve the existing lifecycle state unless a deterministic repair requires otherwise.

### Ideas-created stage requires

At minimum:

- validated insight artifact.

The artifact must pass the current deterministic `research-insight-miner` validator.

If the registry says `ideas_created` but the insight artifact is missing or fails validation:

- treat the insight stage as incomplete;
- repair or regenerate the insight artifact;
- rerun validation;
- do not advance further until PASS.

Do not mark a stage complete merely because a tool or model attempted it.

## Identity Rule

Always use the stable `SRC-...` source ID assigned by `research-library`.

When grounding a registered source:

- reuse its existing source ID;
- never allocate `SRC-UNREGISTERED-...`;
- never create a second source identity for extracted text derived from the same registered source.

When mining insights:

- use claim IDs derived from the registered grounded source;
- preserve source/claim traceability.

## Extraction Rule

Use `research-library` extraction.

Do not implement a second extraction system inside this skill.

Extraction must use a path that hash-verifies against the registered SHA-256 content.

Re-extraction of a source already at a later normal lifecycle stage may refresh extraction output but must not downgrade lifecycle status.

## Grounding Handoff

For every source requiring grounding, invoke `research-source-grounder`.

The grounder must remain responsible for:

- source-only scientific grounding;
- relationship-language preservation;
- causal-status preservation;
- missing-information handling;
- claim-ledger creation;
- source-card creation.

The batch orchestrator must not summarize or reinterpret the source itself as a shortcut.

After valid grounding artifacts are produced:

1. confirm they use the same registered source ID;
2. confirm both artifacts exist;
3. register both with `research-library`;
4. advance `extracted -> grounded` without `--force`.

## Insight Handoff

For every source requiring insights, invoke `research-insight-miner`.

The insight miner must remain responsible for:

- controlled interpretation;
- source/claim traceability;
- inference-level labeling;
- relationship-language fidelity;
- causal-status fidelity;
- deterministic validation.

After the insight artifact is generated:

1. run the deterministic validator;
2. if FAIL, repair only necessary fields and rerun;
3. do not continue until PASS;
4. register the validated artifact with `research-library`;
5. advance `grounded -> ideas_created` without `--force`.

## No Force by Default

Do not use research-library `--force` during normal batch processing.

A lifecycle transition that requires `--force` is a signal to inspect the source state.

Use `--force` only when:

- the user explicitly requests a non-standard lifecycle override; or
- an already-understood registry repair requires it and the user has authorized the repair.

Batch processing must never use `--force` merely to make the workflow continue.

## Failure Isolation

A failure in one source must not corrupt or invalidate completed work for another source.

If one source fails:

1. record the exact failing source ID;
2. preserve its current registry/error state;
3. do not fabricate completion artifacts;
4. do not mark the failed stage complete;
5. continue with other independent sources only when doing so is safe and consistent with the user's request.

At final reporting, distinguish:

- completed;
- already complete;
- skipped;
- failed;
- ignored.

Do not report the whole batch as fully successful when one or more requested sources failed.

## Retry Rule

Retries must resume from the earliest incomplete valid stage.

Examples:

- extraction failed -> retry extraction;
- extraction exists but grounding missing -> ground;
- grounding valid but insights missing -> mine insights;
- insight artifact exists but validator FAIL -> repair insights and rerun validator.

Do not restart the full pipeline unnecessarily.

## Idempotence

Running the same batch request again should not duplicate work or source records.

A repeated batch run should:

- retain the same SHA-256 source IDs;
- skip sources already at or beyond the requested terminal stage when their required artifacts are valid;
- avoid duplicate registry entries;
- avoid duplicate artifact registration;
- continue only unfinished or invalid stages.

## Revision Handling

A revised file is a distinct content identity managed by `research-library`.

If scanning discovers changed content at a previously known path:

- process the new revision under its new source ID;
- preserve the previous source and its artifacts;
- do not overwrite prior grounding or insights;
- do not assume findings from the previous revision apply to the new revision.

Each revision must be grounded and interpreted independently unless the user explicitly requests revision comparison.

## Cross-Source Synthesis Boundary

Default batch processing is source-by-source.

Do not create cross-source synthesis merely because multiple papers are processed in the same batch.

Cross-source synthesis requires an explicit request or a clearly defined synthesis stage.

When synthesis is requested:

- use grounded/validated artifacts rather than raw source memory;
- preserve each source's relationship terminology and causal status;
- keep all source IDs and claim IDs traceable;
- use the cross-source rules from `research-insight-miner`.

## Downstream Work

Do not automatically continue beyond `ideas_created`.

If the user explicitly requests later work:

- `ideas_created -> series_planned`: use the appropriate planning skill;
- `series_planned -> drafted`: use the appropriate drafting skill;
- `drafted -> qa_approved`: use the appropriate quality/review skill;
- later scheduling/publishing stages only when explicitly requested.

The batch skill coordinates state; specialist skills own substantive work.

## Batch Reporting

After processing, provide a concise deterministic report.

Include:

- number of sources inspected;
- number newly registered;
- number completed to requested target;
- number already at target or beyond;
- number skipped/ignored;
- number failed;
- failed source IDs with exact stage/error when any;
- final target stage.

For each processed source, retain source ID and final status.

Do not add a fresh scientific summary of every paper unless the user asks for one.

## Default Batch Completion Criteria

For a default `process new research` request, the batch is complete only when every requested eligible source is in one of these states:

- `ideas_created` with valid required artifacts;
- beyond `ideas_created` with valid required artifacts;
- `ignored`;
- explicitly reported `failed`.

A batch containing failures may be operationally finished but must be reported as **completed with failures**, not PASS.

## Verification

Before reporting batch completion, verify:

- `research-library` was used as registry source of truth? YES
- stable registered source IDs reused? YES
- no duplicate identities created during grounding? YES
- each source resumed from its actual current state? YES
- required artifacts checked before downstream processing? YES
- grounding delegated to `research-source-grounder`? YES
- insights delegated to `research-insight-miner`? YES
- insight validator PASS before `ideas_created` registration? YES
- no normal lifecycle transition used `--force`? YES
- completed sources processed one-at-a-time by default? YES
- failures isolated and reported accurately? YES
- already-complete sources not redundantly reprocessed? YES
- default processing stopped at `ideas_created`? YES
