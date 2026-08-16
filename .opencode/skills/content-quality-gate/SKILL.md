---
name: content-quality-gate
description: Perform a final publication-readiness review for professional, academic, or research-grounded content after factual, voice, naturalness, and destination-specific editing. Return APPROVE, REVISE, or BLOCK with the smallest necessary changes.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "final-qa"
  opencode/slash: "false"
---

# Content Quality Gate

Use this skill as the final publication-readiness gate.

Its job is not to rewrite content from scratch. Its job is to decide whether the current version is ready to publish, needs targeted revision, or must be blocked.

## Responsibility Boundary

`content-quality-gate` evaluates publication quality.

It does **not** replace specialist upstream checks.

Use upstream skills when applicable:

- `factuality-guard` -> factual fidelity and evidence safety;
- `author-voice-editor` -> author voice;
- `text-naturalness-editor` / `text-humanizer` -> natural prose;
- destination/platform-specific review skills -> platform constraints.

The quality gate may identify that one of those areas is weak, but it should not silently redo the specialist workflow unless the user asks for repair.

## Upstream Factuality Rule

For research-grounded, evidence-bearing, or externally checkable content, factuality is a prerequisite rather than a scored quality dimension.

If a current factuality audit is available:

- factuality gate `PASS` -> continue quality review;
- factuality gate `BLOCK` -> final decision must be `BLOCK`.

If factuality has not been checked and the draft contains material externally checkable claims:

- do not assume those claims are safe;
- return `BLOCK` with blocker `factuality_review_required`;
- recommend running `factuality-guard`.

Do not independently invent a second factuality classification system inside this skill.

## Decisions

Use exactly one final decision:

- `APPROVE`
- `REVISE`
- `BLOCK`

### `BLOCK`

Use `BLOCK` when publication should not proceed until a material safety, integrity, or factual problem is resolved.

Block conditions include:

- upstream factuality gate is `BLOCK`;
- material externally checkable claims require factual review but none is available;
- fabricated or unverified personal experience is presented as fact;
- a materially misleading opening, headline, hook, or summary misrepresents the body;
- unattributed quotation, likely plagiarism, or source copying that cannot be accepted as written;
- confidential, private, embargoed, or otherwise non-publishable information is exposed;
- publication would materially misrepresent evidence, authorship, identity, or source attribution;
- a critical platform/legal/organizational requirement is known to be violated.

A blocked draft may also have ordinary quality weaknesses, but blockers take precedence over scoring.

### `REVISE`

Use `REVISE` when there is no blocking condition, but the draft is not publication-ready.

Typical triggers:

- any scored dimension is below `2`;
- total score is below `17/21`;
- opening is weak, generic, or disconnected from the actual value of the piece;
- structure is difficult to follow;
- audience is unclear;
- key point is buried;
- usefulness is too abstract;
- important examples or specifics are missing;
- filler, jargon, repetition, or formulaic prose materially weakens the piece;
- CTA is generic, unnecessary, or disconnected from the content;
- substantial overlap exists with another item in the same supplied series;
- repeated opening/ending pattern makes the series feel formulaic;
- destination/platform conventions are not adequately met.

### `APPROVE`

Use `APPROVE` only when:

1. no block condition exists;
2. every scored dimension is at least `2`;
3. total score is at least `17/21`;
4. no material revision remains necessary.

Do not approve merely because the piece is technically acceptable.

## Scoring

Score each dimension from `0` to `3`.

### Score meaning

`0` = serious quality failure  
`1` = weak; material revision required  
`2` = publication-capable; acceptable  
`3` = strong; clear publication value

Do not award `3` simply because no obvious problem exists.

## Seven Quality Dimensions

### 1. Clarity and Coherence

Check whether the piece is easy to understand and logically organized.

Score `3` when:

- the central point is immediately understandable;
- paragraphs/sections follow a coherent progression;
- references and transitions are clear;
- the ending follows naturally from the body.

Common weaknesses:

- buried thesis;
- abrupt transitions;
- unclear pronouns or referents;
- too many competing ideas;
- conclusion introduces a new argument.

### 2. Specificity and Concreteness

Check whether the writing says something precise rather than relying on vague abstraction.

Score down for:

- generic claims;
- vague nouns such as `things`, `factors`, `aspects`, or `this` without clear referents;
- generic examples;
- unsupported superlatives;
- abstract advice with no concrete meaning.

Specificity must remain evidence-safe. Do not demand invented details merely to increase concreteness.

### 3. Usefulness and Reader Value

Check whether the intended reader gets something worthwhile from the piece.

Possible value includes:

- understanding;
- decision support;
- a practical question;
- a useful distinction;
- a clear implication;
- a framework;
- a memorable evidence-grounded takeaway.

Score down when the draft merely restates information without giving the audience a reason to care.

Do not require a practical recommendation when the evidence does not support one.

### 4. Audience Fit

