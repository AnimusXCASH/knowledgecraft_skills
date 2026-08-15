# KnowledgeCraft Skills

A growing open-source collection of reusable OpenCode skills for research, evidence synthesis, knowledge translation, applied practice, academic workflows, sports science, writing, analysis, and professional knowledge work.

## Initial collection

### Foundation
- `karpathy-guidelines` — adapted coding-agent guardrails for assumptions, simplicity, surgical changes, and verification

### Research
- `research-library`
- `research-batch`
- `research-source-grounder`
- `research-insight-miner`

### Authoring and quality
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

## Install
Copy the wanted directories into `<your-project>/.opencode/skills/`. OpenCode V2 discovers project-local skills automatically.

## Direct humanizer
```text
/text-humanizer

PASTE YOUR TEXT HERE
```

Optional:
```text
/text-humanizer

Mode: professional
Keep my direct writing style.
Do not change any statistics or terminology.

PASTE YOUR TEXT HERE
```

## Research folder workflow
`research-library` includes a deterministic script for hashing, extraction, duplicate/revision tracking, and status storage. Runtime state defaults to `.knowledgecraft/` in the consuming project.

```bash
python .opencode/skills/research-library/scripts/research_library.py scan ./papers
python .opencode/skills/research-library/scripts/research_library.py extract --pending
python .opencode/skills/research-library/scripts/research_library.py status
```

Optional extraction dependencies:
```bash
pip install -r .opencode/skills/research-library/scripts/requirements-optional.txt
```

## Principles
Ground before drafting. Preserve claim strength. Separate fact/inference/opinion/proposal. Never invent personal experience. Improve authentic writing quality rather than gaming AI detectors. Treat changing platform behavior as a current research question, not a permanent rule.

## Third-party attribution
See `THIRD_PARTY_NOTICES.md`.

## License
MIT.
