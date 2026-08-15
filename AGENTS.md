# KnowledgeCraft Skills

This repository serves two purposes:

1. It contains the reusable KnowledgeCraft OpenCode skill library.
2. It is also a working KnowledgeCraft environment where those skills may be used.

# Default Operating Mode

Unless the user explicitly asks to create, modify, debug, refactor, or develop a skill, operate in **WORK MODE**.

In WORK MODE:

- use existing skills when relevant;
- do not create new skill directories;
- do not modify existing skill definitions;
- do not write generated research, writing, analysis, or content artifacts inside `.opencode/skills/`;
- store generated work under `.knowledgecraft/`.

A normal research, writing, analysis, grounding, synthesis, humanization, or content request is **NOT** a request to create a new skill.

# Skill-First Routing

When an existing KnowledgeCraft skill clearly matches the user's task, load that skill before performing the task.

Do not reproduce or approximate a skill's behavior from `AGENTS.md` alone when the corresponding skill is available.

The responsibility split is:

```text
AGENTS.md
    ↓
determines repository-wide behavior,
boundaries, and which skill should be used

SKILL.md
    ↓
defines how that specific task
must actually be performed
```

Therefore:

```text
matching task
    ↓
identify existing KnowledgeCraft skill
    ↓
load skill
    ↓
follow current SKILL.md
    ↓
perform task
    ↓
save output in appropriate .knowledgecraft/ location
```

If a matching skill exists, prefer using it over manually recreating its workflow.

# Skill Development Mode

Enter **SKILL DEVELOPMENT MODE** only when the user explicitly asks to:

- create a skill;
- update a skill;
- modify a `SKILL.md`;
- debug a skill;
- refactor a skill;
- add a new KnowledgeCraft capability;
- change scripts or references belonging to a skill.

Only in SKILL DEVELOPMENT MODE may files under:

```text
.opencode/skills/
```

be created or modified.

Do not infer skill-development intent merely because the current repository is a skill repository.

When uncertain whether the user wants to:

```text
USE A SKILL
```

or:

```text
CREATE OR MODIFY A SKILL
```

default to:

```text
USE THE EXISTING SKILL
```

# Repository Structure

Reusable KnowledgeCraft skills live in:

```text
.opencode/skills/<skill-id>/
```

Generated working artifacts live in:

```text
.knowledgecraft/
```

Recommended working structure:

```text
.knowledgecraft/
├── research/
│   ├── registry/
│   ├── extracted/
│   ├── grounded/
│   ├── insights/
│   └── synthesis/
├── writing/
├── applied/
├── content/
│   ├── ideas/
│   ├── drafts/
│   ├── approved/
│   └── calendar/
├── analytics/
└── scratch/
```

Create these directories when required.

# Hard Output Boundary

Never store generated user/project artifacts inside:

```text
.opencode/
.opencode/skills/
```

unless the artifact itself is explicitly part of SKILL DEVELOPMENT MODE.

Examples of files that must not be written to `.opencode/skills/` during normal work include:

- source cards;
- claim ledgers;
- research summaries;
- extracted papers;
- research insights;
- literature syntheses;
- analysis results;
- writing revisions;
- LinkedIn drafts;
- reports;
- calendars;
- analytics;
- temporary notes.

These belong under:

```text
.knowledgecraft/
```

# Mandatory Research Grounding Routing

For any request whose primary purpose is to:

- ground research;
- create a source card;
- create a claim ledger;
- create a structured evidence base from research;
- extract reusable claims from a paper;
- extract reusable claims from a report;
- extract reusable claims from a research note;
- extract reusable claims from a transcript;
- distinguish source facts from interpretations;
- prepare research material for later synthesis;
- prepare research material for knowledge translation;
- prepare research material for content creation;

you **MUST load `research-source-grounder` before producing or saving the grounded output**.

Do not perform research grounding directly from `AGENTS.md` instructions when `research-source-grounder` is available.

Required sequence:

```text
research-grounding request
        ↓
load research-source-grounder
        ↓
follow current research-source-grounder/SKILL.md
        ↓
create grounded artifacts
        ↓
save under .knowledgecraft/research/grounded/
```

The `research-source-grounder` skill is the authoritative instruction set for grounding behavior.

`AGENTS.md` determines that the skill should be used.

It does not replace the skill.

If `research-source-grounder` cannot be loaded, report that clearly rather than silently approximating its behavior.

# Research Grounding Integrity

When grounding research:

- use only information supported by the supplied source;
- do not invent missing methods;
- do not invent instruments;
- do not invent results;
- do not invent limitations;
- do not invent metadata;
- distinguish source facts from model inference;
- preserve source wording where scientifically meaningful;
- preserve statistical relationship terminology;
- preserve causal strength;
- preserve uncertainty;
- preserve study-design terminology;
- preserve compound claims when splitting them would alter meaning;
- use `Not stated in source` rather than guessing.

