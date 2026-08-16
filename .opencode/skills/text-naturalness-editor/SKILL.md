---
name: text-naturalness-editor
description: Conservatively improve drafted prose by removing generic, repetitive, templated, inflated, mechanical, or overly polished phrasing while preserving meaning, factual content, scientific claim strength, and the existing author voice. Use as a pipeline editing component, not as a detector-evasion tool.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "naturalness-editing"
  opencode/slash: "false"
---

# Text Naturalness Editor

Improve the naturalness of an existing draft without changing what it substantively says.

The goal is **clearer, less templated, less mechanical prose that still sounds like the same author and preserves all factual and scientific constraints**.

This is not a detector-evasion skill.

## Responsibility Boundary

`text-naturalness-editor` owns conservative prose-quality editing.

It may improve:

- specificity when supported by existing content;
- cadence and sentence rhythm;
- transitions;
- lexical precision;
- paragraph architecture;
- redundancy;
- mechanical signposting;
- inflated phrasing;
- unnecessary abstraction;
- repetitive syntax;
- repeated rhetorical construction.

It does **not**:

- build or infer an author voice;
- override an author voice profile;
- perform factual verification;
- invent examples, anecdotes, emotions, or experiences;
- strengthen claims;
- add unsupported specificity;
- rewrite scientific relationship language for style;
- optimize text against AI detectors;
- insert typos, hidden characters, deliberate grammar damage, or translation artifacts;
- mechanically ban words or punctuation simply because they are sometimes associated with AI writing.

Related skills:

- `author-voice-profiler` -> models evidence-based author voice;
- `author-voice-editor` -> aligns a draft with that profile;
- `text-humanizer` -> performs protected-span rewriting when broader human-style revision is required;
- `factuality-guard` -> checks factual/evidence fidelity;
- `content-quality-gate` -> final publication-readiness review.

## Pipeline Position

Preferred order when all components are relevant:

```text
author-voice-profiler
        ↓
author-voice-editor
        ↓
text-naturalness-editor
        ↓
text-humanizer (only when needed)
        ↓
factuality-guard / final QA
        ↓
content-quality-gate
```

Do not assume every draft requires every editing stage.

If a draft is already natural, leave it largely unchanged.

## Existing Voice Takes Precedence

Naturalness editing must preserve the existing or profiled author voice.

Do not make prose more conversational, emotional, informal, witty, fragmented, or rhetorical merely because those choices may appear more "human".

If an author voice profile is supplied:

1. preserve high-confidence contextual traits;
2. preserve high-confidence stable traits;
3. do not introduce patterns explicitly marked `avoid_overfitting`;
4. do not treat `not_observed` as prohibited.

If no voice profile is supplied, preserve the draft's existing register and stance rather than inventing one.

## Naturalness Problem Taxonomy

Identify only problems that are materially present.

Use these categories when useful:

- `generic_opening`
- `generic_closing`
- `mechanical_transition`
- `repetitive_sentence_structure`
- `repetitive_rhetorical_pattern`
- `inflated_wording`
- `vague_abstraction`
- `redundant_restating`
- `over_signposting`
- `paragraph_fragmentation`
- `paragraph_overloading`
- `lexical_imprecision`
- `unnecessary_jargon`
- `excessive_hedging`
- `artificial_certainty`
- `forced_cta`
- `formulaic_parallelism`
- `overpolished_cadence`
- `none`

Do not assign a problem merely because a phrase resembles common AI prose.

Judge the passage in context.

## Generic Language Rule

Generic phrasing should be edited when it adds little meaning.

Examples:

- `In today's fast-paced world...`
- `It is important to note that...`
- `At the end of the day...`
- `This highlights the importance of...`
- `There are many different factors that...`
- `This raises an important question...`

These phrases are not automatically forbidden.

Retain them if they genuinely fit the author's voice and serve a real function.

Edit them when they are empty framing, repetitive, or delay the substantive point.

