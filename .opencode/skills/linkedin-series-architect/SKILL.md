---
name: linkedin-series-architect
description: Design a coherent, evidence-traceable, non-repetitive multi-post LinkedIn series from grounded insights and claims. Use when planning several posts across days or weeks and when sequence, reader jobs, thematic arcs, claim allocation, dependencies, and series-level distinctiveness matter.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "series-planning"
  opencode/slash: "false"
---

# LinkedIn Series Architect

Design a coherent multi-post LinkedIn series from already grounded ideas.

The objective is to decide **which distinct posts should exist and how they should relate to one another**.

Do not draft full posts inside this skill.

## Responsibility Boundary

`linkedin-series-architect` owns:

- series decomposition;
- content pillars;
- reader job per post;
- claim/insight allocation;
- conceptual sequencing;
- dependency ordering;
- series-level overlap control;
- variation in post role and framing;
- continuity across the series;
- planning-level format recommendations;
- handoff briefs for `linkedin-post-drafter`.

It does **not**:

- create new research insights;
- invent evidence;
- write complete posts;
- perform author-voice editing;
- perform naturalness editing;
- perform factuality review;
- perform final content-quality review;
- decide exact publication dates unless explicitly asked as part of planning;
- analyze performance data;
- claim platform ranking effects.

Related skills:

- `research-insight-miner` -> creates grounded/traceable insights;
- `linkedin-post-drafter` -> drafts one post from one approved brief;
- `linkedin-calendar-planner` -> places approved posts into a publishing calendar;
- `linkedin-platform-review` -> reviews finished drafts for LinkedIn presentation;
- `linkedin-performance-review` -> learns cautiously from post-performance data;
- `linkedin-content-pipeline` -> orchestrates the workflow.

## Required Inputs

Prefer:

1. grounded insight records;
2. supporting claim IDs;
3. source IDs;
4. intended audience;
5. broad series objective;
6. optional number of posts;
7. optional cadence or timing constraints;
8. optional prior posts or existing series material.

If the user supplies only broad topics with no grounded insights:

- series planning may still be done at a conceptual level;
- clearly mark evidence-dependent briefs as `evidence_pending`;
- do not invent claim IDs or source support.

If a research-grounded series is requested but no grounded evidence is available, recommend completing grounding/insight mining before drafting evidence-bearing posts.

## Evidence Traceability Rule

Every research-grounded post brief must trace to existing evidence.

Use:

- `source_ids`;
- `supporting_claim_ids`;
- `supporting_insight_ids`.

Do not invent these IDs.

A post may use:

- one insight;
- several compatible insights;
- several supporting claims;

but it must have one clear central purpose.

If a post is purely reflective/opinion-based, mark that explicitly rather than pretending it is research-grounded.

## One Main Job Per Post

Every planned post needs one primary reader job.

Allowed default reader jobs:

- `setup`
- `teach`
- `challenge`
- `evidence`
- `application`
- `synthesis`
- `conversation`
- `story`

Definitions:

### `setup`

Introduces a problem, distinction, or context needed for later posts.

### `teach`

Explains a concept, framework, construct, or evidence-based distinction.

### `challenge`

Questions a common assumption or misconception using supplied evidence/insight.

### `evidence`

Centers one finding, evidence pattern, or result.

### `application`

Translates an already-supported insight into a practical question, decision, or reflection.

### `synthesis`

Combines several already-grounded ideas into a broader view.

### `conversation`

Invites a substantive discussion around an evidence-supported or clearly labeled opinion question.

### `story`

Uses a genuine supplied story, case, experience, or narrative.

A `story` post requires actual story material.

If no genuine story is supplied, mark:

`author_input_required: true`

Do not invent an anecdote.

## Reader-Job Separation

Avoid consecutive posts with identical reader jobs unless there is a clear reason.

Do not create a series where every post is:

```text
evidence → takeaway → question
```

or:

```text
misconception → correction → CTA
```

Variation should be meaningful, not cosmetic.

Two posts with different wording but the same reader job, evidence cluster, and conclusion are probably duplicates.

