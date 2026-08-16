---
name: linkedin-calendar-planner
description: Place QA-approved LinkedIn posts into a coherent publishing calendar while preserving user dates, dependencies, thematic spacing, reader-job and format variety, time sensitivity, explicit experiments, and uncertainty around unsupported posting-time claims.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "calendar"
  opencode/slash: "false"
---

# LinkedIn Calendar Planner

Place **approved LinkedIn posts** into a coherent publishing calendar.

The job is sequencing and scheduling, not drafting or optimizing content.

## Responsibility Boundary

`linkedin-calendar-planner` owns:

- calendar sequencing;
- date assignment;
- time-window assignment when justified;
- cadence implementation;
- dependency ordering;
- theme spacing;
- reader-job spacing;
- format spacing;
- time-sensitive prioritization;
- experiment labeling;
- collision detection;
- schedule-level rationale;
- safe handoff from `qa_approved` to `scheduled`.

It does **not**:

- draft or rewrite posts;
- edit hooks, CTAs, hashtags, mentions, or links;
- change evidence;
- decide factuality;
- perform quality review;
- invent "best" posting times;
- claim knowledge of LinkedIn's current ranking system without verification;
- publish posts;
- mark unapproved drafts as scheduled.

Related skills:

- `linkedin-series-architect` -> defines conceptual sequence;
- `linkedin-platform-review` -> reviews LinkedIn presentation;
- `factuality-guard` -> verifies claims;
- `content-quality-gate` -> determines whether content is approved;
- `linkedin-performance-review` -> evaluates later results;
- `linkedin-content-pipeline` -> orchestrates lifecycle transitions.

## Eligibility Rule

Schedule only posts that are explicitly approved.

Preferred upstream state:

`qa_approved`

Do not schedule:

- `drafted`;
- `needs_input`;
- `blocked`;
- `revise`;
- `factuality_blocked`;
- any post whose approval status is unclear.

If the user explicitly asks to place unapproved drafts into a **provisional planning calendar**, mark them:

`calendar_status: provisional`

and do not mark them `scheduled`.

## Lifecycle Rule

Normal lifecycle:

```text
qa_approved
    ↓
linkedin-calendar-planner
    ↓
scheduled
```

The planner may recommend dates, but it must not falsely advance lifecycle state.

A post becomes `scheduled` only when:

- it is approved;
- a publication date or explicit schedule slot exists;
- required dependencies are satisfied;
- no unresolved scheduling blocker remains.

## User Constraints Take Priority

Obey explicit user constraints first.

Examples:

- fixed publication date;
- no weekend posting;
- two posts per week;
- campaign start/end dates;
- event deadline;
- launch date;
- vacation period;
- blackout dates;
- required sequence;
- minimum spacing.

Do not override explicit constraints with generic platform advice.

If user constraints conflict:

1. identify the conflict;
2. preserve the highest-priority explicit constraint where possible;
3. mark the affected item `needs_decision`;
4. do not silently choose.

## Cadence Rule

If the user supplies a cadence, use it.

Examples:

- Monday and Thursday;
- three posts per week;
- every five days;
- weekly;
- two posts before an event.

If no cadence is supplied:

- do not invent a "best frequency";
- leave cadence unresolved; or
- propose a sustainable range only when the user asks for a recommendation.

Never claim:

- daily is best;
- three times per week is optimal;
- consistency at a specific frequency is algorithmically rewarded;

unless verified current evidence is explicitly available and relevant.

## Exact Time Rule

Do not invent exact posting times.

Use exact clock times only when:

- the user supplied them;
- an external event requires them;
- a verified experiment requires them;
- current verified platform/audience evidence supports them and the user wants that optimization.

Otherwise use:

- broad window;
- `TBD`;
- `not_specified`.

Examples:

```yaml
time_mode: "window"
time_window: "morning"
```

or:

```yaml
time_mode: "TBD"
time_window: null
```

Do not turn "morning" into `09:00` unless the user asked for a concrete time.

## Time Zone Rule

If exact dates/times matter, record the timezone.

Do not silently assume UTC.

Preferred field:

