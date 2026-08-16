# KnowledgeCraft Workflows

This document describes practical ways to use the KnowledgeCraft skill collection without requiring users to understand every skill first.

The pipeline should always inspect existing state before running unnecessary stages.

## 1. Academic source → grounded knowledge

Use when the goal is to convert a paper or source into a reliable research artifact.

```text
research-library
→ research-source-grounder
```

Optional next stage:

```text
→ research-insight-miner
```

Typical outputs:

```text
.knowledgecraft/research/grounded/<source-id>-source-card.md
.knowledgecraft/research/grounded/<source-id>-claim-ledger.yaml
.knowledgecraft/research/insights/<source-id>-insights.yaml
```

Key guarantees:

- source identity is stable;
- claims are traceable;
- null results remain null;
- causal language is not strengthened;
- limitations remain attached.

## 2. Multiple sources → research knowledge base

Use when several papers/documents must be processed consistently.

```text
research-library
→ research-batch
→ research-source-grounder
→ research-insight-miner
```

The batch orchestrator should be used for research-stage batching, not LinkedIn drafting.

Use analysis-specific artifacts rather than a universal summary when source differences matter.

## 3. Grounded research → LinkedIn series

Use when the source is already grounded and insights exist.

```text
research-insight-miner
→ linkedin-series-architect
```

If insights are already valid:

```text
linkedin-series-architect
```

The architect creates:

- series role;
- reader jobs;
- claim allocation;
- insight allocation;
- dependencies;
- overlap assessment;
- one drafting brief per post.

Do not draft the entire series before architecture is valid.

## 4. Series brief → LinkedIn draft

```text
linkedin-post-drafter
```

One ready brief should produce one draft artifact.

The drafter must preserve:

- allowed claim IDs;
- allowed insight IDs;
- causal constraints;
- null findings;
- descriptive relationships;
- missing author-input state.

If a story brief lacks genuine personal material:

```text
needs_input
```

Do not fabricate an anecdote.

## 5. Draft → author-aligned post

If a validated author profile already exists:

```text
author-voice-editor
```

If genuine writing samples exist but there is no profile:

```text
author-voice-profiler
→ author-voice-editor
```

If no genuine samples exist:

- do not fabricate a profile;
- either skip author-specific voice editing;
- or request writing samples when voice matching is important.

## 6. Draft → cleaner natural prose

Use:

```text
text-naturalness-editor
```

when the prose is mechanically repetitive, generic, or unnecessarily stiff.

This is a conservative meaning-preserving edit.

`text-humanizer` is separate.

Use it only when explicitly requested or when its protected-span workflow is specifically appropriate.

It is not part of the automatic default pipeline.

## 7. Draft → publication-ready LinkedIn post

Recommended order:

```text
linkedin-platform-review
→ factuality-guard
→ content-quality-gate
```

Why this order?

Platform review can alter presentation, so factuality should assess the final presented wording rather than an older draft.

Approval requires:

```text
factuality PASS
+
content-quality-gate APPROVE
=
qa_approved
```

Platform review PASS alone is not approval.

## 8. Quality REVISE → local repair

Do not restart the entire workflow.

Route to the smallest relevant owner.

Examples:

### Voice issue

```text
content-quality-gate
→ author-voice-editor
→ factuality-guard
→ content-quality-gate
```

### Naturalness issue

```text
content-quality-gate
→ text-naturalness-editor
→ factuality-guard
→ content-quality-gate
```

### Platform presentation issue

```text
linkedin-platform-review
→ repair
→ factuality-guard
→ content-quality-gate
```

### Unsupported claim

```text
factuality-guard
→ linkedin-post-drafter
```

or, if the problem comes from upstream interpretation:

```text
research-insight-miner
```

After a material text revision, stale QA must not be reused.

## 9. QA-approved posts → publishing calendar

```text
linkedin-calendar-planner
```

Only:

```text
qa_approved
```

posts may become:

```text
scheduled
```

The planner handles:

- cadence;
- fixed dates;
- blackout dates;
- dependencies;
- time-sensitive windows;
- existing locked commitments;
- hard collisions;
- unresolved scheduling decisions.

It should not invent exact "best times."

If the user says:

```text
Thursday morning
```

the planner should preserve a broad window rather than silently creating `09:00`.

## 10. Calendar with blocked items

A correct calendar can contain mixed states:

```text
scheduled
provisional
needs_decision
blocked_by_dependency
expired
```

Planner correctness is not identical to every-item readiness.

For example:

```text
POST-1 scheduled
POST-2 needs_decision
```

can still be a valid completed planning artifact.

A true hard collision should remain visible until resolved.

## 11. Scheduled → published

KnowledgeCraft does not infer publication.

Normal workflow:

```text
scheduled
→ human / authorized publisher
→ published
```

Do not mark a post published simply because its scheduled date has passed.

Publication must be confirmed.

## 12. Published posts → performance learning

```text
linkedin-performance-review
```

Use actual supplied metrics.

The skill:

- preserves raw values;
- distinguishes zero from missing;
- states denominators explicitly;
- calculates valid rates;
- considers observation windows;
- considers exposure;
- keeps paid/organic context visible;
- retains outliers;
- avoids causal and algorithmic claims.

Learning classes:

```text
strong_observation
tentative_pattern
test_next
insufficient_data
```

Qualified learnings may feed back into:

```text
linkedin-series-architect
```

without becoming permanent platform rules.

## 13. Full research → LinkedIn pipeline

For a new evidence-based multi-post project:

```text
research-library
→ research-source-grounder
→ research-insight-miner
→ linkedin-series-architect
→ linkedin-post-drafter
→ author-voice-editor          [when applicable]
→ text-naturalness-editor      [when needed]
→ linkedin-platform-review
→ factuality-guard
→ content-quality-gate
→ linkedin-calendar-planner    [when scheduling requested]
```

`linkedin-content-pipeline` orchestrates this flow.

It should not perform specialist logic itself.

## 14. Resume an existing workflow

The pipeline should start from the latest valid stage.

Examples:

### Already grounded

```text
grounded
→ research-insight-miner
```

### Insights already valid

```text
ideas_created
→ linkedin-series-architect
```

### Series plan already valid

```text
series_planned
→ linkedin-post-drafter
```

### Draft already valid

Continue at the next required editing/review stage.

### QA already valid + calendar requested

```text
qa_approved
→ linkedin-calendar-planner
```

Do not rerun research merely because the pipeline is invoked again.

## 15. Source revision

If `research-library` detects a materially changed source:

```text
source revision
→ invalidate affected grounding
→ invalidate affected insights
→ invalidate affected content
→ invalidate affected QA
```

Resume from the earliest invalid stage.

Do not restart unrelated items.

## 16. Failure isolation

Suppose a three-post series has:

```text
POST-1 ready
POST-2 needs personal story input
POST-3 draft validator FAIL
```

Correct behavior:

```text
POST-1 → continue
POST-2 → needs_input
POST-3 → repair at linkedin-post-drafter
```

Do not block POST-1 simply because POST-2 and POST-3 have issues.

## 17. End-to-end integration test

KnowledgeCraft has been tested through a synthetic evidence-to-LinkedIn workflow that produced:

```text
1 source
→ deterministic source registration
→ grounding
→ insights
→ author voice profile
→ 3-post series
→ 3 drafts
→ voice edits
→ naturalness edits
→ platform reviews
→ factuality PASS
→ content-quality APPROVE
→ 3 qa_approved posts
→ 3 scheduled posts
```

No post was marked published.

The human publication boundary remained intact.

This integration pattern should be reused when validating future major changes to the LinkedIn subsystem.
