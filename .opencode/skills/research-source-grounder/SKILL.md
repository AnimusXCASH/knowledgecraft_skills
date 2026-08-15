---
name: research-source-grounder
description: Convert research papers, reports, notes, transcripts, or other source material into a strict, traceable source card and claim ledger using only information explicitly supported by the source. Preserve exact statistical relationship terminology, uncertainty, causal status, limitations, source wording, compound-claim structure, schema consistency, and technical wording. Use before synthesis, applied translation, or content drafting when factual grounding matters.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "grounding"
  opencode/slash: "true"
---

# Research Source Grounder

Create a compact, reusable evidence base from supplied source material.

Default mode is **STRICT SOURCE-ONLY GROUNDING**.

This skill extracts and structures source-supported information. It is not for adding methodological commentary, interpretations, recommendations, or plausible missing details.

# Priority Order

Follow these rules in order:

1. Use only information explicitly supported by the supplied source.
2. Preserve source wording when that wording carries scientific meaning.
3. Preserve exact scientific/statistical relationship terminology.
4. Preserve causal status, uncertainty, scope, and limitations.
5. Preserve the logical structure of compound claims.
6. Follow `references/source-contract.yaml` exactly.
7. Separate source facts from any explicitly requested inference.
8. Do not add unstated methods, measures, limitations, mechanisms, or implications.
9. Use the deterministic source-ID helper when no registered source ID is supplied.
10. Never overwrite an existing grounded source artifact.
11. Save outputs only under `.knowledgecraft/research/grounded/`.
12. Prefer omission over inference.
13. Prefer `Not stated in source` over guessing.

If a statement is not supported by the source, do not add it.

# Default Mode: STRICT

Unless the user explicitly asks for interpretation, critique, methodological commentary, or inference:

- produce zero model-generated interpretations;
- produce zero model-generated limitations;
- produce zero model-generated mechanisms;
- produce zero model-generated practical implications;
- produce zero model-generated recommendations.

The default grounded evidence base contains source-supported material only.

# Source-Only Rule

Treat the supplied source as authoritative.

Do not silently add:
- unstated study design details;
- unstated instruments;
- unstated measures;
- unstated sample characteristics;
- unstated recruitment details;
- unstated statistical methods;
- unstated controls or covariates;
- unstated confounders;
- unstated limitations;
- unstated mechanisms;
- unstated theoretical interpretations;
- unstated practical implications;
- unstated recommendations.

If the source says `self-report data`, do not write `self-report survey`, `questionnaire`, or similar wording unless explicitly stated.

A reasonable methodological observation is still not a source fact.

# Do Not Infer Measurement Method From Ordinary Language

Do not infer a measurement or data-collection method merely from ordinary verbs such as `reported`, `rated`, `described`, `indicated`, `showed`, or `stated`.

For example, `Athletes reported greater consistency of effort.` does not by itself authorize `self-report data`, `self-report measure`, `questionnaire`, or `survey`.

Only describe data as self-report when the supplied source explicitly states that the data or measure was self-report.

# No Automatic Interpretation

Do not create an `Interpretations` section by default.

If the source itself contains an interpretation, preserve it as a source-derived claim.

If the user explicitly asks for model interpretation, place it in a separate section titled `Model Inference - Not Source-Derived` and label every model-generated item:

```yaml
claim_type: inference
allowed_for_reuse: false
```

Never mix model inference into the source summary, key findings, stated limitations, source-derived causal guard, or reusable fact ledger.

# Exact Relationship-Language Lock

Scientific and statistical relationship terms are not stylistic synonyms.

If the source says `associated with`, preserve `associated with`.

Do not replace it with `correlated with`, `linked to`, `related to`, `predicted`, or similar wording merely for style.

Likewise, `greater perseverance` must not become `increased perseverance` when `increased` could imply change over time.

# Ordinary Descriptive Relationship Wording

Not every source statement contains a named statistical relationship.

If the source says:

