---
name: factuality-guard
description: Audit drafted text against source evidence or a claim ledger. Use before publication when writing contains statistics, research findings, dates, named entities, quotations, causal claims, or other externally checkable statements.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "factual-qa"
  opencode/slash: "false"
---

# Factuality Guard
Treat every externally checkable statement as a claim. Link it to evidence and check number, unit, date, population, direction, magnitude, causal language, attribution, quotation fidelity, and uncertainty.

Assign `SUPPORTED`, `OVERSTATED`, `UNSUPPORTED`, `CONFLICTING`, or `NEEDS_SOURCE`.

Source summaries do not authorize stronger claims. Association must not become causation. Examples are not universal rules. Do not fabricate references. Personal claims require supplied evidence or author confirmation. Materially unsupported/overstated claims block publication.
