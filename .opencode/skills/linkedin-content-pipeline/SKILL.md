---
name: linkedin-content-pipeline
description: Orchestrate an evidence-grounded LinkedIn content workflow from source material to distinct post ideas, series planning, drafting, voice editing, factual review, quality control, calendar planning, and optional performance learning.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "orchestration"
  opencode/slash: "true"
---

# LinkedIn Content Pipeline

Use this as the end-to-end LinkedIn workflow.

## Principle
Optimize for usefulness, specificity, evidence, real author voice, and audience relevance. Do not optimize for AI-detector scores or invent personal experience.

## Routing
Use only the skills needed:
1. `research-library` for local source discovery/tracking.
2. `research-batch` for new or unfinished sources in bulk.
3. `research-source-grounder` for source cards and claim ledgers.
4. `research-insight-miner` for distinct angles.
5. `linkedin-series-architect` for multi-post arcs.
6. `author-voice-profiler` when genuine writing samples exist.
7. `linkedin-post-drafter` for grounded drafts.
8. `author-voice-editor` for voice alignment.
9. `text-naturalness-editor` for conservative naturalness editing.
10. `linkedin-platform-review` for LinkedIn presentation.
11. `factuality-guard` for claim verification.
12. `content-quality-gate` for APPROVE / REVISE / BLOCK.
13. `linkedin-calendar-planner` for approved-post sequencing.
14. `linkedin-performance-review` for later analytics learning.

## Guardrails
- Distinguish fact, inference, opinion, and proposal.
- Preserve names, dates, numbers, citations, technical terms, and claim strength.
- Never invent anecdotes, quotes, achievements, customers, or emotions.
- Never turn association into causation.
- Do not add deliberate mistakes to appear human.
- Do not treat platform folklore as guaranteed ranking rules.
- Keep publication under human review unless the user explicitly configures an authorized publishing workflow.

## Finish condition
A post is ready only after factuality and quality checks pass and it does not substantially duplicate another post in the same series.
