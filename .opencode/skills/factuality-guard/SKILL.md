---
name: factuality-guard
description: Audit drafted text against grounded evidence, claim ledgers, or supplied sources before publication. Use when writing contains research findings, statistics, dates, named entities, quotations, causal claims, personal claims, or other externally checkable statements that must remain faithful to evidence.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "factual-qa"
  opencode/slash: "false"
---

# Factuality Guard

Use this skill as the final factual QA layer between evidence-grounded work and publication-ready writing.

Its job is to detect claim drift.

It does **not** replace `research-source-grounder`, and it does **not** generate new scientific interpretations.

When grounded claim ledgers exist, treat them as the primary evidence contract.

## Core Boundary

`factuality-guard` answers:

- What externally checkable claims appear in the draft?
- Which grounded claim or source supports each one?
- Did the draft preserve the original number, direction, population, relationship language, causal status, attribution, quotation, and uncertainty?
- Did the draft introduce information not supported by the evidence?
- Does any factual problem block publication?

It must not:

- invent missing evidence;
- strengthen a source claim to make prose smoother;
- infer a mechanism;
- infer causality;
- infer non-causality from failure to establish causality;
- fabricate references;
- silently correct the source;
- resolve conflicting evidence without explicit support;
- rewrite the draft unless the user asks for repair.

## Evidence Priority

Use evidence in this order when available:

1. grounded claim ledger;
2. grounded source card;
3. supplied source text;
4. explicitly supplied author/personal confirmation.

Do not treat model memory as evidence for a claim being audited.

If the draft contains an externally checkable claim and no supplied evidence supports it, classify it `NEEDS_SOURCE` or `UNSUPPORTED` according to the rules below.

## Claim Unit

Treat every externally checkable statement as a claim.

Split compound sentences when different parts have different support.

Example:

`The intervention improved performance and reduced dropout.`

must be audited as at least two claims if improvement and dropout are supported separately.

Do not allow one supported clause to hide an unsupported clause.

## Audit Statuses

Every audited claim receives exactly one primary status:

### `SUPPORTED`

The draft claim is materially faithful to supplied evidence.

This requires preservation of all scientifically or factually meaningful qualifiers.

### `OVERSTATED`

The draft has evidence behind it, but expresses a stronger, broader, more certain, more causal, more general, or more precise claim than the evidence supports.

Examples:

- `was associated with` -> `caused`;
- `may` -> `will`;
- `in this sample` -> universal statement;
- `did not establish causality` -> `was non-causal`;
- `reported greater perseverance` -> `predicted perseverance` when prediction was not grounded.

### `UNSUPPORTED`

Supplied evidence does not support the claim and the draft presents it as fact.

Examples:

- invented mechanism;
- invented moderator;
- invented study detail;
- invented implication stated as established fact;
- unsupported personal anecdote presented as true.

### `CONFLICTING`

The supplied evidence materially conflicts with the draft claim, or supplied sources materially conflict with each other in a way that prevents the draft claim from being accepted as written.

Do not choose one conflicting source as correct without a justified basis.

### `NEEDS_SOURCE`

The claim is externally checkable but no adequate evidence was supplied for auditing it.

Use this especially for:

- dates;
- named entities;
- publication facts;
- current statistics;
- biographical claims;
- personal claims;
- quotations;
- references not present in supplied evidence.

Do not upgrade `NEEDS_SOURCE` to `SUPPORTED` from general knowledge.

## Mandatory Fidelity Checks

For every substantive claim, check all applicable dimensions.

### 1. Claim content

Does the evidence support the actual proposition?

### 2. Population

Preserve who the evidence concerns.

Examples of drift:

- `146 youth athletes` -> `athletes`;
- `adolescent athletes` -> `all athletes`;
- one sport -> all sports.

Removing a population qualifier is acceptable only when it does not materially broaden the claim.

### 3. Context

Preserve material setting or scope when supplied.

Do not generalize from one context to another as if directly established.

### 4. Direction

Preserve positive, negative, null, mixed, or unclear direction exactly.

Do not reverse or simplify direction.

### 5. Magnitude

Preserve effect size, strength, frequency, or magnitude when stated.

Do not change `small` to `meaningful`, `moderate`, `strong`, or similar without evidence.

### 6. Numbers and statistics

Check:

- sample size;
- percentages;
- means;
- standard deviations;
- coefficients;
- odds ratios;
- confidence intervals;
- p-values;
- dates;
- durations;
- units;
- denominators;
- decimal precision when material.