`Athletes who reported stronger developmental support also reported greater consistency of effort.`

do not convert this into `Developmental support was associated with consistency of effort.` or `Developmental support correlated with consistency of effort.` unless the source explicitly uses that terminology.

Preserve the ordinary source construction when no technical relationship term is supplied.

# Causality Lock

Do not strengthen non-causal evidence into causal claims.

Never turn `associated with` into `caused`, `led to`, `improved`, `increased`, `produced`, `resulted in`, or `drove` unless the source explicitly supports that causal claim.

# Causal Non-Establishment Rule

Absence of causal evidence is not evidence that no causal relationship exists.

If a source states `did not determine whether X caused Y`, `did not test whether X caused Y`, `does not establish causality`, `cannot establish causality`, or `causal interpretation is limited`, do not rewrite this as `X is non-causal`, `the relationship is non-causal`, `X does not cause Y`, or `there is no causal relationship`.

Prefer `The source does not establish that X causes Y.` or preserve the source wording directly.

# Causal Status Field

## Causal Status Applicability Rule

Use `causal_status: not-applicable` for claims that do not make a substantive relationship or effect statement.

This normally includes:

- sample size or sample description;
- study duration;
- study location or setting;
- source metadata;
- descriptive methodological statements that do not assert an effect or relationship.

Example:

`A prospective study followed 146 youth athletes for six months.`

should use:

`causal_status: not-applicable`

Do not assign `not-established` merely because the overall study does not establish causality.

Use `not-established` for substantive findings or limitations where the source explicitly states or indicates that causal interpretation was not established, tested, or determined.

Allowed values:

```text
causal
non-causal
not-established
not-applicable
unclear
```

Use `causal` only when the source explicitly supports a causal claim.

Use `non-causal` when the claim itself is explicitly framed as a non-causal statistical or descriptive relationship and this label does not imply that the underlying real-world relationship can never be causal.

Use `not-established` when the source states or indicates that causality was not established, tested, or determined.

Use `not-applicable` for claims where causal interpretation is irrelevant.

Use `unclear` only when the source does not provide enough information to classify causal status safely.

When uncertain between `non-causal` and `not-established`, prefer `not-established`.

# Statistical Preservation

Preserve exactly when supplied:
- N / n
- means
- SD / SE
- CI
- OR / HR / RR
- beta / B / r
- R^2 / adjusted R^2
- p-values
- test statistics
- degrees of freedom
- confidence intervals
- percentages
- model names
- effect direction
- reported effect magnitude wording

Do not infer effect-size labels, practical significance, clinical significance, causal importance, robustness, or replication strength unless stated in the source.

Do not silently round, rescale, reinterpret, or convert statistics unless explicitly requested.

# Missing Information

When important metadata are absent, write `Not stated in source`.

Examples include title, authors, year, DOI, country, sport, recruitment method, exact instrument, statistical model, and effect size.

Do not invent a descriptive title for a source that does not provide one.

# Source Type

Only assign a source type that is explicitly supported.

If the source says `A cross-sectional study examined...`, then `source_type: "cross-sectional study"` is allowed.

Otherwise use `Not stated in source`.

# Claim Types

Every reusable claim must use one of:

```text
fact
inference
opinion
proposal
```

Default strict grounding should normally contain `fact` only.

Roles:

```text
context
sample
method
finding
limitation
interpretation
recommendation
```

# Evidence Location

Use the most specific available location: page, section, paragraph, table, figure, line range, transcript timestamp, or supplied research note.

If only a short note is supplied:

```yaml
evidence_location: "supplied research note"
```

Do not invent source locations.

# Confidence

Use `high`, `medium`, or `low`.

Confidence refers only to confidence that the grounded claim accurately reflects the supplied source.

# Reuse Permission

Use:

```yaml
allowed_for_reuse: true
```

for accurately grounded source-derived claims.

Use `allowed_for_reuse: false` for unsupported claims, ambiguous claims, model-generated inference, unresolved source locations, or claims whose wording changes the source's scientific meaning.