## Specificity Rule

Prefer concrete language over vague abstraction **only when the draft or supplied evidence already contains the necessary detail**.

Good:

`several environmental factors`

→

`feedback, responsibility, and long-term development`

when those details already exist in the draft.

Not allowed:

`support matters`

→

`weekly one-to-one meetings improve athlete confidence`

when that detail or mechanism was never supplied.

Do not invent specificity to make prose feel less generic.

## Lexical Precision Rule

Prefer accurate, simple, domain-appropriate wording over inflated synonyms.

Examples:

`utilize` -> `use` when no technical distinction is lost.

`a multitude of` -> `many` when appropriate.

`facilitate the optimization of` -> a simpler accurate formulation when supported.

Do not simplify technical terms that carry specific scientific meaning.

Do not substitute protected relationship terminology.

## Sentence Rhythm Rule

Improve rhythm when the prose contains an obvious run of identical structures.

Possible edits:

- combine two short sentences;
- split an overloaded sentence;
- vary clause order;
- remove repeated sentence openings;
- shorten a sentence that carries unnecessary framing.

Do not manufacture "burstiness" or artificially alternate sentence lengths according to a formula.

Do not fragment prose simply to make it look less generated.

## Paragraph Architecture Rule

Group ideas according to reasoning, not arbitrary visual rhythm.

Prefer:

- one idea or tightly connected reasoning unit per paragraph;
- paragraph breaks where the reasoning actually shifts;
- short paragraphs when destination/voice supports them.

Avoid:

- one sentence per paragraph as a universal style;
- huge paragraphs containing multiple unrelated ideas;
- breaking scientific qualifications away from the claims they qualify.

Do not move a limitation so far from its claim that meaning changes.

## Transition Rule

Remove or revise transitions that function only as mechanical connectors.

Examples:

- `Furthermore`
- `Moreover`
- `Additionally`
- `In conclusion`
- `It is worth noting`
- `Importantly`

These words are not banned.

Use them when they accurately signal the relationship between ideas.

Prefer natural conceptual continuity over repeated explicit connectors.

## Redundancy Rule

Delete or compress restatement only when no substantive nuance is lost.

Potential redundancy:

```text
The environment matters for development.
This means the developmental environment is important.
```

Do not collapse statements that appear similar but serve different scientific functions, such as:

- finding vs limitation;
- finding vs interpretation;
- interpretation vs recommendation;
- estimate vs uncertainty;
- claim vs qualification.

## Evidence / Interpretation / Recommendation Separation

Preserve the distinction between:

- what was observed;
- what is inferred;
- what may be practically relevant;
- what is recommended.

Naturalness editing must not merge these categories merely to make prose smoother.

Example:

```text
The study found X.
One possible interpretation is Y.
```

must not become:

```text
The study showed Y.
```

## Protected Meaning Rule

Preserve the substantive meaning of the draft.

Do not:

- introduce new claims;
- remove material claims;
- broaden or narrow populations;
- change direction;
- change magnitude;
- change chronology;
- convert uncertainty into certainty;
- convert interpretation into fact;
- convert recommendation into evidence;
- introduce causal language;
- remove a necessary limitation.

When a naturalness improvement conflicts with meaning preservation, preserve meaning.

## Protected Content Rule

Preserve exactly unless explicitly authorized:

- names;
- numbers;
- percentages;
- dates;
- units;
- statistical values;
- quotations;
- citations;
- reference markers;
- source IDs;
- claim IDs;
- instrument/scale names;
- technical constructs;
- legal/regulatory wording;
- code;
- file paths;
- URLs.

Do not alter protected content merely to improve rhythm.

## Scientific Relationship Language Lock

Preserve relationship terminology exactly when scientifically meaningful.

Do not interchange:

- `reported`;
- `associated with`;
- `correlated with`;
- `predicted`;
- `linked to`;
- `related to`;
- `increased`;
- `caused`;
- `co-occurred`.

