---
name: research-insight-miner
description: Generate distinct, traceable insights, synthesis points, implications, hypotheses, evidence gaps, and communication angles from already-grounded research while preserving the original claims, relationship language, causal status, uncertainty, and source limitations. Use after research-source-grounder when moving from source truth to controlled interpretation.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "ideation"
  opencode/slash: "false"
---

# Research Insight Miner

Generate useful interpretation from grounded evidence without mutating the evidence itself.

This skill operates after `research-source-grounder`.

Its job is to move from:

grounded claims -> traceable synthesis -> clearly labeled insight

It must never silently convert inference into source fact.

# Core Boundary

`research-source-grounder` defines what the source says.

`research-insight-miner` explores what can reasonably be synthesized, questioned, translated, or hypothesized from those grounded claims.

Never rewrite a grounded claim to make an insight stronger.

Never alter:

- source wording when scientifically meaningful;
- statistical relationship terminology;
- causal status;
- uncertainty;
- sample or context;
- source-stated limitations;
- reported statistics.

If an insight requires changing any of those, the insight is invalid.

# Required Input

Prefer grounded artifacts produced by `research-source-grounder`, especially:

- source cards;
- claim ledgers;
- source IDs;
- claim IDs;
- causal guards;
- explicitly stated limitations.

Every substantive insight must trace back to one or more grounded claim IDs.

If raw research material is supplied without a grounded evidence base and factual grounding matters, use `research-source-grounder` first.

Do not treat ungrounded model summaries as equivalent to grounded claims.

# Traceability - Mandatory

Every insight must identify:

- `supporting_claim_ids`;
- `source_ids`.

Do not create an insight that cannot be traced to grounded evidence.

For cross-source insights, list every source and claim that materially supports the insight.

Do not cite a claim merely because it is topically related.

# Preserve Grounded Facts

Grounded claims remain immutable.

When referring to a grounded finding, preserve the original scientific meaning.

If the source says `associated with`, do not restate it as:

- caused;
- improved;
- increased;
- led to;
- predicted;

unless the grounded claim itself supports that wording.

If the source uses ordinary descriptive wording rather than a technical relationship term, do not invent one.

# Causal Inheritance Rule

Insights may not be more causal than their supporting grounded claims.

If supporting claims use:

`causal_status: not-established`

the insight must not state or imply that X causes Y.

Do not introduce causal mechanisms with language such as:

- because;
- leads to;
- drives;
- results in;
- improves;
- produces;

unless causal support exists in the grounded evidence.

When causality is not established, prefer language such as:

- may;
- could;
- is consistent with;
- raises the possibility;
- suggests a question;
- warrants testing;

when an inference genuinely requires such wording.

Do not use uncertainty words merely to disguise an unsupported causal claim.

# Relationship-Language Preservation

When an insight directly restates a source relationship, preserve the source's relationship language.

Examples:

`associated with` remains `associated with`.

`correlated with` remains `correlated with`.

`predicted` remains `predicted` only when the grounded source supports that term.

Ordinary source wording such as `reported ... also reported` must not automatically become `associated with`, `correlated with`, or `predicted`.

## Null Relationship-Language Rule

When a supporting grounded claim has `relationship_language: null`, do not introduce a technical relationship label when discussing that claim.

Do not replace ordinary grounded wording with terms such as:

- association;
- associated with;
- correlation;
- correlated with;
- relationship;
- linked to;
- prediction;
- predicted.

This rule applies throughout the entire insight artifact, including:

- `insight`;
- `evidence_basis`;
- `source_limitations`;
- `insight_risks`;
- audience-facing wording.

Preserve the grounded claim's ordinary descriptive construction whenever the relationship itself must be described.

For example, if the grounded claim says:

`Athletes who reported stronger coach support also reported greater perseverance.`

do not rewrite it as:

`Coach support was associated with perseverance.`

or:

`Coach support was linked to perseverance.`

### No Relationship-Language Substitution

