#!/usr/bin/env python3
"""
Deterministic validator for KnowledgeCraft research-insight-miner outputs.

Validates:
- exact insight schema
- source/claim traceability
- grounded source limitations
- hypothesis inference level
- null relationship-language protection
- verbatim reuse of null-relationship findings
- unsupported explanatory phrasing
- output location

Usage:
  py validate_insights.py PATH_TO_INSIGHTS.yaml
  py validate_insights.py PATH_TO_INSIGHTS.yaml --claims PATH_TO_CLAIM_LEDGER.yaml
  py validate_insights.py PATH_TO_INSIGHTS.yaml --claims-dir PATH_TO_GROUNDED_DIR
"""

from __future__ import annotations

import argparse
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: py -m pip install pyyaml")
    raise SystemExit(2)


REQUIRED_FIELDS = [
    "insight_id",
    "insight_type",
    "insight",
    "supporting_claim_ids",
    "source_ids",
    "inference_level",
    "evidence_basis",
    "audience",
    "audience_problem_or_decision",
    "practical_or_conceptual_consequence",
    "angle",
    "novelty_reason",
    "source_limitations",
    "insight_risks",
    "author_input_needed",
    "allowed_for_reuse",
]

ALLOWED_INSIGHT_TYPES = {
    "synthesis",
    "implication",
    "hypothesis",
    "evidence_gap",
    "tension",
    "application_question",
    "communication_angle",
    "decision_framework",
    "misconception_correction",
}

ALLOWED_INFERENCE_LEVELS = {"low", "moderate", "high"}

# Terms that must not be invented when a supporting grounded finding has
# relationship_language: null.
FORBIDDEN_NULL_RELATIONSHIP_PATTERNS = [
    r"\bassociation\b",
    r"\bassociations\b",
    r"\bassociated with\b",
    r"\bcorrelation\b",
    r"\bcorrelations\b",
    r"\bcorrelated with\b",
    r"\brelationship\b",
    r"\brelationships\b",
    r"\blinked to\b",
    r"\blinks? between\b",
    r"\brelates? to\b",
    r"\brelated to\b",
    r"\brelated claims?\b",
    r"\bco-?occurs? with\b",
    r"\bco-?occurrence\b",
    r"\bobserved together\b",
    r"\breported together\b",
    r"\bfound together\b",
    r"\bpaired reporting\b",
    r"\bpaired pattern\b",
    r"\breporting pattern\b",
    r"\bobserved pattern\b",
    r"\bshared pattern\b",
    r"\bcorresponding pattern\b",
    r"\bconnection\b",
    r"\blinkage\b",
    r"\bpairing\b",
    r"\binterplay\b",
    r"\baccompanies\b",
    r"\bcorresponds with\b",
    r"\btracks with\b",
    r"\bgoes with\b",
    r"\baligns with\b",
    r"\bconnected with\b",
    r"\btied to\b",
    r"\bpredict(?:s|ed|ing|ion|ions|ive|ively)?\b",
    r"\balongside\b",
    r"\bco[- ]presence\b",
    r"\bpresent alongside\b",
    r"\bappears? alongside\b",
    r"\boccurs? alongside\b",
    r"\bfound alongside\b",
]

UNSUPPORTED_EXPLANATION_PATTERNS = [
    r"\bmay reflect\b",
    r"\bmay be due to\b",
    r"\bmay result from\b",
    r"\bmay be explained by\b",
]

FORBIDDEN_NOT_ESTABLISHED_CAUSAL_PATTERNS = [
    r"\bnon[- ]causal\b",
    r"\bno causal relationship\b",
    r"\bdoes not cause\b",
    r"\bdo not cause\b",
    r"\bcannot cause\b",
]

FORBIDDEN_CROSS_SOURCE_COMPARATIVE_PATTERNS = [
    r"\breplicat(?:e|ed|es|ion|ions)\b",
    r"\bconfirm(?:s|ed|ation)?\b",
    r"\bconsistent\b",
    r"\bconsistency\b",
    r"\bconvergent\b",
    r"\bconvergence\b",
    r"\bcontradictory\b",
    r"\bcontradiction\b",
    r"\bconflicting\b",
    r"\bconflict\b",
]