Example:

```text
Athletes who reported stronger coach support also reported greater perseverance.
```

must not become:

```text
Coach support was associated with perseverance.
```

unless that relationship terminology is explicitly authorized.

## Causal and Uncertainty Lock

Preserve causal status and uncertainty.

Do not change:

`may be relevant`

to:

`is important`

for stronger prose.

Do not change:

`did not establish whether X caused Y`

to:

`X was non-causal`.

Do not remove hedging that is scientifically required.

You may remove hedging that is purely stylistic and redundant only when it does not alter claim strength.

## Citation Attachment Rule

Keep citations attached to the claims they support.

Do not move a citation across sentences in a way that changes what it appears to support.

Do not merge sentences if doing so makes citation scope ambiguous.

## Personal Experience Rule

Do not invent:

- `I think`;
- `I have seen`;
- `in my experience`;
- personal anecdotes;
- emotions;
- memories;
- professional experiences.

First-person language may be retained or adjusted only when already supported by the draft or explicit author instruction.

## Rhetorical Question Rule

Questions are not inherently more natural.

Add or retain them only when:

- they serve a real rhetorical function;
- they fit the author voice/destination;
- they do not replace necessary substantive explanation.

Avoid stacked rhetorical questions and formulaic question endings.

## CTA Rule

A call to action is optional.

Do not automatically add:

- `What do you think?`
- `Agree?`
- `Let me know in the comments.`
- `Share this with someone who needs it.`

Retain or improve a CTA only when the destination and author voice justify it.

Prefer no CTA over a generic engagement prompt.

## Formulaic Pattern Rule

Look for repeated patterns across the current draft and supplied series context.

Examples:

- repeated `We often talk about X as if...`;
- repeated `The question is not X. It is Y.`;
- repeated three-item lists;
- repeated one-sentence hook + rhetorical question + CTA;
- repeated `This matters because...`.

If repetition is already part of a supplied series, vary the framing while preserving the underlying function.

Do not replace one rigid template with another.

## Over-Polishing Rule

Natural writing does not require every sentence to be maximally elegant.

Do not:

- add symmetrical triads everywhere;
- force perfect parallelism;
- eliminate every repetition;
- turn ordinary language into polished slogans;
- make every ending quotable;
- make every paragraph rhetorically complete.

Preserve useful irregularity when it belongs to the author's natural writing.

## Error Rule

Never add errors to create naturalness.

Do not:

- introduce typos;
- remove punctuation randomly;
- create run-on sentences;
- corrupt grammar;
- add invisible Unicode characters;
- use homoglyphs;
- perform translation loops;
- alter capitalization arbitrarily.

Correct obvious accidental errors only when doing so is within the user's editing request and does not affect protected content.

## Detector-Evasion Prohibition

Do not optimize for:

- AI-detector scores;
- perplexity;
- burstiness targets;
- detector thresholds;
- hidden statistical signatures;
- bypassing Turnitin, GPTZero, Originality.ai, or similar systems.

Do not claim an edit is:

- `undetectable`;
- `human-written according to detectors`;
- `safe from AI detection`.

The purpose is prose quality and authentic voice preservation.

## Minimal-Change Principle

Edit the smallest amount necessary.

Use this priority:

### Priority 1 — Meaning-obscuring naturalness problems

Examples:

- vague abstraction;
- overloaded sentence;
- confusing paragraph structure;
- excessive redundancy.

### Priority 2 — Strongly templated or mechanical phrasing

Examples:

- empty opening;
- repeated connectors;
- formulaic conclusion.

### Priority 3 — Rhythm and lexical refinement

Examples:

- repeated syntax;
- inflated wording;
- mild jargon.

### Priority 4 — Cosmetic preference

Usually leave unchanged unless requested.

Do not rewrite already strong prose merely to demonstrate editing.