```yaml
timezone: "Europe/Helsinki"
```

If timezone is unknown and materially affects the schedule, mark:

`timezone_required: true`

Do not invent one.

## Dependency Rule

Preserve conceptual dependencies supplied by the series plan.

If:

`POST-004` depends on `POST-002` and `POST-003`

then schedule `POST-004` after both.

Do not violate dependencies merely to create theme variety.

If a prerequisite cannot be scheduled in time:

- mark the dependent post `blocked_by_dependency`;
- explain which prerequisite is missing.

## Theme Spacing

Avoid placing near-identical themes consecutively when alternatives exist.

Consider:

- content pillar;
- main topic;
- claim cluster;
- reader problem;
- series role.

Do not spread posts so far apart that a dependent series loses coherence.

Spacing is a balance between:

- avoiding repetition;
- maintaining continuity.

## Reader-Job Spacing

Avoid unnecessary consecutive posts with identical reader jobs.

Examples:

- evidence -> evidence -> evidence;
- application -> application -> application.

This is not a hard prohibition.

Consecutive identical jobs are acceptable when:

- the campaign requires them;
- the posts are time-sensitive;
- the content is genuinely distinct;
- the user explicitly requests it.

Record intentional repetition.

## Format Spacing

Avoid mechanical repetition of the same format when variation would help and alternatives already exist.

Do not change a post's approved format merely to create diversity.

A text post remains a text post unless another skill/user revises it.

The planner sequences formats; it does not redesign them.

## Time-Sensitive Content

Prioritize genuinely time-sensitive content.

Examples:

- event-linked post;
- publication announcement;
- conference;
- deadline;
- launch;
- seasonal issue;
- response to a dated report.

Record:

- `time_sensitivity`;
- `not_before`;
- `not_after`;
- reason.

Do not label evergreen content urgent for engagement purposes.

If a time-sensitive window has passed, do not schedule it as though still current.

Mark it:

`expired`

or request a revised framing upstream.

## Evergreen Content

Evergreen content can be moved more freely to solve:

- theme collisions;
- dependency gaps;
- cadence constraints;
- campaign congestion.

Do not falsely add urgency to evergreen material.

## Planner Success vs Calendar Readiness

Do not confuse **safe planner behavior** with `ready_to_schedule: true`.

A planning run can be correct even when the resulting calendar is not ready to schedule.

Examples of correct outcomes:

- a dependent post is `blocked_by_dependency`;
- an exact-time request is `needs_decision` because timezone is missing;
- two locked posts create an unresolved hard collision;
- a time-sensitive post is marked `expired`.

These are not planner failures when the constraint is detected, surfaced, and handled safely.

`ready_to_schedule` describes the operational state of the produced calendar.

It does **not** describe whether the planner followed its rules correctly.

A semantic regression should therefore PASS a case when the planner correctly withholds scheduling because a blocker exists.

## Constraint-Respect Semantics

Calendar-check booleans should describe whether the planner **respected the rule**, not whether every requested item was successfully scheduled.

### Dependencies

Set:

`dependencies_respected: true`

when no scheduled post violates prerequisite order.

A post correctly marked `blocked_by_dependency` because its prerequisite cannot yet be scheduled is evidence that the dependency rule **was respected**.

Do not set `dependencies_respected: false` merely because an unresolved dependency exists.

### Exact-Time Safety

Set:

`exact_time_requirements_respected: true`

when every scheduled exact time is supported by the available information.

This remains `true` when an exact-time request is withheld because timezone or another required input is missing.

The unsafe condition is scheduling unsupported precision.

### Scheduling Decisions

Use:

`unresolved_decisions_remaining: true`

when one or more entries require user input before they can be assigned a valid slot.

Examples:

- timezone missing for an exact-time request;
- two locked commitments require user choice;
- no scheduling horizon exists for placing a cadence-constrained post;
- explicit user constraints conflict.

An unresolved decision is not automatically a hard collision.

## Conflict vs Collision

Distinguish an unresolved **decision** from an actual **slot/constraint collision**.

### Decision blocker

Examples:

- exact time requested but timezone missing;
- user gave two alternative dates but no preference;
- cadence supplied but no usable scheduling horizon exists.

These should normally use:

`calendar_status: needs_decision`

without creating a `hard` collision unless two actual constraints occupy incompatible states.

### Hard collision

Use `hard` only when two or more concrete constraints cannot simultaneously be satisfied.

Examples:

- two locked posts on the same date when `maximum_posts_per_day: 1`;
- a fixed date falls on a user blackout date and neither may move;
- a dependent post is itself locked before an immovable prerequisite.

Do not call a merely unscheduled post a hard collision.

## Collision Detection

Check for schedule collisions such as:

- two posts assigned to the same slot when only one is allowed;
- mutually exclusive campaign priorities;
- dependent post scheduled before prerequisite;
- post outside allowed date range;
- post on blackout date;
- time-sensitive post after deadline;
- identical themes stacked despite available alternatives.

Classify collisions:

- `none`;
- `soft`;
- `hard`.

### `soft`

Suboptimal but publishable.

Example:

two consecutive posts have the same reader job.

### `hard`

Schedule is invalid or violates an explicit constraint.

Example:

dependent post before prerequisite.

Hard collisions must be resolved before `scheduled`.

## Experiments

Mark experiments explicitly.

Possible experiment dimensions:

- opening style;
- post format;
- CTA vs no CTA;
- topic framing;
- posting window;
- content length;
- evidence-led vs application-led framing.

Calendar planner does not design the content treatment itself.

It may assign already-approved variants to slots.

Prefer one major variable at a time where possible.

Do not call ordinary scheduling variation an experiment unless:

- comparison is intentional;
- variable is stated;
- observation window is defined;
- success metric is stated or deferred to performance review.

## Experiment Causality Guard

Scheduling an experiment does not make it causal research.

Do not claim:

- this time caused better reach;
- this format caused more saves;
- this CTA produced more leads;

from simple post-to-post comparisons.

`linkedin-performance-review` handles cautious interpretation later.

## Platform Folklore Guard

Do not encode unsupported rules such as:

- Tuesday at 9 a.m. is best;
- weekends are bad;
- mornings outperform afternoons;
- posting every day is rewarded;
- a specific gap between posts boosts reach.

If a scheduling recommendation materially relies on a current platform claim:

- verify it when verification tools are available; or
- mark `needs_current_verification`; or
- schedule without relying on the claim.

## Current-Fact Boundary

Stable scheduling judgment:

- dependency order;
- user blackout dates;
- theme repetition;
- campaign deadline;
- approved/unapproved state;
- spacing based on supplied series structure.

Time-sensitive external/platform fact:

- current LinkedIn recommendation;
- current event date not supplied;
- current audience activity pattern from analytics;
- current platform feature constraints.

Do not guess time-sensitive facts.

## Existing Calendar Rule

If an existing calendar is supplied:

- preserve existing confirmed commitments;
- do not overwrite dates silently;
- identify conflicts;
- insert around locked items where possible.

Use:

```yaml
slot_lock: "locked|flexible"
```

Locked items move only with explicit user permission.

## Publication Window

A slot may use:

### Exact

```yaml
date: "2026-09-10"
time_mode: "exact"
time: "09:30"
```

Use only when justified.

### Window

```yaml
date: "2026-09-10"
time_mode: "window"
time_window: "morning"
```

### Date only

```yaml
date: "2026-09-10"
time_mode: "TBD"
```

### Unscheduled

```yaml
date: null
time_mode: "TBD"
```

Do not fake precision.

## Calendar Status

Per item use:

- `scheduled`
- `provisional`
- `needs_decision`
- `blocked_by_dependency`
- `expired`

### `scheduled`

Approved and assigned a valid publication slot.

### `provisional`

Placed for planning, but not publication-ready or not confirmed.

### `needs_decision`

User input is required to resolve a scheduling choice/conflict.

### `blocked_by_dependency`

Cannot be scheduled because a prerequisite is unresolved.

### `expired`

A time-sensitive opportunity has passed.

## Approval Preservation

Record the upstream approval state.