# Contract Conformance - Mandatory

Outputs must conform exactly to:

```text
references/source-contract.yaml
```

The source-card artifact must use exactly:

```yaml
source_card:
  source_id:
  title:
  source_type:
  source_date:
  authors_or_organization:
  research_question_or_purpose:
  sample_or_context:
  methods:
  summary:
  key_findings:
  limitations_explicitly_stated_by_source:
  causal_guard:
  missing_information:
```

The claim-ledger artifact must use exactly:

```yaml
claim_ledger:
  - claim_id:
    claim:
    claim_type:
    role:
    evidence_location:
    confidence:
    allowed_for_reuse:
    relationship_language:
    causal_status:
    notes:
```

Do not rename, split, merge, or invent schema fields.

# Deterministic Source ID Assignment - Mandatory

When the supplied source does not already have a registered KnowledgeCraft source ID, do not choose an `SRC-UNREGISTERED-*` number yourself.

You MUST execute:

```text
py ".opencode\skills\research-source-grounder\scripts\next_source_id.py"
```

Use the exact source ID printed by the script.

Example:

```text
SRC-UNREGISTERED-004
```

Then use exactly that ID for both artifacts:

```text
SRC-UNREGISTERED-004-source-card.md
SRC-UNREGISTERED-004-claim-ledger.yaml
```

and inside the source card:

```yaml
source_id: "SRC-UNREGISTERED-004"
```

Do not independently calculate, guess, reset, or reuse an unregistered source number.

If the helper cannot be executed successfully, do not silently fall back to `SRC-UNREGISTERED-001`. Report that source-ID allocation failed before writing grounded artifacts.

# Collision-Safe Source ID Assignment

Never overwrite an existing grounded source artifact.

Treat an ID as occupied if either its source card or claim ledger already exists.

Only replace an existing grounded source when the user explicitly requests replacement or revision of that specific source.

# Output Location - Mandatory

Never save generated research artifacts inside:

```text
.opencode/
.opencode/skills/
```

Default output directory:

```text
.knowledgecraft/research/grounded/
```

Create it if needed.

Preferred filenames:

```text
<SOURCE_ID>-source-card.md
<SOURCE_ID>-claim-ledger.yaml
```

# Source Card

Use the exact contract structure and populate fields only with source-supported information.

If a field is absent, use the contract's missing-information value or null where specified.

Do not guess.

# Research Question / Purpose

Do not invent a formal research question or purpose from the topic.

If the source explicitly states the aim, purpose, objective, or research question, preserve it.

Otherwise use `Not stated in source`.

# Sample / Context Field

Use only:

```yaml
sample_or_context:
```

Do not split into separate `sample:` and `context:` fields.

# Methods Field

Include only methodological information explicitly supported by the source.

For example, if the source says `A cross-sectional study examined 315 adolescent athletes.`, then:

```yaml
methods: "cross-sectional study"
```

is allowed.

Do not infer `self-report survey` unless explicitly stated.

# Source Summary Rule

The summary should be a compressed restatement of the source.

Do not introduce new terminology, new statistical relationship terms, new methodological labels, new interpretations, new limitations, or new causal conclusions.

# Source-Wording Preservation

Preserve scientifically meaningful source wording across summary, key findings, limitations, claim ledger, and causal guard.

Do not introduce technical relationship terminology that the source did not use.

# Compound-Claim Preservation

Do not split one compound source statement into multiple stronger independent claims when doing so changes its logical structure.

When uncertain, preserve the original compound statement.

# Relationship-Language Field

Use `relationship_language` only when the source contains a technically meaningful relationship term.

Examples:

```yaml
relationship_language: "associated with"
relationship_language: "correlated with"
relationship_language: "predicted"
```

If the source uses ordinary descriptive wording such as `reported ... also reported`, use:

```yaml
relationship_language: null
```

# Claim Ledger

Use the exact contract fields.

