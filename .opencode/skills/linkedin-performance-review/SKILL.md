---
name: linkedin-performance-review
description: Analyze LinkedIn post-performance data conservatively, preserve raw metrics, calculate transparent rates, compare posts with exposure/context caveats, classify findings by evidential strength, and turn observations into cautious future tests without causal or algorithmic overclaiming.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "analytics"
  opencode/slash: "false"
---

# LinkedIn Performance Review

Analyze LinkedIn post-performance data and convert it into **cautious, reusable content learnings**.

The job is to describe what happened, calculate transparent metrics, identify tentative patterns, and propose future tests without pretending ordinary social-media analytics establish causality.

## Responsibility Boundary

`linkedin-performance-review` owns:

- preserving supplied raw performance data;
- transparent rate calculation;
- denominator disclosure;
- post-age / exposure awareness;
- within-sample comparison;
- median / distribution-aware summaries where useful;
- identification of possible patterns;
- classification of learning strength;
- outlier awareness;
- experiment-result summaries;
- future-test suggestions;
- uncertainty and caveat reporting;
- separating observation from explanation.

It does **not**:

- infer LinkedIn algorithm rules;
- claim one content feature caused performance from ordinary post comparisons;
- invent missing metrics;
- invent benchmarks;
- invent audience/network growth;
- silently compare posts with incompatible measurement windows;
- rewrite published posts;
- erase author voice to optimize short-term metrics;
- perform attribution modelling without appropriate data;
- treat correlation as causation;
- perform platform scheduling.

Related skills:

- `linkedin-calendar-planner` -> plans future publication timing/experiments;
- `linkedin-content-pipeline` -> orchestrates workflow;
- `research-insight-miner` -> creates research/content insights, not performance claims;
- `content-quality-gate` -> judges content quality before publication.

## Input Expectations

Prefer a dataset containing, where available:

- `post_id`;
- publication date/time;
- observation date/time;
- post age;
- impressions;
- unique viewers/reach if supplied;
- reactions;
- comments;
- reposts/shares;
- saves;
- clicks;
- profile views;
- follows;
- leads/conversions;
- format;
- topic/pillar;
- reader job;
- opening type;
- CTA type;
- link presence;
- organic/paid status;
- experiment ID / variant;
- network/follower size at publication if available.

Use only supplied metrics.

Missing data is missing data.

Do not convert absent values to zero unless the source explicitly means zero.

## Raw Data Preservation

Preserve original counts exactly.

Do not:

- alter counts;
- round raw counts;
- reconstruct missing counts;
- infer impressions from rates;
- infer saves from engagement;
- infer network size from reach.

Store raw values separately from derived values.

## Zero vs Missing Rule

Distinguish:

```text
0
```

from:

```text
null / not supplied
```

`0` means the metric was measured and no events occurred.

`null` means the metric is missing, unavailable, or not supplied.

Never replace `null` with `0`.

## Denominator Rule

Every derived rate must state its denominator.

Examples:

### Impression-based rate

```text
reaction_rate = reactions / impressions
comment_rate = comments / impressions
share_rate = shares / impressions
save_rate = saves / impressions
click_through_rate = clicks / impressions
profile_view_rate = profile_views / impressions
follow_rate = follows / impressions
lead_rate = leads / impressions
```

Use these only when the denominator is actually available and appropriate.

If reach/unique viewers is supplied and a rate is calculated against that denominator, label it explicitly.

Do not call two rates equivalent when their denominators differ.

## Rate Calculation

For rate:

```text
rate = numerator / denominator
```

Prefer storing:

- raw proportion;
- percentage for display;
- numerator;
- denominator.

Example:

```yaml
save_rate:
  numerator: 12
  denominator: 2400
  denominator_name: "impressions"
  proportion: 0.005
  percent: 0.5
```

If denominator is:

- missing;
- zero;
- incompatible;

set rate to `null` and explain why.

Do not divide by zero.

## Engagement Aggregates

Do not assume a universal definition of "engagement rate."

If creating an aggregate, define it explicitly.

Example:

```text
engagement_events = reactions + comments + shares + saves + clicks
engagement_rate = engagement_events / impressions
```