Check whether the piece is appropriate for the intended reader.

Assess:

- assumed knowledge;
- terminology;
- explanation depth;
- tone;
- relevance;
- reader problem or decision.

A technically strong draft can still score poorly if written for the wrong audience.

If no audience is specified and the content cannot be evaluated responsibly without one, score down and request clarification rather than inventing an audience.

### 5. Voice and Naturalness

Check whether the prose sounds purposeful, human, and consistent with the supplied or established author voice.

Score down for:

- generic AI-style framing;
- repetitive sentence patterns;
- excessive rhetorical signposting;
- artificial enthusiasm;
- canned transitions;
- inflated language;
- unnecessary hedging;
- choppy or mechanical rhythm;
- obvious imitation of a voice without evidence.

Do not use this dimension to encourage detector evasion.

If an author voice profile or prior voice review exists, use it. Do not invent personal voice characteristics.

### 6. Destination and Format Fit

Check whether the piece suits where it will be used.

Examples:

- academic manuscript;
- dissertation;
- internal report;
- email;
- LinkedIn;
- website;
- presentation;
- professional briefing.

Assess only destination constraints that are supplied or known through the active workflow.

Do not invent platform rules.

If no destination is specified and destination materially affects readiness, score conservatively and identify the missing context.

### 7. Distinctiveness and Non-Redundancy

Check whether the piece has a clear reason to exist as a separate item.

Within a single draft, assess:

- repeated ideas;
- duplicated paragraphs;
- repetitive opening/closing construction;
- redundant explanation;
- multiple sections making the same point.

When series context is supplied, also assess:

- substantial overlap with other items;
- repeated hook pattern;
- repeated CTA pattern;
- same insight presented with superficial wording changes.

Do not claim series-level novelty when comparison material was not supplied.

## Opening / Hook Integrity

An opening should earn attention without misrepresenting the content.

A strong opening may be:

- direct;
- intriguing;
- practical;
- surprising;
- question-led;
- evidence-led.

Do not require clickbait.

`BLOCK` if the opening materially misstates evidence or promises a conclusion the body does not support.

`REVISE` if the opening is merely weak, generic, repetitive, or disconnected.

## Ending / CTA Integrity

A CTA is optional unless the destination requires one.

Do not penalize a strong academic or professional ending simply because it lacks a CTA.

Score down when a CTA is:

- generic (`What do you think?`);
- unrelated to the content;
- manipulative;
- repetitive across a series;
- stronger than the evidence;
- included only because a template expects one.

Prefer a natural ending over a forced engagement prompt.

## Generic / Formulaic Prose

Flag formulaic prose when it materially reduces quality.

Examples:

- repeated `This raises an important question`;
- repeated `In today's fast-paced world`;
- empty scene-setting;
- generic motivational closing;
- stacked rhetorical questions;
- repetitive three-part constructions used mechanically;
- excessive em-dash or colon framing;
- paragraph-after-paragraph with identical sentence rhythm;
- generic `key takeaway` language without an actual distinctive takeaway.

Do not reject a phrase merely because AI systems sometimes use it. Judge whether the writing is actually repetitive, generic, or context-poor.

## Jargon and Complexity

Use technical language when the audience and destination require it.

Do not simplify scientific terminology merely to sound conversational.

Flag jargon when:

- it is unnecessary for the audience;
- a simpler phrase preserves the meaning;
- terminology is used without needed explanation;
- abstraction obscures the actual point.

## Evidence-Safe Quality Review

Never improve quality by weakening scientific fidelity.

Do not recommend:

- stronger causal language for impact;
- removing an important limitation merely to make the piece cleaner;
- replacing exact scientific wording with an unsupported relationship synonym;
- turning an inference into a fact;
- inventing a personal anecdote;
- fabricating examples;
- adding unsupported certainty;
- making a claim broader to create a stronger hook.

When quality and evidence fidelity conflict, evidence fidelity wins.

### QA Meta-Text Fidelity Rule

The quality gate's own output must obey the same evidence constraints as the draft.

This applies to:

- score reasons;
- blockers;
- strengths;
- required revisions;
- example replacement wording.

Do not introduce scientific or factual terminology merely to explain the quality judgment.

Examples:

If the draft/source says:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

do not describe this in a score reason as:

- `a correlation`;
- `an association`;
- `a predictive relationship`;
- `a causal effect`;

unless that terminology is explicitly available from the upstream evidence contract.

Prefer neutral wording such as:

`The draft preserves the study finding and its causal limitation.`

Likewise, a required revision must not create a stronger claim than the existing draft or supplied evidence.

Bad headline repair:

`One Habit That Can Improve Coach Coordination`

when no evidence establishes that the practice improves coordination.

Safer repair:

`Using a Weekly Coach Meeting to Support Coordination`

or another scope-accurate headline that does not add a new causal claim.

A quality review is not valid if its own explanations or suggested edits introduce factual drift.

## Minimal-Change Rule

