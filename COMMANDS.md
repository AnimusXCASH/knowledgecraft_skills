# KnowledgeCraft Command Recipes

Copy-paste examples for common tasks.

Run OpenCode from your project root, where `AGENTS.md`, `.opencode/skills/`, and your input folders are visible.

---

## Research: one paper

Place the paper here:

```text
./papers/my-paper.pdf
```

Then:

```text
Process ./papers/my-paper.pdf for my research knowledge base.

Register the source, extract it, ground it faithfully, and create validated research insights.

Preserve null findings, limitations, uncertainty, study design, statistical relationship terminology, and causal boundaries.

Do not create social-media content.
```

---

## Research: scan only

```text
/research-library

Scan ./papers and show me:
- new sources;
- previously processed sources;
- duplicates/revisions;
- extraction status;
- lifecycle status.
```

---

## Research: deterministic library CLI

```powershell
py .opencode/skills/research-library/scripts/research_library.py scan ./papers
py .opencode/skills/research-library/scripts/research_library.py extract --pending
py .opencode/skills/research-library/scripts/research_library.py status
```

---

## Research: process all new papers

```text
/research-batch

Process all new and unfinished research in ./papers through ideas_created.

Use research-library for source identity/extraction.
Use research-source-grounder before research-insight-miner.
Preserve null findings and causal boundaries.

Stop after validated research insights.
Do not create LinkedIn content.
```

---

## Research: ground a registered source

```text
Use research-source-grounder on SRC-123.

Create the source card and claim ledger.
Use only source-supported information.
Preserve null findings, uncertainty, design terminology, relationship direction, and causal strength.
```

---

## Research: create insights from grounded evidence

```text
Use research-insight-miner on the validated grounded artifacts for SRC-123.

Create distinct evidence-grounded insights, applied questions, and communication angles.

Do not introduce new findings, mechanisms, mediation, or causal claims.
```

---

## LinkedIn: create a series from validated insights

```text
Create a three-post LinkedIn series from the validated insights for SRC-123.

Use linkedin-series-architect.
Preserve claim and insight traceability.
Give the posts distinct reader jobs.
Avoid unnecessary overlap.
Do not invent personal stories.
```

---

## LinkedIn: draft one post

```text
Draft POST-002 from its validated series brief.

Use linkedin-post-drafter.
Use only allowed claims/insights.
Do not strengthen causal or relationship language.
```

---

## LinkedIn: prepare one post through QA

```text
Take POST-002 through the remaining LinkedIn publication-preparation workflow.

Use my validated author voice profile if available.
Use text-naturalness-editor only if the prose benefits from it.
Run linkedin-platform-review.
Then run factuality-guard on the final platform-reviewed text.
Then run content-quality-gate.

Do not schedule or publish.
```

---

## Combined: paper → research → LinkedIn

```text
/linkedin-content-pipeline

Process ./papers/my-paper.pdf from research registration through a three-post evidence-grounded LinkedIn series.

Required order:
research-library
→ research-source-grounder
→ research-insight-miner
→ linkedin-series-architect
→ linkedin-post-drafter
→ relevant voice/naturalness editing
→ linkedin-platform-review
→ factuality-guard
→ content-quality-gate

Do not publish anything.
```

---

## Combined: paper → research → LinkedIn → calendar

```text
/linkedin-content-pipeline

Process ./papers/my-paper.pdf into my research knowledge base and create a three-post LinkedIn series.

Prepare all posts through legitimate qa_approved state.

Then create a calendar with:
- timezone: Europe/Helsinki
- cadence: Monday and Thursday
- maximum 1 post per day

Do not invent exact posting times.
Do not publish.
```

---

## Resume existing work

```text
Continue this KnowledgeCraft workflow from the latest valid stage.

Inspect the registry, existing artifacts, validators, and lifecycle state first.

Do not rerun valid upstream work unnecessarily.
```

---

## Check one post for factuality

```text
Run factuality-guard on POST-002 against its grounded source/claim artifacts.

Check numbers, relationship direction, causal language, uncertainty, limitations, and population.

Do not rewrite unsupported claims into new claims.
```

---

## Create a calendar

```text
Create a LinkedIn calendar for the current qa_approved posts.

Timezone: Europe/Helsinki
Cadence: Monday and Thursday
Maximum posts per day: 1

Preserve dependencies and blackout dates.
Do not invent an exact "best time."
```

---

## Learn from published performance

```text
Use linkedin-performance-review on the supplied published-post metrics.

Preserve raw counts.
Distinguish zero from missing.
State denominators.
Consider observation windows and exposure.
Do not infer algorithm rules or causality.

Return learnings only as:
strong_observation
tentative_pattern
test_next
insufficient_data
```

---

## Build an author voice profile

Put genuine writing samples somewhere accessible, for example:

```text
./author-samples/
```

Then:

```text
Create an author voice profile from the genuine writing samples in ./author-samples/.

Base the profile only on evidenced writing characteristics.
Do not invent personal biography or preferences.
```

---

## Direct text humanization

```text
/text-humanizer

Mode: professional
Keep my direct writing style.
Preserve all facts, statistics, citations, technical terminology, and causal meaning.

PASTE TEXT HERE
```

---

## Repository validation

```powershell
.\scripts\check-all.ps1
```

or:

```powershell
py .\scripts\check_all.py --root .
```

Expected final line:

```text
KNOWLEDGECRAFT CHECK: PASS
```