Only do this if:

- all included components are available;
- double-counting limitations are understood;
- the exact formula is documented.

If components are missing, do not silently treat them as zero.

Prefer component-specific rates when possible.

## Observation Window Rule

Post metrics are not comparable merely because they are in the same table.

Record or derive observation window when possible:

```text
post_age_hours
post_age_days
```

A post observed for 2 hours should not be directly treated as equivalent to a post observed for 14 days.

Classify comparability:

- `comparable`
- `partially_comparable`
- `not_comparable`
- `unknown`

If observation windows differ materially, either:

- use a common window if supplied;
- compare only metrics measured at equivalent windows;
- or downgrade the inference.

Do not invent normalized performance trajectories without time-series data.

## Exposure Rule

Impressions are exposure, not success by themselves.

When comparing outcome counts, consider exposure.

Example:

Post A:
- 20 saves
- 10,000 impressions

Post B:
- 15 saves
- 2,000 impressions

Raw saves alone and save rate tell different stories.

Report both when useful.

Do not rank posts solely by raw reactions if impression exposure differs substantially.

## Network Size Rule

If network/follower size differs across periods and is supplied, record it as context.

Do not invent network-size normalization.

Do not assume a larger network fully explains impression differences.

Use:

`possible contextual factor`

not:

`cause`.

## Paid vs Organic Rule

Do not directly compare paid and organic performance without labeling the difference.

Record:

- `organic`
- `paid`
- `mixed`
- `unknown`

Paid amplification may change exposure and audience composition.

Do not treat paid-vs-organic differences as evidence about content quality alone.

## Context Variables

Where supplied, consider:

- topic;
- pillar;
- format;
- reader job;
- post age;
- posting day/time;
- audience size;
- paid status;
- external events;
- campaign;
- link presence;
- CTA;
- opening mechanism;
- series position.

These are contextual variables, not automatically explanatory variables.

## Comparison Rule

Compare only when the comparison question is meaningful.

Examples:

- save rate across evidence-led vs application-led posts;
- comment rate across conversation vs evidence reader jobs;
- median click-through rate for link vs no-link posts;
- performance of explicit experiment variants.

Avoid arbitrary fishing across many features with tiny samples.

## Distribution-Aware Summary

When several posts are compared, prefer robust summaries such as:

- median;
- range;
- interquartile range when useful;
- count of posts;
- raw values.

Do not rely only on mean when one viral/outlier post dominates.

Do not call a difference stable when based on one post per group.

## Outlier Rule

Flag unusually high/low posts when they materially affect group summaries.

Do not automatically delete outliers.

Ask:

- is this a real post?;
- was it paid?;
- was an external event involved?;
- was exposure window different?;
- did it have unusual audience distribution?;

Keep outliers visible unless the user explicitly defines an exclusion rule.

## Small-Sample Rule

Sample size constrains what can be learned.

Examples:

### n = 1 vs n = 1

Use:

`insufficient data`

or:

`test next`

Do not call it a pattern.

### several posts with same direction

May support:

`tentative pattern`

depending on comparability.

### repeated, comparable observations with clear separation

May support:

`strong observation`

within this dataset.

Even a strong observation is not automatically causal.

## Learning Classes

Use exactly:

- `strong_observation`
- `tentative_pattern`
- `test_next`
- `insufficient_data`

### `strong_observation`

A clear descriptive pattern in the supplied dataset with enough comparable observations that it is reasonable to summarize confidently.

Example:

`Across 12 comparable posts, evidence-led posts had a higher median save rate than application-led posts.`

This does **not** mean the evidence-led format caused the difference.

### `tentative_pattern`

A possible recurring difference, but sample size, comparability, confounding, or variability limits confidence.

### `test_next`

A plausible question worth testing prospectively.

It is not a result.

### `insufficient_data`

The supplied data are too sparse, incompatible, incomplete, or confounded for a useful conclusion.

## Causal Guard

Ordinary LinkedIn analytics are observational.

Do not say:

- the hook caused more reach;
- the carousel caused more saves;
- posting Tuesday caused more engagement;
- the CTA generated more leads;
- LinkedIn rewarded the post;
- the algorithm preferred the topic.

Prefer:

- `Posts with X had a higher median Y in this sample.`
- `This pattern is worth testing prospectively.`
- `The difference could reflect topic, audience, timing, exposure, or other factors.`
- `These data do not isolate the effect of X.`

## Algorithm Guard

Performance data cannot reveal the internal LinkedIn algorithm.

Do not infer:

- ranking weights;
- hidden penalties;
- platform preferences;
- suppression;
- boost mechanisms.

A post receiving fewer impressions does not prove suppression.

A post receiving more impressions does not prove algorithmic preference.

## Explanation Boundary

Separate:

### Observation

`Evidence-led posts had a higher median save rate in this sample.`

### Possible explanation

`One possibility is that readers found those posts more reference-worthy.`

Only include an explanation when clearly labeled as hypothesis/speculation.

### Causal claim

`Evidence-led posts generated more saves because readers value research.`

Do not make this claim from ordinary analytics.

## Mechanism Rule

Do not invent audience psychology such as:

- readers trusted it more;
- users found it more useful;
- people were emotionally moved;
- the audience preferred authenticity;
- the algorithm rewarded dwell time;

unless separately supported.

If proposed, label as a hypothesis for future testing.

## Benchmark Rule

Do not invent industry benchmarks.

If no benchmark is supplied:

- compare the user's posts against each other;
- do not classify performance as "good", "poor", "above average", or "viral" using memory.

If an external benchmark is supplied:

- record source/date;
- check metric definition and denominator compatibility;
- do not compare incompatible metrics.

If current benchmark verification is requested, verify separately using appropriate current sources.

## Metric Direction Rule

Higher is not always inherently better.

Examples:

- impressions may be desirable but broad exposure can reduce rates;
- comments may be valuable but not all comments represent target-audience value;
- clicks may matter more for a traffic objective;
- saves may matter more for reference-oriented content;
- leads may matter more for commercial objectives.

Tie metric interpretation to the stated objective where available.

Do not optimize every post for every metric.

## Objective Rule

Prefer explicit post/campaign objectives.

Examples:

- awareness;
- conversation;
- saves/reference value;
- website traffic;
- profile discovery;
- follower growth;
- lead generation.

Judge relevant metrics against the objective.

If objective is missing:

- report descriptive performance;
- avoid declaring a winner solely from a generic engagement score.

## Experiment Review

If a calendar experiment is supplied:

- preserve experiment ID;
- preserve planned variable;
- preserve variants;
- preserve success metric;
- compare only the intended variable where feasible.

Do not upgrade an observational posting experiment into causal research.

Use:

`experimental content test`

or:

`planned content comparison`

rather than scientific causal language unless the design genuinely supports it.

## One-Major-Variable Rule

For future tests, prefer changing one major content variable at a time.

Examples:

- evidence-led vs application-led opening;
- CTA vs no CTA;
- text vs document format;
- broad morning window vs afternoon window.

Do not propose a test where simultaneously changing:

- topic;
- format;
- hook;
- CTA;
- posting time;
- length;

makes interpretation impossible.

## Multiple Comparisons / Fishing Rule

If many dimensions are explored:

- label exploratory findings;
- avoid presenting the single largest difference as definitive;
- note that chance variation becomes more likely when many comparisons are inspected.

Do not fabricate statistical significance tests.

## Statistical Testing Boundary

Do not automatically run inferential tests on tiny social-media samples.

Only use formal statistics when:

- sample size/design make them meaningful;
- user asks;
- assumptions are considered;
- interpretation remains appropriately cautious.

Do not use a p-value to manufacture certainty from weak observational data.

## Missing Metrics

When a metric is absent:

```yaml
value: null
reason: "not supplied"
```

Do not estimate it.

## Data Quality Flags

Use flags such as:

- `missing_observation_window`
- `unequal_observation_window`
- `missing_impressions`
- `zero_denominator`
- `mixed_paid_organic`
- `network_size_changed`
- `outlier_present`
- `small_group_n`
- `metric_definition_unclear`
- `incompatible_denominator`
- `external_event_possible`
- `experiment_variable_confounded`

