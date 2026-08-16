---
name: author-voice-profiler
description: Build a reusable, evidence-traceable author voice profile from genuine writing samples such as posts, emails, notes, articles, or transcripts. Use when repeated writing should consistently sound like a real author rather than a generic persona.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "voice-modeling"
  opencode/slash: "false"
---

# Author Voice Profiler

Build a reusable author voice profile from genuine supplied writing.

The profile should describe **how the author tends to write**, not invent who the author is.

## Responsibility Boundary

`author-voice-profiler` owns voice observation and profiling.

It does not:

- rewrite a target draft;
- humanize text;
- imitate another person;
- infer personality, intelligence, values, demographics, or identity from style;
- decide whether factual claims are true;
- turn isolated quirks into permanent voice rules.

Downstream skills may use the profile:

- `author-voice-editor` -> align a draft with the profiled voice;
- `text-naturalness-editor` -> improve naturalness without erasing voice;
- `text-humanizer` -> edit surrounding prose while preserving protected factual/scientific spans.

## Input Requirements

Use only genuine supplied samples that are reasonably attributable to the author.

Suitable samples include:

- posts;
- emails;
- notes;
- articles;
- reports;
- manuscript prose;
- transcripts of the author's own speech;
- other first-party writing.

Do not treat these as author voice evidence unless the user explicitly confirms authorship:

- quotations;
- copied passages;
- templates;
- AI-generated drafts;
- collaborative text with unknown authorship;
- pasted source material;
- text written on behalf of another person.

If authorship is mixed or uncertain, mark the affected sample as `uncertain` and exclude it from high-confidence trait inference.

## Sample Sufficiency

Use these overall profile-confidence bands:

- fewer than 3 substantial genuine samples -> `provisional`;
- 3-7 substantial genuine samples -> `moderate`;
- 8-20 substantial genuine samples -> `strong`;
- more than 20 -> still `strong`; additional samples improve coverage rather than creating a higher label.

Do not treat sample count alone as proof of a trait.

A trait can still have lower confidence when evidence is sparse, inconsistent, genre-specific, or concentrated in one sample.

## Sample Inventory

Assign stable sample IDs:

`VOICE-S001`, `VOICE-S002`, ...

For each sample record:

- sample ID;
- source label or filename if available;
- genre/destination;
- approximate length;
- authorship status: `confirmed|probable|uncertain`;
- whether it is eligible for trait inference;
- notable context.

Do not modify the original samples.

## Core Principle: Evidence Before Persona

Every meaningful voice trait must be grounded in observed sample evidence.

Prefer descriptions such as:

- `usually opens directly with the subject`;
- `often uses short standalone paragraphs in LinkedIn posts`;
- `uses first person sparingly in academic prose`;
- `frequently uses questions to shift from evidence to practice`.

Avoid unsupported persona statements such as:

- `confident leader`;
- `warm personality`;
- `analytical thinker`;
- `naturally persuasive`;
- `humble`;
- `authoritative`.

Those may be impressions, but they are not reliable voice traits unless converted into observable textual behavior.

## Stable Trait vs Context Trait

Do not force all writing into one universal style.

Separate:

### Stable traits

Patterns that recur across multiple genres or contexts.

Examples:

- direct openings;
- moderate sentence length;
- low emoji use;
- preference for concrete nouns;
- restrained emotional language.

### Context-dependent traits

Patterns that clearly change by destination or genre.

Examples:

- academic writing uses more hedging;
- LinkedIn uses shorter paragraphs;
- email uses contractions more often;
- reports use headings and compact lists.

If the author has different legitimate modes, represent them explicitly instead of averaging them into a vague compromise voice.

## Trait Families

Profile only traits supported by the samples.

Candidate families include:

### Register and Directness

- formality;
- directness;
- conversational vs technical register;
- degree of rhetorical framing;
- explicitness of claims.

### Syntax and Rhythm

- sentence-length tendency;
- sentence-length variation;
- simple vs layered syntax;
- fragments;
- rhetorical questions;
- sentence-opening patterns;
- rhythm and pacing.

### Paragraphing and Structure

- paragraph length;
- use of standalone lines;
- sectioning;
- lists;
- transitions;
- opening style;
- ending style.

### Person and Stance