Never silently round a value in a way that changes meaning.

If the draft intentionally rounds harmlessly, note that as acceptable rather than inventing precision.

### 7. Relationship language

Preserve grounded relationship terminology.

If `relationship_language` contains a technical phrase such as:

`associated with`

do not accept substitutions such as:

- caused;
- predicted;
- led to;
- resulted in;
- explained;
- drove;
- influenced;

unless separately grounded.

If `relationship_language: null`, do not introduce a new technical relationship label merely because it sounds clearer.

Ordinary source wording such as:

`athletes who reported X also reported Y`

does not authorize:

- association;
- correlation;
- prediction;
- relationship;
- linkage;
- co-occurrence;

unless grounded elsewhere.

### 8. Causal status

Preserve causal strength exactly.

For `causal_status: not-established`:

Allowed meaning:

`The study did not establish whether X caused Y.`

Not equivalent:

- `X was non-causal`;
- `X does not cause Y`;
- `there was no causal relationship`;
- `X caused Y`;
- `X improves Y`.

Failure to establish causality is not evidence of absence of causality.

### 9. Uncertainty

Preserve meaningful uncertainty.

Examples:

- `may` must not become `does`;
- `suggests` must not become `demonstrates`;
- `unclear` must not become a directional conclusion;
- confidence-interval uncertainty must not be erased when material.

### 10. Attribution

Verify who said, found, reported, estimated, or concluded the claim.

Do not transfer a statement from participants to authors, from authors to institutions, or from one source to another.

### 11. Quotations

A direct quotation must match supplied source text exactly except for clearly indicated omissions or harmless typography normalization.

If exact source text is unavailable, classify quotation fidelity as `NEEDS_SOURCE`.

Do not fabricate quotations from paraphrases.

### 12. Limitations

If the draft mentions a source limitation, preserve its meaning.

Do not:

- strengthen a limitation;
- convert a stated limitation into a broader criticism;
- turn `did not establish causality` into `non-causal`;
- invent unreported confounders, biases, mechanisms, or design defects as source-stated limitations.

Model-generated critique may be useful elsewhere, but it must not be presented as a source-stated limitation.

### 13. Inference versus fact

If the evidence contains an inference, opinion, proposal, hypothesis, or application question, do not audit it as though it were an established source fact.

Preserve the distinction.

A model-generated insight may be acceptable in a draft when clearly framed as interpretation, but not when rewritten as an empirical finding.

## Source-Ledger Rules

When a claim ledger is supplied:

- use `claim_id` for traceability;
- respect `allowed_for_reuse`;
- respect `claim_type`;
- respect `role`;
- respect `relationship_language`;
- respect `causal_status`;
- preserve exact statistics present in the claim;
- do not treat `notes` as scientific evidence unless the contract explicitly says they are reusable evidence.

If a draft claim uses more than one grounded claim, list all relevant grounded claim IDs that form the evidence basis for the audit classification.

If no grounded claim provides an evidence basis for the draft claim, do not fabricate one.

### Evidence-Basis Traceability Rule

`supporting_claim_ids` means the grounded claims used to evaluate the draft claim, not only claims that fully support the draft as written.

Therefore:

- `SUPPORTED`: include the grounded claim IDs that support the draft;
- `OVERSTATED`: include the grounded claim IDs that establish the weaker/source-faithful basis and, when relevant, the limitation that shows why the draft is too strong;
- `CONFLICTING`: include the grounded claim IDs that directly conflict with the draft;
- `NEEDS_SOURCE`: normally use `[]` when no supplied evidence covers the claim;
- `UNSUPPORTED`: normally use `[]` when the asserted content has no grounded basis, although a nearby grounded claim may still be referenced in `required_fix` as a safe replacement.

Do not leave `supporting_claim_ids` empty for an `OVERSTATED` or `CONFLICTING` claim when the classification depends on supplied grounded evidence.

Examples:

Grounded finding:

`SRC-FACT-001-01: Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

Grounded limitation:

`SRC-FACT-001-02: The study did not establish whether stronger coach support caused greater perseverance.`

Draft:

`Coach support caused greater perseverance six months later.`

Correct traceability:

```yaml
status: OVERSTATED
supporting_claim_ids:
  - SRC-FACT-001-01
  - SRC-FACT-001-02