## Content Pillars

Use a small number of coherent pillars.

A pillar should represent a meaningful recurring theme, not a vague category.

Good:

- athlete ownership;
- developmental environment;
- perseverance;
- dropout cognition;
- coaching practice.

Weak:

- thoughts;
- ideas;
- motivation;
- miscellaneous research.

Avoid creating one pillar per post.

Avoid making pillars so broad that every post fits all of them.

## Claim Allocation

Allocate evidence deliberately.

Do not reuse the same central grounded claim across multiple posts unless:

- the reader job is materially different;
- the post answers a different audience problem;
- the conclusion is different;
- reuse is explicitly intentional.

Track:

- `primary_claim_ids`;
- `secondary_claim_ids`.

A primary claim should not be primary in many posts by default.

Secondary reuse is acceptable when necessary for context.

## Insight Allocation

Each post should have one primary insight or one tightly integrated insight cluster.

Avoid:

- stuffing all insights into the first post;
- splitting one small insight into many near-duplicate posts;
- assigning unrelated insights to one post simply to create variety.

When several insights depend on one prerequisite concept, create that prerequisite post first.

## Dependency Rule

Sequence posts according to conceptual dependency.

Examples:

- define the construct before debating its implications;
- establish the finding before discussing application;
- introduce the environmental perspective before presenting a multi-factor synthesis;
- explain a distinction before using it in a later decision framework.

Do not sequence only for rhetorical drama.

## Series Arc

A series does not need a rigid narrative arc, but the sequence should make sense.

Possible arc patterns include:

```text
setup → evidence → application → synthesis
```

```text
challenge → teach → evidence → conversation
```

```text
evidence → teach → application → synthesis
```

Do not force every series into the same pattern.

Continuity should be subtle unless numbered parts genuinely help the reader.

Avoid unnecessary:

- `Part 1`;
- `Part 2`;
- `Part 3`;

when each post can stand independently.

## Distinctiveness Test

Before approving the plan, compare every pair of posts for overlap.

Check:

- primary claim;
- supporting claim cluster;
- primary insight;
- reader job;
- opening mechanism;
- core distinction;
- example/story;
- main consequence;
- conclusion;
- CTA type;
- proposed format.

Flag posts when several of these overlap materially.

Use:

- `distinct`
- `partial_overlap`
- `substantial_overlap`

`substantial_overlap` must be resolved before mass drafting.

## Opening-Mechanism Planning

At planning stage, describe the opening mechanism, not the exact final hook.

Examples:

- direct observation;
- evidence-led statement;
- misconception;
- practical question;
- contrast;
- short scenario from supplied material;
- data point;
- conceptual tension.

Do not write polished final hooks unless explicitly asked.

Avoid assigning the same opening mechanism to consecutive posts by default.

## Ending / CTA Planning

Plan the **function** of the ending, not exact CTA wording.

Possible ending functions:

- concise takeaway;
- reflective question;
- practical next step;
- unresolved tension;
- synthesis;
- no CTA.

Do not force engagement prompts.

Do not make every post end with:

`What do you think?`

A strong post may have no CTA.

## Format Planning

Recommend format only when it serves the post.

Possible formats:

- text post;
- document/carousel;
- figure/chart-led post;
- image + text;
- article/newsletter;
- short list;
- narrative post.

Do not claim that one format will receive more reach unless current evidence is explicitly supplied/verified.

Format diversity is useful only when it fits the content.

## Series-Level Repetition Rules

Flag repeated:

- `We often talk about X as if...`;
- `The question is not X. It is Y.`;
- `This matters because...`;
- three-item list structures;
- identical opening questions;
- identical evidence-to-application movement;
- generic coaching reflection endings;
- identical CTA style.

Do not prohibit a pattern after one use.

The problem is repeated structure that makes multiple posts interchangeable.

## Audience Rule

All posts in a series may share the same audience, but their reader problems should still differ.

For each post identify:

- intended audience;
- audience problem/question;
- reader job;
- reason this post deserves to exist separately.

If a post cannot answer that last question clearly, reconsider it.

