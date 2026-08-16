---
name: author-voice-editor
description: Edit an existing draft toward a supplied author voice profile while preserving meaning, facts, numbers, citations, technical terms, claim strength, and evidence constraints. Use when content is substantively correct but does not yet sound like the profiled author.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "voice-editing"
  opencode/slash: "false"
---

# Author Voice Editor

Edit an existing draft toward a supplied author voice profile.

The objective is **voice alignment without factual drift, overfitting, or formulaic imitation**.

## Responsibility Boundary

`author-voice-editor` owns voice alignment of an existing draft.

It does not:

- build the author voice profile;
- invent an author voice when no usable profile exists;
- perform full factual verification;
- strengthen scientific or causal claims;
- humanize text for detector evasion;
- imitate another person's writing;
- intentionally reproduce typos, grammar mistakes, transcription artifacts, or formatting accidents;
- replace a draft's substantive argument with a different one.

Related skills:

- `author-voice-profiler` -> creates the evidence-based voice profile;
- `factuality-guard` -> audits factual/evidence fidelity;
- `text-naturalness-editor` -> improves naturalness after voice alignment when needed;
- `text-humanizer` -> may edit surrounding prose while preserving protected spans;
- `content-quality-gate` -> final publication-readiness review.

## Required Inputs

Prefer:

1. the current draft;
2. a current `author_voice_profile`;
3. destination/genre when known;
4. audience when known;
5. any protected factual/scientific constraints already established upstream.

Default profile location:

`.knowledgecraft/writing/author-voice-profile.yaml`

If no usable voice profile exists:

- do not infer a full author voice from the target draft alone;
- do not silently create a persona;
- report that voice alignment is under-specified;
- recommend `author-voice-profiler`.

A small edit may still be possible when the user provides explicit style instructions, but label that as instruction-based editing rather than evidence-based author-voice matching.

## Profile Precedence

Apply profile evidence in this order:

1. destination/context-specific traits that match the current draft;
2. stable cross-context traits;
3. medium-confidence traits when compatible;
4. low-confidence traits only selectively.

Do not force a cross-context trait over a stronger context-specific pattern.

Example:

If the stable profile says:

`direct openings`

but the academic context profile shows:

`qualified framing before interpretation`

then an academic draft may legitimately retain cautious framing.

## Confidence Use

Use trait confidence conservatively.

### High confidence

May drive clear edits when relevant to the draft.

### Medium confidence

Use selectively, especially when multiple medium-confidence traits point in the same direction.

### Low confidence

Do not make material changes solely to satisfy a low-confidence trait.

Do not treat overall profile confidence as permission to enforce every individual trait strongly.

## Voice Alignment Target

Match **patterns**, not exact sentences.

Prioritize high-impact mismatches such as:

- directness;
- sentence rhythm;
- paragraph length;
- first-person level;
- contraction use;
- question frequency;
- hedging;
- vocabulary/register;
- transition style;
- opening pattern;
- ending/CTA style;
- formatting density.

Do not mechanically reproduce:

- exact recurring phrases;
- identical hooks;
- identical closing constructions;
- identical paragraph lengths;
- repeated rhetorical templates;
- one-off formatting quirks.

## Protected Meaning Rule

The edit must preserve the draft's substantive meaning unless the user explicitly asks for substantive revision.

Do not:

- add a new argument;
- remove a material qualification;
- reverse a position;
- broaden the population;
- narrow the population;
- change direction of a finding;
- change magnitude;
- change chronology;
- change whether a statement is fact, inference, opinion, or proposal.

If voice alignment would require changing meaning, leave the passage unchanged and report the mismatch.

## Protected Content Rule

Preserve exactly unless the user explicitly authorizes change:

- names;
- numbers;
- percentages;
- dates;
- units;
- statistical values;
- quotations;
- citations;
- reference markers;
- technical constructs;
- scale/instrument names;
- legal/regulatory wording;
- code;
- file paths;
- IDs;
- source IDs;
- claim IDs.

Minor punctuation immediately surrounding protected material may change only when doing so does not alter the protected content or citation attachment.

## Scientific and Relationship Language Lock

When the draft contains scientific or evidence-grounded language, preserve relationship strength.

Do not substitute among terms such as:

- `reported`;
- `associated with`;
- `correlated with`;
- `predicted`;
- `increased`;
- `caused`;
- `linked to`;
- `related to`;
- `co-occurred`.