```

The draft is not supported as written, but those grounded claims are the evidence basis for identifying the overstatement.

## Personal Claims

Personal statements such as:

- `In my coaching experience...`;
- `I have seen...`;
- `Our club found...`;
- `My athletes often...`;

require either:

- supplied author confirmation;
- supplied records;
- explicit instruction to treat the statement as the author's own assertion.

Do not invent a personal anecdote to make writing sound human.

If confirmation is absent and factual truth matters, use `NEEDS_SOURCE`.

## Reference and Citation Guard

Do not fabricate references.

When a draft names a paper, author, year, DOI, journal, organization, or report:

- verify it against supplied evidence;
- otherwise use `NEEDS_SOURCE`.

Do not infer a citation merely because a claim resembles known literature.

## Current or Time-Sensitive Claims

If a claim depends on current information and no current source was supplied, classify it `NEEDS_SOURCE`.

Examples:

- current office-holder;
- current law or policy;
- current software version;
- current market statistic;
- current ranking;
- current organizational role.

The guard itself should not silently browse or replace evidence unless the user explicitly requests external verification.

## Output Contract

Default output is a factuality audit.

Use this structure:

```yaml
factuality_audit:
  draft_id: null
  evidence_basis:
    source_ids: []
    claim_ledger_used: true
  claims:
    - audit_id: "FQ-001"
      draft_claim: ""
      status: "SUPPORTED|OVERSTATED|UNSUPPORTED|CONFLICTING|NEEDS_SOURCE"
      supporting_claim_ids: []
      evidence_excerpt: null
      issues: []
      required_fix: null
      publication_blocking: false
  summary:
    total_claims: 0
    supported: 0
    overstated: 0
    unsupported: 0
    conflicting: 0
    needs_source: 0
    publication_gate: "PASS|BLOCK"
    blocking_claim_ids: []