## Evidence vs Opinion Rule

Label planned content accurately.

Use:

- `evidence_grounded`
- `evidence_informed_interpretation`
- `author_opinion`
- `application_question`
- `story`

Do not disguise interpretation as evidence.

Do not turn an application question into an empirical conclusion.

## Research Safety Rule

Series planning must preserve upstream evidence constraints.

Do not:

- strengthen relationship language;
- turn association into causation;
- broaden populations;
- invent mechanisms;
- invent limitations;
- invent practical effects;
- turn a research question into a finding;
- turn an interpretation into a fact.

The architect plans content structure; it does not rewrite evidence.

## Missing Author Input

Mark missing personal material explicitly.

Examples:

```yaml
author_input_required: true
author_input_needed:
  - "A genuine coaching example illustrating this distinction."
```

Do not fabricate:

- personal experiences;
- athlete stories;
- club examples;
- conversations;
- failures;
- successes;
- emotions;
- achievements.

## Number of Posts

Do not maximize post count.

Prefer the smallest number of posts that gives each major idea a distinct job.

If five grounded insights can be communicated clearly in three posts, do not create seven posts merely to fill a calendar.

If the user requests a fixed number, obey it where possible but flag when the evidence does not support that many distinct posts.

## Cadence

Series architecture may record user cadence constraints, but exact scheduling belongs to `linkedin-calendar-planner`.

If cadence is unspecified:

- do not invent an algorithmic best frequency;
- leave cadence unresolved or suggest a sustainable range only if the user asks.

## Output Location

Default plan:

`.knowledgecraft/content/ideas/linkedin-series-plan.yaml`

Optional readable companion:

`.knowledgecraft/content/ideas/linkedin-series-plan.md`

Do not write generated plans into `.opencode/skills/`.

## Output Contract

Use this structure:

```yaml
linkedin_series_plan:
  series_id: "LIS-001"
  title: null
  objective: ""
  audience: ""
  series_status: "planned|needs_input|blocked"
  source_ids: []
  insight_ids: []
  claim_ids: []
  pillars:
    - pillar_id: "PILLAR-01"
      name: ""
      purpose: ""
  posts:
    - post_id: "POST-001"
      sequence: 1
      working_title: ""
      drafting_status: "ready|needs_input|blocked"
      pillar_ids: []
      audience: ""
      audience_problem_or_question: ""
      reader_job: "setup|teach|challenge|evidence|application|synthesis|conversation|story"
      evidence_mode: "evidence_grounded|evidence_informed_interpretation|author_opinion|application_question|story"
      primary_insight_ids: []
      supporting_insight_ids: []
      primary_claim_ids: []
      secondary_claim_ids: []
      source_ids: []
      main_point: ""
      why_separate_post: ""
      prerequisite_post_ids: []
      opening_mechanism: ""
      ending_function: ""
      recommended_format: ""
      author_input_required: false
      author_input_needed: []
      drafting_constraints: []
  overlap_review:
    - post_ids:
        - "POST-001"
        - "POST-002"
      overlap_level: "distinct|partial_overlap|substantial_overlap"
      overlap_dimensions: []
      action: "none|revise|merge|drop"
      note: ""
  series_checks:
    substantial_overlap_remaining: false
    prerequisite_order_valid: true
    every_post_has_distinct_reader_job_or_reason: true
    evidence_traceability_complete: true
    unsupported_story_material_required: false
  handoff:
    ready_for_drafting: true
    next_skill: "linkedin-post-drafter"
    notes: []
```

## Drafting Constraints

Use `drafting_constraints` to preserve important planning boundaries.

Examples:

```yaml
drafting_constraints:
  - "Do not claim causality."
  - "Keep the empirical finding separate from the coaching implication."
  - "Do not invent a personal coaching example."
  - "Do not reuse the opening pattern from POST-002."
```

These constraints should come from the actual evidence/series design.

Do not create restrictions merely to make the plan look detailed.

## Handoff Rule

Set `drafting_status` per post:

- `ready` -> safe to hand to `linkedin-post-drafter`;
- `needs_input` -> concept is viable but required author material or evidence is missing;
- `blocked` -> the brief should not proceed as currently framed.

A plan is `ready_for_drafting: true` when at least one post is `ready` and every ready post satisfies the handoff rules below.

For every `ready` post:

- reader job is clear;
- evidence-bearing content has source + claim + insight traceability;
- no substantial overlap remains with another ready post;
- prerequisites exist and occur earlier;
- no required author input is missing;
- the post has a clear reason to exist separately.

If some posts need author input:

- set those posts to `drafting_status: needs_input`;
- set `author_input_required: true`;
- state exactly what input is needed;
- keep unaffected valid briefs `ready` when appropriate;
- set series status `needs_input` when unresolved input remains in the planned series.

Do not silently draft around missing inputs.

## Minimal Planning Rule

Do not over-design the series.

The architect should create enough structure to prevent duplication and evidence drift, but not prescribe every sentence before drafting.

Good series planning leaves room for `linkedin-post-drafter` and voice editing.

## Deterministic Validation

After writing the structured series-plan YAML, validate its mechanical consistency before reporting the plan complete.

Run:

```powershell
py ".opencode/skills/linkedin-series-architect/scripts/validate_linkedin_series_plan.py" ".knowledgecraft/content/ideas/linkedin-series-plan.yaml"
```

If validation returns `FAIL`:

1. do not report the series plan as complete;
2. read every validation error;
3. repair only the affected YAML, traceability, status, overlap, sequence, or prerequisite fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- valid YAML and required top-level structure;
- unique post IDs;
- unique positive sequence numbers;
- allowed reader jobs, evidence modes, and drafting statuses;
- per-post source/claim/insight references are listed in the plan-level registries;
- ready evidence-bearing posts have at least one source ID, one claim ID, and one insight ID;
- ready posts do not still require author input;
- `needs_input` posts identify what author input is needed;
- story briefs with missing genuine story material cannot be `ready`;
- prerequisite post IDs exist;
- prerequisites occur earlier in the sequence;
- substantial overlap cannot remain between two ready posts;
- `series_checks.substantial_overlap_remaining` agrees with ready-post overlap state;
- `series_checks.prerequisite_order_valid` agrees with the actual prerequisite order;
- `series_checks.evidence_traceability_complete` agrees with ready evidence-bearing posts;
- handoff `ready_for_drafting` agrees with whether at least one valid ready post exists;
- a ready handoff points to `linkedin-post-drafter`.

The validator does **not** decide whether two posts are semantically too similar, whether an insight genuinely supports a claim, whether a reader job is strategically correct, or whether the series is interesting. Those remain model/reviewer responsibilities.

## Final Review Sequence

1. load grounded insights/claims;
2. identify audience and series objective;
3. cluster ideas into a small number of pillars;
4. assign one primary reader job per candidate post;
5. allocate primary and secondary evidence;
6. identify conceptual dependencies;
7. order posts;
8. assign opening mechanisms and ending functions;
9. check format fit at planning level;
10. run pairwise overlap review;
11. merge/drop/reframe substantial duplicates;
12. mark missing author input;
13. verify traceability;
14. produce handoff-ready briefs.

## Final Checks

Before completing the series plan, verify:

- series objective clear? YES
- audience identified? YES
- pillars coherent and limited? YES
- each post has one primary reader job? YES
- each post has a separate reason to exist? YES
- evidence-bearing posts trace to existing source/claim/insight IDs? YES
- no invented IDs? YES
- primary claims not unnecessarily reused across posts? YES
- prerequisite order valid? YES
- substantial overlap resolved? YES
- opening mechanisms not mechanically repeated? YES
- ending functions not mechanically repeated? YES
- no unsupported story/personal material invented? YES
- evidence vs interpretation/opinion labeled correctly? YES
- no causal or relationship strengthening introduced? YES
- no platform folklore treated as fact? YES
- exact scheduling left to calendar planner unless explicitly requested? YES
- plan detailed enough for drafting but not over-scripted? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- generated artifacts saved outside `.opencode/skills/`? YES
