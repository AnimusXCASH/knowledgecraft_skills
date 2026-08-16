from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "ERROR: PyYAML is required. Install with: py -m pip install pyyaml"
    ) from exc

ALLOWED_STATUSES = {
    "SUPPORTED",
    "OVERSTATED",
    "UNSUPPORTED",
    "CONFLICTING",
    "NEEDS_SOURCE",
}

SUMMARY_KEYS = {
    "SUPPORTED": "supported",
    "OVERSTATED": "overstated",
    "UNSUPPORTED": "unsupported",
    "CONFLICTING": "conflicting",
    "NEEDS_SOURCE": "needs_source",
}


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: File not found: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"ERROR: Invalid YAML in {path}: {exc}") from exc


def validate(audit_path: Path) -> list[str]:
    data = load_yaml(audit_path)
    errors: list[str] = []

    if not isinstance(data, dict) or "factuality_audit" not in data:
        return ["Top-level key `factuality_audit` is required."]

    audit = data["factuality_audit"]
    if not isinstance(audit, dict):
        return ["`factuality_audit` must be a mapping."]

    claims = audit.get("claims")
    summary = audit.get("summary")

    if not isinstance(claims, list):
        errors.append("`factuality_audit.claims` must be a list.")
        return errors

    if not isinstance(summary, dict):
        errors.append("`factuality_audit.summary` must be a mapping.")
        return errors

    seen_ids: set[str] = set()
    actual_counts = {status: 0 for status in ALLOWED_STATUSES}
    actual_blocking: list[str] = []

    for idx, claim in enumerate(claims, start=1):
        prefix = f"claim[{idx}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix}: claim entry must be a mapping.")
            continue

        audit_id = claim.get("audit_id")
        status = claim.get("status")
        supporting = claim.get("supporting_claim_ids")
        blocking = claim.get("publication_blocking")

        if not isinstance(audit_id, str) or not audit_id.strip():
            errors.append(f"{prefix}: non-empty `audit_id` is required.")
            audit_id = prefix
        elif audit_id in seen_ids:
            errors.append(f"{audit_id}: duplicate audit_id.")
        else:
            seen_ids.add(audit_id)

        if status not in ALLOWED_STATUSES:
            errors.append(
                f"{audit_id}: invalid status {status!r}; "
                f"expected one of {sorted(ALLOWED_STATUSES)}."
            )
        else:
            actual_counts[status] += 1

        if not isinstance(supporting, list):
            errors.append(f"{audit_id}: `supporting_claim_ids` must be a list.")
            supporting = []

        # Evidence-basis traceability rule.
        if status in {"SUPPORTED", "OVERSTATED", "CONFLICTING"} and not supporting:
            errors.append(
                f"{audit_id}: status {status} requires at least one "
                "`supporting_claim_ids` entry."
            )

        if not isinstance(blocking, bool):
            errors.append(f"{audit_id}: `publication_blocking` must be true/false.")
        elif blocking:
            actual_blocking.append(audit_id)

    # Summary arithmetic
    expected_total = len(claims)
    if summary.get("total_claims") != expected_total:
        errors.append(
            f"summary.total_claims is {summary.get('total_claims')!r}; "
            f"expected {expected_total}."
        )

    for status, key in SUMMARY_KEYS.items():
        expected = actual_counts[status]
        actual = summary.get(key)
        if actual != expected:
            errors.append(
                f"summary.{key} is {actual!r}; expected {expected} "
                f"from final claim statuses."
            )

    count_sum = sum(actual_counts.values())
    if count_sum != expected_total:
        errors.append(
            f"Internal status count sum is {count_sum}; expected {expected_total}."
        )

    reported_blocking = summary.get("blocking_claim_ids")
    if not isinstance(reported_blocking, list):
        errors.append("summary.blocking_claim_ids must be a list.")
        reported_blocking = []

    if reported_blocking != actual_blocking:
        errors.append(
            "summary.blocking_claim_ids does not exactly match claims with "
            f"publication_blocking: true. Expected {actual_blocking!r}, "
            f"got {reported_blocking!r}."
        )

    expected_gate = "BLOCK" if actual_blocking else "PASS"
    if summary.get("publication_gate") != expected_gate:
        errors.append(
            f"summary.publication_gate is {summary.get('publication_gate')!r}; "
            f"expected {expected_gate!r}."
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft factuality-guard audit consistency."
    )
    parser.add_argument("audit", help="Path to factuality audit YAML.")
    args = parser.parse_args()

    path = Path(args.audit).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for i, error in enumerate(errors, start=1):
            print(f"{i}. {error}")
        print(f"File: {path}")
        return 1

    data = load_yaml(path)
    claims = data["factuality_audit"]["claims"]
    print(f"PASS: {len(claims)} factuality claim(s) validated")
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
