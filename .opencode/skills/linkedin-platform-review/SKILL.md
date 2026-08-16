---
name: linkedin-platform-review
description: Review and lightly edit a LinkedIn post for platform presentation, first-screen clarity, mobile readability, formatting, CTA fit, mentions, hashtags, links, and content-format suitability while preserving substance and avoiding unverified algorithm folklore.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "platform-review"
  opencode/slash: "false"
---

# LinkedIn Platform Review

Review a drafted LinkedIn post for **LinkedIn-specific presentation** while keeping its substantive meaning intact.

This skill is a platform-fit editor, not a research interpreter, factuality checker, voice profiler, or engagement-hack generator.

## Responsibility Boundary

`linkedin-platform-review` owns:

- first-screen clarity;
- opening presentation;
- mobile readability;
- paragraph density;
- line-break use;
- list readability;
- CTA fit;
- mention fit;
- hashtag restraint/relevance;
- external-link presentation;
- post-format suitability;
- obvious engagement bait;
- avoidable platform-friction in presentation;
- light edits that preserve meaning.

It does **not**:

- create or strengthen scientific claims;
- change causal or relationship language;
- invent mechanisms;
- add new evidence;
- invent citations;
- perform author-voice profiling;
- perform full voice rewriting;
- perform detector-oriented humanization;
- decide factual truth;
- perform final content-quality approval;
- claim knowledge of LinkedIn's current ranking system without verification;
- schedule the post.

Related skills:

- `linkedin-post-drafter` -> creates the first evidence-safe draft;
- `author-voice-editor` -> aligns the text with the author's evidence-based voice profile;
- `text-naturalness-editor` -> removes mechanical/generic prose conservatively;
- `factuality-guard` -> verifies factual fidelity after platform edits;
- `content-quality-gate` -> makes the final APPROVE / REVISE / BLOCK decision;
- `linkedin-calendar-planner` -> schedules approved posts.

## Input Expectations

Prefer:

- one complete LinkedIn draft;
- audience;
- reader job;
- evidence mode;
- intended ending function;
- optional recommended format;
- optional author constraints;
- optional prior series context.

If the input is incomplete, review what is available and identify the missing platform-relevant information.

Do not fill missing factual or personal content.

## Substance Preservation Rule

Keep the post's substantive meaning intact.

Do not change:

- names;
- dates;
- numbers;
- units;
- statistics;
- citations;
- technical constructs;
- population;
- direction;
- magnitude;
- relationship terminology;
- causal status;
- uncertainty;
- limitation language;
- factual attribution.

Do not turn:

`was associated with`

into:

- linked to;
- led to;
- reduced;
- improved;
- predicted;
- caused.

Do not turn descriptive wording such as:

`athletes who reported X also reported Y`

into a technical relationship label unless that label is already authorized.

If a presentation improvement would require changing substantive meaning, do not make that edit.

Flag it for the appropriate upstream/downstream skill instead.

## Light-Edit Rule

Prefer the smallest platform-specific edit that solves the problem.

Allowed examples:

- split a dense paragraph;
- remove unnecessary blank lines;
- move an existing clear sentence earlier;
- shorten a generic opening without changing the claim;
- convert genuinely list-shaped material into bullets;
- remove a forced CTA;
- remove irrelevant hashtags;
- clarify the visible structure;
- recommend a different post format without rewriting the evidence.

Do not perform a broad rewrite merely because the post could sound different.

## First-Screen Clarity

The opening portion should quickly establish what the post is about and why it deserves attention.

Check:

- is the topic identifiable early?;
- is the opening understandable without several setup paragraphs?;
- does the opening overclaim?;
- does it rely on vague suspense?;
- is important context hidden too far down?;
- would a small reordering improve orientation?;

Do not require a "hook" template.

A direct, specific opening is acceptable.

A careful scientific opening is acceptable.

Do not manufacture drama.

## Opening Safety

A platform-friendly opening cannot be stronger than the body evidence.

Reject openings such as:

- `This changes everything.`
- `We finally know what causes dropout.`
- `Your coaching environment determines athlete grit.`

when the supplied content does not support them.

A cautious body does not repair an unsafe opening.

If the opening creates a new claim, remove or revise it.

## Mobile Readability

Review the post as something likely read on a phone.

Check:

- paragraph length;
- visual density;
- long unbroken blocks;
- excessive one-line fragments;
- awkward bullet wrapping;
- excessive spacing;
- headings that add clutter;
- sentence fragments used only for effect.

Do not enforce a rigid "one sentence per paragraph" style.

Mobile readability means readable structure, not maximal fragmentation.

## Paragraph Rule