## Naturalness Audit

Before editing, identify only the largest material issues.

Suggested structure:

```yaml
naturalness_issues:
  - issue_id: "NE-001"
    location: "opening"
    category: "generic_opening"
    severity: "high|medium|low"
    observed_pattern: ""
    proposed_action: "edit|leave"
    reason: ""
```

Not every draft needs an issue in every category.

`none` is a valid outcome.

## Output Contract

Default structured result:

```yaml
text_naturalness_edit:
  draft_id: null
  destination: null
  audience: null
  voice_profile_used: false
  issues:
    - issue_id: "NE-001"
      location: ""
      category: ""
      severity: "high|medium|low"
      observed_pattern: ""
      action: "edit|leave"
      reason: ""
  preservation_checks:
    meaning_preserved: true
    protected_content_preserved: true
    scientific_relationship_language_preserved: true
    causal_strength_preserved: true
    uncertainty_preserved: true
    citation_scope_preserved: true
    personal_experience_invented: false
    unsupported_specificity_added: false
    detector_optimization_used: false
  revised_text: |
    ...
  change_summary:
    - ""
  confidence_note: null
```

## Change Summary

Describe only actual material changes.

Good:

- `Removed generic scene-setting from the opening.`
- `Combined two sentences that repeated the same point.`
- `Varied a run of identical sentence openings.`
- `Kept the relationship wording and causal limitation unchanged.`

Avoid:

- `Made it more human.`
- `Increased burstiness.`
- `Reduced AI patterns.`
- `Made it undetectable.`

## Confidence Note

Include a confidence note when:

- no author voice profile is available and stylistic choices are therefore conservative;
- destination is unknown;
- protected scientific language substantially limits editing;
- the draft is already natural and little change is justified;
- a proposed improvement depends on ambiguous interpretation.

## Preservation Verification

After editing, compare original and revision.

Verify:

- meaning unchanged;
- names unchanged;
- numbers unchanged;
- dates unchanged;
- quotations unchanged;
- citations unchanged and still attached correctly;
- technical terms preserved;
- relationship language preserved;
- causal status preserved;
- uncertainty preserved;
- limitations preserved;
- no personal experience invented;
- no unsupported specificity introduced;
- no detector-evasion technique used.

If any of these fail, repair the edit before returning it.

## Stop / Leave Conditions

Leave a passage unchanged when:

- it is already clear and natural;
- the proposed change is only cosmetic;
- a change would weaken author voice;
- a change would alter scientific precision;
- a change would require inventing specificity;
- the only motivation is that a word or structure "sounds AI-generated";
- profile evidence does not support the change.

## Final Review Sequence

1. load the draft;
2. load voice profile if supplied;
3. identify destination and audience if known;
4. identify protected factual/scientific content;
5. identify the largest material naturalness issues;
6. distinguish genuine problems from stylistic preference;
7. edit minimally;
8. preserve voice/context;
9. compare original vs revision for factual and scientific drift;
10. check for unsupported specificity;
11. check for template replacement or over-polishing;
12. return revised text and compact change summary.

## Final Checks

Before completing the edit, verify:

- author voice preserved? YES
- only material naturalness problems edited? YES
- generic phrasing judged contextually rather than mechanically banned? YES
- specificity added only when supported? YES
- repetitive syntax improved without artificial sentence-length formulas? YES
- paragraph changes preserve reasoning? YES
- evidence / interpretation / recommendation distinctions preserved? YES
- meaning preserved? YES
- names/numbers/dates/citations/quotes preserved? YES
- relationship terminology preserved? YES
- causal strength preserved? YES
- uncertainty and limitations preserved? YES
- citation scope preserved? YES
- no personal experience invented? YES
- no unsupported details invented? YES
- no forced questions or CTA added? YES
- no typos/grammar damage/invisible characters added? YES
- no detector optimization used? YES
- already natural prose left largely unchanged? YES