QA should specify the smallest changes necessary to reach publication readiness.

Do not rewrite the entire piece when only two sentences need revision.

For each required revision:

1. identify the location or issue;
2. explain why it matters;
3. specify the smallest required change;
4. preserve already strong material.

If the user asks for a rewrite, specialist writing skills may be used after the gate decision.

## Output Contract

Use this structure:

```yaml
content_quality_gate:
  content_id: null
  destination: null
  audience: null
  upstream_checks:
    factuality:
      required: true
      status: "PASS|BLOCK|NOT_REQUIRED|NOT_RUN"
  blockers: []
  scores:
    clarity_coherence:
      score: 0
      reason: ""
    specificity_concreteness:
      score: 0
      reason: ""
    usefulness_reader_value:
      score: 0
      reason: ""
    audience_fit:
      score: 0
      reason: ""
    voice_naturalness:
      score: 0
      reason: ""
    destination_format_fit:
      score: 0
      reason: ""
    distinctiveness_nonredundancy:
      score: 0
      reason: ""
  total_score: 0
  decision: "APPROVE|REVISE|BLOCK"
  required_revisions: []
  strengths: []
```

## Scoring Consistency

`total_score` must equal the sum of the seven dimension scores.

Maximum:

`21`

Decision logic:

```text
if blocker exists:
    BLOCK
elif any dimension < 2:
    REVISE
elif total_score < 17:
    REVISE
else:
    APPROVE
```

Do not manually override the decision because the draft feels generally good.

## Required Revision Contract

Each required revision should be concise and actionable.

Preferred form:

```yaml
- location: "opening"
  issue: "generic opening"
  smallest_change: "Replace the first two sentences with one direct sentence stating the actual reader problem."
```

Do not include a complete rewrite unless explicitly requested.

For `APPROVE`, `required_revisions` should normally be empty.

For `REVISE`, at least one required revision must identify what prevents approval.

For `BLOCK`, blockers must explain what prevents publication. Ordinary quality revisions may also be listed separately when useful.

All example replacement wording must remain within the factual and causal strength of the supplied content and upstream evidence. If safe replacement wording cannot be given without making a new factual claim, describe the required structural change without drafting new claim language.

## Strengths

Include only real strengths that help explain why the piece is close to or ready for publication.

Avoid generic praise such as:

- `well written`;
- `strong content`;
- `great post`.

Prefer specific observations such as:

- `The central distinction is clear by the end of the first paragraph.`
- `The conclusion returns to the reader decision introduced in the opening.`

Strengths are optional and must not dilute a `BLOCK` or `REVISE` decision.

## Deterministic Validation

After writing the structured gate output to YAML, validate the mechanical parts of the decision.

Recommended temporary path:

`.knowledgecraft/scratch/content-quality-gate.yaml`

Run:

```powershell
py ".opencode/skills/content-quality-gate/scripts/validate_content_quality_gate.py" ".knowledgecraft/scratch/content-quality-gate.yaml"
```

If validation returns `FAIL`:

1. do not report the gate as complete;
2. read every validation error;
3. repair only the affected structural, arithmetic, or decision fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- the seven required quality dimensions;
- score range `0-3`;
- non-empty score reasons;
- total-score arithmetic;
- allowed factuality status values;
- factuality-required consistency;
- blocker precedence;
- factuality `BLOCK` / required `NOT_RUN` precedence;
- mechanical `APPROVE` / `REVISE` / `BLOCK` decision logic;
- required-revision presence for `REVISE`;
- blocker presence for `BLOCK`;
- empty required revisions for `APPROVE`;
- required-revision field structure.

The validator does **not** determine whether a quality score is semantically correct, whether prose is genuinely natural, or whether factual wording is scientifically faithful. Those remain model/reviewer responsibilities governed by this skill and upstream evidence checks.

## Final Review Sequence

Use this order:

1. identify destination and audience;
2. check whether factuality review is required and available;
3. identify block conditions;
4. score all seven dimensions;
5. calculate the total;
6. apply decision logic mechanically;
7. list only the smallest required revisions;
8. verify that recommended changes do not create factual drift;
9. report the final decision.

## Final Checks

Before completing the gate, verify:

- destination identified or missing context explicitly noted? YES
- audience identified or missing context explicitly noted? YES
- factuality prerequisite handled correctly? YES
- all block conditions checked? YES
- all seven dimensions scored 0-3? YES
- score reasons are specific? YES
- total equals sum of seven dimensions? YES
- any score below 2 forces REVISE unless already BLOCK? YES
- total below 17 forces REVISE unless already BLOCK? YES
- blocker forces BLOCK? YES
- required revisions are minimal and actionable? YES
- recommendations preserve evidence fidelity? YES
- score reasons/blockers/strengths avoid invented scientific terminology? YES
- example replacement wording avoids new unsupported factual or causal claims? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- APPROVE contains no unresolved material revision? YES