STUDY_DESIGN_PATTERNS = {
    "cross-sectional": r"\bcross[- ]sectional\b",
    "longitudinal": r"\blongitudinal\b",
    "prospective": r"\bprospective\b",
    "retrospective": r"\bretrospective\b",
    "randomized": r"\brandomi[sz]ed\b",
    "experimental": r"\bexperimental\b",
    "observational": r"\bobservational\b",
    "cohort": r"\bcohort\b",
    "case-control": r"\bcase[- ]control\b",
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def walk_strings(value: Any, path: str = "") -> Iterable[tuple[str, str]]:
    """Yield (field_path, string_value) recursively."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}" if path else str(key)
            yield from walk_strings(item, child)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            child = f"{path}[{idx}]"
            yield from walk_strings(item, child)


def sentence_segments(text: str) -> list[str]:
    """Split a generated field into sentence-like segments for local fidelity checks."""
    parts = re.split(r"(?<=[.!?])\s+|[\r\n]+", text)
    return [part.strip() for part in parts if part and part.strip()]


def load_yaml_documents(path: Path) -> list[Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return list(yaml.safe_load_all(f))


def extract_insights(documents: list[Any]) -> list[dict[str, Any]]:
    insights: list[dict[str, Any]] = []
    for doc in documents:
        if doc is None:
            continue
        if isinstance(doc, dict) and isinstance(doc.get("insights"), list):
            insights.extend(x for x in doc["insights"] if isinstance(x, dict))
        elif isinstance(doc, dict) and "insight_id" in doc:
            insights.append(doc)
        elif isinstance(doc, list):
            insights.extend(x for x in doc if isinstance(x, dict))
    return insights


def claim_source_id(claim_id: str) -> str:
    # Standard KnowledgeCraft claim IDs end in -NN, e.g. SRC-...-01.
    return re.sub(r"-\d+$", "", claim_id)


def load_claims_from_file(path: Path) -> list[dict[str, Any]]:
    docs = load_yaml_documents(path)
    claims: list[dict[str, Any]] = []

    for doc in docs:
        if not isinstance(doc, dict):
            continue
        ledger = doc.get("claim_ledger")
        if isinstance(ledger, list):
            claims.extend(x for x in ledger if isinstance(x, dict))
    return claims


def collect_claim_files(args: argparse.Namespace, repo_root: Path) -> list[Path]:
    files: list[Path] = []

    if args.claims:
        for value in args.claims:
            p = Path(value).resolve()
            if p.is_file():
                files.append(p)
            else:
                print(f"ERROR: claims file not found: {p}")
                raise SystemExit(2)

    if args.claims_dir:
        claim_dir = Path(args.claims_dir).resolve()
    else:
        claim_dir = repo_root / ".knowledgecraft" / "research" / "grounded"

    if claim_dir.exists():
        files.extend(sorted(claim_dir.glob("*-claim-ledger.yaml")))

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(files))


def find_repo_root(script_path: Path) -> Path:
    # Expected location:
    # repo/.opencode/skills/research-insight-miner/scripts/validate_insights.py
    try:
        return script_path.resolve().parents[4]
    except IndexError:
        return Path.cwd().resolve()


def near_paraphrase(source_claim: str, candidate: str) -> bool:
    """
    Detect likely paraphrase of a null-relationship claim.

    Exact reuse is allowed. A candidate is suspicious when it shares much of
    the claim's lexical content but changes the wording.
    """
    source_n = normalize(source_claim)
    cand_n = normalize(candidate)

    if not source_n or not cand_n:
        return False

    if source_n in cand_n:
        return False

    source_tokens = source_n.split()
    cand_tokens = cand_n.split()
    if len(source_tokens) < 6 or len(cand_tokens) < 5:
        return False

    source_set = set(source_tokens)
    cand_set = set(cand_tokens)
    coverage = len(source_set & cand_set) / max(1, len(source_set))

    ratio = SequenceMatcher(None, source_n, cand_n).ratio()

    # Designed to catch near-copy edits such as reported -> report,
    # while avoiding unrelated metadata strings.
    return coverage >= 0.60 and ratio >= 0.52


def validate(
    insights_path: Path,
    insights: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    repo_root: Path,
) -> list[str]:
    errors: list[str] = []

    if not insights:
        return ["No insights found in the supplied YAML file."]

    # Output location check.
    expected_dir = repo_root / ".knowledgecraft" / "research" / "insights"
    try:
        insights_path.resolve().relative_to(expected_dir.resolve())
    except ValueError:
        errors.append(
            f"Output file is outside .knowledgecraft/research/insights/: {insights_path}"
        )

    claim_map: dict[str, dict[str, Any]] = {}
    for claim in claims:
        cid = claim.get("claim_id")
        if isinstance(cid, str) and cid:
            claim_map[cid] = claim

    if not claim_map:
        errors.append(
            "No grounded claims were loaded. Supply --claims or ensure "
            ".knowledgecraft/research/grounded/*-claim-ledger.yaml exists."
        )
        return errors

    seen_insight_ids: set[str] = set()

    for idx, insight in enumerate(insights, start=1):
        prefix = f"Insight #{idx}"

        insight_id = insight.get("insight_id")
        if isinstance(insight_id, str) and insight_id:
            prefix = insight_id
            if insight_id in seen_insight_ids:
                errors.append(f"{prefix}: duplicate insight_id.")
            seen_insight_ids.add(insight_id)
        else:
            errors.append(f"{prefix}: missing or invalid insight_id.")

        actual_fields = set(insight.keys())
        required_fields = set(REQUIRED_FIELDS)
        missing = sorted(required_fields - actual_fields)
        extra = sorted(actual_fields - required_fields)

        if missing:
            errors.append(f"{prefix}: missing schema fields: {', '.join(missing)}")
        if extra:
            errors.append(f"{prefix}: unexpected schema fields: {', '.join(extra)}")

        insight_type = insight.get("insight_type")
        if insight_type not in ALLOWED_INSIGHT_TYPES:
            errors.append(f"{prefix}: invalid insight_type: {insight_type!r}")

        inference_level = insight.get("inference_level")
        if inference_level not in ALLOWED_INFERENCE_LEVELS:
            errors.append(f"{prefix}: invalid inference_level: {inference_level!r}")

        # Strict deterministic rule: hypotheses are model-generated extensions.
        if insight_type == "hypothesis" and inference_level != "high":
            errors.append(
                f"{prefix}: hypothesis must use inference_level: high."
            )

        supporting_ids = insight.get("supporting_claim_ids")
        source_ids = insight.get("source_ids")

        if not isinstance(supporting_ids, list) or not supporting_ids:
            errors.append(f"{prefix}: supporting_claim_ids must be a non-empty list.")
            supporting_ids = []

        if not isinstance(source_ids, list) or not source_ids:
            errors.append(f"{prefix}: source_ids must be a non-empty list.")
            source_ids = []

        resolved_claims: list[dict[str, Any]] = []
        for cid in supporting_ids:
            if not isinstance(cid, str):
                errors.append(f"{prefix}: non-string supporting claim ID: {cid!r}")
                continue
            claim = claim_map.get(cid)
            if claim is None:
                errors.append(f"{prefix}: unresolved supporting claim ID: {cid}")
                continue
            resolved_claims.append(claim)

            expected_source = claim_source_id(cid)
            if expected_source not in source_ids:
                errors.append(
                    f"{prefix}: source_ids missing {expected_source} required by {cid}."
                )

        # Source limitations must be exact grounded claims and traced.
        source_limitations = insight.get("source_limitations")
        if source_limitations is None:
            source_limitations = []
        if not isinstance(source_limitations, list):
            errors.append(f"{prefix}: source_limitations must be a list.")
            source_limitations = []

        for limitation in source_limitations:
            if not isinstance(limitation, str):
                errors.append(f"{prefix}: non-string source limitation: {limitation!r}")
                continue

            matches = [
                c for c in claim_map.values()
                if isinstance(c.get("claim"), str)
                and c.get("claim") == limitation
            ]
            if not matches:
                errors.append(
                    f"{prefix}: source limitation is not an exact grounded claim: "
                    f"{limitation!r}"
                )
                continue

            matched_ids = {
                c.get("claim_id")
                for c in matches
                if isinstance(c.get("claim_id"), str)
            }
            if not matched_ids.intersection(set(supporting_ids)):
                errors.append(
                    f"{prefix}: source limitation reused without its claim ID in "
                    f"supporting_claim_ids: {limitation!r}"
                )

        # Null relationship-language enforcement.
        null_relation_claims = [
            c for c in resolved_claims
            if c.get("relationship_language") is None
            and c.get("role") == "finding"
            and isinstance(c.get("claim"), str)
        ]

        named_relation_claims = [
            c for c in resolved_claims
            if isinstance(c.get("relationship_language"), str)
            and c.get("relationship_language")
            and c.get("role") == "finding"
            and isinstance(c.get("claim"), str)
        ]

        has_not_established_causality = any(
            c.get("causal_status") == "not-established"
            for c in resolved_claims
        )

        is_cross_source = len({sid for sid in source_ids if isinstance(sid, str)}) > 1
        all_strings = list(walk_strings(insight))

        if null_relation_claims:
            for field_path, text in all_strings:
                # Exact grounded source limitation can legitimately use causal terms,
                # but still must not introduce relationship shorthand.
                for pattern in FORBIDDEN_NULL_RELATIONSHIP_PATTERNS:
                    if re.search(pattern, text, flags=re.IGNORECASE):
                        errors.append(
                            f"{prefix}: forbidden null-relationship wording in "
                            f"{field_path}: {text!r}"
                        )
                        break

                for pattern in UNSUPPORTED_EXPLANATION_PATTERNS:
                    if re.search(pattern, text, flags=re.IGNORECASE):
                        errors.append(
                            f"{prefix}: unsupported explanatory wording in "
                            f"{field_path}: {text!r}"
                        )
                        break

                if has_not_established_causality:
                    for pattern in FORBIDDEN_NOT_ESTABLISHED_CAUSAL_PATTERNS:
                        if re.search(pattern, text, flags=re.IGNORECASE):
                            errors.append(
                                f"{prefix}: categorical causal wording is too strong "
                                f"for causal_status: not-established in {field_path}: "
                                f"{text!r}"
                            )
                            break

            for claim in null_relation_claims:
                claim_text = claim["claim"]
                claim_id = claim.get("claim_id", "<unknown>")
                for field_path, field_text in all_strings:
                    if field_path.endswith("supporting_claim_ids"):
                        continue
                    for segment in sentence_segments(field_text):
                        if near_paraphrase(claim_text, segment):
                            errors.append(
                                f"{prefix}: likely paraphrase of null-relationship claim "
                                f"{claim_id} in {field_path}; reuse the grounded claim "
                                f"verbatim or use relationship-neutral wording. "
                                f"Value: {segment!r}"
                            )
                            break

        # Named relationship terminology must survive close restatements.
        for claim in named_relation_claims:
            claim_text = claim["claim"]
            claim_id = claim.get("claim_id", "<unknown>")
            relationship_language = str(claim.get("relationship_language"))
            rel_n = normalize(relationship_language)

            for field_path, field_text in all_strings:
                if field_path.endswith("supporting_claim_ids"):
                    continue
                for segment in sentence_segments(field_text):
                    if near_paraphrase(claim_text, segment):
                        if rel_n not in normalize(segment):
                            errors.append(
                                f"{prefix}: close restatement of claim {claim_id} in "
                                f"{field_path} dropped or changed the grounded "
                                f"relationship language {relationship_language!r}. "
                                f"Value: {segment!r}"
                            )
                            break

        # Low-inference synthesis must not invent study-design labels.
        if inference_level == "low":
            grounded_text = " ".join(
                str(c.get("claim", "")) for c in resolved_claims
            )
            for field_path, field_text in all_strings:
                for design_name, pattern in STUDY_DESIGN_PATTERNS.items():
                    if re.search(pattern, field_text, flags=re.IGNORECASE):
                        if not re.search(pattern, grounded_text, flags=re.IGNORECASE):
                            errors.append(
                                f"{prefix}: unsupported study-design label "
                                f"{design_name!r} in {field_path}; the supporting "
                                f"grounded claims do not state this design. "
                                f"Value: {field_text!r}"
                            )

        # Cross-source comparisons should remain descriptive unless stronger
        # comparative labels are explicitly grounded.
        if is_cross_source:
            for field_path, field_text in all_strings:
                for pattern in FORBIDDEN_CROSS_SOURCE_COMPARATIVE_PATTERNS:
                    if re.search(pattern, field_text, flags=re.IGNORECASE):
                        errors.append(
                            f"{prefix}: cross-source comparative label is too strong "
                            f"or insufficiently grounded in {field_path}: "
                            f"{field_text!r}"
                        )
                        break

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft research-insight-miner YAML output."
    )
    parser.add_argument("insights_file", help="Insight YAML file to validate.")
    parser.add_argument(
        "--claims",
        action="append",
        help="Grounded claim-ledger YAML file. May be supplied multiple times.",
    )
    parser.add_argument(
        "--claims-dir",
        help="Directory containing *-claim-ledger.yaml files. "
             "Defaults to .knowledgecraft/research/grounded/.",
    )
    args = parser.parse_args()

    script_path = Path(__file__)
    repo_root = find_repo_root(script_path)
    insights_path = Path(args.insights_file).resolve()

    if not insights_path.is_file():
        print(f"ERROR: insight file not found: {insights_path}")
        return 2

    try:
        insight_docs = load_yaml_documents(insights_path)
    except Exception as exc:
        print(f"FAIL: could not parse insight YAML: {exc}")
        return 1

    insights = extract_insights(insight_docs)

    claim_files = collect_claim_files(args, repo_root)
    claims: list[dict[str, Any]] = []
    for path in claim_files:
        try:
            claims.extend(load_claims_from_file(path))
        except Exception as exc:
            print(f"FAIL: could not parse claim ledger {path}: {exc}")
            return 1

    errors = validate(
        insights_path=insights_path,
        insights=insights,
        claims=claims,
        repo_root=repo_root,
    )

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for i, error in enumerate(errors, start=1):
            print(f"{i}. {error}")
        return 1

    print(f"PASS: {len(insights)} insight(s) validated")
    print(f"Claims loaded: {len(claims)}")
    print(f"File: {insights_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
