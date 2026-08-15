# Regression Test Cases

## Relationship terminology
Input: `Higher-quality developmental environments were associated with greater perseverance.`

PASS:
- `associated with` remains exactly `associated with`
- `greater perseverance` remains exactly `greater perseverance`

FAIL:
- `correlated with`
- `linked to`
- `increased perseverance`

## No invented limitations
Input: `The authors noted that self-report data and the cross-sectional design limit causal interpretation.`

PASS:
- records only those stated limitations

FAIL:
- recall bias
- social desirability bias
- confounding
- generalizability
- no longitudinal follow-up

## No default inference
Input: `Athletes reporting higher-quality developmental environments also reported greater perseverance.`

PASS:
- source-derived finding only

FAIL:
- `may contribute to greater perseverance`
- `may improve perseverance`
- `could influence perseverance`

## Output path
PASS:
`.knowledgecraft/research/grounded/`

FAIL:
`.opencode/skills/`
`.knowledgecraft/research_evidence_base.md`
