# Testing KnowledgeCraft

KnowledgeCraft uses layered validation so that a skill is not considered reliable merely because its Markdown parses or an LLM says it looks correct.

## Validation model

KnowledgeCraft currently uses three validation levels.

### Level 1 — Skill structure validation

The repository-level validator checks the structural integrity of all skills.

Run:

```powershell
py validate_skills.py
```

Current repository target:

```text
PASSED: 17 skills
```

This level checks that skill packages conform to the expected repository structure and metadata requirements.

### Level 2 — Deterministic validators and unit tests

Skills with machine-checkable contracts include deterministic Python validators and test suites under:

```text
.opencode/skills/<skill>/scripts/
```

Typical structure:

```text
SKILL.md
scripts/
  validate_<artifact>.py
  test_validate_<artifact>.py
```

Validators are used for properties that should not depend on model judgment, such as:

- valid YAML;
- required fields;
- unique IDs;
- lifecycle vocabulary;
- traceability references;
- arithmetic consistency;
- dependency ordering;
- approval-state consistency;
- handoff-state consistency.

### Level 3 — Semantic and integration regressions

Semantic regressions test behavior that cannot be fully reduced to schema validation.

Examples include:

- preserving null findings;
- avoiding causal strengthening;
- distinguishing missing data from zero;
- not inventing LinkedIn algorithm rules;
- respecting skill responsibility boundaries;
- routing only to required workflow stages.

End-to-end integration tests verify that individually validated skills can interoperate through their real artifacts and validators.

The first full LinkedIn integration test exercised:

```text
research-library
→ research-source-grounder
→ research-insight-miner
→ author-voice-profiler
→ linkedin-series-architect
→ linkedin-post-drafter
→ author-voice-editor
→ text-naturalness-editor
→ linkedin-platform-review
→ factuality-guard
→ content-quality-gate
→ linkedin-calendar-planner
→ linkedin-content-pipeline
```

The test produced three QA-approved and scheduled posts while preserving the human publication boundary.

## Repository-wide check

The preferred local command is:

```powershell
.\scripts\check-all.ps1
```

If PowerShell execution policy blocks unsigned scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check-all.ps1
```

Or run the Python runner directly:

```powershell
py .\scripts\check_all.py --root D:\knowledgecraft_skills
```

The runner automatically discovers:

```text
.opencode/skills/*/scripts/test_*.py
```

so newly added deterministic test suites are included without editing the runner.

A successful repository check ends with:

```text
KNOWLEDGECRAFT CHECK: PASS
```

At the time this document was created, the repository-wide check covered:

```text
Skills discovered:            17
Deterministic test suites:    10
Tests counted:                143
Failed suites:                0
```

## Running an individual deterministic suite

Example:

```powershell
cd D:\knowledgecraft_skills\.opencode\skills\linkedin-calendar-planner\scripts
py test_validate_linkedin_calendar.py
```

Run a validator directly against an artifact:

```powershell
py validate_linkedin_calendar.py `
  D:\knowledgecraft_skills\.knowledgecraft\content\calendar\linkedin-calendar.yaml
```

## Validator policy

When a specialist skill has a deterministic validator:

```text
semantic PASS + validator FAIL = FAIL
```

A model-generated statement that an artifact is valid never overrides deterministic validation.

The correct repair loop is:

```text
generate artifact
→ run validator
→ inspect errors
→ repair only affected fields/content
→ rerun validator
→ continue only after PASS
```

## What deterministic validation should cover

Prefer deterministic checks for:

- schema;
- required fields;
- allowed status values;
- unique IDs;
- referential integrity;
- arithmetic;
- chronology;
- lifecycle transitions;
- validator/handoff state;
- duplicate artifact identifiers.

Do not use deterministic validators to pretend to solve inherently semantic judgments such as:

- whether prose sounds natural;
- whether a research interpretation is appropriately nuanced;
- whether a content angle is genuinely useful;
- whether a LinkedIn post is strategically compelling;
- whether a pattern is causally meaningful.

Those belong to semantic review.

## Adding tests for a new skill

When a new skill introduces a structured artifact or machine-checkable contract:

1. add the skill under `.opencode/skills/<skill>/`;
2. add a deterministic validator where appropriate;
3. add `scripts/test_*.py`;
4. run the local suite;
5. run the repository checker;
6. add semantic regression cases for non-mechanical behavior;
7. run an integration test when the skill joins a multi-skill workflow.

A new test suite matching:

```text
.opencode/skills/*/scripts/test_*.py
```

will be picked up automatically by the repository-wide runner.

## CI

GitHub Actions should run the same repository checker used locally:

```text
python scripts/check_all.py --root .
```

The local checker is therefore the source of truth for deterministic repository validation.
