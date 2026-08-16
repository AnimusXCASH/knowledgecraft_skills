---
name: linkedin-content-pipeline
description: Orchestrate the KnowledgeCraft evidence-grounded LinkedIn workflow from research readiness through series planning, one-post drafting, editing, platform review, factuality and quality gates, scheduling, publication-state tracking, and optional performance learning without duplicating specialist skill logic.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "orchestration"
  opencode/slash: "true"
---

# LinkedIn Content Pipeline

Orchestrate the end-to-end KnowledgeCraft LinkedIn workflow.

This skill decides **what stage comes next, which specialist skill owns it, and whether the workflow may advance**.

It does not perform the specialist work itself.

## Core Principle

Use the smallest necessary sequence of specialist skills.

The pipeline owns routing and state transitions.

Each specialist skill owns its own substantive method.

Do not duplicate:

- research grounding;
- insight creation;
- series design;
- drafting;
- voice editing;
- naturalness editing;
- platform review;
- factuality review;
- quality scoring;
- calendar scheduling;
- performance interpretation.

## Responsibility Boundary

`linkedin-content-pipeline` owns:

- workflow-state inspection;
- next-step routing;
- prerequisite checks;
- lifecycle transition control;
- resume/retry behavior;
- failure isolation;
- artifact handoff;
- orchestration reporting;
- human-review boundaries;
- optional performance-learning loop.

It does **not**:

- write research claims;
- create insights;
- draft posts;
- edit prose;
- calculate platform metrics;
- invent approval;
- invent publication status;
- infer platform ranking rules;
- publish content unless a separate explicitly authorized publishing workflow exists.

## Normal Lifecycle

The KnowledgeCraft lifecycle is:

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

Do not skip required lifecycle stages merely because a downstream artifact can technically be created.

## Stage Ownership

Use these owners:

### Research readiness

`research-library`

Owns:

- source identity;
- registry state;
- revision tracking;
- lifecycle state;
- stage artifacts.

### Bulk research completion

`research-batch`

Use when multiple sources are new/incomplete and the target is a research stage.

Do not use it for LinkedIn drafting or QA.

### Grounding

`research-source-grounder`

Owns:

- source cards;
- claim ledgers;
- source-faithful factual grounding.

### Insight creation

`research-insight-miner`

Owns:

- controlled interpretation;
- communication angles;
- applications/questions;
- evidence gaps;
- synthesis insights.

### Series planning

`linkedin-series-architect`

Owns:

- series decomposition;
- reader jobs;
- claim/insight allocation;
- dependencies;
- overlap control;
- drafting briefs.

### Post drafting

`linkedin-post-drafter`

Owns:

- one-post draft from one approved brief;
- used-vs-available claim/insight traceability;
- missing author input;
- evidence-safe first draft.

### Author voice

`author-voice-profiler`

Use only when genuine author writing samples exist and no suitable current profile exists.

Do not fabricate a profile.

`author-voice-editor`

Owns:

- evidence-based voice alignment.

### Naturalness

`text-naturalness-editor`

Owns:

- conservative prose-quality cleanup;
- mechanical/generic wording reduction;
- readability without detector optimization.

### Optional direct humanization

`text-humanizer`

Do **not** include automatically in the standard pipeline.

Use only when the user explicitly requests humanization/direct rewriting or the workflow specifically calls for that protected-span editing mode.

### LinkedIn presentation

`linkedin-platform-review`

Owns:

- first-screen clarity;
- mobile readability;
- CTA/hashtag/mention/link fit;
- format suitability;
- platform-folklore guard.

### Factuality

`factuality-guard`

Owns:

- final claim-level evidence verification;
- causal/relationship/uncertainty fidelity;
- unsupported-claim detection.

### Final quality

`content-quality-gate`

Owns:

- final quality decision:
  `APPROVE`
  `REVISE`
  `BLOCK`

Factuality is an upstream prerequisite, not a quality score.

### Calendar

`linkedin-calendar-planner`

Owns:

- approved-post sequencing;
- dates/windows;
- dependencies;
- collisions;
- schedule readiness.

### Performance learning

`linkedin-performance-review`