When `relationship_language: null`, do not evade the restriction by introducing alternative or informal relationship labels.

This includes wording such as:

- relates to;
- related to;
- co-occurs with;
- observed together;
- accompanies;
- corresponds with;
- tracks with;
- goes with;
- aligns with;
- connected with;
- tied to.

If the relationship itself must be described, preserve the grounded source construction as closely as practical.

For example, if the grounded claim states:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

prefer that wording or a very close grammatical compression.

Do not convert it into:

`Coach support and perseverance were observed together.`

`Coach support relates to later perseverance.`

`Coach support co-occurs with perseverance.`

The purpose of `relationship_language: null` is to prevent the insight layer from assigning a relationship label that the grounded source did not provide.

### Source-Construction Lock for Null Relationships

When `relationship_language: null`, the grounded source construction is authoritative.

Do not create a new label, noun phrase, or shorthand for the relationship between the variables.

This prohibition includes wording such as:

- related claims;
- reported together;
- found together;
- paired reporting;
- paired pattern;
- reporting pattern;
- observed pattern;
- shared pattern;
- corresponding pattern;
- connection;
- linkage;
- pairing;
- interplay.

Do not replace the grounded construction with a noun such as `pattern`, `pairing`, `connection`, or `relationship` merely for concision.

When referring to the finding, either:

1. preserve the grounded claim directly; or
2. use a close grammatical compression that does not assign a new relationship label.

For example, preserve:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

Do not write:

`The two variables were reported together.`

`The paired reporting pattern...`

`The two related findings...`

`This pattern between coach support and perseverance...`

This rule applies to every generated field, including `insight`, `evidence_basis`, `audience_problem_or_decision`, `practical_or_conceptual_consequence`, `source_limitations`, `insight_risks`, and summaries.

When no relationship terminology is available from the grounded evidence, repetition of the grounded construction is preferred over stylistic variation.

### Canonical Wording Rule for Null Relationships

When `relationship_language: null`, do not search for alternative wording to describe the relationship between the variables.

The grounded claim itself is the canonical wording.

Whenever a generated field needs to describe that finding, either:

1. quote or reuse the grounded claim directly; or
2. make only grammatical changes that preserve the same construction without creating a relationship label or shorthand.

Do not summarize the relationship using abstractions such as:

- pattern;
- observed pattern;
- reported pattern;
- finding pattern;
- observed together;
- variables occurring together;
- connection;
- relationship;
- pairing;
- correspondence.

This rule applies to all fields, including:

- `insight`;
- `evidence_basis`;
- `audience`;
- `audience_problem_or_decision`;
- `practical_or_conceptual_consequence`;
- `source_limitations`;
- `insight_risks`;
- summaries.

If natural wording would require inventing a relationship label, repeat the grounded construction instead.

Scientific fidelity takes priority over stylistic variation.

### Verbatim Relationship Rule for Null Relationships

When `relationship_language: null`, any field that describes the substantive finding between variables MUST reuse the grounded claim verbatim.

Do not paraphrase the relationship.

Do not replace the grounded construction with:

- a synonym;
- a shorthand label;
- an abstract noun;
- a summary phrase;
- a stylistic variation;
- a newly invented relationship verb.

This is a deterministic rule.

If the grounded claim is:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

then any generated field that needs to state that finding must use exactly:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

The following are not allowed:

`Coach support and perseverance were observed together.`

`The finding showed a pattern between coach support and perseverance.`

`The two reports co-occurred.`

`Coach support related to later perseverance.`

`There was a connection between coach support and perseverance.`

If a field does not need to restate the substantive finding, keep it relationship-neutral.

For example, prefer:

`evidence_basis: "supported by grounded claims SRC-TEST-001-01 and SRC-TEST-001-02"`

over:

`evidence_basis: "supported by an observed reporting pattern"`

Prefer:

`audience_problem_or_decision: "deciding how to interpret the grounded finding in practice"`

over:

`audience_problem_or_decision: "deciding how to respond to the relationship between coach support and perseverance"`

