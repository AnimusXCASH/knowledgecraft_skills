# Skill Index

KnowledgeCraft currently contains 17 reusable skills.

| Skill | Category | Slash | Typical use |
|---|---|---:|---|
| `karpathy-guidelines` | foundation | no | Coding/repository guardrails |
| `research-library` | research | yes | Scan/hash/extract/track sources |
| `research-batch` | research | yes | Process new/unfinished research in bulk |
| `research-source-grounder` | research | no | Create source cards and claim ledgers |
| `research-insight-miner` | research | no | Create traceable evidence-grounded insights |
| `author-voice-profiler` | writing | no | Learn a voice profile from genuine samples |
| `author-voice-editor` | writing | no | Align a draft to a validated voice profile |
| `text-naturalness-editor` | writing | no | Conservative pipeline naturalness editing |
| `text-humanizer` | writing | yes | Direct editing of pasted text |
| `factuality-guard` | quality | no | Check claims against supplied evidence |
| `content-quality-gate` | quality | no | Final approve/revise/block QA |
| `linkedin-content-pipeline` | LinkedIn | yes | Outcome-first end-to-end orchestration |
| `linkedin-series-architect` | LinkedIn | no | Multi-post series design and briefs |
| `linkedin-post-drafter` | LinkedIn | no | Draft one evidence-grounded LinkedIn post |
| `linkedin-platform-review` | LinkedIn | no | LinkedIn presentation review |
| `linkedin-calendar-planner` | LinkedIn | no | Schedule qa_approved posts safely |
| `linkedin-performance-review` | LinkedIn | no | Learn cautiously from published analytics |

## Slash-enabled user commands

```text
/research-library
/research-batch
/linkedin-content-pipeline
/text-humanizer
```

Slash-enabled skills are convenient user entry points.

Other specialist skills are usually selected automatically through `AGENTS.md` / orchestration, or requested explicitly by name.

## Research input convention

Recommended source folder:

```text
./papers/
```

Example:

```text
./papers/my-paper.pdf
```

Then:

```text
/research-batch

Process all new papers in ./papers through ideas_created.
```

Or:

```text
Process ./papers/my-paper.pdf for my research knowledge base.
```

Generated state belongs under:

```text
.knowledgecraft/
```

not in the input folder and not under `.opencode/skills/`.

## Direct utility example

```text
/text-humanizer

Mode: professional
Preserve statistics, citations, terminology, and causal meaning.

PASTE TEXT HERE
```

For workflow recipes, see:

```text
GETTING_STARTED.md
COMMANDS.md
WORKFLOWS.md
```
