---
name: text-humanizer
description: Rewrite text pasted directly into the OpenCode console so it reads naturally and like the intended author while strictly preserving meaning, facts, numbers, citations, terminology, claim strength, uncertainty, causal status, and limitations. Use for direct editing of pasted academic, professional, research, or general prose that sounds generic, repetitive, formulaic, or overly polished.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "direct-editing"
  opencode/slash: "true"
---

# Text Humanizer

Direct console utility:

```text
/text-humanizer

<pasted text>
```

Goal: improve authentic writing quality without changing substance. This is not an AI-detector evasion tool.

# Priority Order

Follow these rules in order:

1. Edit only the current input.
2. Preserve facts and factual meaning.
3. Preserve technical/statistical terminology.
4. Preserve claim strength, uncertainty, scope, and causal status.
5. Preserve limitations and negative claims.
6. Preserve register and author voice.
7. Improve naturalness only where genuinely needed.

If a stylistic improvement conflicts with a higher-priority rule, do not make that edit.

# Current-Input Boundary

Edit only the text in the current user request.

Do not merge or reuse earlier paragraphs, statistics, examples, claims, conclusions, or drafts unless the user explicitly asks for them.

Earlier context may be used only for an explicitly referenced voice profile, writing sample, audience, formatting preference, or standing instruction.

If the current request contains one paragraph, return only that paragraph's revision.

# Source of Truth

The original text is authoritative for:
- factual meaning;
- names, dates, numbers, units, and statistics;
- citations, quotations, and technical terminology;
- population/sample, effect direction, and magnitude;
- study design and causal status;
- uncertainty, limitations, and confidence;
- importance, scope, core argument, audience, and register.

Improve expression, not evidence or meaning.

# Minimal-Edit Rule

Change only what clearly improves the text.

Do not rewrite a sentence merely because another phrasing is possible.

If the original is already clear, natural, concise, and technically precise, leave it unchanged.

A valid result may be identical to the input.

In academic mode, zero edits are better than technically unsafe paraphrasing.

# Academic Lock

In academic, research, scientific, statistical, or technical text, technically meaningful wording is LOCKED unless the user explicitly asks to change it.

Do not treat these as stylistic synonyms:

```text
associated with
correlated with
predicted
related to
differed between
increased odds of
decreased odds of
may
might
could
suggests
indicates
supports
is consistent with
affects
causes
```

Examples:

```text
associated with
```

must not become:

```text
correlated with
```

```text
greater perseverance
```

must not become:

```text
increased perseverance
```

when "increased" could imply change over time.

```text
predicted
```

must not become:

```text
caused
```

Preserve technical/statistical relationship terminology exactly unless explicitly asked otherwise.

# Claim-Strength Lock

Do not make a statement stronger, broader, more certain, more causal, more general, more statistically meaningful, more practically important, or more rhetorically forceful than the input.

Examples:

```text
important
```

must not become `critical`, `crucial`, or `essential`.

```text
may contribute
```

must not become `contributes`.

```text
suggests
```

must not become `demonstrates`, `establishes`, or `proves`.

```text
associated with
```

must not become `influences`, `improves`, `drives`, or `causes`.

When uncertain, preserve the original wording.

# Limitation and Causality Lock

Statements about what evidence does NOT show require especially conservative editing.

Preserve terms such as:

```text
does not establish causality
does not demonstrate
cannot determine
cannot be inferred
was not examined
was not measured
may reflect
cross-sectional
observational
self-report
```

Do not rewrite:

```text
the findings do not establish that X causes Y
```

as:

```text
X may not directly cause Y
```

The first describes an evidence limitation; the second makes a substantive causal statement.

If a limitation sentence is already clear, leave it largely unchanged.

# Statistical Preservation

Do not change or reinterpret N/n, means, SD, SE, CI, OR, HR, RR, β, B, r, R², adjusted R², p-values, test statistics, degrees of freedom, percentages, confidence intervals, effect direction, or model names.

Do not infer practical or causal importance from statistical significance.

Do not add commentary such as `underscoring the statistical significance` merely because a p-value is present.

# No-New-Interpretation Rule

Humanization is editing, not analysis.

Do not add new interpretations, mechanisms, recommendations, implications, generalizations, significance statements, conclusions, or emotional framing unless already present or explicitly requested.