Prefer:

`practical_or_conceptual_consequence: "supports monitoring and further investigation without implying causality"`

over:

`practical_or_conceptual_consequence: "respond to the co-occurrence of coach support and perseverance"`

If a natural sentence cannot be written without paraphrasing the null relationship, repeat the grounded claim verbatim or make the field relationship-neutral.

This rule overrides stylistic variety, concision, and avoidance of repetition.

## Source-Limitation Preservation Rule

`source_limitations` must contain only limitations already present in the grounded evidence.

Preserve the grounded limitation wording verbatim whenever practical.

Do not summarize, reinterpret, strengthen, generalize, or add terminology to a grounded limitation.

Any model-generated concern about interpretation, transfer, application, or overgeneralization belongs under `insight_risks`, not `source_limitations`.

## Non-Causal Practice Implication Rule

When the supporting evidence has `causal_status: not-established`, do not recommend changing X for the purpose of improving, increasing, reducing, or causing Y.

Do not convert non-causal grounded evidence into an intervention recommendation.

A practical implication may instead identify:

- something worth monitoring;
- something worth considering in decision making;
- something worth investigating;
- a question for practice;
- a candidate factor for future testing.

If an implication proposes an intervention intended to change the outcome, causal effectiveness must not be presented as supported by the grounded evidence.

## Output Language Consistency

Write generated fields consistently in the language requested by the user.

Do not introduce unexplained words, characters, or phrases from another language unless they occur in quoted source material.

# Insight Types

Use one of the following:

- `synthesis`
- `implication`
- `hypothesis`
- `evidence_gap`
- `tension`
- `application_question`
- `communication_angle`
- `decision_framework`
- `misconception_correction`

## Synthesis

A synthesis combines grounded claims without adding a new causal explanation or mechanism.

It may identify:

- convergence;
- contrast;
- recurring findings;
- differences across contexts;
- complementary findings.

A synthesis must remain within what the supporting claims justify.

## Implication

An implication is a model-generated interpretation of what grounded findings may mean for a decision, practice, theory, or future work.

It is not a source fact unless the source explicitly made the same implication.

Label it clearly as interpretation.

Do not write a recommendation as though the evidence directly proved that the recommended action will work.

## Hypothesis

A hypothesis is a new, testable proposition suggested by the evidence.

It is not an established finding.

Use hypothesis language explicitly.

Do not backfill a mechanism into the grounded evidence.

### Hypothesis Inference-Level Rule

A model-generated hypothesis that extends beyond the supplied grounded evidence must use:

`inference_level: high`

This includes hypotheses involving:

- another sample;
- another population;
- another setting;
- another timeframe;
- a proposed mechanism;
- a proposed explanatory variable;
- a proposed causal test.

Do not use `moderate` merely because the hypothesis is phrased cautiously.

## Evidence Gap

An evidence gap identifies something needed to answer a relevant question that is absent or unresolved in the grounded evidence.

Do not present absence from one source as proof that the broader literature contains no evidence.

Prefer:

`Not established in the supplied grounded evidence.`

over:

`No evidence exists.`

## Tension

A tension identifies grounded claims that appear to differ, conflict, or point in different directions.

Do not force reconciliation.

Preserve differences in:

- populations;
- measures;
- designs;
- outcomes;
- timeframes;
- relationship terminology.

If the available grounded information cannot explain the difference, say so.

## Application Question

An application question translates evidence into a question for practice without pretending the answer is established.

It must obey the same relationship-language rules as every other field.

When `relationship_language: null`, reuse the grounded finding verbatim inside the question if the finding must be stated.

For example:

`If athletes in another setting report stronger coach support at baseline and also report greater perseverance six months later, what would practitioners need to consider before acting on that information?`

Do not replace the grounded construction with `pattern`, `relationship`, `association`, `co-occurrence`, or similar shorthand.

Do not imply that transfer across contexts has already been demonstrated.

## Communication Angle

A communication angle is a way to explain grounded evidence to a defined audience.