These are not interchangeable for voice purposes.

If the grounded wording uses:

`athletes who reported X also reported Y`

do not rewrite it as:

`X was associated with Y`

unless that terminology is explicitly authorized by the evidence contract.

## Causal and Uncertainty Lock

Preserve:

- causal status;
- uncertainty;
- hedging required by evidence;
- limitations;
- conditional language.

Do not change:

`may be relevant`

to:

`is important`

merely because the author profile favors directness.

Do not change:

`the study did not establish whether X caused Y`

to:

`X was non-causal`.

Voice should adapt around the scientific constraint, not replace it.

## First-Person Rule

Match first-person use only where supported by the relevant context profile.

Do not insert:

- `I think`;
- `in my experience`;
- `we know`;
- `I have seen`;
- personal anecdotes;

unless the draft/user/source already supports those statements.

A profile showing that the author sometimes uses first person does not authorize fabricated personal experience.

## Contraction Rule

Contractions may be adjusted when supported by context.

Examples:

`I have` -> `I've`

`do not` -> `don't`

Only do this when:

- the relevant profile supports contractions;
- the destination permits them;
- the change does not occur inside protected text or quotations.

Do not force contractions into academic or formal contexts merely because they appear in email samples.

## Question Rule

Use rhetorical or reflective questions only when profile evidence supports them for the relevant context.

Do not add questions merely to make prose seem more human.

Do not convert every insight into a question.

If the profile shows questions as occasional rather than stable, preserve selectivity.

## Recurring Language Rule

Recurring language from the profile is evidence of **function**, not a phrase bank.

Example profile observation:

`often shifts from evidence to practice using a direct reflective question`

Good alignment:

Use a context-appropriate transition from evidence to a practical question.

Bad alignment:

Repeatedly insert:

`For coaches, the useful question is...`

Do not make future writing more repetitive than the original samples.

## Avoided / Uncertain Traits Rule

Respect explicit profile guidance such as:

- `avoid_overfitting`;
- `not_observed`;
- `uncertain`;
- `contradicted`.

Do not convert `not_observed` into a prohibition.

Example:

`emoji: not_observed`

does not mean:

`remove all emoji`

unless the user or profile explicitly says they should be avoided.

## Error Preservation Rule

Never reproduce errors simply because they occurred in genuine samples.

Do not imitate:

- misspellings;
- malformed grammar;
- accidental duplication;
- mojibake;
- OCR artifacts;
- accidental capitalization;
- transcription noise.

Correct obvious errors only when editing them does not change meaning and the user has asked for editing rather than strict transcription.

## Minimal-Change Principle

Change only what materially improves voice alignment.

Prefer:

`largest evidence-backed mismatch first`

over:

`rewrite every sentence`.

A good voice edit often leaves substantial portions untouched.

Do not degrade already well-aligned prose merely to demonstrate that editing occurred.

## Edit Priority

Use this sequence:

### Priority 1 — High-confidence contextual mismatch

Examples:

- academic draft is overly conversational despite strong academic profile evidence;
- email is unnecessarily formal despite strong email profile evidence.

### Priority 2 — High-confidence stable mismatch

Examples:

- long scene-setting where the author consistently opens directly;
- dense paragraphing where short paragraphing is strongly supported.

### Priority 3 — Medium-confidence refinement

Examples:

- modest contraction adjustment;
- selective question use;
- transition style.

### Priority 4 — Low-confidence / cosmetic differences

Usually leave unchanged unless the user asks for stronger stylistic matching.

## No Voice Inflation

Do not exaggerate the author's patterns.

If the profile says:

`questions: occasional`

do not make the edited draft question-heavy.

If the profile says:

`short paragraphs`

do not turn every sentence into a standalone paragraph.

If the profile says:

`direct`

do not make the prose abrupt or aggressive.

The target is resemblance, not caricature.

## Destination Awareness

Apply voice within the destination.

The same author may legitimately write differently in:

- academic manuscripts;
- dissertation chapters;
- LinkedIn posts;
- email;
- internal reports;
- websites.

Do not make all destinations converge into one generalized voice.

If destination is unknown and context affects major voice choices:

- make only stable high-confidence edits;
- avoid context-dependent changes;
- report the limitation.

## Audience Awareness