## Output Location

Default:

`.knowledgecraft/analytics/linkedin-performance-review.yaml`

Optional readable summary:

`.knowledgecraft/analytics/linkedin-performance-review.md`

Do not write analytics artifacts into `.opencode/skills/`.

## Output Contract

Use:

```yaml
linkedin_performance_review:
  review_id: "LPRF-001"
  analysis_scope:
    start_date: null
    end_date: null
    post_count: 0
    objective: null
  metric_definitions:
    - metric: "save_rate"
      numerator: "saves"
      denominator: "impressions"
      formula: "saves / impressions"
  posts:
    - post_id: "POST-001"
      published_at: null
      observed_at: null
      observation_window_hours: null
      comparability: "comparable|partially_comparable|not_comparable|unknown"
      paid_status: "organic|paid|mixed|unknown"
      metadata:
        pillar: null
        reader_job: null
        format: null
        opening_type: null
        cta_type: null
        experiment_id: null
        experiment_variant: null
      raw_metrics:
        impressions: null
        reactions: null
        comments: null
        shares: null
        saves: null
        clicks: null
        profile_views: null
        follows: null
        leads: null
      derived_metrics:
        save_rate:
          numerator: null
          denominator: null
          denominator_name: "impressions"
          proportion: null
          percent: null
        comment_rate:
          numerator: null
          denominator: null
          denominator_name: "impressions"
          proportion: null
          percent: null
      data_quality_flags: []
  comparisons:
    - comparison_id: "CMP-001"
      question: ""
      groups:
        - label: ""
          post_ids: []
          n: 0
          summary_metrics: {}
      comparability: "comparable|partially_comparable|not_comparable|unknown"
      descriptive_result: ""
      caveats: []
  learnings:
    - learning_id: "LRN-001"
      classification: "strong_observation|tentative_pattern|test_next|insufficient_data"
      statement: ""
      supporting_post_ids: []
      supporting_comparison_ids: []
      evidence_basis: ""
      confounders_or_alternatives: []
      reusable: true
  future_tests:
    - test_id: "TEST-001"
      question: ""
      major_variable: ""
      variants: []
      primary_metric: null
      controls_or_constants: []
      interpretation_guard: "Observational content test; do not infer causality from post-to-post differences alone."
  global_data_quality:
    issues: []
    overall_comparability: "comparable|partially_comparable|not_comparable|unknown"
  summary:
    strongest_observation: null
    most_useful_tentative_pattern: null
    highest_priority_test_next: null
    insufficient_data_questions: []
  handoff:
    ready_for_reuse: true
    next_skill: "linkedin-series-architect"
    notes: []
```

## Learning Traceability

Every learning must identify:

- supporting posts;
- supporting comparison(s), where applicable;
- evidence basis;
- confounders/alternative explanations.

Do not write a generic learning with no traceability.

## Reusability Rule

Set:

`reusable: true`

only when the learning is appropriately qualified and useful for future planning.

A learning can be reusable even when tentative, provided its uncertainty remains attached.

Do not turn:

`tentative_pattern`

into a permanent content rule downstream.

## Strong Observation Threshold

There is no universal numeric threshold.

Use judgment based on:

- number of posts;
- comparability;
- consistency;
- magnitude;
- outliers;
- missingness;
- exposure;
- alternative explanations.

When uncertain, downgrade.

## Performance Does Not Override Voice

Do not conclude:

`Use more sensational hooks because they received more impressions.`

without considering:

- objective;
- evidence safety;
- author voice;
- content quality;
- audience relevance;
- sample size.

Performance learning should improve decision-making, not turn the content system into engagement chasing.

## Handoff Rule

A review may hand reusable learnings back to:

`linkedin-series-architect`

only when:

- calculations are complete where possible;
- raw metrics are preserved;
- denominators are explicit;
- observation-window comparability is considered;
- causal claims are absent;
- learning classifications match evidential strength;
- unresolved data-quality issues remain attached.

If data are too incomplete for reusable learning:

```yaml
ready_for_reuse: false
```

Do not manufacture recommendations to force a handoff.

## Deterministic Validation

After writing the structured performance-review YAML, validate its mechanical consistency before reporting completion.

Run:

```powershell
py ".opencode/skills/linkedin-performance-review/scripts/validate_linkedin_performance_review.py" ".knowledgecraft/analytics/linkedin-performance-review.yaml"
```

If validation returns `FAIL`:

1. do not report the review as complete;
2. read every validation error;
3. repair only the affected YAML, arithmetic, denominator, traceability, experiment, classification, or handoff fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- valid YAML and required top-level structure;
- `analysis_scope.post_count` matches the number of post records;
- unique post, comparison, learning, and future-test IDs;
- raw metrics are non-negative integers or null;
- zero remains distinct from null;
- derived rates use explicit numerator, denominator, denominator name, proportion, and percent;
- known impression-based derived rates match the corresponding raw numerator and impression denominator;
- denominator zero or missing cannot produce a numeric rate;
- missing numerator cannot silently become zero;
- `proportion = numerator / denominator`;
- `percent = proportion * 100`;
- observation-window hours agree with supplied publication/observation timestamps when both are parseable;
- comparability and paid-status values use allowed vocabulary;
- comparison post IDs exist and group `n` matches listed post IDs;
- learning classifications use the allowed vocabulary;
- learning supporting post/comparison IDs exist;
- `strong_observation` cannot be supported by fewer than two posts;
- future tests contain one named major variable, at least two variants, and an interpretation guard;
- experiment IDs used by posts are preserved as identifiers rather than silently changed;
- handoff readiness is not allowed when the artifact is mechanically invalid;
- ready handoff points to `linkedin-series-architect`.

The validator intentionally does **not** decide whether:

- a descriptive pattern deserves `strong_observation` rather than `tentative_pattern`;
- two observation windows are substantively comparable;
- an outlier is scientifically important;
- paid/organic differences are adequately controlled;
- a benchmark is trustworthy;
- an algorithmic or causal statement is semantically overclaimed;
- a future test truly changes only one major variable.

Those remain semantic/reviewer responsibilities.

## Minimal Analysis Rule

Do not calculate every possible metric merely because it is available.

Focus on:

- the user's objective;
- metrics relevant to that objective;
- comparisons with enough data to be meaningful.

Avoid analytics theater.

## Review Procedure

1. load supplied performance data;
2. preserve raw values exactly;
3. distinguish zero from missing;
4. define relevant metrics and denominators;
5. calculate valid rates;
6. identify observation windows;
7. assess comparability;
8. identify paid/organic/context differences;
9. summarize individual-post performance;
10. create only meaningful comparisons;
11. inspect outliers and small groups;
12. separate observations from explanations;
13. classify learnings;
14. propose minimal future tests;
15. attach confounders and data-quality caveats;
16. verify no causal/algorithmic claims;
17. produce reusable handoff only when warranted.

## Final Checks

Before completing the review, verify:

- raw counts preserved? YES
- zero distinguished from missing? YES
- no missing metric converted to zero? YES
- denominators explicit? YES
- no division by zero? YES
- derived rates mathematically coherent? YES
- observation windows considered? YES
- incompatible windows not treated as equivalent? YES
- exposure considered when comparing counts? YES
- paid vs organic labeled where known? YES
- network-size/context changes not treated as causes? YES
- outliers retained/flagged rather than silently removed? YES
- group sample sizes reported? YES
- tiny samples not called strong patterns? YES
- comparisons traceable to post IDs? YES
- learning classifications justified? YES
- no causal claims from ordinary analytics? YES
- no LinkedIn algorithm rules inferred? YES
- no unsupported audience psychology invented? YES
- no industry benchmarks invented? YES
- metric interpretation tied to objective where available? YES
- exploratory fishing not presented as confirmation? YES
- future tests alter one major variable where possible? YES
- experimental comparisons retain causal guard? YES
- performance learning does not override evidence safety/voice? YES
- handoff readiness matches data quality? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- generated artifacts saved outside `.opencode/skills/`? YES
