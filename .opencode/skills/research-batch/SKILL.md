---
name: research-batch
description: Resume and batch-process only new or unfinished research sources from a local research registry. Use for requests such as process new papers, catch up the research folder, or continue where a previous research-to-content workflow stopped.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "research-orchestration"
  opencode/slash: "true"
---

# Research Batch
Load `research-library` first.

Default flow: scan → extract → resume each source from its current valid state → save artifacts → update state.

If the user only says “process new research”, stop at `ideas_created`: `scan → extract → ground → mine ideas → stop`. Do not automatically turn every source into publishable content.

Resume from: `extracted` → grounding; `grounded` → insight mining; `ideas_created` → stop unless downstream work is requested; `series_planned` → draft if requested; `drafted` → QA if requested.

If a recorded artifact is missing, treat the stage as incomplete. Prefer one full source → compact artifacts → next source.
