---
name: linkedin-post-drafter
description: Draft one LinkedIn post from an approved, evidence-traceable post brief while preserving claim strength, causal status, source boundaries, and any supplied author constraints. Use after series planning when the post's audience, reader job, main point, and evidence are already selected.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "drafting"
  opencode/slash: "false"
---

# LinkedIn Post Drafter

Draft **one LinkedIn post from one approved brief**.

The job is to turn an already-selected idea into a clear first draft without inventing evidence, personal experience, mechanisms, or stronger conclusions.

## Responsibility Boundary

`linkedin-post-drafter` owns:

- one-post drafting;
- turning a post brief into readable LinkedIn prose;
- preserving the assigned reader job;
- using only allowed claims/insights;
- maintaining evidence vs interpretation boundaries;
- choosing a fitting draft structure;
- creating a legitimate opening;
- creating an appropriate ending or no CTA;
- recording which claims/insights were actually used;
- flagging missing author input instead of fabricating it.

It does **not**:

- create new research insights;
- expand the evidence base;
- invent source, claim, or insight IDs;
- invent personal stories, experiences, quotes, emotions, achievements, or conversations;
- perform author-voice profiling;
- perform final voice alignment;
- perform naturalness editing;
- perform LinkedIn platform review;
- perform factuality review;
- perform final quality gating;
- decide publication timing.

Related skills:

- `linkedin-series-architect` -> creates the approved post brief;
- `author-voice-editor` -> aligns the draft with an evidence-based author profile;
- `text-naturalness-editor` -> removes mechanical/generic prose conservatively;
- `linkedin-platform-review` -> reviews the finished draft for LinkedIn presentation;
- `factuality-guard` -> verifies factual fidelity;
- `content-quality-gate` -> final publication decision.

## Required Inputs

Prefer an approved brief containing:

- `post_id`;
- `drafting_status`;
- audience;
- audience problem/question;
- reader job;
- evidence mode;
- main point;
- source IDs;
- claim IDs;
- insight IDs;
- drafting constraints;
- opening mechanism;
- ending function;
- optional recommended format;
- optional author-input requirements.

If a brief is marked:

`drafting_status: needs_input`

do not silently fill the missing material.

If a brief is marked:

`drafting_status: blocked`

do not draft it as written.

If no approved brief is supplied, build only the smallest provisional brief needed and clearly label it provisional.

## One-Post Rule

Draft one post at a time unless the user explicitly requests batch drafting.

Do not draft an entire series from a series plan by default.

This reduces:

- evidence drift;
- repeated hooks;
- repeated endings;
- accidental claim reuse;
- generic series templating.

## Brief Is the Contract

Treat the approved brief as the drafting boundary.

Do not:

- change the reader job;
- change the main point;
- add unrelated insights;
- pull in other series claims merely because they are available;
- convert a supporting claim into the central claim without justification;
- change the evidence mode.

If the brief is flawed or under-specified, report the problem rather than silently redesigning it.

## Evidence Traceability

Every evidence-bearing draft must retain traceability to the supplied brief.

Track:

- `source_ids`;
- `claim_ids_used`;
- `insight_ids_used`.

Use only IDs already present in the approved brief.

Do not invent IDs.

Do not cite a claim ID in metadata if its substance was not actually used in the draft.

## Evidence Mode

Respect the brief's `evidence_mode`.

### `evidence_grounded`

The post centers grounded findings or source-faithful facts.

Do not add interpretation beyond what is already authorized.

### `evidence_informed_interpretation`

The post may express an existing grounded insight or controlled interpretation.

Keep the distinction between evidence and interpretation visible.

### `application_question`

Translate the evidence into a practical question or decision frame without pretending the application is an empirical finding.

### `author_opinion`

Clearly write as opinion or perspective.

Do not present it as research evidence.

### `story`

Requires genuine supplied story material.

If story material is missing, return `needs_input`.

## Claim Fidelity Rule

Use the supplied claims faithfully.

Do not change:

- population;
- direction;
- magnitude;
- timing;
- sample size;
- relationship terminology;
- causal status;
- uncertainty;
- limitation wording when scientifically meaningful.