It must remain faithful to the evidence.

It must not exaggerate novelty, certainty, causality, or practical effectiveness.

## Decision Framework

A decision framework organizes grounded evidence around a practical or conceptual decision.

It may structure trade-offs or questions.

It must not invent thresholds, rules, or recommendations unsupported by the evidence.

## Misconception Correction

Use only when the grounded evidence genuinely contradicts or qualifies a clearly stated misconception.

Do not invent a straw-man misconception merely to make content more interesting.

# Inference Level

Assign one of:

- `low`
- `moderate`
- `high`

`low`:
The insight is a close synthesis of grounded claims with little added interpretation.

`moderate`:
The insight adds a plausible conceptual or practical implication beyond direct restatement.

`high`:
The insight introduces a hypothesis, proposed mechanism, transfer to a new context, or other substantial model-generated interpretation.

Inference level describes distance from the grounded evidence, not evidence quality.

# Evidence Strength

Do not invent formal evidence-strength ratings unless the grounded inputs contain an explicit evidence appraisal.

Do not label evidence as:

- strong;
- weak;
- robust;
- definitive;
- high-quality;
- low-quality;

unless that characterization is grounded.

Instead describe the basis concretely, for example:

- `supported by one grounded source`;
- `supported by three grounded sources`;
- `supported by convergent grounded claims`;
- `grounded claims are mixed`;
- `insufficient grounded information to judge`.

# Mechanisms

Do not present a mechanism as established unless the grounded evidence explicitly supports that mechanism.

If a plausible mechanism is useful, classify it as:

`insight_type: hypothesis`

and make clear that it is proposed rather than demonstrated.

Never insert a proposed mechanism back into the source summary or grounded claim ledger.

## Ungrounded Explanatory Detail Rule

Do not introduce specific explanatory variables, mechanisms, mediators, moderators, confounders, contextual factors, or alternative causes that are absent from the grounded evidence merely to make an insight more interesting.

Examples of unsupported additions include:

- peers;
- family;
- prior experiences;
- motivation;
- confidence;
- organizational culture;
- socioeconomic factors;
- personality;
- unmeasured variables;

unless those concepts are present in the grounded evidence or the user explicitly requests speculative hypothesis generation.

A hypothesis may propose something beyond the grounded evidence, but the degree of speculation must remain visible.

When the grounded evidence does not identify a mechanism or alternative explanatory factor, prefer generic wording such as:

`Other factors may warrant investigation.`

Do not silently replace missing explanatory information with specific plausible examples.

Do not write that a grounded finding `may reflect`, `may be due to`, `may result from`, or `may be explained by` unspecified other factors unless the user explicitly requests speculative explanation.

If the evidence leaves explanation unresolved, prefer:

`The grounded evidence does not establish an explanation for this finding.`

or, when useful:

`Other factors may warrant investigation.`

Do not turn absence of explanatory information into an alternative explanation.

When speculative mechanisms or variables are explicitly requested:

- classify the item as `hypothesis`;
- use `inference_level: high`;
- state that the proposed explanation is not contained in the grounded source;
- do not place the proposal in `source_limitations` or `evidence_basis`;
- consider `allowed_for_reuse: false` when the proposal is highly speculative.

## Interpretive Causal-Language Guard

Causal-language restrictions apply not only to conclusions but also to explanations, hypotheses, questions, risks, and practical implications.

When causality is not established, avoid unsupported wording such as:

- accounts for;
- explains;
- drives;
- produces;
- determines;
- shapes;
- influences;
- changes;
- shifts;
- results in;

unless clearly presented as an explicitly requested hypothesis and labeled accordingly.

Do not introduce these terms merely to describe uncertainty around a non-causal grounded finding.

## Question-Language Preservation

Application questions and research questions must obey the same relationship-language rules as declarative insights.

When `relationship_language: null`, do not ask:

`How does X relate to Y?`

`What explains the relationship between X and Y?`

`Which factors predict Y?`

