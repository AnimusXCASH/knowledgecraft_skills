# KnowledgeCraft Architecture

KnowledgeCraft is a skill-oriented workflow framework for OpenCode.

It is designed around a simple architectural principle:

> Each skill owns one bounded responsibility, produces explicit artifacts, and hands work to the next specialist only when its contract is satisfied.

The framework is intentionally not a single monolithic agent.

## Repository roles

The repository has two distinct operational areas.

### `.opencode/skills/`

Reusable skill definitions and their deterministic tooling.

This directory is intended to be committed to Git.

Example:

```text
.opencode/
  skills/
    research-source-grounder/
      SKILL.md
    linkedin-calendar-planner/
      SKILL.md
      scripts/
        validate_linkedin_calendar.py
        test_validate_linkedin_calendar.py
```

### `.knowledgecraft/`

Generated working state and local artifacts.

Typical structure:

```text
.knowledgecraft/
  research/
    registry/
    extracted/
    grounded/
    insights/
    synthesis/
  writing/
  applied/
  content/
    ideas/
    drafts/
    approved/
    calendar/
  analytics/
  scratch/
```

Generated artifacts should not be written into `.opencode/skills/`.


## Input boundary

KnowledgeCraft should keep raw user inputs separate from generated workflow state.

Recommended project convention:

```text
<project>/
├── papers/                         # user-provided research sources
├── .opencode/skills/               # reusable KnowledgeCraft skills
└── .knowledgecraft/                # generated state/artifacts
```

The default research input convention is:

```text
./papers/
```

A source can also remain anywhere else if the user supplies its explicit path.

The important boundary is:

```text
papers/ or explicit source path
        ↓
      INPUT

.knowledgecraft/
        ↓
GENERATED STATE / OUTPUT
```

`research-library` owns source registration, deterministic identity, path tracking, extraction, duplicate/revision detection, and lifecycle state.

Raw papers should not be manually stored in generated artifact directories such as:

```text
.knowledgecraft/research/grounded/
.knowledgecraft/research/insights/
```

The repository's `papers/.gitignore` convention is intended to reduce accidental commits of local/copyrighted/private research files.

## Core lifecycle

KnowledgeCraft uses the following primary research-to-publication lifecycle:

```text
new
→ extracted
→ grounded
→ ideas_created
→ series_planned
→ drafted
→ qa_approved
→ scheduled
→ published
```

Exceptional states:

```text
failed
ignored
```

Lifecycle state is evidence of actual workflow progress, not an aspiration.

## Skill categories

### Foundation

`karpathy-guidelines`

Provides reasoning and implementation discipline adapted for KnowledgeCraft.

### Research

`research-library`

Owns:

- deterministic source identity;
- registry state;
- revisions;
- extraction;
- source-path tracking;
- lifecycle state.

`research-batch`

Owns:

- multi-source orchestration;
- stage batching;
- structured batch reporting.

`research-source-grounder`

Owns:

- source-faithful source cards;
- claim ledgers;
- relationship preservation;
- null-result preservation;
- causal-language protection.

`research-insight-miner`

Owns:

- controlled interpretation;
- applied/research communication angles;
- cross-source synthesis;
- insight traceability.

### Writing and voice

`author-voice-profiler`

Creates evidence-based voice profiles from genuine writing samples.

`author-voice-editor`

Aligns writing with a validated author profile without changing protected meaning.

`text-naturalness-editor`

Performs conservative prose-quality refinement.

`text-humanizer`

Provides direct protected-span humanization when explicitly requested.

It is intentionally not an automatic stage in the standard LinkedIn pipeline.

### Quality

`factuality-guard`

Owns final claim-level factuality review.

`content-quality-gate`

Owns final content quality decisions:

```text
APPROVE
REVISE
BLOCK
```

Factuality is a prerequisite, not a quality score.

### LinkedIn

`linkedin-series-architect`

Owns multi-post decomposition and drafting briefs.

`linkedin-post-drafter`

Turns one approved brief into one evidence-safe post draft.

`linkedin-platform-review`

