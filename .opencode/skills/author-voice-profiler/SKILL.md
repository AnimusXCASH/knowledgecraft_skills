---
name: author-voice-profiler
description: Build a reusable author voice profile from genuine writing samples such as past posts, emails, notes, articles, or transcripts. Use when repeated writing should consistently sound like a real author rather than a generic persona.
license: MIT
compatibility: opencode
metadata:
  collection: "knowledgecraft-skills"
  stage: "voice-modeling"
  opencode/slash: "false"
---

# Author Voice Profiler
Infer style only from genuine supplied samples. Prefer 8–20 substantial samples; 3–7 supports medium confidence; fewer than 3 is provisional.

Profile stable traits: formality, directness, sentence rhythm, paragraphing, first-person use, contractions, questions, humor, emotional intensity, punctuation, transitions, domain vocabulary, hedging, storytelling, CTA style, emoji style, recurring phrases, and consistently avoided styles.

Do not encode typos, accidental grammar errors, copied wording, one-off formatting, or unsupported personality assumptions. Return confidence and sample evidence for high-impact traits.