For example:

```text
associated with
```

must not casually become:

```text
correlated with
linked to
caused
```

Likewise:

```text
reported ... also reported
```

must not automatically be converted into a named statistical relationship that the source did not provide.

Detailed grounding behavior belongs to:

```text
.opencode/skills/research-source-grounder/SKILL.md
```

# Research Artifact Locations

Research registry:

```text
.knowledgecraft/research/registry/
```

Extracted research:

```text
.knowledgecraft/research/extracted/
```

Grounded research:

```text
.knowledgecraft/research/grounded/
```

Research insights:

```text
.knowledgecraft/research/insights/
```

Cross-source synthesis:

```text
.knowledgecraft/research/synthesis/
```

Do not place these artifacts directly in `.knowledgecraft/` when a more specific directory exists.

# Research Library Routing

When the user asks to:

- scan research folders;
- identify new research files;
- identify previously processed sources;
- extract PDFs or DOCX files;
- detect duplicate sources;
- detect revised sources;
- inspect research processing status;

use the existing:

```text
research-library
```

skill when relevant.

Research-library state should remain under:

```text
.knowledgecraft/research/
```

# Research Batch Routing

When the user asks to:

- process all new research;
- continue unfinished research processing;
- catch up a research folder;
- process several new papers;
- resume previously interrupted research processing;

use:

```text
research-batch
```

when relevant.

Unless the user requests downstream content creation, the normal batch stopping point is:

```text
ideas_created
```

Do not automatically turn every research source into LinkedIn posts.

# Research Insight Routing

When grounded research already exists and the user asks to:

- identify useful insights;
- derive communication angles;
- identify applied implications;
- create distinct evidence-grounded ideas;
- identify potential research-to-practice themes;

use:

```text
research-insight-miner
```

when relevant.

Do not use the insight miner as a replacement for grounding.

The normal order is:

```text
source
    ↓
research-source-grounder
    ↓
grounded claims
    ↓
research-insight-miner
```

# Writing and Humanization Routing

For direct editing of text pasted into OpenCode, use:

```text
text-humanizer
```

when appropriate.

For pipeline-level naturalness editing, use:

```text
text-naturalness-editor
```

when appropriate.

For learning a real author's writing style from genuine samples, use:

```text
author-voice-profiler
```

For aligning a draft with an existing voice profile, use:

```text
author-voice-editor
```

Do not create a new writing skill merely because the user asks to edit text.

# Writing Integrity

When editing research or technical writing:

- preserve facts;
- preserve statistics;
- preserve citations;
- preserve technical terminology;
- preserve statistical relationship terminology;
- preserve causal status;
- preserve uncertainty;
- preserve limitations;
- preserve claim strength.

Naturalness must never override scientific integrity.

# Factuality Routing

When the task requires checking whether a draft accurately represents supplied evidence, use:

```text
factuality-guard
```

when relevant.

This is especially important for:

- causal claims;
- statistics;
- quotations;
- dates;
- named entities;
- research findings;
- claims whose wording may be stronger than the evidence.

# LinkedIn Routing

For an end-to-end LinkedIn workflow, use:

```text
linkedin-content-pipeline
```

when appropriate.

Relevant supporting skills include:

```text
linkedin-series-architect
linkedin-post-drafter
linkedin-platform-review
linkedin-calendar-planner
linkedin-performance-review
```

Do not treat changing platform-algorithm folklore as permanent factual rules.

# Foundation

For coding, scripts, schemas, tests, repository modifications, and skill-development work, follow:

```text
karpathy-guidelines
```

Core principles:

- surface important assumptions;
- prefer the simplest adequate solution;
- make narrowly scoped changes;
- define verifiable success criteria;
- verify before declaring completion.

# Skill Contribution Rules

When explicitly operating in SKILL DEVELOPMENT MODE:

- keep skills generic and reusable;
- store each skill at `.opencode/skills/<skill-id>/SKILL.md`;
- use lowercase kebab-case IDs;
- keep descriptions specific enough for automatic routing;
- place supporting material under the skill's `references/` or `scripts/`;
- do not add private research or user-specific data;
- do not add detector-evasion instructions;
- do not encode unstable platform folklore as permanent rules;
- preserve factual meaning and evidential strength in research-related skills.

After modifying skills, run:

```text
py validate_skills.py
```

before considering the repository valid.

# Default Decision Rule

When uncertain:

```text
Does an existing KnowledgeCraft skill match this task?
```

If yes:

```text
LOAD AND USE IT
```

If no:

```text
perform the task normally
```

Only create or modify a skill when the user explicitly requests skill development.