unless those relationship terms are supported by the grounded claims.

Prefer questions that preserve the original construction.

For example:

`Would athletes who report stronger coach support at baseline also report greater perseverance at a later assessment in another sample?`

# Source Limitations vs Insight Risks

Keep these separate.

`source_limitations`:
Only limitations already grounded from the source.

`insight_risks`:
Risks introduced by the interpretive step, such as transfer to another population, overgeneralization, or dependence on a small claim base.

Do not rewrite model-generated risk notes as though the source authors stated them.

# Distinctness Rule

Do not generate multiple ideas that are merely stylistic paraphrases of the same insight.

Merge or discard ideas that share the same:

- supporting claim cluster;
- audience problem;
- core takeaway;
- practical or conceptual consequence;
- reader action.

A new title or hook does not make an insight substantively new.

# Audience and Decision Relevance

For communication or applied insights, identify:

- audience;
- audience problem, decision, or misconception;
- why the grounded evidence matters to that audience.

Do not invent personal anecdotes, client stories, coaching stories, organizational examples, or lived experience.

If practitioner or author experience would materially improve the insight, identify it as `author_input_needed` rather than inventing it.

# Cross-Source Synthesis

When working across multiple grounded sources:

1. preserve each source's original claims;
2. compare only claims that are meaningfully comparable;
3. retain differences in design, population, context, measure, outcome, and timing when known;
4. do not treat repeated findings as proof of causality;
5. do not call findings replicated, confirmed, consistent, convergent, contradictory, conflicting, or equivalent unless that characterization is explicitly justified by the grounded evidence;
6. do not call findings contradictory when they may simply concern different questions;
7. list all supporting source IDs and claim IDs.

If comparability cannot be established from grounded information, state that clearly.

## Cross-Source Finding Preservation Rule

When a cross-source insight describes a grounded finding from a source, preserve that source's finding wording exactly whenever practical.

If different sources use different relationship language, retain each source's own wording rather than creating a common relationship label.

For example, if Source A states:

`Perceived coach support was associated with perseverance at the same assessment.`

and Source B states:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

do not rewrite both as:

`Higher coach support was present alongside higher perseverance.`

Do not rewrite Source A as ordinary descriptive wording if it explicitly uses `associated with`.

Do not rewrite Source B as `associated with`, `related to`, `linked to`, `co-occurring with`, `present alongside`, or another relationship label when its grounded `relationship_language` is null.

Prefer:

`Source A states: "Perceived coach support was associated with perseverance at the same assessment." Source B states: "Athletes who reported stronger coach support at baseline also reported greater perseverance six months later."`

Then describe only the grounded differences that can be supported safely.

## No Design Inference From Timing

Do not infer a study-design label from temporal wording alone.

A statement that something was measured at baseline and again six months later does not by itself authorize labels such as:

- longitudinal;
- prospective;
- cohort;
- repeated-measures;

unless the grounded source explicitly states that design.

Preserve the supplied timing directly, for example:

`baseline and six months later`

rather than inventing:

`a longitudinal design`

When one source explicitly states a design and another source provides only timing, preserve that asymmetry.

## Cross-Source Comparability Language

Default to descriptive comparison rather than evaluative comparison.

Prefer wording such as:

- `Source A states...`;
- `Source B states...`;
- `the sources differ in timing`;
- `the supplied populations differ`;
- `the grounded evidence does not establish whether the findings are directly comparable`.

Avoid labels such as:

- replicated;
- confirmed;
- consistent;
- convergent;
- contradictory;
- conflicting;
- equivalent;

unless the grounded evidence and user task clearly justify that classification.

Do not manufacture a shared relationship description merely to make cross-source prose smoother.

# Complete Traceability Rule

Every grounded claim materially represented anywhere in an insight artifact must be included in `supporting_claim_ids`.

If a source limitation is reproduced in `source_limitations`, include the claim ID containing that limitation.

If a causal guard or other grounded claim materially constrains an insight, include its claim ID.

