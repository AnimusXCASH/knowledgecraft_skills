# Getting Started with KnowledgeCraft

KnowledgeCraft is a reusable OpenCode skill framework for evidence-grounded research, academic knowledge work, professional writing, and LinkedIn content workflows.

You do **not** need to invoke every skill manually.

Start by deciding what outcome you want.

---

# 1. Choose Your Usage Mode

KnowledgeCraft supports three primary modes:

```text
A. Academic / Research
B. LinkedIn / Content
C. Combined Research → LinkedIn
```

You can also invoke individual specialist skills directly when you already know the exact stage you need.

---

# 2. Academic / Research Mode

Use this mode when your goal is:

- building a research knowledge base;
- processing academic papers;
- extracting source-faithful findings;
- creating claim ledgers;
- generating research insights;
- supporting PhD or academic workflows;
- synthesizing evidence;
- translating research into applied-practice questions.

Typical workflow:

```text
source / paper
    ↓
research-library
    ↓
research-source-grounder
    ↓
research-insight-miner
    ↓
grounded research knowledge
```

## Simple prompt

```text
Process this paper for my research knowledge base.

Register the source, ground it faithfully, and create research insights.

Preserve null findings, limitations, uncertainty, and causal boundaries.

Do not create social-media content.
```

If your repository `AGENTS.md` routing is active, a short request can also be enough:

```text
Process this paper for my research knowledge base.
```

KnowledgeCraft should inspect current state and route to the required research skills.

## Ground only

If you want source-faithful extraction without interpretation:

```text
Use research-source-grounder on this source.

Create a source card and claim ledger.

Preserve all null findings, uncertainty, limitations, relationship direction, and causal boundaries.
```

## Insight mining only

If the source is already grounded:

```text
Use research-insight-miner on the validated grounded claims for SRC-123.

Create communication-useful and applied insights without introducing new findings or causal mechanisms.
```

## Multiple papers

For several sources:

```text
Process these sources through the KnowledgeCraft research workflow.

Register each source, complete the required grounding stage, and create validated insight artifacts.

Use research-batch where appropriate.
```

---

# 3. LinkedIn / Content Mode

Use this mode when your research or approved insights already exist and your goal is content creation.

Typical workflow:

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
```

Scheduling is optional:

```text
qa_approved
    ↓
linkedin-calendar-planner
    ↓
scheduled
```

## Create a series

```text
Use these grounded research insights to create a three-post LinkedIn series.

Preserve source and claim traceability.

Keep the posts distinct, avoid unsupported mechanisms, and do not invent personal stories.
```

## Draft one post

```text
Draft POST-002 from its approved series brief.

Use only the claims and insights allowed by the brief.

Do not strengthen causal or relationship language.
```

## Prepare a draft for publication

```text
Take POST-002 through the remaining LinkedIn preparation workflow.

Use my validated author voice profile if available.

Apply naturalness editing only if needed.

Run LinkedIn platform review, factuality review, and the content quality gate.

Do not schedule or publish yet.
```

## Create a calendar

```text
Create a publishing calendar for my qa_approved LinkedIn posts.

Respect dependencies, fixed dates, blackout dates, and any cadence I provide.

Do not invent exact "best posting times."
```

---

# 4. Combined Research → LinkedIn Mode

This is the full evidence-to-content workflow.

Use it when you have a paper, report, or research source and want both:

1. durable research knowledge; and
2. evidence-grounded LinkedIn content.

Typical workflow:

```text
research source
     ↓
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
```

## Full combined prompt

```text
Process this research paper and turn it into an evidence-grounded LinkedIn series.

First register and ground the source.
Then create communication-useful insights.
Create a three-post LinkedIn series.
Draft each post from its approved brief.
Use my existing validated author voice profile if available.
Apply naturalness editing only where useful.
Run LinkedIn platform review, factuality review, and final content quality review.

Do not publish anything.
```

If scheduling is also wanted:

```text
After all posts are legitimately qa_approved, create a publishing calendar using my supplied cadence and date constraints.

Do not invent exact posting times.
```

---

# 5. Automatic Routing vs Direct Skill Use

KnowledgeCraft supports two ways of working.

## Outcome-first / automatic routing

Use this when you know what you want but do not care which internal skill should run.

Examples:

```text
Turn this paper into a LinkedIn series.
```

```text
Get this post ready to publish.
```

```text
Continue from where the workflow stopped.
```

```text
Add these papers to my research knowledge base.
```

The orchestrator/root routing should:

1. inspect current state;
2. reuse valid existing artifacts;
3. identify the minimum missing stage;
4. route to the owning specialist skill;
5. require validator PASS where applicable.

## Direct specialist use

Use this when you know the exact task.

Examples:

```text
Use research-source-grounder on SRC-123.
```

```text
Run factuality-guard on POST-002.
```

```text
Use linkedin-series-architect to turn these validated insights into a five-post series.
```

```text
Run linkedin-calendar-planner on the current qa_approved posts.
```

Direct invocation is useful for debugging, revision, or advanced workflows.

---

# 6. Which Skill Should I Use?

```text
What do you want?