Use paragraph breaks when the rhetorical or logical unit changes.

Avoid both extremes:

### Too dense

One large block that combines:

- setup;
- finding;
- interpretation;
- implication;
- CTA.

### Too fragmented

A sequence like:

```text
Perseverance matters.

But context matters too.

A lot.

More than we think.

Maybe.
```

unless the author's established voice and content genuinely justify it.

## List Rule

Use bullets only when the content is actually list-shaped.

Do not convert ordinary prose into three bullets simply because LinkedIn posts often use bullets.

Do not create artificial "3 lessons", "5 takeaways", or numbered frameworks from content that was not structured that way.

## CTA Rule

A CTA is optional.

Evaluate whether the ending fits the post's reader job.

Good options may include:

- concise takeaway;
- genuine reflective question;
- specific practical question;
- next step;
- synthesis;
- unresolved tension;
- no CTA.

Remove or revise low-value engagement bait such as:

- `Agree?`;
- `Thoughts?`;
- `Comment YES if...`;
- `Tag someone who needs this`;
- `Like and share if you agree`;
- `What do you think?` when disconnected from the post.

Do not add a CTA when the supplied ending function is `no CTA`.

## Engagement-Bait Rule

Flag attempts whose primary function is to manipulate reactions rather than help the reader.

Examples:

- reaction voting;
- comment-to-receive gimmicks;
- arbitrary tagging requests;
- forced "agree/disagree" prompts;
- inflated controversy;
- fake scarcity or urgency.

Do not confuse every question with engagement bait.

A substantive question can be appropriate.

## Hashtag Rule

Hashtags are optional.

Check only:

- relevance;
- duplication;
- excessive quantity;
- overly broad tags;
- misleading tags;
- tags that add no discoverability/context value.

Do not enforce a permanent "best number of hashtags."

Do not claim a specific hashtag count improves reach unless that claim has been verified for the current platform context.

If hashtags are not helping the post, recommend none.

## Mention Rule

Mentions should be genuinely relevant.

Do not add people or organizations merely to increase visibility.

Do not invent handles.

Do not tag:

- uninvolved people;
- prominent figures for attention;
- organizations not actually connected to the content.

If an exact LinkedIn handle is not supplied or verified, do not fabricate it.

## External-Link Rule

Do not assume external links are always penalized.

Treat link placement as a presentation/measurement choice unless current official or otherwise appropriate evidence is supplied.

Review:

- whether the link interrupts the post;
- whether the reader understands why it is included;
- whether a source/reference should be named in text;
- whether the user explicitly wants the link in the body, comments, or elsewhere.

Do not move a link solely because of platform folklore.

## Format Suitability

Evaluate whether the content naturally fits:

- text post;
- document/carousel;
- image + text;
- chart/figure-led post;
- article/newsletter;
- short list;
- narrative post.

Recommend a different format only when it serves the content.

Examples:

- multi-step framework -> document/carousel may be useful;
- single clear research finding -> text post may be sufficient;
- figure is central to comprehension -> figure/chart-led post may fit;
- long technical argument -> article/newsletter may deserve consideration.

Do not claim one format will receive more reach unless current evidence is supplied or verified.

## Platform Folklore Guard

Do not encode permanent rules such as:

- `links kill reach`;
- `three hashtags is optimal`;
- `Tuesday morning is best`;
- `carousels always outperform text`;
- `LinkedIn rewards short posts`;
- `the algorithm prefers comments over saves`;
- `editing a post after publishing reduces reach`.

Platform behavior changes and many public claims are weakly supported.

If a recommendation materially depends on a **current LinkedIn platform fact**, then:

1. verify it from current official LinkedIn guidance when verification tools are available; or
2. mark it `needs_current_verification`; or
3. make the recommendation without relying on that platform claim.

Do not silently convert folklore into policy.

## Current-Fact Verification Boundary

Distinguish:

### Stable presentation judgment

Examples:

- paragraph is visually dense;
- CTA is generic;
- hashtag is irrelevant;
- link interrupts the sentence;
- opening is vague.

These can be reviewed directly.

### Time-sensitive platform claim

Examples:

- maximum current post length;
- current document upload limits;
- current supported file types;
- current hashtag behavior;
- current ranking-system claims;
- current newsletter eligibility;
- current link-preview behavior.

Do not assert these from memory when they materially affect the recommendation.

Record:

```yaml
verification_status: "not_needed|verified|needs_current_verification"
```

## Scientific / Evidence Safety

Platform editing must not alter evidence meaning.

Preserve:

- exact relationship wording;
- causal guard;
- uncertainty;
- distinction between finding and interpretation;
- distinction between interpretation and recommendation;
- explicit limitations;
- citation attachment.

