from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "ERROR: PyYAML is required. Install with: py -m pip install pyyaml"
    ) from exc


SCORE_KEYS = (
    "clarity_coherence",
    "specificity_concreteness",
    "usefulness_reader_value",
    "audience_fit",
    "voice_naturalness",
    "destination_format_fit",
    "distinctiveness_nonredundancy",
)

DECISIONS = {"APPROVE", "REVISE", "BLOCK"}
FACTUALITY_STATUSES = {"PASS", "BLOCK", "NOT_REQUIRED", "NOT_RUN"}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: File not found: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"ERROR: Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("ERROR: YAML root must be a mapping.")
    return data


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    gate = data.get("content_quality_gate")
    if not isinstance(gate, dict):
        return ["Top-level `content_quality_gate` mapping is required."]

    blockers = gate.get("blockers")
    if not isinstance(blockers, list):
        errors.append("`blockers` must be a list.")
        blockers = []

    scores = gate.get("scores")
    if not isinstance(scores, dict):
        errors.append("`scores` must be a mapping.")
        scores = {}

    actual_score_keys = set(scores.keys())
    expected_score_keys = set(SCORE_KEYS)

    missing = expected_score_keys - actual_score_keys
    extra = actual_score_keys - expected_score_keys

    if missing:
        errors.append(
            "Missing score dimension(s): " + ", ".join(sorted(missing)) + "."
        )
    if extra:
        errors.append(
            "Unexpected score dimension(s): " + ", ".join(sorted(extra)) + "."
        )

    numeric_scores: list[int] = []
    for key in SCORE_KEYS:
        entry = scores.get(key)
        if not isinstance(entry, dict):
            errors.append(f"`scores.{key}` must be a mapping.")
            continue

        score = entry.get("score")
        reason = entry.get("reason")

        if isinstance(score, bool) or not isinstance(score, int) or score < 0 or score > 3:
            errors.append(f"`scores.{key}.score` must be an integer from 0 to 3.")
        else:
            numeric_scores.append(score)

        if not _nonempty_string(reason):
            errors.append(f"`scores.{key}.reason` must be a non-empty string.")

    total_score = gate.get("total_score")
    if isinstance(total_score, bool) or not isinstance(total_score, int):
        errors.append("`total_score` must be an integer.")
    elif len(numeric_scores) == len(SCORE_KEYS):
        expected_total = sum(numeric_scores)
        if total_score != expected_total:
            errors.append(
                f"`total_score` is {total_score}; expected {expected_total} "
                "from the seven dimension scores."
            )

    decision = gate.get("decision")
    if decision not in DECISIONS:
        errors.append(
            f"`decision` must be one of {sorted(DECISIONS)}."
        )

    required_revisions = gate.get("required_revisions")
    if not isinstance(required_revisions, list):
        errors.append("`required_revisions` must be a list.")
        required_revisions = []
    else:
        for idx, revision in enumerate(required_revisions, start=1):
            if not isinstance(revision, dict):
                errors.append(
                    f"`required_revisions[{idx}]` must be a mapping."
                )
                continue
            for field in ("location", "issue", "smallest_change"):
                if not _nonempty_string(revision.get(field)):
                    errors.append(
                        f"`required_revisions[{idx}].{field}` "
                        "must be a non-empty string."
                    )

    strengths = gate.get("strengths")
    if strengths is not None and not isinstance(strengths, list):
        errors.append("`strengths` must be a list when present.")

    upstream = gate.get("upstream_checks")
    factuality_required = None
    factuality_status = None

    if not isinstance(upstream, dict):
        errors.append("`upstream_checks` must be a mapping.")
    else:
        factuality = upstream.get("factuality")
        if not isinstance(factuality, dict):
            errors.append("`upstream_checks.factuality` must be a mapping.")
        else:
            factuality_required = factuality.get("required")
            factuality_status = factuality.get("status")

            if not isinstance(factuality_required, bool):
                errors.append(
                    "`upstream_checks.factuality.required` must be boolean."
                )

            if factuality_status not in FACTUALITY_STATUSES:
                errors.append(
                    "`upstream_checks.factuality.status` must be one of "
                    f"{sorted(FACTUALITY_STATUSES)}."
                )

            if factuality_required is True and factuality_status == "NOT_REQUIRED":
                errors.append(
                    "Factuality cannot be `required: true` with status `NOT_REQUIRED`."
                )

    # Mechanical decision rule.
    blocker_exists = len(blockers) > 0
    factuality_forces_block = (
        factuality_required is True
        and factuality_status in {"BLOCK", "NOT_RUN"}
    )

    expected_decision = None
    if blocker_exists or factuality_forces_block:
        expected_decision = "BLOCK"
    elif len(numeric_scores) == len(SCORE_KEYS) and isinstance(total_score, int):
        if any(score < 2 for score in numeric_scores) or total_score < 17:
            expected_decision = "REVISE"
        else:
            expected_decision = "APPROVE"

    if (
        expected_decision is not None
        and decision in DECISIONS
        and decision != expected_decision
    ):
        errors.append(
            f"`decision` is {decision}; expected {expected_decision} "
            "from blockers/factuality/scores."
        )

    if decision == "APPROVE" and required_revisions:
        errors.append("APPROVE requires `required_revisions` to be empty.")

    if decision == "REVISE" and not required_revisions:
        errors.append("REVISE requires at least one required revision.")

    if decision == "BLOCK" and not blockers:
        errors.append("BLOCK requires at least one blocker.")

    if factuality_forces_block and not blockers:
        errors.append(
            "Required factuality status BLOCK/NOT_RUN must be represented in `blockers`."
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft content-quality-gate output."
    )
    parser.add_argument("audit", help="Path to content-quality-gate YAML.")
    args = parser.parse_args()

    path = Path(args.audit).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    data = load_yaml(path)
    gate = data["content_quality_gate"]
    print(
        "PASS: content quality gate validated "
        f"(decision={gate['decision']}, total={gate['total_score']}/21)"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