Owns:

- raw metrics;
- transparent rates;
- cautious comparisons;
- learning classifications;
- future tests.

## Default Workflow

For a new evidence-based LinkedIn content request:

```text
research-library
    ↓
research-source-grounder
    ↓
research-insight-miner
    ↓
linkedin-series-architect
    ↓
linkedin-post-drafter
    ↓
author-voice-editor            [if profile available/needed]
    ↓
text-naturalness-editor        [if naturalness refinement needed]
    ↓
linkedin-platform-review
    ↓
factuality-guard
    ↓
content-quality-gate
    ↓
linkedin-calendar-planner      [only when scheduling requested]
```

Do not invoke every skill automatically.

Inspect current state first.

## Skill-First Routing

If a required stage has a dedicated skill, load/use that skill.

The pipeline should not approximate specialist behavior in prose.

Examples:

- missing grounding -> route to `research-source-grounder`;
- missing insights -> route to `research-insight-miner`;
- overlap in series -> route to `linkedin-series-architect`;
- factuality BLOCK -> route back to the stage that introduced the unsupported claim;
- quality REVISE -> route to the skill matching the revision type.

## State Inspection Before Work

Before routing, inspect:

1. source registry state;
2. existing stage artifacts;
3. validator status where applicable;
4. post/series approval state;
5. whether requested output already exists and is current;
6. whether an upstream revision made downstream artifacts stale.

Do not recreate valid current artifacts unnecessarily.

## Artifact Truth Rule

Prefer structured artifacts and their validators over conversational summaries.

Examples:

- valid grounded claim ledger > remembered source summary;
- validated series-plan YAML > prose description of the plan;
- validated post-draft YAML > chat claim that draft is ready;
- factuality audit > generic statement that facts look correct;
- quality-gate artifact > assumption that content is approved;
- validated calendar > narrative schedule summary.

If chat text conflicts with the structured artifact, inspect the artifact.

## Validator Rule

When a specialist skill has a deterministic validator, the pipeline must require validator PASS before treating that artifact as mechanically complete.

Current validated LinkedIn stages include:

- `linkedin-series-architect`;
- `linkedin-post-drafter`;
- `linkedin-platform-review`;
- `linkedin-calendar-planner`;
- `linkedin-performance-review`.

Other KnowledgeCraft validators should also be respected when their stages are used.

A semantic model claim of `PASS` does not override a deterministic validator `FAIL`.

## Research Readiness Routing

If source status is:

### `new`

Route to extraction/grounding workflow.

### `extracted`

Route to `research-source-grounder`.

### `grounded`

Route to `research-insight-miner`.

### `ideas_created`

Research side is ready for LinkedIn planning.

Do not regenerate insights unless:

- explicitly requested;
- source revision makes them stale;
- validator fails;
- existing insights do not address the requested communication objective.

## Series Routing

If no valid series plan exists and multi-post planning is requested:

route to:

`linkedin-series-architect`

Do not mass-draft first and organize later.

If only one standalone post is requested:

a full series plan is not mandatory.

Create/use a minimal approved post brief and route to `linkedin-post-drafter`.

## Drafting Routing

Draft only briefs with safe upstream status.

Do not draft:

- blocked briefs;
- story briefs missing genuine story input;
- evidence-bearing briefs missing required traceability.

Default to one post at a time.

Batch drafting requires explicit request or a validated workflow reason.

## Voice Routing

If the user wants author-specific voice:

### Existing current profile

Use `author-voice-editor`.

### Genuine samples supplied but no profile

Route:

```text
author-voice-profiler
→ author-voice-editor
```

### No genuine samples

Do not invent a voice profile.

Proceed without profile or request samples if voice matching is material.

## Naturalness Routing

Use `text-naturalness-editor` only when the draft benefits from conservative naturalness/readability refinement.

Do not force a naturalness pass on already-clean text.

Do not automatically invoke `text-humanizer`.

`text-humanizer` remains an optional direct editing tool.

## Platform Review Routing

Before factuality QA, run `linkedin-platform-review` when the destination is LinkedIn and presentation review is needed.

Its output may alter presentation.