Do not reuse grounded content in a field while omitting its claim ID from traceability.

# Output Schema

For each insight use:

```yaml
insight_id: ""
insight_type: "synthesis|implication|hypothesis|evidence_gap|tension|application_question|communication_angle|decision_framework|misconception_correction"
insight: ""
supporting_claim_ids: []
source_ids: []
inference_level: "low|moderate|high"
evidence_basis: ""
audience: null
audience_problem_or_decision: null
practical_or_conceptual_consequence: null
angle: null
novelty_reason: null
source_limitations: []
insight_risks: []
author_input_needed: null
allowed_for_reuse: true
```

Do not invent additional fields unless the user explicitly requests a different structure.

# Reuse Rule

`allowed_for_reuse: true` means the insight may be reused only as a clearly labeled insight, synthesis, implication, question, or hypothesis.

It does not convert the insight into a source fact.

Use `allowed_for_reuse: false` when:

- traceability is incomplete;
- the inference is too speculative;
- supporting claims conflict materially;
- a required source is missing;
- causal or statistical meaning would be distorted;
- the insight depends on unstated assumptions that cannot be made explicit safely.


# Mandatory Deterministic Validation

The natural-language rules in this skill are necessary but are not sufficient for final acceptance.

Every generated insight artifact MUST pass the deterministic validator before the run is considered complete.

Validator:

` .opencode/skills/research-insight-miner/scripts/validate_insights.py `

For normal KnowledgeCraft grounded inputs, run:

```text
py ".opencode\skills\research-insight-miner\scripts\validate_insights.py" "<INSIGHT_ARTIFACT_PATH>"
```

The validator loads grounded claim ledgers from:

`.knowledgecraft/research/grounded/`

When grounded claims are supplied inline for a synthetic or regression test and do not exist in the grounded directory, provide the exact claim ledger explicitly:

```text
py ".opencode\skills\research-insight-miner\scripts\validate_insights.py" "<INSIGHT_ARTIFACT_PATH>" --claims "<CLAIM_LEDGER_PATH>"
```

For synthetic tests, any temporary claim-ledger fixture must reproduce the supplied grounded claims exactly and should be stored under:

`.knowledgecraft/scratch/`

Do not invent or reinterpret claims when creating a validation fixture.

## Validation Failure Rule

If the validator returns `FAIL`:

1. do not report the insight artifact as successfully completed;
2. read every reported validation issue;
3. revise only the fields needed to correct those issues;
4. rerun the validator;
5. repeat until the validator returns `PASS`.

Do not bypass, ignore, suppress, or reinterpret validator failures.

If the validator cannot be executed, report that deterministic validation could not be completed.

Do not claim that the artifact passed validation when the validator did not return `PASS`.

## Candidate Rewrite Rule

During one active generation run, a candidate insight artifact may be rewritten as needed to resolve validator failures.

This is not treated as replacement of a previously accepted artifact.

After an artifact has passed validation and the run is complete, do not overwrite it in a later run unless the user explicitly requests revision or replacement.

## Validator-Guided Repair for Null Relationships

When the validator reports a likely paraphrase of a grounded claim whose `relationship_language` is `null`, do one of the following:

1. reuse the grounded claim verbatim inside the generated field; or
2. rewrite the field so it is relationship-neutral and does not restate the finding.

Do not solve the validator failure by inventing another synonym or shorthand.

Example grounded claim:

`Athletes who reported stronger coach support at baseline also reported greater perseverance six months later.`

Acceptable hypothesis structure:

`The grounded finding was: "Athletes who reported stronger coach support at baseline also reported greater perseverance six months later." A future study could test whether this exact finding is reproduced in another sample.`

Acceptable application-question structure:

`The grounded finding was: "Athletes who reported stronger coach support at baseline also reported greater perseverance six months later." What should practitioners consider before using this finding in another context?`

## Validator-Guided Traceability Repair

When a grounded limitation, causal guard, or other grounded statement appears anywhere in an insight artifact, its claim ID must be present in `supporting_claim_ids`.