Owns LinkedIn presentation review only.

`linkedin-calendar-planner`

Owns scheduling, dependencies, blackout dates, collisions, and calendar readiness.

`linkedin-performance-review`

Owns performance metrics, transparent rates, cautious comparison, and reusable learnings.

`linkedin-content-pipeline`

Owns orchestration only.

It decides:

- what state exists;
- what is missing;
- which specialist owns the next step;
- whether a validator passed;
- whether lifecycle may advance.

It does not duplicate specialist logic.

## LinkedIn reference architecture

```text
grounded claims / insights
        ↓
linkedin-series-architect
        ↓
linkedin-post-drafter
        ↓
author-voice-editor
        ↓
text-naturalness-editor
        ↓
linkedin-platform-review
        ↓
factuality-guard
        ↓
content-quality-gate
        ↓
qa_approved
        ↓
linkedin-calendar-planner
        ↓
scheduled
        ↓
human / authorized publication
        ↓
published
        ↓
linkedin-performance-review
        ↓
qualified learnings
        └────────────→ future series planning
```

`text-humanizer` remains optional and explicit.

## Responsibility boundaries

KnowledgeCraft avoids overlapping skill ownership.

Examples:

### Grounder vs insight miner

Grounder:

```text
What does the source actually support?
```

Insight miner:

```text
What controlled interpretation or communication angle can safely be derived from those grounded claims?
```

### Post drafter vs platform review

Post drafter:

```text
What should the evidence-safe post say?
```

Platform review:

```text
How should this already-safe post be presented for LinkedIn?
```

### Factuality vs quality

Factuality:

```text
Is the substantive content supportable?
```

Quality:

```text
Is the supportable content good enough to approve?
```

### Calendar planner vs performance review

Calendar planner:

```text
When and in what sequence should approved content be scheduled?
```

Performance review:

```text
What can cautiously be learned from actual published performance?
```

## Artifact-first architecture

Structured artifacts are the primary interface between stages.

Examples:

```text
source card
claim ledger
insight bundle
series plan
post draft
platform review
factuality audit
quality-gate decision
calendar
performance review
pipeline report
```

Conversational summaries are secondary.

When structured artifact state conflicts with conversational prose, inspect the artifact.

## Validator architecture

Where a contract is mechanically testable, KnowledgeCraft uses deterministic validation.

Typical pattern:

```text
SKILL.md
scripts/
  validate_<artifact>.py
  test_validate_<artifact>.py
```

The governing rule is:

```text
validator FAIL blocks lifecycle advancement
```

Semantic judgment cannot override deterministic failure.

## Revision and stale-state architecture

Downstream approval is version-sensitive.

A material text change after QA invalidates stale approval:

```text
material text revision
→ factuality-guard
→ content-quality-gate
```

A material source revision may invalidate:

```text
grounding
→ insights
→ series
→ drafts
→ QA
```

Only affected downstream artifacts should be rerun.

Unrelated sources/items should remain valid.

## Failure isolation

KnowledgeCraft is item-aware.

If three posts are being prepared and:

- one is valid;
- one needs author input;
- one fails a validator;

the valid post may continue.

The pipeline reports state per item rather than globally blocking everything.

## Publication boundary

KnowledgeCraft does not infer publication.

The normal boundary is:

```text
scheduled
→ human / authorized publisher
→ published
```

A scheduled date passing is not evidence that publication occurred.

## Performance feedback loop

Performance analytics produce qualified learnings:

```text
strong_observation
tentative_pattern
test_next
insufficient_data
```

These classifications remain attached when reused.

KnowledgeCraft does not convert:

```text
tentative_pattern
```

into:

```text
platform rule
```

and does not convert:

```text
strong_observation
```

into:

```text
causal explanation
```

## Design principles

KnowledgeCraft should remain:

- modular;
- source-grounded;
- artifact-first;
- validator-aware;
- idempotent where practical;
- conservative about causality;
- conservative about platform folklore;
- explicit about missing information;
- safe to resume from the latest valid stage;
- open to extension without turning into a monolith.