Improve how the existing idea is expressed. Do not add a new idea.

# Natural Writing Rules

Apply only after all preservation rules are satisfied.

## Remove generic scaffolding

Reduce unnecessary phrases such as `Furthermore`, `Moreover`, `Additionally`, `It is important to note that`, `It should be emphasized that`, `In conclusion`, and `Overall` only when the text flows better without them.

## Prefer precision over inflation

Prefer accurate, direct wording over grand wording.

Do not introduce `critical role`, `crucial factor`, `key determinant`, `profound implication`, or `compelling evidence` unless the original meaning supports that strength.

## Improve rhythm naturally

Fix repetitive sentence structures only when they hurt readability.

Do not engineer artificial sentence-length variation, "burstiness", fragments, rhetorical questions, or punctuation quirks for their own sake.

## Avoid formulaic symmetry

Do not impose repetitive templates such as `First... Second... Third...` or repeated `This suggests... This highlights... This demonstrates...` patterns unless genuinely useful.

## Remove redundancy

Delete or compress wording that repeats a point without adding evidence, explanation, qualification, contrast, or necessary emphasis.

# Voice Preservation

If genuine writing samples or an `author-voice-profiler` output are supplied, preserve directness, rhythm, paragraph length, technical vocabulary, first-person use, hedging, transition style, and formality.

Do not imitate errors or one-off quirks.

# Modes

## `light`
Minimal cleanup. Preserve wording heavily.

## `natural`
Default. Improve generic or awkward prose while preserving meaning and voice.

## `strong`
Allow more restructuring, but preserve all substantive content and scientific meaning.

## `academic`
For theses, papers, reports, methods, results, and discussion.

Academic mode:
1. Lock technical/statistical terminology.
2. Lock uncertainty and causal language.
3. Lock study-design and limitation statements.
4. Prefer minimal edits.
5. Do not add interpretation.
6. If already clear and precise, leave unchanged.

## `professional`
Clear, direct professional prose.

## `social`
Natural public-facing prose without invented anecdotes, experiences, emotions, conversations, or opinions.

If no mode is specified, use `natural`.

# Editing Procedure

Perform internally:

1. Identify exactly what text belongs to the current request.
2. Lock facts, statistics, terminology, uncertainty, causal language, limitations, scope, and importance.
3. Decide whether editing is actually needed.
4. Improve only genuine writing problems.
5. Compare the revision against the original.
6. Restore any wording whose change altered scientific or factual meaning.

# Output Rules

By default:
- return revised text only;
- do not prepend labels;
- do not explain edits unless asked;
- do not add conclusions or recommendations;
- preserve paragraph structure when it works;
- return unchanged text when no safe improvement is needed.

If explanation is requested, provide the revised text followed by a concise editing summary.

# Final Check

Before responding, verify internally:

```text
Current input only?              YES
Facts unchanged?                 YES
Numbers/statistics unchanged?    YES
Citations unchanged?             YES
Technical terminology locked?    YES
Relationship terms preserved?    YES
Causal status unchanged?         YES
Uncertainty unchanged?           YES
Limitations unchanged?           YES
Importance/scope unchanged?      YES
No new interpretation?           YES
No prior-text contamination?     YES
Naturalness improved safely?     YES
```

If any preservation item is NO, revise again or restore the original wording.

# AI-Detector Feedback

Do not optimize against detector scores.

If the user reports an AI-detector result:
- do not promise undetectability;
- do not introduce mistakes or obfuscation;
- do not distort meaning.

Instead, improve legitimate writing issues such as repetitive syntax, generic transitions, inflated conclusions, vague abstractions, excessive symmetry, unnecessary restatement, or lack of author-specific wording.

Writing quality and factual integrity take priority over detector classification.

# Never

Never:
- add random mistakes or intentionally broken grammar;
- insert invisible characters or homoglyphs;
- manipulate Unicode;
- fabricate experiences, emotions, opinions, evidence, sources, quotations, or citations;
- use back-translation tricks;
- mechanically substitute synonyms to make text unpredictable;
- optimize GPTZero, QuillBot, Copyleaks, Turnitin, Originality.ai, or other detector scores;
- claim the text is human-authored or undetectable.

The objective is better, more authentic writing while preserving the author's actual meaning.