Do not turn:

`was associated with`

into:

- caused;
- improved;
- reduced;
- prevented;
- drove;
- led to.

Do not turn:

`athletes who reported X also reported Y`

into:

`X was associated with Y`

unless that relationship terminology is explicitly available from the grounded claim.

## Causal Lock

If the evidence does not establish causality:

- do not imply causality in the hook;
- do not imply causality in the body;
- do not imply causality in the takeaway;
- do not imply causality in the CTA.

A cautious body does not repair a causal headline.

## Interpretation Boundary

Keep distinct:

- finding;
- interpretation;
- application;
- recommendation.

Example:

```text
Finding:
Higher perseverance was associated with lower odds of serious dropout thoughts.

Interpretation:
This may make perseverance relevant to how dropout-related thinking is discussed.

Application question:
What parts of the environment may support persistence?

Not allowed:
Building perseverance will prevent dropout.
```

Do not merge these layers merely to make the post smoother.

## Unsupported Mechanism Rule

Do not invent mechanisms such as:

- confidence;
- motivation;
- resilience;
- trust;
- psychological safety;
- belonging;
- identity;
- self-efficacy;

unless they are explicitly supplied in the brief/evidence.

A mechanism that sounds plausible is still unsupported if it was not supplied.

## Personal Experience Rule

Never invent:

- `In my experience...`;
- `I've seen...`;
- athlete stories;
- coaching conversations;
- personal failures;
- successes;
- emotions;
- client examples;
- club cases;
- quotes.

If the reader job is `story` and no genuine story is supplied:

```yaml
draft_status: needs_input
author_input_required: true
```

Specify exactly what input is needed.

## Opening Rule

The opening should earn attention legitimately.

Use the assigned opening mechanism from the brief as guidance.

Possible mechanisms:

- direct observation;
- evidence-led statement;
- misconception;
- practical question;
- contrast;
- supplied story;
- data point;
- conceptual tension.

Do not force:

- sensationalism;
- clickbait;
- unsupported certainty;
- `You won't believe...`;
- fabricated urgency;
- exaggerated claims.

Do not write a stronger opening than the evidence permits.

## No Hook Template Rule

Do not default to:

```text
We often talk about X as if...
```

or:

```text
The question is not X. It is Y.
```

or:

```text
This changes everything.
```

unless the approved brief and series context justify that form.

The opening should fit the idea, not a universal LinkedIn template.

## Body Structure

Choose the simplest structure that fits the reader job.

Possible structures include:

- observation -> evidence -> implication;
- finding -> interpretation -> application question;
- misconception -> correction -> consequence;
- problem -> evidence -> practical frame;
- evidence -> limitation -> takeaway;
- question -> reasoned answer;
- concise argument;
- genuine story -> lesson.

Do not force every post into:

```text
hook
three bullets
CTA
```

Lists are appropriate only when the content is genuinely list-shaped.

## Technical Language

Keep useful technical terms when they matter.

Do not oversimplify a construct merely because the destination is LinkedIn.

Where useful:

- define once;
- explain briefly;
- retain the exact construct name.

Do not substitute a looser term if it changes scientific meaning.

## Numbers and Statistics

Use numbers only when:

- they are present in the allowed evidence;
- they materially help the reader;
- their meaning can be communicated accurately.

Preserve exact values.

Do not:

- round without permission when precision matters;
- reinterpret p-values;
- add practical significance;
- describe an effect as large/small unless supplied;
- use a statistic as a dramatic hook if that framing is misleading.

## Citations and Source Mentions

Do not invent citations or references.

If formal citations are supplied and the brief requires them, preserve them accurately.

If a LinkedIn post does not need formal in-text citation, retain source traceability in metadata even if the visible draft uses a lighter source mention.

Do not fabricate author/year details.

## Author Voice

If an author voice profile is supplied, use it only as a light drafting aid.

Do not attempt full voice matching inside this skill.

Prefer:

- structural compatibility;
- appropriate first-person level;
- appropriate formality;
- known recurring functional patterns.

Leave detailed alignment to `author-voice-editor`.

Do not turn recurring profile phrases into templates.

## Naturalness

