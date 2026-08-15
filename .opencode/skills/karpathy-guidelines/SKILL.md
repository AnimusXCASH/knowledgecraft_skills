---
name: karpathy-guidelines
description: Foundation coding-behavior guidelines adapted from the MIT-licensed multica-ai/andrej-karpathy-skills project. Use when writing, reviewing, debugging, or refactoring code to surface assumptions, prefer simple solutions, keep changes narrowly scoped, and verify success with concrete checks.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "foundation"
  upstream: "multica-ai/andrej-karpathy-skills"
  adapted: "true"
  opencode/slash: "false"
---

# Karpathy Guidelines

Foundation guidance for coding tasks. This KnowledgeCraft version is an adapted summary of the MIT-licensed `karpathy-guidelines` skill from `multica-ai/andrej-karpathy-skills`, itself derived from Andrej Karpathy's public observations about common LLM coding failures.

Use judgment for trivial one-line tasks; the purpose is to reduce costly mistakes on non-trivial work, not to create ceremony.

## 1. Clarify before implementation

Before changing code:

- Identify assumptions that materially affect the solution.
- Do not silently choose between plausible interpretations when the distinction matters.
- Surface trade-offs or uncertainty that could change the implementation.
- Prefer resolving important ambiguity before building on top of it.
- If the requested approach is needlessly complex, point out the simpler alternative.

## 2. Prefer the simplest adequate solution

Solve the current problem with the least complexity that reliably meets the requirement.

- Avoid speculative features.
- Avoid abstractions that exist only for hypothetical future reuse.
- Do not add configuration merely to appear flexible.
- Keep interfaces and control flow as small as the task allows.
- If the implementation becomes much larger than the problem warrants, simplify it.

## 3. Keep changes surgical

When modifying an existing project:

- Change only what is necessary for the request.
- Preserve surrounding conventions and style unless the user asked for broader refactoring.
- Do not clean up unrelated code as a side effect.
- Remove only the dead imports, variables, or helpers made obsolete by your own change.
- Be able to explain how each meaningful change contributes to the requested outcome.

## 4. Work toward verifiable completion

Translate implementation requests into observable success criteria.

For non-trivial work:

1. Define the outcome that must be true.
2. Choose a check that demonstrates it.
3. Implement the smallest change needed.
4. Run or inspect the check.
5. Continue only if the criterion is not yet met.

Prefer concrete verification such as tests, reproduction steps, validation scripts, type checks, builds, or before/after behavior over vague confidence that the change "should work".

## KnowledgeCraft integration

Apply this skill primarily to coding, scripts, schemas, automation, tests, and repository maintenance.

It does **not** override domain-specific KnowledgeCraft skills. For example:

- research claims still follow `research-source-grounder` and `factuality-guard`;
- writing still follows author-voice and naturalness skills;
- LinkedIn work still follows the LinkedIn-specific review skills.

The foundation rule is simple: **understand the task, avoid unnecessary complexity, limit scope, and verify the result.**