Example:

```yaml
approval_status: "qa_approved"
```

Do not change it.

If a post is not approved, it cannot become `scheduled`.

## Do Not Modify Content

The planner must not rewrite:

- working title;
- post text;
- hook;
- CTA;
- evidence;
- hashtags;
- links;
- source IDs.

It may reference content metadata for sequencing.

If content must change to fit a date/event, route upstream.

## Output Location

Default:

`.knowledgecraft/content/calendar/linkedin-calendar.yaml`

Do not write generated calendar artifacts into `.opencode/skills/`.

## Output Contract

Use:

```yaml
linkedin_calendar:
  calendar_id: "LICAL-001"
  timezone: null
  timezone_required: false
  cadence:
    source: "user|proposed|unspecified"
    description: ""
  date_range:
    start: null
    end: null
  constraints:
    fixed_dates: []
    blackout_dates: []
    allowed_days: []
    minimum_spacing_days: null
    maximum_posts_per_day: 1
  entries:
    - calendar_entry_id: "CAL-001"
      post_id: "POST-001"
      approval_status: "qa_approved"
      calendar_status: "scheduled|provisional|needs_decision|blocked_by_dependency|expired"
      slot_lock: "locked|flexible"
      date: null
      time_mode: "exact|window|TBD"
      time: null
      time_window: null
      pillar_ids: []
      reader_job: ""
      format: ""
      prerequisite_post_ids: []
      time_sensitivity: "evergreen|time_sensitive"
      not_before: null
      not_after: null
      time_sensitivity_reason: null
      experiment_id: null
      scheduling_rationale: ""
      conflicts: []
  experiments:
    - experiment_id: "EXP-001"
      hypothesis: ""
      variable: ""
      variants: []
      success_metric: null
      interpretation_guard: "Observational comparison; do not infer causality from post-to-post differences."
  collision_review:
    - collision_id: "COL-001"
      entry_ids: []
      collision_level: "none|soft|hard"
      collision_type: ""
      explanation: ""
      action: "none|resolved|needs_decision"
  calendar_checks:
    only_approved_posts_scheduled: true
    dependencies_respected: true
    hard_collisions_remaining: false
    unresolved_decisions_remaining: false
    explicit_user_dates_preserved: true
    blackout_dates_respected: true
    time_sensitive_windows_respected: true
    exact_time_requirements_respected: true
    unsupported_platform_timing_claims_used: false
  handoff:
    ready_to_schedule: true
    lifecycle_transition: "qa_approved -> scheduled"
    notes: []
```

## Calendar-Level Readiness

Set:

`ready_to_schedule: true`

only when:

- at least one entry is validly `scheduled`;
- every scheduled entry is approved;
- no scheduled entry violates a dependency;
- no unresolved hard collision invalidates a scheduled slot;
- explicit user dates are preserved;
- blackout dates are respected;
- time-sensitive windows are respected;
- every scheduled exact time is user-supplied or otherwise justified;
- no unresolved material platform-timing claim is required.

A calendar may contain `provisional`, `needs_decision`, `blocked_by_dependency`, or `expired` entries and still be ready for its **other valid scheduled entries**.

Set `ready_to_schedule: false` when no valid scheduled entry exists, or when a hard collision invalidates the schedule that would otherwise be handed off.

Do not set `ready_to_schedule: false` merely because one unrelated provisional/blocked item remains when other scheduled entries are valid.

Always describe unresolved entries in handoff notes.

## Deterministic Validation

After writing the structured calendar YAML, validate its mechanical consistency before reporting completion.

Run:

```powershell
py ".opencode/skills/linkedin-calendar-planner/scripts/validate_linkedin_calendar.py" ".knowledgecraft/content/calendar/linkedin-calendar.yaml"
```

If validation returns `FAIL`:

1. do not report the calendar as complete;
2. read every validation error;
3. repair only the affected YAML, status, date/time, prerequisite, collision, experiment, check, or handoff fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- valid YAML and required top-level structure;
- unique calendar-entry IDs and post IDs;
- allowed calendar status, slot-lock, time-mode, collision, and cadence values;
- scheduled entries are `qa_approved`;
- scheduled entries have a date;
- exact scheduled times have an explicit time and a known timezone;
- broad windows are not encoded as exact times;
- `TBD` does not silently contain an exact time;
- blackout dates are not used by scheduled entries;
- scheduled time-sensitive posts remain inside `not_before` / `not_after`;
- expired entries are not treated as scheduled;
- prerequisite post IDs exist;
- scheduled dependent posts do not precede or bypass unscheduled prerequisites;
- per-day scheduled counts do not exceed `maximum_posts_per_day`;
- experiment IDs are unique and referenced experiments exist;
- experiment records include variable, variants, and an interpretation guard;
- hard-collision and unresolved-decision booleans agree with structured entries/collision review;
- approval, dependency, blackout, time-window, and exact-time safety checks agree with the calendar data;
- `ready_to_schedule: true` is never allowed when the calendar is mechanically unsafe;
- ready handoff uses lifecycle transition `qa_approved -> scheduled`.

The validator intentionally allows `ready_to_schedule: false` for a mechanically safe calendar when the planner conservatively withholds handoff because of a broader unresolved dependency or user decision. It validates **unsafe readiness**, not strategic willingness to schedule.

The validator does **not** determine whether:

- theme spacing is strategically optimal;
- reader-job spacing is ideal;
- an unresolved decision should be considered important enough to withhold the whole calendar;
- a post is substantively time-sensitive;
- an experiment is causally informative;
- a user-supplied time is actually a good time to post;
- LinkedIn algorithm folklore has been introduced in free-text rationale.

Those remain semantic/reviewer responsibilities.

## Minimal Scheduling Rule

Do not fill empty calendar space for the sake of completeness.

If only three approved posts exist:

- schedule three posts;
- do not invent additional content;
- do not pull blocked drafts into the calendar.

## Schedule Rationale

For every scheduled/provisional entry, give a concise rationale based on actual constraints.

Good:

- `Scheduled after POST-001 because this post depends on its construct explanation.`
- `Placed between two environment-focused posts to reduce thematic repetition.`
- `Scheduled before the event deadline supplied by the user.`

Weak:

- `Best time for engagement.`
- `The algorithm prefers this day.`
- `This should perform well.`

## Review Procedure

1. load approved posts and relevant series metadata;
2. verify approval status;
3. load user cadence/date constraints;
4. identify timezone needs;
5. identify dependencies;
6. identify time-sensitive windows;
7. identify locked existing commitments;
8. assign fixed constraints first;
9. place prerequisite posts before dependents;
10. distribute themes/reader jobs/formats where possible;
11. label experiments explicitly;
12. avoid unsupported exact-time optimization;
13. run collision review;
14. resolve hard collisions or mark needs decision;
15. verify lifecycle eligibility;
16. produce calendar handoff.

## Final Checks

Before completing the calendar, verify:

- only approved posts marked scheduled? YES
- unapproved items only provisional/blocked? YES
- explicit user dates obeyed? YES
- blackout dates respected? YES
- timezone recorded when material? YES
- no exact time invented? YES
- cadence user-supplied or clearly labeled proposed/unspecified? YES
- prerequisite order valid for every scheduled post? YES
- blocked dependency treated as rule-respecting rather than rule-violating? YES
- missing timezone/exact-time input treated as needs_decision rather than unsupported scheduling? YES
- unresolved decision distinguished from actual hard collision? YES
- time-sensitive posts within valid window? YES
- evergreen content not given fake urgency? YES
- theme repetition reduced where possible? YES
- reader-job repetition reduced where possible? YES
- format diversity not forced by modifying content? YES
- existing locked calendar commitments preserved? YES
- experiments explicitly labeled? YES
- experiment variable clear? YES
- no causal interpretation of future performance implied? YES
- no unsupported "best day/time" claim? YES
- no LinkedIn algorithm folklore used? YES
- no post text/content modified? YES
- hard collisions resolved or marked needs_decision? YES
- lifecycle transition represented accurately? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- generated artifact saved outside `.opencode/skills/`? YES
