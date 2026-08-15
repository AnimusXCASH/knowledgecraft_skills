---
name: text-naturalness-editor
description: Conservatively edit drafted prose to remove generic, repetitive, templated, inflated, or overly polished LLM-style phrasing while preserving factual meaning and the existing author voice. Use as a pipeline editing component rather than a detector-evasion tool.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "naturalness-editing"
  opencode/slash: "false"
---

# Text Naturalness Editor
Improve specificity, cadence, transitions, lexical precision, stance, paragraph architecture, and redundancy only where doing so improves the prose.

Replace vague abstractions with supported concrete detail; fix obvious runs of identical sentence structure; remove mechanical connectors; prefer accurate/simple/domain language over inflated phrasing; clarify evidence vs interpretation vs recommendation; group related reasoning; cut restatements that add nothing.

Never invent anecdotes/emotions, add typos, insert invisible characters, corrupt grammar, use translation loops, optimize detector scores, or mechanically ban words because they sometimes occur in AI writing.
