# Contributing
New skills should solve one reusable problem well.

1. Create `.opencode/skills/<skill-id>/SKILL.md`.
2. Use a lowercase kebab-case ID.
3. Include a clear description so OpenCode can route correctly.
4. Explain when the skill should and should not be used.
5. Keep source/claim integrity explicit when handling research.
6. Add references/scripts only when they improve reliability.
7. Run `python validate_skills.py`.

Do not contribute private datasets/papers, personal voice samples, detector-evasion tricks, fabricated examples/citations, or unstable ranking folklore presented as fact.

## Coding contributions

For implementation changes, follow `karpathy-guidelines`: keep scope narrow, avoid speculative abstraction, and add or run a concrete verification step where practical.
