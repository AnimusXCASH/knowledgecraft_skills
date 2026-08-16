# KnowledgeCraft Skills

KnowledgeCraft is an open-source OpenCode skill framework for **research, evidence grounding, academic knowledge work, writing, quality assurance, research-to-content translation, and LinkedIn workflows**.

It is designed as a modular system rather than one monolithic agent: each skill owns a bounded responsibility, produces explicit artifacts, and hands work forward only when its contract is satisfied.

## What can I use it for?

KnowledgeCraft supports three main modes:

| Mode | Start with | Typical result |
|---|---|---|
| **Academic / Research** | PDF/DOCX/research source | registered source, source card, claim ledger, validated insights |
| **LinkedIn / Content** | grounded evidence or approved insights | series, drafts, QA-approved posts, calendar |
| **Combined** | research source | durable research artifacts **and** evidence-grounded LinkedIn content |

The research subsystem works independently. You do not need to use LinkedIn features.

## Quick start

### 1. Install KnowledgeCraft into an OpenCode project

Recommended project layout:

```text
your-project/
├── AGENTS.md
├── papers/                         ← YOU PUT RESEARCH PAPERS HERE
├── .opencode/
│   └── skills/
│       ├── research-library/
│       ├── research-source-grounder/
│       ├── research-insight-miner/
│       └── ...
└── .knowledgecraft/                ← GENERATED AUTOMATICALLY
```

Copy the KnowledgeCraft `.opencode/skills/` directory into your project and use the repository `AGENTS.md` if you want the documented automatic-routing behavior.

### 2. Put a research paper in `./papers/`

Example:

```text
your-project/
└── papers/
    └── Aalberg_and_Saether_2016.pdf
```

`papers/` is **input**.

`.knowledgecraft/` is **generated state/output**.

Do not manually place papers in:

```text
.knowledgecraft/research/grounded/
.knowledgecraft/research/insights/
```

Those directories are produced by the workflow.

You can also use a paper located elsewhere by giving its explicit path.

### 3. Start OpenCode from the project root

For example:

```powershell
cd D:\my-project
opencode
```

Use the OpenCode command/version installed on your system.

### 4. Tell KnowledgeCraft what you want

Research only:

```text
Process ./papers/Aalberg_and_Saether_2016.pdf for my research knowledge base.

Register the source, extract it, ground it faithfully, and create validated research insights.

Preserve null findings, limitations, uncertainty, and causal boundaries.
Do not create social-media content.
```

Process all new papers:

```text
Process all new and unfinished research in ./papers through ideas_created.
```

Research → LinkedIn:

```text
Process ./papers/Aalberg_and_Saether_2016.pdf into my research knowledge base and then create a three-post evidence-grounded LinkedIn series.

Take the posts through factuality and quality review.
Do not publish anything.
```

KnowledgeCraft should inspect existing state and resume from the latest valid stage instead of restarting unnecessarily.

## Direct commands

User-facing slash-enabled skills currently include:

```text
/research-library
/research-batch
/linkedin-content-pipeline
/text-humanizer
```

Examples:

```text
/research-library

Scan ./papers, extract pending sources, and show status.
```

```text
/research-batch

Process all new and unfinished research in ./papers through ideas_created.
```

```text
/linkedin-content-pipeline

Take the validated research insights for SRC-123 and create a three-post LinkedIn series.
Prepare the posts through final QA.
Do not publish.
```

Most specialist skills are normally selected automatically by `AGENTS.md` / the pipeline, but advanced users can explicitly request them by name.

## Deterministic research-library CLI

The research library also includes a deterministic CLI:

```bash
python .opencode/skills/research-library/scripts/research_library.py scan ./papers
python .opencode/skills/research-library/scripts/research_library.py extract --pending
python .opencode/skills/research-library/scripts/research_library.py status
```

Optional extraction dependencies:

```bash
pip install -r .opencode/skills/research-library/scripts/requirements-optional.txt
```

The library tracks source identity, path, extraction state, duplicates/revisions, and lifecycle under `.knowledgecraft/research/`.

## Where files go

### User inputs

Recommended:

```text
papers/                          research papers/reports you provide
```

For one-off work you may also reference an absolute or relative source path directly.

### Generated research artifacts

```text
.knowledgecraft/research/registry/
.knowledgecraft/research/extracted/
.knowledgecraft/research/grounded/
.knowledgecraft/research/insights/
.knowledgecraft/research/synthesis/
```

### Generated content artifacts

```text
.knowledgecraft/content/ideas/
.knowledgecraft/content/drafts/
.knowledgecraft/content/approved/
.knowledgecraft/content/calendar/
```

### Generated writing/analytics artifacts

```text
.knowledgecraft/writing/
.knowledgecraft/analytics/
```

The included `papers/.gitignore` keeps local papers out of Git by default.

## Workflow overview

```text
                         RESEARCH
paper / report
     ↓
research-library
     ↓
research-source-grounder
     ↓
research-insight-miner
     │
     ├──────────────→ academic / research use
     │
     └──────────────→ LinkedIn/content
                         ↓
               linkedin-series-architect
                         ↓
               linkedin-post-drafter
                         ↓
                 author voice / naturalness
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
              human/authorized publication
                         ↓
                      published
                         ↓
             linkedin-performance-review
```

## Skill collection

### Foundation

- `karpathy-guidelines`

### Research

- `research-library`
- `research-batch`
- `research-source-grounder`
- `research-insight-miner`

### Writing and quality

- `author-voice-profiler`
- `author-voice-editor`
- `text-naturalness-editor`
- `text-humanizer`
- `factuality-guard`
- `content-quality-gate`

### LinkedIn / research-to-content

- `linkedin-content-pipeline`
- `linkedin-series-architect`
- `linkedin-post-drafter`
- `linkedin-platform-review`
- `linkedin-calendar-planner`
- `linkedin-performance-review`

See [`SKILLS.md`](SKILLS.md) for the skill index.

## Documentation

Start here:

- [`GETTING_STARTED.md`](GETTING_STARTED.md) — setup, where to put files, and copy-paste commands
- [`COMMANDS.md`](COMMANDS.md) — quick command/prompt recipes
- [`WORKFLOWS.md`](WORKFLOWS.md) — Academic, LinkedIn, and Combined workflow contracts
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — internal architecture and artifact boundaries
- [`TESTING.md`](TESTING.md) — deterministic, semantic, and integration validation
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — attribution

## Validation

Run the entire deterministic repository check:

```powershell
.\scripts\check-all.ps1
```

or:

```powershell
py .\scripts\check_all.py --root .
```

A successful run ends with:

```text
KNOWLEDGECRAFT CHECK: PASS
```

## Core principles

- Ground before drafting.
- Preserve claim strength.
- Preserve null findings and limitations.
- Separate source fact, inference, opinion, and proposal.
- Never invent personal experience.
- Treat current platform behavior as something to verify, not permanent folklore.
- Reuse validated artifacts instead of restarting workflows.
- Keep generated work under `.knowledgecraft/`, not inside `.opencode/skills/`.

## Third-party attribution

See `THIRD_PARTY_NOTICES.md`.

## License

MIT.