- first-person singular;
- first-person plural;
- second person;
- impersonal constructions;
- hedging;
- certainty;
- qualification;
- reflective framing.

### Lexical Preferences

- domain vocabulary;
- plain vs abstract wording;
- recurring connectors;
- preferred verbs;
- repeated phrases;
- jargon density;
- common contrast structures.

### Punctuation and Formatting

- commas;
- semicolons;
- colons;
- em dashes;
- parentheses;
- bullets;
- bolding;
- capitalization;
- emoji.

### Rhetorical Devices

- questions;
- contrasts;
- examples;
- analogies;
- storytelling;
- repetition;
- triads;
- callbacks;
- calls to action.

### Emotional and Interpersonal Tone

Describe only observable textual intensity and interpersonal style.

Examples:

- restrained enthusiasm;
- frequent appreciation language in email;
- low emotional intensity in academic prose.

Do not convert this into personality inference.

## Trait Evidence Rule

For every high-impact trait, record:

- trait;
- observed pattern;
- confidence;
- supporting sample IDs;
- counterexample sample IDs when relevant;
- context scope;
- evidence note.

High-impact traits include anything downstream editors are likely to enforce strongly, such as:

- directness;
- paragraphing;
- sentence rhythm;
- first-person use;
- question frequency;
- hedging;
- CTA behavior;
- punctuation habits;
- recurring framing patterns.

Do not mark a high-impact trait `high` confidence based on one sample.

## Confidence Per Trait

Use:

- `high`
- `medium`
- `low`

Interpretation:

### High

Repeated, clear pattern across several eligible samples with little meaningful contradiction.

### Medium

Pattern appears multiple times but is context-dependent, uneven, or supported by a smaller sample base.

### Low

Tentative pattern, limited evidence, or meaningful counterexamples.

Confidence refers to **confidence that the trait characterizes the author's writing**, not whether the style is good.

## Counterexample Rule

Actively look for counterexamples.

If a proposed trait is:

`Author avoids rhetorical questions`

but several supplied samples contain them, the trait must be revised or rejected.

If a trait holds only in one genre, scope it to that genre.

Do not hide contradictory samples merely to produce a cleaner profile.

## Absence Is Not Avoidance

Do not infer a strong negative preference merely because something is absent.

For example:

- no emoji in three academic samples does not prove `author avoids emoji`;
- no humor in a report does not prove `author never uses humor`;
- no first-person singular in one article does not prove `author avoids I`.

Use `not_observed` when appropriate.

Use `avoids` only when the broader sample set provides meaningful evidence of consistent avoidance or the author explicitly states the preference.

## Error and Artifact Filtering

Do not encode as voice:

- typos;
- spelling mistakes;
- accidental grammar errors;
- OCR corruption;
- mojibake;
- unfinished sentences caused by transcription;
- duplicated text;
- formatting artifacts;
- citation formatting imposed by a journal;
- one-off platform constraints.

If an unusual feature might be intentional, keep it low-confidence unless it recurs.

## Recurring Phrase Rule

Recurring phrases can be useful evidence, but do not turn the profile into a phrase-copying template.

Record recurring language as one of:

- `recurring`;
- `occasional`;
- `not_stable`.

Downstream editors should preserve the **pattern or function** where possible, not mechanically reuse the exact phrase.

Example:

Observed:
`For coaches, the useful question is...`

Profile:
`often shifts from evidence to practice using a direct reflective question`

Not:
`always write "For coaches, the useful question is..."`

This prevents formulaic imitation.

## Genre Balance Rule

Do not let one dominant genre erase the others.

If 15 LinkedIn posts and 2 academic passages are supplied:

- LinkedIn traits may have strong support for LinkedIn;
- academic traits remain lower-confidence;
- do not apply LinkedIn paragraphing rules to academic prose.

Report coverage by genre.

## Temporal Drift

If samples span a meaningful period and the style appears to change:

- do not silently average old and new writing;
- identify a possible temporal shift;
- prefer recent samples only if the user asks for current voice or if the task explicitly targets the current style;
- otherwise preserve the distinction.

Do not call a change `improvement` unless the user frames it that way.

## Output Location

Default generated profile:

`.knowledgecraft/writing/author-voice-profile.yaml`

Optional human-readable companion:

`.knowledgecraft/writing/author-voice-profile.md`