Therefore factuality review should assess the **post-platform-review text**, not an older draft.

## Factuality Gate

No evidence-bearing post may advance to final quality approval when:

`factuality-guard = BLOCK`

When factuality identifies:

- unsupported claim;
- overstatement;
- conflicting number;
- invented relationship;
- causal overstatement;
- unsupported mechanism;

route the issue back to the stage that introduced it.

Do not let later editors "smooth over" a factuality blocker.

## Quality Gate

`content-quality-gate` runs after factuality.

Allowed outcomes:

### `APPROVE`

Eligible for:

`qa_approved`

### `REVISE`

Do not advance lifecycle.

Route the revision according to issue type.

### `BLOCK`

Do not advance lifecycle.

Resolve the blocker or stop.

## Revision Routing

Use the smallest relevant owner.

Examples:

### Evidence problem

```text
factuality-guard
→ research-source-grounder / research-insight-miner / linkedin-post-drafter
```

depending on where drift occurred.

### Voice problem

```text
content-quality-gate
→ author-voice-editor
```

### Mechanical/generic prose

```text
content-quality-gate
→ text-naturalness-editor
```

### LinkedIn presentation problem

```text
content-quality-gate or platform review
→ linkedin-platform-review
```

### Series duplication

```text
content-quality-gate
→ linkedin-series-architect
```

Do not rerun the entire pipeline when one local repair is enough.

## Re-QA After Revision

Any material text revision after factuality review requires factuality to be reconsidered.

Any material text revision after quality approval invalidates the prior approval.

Safe rule:

```text
material text change
→ factuality-guard
→ content-quality-gate
```

before returning to `qa_approved`.

Do not preserve stale QA status after content changes.

## Approval Transition

Set lifecycle to:

`qa_approved`

only when:

- factuality review passes;
- content quality returns `APPROVE`;
- the approved text is the same substantive version that was reviewed;
- no unresolved author input remains.

Do not infer approval from:

- a good-looking draft;
- platform-review PASS;
- user enthusiasm;
- a semantic regression artifact.

## Scheduling Routing

Run `linkedin-calendar-planner` only for content that needs a publication calendar.

Only `qa_approved` content may become `scheduled`.

Provisional calendar placement does not advance lifecycle.

Respect the calendar planner's distinction between:

- planner correctness;
- calendar readiness;
- needs decision;
- blocked dependency;
- hard collision.

## Publication Boundary

This pipeline does not publish by itself.

Default boundary:

```text
scheduled
→ human publication
→ published
```

Only mark `published` when actual publication is confirmed by:

- user;
- authorized publishing system;
- verified platform record.

Do not mark scheduled content as published merely because the publication date passed.

## Performance Loop

When actual post metrics are available:

```text
published posts
    ↓
linkedin-performance-review
    ↓
qualified learnings
    ↓
linkedin-series-architect
```

Only reuse learnings that retain their classification and caveats.

Do not convert:

`tentative_pattern`

into:

`platform rule`.

Do not convert:

`strong_observation`

into:

`causal explanation`.

## Performance Learning Does Not Rewrite History

Do not alter historical approved/published posts to make prior decisions appear aligned with later analytics.

Performance learnings apply prospectively.

## Human Review Boundary

Human review remains required for publication unless the user explicitly configures an authorized publishing workflow.

The pipeline may produce:

- approved content;
- schedule-ready content;
- publication checklist.

It must not imply autonomous publishing permission.

## Resume Rule

Resume from the latest valid current stage.

Examples:

### Existing grounded source + valid insights

Start at series planning.

### Existing valid series plan + no draft

Start at post drafting.

### Existing valid draft + no voice/platform QA

Start at the next required editing/review stage.

### Existing factuality PASS + quality REVISE

Repair only the specified quality issue, then rerun required QA.

### Existing `qa_approved` post + scheduling request

Start at calendar planning.

Do not restart research unnecessarily.

## Idempotence Rule

Rerunning the pipeline without changed inputs should not:

- duplicate source IDs;
- duplicate insights;
- duplicate series briefs;
- duplicate draft IDs unnecessarily;
- advance lifecycle twice;
- overwrite approved content with a new version silently.