Voice alignment must not reduce comprehension for the intended audience.

Do not preserve technical density merely because it appears in academic samples when editing for a general audience.

Do not oversimplify specialist terminology when the audience requires it.

When audience and profile pressure conflict, preserve meaning and reader comprehension.

## Voice Mismatch Audit

Before editing, identify the largest evidence-backed mismatches.

Use a compact internal or structured audit:

```yaml
voice_mismatches:
  - mismatch_id: "VM-001"
    location: "opening"
    observed_draft_pattern: ""
    target_profile_pattern: ""
    profile_scope: "stable|context:<name>"
    trait_confidence: "high|medium|low"
    supporting_sample_ids: []
    action: "edit|leave"
    reason: ""
```

Do not invent supporting sample IDs. Use only IDs present in the supplied profile.

Not every profile trait must produce a mismatch.

## Output Contract

Default structured result:

```yaml
author_voice_edit:
  draft_id: null
  destination: null
  audience: null
  profile_id: null
  profile_confidence: null
  context_profile_used: null
  mismatches:
    - mismatch_id: "VM-001"
      location: ""
      observed_draft_pattern: ""
      target_profile_pattern: ""
      profile_scope: ""
      trait_confidence: "high|medium|low"
      supporting_sample_ids: []
      action: "edit|leave"
      reason: ""
  preservation_checks:
    meaning_preserved: true
    protected_content_preserved: true
    causal_strength_preserved: true
    uncertainty_preserved: true
    personal_experience_invented: false
    exact_phrase_overfitting_detected: false
  revised_text: |
    ...
  change_summary:
    - ""
  confidence_note: null
```

## Change Summary

Keep the change summary brief.

Describe functions rather than praising the output.

Examples:

- `Shortened the opening to match the profile's direct LinkedIn pattern.`
- `Split one dense paragraph because short LinkedIn paragraphs are strongly supported.`
- `Kept the scientific relationship wording unchanged despite surrounding voice edits.`

Do not say:

- `made it more human`;
- `made it undetectable`;
- `perfectly matched the author`;
- `100% authentic`.

## Confidence Note

Include a confidence note when:

- profile confidence is provisional/moderate;
- destination has little profile coverage;
- major relevant traits are low-confidence;
- the draft is already well aligned and little editing is justified;
- protected scientific text constrains voice matching.

A confidence note is optional when strong profile evidence directly covers the destination.

## Preservation Verification

After editing, compare draft and revision.

Verify explicitly:

- names unchanged;
- numbers unchanged;
- dates unchanged;
- quotations unchanged;
- citations unchanged;
- technical terms unchanged unless explicitly authorized;
- relationship language unchanged where protected;
- causal status unchanged;
- uncertainty/limitations preserved;
- no personal experience invented;
- no new substantive claims introduced.

If any protected change is necessary, do not silently make it. Report it for user decision.

## Failure / Stop Conditions

Do not perform evidence-based voice alignment when:

- no usable profile exists;
- profile authorship basis is materially uncertain;
- target destination requires context not represented and stable traits are insufficient;
- requested imitation is of a different real person;
- required edits would alter protected meaning.

In those cases, explain the limitation and make only safe changes explicitly authorized by the user.

## Final Review Sequence

1. load the draft;
2. load the author voice profile;
3. identify destination and audience;
4. select matching context profile;
5. identify protected content and scientific wording;
6. identify largest evidence-backed voice mismatches;
7. prioritize high-confidence contextual/stable traits;
8. edit minimally;
9. compare original vs revision for protected-content drift;
10. check for phrase/template overfitting;
11. produce revised text and compact change summary;
12. add confidence note when warranted.

## Final Checks

Before completing the edit, verify:

- usable voice profile loaded? YES
- relevant context profile selected when available? YES
- only evidence-backed traits drove edits? YES
- low-confidence traits were not over-enforced? YES
- stable/context precedence handled correctly? YES
- meaning preserved? YES
- names/numbers/dates/citations/quotes preserved? YES
- scientific relationship language preserved? YES
- causal status preserved? YES
- uncertainty and limitations preserved? YES
- no personal experience invented? YES
- recurring phrases not turned into templates? YES
- typos/artifacts not imitated? YES
- already aligned text left alone where appropriate? YES
- destination differences respected? YES
- change summary describes actual edits only? YES