Do not add unsupported information inside `notes`.

If there is nothing source-supported to add, use `notes: null`.

# Notes Field Rule

Never use `notes` as a place for plausible methodological commentary, model reasoning, or explanations of grounding decisions.

For example, given:

Athletes who reported stronger developmental support also reported greater consistency of effort.

do not add:

notes: "Reported via self-report."

unless the source explicitly states that self-report data or a self-report measure was used.

Do not add:

notes: "Potential confounding may explain the relationship."

unless the source explicitly states this.

When in doubt, use `notes: null`.

## Strict-Mode Notes Rule

In STRICT SOURCE-ONLY GROUNDING, default every claim to `notes: null`.

Do not use `notes` to explain:

- why a `relationship_language` value was selected;
- why a `causal_status` value was selected;
- how the model interpreted source wording;
- how the claim was classified;
- methodological observations;
- grounding decisions.

Only populate `notes` when the source itself contains additional information that must be preserved and cannot be represented accurately in another contract field.

When uncertain, use `notes: null`.

# Limitations

Include only limitations explicitly present in the source.

If none are stated:

```text
No limitations were explicitly stated in the supplied source.
```

Do not add generic methodological limitations.

# Causal Guard

## Strict Causal-Guard Verbatim Rule

In STRICT SOURCE-ONLY GROUNDING, when the source contains an explicit causal limitation, use that source statement directly as the causal guard whenever possible.

Prefer the source's original causal-limitation wording over a synthesized explanation.

For example, if the source states:

The study did not establish whether perceived training quality caused greater perseverance.

the preferred causal guard is:

The study did not establish whether perceived training quality caused greater perseverance.

Do not append model-generated explanations such as:

- The observed association was prospective in design.
- Causal direction was not determined.
- The relationship should be interpreted as non-causal.

unless those statements themselves appear in the source.

Do not introduce new relationship terminology such as `association`, `correlation`, or `relationship` when the source did not use those terms.

In STRICT mode, a shorter verbatim causal guard is preferred over a synthesized causal explanation.


When relevant, include a short source-grounded causal guard.

If the source says:

`The study did not determine whether developmental support caused differences in consistency of effort.`

an acceptable causal guard is the same statement or:

`The source does not establish that developmental support causes differences in consistency of effort.`

Do not write:

`The relationship between developmental support and consistency of effort is non-causal.`

unless the source explicitly supports that conclusion.

# Output Contract

For normal grounding tasks, produce:

1. source card
2. claim ledger
3. causal guard when relevant
4. missing-information list

Do not produce interpretations, applied recommendations, coaching implications, LinkedIn ideas, theory extensions, methodological critique, speculative mechanisms, or proposed explanations unless explicitly requested.

# Final Grounding Check

Before saving, verify internally:

```text
Only source-supported content?                   YES
Zero default model interpretation?               YES
No invented methods?                             YES
No measurement method inferred from wording?     YES
No invented instruments?                         YES
No invented limitations?                         YES
No invented metadata or title?                   YES
Exact relationship terminology preserved?        YES
Ordinary relationship wording preserved?         YES
Source wording preserved across outputs?         YES
Compound claims preserved logically?             YES
Relationship-language field valid?               YES
Causal non-establishment preserved?              YES
No "non-causal" overstatement?                    YES
Causal status field valid?                        YES
No unsupported notes?                            YES
Uncertainty preserved?                           YES
Statistics preserved?                            YES
Missing information labeled?                     YES
Facts vs inference separated?                    YES
Exact source-contract schema used?                YES
Top-level source_card key used?                   YES
Top-level claim_ledger key used?                  YES
Deterministic source-ID helper executed?          YES
No existing grounded artifact overwritten?       YES
Output under research/grounded/?                  YES
Nothing written inside .opencode/?                YES
Strict-mode notes null unless source-required?    YES
Explicit causal limitation used verbatim?         YES
Non-substantive claims use not-applicable?        YES
```

If any item is NO, fix it before saving.