If current validated artifacts already satisfy the requested stage, report/reuse them.

## Source Revision Rule

If a source revision invalidates upstream evidence:

1. follow `research-library` revision/staleness rules;
2. treat affected grounding/insights/content as potentially stale;
3. do not preserve downstream approval blindly;
4. rerun only affected stages.

A new source version must not silently inherit old factual approval.

## Failure Isolation

A failure for one post should not automatically block unrelated posts.

Examples:

- one story post needs author input;
- one draft fails factuality;
- one scheduled post has a dependency problem.

Continue valid independent items when appropriate.

Report per-item state clearly.

## Stop Conditions

Stop and report rather than approximate when:

- required grounded evidence is missing;
- requested personal story is missing;
- specialist validator fails and cannot be repaired safely;
- factuality is blocked;
- quality is blocked;
- user decision is required;
- publishing authorization is absent for a requested automated publication action.

## Do Not Invent Workflow Success

Never report:

- grounded;
- validated;
- approved;
- scheduled;
- published;

unless the corresponding artifact/state supports it.

A narrative statement is not a substitute for a state transition.

## Output Location

Default orchestration report:

`.knowledgecraft/content/linkedin-pipeline-report.yaml`

Optional readable summary:

`.knowledgecraft/content/linkedin-pipeline-report.md`

Do not write generated workflow artifacts into `.opencode/skills/`.

## Output Contract

Use:

```yaml
linkedin_content_pipeline:
  run_id: "LCPIP-001"
  requested_goal: ""
  mode: "standalone_post|series|research_to_content|qa_only|calendar_only|performance_learning"
  inspected_state:
    source_ids: []
    series_plan: null
    post_ids: []
    current_lifecycle_states: {}
    stale_artifacts: []
  routing:
    - step: 1
      item_id: ""
      from_state: ""
      required_skill: ""
      reason: ""
      status: "pending|completed|skipped|blocked|needs_input|failed"
      artifact: null
      validator_required: false
      validator_status: "not_required|not_run|pass|fail"
  item_states:
    - item_id: ""
      item_type: "source|series|post|calendar|performance_review"
      lifecycle_before: null
      lifecycle_after: null
      current_status: ""
      blockers: []
      next_required_skill: null
      artifact_refs: []
  qa:
    - post_id: ""
      factuality_status: "not_run|pass|block"
      quality_status: "not_run|APPROVE|REVISE|BLOCK"
      qa_approved: false
  calendar:
    requested: false
    artifact: null
    ready_to_schedule: null
  publication:
    authorized_workflow_present: false
    published_confirmed: false
  performance_loop:
    requested: false
    reusable_learning_ids: []
  summary:
    completed_steps: 0
    skipped_steps: 0
    blocked_items: 0
    failed_items: 0
    needs_input_items: 0
  handoff:
    workflow_complete_for_requested_goal: false
    next_action: ""
    notes: []
```

## Routing Status Semantics

Use:

### `pending`

Step has not run.

### `completed`

Required specialist stage completed and required validation passed.

### `skipped`

Stage was unnecessary because a valid current artifact already satisfied it.

### `blocked`

Upstream state prevents safe continuation.

### `needs_input`

User input is required.

### `failed`

Execution/validation failed.

Do not use `completed` for a specialist stage that returned a blocker.

## Lifecycle Reporting

`lifecycle_after` must be:

- a valid actual lifecycle state; or
- unchanged from `lifecycle_before`.

Do not use aspirational states.

Example:

A post that passes platform review but has not yet passed factuality/quality remains:

`drafted`

not:

`qa_approved`.

## Workflow Completion

Set:

`workflow_complete_for_requested_goal: true`

only when the user's requested goal has actually been achieved.

Examples:

### Goal: "Draft this LinkedIn post"

Complete when a requested draft artifact is produced at the requested level.

It does not require scheduling.

### Goal: "Get this ready to publish"

Complete only after required factuality + quality approval.

### Goal: "Create a calendar"

Complete when the requested calendar artifact is produced, even if it correctly contains `needs_decision` entries, provided the requested planning work is complete.

Do not confuse:

`workflow completed`

with:

`every item operationally ready`.

### Goal: "Publish it"

Do not mark complete without authorized/confirmed publication.

## Deterministic Orchestration Validation

After writing the structured pipeline report, validate its mechanical consistency before reporting completion.

Run:

```powershell
py ".opencode/skills/linkedin-content-pipeline/scripts/validate_linkedin_content_pipeline.py" ".knowledgecraft/content/linkedin-pipeline-report.yaml"
```

If validation returns `FAIL`:

1. do not report the pipeline run as complete;
2. read every validation error;
3. repair only the affected orchestration-report fields;
4. do not manufacture specialist success to satisfy the validator;
5. rerun the validator until `PASS`.

The validator checks:

- valid YAML and required top-level structure;
- allowed pipeline modes;
- unique routing steps and item-state IDs;
- allowed routing and validator statuses;
- `completed` specialist steps cannot retain validator `fail`;
- steps requiring validators cannot be `completed` with validator `not_run`;
- `skipped` validator stages cannot pretend to have executed a failing validator;
- lifecycle values use the KnowledgeCraft lifecycle vocabulary;
- QA records use allowed factuality/quality states;
- `qa_approved: true` requires factuality `pass` + quality `APPROVE`;
- an item advancing to `qa_approved` requires a matching approved QA record;
- calendar readiness fields are typed consistently;
- publication cannot be reported confirmed without an authorized/verified publication path;
- summary counts agree with routing/item states;
- `workflow_complete_for_requested_goal: true` cannot coexist with failed or blocked orchestration steps unless those items are explicitly outside the completed requested goal;
- generated handoff contains a concrete next action;
- published-confirmed state is not inferred merely from schedule metadata.

The validator intentionally does **not** decide:

- whether the chosen specialist route is semantically optimal;
- whether a skipped stage was truly unnecessary;
- whether a source revision materially invalidates downstream artifacts;
- whether a material edit really requires re-QA;
- whether a calendar `needs_decision` item should prevent goal completion;
- whether performance learnings are substantively reusable.

Those remain semantic orchestration responsibilities.

## Minimal Orchestration Rule

Do not run stages just because they exist.

Examples:

- no voice profile requested/available -> do not force voice profiling;
- clean prose -> naturalness editing may be skipped;
- standalone post -> series architect may be skipped;
- no scheduling request -> calendar planner should not run;
- no performance data -> performance review should not run.

## Orchestration Procedure

1. identify the user's actual requested goal;
2. inspect current registry/lifecycle/artifacts;
3. detect stale or invalid artifacts;
4. determine the minimum missing stages;
5. route each stage to its owning specialist skill;
6. require deterministic validator PASS where applicable;
7. preserve per-item blockers/needs-input states;
8. advance lifecycle only when transition requirements are satisfied;
9. rerun factuality + quality after material text revisions;
10. schedule only approved posts when requested;
11. stop at human publication boundary unless separately authorized;
12. run performance learning only from actual supplied metrics;
13. produce orchestration report with next action.

## Final Checks

Before completing a pipeline run, verify:

- requested goal identified? YES
- current state inspected before work? YES
- valid existing artifacts reused? YES
- stale artifacts not treated as current? YES
- specialist skills used instead of duplicated logic? YES
- only necessary stages run? YES
- deterministic validators respected? YES
- semantic PASS never overrode validator FAIL? YES
- research evidence traceability preserved? YES
- no personal story invented? YES
- no causal/relationship strengthening introduced by orchestration? YES
- no automatic text-humanizer pass added? YES
- material revisions invalidated stale QA? YES
- factuality PASS required before quality approval? YES
- quality APPROVE required for qa_approved? YES
- unapproved content not marked scheduled? YES
- scheduled content not marked published without confirmation? YES
- performance learning retained caveats? YES
- failures isolated per item where possible? YES
- lifecycle transitions accurate? YES
- workflow completion matched requested goal rather than aspirational end state? YES
- human publication boundary preserved? YES
- deterministic orchestration validator executed? YES
- deterministic orchestration validator returned PASS? YES
- generated artifacts saved outside `.opencode/skills/`? YES
