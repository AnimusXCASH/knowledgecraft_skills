---
name: content-quality-gate
description: Perform a final publication-readiness review for professional or research-grounded content. Use after factual, voice, naturalness, and platform editing to return an APPROVE, REVISE, or BLOCK decision.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "final-qa"
  opencode/slash: "false"
---

# Content Quality Gate
Score 0–3 for factuality, specificity, usefulness, voice match, naturalness, destination/platform fit, and novelty within the current series.

BLOCK for fabricated/unsupported factual claims, invented personal experience, materially misleading openings, unattributed quotation/plagiarism, confidential content, or claims materially stronger than evidence.

REVISE for any score below 2, substantial overlap with another item, vague audience, generic CTA, unnecessary filler/jargon, or repeated opening pattern.

APPROVE only when there is no block condition, every dimension is at least 2, and total score is at least 17/21. Specify the smallest required changes rather than rewriting everything inside QA.