Draft clear prose, but do not over-optimize naturalness here.

Avoid obvious mechanical filler and inflated language.

Do not perform detector-oriented editing.

Detailed naturalness refinement belongs to `text-naturalness-editor`.

## CTA Rule

A CTA is optional.

Use the brief's ending function.

Possible endings:

- concise takeaway;
- reflective question;
- practical next step;
- unresolved tension;
- synthesis;
- no CTA.

Do not automatically append:

- `What do you think?`;
- `Agree?`;
- `Let me know in the comments.`;
- `Share this with someone...`.

A post may end naturally without a CTA.

## Reader Value Rule

Every post should give the reader one clear reason to care.

Possible value:

- a useful distinction;
- a finding;
- a misconception correction;
- a practical question;
- a decision frame;
- a synthesis;
- a genuine story.

Do not pad a weak insight with motivational language.

## Specificity Rule

Prefer concrete detail when it already exists in the brief/evidence.

Do not invent details to make the post sound vivid.

Good:

Use the supplied distinction between developmental variation and perseverance.

Not allowed:

Invent a 15-year-old athlete, a training conversation, or a confidence mechanism.

## Missing Input Rule

If a required element is missing, report it precisely.

Example:

```yaml
author_input_required: true
author_input_needed:
  - "A genuine coaching situation where an athlete developed at a different pace from teammates."
```

Do not replace missing input with generic filler.

## Draft Status

Use exactly one:

- `ready_for_editing`
- `needs_input`
- `blocked`

### `ready_for_editing`

Use when:

- the brief is ready;
- required evidence exists;
- no missing personal/story input blocks the draft;
- the draft stays inside supplied evidence/interpretation boundaries.

### `needs_input`

Use when a viable draft depends on missing author material or missing evidence.

For `needs_input`:

- do not create a complete post around the missing material;
- set `draft_text: ""`;
- identify the missing material in `author_input_needed` and/or `omitted_or_deferred`;
- set `handoff.ready_for_author_voice_edit: false`.

### `blocked`

Use when the supplied brief itself is unsafe or materially inconsistent, such as:

- causal framing unsupported by the evidence;
- missing required traceability;
- evidence contradicts the requested main point;
- the brief is marked blocked upstream.

For `blocked`:

- do not draft around the unsafe brief;
- set `draft_text: ""`;
- explain the blocker in `omitted_or_deferred` and/or handoff notes;
- set `handoff.ready_for_author_voice_edit: false`.

## Output Location

Default:

`.knowledgecraft/content/drafts/<post_id>.yaml`

Optional human-readable draft:

`.knowledgecraft/content/drafts/<post_id>.md`

Do not write generated drafts into `.opencode/skills/`.

## Output Contract

Use:

```yaml
linkedin_post_draft:
  draft_id: "DRAFT-001"
  post_id: "POST-001"
  draft_status: "ready_for_editing|needs_input|blocked"
  destination: "LinkedIn"
  audience: ""
  reader_job: "setup|teach|challenge|evidence|application|synthesis|conversation|story"
  evidence_mode: "evidence_grounded|evidence_informed_interpretation|author_opinion|application_question|story"
  main_point: ""
  source_ids: []
  claim_ids_available: []
  insight_ids_available: []
  claim_ids_used: []
  insight_ids_used: []
  author_input_required: false
  author_input_needed: []
  drafting_constraints:
    - ""
  draft_text: |
    ...
  omitted_or_deferred:
    - item: ""
      reason: ""
  preservation_checks:
    no_new_claims: true
    relationship_language_preserved: true
    causal_status_preserved: true
    uncertainty_preserved: true
    unsupported_mechanism_added: false
    personal_experience_invented: false
    unsupported_story_invented: false
    source_traceability_preserved: true
  handoff:
    ready_for_author_voice_edit: true
    next_skill: "author-voice-editor"
    notes: []
```

## Used-vs-Available Traceability

`claim_ids_available` and `insight_ids_available` describe what the brief allowed.

`claim_ids_used` and `insight_ids_used` describe what the draft actually used.

Do not automatically mark every available claim as used.