```

## `issues` Vocabulary

Use concise issue labels when applicable:

- `number_mismatch`
- `unit_mismatch`
- `date_mismatch`
- `population_broadened`
- `context_broadened`
- `direction_changed`
- `magnitude_changed`
- `relationship_strengthened`
- `relationship_invented`
- `causal_overstatement`
- `causal_absence_invented`
- `uncertainty_removed`
- `attribution_error`
- `quotation_mismatch`
- `unsupported_mechanism`
- `unsupported_limitation`
- `inference_as_fact`
- `reference_unverified`
- `personal_claim_unverified`
- `source_conflict`
- `missing_evidence`

Multiple issue labels may apply to one claim.

## Publication Gate

Default gate:

`PASS`

only when there are no materially publication-blocking factual problems.

Default blocking statuses:

- `OVERSTATED`
- `UNSUPPORTED`
- `CONFLICTING`
- `NEEDS_SOURCE`

A `NEEDS_SOURCE` claim may be non-blocking only when it is clearly non-material and publication does not depend on factual verification.

Do not mark `PASS` merely because most claims are supported.

One materially false or unsupported claim can block publication.

## Repair Behavior

By default, audit first.

Do not silently rewrite the draft while auditing.

If the user asks for repair:

1. preserve supported text where possible;
2. repair only the failing claim or clause;
3. restore source-faithful terminology;
4. remove unsupported material when it cannot be safely repaired;
5. rerun the audit on the repaired draft;
6. do not report factual QA complete until publication gate becomes `PASS`, unless the user accepts unresolved blockers.

### Required-Fix Fidelity Rule

The `required_fix` field is itself part of the factuality audit and must obey the same evidence constraints as the audited claim.

Never suggest a replacement term that the evidence does not authorize.

If the supporting grounded finding has `relationship_language: null`, `required_fix` must not recommend terms such as:

- `associated with`;
- `correlated with`;
- `related to`;
- `linked to`;
- `predicted`;
- `co-occurred with`;
- `relationship`;
- `connection`.

Instead, recommend exact grounded wording or relationship-neutral repair.

Example:

Grounded:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

Bad required fix:

`Replace "caused" with "was associated with".`

Good required fix:

`Replace the causal wording with the grounded wording: "Athletes who reported stronger coach support at baseline also reported greater perseverance six months later."`

Likewise, when `causal_status: not-established`, a required fix must preserve non-establishment and must not suggest `non-causal`, `no causal relationship`, or another categorical absence-of-causality claim.

A factuality audit is not valid if its own repair advice introduces claim drift.

## Examples

### Association -> causation

Grounded:

`Perceived coach support was associated with perseverance.`

Draft:

`Coach support increased perseverance.`

Result:

`OVERSTATED`

Issues:

- `relationship_strengthened`
- `causal_overstatement`

### Causality not established -> non-causal

Grounded:

`The study did not establish whether coach support caused perseverance.`

Draft:

`The relationship between coach support and perseverance was non-causal.`

Result:

`OVERSTATED`

Issue:

- `causal_absence_invented`

### Ordinary wording -> prediction

Grounded:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

Draft:

`Coach support predicted later perseverance.`

Result:

`OVERSTATED`

Issues:

- `relationship_invented`
- `relationship_strengthened`

Required-fix guidance must reuse the grounded descriptive construction or stay relationship-neutral. It must **not** suggest `associated with` or another technical relationship label.

### Unsupported mechanism

Grounded:

`Athletes who reported stronger coach support also reported greater perseverance.`

Draft:

`Coach support improved perseverance by increasing athlete confidence.`

Result:

`UNSUPPORTED`

Issues:

- `causal_overstatement`
- `unsupported_mechanism`

### Correctly framed interpretation

Grounded fact:

`Athletes who reported stronger coach support also reported greater perseverance.`

Draft:

`One possible interpretation is that coach support may be worth examining further, although the study did not establish causality.`

Result may be:

`SUPPORTED`

only when the interpretation is clearly framed as interpretation and does not claim the source established it.

## Deterministic Audit Validation

After writing the factuality audit YAML, run the deterministic validator:

```powershell
py ".opencode/skills/factuality-guard/scripts/validate_factuality_audit.py" "<AUDIT_FILE>.yaml"
```

The validator checks deterministic audit integrity, including:

- valid claim statuses;
- unique audit IDs;
- evidence-basis traceability for `SUPPORTED`, `OVERSTATED`, and `CONFLICTING` claims;
- summary counts recomputed from final claim statuses;
- `total_claims` arithmetic;
- `blocking_claim_ids` consistency;
- publication gate consistency.

The validator does **not** decide whether a scientific classification is semantically correct. That remains the factuality-guard's evidence-audit responsibility.

If validation returns `FAIL`:

1. do not report the audit complete;
2. read every validator error;
3. repair only the affected audit fields;
4. rerun the validator;
5. continue until `PASS`.

Do not ignore a deterministic validation failure.

## Completion Rule

A factuality audit is complete only after:

- all externally checkable claims have been considered;
- compound claims have been split where needed;
- evidence traceability is recorded;
- relationship and causal wording have been checked;
- numbers/statistics have been checked when present;
- unsupported additions have been identified;
- publication gate has been assigned;
- summary counts have been recomputed from the final claim statuses;
- `total_claims` equals the sum of all five status counts;
- `blocking_claim_ids` exactly matches the claims marked `publication_blocking: true`;
- evidence-based `OVERSTATED` and `CONFLICTING` claims retain their grounded evidence IDs in `supporting_claim_ids`.

Do not report a draft as factually safe when material blockers remain.

### Summary Consistency Rule

The summary is derived data and must be internally consistent with the claim-level audit.

Before completion:

1. count claim statuses from the final audited claims;
2. set `supported`, `overstated`, `unsupported`, `conflicting`, and `needs_source` from those counts;
3. verify their sum equals `total_claims`;
4. rebuild `blocking_claim_ids` from claims where `publication_blocking: true`;
5. set `publication_gate: BLOCK` if any material blocker remains.

Do not manually carry forward summary counts from an earlier draft of the audit.

## Final Checks

Before reporting factual QA complete, verify:

- every externally checkable claim audited? YES
- compound claims split when necessary? YES
- evidence IDs traced where available? YES
- numbers and units preserved? YES
- population/context preserved? YES
- relationship language preserved? YES
- `not-established` not rewritten as `non-causal`? YES
- causality not invented? YES
- unsupported mechanisms absent or flagged? YES
- source limitations preserved? YES
- inference distinguished from fact? YES
- quotations verified or marked `NEEDS_SOURCE`? YES
- references verified or marked `NEEDS_SOURCE`? YES
- personal claims verified or marked appropriately? YES
- material factual problems block publication? YES
- required-fix advice obeys the same relationship/causal constraints? YES
- summary counts match final claim statuses? YES
- blocking claim IDs match publication_blocking flags? YES
- overstated/conflicting claims retain evidence-basis claim IDs? YES
- deterministic factuality audit validator executed? YES
- deterministic validator returned PASS? YES