If the validator reports that a source limitation was reused without its claim ID, add the exact grounded claim ID that contains that limitation.

Do not remove the claim from traceability merely to make the validator pass.

# Validator Dependency

The validator requires PyYAML.

If Python reports that the `yaml` module is unavailable, install it with:

```text
py -m pip install pyyaml
```


# Completion Reporting Rule

After deterministic validation returns `PASS`, keep the final completion message operational and validator-safe.

By default report only:

- validator PASS status;
- number of validated insights;
- artifact path;
- validation fixture path when relevant.

Do not add a fresh substantive summary of the findings after validation unless the user explicitly asks for one.

A post-validation prose summary is not covered by the artifact validator and can accidentally reintroduce unsupported relationship or causal wording.

Preferred completion pattern:

`PASS: 4 insights validated.`

`Artifact: .knowledgecraft/research/insights/<FILE>.yaml`

`Validation fixture: .knowledgecraft/scratch/<FILE>.yaml`

Do not summarize validated `not-established` evidence as `non-causal`.

Do not introduce new relationship terminology in the completion message.

# Output Location

Save generated insight artifacts under:

`.knowledgecraft/research/insights/`

Never save generated outputs inside:

`.opencode/`
`.opencode/skills/`

Preferred filenames:

Single source:
`<SOURCE_ID>-insights.yaml`

Cross-source:
`<PROJECT_OR_TOPIC>-insights.yaml`

Never overwrite an existing insight artifact unless the user explicitly requests revision or replacement.

# Default Workflow

1. Identify the grounded source cards and claim ledgers.
2. Confirm source IDs and claim IDs.
3. Read causal guards and explicit limitations.
4. Cluster claims by substantive question.
5. Generate candidate insights.
6. Classify each insight type.
7. Assign inference level.
8. Check every insight against causal and relationship-language constraints.
9. Attach supporting source IDs and claim IDs.
10. Separate source limitations from interpretive risks.
11. Merge duplicate or near-duplicate insights.
12. Write the candidate insight artifact.
13. Run the deterministic insight validator.
14. Repair every validator failure and rerun until `PASS`.
15. Treat the artifact as complete only after validation passes.

# Final Insight Check

Before saving, verify internally:

```text
Grounded inputs used?                               YES
Every insight traces to claim IDs?                  YES
Every insight traces to source IDs?                 YES
Grounded claims left unchanged?                     YES
Relationship terminology preserved?                YES
Causal status not strengthened?                     YES
No unsupported causal mechanism?                   YES
Inference level assigned correctly?                 YES
Source facts separated from interpretation?         YES
Source limitations preserved as source limitations? YES
Model-generated risks kept separate?                YES
Evidence strength not invented?                     YES
Cross-source comparability checked?                 YES
Duplicate insights merged or discarded?             YES
No invented personal anecdotes?                     YES
Output under research/insights/?                    YES
Nothing written inside .opencode/?                  YES
Null relationship language preserved globally?     YES
No surrogate relationship terminology introduced?  YES
No relationship shorthand invented?                YES
Null relationships use canonical source wording?    YES
Null relationship descriptions verbatim?           YES
Relationship-neutral metadata used where possible? YES
Source limitations preserved without rewriting?    YES
Non-causal evidence not turned into intervention?  YES
Output language internally consistent?              YES
No ungrounded explanatory variables introduced?    YES
No unsupported alternative explanation introduced? YES
Causal-language guard applied to all fields?        YES
Questions preserve relationship-language rules?    YES
Hypotheses beyond grounded evidence marked high?    YES
All reused grounded content traced to claim IDs?    YES
Cross-source finding wording preserved?             YES
No design inferred from timing alone?               YES
No unsupported cross-source comparison labels?      YES
Post-validation completion message validator-safe?  YES
Deterministic validator executed?                   YES
Deterministic validator returned PASS?              YES
No validator failures ignored?                      YES
```

If any item is NO, revise or discard the insight before saving.