If a limitation claim materially shapes the draft, include its ID in `claim_ids_used` even if the draft expresses the limitation in source-faithful paraphrase.

## Omitted / Deferred Content

Use `omitted_or_deferred` when a tempting element is intentionally not drafted.

Examples:

```yaml
- item: "personal coaching story"
  reason: "No genuine story material was supplied."
```

```yaml
- item: "confidence mechanism"
  reason: "Not supported by supplied claims or insights."
```

This makes non-invention visible.

## Handoff Rule

Set:

`ready_for_author_voice_edit: true`

only when:

- `draft_status` is `ready_for_editing`;
- the post has a complete draft;
- evidence-bearing content retains traceability;
- no required author input is missing;
- no unresolved causal/evidence conflict remains.

Otherwise set it false.

## Deterministic Validation

After writing a structured draft YAML, validate its mechanical consistency before reporting it complete.

Run:

```powershell
py ".opencode/skills/linkedin-post-drafter/scripts/validate_linkedin_post_draft.py" ".knowledgecraft/content/drafts/<post_id>.yaml"
```

If validation returns `FAIL`:

1. do not report the draft as complete;
2. read every validation error;
3. repair only the affected YAML, traceability, status, preservation-check, or handoff fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- valid YAML and required top-level structure;
- allowed draft status, reader job, and evidence mode;
- non-empty draft/post identifiers;
- `destination: LinkedIn`;
- ID lists contain unique non-empty strings;
- `claim_ids_used` are a subset of `claim_ids_available`;
- `insight_ids_used` are a subset of `insight_ids_available`;
- ready evidence-bearing drafts retain source, claim, and available-insight traceability;
- ready evidence-bearing drafts actually use at least one allowed claim;
- `ready_for_editing` drafts contain non-empty draft text;
- `ready_for_editing` drafts do not still require author input;
- `needs_input` drafts identify required input and do not contain a completed draft;
- `blocked` drafts do not contain a completed draft;
- omitted/deferred items use structured `item` + `reason` fields;
- all preservation checks are present and boolean;
- ready drafts have safe preservation-check values;
- handoff readiness agrees with draft status and safety;
- ready handoff points to `author-voice-editor`.

The validator does **not** determine whether:

- prose is genuinely good;
- a claim was semantically paraphrased correctly;
- causal or relationship wording was subtly strengthened;
- a mechanism was invented in natural language;
- a personal story is genuine;
- an available source/claim/insight ID exists in the upstream registry.

Those remain semantic/evidence-review responsibilities.

## Minimal Drafting Rule

Do not over-build the post.

The first draft should be:

- complete enough to edit;
- evidence-safe;
- structurally coherent;
- not polished into final publication prose.

Leave room for:

- `author-voice-editor`;
- `text-naturalness-editor`;
- `linkedin-platform-review`;
- factuality and quality QA.

## Final Review Sequence

1. load one approved post brief;
2. verify drafting status;
3. identify reader job and main point;
4. identify allowed claims/insights;
5. identify relationship/causal constraints;
6. identify missing author input;
7. choose a fitting structure;
8. draft one post;
9. compare draft against the brief;
10. verify used claim/insight IDs;
11. check for invented mechanisms/story/personal experience;
12. check opening and ending for unsupported strengthening;
13. set draft status;
14. produce safe handoff.

## Final Checks

Before completing the draft, verify:

- one post only? YES
- approved brief followed? YES
- reader job preserved? YES
- main point preserved? YES
- evidence mode preserved? YES
- only available source/claim/insight IDs used? YES
- claim IDs used reflect actual content? YES
- insight IDs used reflect actual content? YES
- no IDs invented? YES
- population/direction/magnitude/timing preserved? YES
- relationship terminology preserved? YES
- causal status preserved? YES
- uncertainty/limitations preserved? YES
- no unsupported mechanisms invented? YES
- no personal experience/story invented? YES
- opening no stronger than evidence? YES
- no forced hook template? YES
- no forced CTA? YES
- no fabricated citation? YES
- no platform folklore inserted? YES
- missing author input reported explicitly? YES
- handoff status consistent with draft status? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- generated artifacts saved outside `.opencode/skills/`? YES
