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


DISPOSITIONS = {"processed", "already_complete", "ignored", "failed"}
PASS_FAIL = {"PASS", "FAIL"}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: File not found: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"ERROR: Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("ERROR: Batch report YAML root must be a mapping.")
    return data


def validate(report_path: Path) -> list[str]:
    data = load_yaml(report_path)
    errors: list[str] = []

    report = data.get("batch_report")
    if not isinstance(report, dict):
        return ["Top-level `batch_report` mapping is required."]

    sources = report.get("sources")
    summary = report.get("summary")

    if not isinstance(sources, list):
        errors.append("`batch_report.sources` must be a list.")
        return errors

    if not isinstance(summary, dict):
        errors.append("`batch_report.summary` must be a mapping.")
        return errors

    seen_ids: set[str] = set()
    disposition_counts = {key: 0 for key in DISPOSITIONS}

    for idx, source in enumerate(sources, start=1):
        prefix = f"source[{idx}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix}: source entry must be a mapping.")
            continue

        source_id = source.get("source_id")
        disposition = source.get("disposition")
        actions = source.get("actions")
        start = source.get("start")
        end = source.get("end")
        error = source.get("error")

        if not isinstance(source_id, str) or not source_id.strip():
            errors.append(f"{prefix}: non-empty `source_id` is required.")
            source_id = prefix
        elif source_id in seen_ids:
            errors.append(f"{source_id}: duplicate source_id in batch report.")
        else:
            seen_ids.add(source_id)

        if disposition not in DISPOSITIONS:
            errors.append(
                f"{source_id}: invalid disposition {disposition!r}; "
                f"expected one of {sorted(DISPOSITIONS)}."
            )
        else:
            disposition_counts[disposition] += 1

        if not isinstance(actions, list):
            errors.append(f"{source_id}: `actions` must be a list.")
            actions = []

        if disposition == "processed" and not actions:
            errors.append(
                f"{source_id}: disposition `processed` requires at least one action."
            )

        if disposition == "already_complete" and actions:
            errors.append(
                f"{source_id}: `already_complete` must not report processing actions."
            )

        if disposition == "ignored":
            if actions:
                errors.append(
                    f"{source_id}: `ignored` must not report processing actions."
                )
            if end != "ignored":
                errors.append(
                    f"{source_id}: disposition `ignored` requires end: ignored."
                )

        if disposition == "failed" and not error:
            errors.append(
                f"{source_id}: disposition `failed` requires a non-empty error."
            )

        if not isinstance(start, str) or not start:
            errors.append(f"{source_id}: non-empty `start` is required.")

        if not isinstance(end, str) or not end:
            errors.append(f"{source_id}: non-empty `end` is required.")

    expected_inspected = len(sources)
    if summary.get("sources_inspected") != expected_inspected:
        errors.append(
            f"summary.sources_inspected is {summary.get('sources_inspected')!r}; "
            f"expected {expected_inspected}."
        )

    key_map = {
        "processed": "sources_processed",
        "already_complete": "sources_already_complete",
        "ignored": "sources_ignored",
        "failed": "sources_failed",
    }

    for disposition, summary_key in key_map.items():
        expected = disposition_counts[disposition]
        actual = summary.get(summary_key)
        if actual != expected:
            errors.append(
                f"summary.{summary_key} is {actual!r}; expected {expected} "
                f"from per-source dispositions."
            )

    partition_sum = sum(disposition_counts.values())
    if partition_sum != expected_inspected:
        errors.append(
            f"Per-source disposition count is {partition_sum}; "
            f"expected {expected_inspected} inspected sources."
        )

    forced = report.get("forced_transitions_used")
    duplicates = report.get("duplicate_source_records")
    idempotence = report.get("second_run_idempotence")
    result = report.get("batch_result")

    if not isinstance(forced, int) or forced < 0:
        errors.append("`forced_transitions_used` must be a non-negative integer.")

    if not isinstance(duplicates, int) or duplicates < 0:
        errors.append("`duplicate_source_records` must be a non-negative integer.")

    if idempotence not in PASS_FAIL:
        errors.append("`second_run_idempotence` must be PASS or FAIL.")

    if result not in PASS_FAIL:
        errors.append("`batch_result` must be PASS or FAIL.")

    expected_result = "PASS"
    if (
        disposition_counts["failed"] > 0
        or forced not in {0}
        or duplicates not in {0}
        or idempotence != "PASS"
    ):
        expected_result = "FAIL"

    if result in PASS_FAIL and result != expected_result:
        errors.append(
            f"`batch_result` is {result!r}; expected {expected_result!r} "
            "from failures/forced transitions/duplicates/idempotence."
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft research-batch report consistency."
    )
    parser.add_argument("report", help="Path to batch report YAML.")
    args = parser.parse_args()

    path = Path(args.report).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    data = load_yaml(path)
    count = len(data["batch_report"]["sources"])
    print(f"PASS: batch report validated for {count} source(s)")
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