Build research knowledge?
→ research-library
→ research-source-grounder
→ research-insight-miner

Process many research sources?
→ research-batch

Create a LinkedIn series from validated evidence?
→ linkedin-series-architect

Draft one approved post brief?
→ linkedin-post-drafter

Create an author voice profile?
→ author-voice-profiler

Apply an existing author voice?
→ author-voice-editor

Improve mechanical/generic prose?
→ text-naturalness-editor

Explicit protected-span humanization?
→ text-humanizer

Review LinkedIn presentation?
→ linkedin-platform-review

Check factual accuracy?
→ factuality-guard

Make final approve/revise/block decision?
→ content-quality-gate

Schedule qa_approved posts?
→ linkedin-calendar-planner

Learn from published performance?
→ linkedin-performance-review

Need the system to decide what happens next?
→ linkedin-content-pipeline / automatic routing
```

---

# 7. KnowledgeCraft Is Not LinkedIn-Only

The research layer is independent.

```text
                         ┌→ academic writing
                         ├→ PhD knowledge base
                         ├→ evidence synthesis
research foundation ─────┼→ applied-practice translation
                         ├→ professional reports
                         └→ LinkedIn/content
```

You can use only the academic/research skills and never invoke the LinkedIn subsystem.

Likewise, the LinkedIn skills can work from already-grounded evidence without reprocessing the original research every time.

---

# 8. Important Workflow Rules

## Preserve evidence boundaries

KnowledgeCraft should never silently transform:

```text
associated with
```

into:

```text
caused
improved
protected
prevented
```

unless the source genuinely supports that interpretation.

## Preserve null findings

A non-significant or null result remains part of the evidence base.

Do not silently discard inconvenient findings.

## Do not fabricate personal stories

Story-based content requires genuine author-provided material.

Missing story input should produce:

```text
needs_input
```

not an invented anecdote.

## Do not invent LinkedIn algorithm rules

KnowledgeCraft should not claim:

- Tuesday is best;
- 9:00 is optimal;
- carousels are boosted;
- external links are suppressed;
- daily posting is rewarded;

without current verified evidence relevant to the request.

## QA is version-sensitive

A material text change after approval requires:

```text
factuality-guard
→ content-quality-gate
```

again.

Old approval must not silently survive substantive edits.

## Scheduling is not publishing

Normal boundary:

```text
scheduled
→ human / authorized publisher
→ published
```

A scheduled date passing does not prove publication.

---

# 9. Resume Instead of Restart

KnowledgeCraft should inspect the latest valid state.

Examples:

```text
new
→ start research processing
```

```text
grounded
→ start at research-insight-miner
```

```text
ideas_created
→ start at linkedin-series-architect
```

```text
series_planned
→ start at linkedin-post-drafter
```

```text
drafted
→ continue at the next required editing/QA stage
```

```text
qa_approved + user asks for calendar
→ start at linkedin-calendar-planner
```

Do not rerun research unnecessarily.

---

# 10. Generated Artifacts

Reusable skill definitions live in:

```text
.opencode/skills/
```

Generated working artifacts belong in:

```text
.knowledgecraft/
```

Typical locations:

```text
.knowledgecraft/research/grounded/
.knowledgecraft/research/insights/
.knowledgecraft/writing/
.knowledgecraft/content/ideas/
.knowledgecraft/content/drafts/
.knowledgecraft/content/calendar/
.knowledgecraft/analytics/
```

Do not place generated project artifacts inside `.opencode/skills/`.

---

# 11. Validate the Repository

Run the complete deterministic repository check:

```powershell
.\scripts\check-all.ps1
```

or:

```powershell
py .\scripts\check_all.py --root D:\knowledgecraft_skills
```

Successful validation ends with:

```text
KNOWLEDGECRAFT CHECK: PASS
```

See:

```text
TESTING.md
```

for the full testing model.

---

# 12. Recommended First Experiments

## Research-only

Take one real research paper and run:

```text
research-library
→ research-source-grounder
→ research-insight-miner
```

Inspect the claim ledger before using downstream insights.

## LinkedIn-only

Take one already-grounded insight and run:

```text
linkedin-series-architect
→ linkedin-post-drafter
→ linkedin-platform-review
→ factuality-guard
→ content-quality-gate
```

## Full workflow

Take one paper and ask:

```text
Process this paper into my research knowledge base and then turn the validated insights into a three-post LinkedIn series.

Do not publish anything.
```

The system should reuse its existing artifacts if you invoke it again later.
