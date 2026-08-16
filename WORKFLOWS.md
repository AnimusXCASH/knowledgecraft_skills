# KnowledgeCraft Workflows

KnowledgeCraft supports three primary modes:

```text
1. Academic / Research
2. LinkedIn / Content
3. Combined Research → LinkedIn
```

For copy-paste usage, see:

```text
GETTING_STARTED.md
COMMANDS.md
```

---

# Input and Output Convention

Recommended research input folder:

```text
./papers/
```

Example:

```text
your-project/
├── papers/
│   └── my-paper.pdf
├── .opencode/skills/
└── .knowledgecraft/
```

Raw source:

```text
./papers/my-paper.pdf
```

Generated research state:

```text
.knowledgecraft/research/
```

A source may live elsewhere if the user supplies its path. The workflow should track the actual source path rather than requiring duplication inside `.knowledgecraft/`.

---

# Mode 1 — Academic / Research

Use this for:

- research knowledge bases;
- academic papers;
- PhD workflows;
- evidence synthesis;
- source-faithful claim extraction;
- research insights;
- applied-practice translation.

Core flow:

```text
./papers/my-paper.pdf
        ↓
research-library
        ↓
research-source-grounder
        ↓
research-insight-miner
        ↓
reusable research knowledge
```

## One source

```text
Process ./papers/my-paper.pdf for my research knowledge base.
```

Expected generated areas:

```text
.knowledgecraft/research/registry/
.knowledgecraft/research/extracted/
.knowledgecraft/research/grounded/
.knowledgecraft/research/insights/
```

Grounding must preserve:

- null findings;
- design terminology;
- relationship direction;
- uncertainty;
- limitations;
- causal strength.

## Multiple sources

```text
/research-batch

Process all new and unfinished research in ./papers through ideas_created.
```

Normal research-batch stopping point:

```text
ideas_created
```

unless the user explicitly requests downstream content creation.

---

# Mode 2 — LinkedIn / Content

Use this when grounded evidence or validated insights already exist.

```text
grounded claims / insights
        ↓
linkedin-series-architect
        ↓
linkedin-post-drafter
        ↓
author-voice-editor              [when applicable]
        ↓
text-naturalness-editor          [when useful]
        ↓
linkedin-platform-review
        ↓
factuality-guard
        ↓
content-quality-gate
        ↓
qa_approved
        ↓
linkedin-calendar-planner        [when scheduling requested]
```

`text-humanizer` is not an automatic pipeline stage.

## Series planning

`linkedin-series-architect` owns:

- multi-post decomposition;
- reader jobs;
- claim/insight allocation;
- dependencies;
- overlap control;
- drafting briefs.

## Drafting

`linkedin-post-drafter` converts one ready brief into one evidence-safe draft.

Missing personal story material should produce:

```text
needs_input
```

not a fabricated anecdote.

## Publication preparation

Recommended QA order:

```text
linkedin-platform-review
→ factuality-guard
→ content-quality-gate
```

Approval requires:

```text
factuality PASS
+
quality APPROVE
=
qa_approved
```

## Scheduling

Only `qa_approved` posts may become `scheduled`.

A calendar may contain:

```text
scheduled
provisional
needs_decision
blocked_by_dependency
expired
```

Do not invent exact "best posting times."

---

# Mode 3 — Combined Research → LinkedIn

Start with a source:

```text
./papers/my-paper.pdf
```

Then:

```text
research-library
→ research-source-grounder
→ research-insight-miner
→ linkedin-series-architect
→ linkedin-post-drafter
→ relevant voice/naturalness editing
→ linkedin-platform-review
→ factuality-guard
→ content-quality-gate
→ linkedin-calendar-planner        [optional]
```

Use `linkedin-content-pipeline` for outcome-first orchestration.

Example:

```text
/linkedin-content-pipeline

Process ./papers/my-paper.pdf into my research knowledge base and turn the validated insights into a three-post LinkedIn series.

Prepare all posts through final QA.
Do not publish.
```

---

# Automatic Routing vs Direct Skill Use

Use automatic routing when you specify an outcome:

```text
Process these papers for my research knowledge base.
```

```text
Turn this paper into a three-post LinkedIn series.
```

```text
Get POST-002 ready to publish.
```

Use a specialist directly when you know the exact stage:

```text
Use research-source-grounder on SRC-123.
```

```text
Run factuality-guard on POST-002.
```

```text
Run linkedin-calendar-planner on current qa_approved posts.
```

The orchestrator should inspect state first and run only the minimum missing stages.

---

# Resume Semantics

```text
new
→ research-library / extraction
```

```text
extracted
→ research-source-grounder
```

```text
grounded
→ research-insight-miner
```

```text
ideas_created
→ linkedin-series-architect
```

```text
series_planned
→ linkedin-post-drafter
```

```text
drafted
→ remaining editing/QA
```

```text
qa_approved
→ scheduling, if requested
```

Do not rerun valid upstream work unnecessarily.

---

# Revisions

A material source revision may invalidate affected:

```text
grounding
→ insights
→ series
→ drafts
→ QA
```

A material text revision after QA requires:

```text
factuality-guard
→ content-quality-gate
```

again.

Only affected items should be rerun.

---

# Publication Boundary

Normal boundary:

```text
scheduled
→ human / authorized publisher
→ published
```

A scheduled date passing does not prove publication.

---

# Performance Feedback Loop

```text
published posts
→ linkedin-performance-review
→ qualified learnings
→ future series planning
```

Learning classes remain:

```text
strong_observation
tentative_pattern
test_next
insufficient_data
```

Do not convert observational patterns into platform rules or causal claims.

---

# Failure Isolation

For three posts:

```text
POST-1 ready
POST-2 needs personal story input
POST-3 validator FAIL
```

correct behavior is:

```text
POST-1 → continue
POST-2 → needs_input
POST-3 → local repair
```

Do not block unrelated valid items.

---

# End-to-End Validation

KnowledgeCraft has been exercised through a synthetic research-to-LinkedIn integration flow that produced:

```text
1 registered source
→ grounding
→ insights
→ author voice profile
→ 3-post series
→ 3 drafts
→ voice/naturalness refinement
→ platform review
→ factuality PASS
→ quality APPROVE
→ 3 qa_approved posts
→ 3 scheduled posts
```

No post was marked published.

The human publication boundary remained intact.