Do not shorten away a limitation when doing so would make the remaining claim stronger.

Do not make a scientific post "punchier" by removing necessary qualification.

## Voice Boundary

Do not use this skill to recreate the author's voice.

Minor stylistic changes for platform readability are allowed.

If the post needs substantial voice repair, route to:

`author-voice-editor`

If the post sounds mechanically written, route to:

`text-naturalness-editor`

Do not duplicate those skills.

## Naturalness Boundary

Do not add:

- intentional mistakes;
- fake slang;
- artificial sentence-length variation;
- excessive fragments;
- personal anecdotes;
- rhetorical questions;

merely to make the post feel "human."

Platform review is about presentation, not detector evasion.

## Series Awareness

If series context is supplied, check for obvious platform-level repetition:

- same opening mechanism;
- same first line;
- same CTA;
- same bullet layout;
- same ending;
- same visible rhythm.

Do not redesign the whole series.

Flag repeated presentation patterns for `linkedin-series-architect` if the issue is structural across multiple posts.

## Platform Review Status

Use exactly one:

- `pass`
- `revise`
- `needs_current_verification`

### `pass`

Use when the post is platform-presentable and no material platform issue remains.

### `revise`

Use when platform-specific presentation edits are needed.

A revised version may be supplied.

### `needs_current_verification`

Use only when a material recommendation depends on a current platform feature/rule that has not been verified.

Do not use this status for ordinary writing uncertainty.

## Issue Types

Use issue types such as:

- `opening_unclear`
- `opening_overclaim`
- `mobile_density`
- `over_fragmented`
- `list_misuse`
- `cta_forced`
- `engagement_bait`
- `hashtag_irrelevant`
- `hashtag_excessive`
- `mention_irrelevant`
- `mention_unverified`
- `link_interrupts_flow`
- `format_mismatch`
- `platform_claim_unverified`
- `series_presentation_repetition`
- `substance_change_required`

Do not create issue types merely to sound detailed.

## Output Location

Default:

`.knowledgecraft/content/drafts/<post_id>-platform-review.yaml`

Do not write generated reviews into `.opencode/skills/`.

## Output Contract

Use:

```yaml
linkedin_platform_review:
  review_id: "LPR-001"
  post_id: "POST-001"
  platform_status: "pass|revise|needs_current_verification"
  destination: "LinkedIn"
  original_text: |
    ...
  revised_text: |
    ...
  issues:
    - issue_id: "LPRI-001"
      issue_type: "opening_unclear"
      severity: "low|medium|high"
      location: "opening|body|ending|hashtags|mentions|link|format|series"
      issue_status: "open|resolved|advisory"
      explanation: ""
      change_required: true
      suggested_action: ""
  platform_checks:
    first_screen_clear: true
    mobile_readable: true
    paragraphing_appropriate: true
    lists_content_shaped: true
    cta_appropriate: true
    engagement_bait_absent: true
    hashtags_relevant_or_absent: true
    mentions_relevant_or_absent: true
    link_treatment_reasonable: true
    format_fit_reasonable: true
  current_platform_claims:
    - claim: ""
      material_to_decision: true
      verification_status: "not_needed|verified|needs_current_verification"
      source_note: null
  preservation_checks:
    substantive_meaning_preserved: true
    names_dates_numbers_preserved: true
    technical_terms_preserved: true
    relationship_language_preserved: true
    causal_status_preserved: true
    uncertainty_preserved: true
    limitations_preserved: true
    citations_preserved: true
    no_new_claims: true
    no_personal_experience_invented: true
  handoff:
    ready_for_factuality_review: true
    next_skill: "factuality-guard"
    notes: []
```

## Original vs Revised Text

`original_text` must preserve the exact input text.

`revised_text` contains only the platform-oriented revision.

If no edits are needed:

```yaml
revised_text: |
  <same text as original>
```

Do not silently omit the original.

## Issue Severity

Use:

### `low`

Minor presentational improvement.

### `medium`

Material readability, clarity, CTA, or format problem that should be fixed before publication.

### `high`

A platform-facing problem that materially distorts the post or prevents a safe presentation, such as:

- a causal/unsupported opening added for attention;
- substantive meaning would have to change to make the proposed presentation work;
- a material recommendation depends on an unverified current platform rule.

Do not use severity as a substitute for factuality review.

## Issue Status

Use:

- `open` -> still requires action before platform review can pass;
- `resolved` -> issue was identified and corrected in `revised_text`;
- `advisory` -> observation worth recording but not required for platform readiness.

If `change_required: true`, the issue cannot remain `advisory`.