Never write generated profile artifacts into `.opencode/skills/`.

## Output Contract

Use this YAML structure:

```yaml
author_voice_profile:
  profile_id: "VOICE-P001"
  profile_confidence: "provisional|moderate|strong"
  sample_count:
    total: 0
    eligible: 0
    uncertain: 0
  coverage:
    genres: []
    notes: []
  samples:
    - sample_id: "VOICE-S001"
      label: null
      genre: null
      approximate_length: null
      authorship: "confirmed|probable|uncertain"
      eligible_for_inference: true
      notes: null
  stable_traits:
    - trait: ""
      pattern: ""
      confidence: "high|medium|low"
      supporting_sample_ids: []
      counterexample_sample_ids: []
      context_scope: "cross-context"
      evidence_note: ""
  context_profiles:
    - context: ""
      confidence: "high|medium|low"
      traits:
        - trait: ""
          pattern: ""
          confidence: "high|medium|low"
          supporting_sample_ids: []
          counterexample_sample_ids: []
          evidence_note: ""
  recurring_language:
    - expression_or_pattern: ""
      stability: "recurring|occasional|not_stable"
      supporting_sample_ids: []
      usage_note: ""
  not_observed_or_uncertain:
    - feature: ""
      status: "not_observed|uncertain|contradicted"
      note: ""
  downstream_guidance:
    preserve:
      - ""
    use_selectively:
      - ""
    avoid_overfitting:
      - ""
  limitations:
    - ""
```

## Downstream Guidance

The profile should end with practical editing guidance.

### `preserve`

Only high-confidence traits that are safe to maintain across the relevant scope.

### `use_selectively`

Medium-confidence or context-specific traits.

### `avoid_overfitting`

Features that should not become rigid templates.

Typical examples:

- exact recurring phrases;
- identical opening formulas;
- identical paragraph lengths;
- forced questions;
- forced contractions;
- deliberate reproduction of typos.

## Minimal Inference Rule

When evidence is insufficient:

say:

`insufficient evidence`

or:

`not observed in supplied samples`

rather than guessing.

The profiler should be useful because it is selective, not because it fills every possible trait field.

## Deterministic Validation

After writing the structured profile YAML, validate its mechanical consistency.

Run:

```powershell
py ".opencode/skills/author-voice-profiler/scripts/validate_author_voice_profile.py" ".knowledgecraft/writing/author-voice-profile.yaml"
```

If validation returns `FAIL`:

1. do not report the profile as complete;
2. read every validation error;
3. repair only the affected structural, count, confidence, or traceability fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- sample-ID format and uniqueness;
- sample-count arithmetic;
- eligible and uncertain sample counts;
- overall profile-confidence band from eligible sample count;
- allowed authorship/confidence/status values;
- supporting/counterexample sample IDs exist;
- high-confidence traits have at least two supporting samples;
- high-confidence traits do not rely on uncertain-authorship or ineligible samples;
- recurring-language stability values;
- downstream-guidance structure;
- limitations structure.

The validator does **not** decide whether a stylistic observation is semantically correct, whether a sample is truly substantial, whether a phrase is genuinely characteristic, or whether a trait should be stable versus context-specific. Those remain profiler/reviewer responsibilities.

## Final Review Sequence

1. inventory samples;
2. assess authorship eligibility;
3. classify genre/context;
4. assess overall sample sufficiency;
5. identify candidate recurring traits;
6. search for counterexamples;
7. separate stable from context-specific traits;
8. assign trait confidence;
9. identify recurring language without turning it into templates;
10. record unknowns and limitations;
11. produce downstream guidance;
12. save the profile under `.knowledgecraft/writing/`.

## Final Checks

Before completing the profile, verify:

- only genuine/eligible samples influenced high-confidence traits? YES
- sample IDs assigned consistently? YES
- overall profile confidence matches sample sufficiency? YES
- high-impact traits include supporting sample IDs? YES
- counterexamples considered? YES
- genre-specific traits are scoped correctly? YES
- absence was not incorrectly turned into avoidance? YES
- personality assumptions excluded? YES
- typos/artifacts excluded from voice? YES
- recurring phrases were not converted into mandatory templates? YES
- limitations and uncertainty reported? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- generated artifacts saved outside `.opencode/skills/`? YES