A `pass` review may retain resolved/advisory issues, but must not retain any `open` issue with `change_required: true`.

## Status Logic

Use `revise` when:

- one or more issues require platform edits;
- all required edits can be made without changing substantive meaning.

Use `needs_current_verification` when:

- a material platform recommendation depends on an unverified current fact.

Use `pass` when:

- no material platform issue remains;
- no material current-platform claim is unresolved.

If you revise the text successfully during the review and no issue remains, `pass` is allowed, but keep the resolved issue entries and describe the edits.

## Handoff Rule

Set:

`ready_for_factuality_review: true`

only when:

- platform status is `pass`;
- revised text is complete;
- no material current-platform verification is unresolved;
- substantive meaning is preserved;
- relationship and causal language are preserved;
- no new claim or personal experience was introduced.

Otherwise set it false.

The next substantive QA step is:

`factuality-guard`

Do not skip factuality review merely because the platform review passed.

## Minimal Intervention Rule

Do not make edits merely to demonstrate activity.

If the draft is already clear, readable, restrained, and appropriate for LinkedIn:

- leave it substantially unchanged;
- return `pass`;
- explain that no material platform edit was necessary.

## Deterministic Validation

After writing the structured platform-review YAML, validate its mechanical consistency before reporting completion.

Run:

```powershell
py ".opencode/skills/linkedin-platform-review/scripts/validate_linkedin_platform_review.py" ".knowledgecraft/content/drafts/<post_id>-platform-review.yaml"
```

If validation returns `FAIL`:

1. do not report the platform review as complete;
2. read every validation error;
3. repair only the affected YAML, issue status, platform-check, verification, preservation, or handoff fields;
4. rerun the validator;
5. continue until `PASS`.

The validator checks:

- valid YAML and required top-level structure;
- non-empty review/post IDs;
- `destination: LinkedIn`;
- allowed platform status;
- non-empty original and revised text;
- issue IDs are unique;
- issue type, severity, location, issue status, explanation, and action fields are structurally valid;
- `change_required: true` cannot be `advisory`;
- `pass` cannot retain open required-change issues;
- `revise` must contain at least one open required-change issue;
- every platform check is present and boolean;
- every preservation check is present and boolean;
- `pass` requires safe platform and preservation checks;
- current-platform claim records use allowed verification statuses;
- material unresolved current-platform claims prevent `pass`;
- `needs_current_verification` requires at least one material unresolved platform claim;
- `verified` current-platform claims include a source note;
- handoff readiness agrees with platform status, unresolved verification state, and preservation safety;
- ready handoff points to `factuality-guard`.

The validator does **not** determine whether:

- the actual prose is mobile-readable;
- an opening is semantically overclaimed;
- a hashtag or mention is genuinely relevant;
- a link recommendation is strategically good;
- a platform claim is factually verified by the cited source note;
- a scientific phrase was subtly changed in meaning.

Those remain semantic/reviewer responsibilities.

## Review Procedure

1. read the entire draft;
2. identify the audience and reader job;
3. freeze substantive claims and protected details;
4. inspect the opening;
5. inspect mobile readability and paragraphing;
6. inspect lists;
7. inspect ending/CTA;
8. inspect hashtags;
9. inspect mentions;
10. inspect link treatment;
11. inspect format fit;
12. identify any current platform claims needed for the recommendation;
13. verify or flag time-sensitive platform claims;
14. make only necessary platform edits;
15. compare revised text against original;
16. verify evidence/causal/uncertainty preservation;
17. set platform status;
18. produce safe handoff.

## Final Checks

Before completing the review, verify:

- one post reviewed? YES
- original text preserved in output? YES
- substantive meaning preserved? YES
- opening clear without overclaiming? YES
- mobile readability reasonable? YES
- paragraphing not too dense or fragmented? YES
- lists used only when content is list-shaped? YES
- CTA appropriate or intentionally absent? YES
- engagement bait absent? YES
- hashtags relevant/restrained or absent? YES
- mentions relevant/verified or absent? YES
- link treatment based on flow, not folklore? YES
- format recommendation serves content? YES
- no ranking/reach folklore asserted as fact? YES
- time-sensitive platform claims verified or flagged? YES
- no names/dates/numbers/statistics changed? YES
- relationship terminology preserved? YES
- causal status preserved? YES
- uncertainty and limitations preserved? YES
- citations preserved? YES
- no new claims added? YES
- no personal experience invented? YES
- no detector-oriented editing? YES
- handoff consistent with platform status? YES
- deterministic validator executed? YES
- deterministic validator returned PASS? YES
- generated artifact saved outside `.opencode/skills/`? YES
