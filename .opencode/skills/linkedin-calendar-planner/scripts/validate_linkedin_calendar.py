from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "ERROR: PyYAML is required. Install with: py -m pip install pyyaml"
    ) from exc


CALENDAR_STATUSES = {
    "scheduled",
    "provisional",
    "needs_decision",
    "blocked_by_dependency",
    "expired",
}
SLOT_LOCKS = {"locked", "flexible"}
TIME_MODES = {"exact", "window", "TBD"}
CADENCE_SOURCES = {"user", "proposed", "unspecified"}
TIME_SENSITIVITY = {"evergreen", "time_sensitive"}
COLLISION_LEVELS = {"none", "soft", "hard"}
COLLISION_ACTIONS = {"none", "resolved", "needs_decision"}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"ERROR: File not found: {path}")

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise SystemExit(f"ERROR: Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("ERROR: YAML root must be a mapping.")
    return data


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(
    errors: list[str],
    value: Any,
    field: str,
    *,
    allow_empty: bool = True,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"`{field}` must be a list.")
        return []
    out: list[str] = []
    for i, item in enumerate(value, start=1):
        if not _nonempty_str(item):
            errors.append(f"`{field}[{i}]` must be a non-empty string.")
        else:
            out.append(item)
    if not allow_empty and not out:
        errors.append(f"`{field}` must contain at least one value.")
    return out


def _parse_date(
    errors: list[str],
    value: Any,
    field: str,
    *,
    required: bool = False,
) -> date | None:
    if value is None:
        if required:
            errors.append(f"`{field}` requires a YYYY-MM-DD date.")
        return None
    if not _nonempty_str(value):
        errors.append(f"`{field}` must be null or a YYYY-MM-DD string.")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"`{field}` must use YYYY-MM-DD format.")
        return None


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    cal = data.get("linkedin_calendar")
    if not isinstance(cal, dict):
        return ["Top-level `linkedin_calendar` mapping is required."]

    if not _nonempty_str(cal.get("calendar_id")):
        errors.append("`calendar_id` must be a non-empty string.")

    timezone = cal.get("timezone")
    if timezone is not None and not _nonempty_str(timezone):
        errors.append("`timezone` must be null or a non-empty string.")

    timezone_required = cal.get("timezone_required")
    if not isinstance(timezone_required, bool):
        errors.append("`timezone_required` must be boolean.")
        timezone_required = False

    cadence = cal.get("cadence")
    if not isinstance(cadence, dict):
        errors.append("`cadence` must be a mapping.")
        cadence = {}
    if cadence.get("source") not in CADENCE_SOURCES:
        errors.append(
            f"`cadence.source` must be one of {sorted(CADENCE_SOURCES)}."
        )
    if not isinstance(cadence.get("description"), str):
        errors.append("`cadence.description` must be a string.")

    date_range = cal.get("date_range")
    if not isinstance(date_range, dict):
        errors.append("`date_range` must be a mapping.")
        date_range = {}
    range_start = _parse_date(errors, date_range.get("start"), "date_range.start")
    range_end = _parse_date(errors, date_range.get("end"), "date_range.end")
    if range_start and range_end and range_end < range_start:
        errors.append("`date_range.end` cannot precede `date_range.start`.")

    constraints = cal.get("constraints")
    if not isinstance(constraints, dict):
        errors.append("`constraints` must be a mapping.")
        constraints = {}

    fixed_dates = _string_list(errors, constraints.get("fixed_dates"), "constraints.fixed_dates")
    blackout_strings = _string_list(
        errors, constraints.get("blackout_dates"), "constraints.blackout_dates"
    )
    _string_list(errors, constraints.get("allowed_days"), "constraints.allowed_days")

    for i, d in enumerate(fixed_dates, start=1):
        _parse_date(errors, d, f"constraints.fixed_dates[{i}]")
    blackout_dates: set[date] = set()
    for i, d in enumerate(blackout_strings, start=1):
        parsed = _parse_date(errors, d, f"constraints.blackout_dates[{i}]")
        if parsed:
            blackout_dates.add(parsed)

    min_spacing = constraints.get("minimum_spacing_days")
    if min_spacing is not None and (
        isinstance(min_spacing, bool) or not isinstance(min_spacing, int) or min_spacing < 0
    ):
        errors.append("`constraints.minimum_spacing_days` must be null or a non-negative integer.")

    max_per_day = constraints.get("maximum_posts_per_day")
    if isinstance(max_per_day, bool) or not isinstance(max_per_day, int) or max_per_day < 1:
        errors.append("`constraints.maximum_posts_per_day` must be a positive integer.")
        max_per_day = 1

    entries = cal.get("entries")
    if not isinstance(entries, list):
        errors.append("`entries` must be a list.")
        entries = []

    entry_ids: set[str] = set()
    post_ids: set[str] = set()
    entry_by_post: dict[str, dict[str, Any]] = {}
    entry_date: dict[str, date | None] = {}
    scheduled_dates: list[date] = []

    only_approved_scheduled = True
    dependencies_respected = True
    blackout_respected = True
    windows_respected = True
    exact_time_respected = True
    unresolved_decisions = False

    for i, entry in enumerate(entries, start=1):
        prefix = f"entries[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        entry_id = entry.get("calendar_entry_id")
        if not _nonempty_str(entry_id):
            errors.append(f"`{prefix}.calendar_entry_id` must be a non-empty string.")
            entry_id = prefix
        elif entry_id in entry_ids:
            errors.append(f"Duplicate calendar_entry_id {entry_id!r}.")
        else:
            entry_ids.add(entry_id)

        post_id = entry.get("post_id")
        if not _nonempty_str(post_id):
            errors.append(f"`{prefix}.post_id` must be a non-empty string.")
            post_id = prefix
        elif post_id in post_ids:
            errors.append(f"Duplicate post_id {post_id!r} in calendar entries.")
        else:
            post_ids.add(post_id)
            entry_by_post[post_id] = entry

        approval = entry.get("approval_status")
        if not _nonempty_str(approval):
            errors.append(f"{post_id}: `approval_status` must be a non-empty string.")

        status = entry.get("calendar_status")
        if status not in CALENDAR_STATUSES:
            errors.append(
                f"{post_id}: `calendar_status` must be one of {sorted(CALENDAR_STATUSES)}."
            )

        slot_lock = entry.get("slot_lock")
        if slot_lock not in SLOT_LOCKS:
            errors.append(
                f"{post_id}: `slot_lock` must be one of {sorted(SLOT_LOCKS)}."
            )

        d = _parse_date(
            errors,
            entry.get("date"),
            f"{post_id}.date",
            required=(status == "scheduled"),
        )
        entry_date[post_id] = d

        if d and range_start and d < range_start:
            errors.append(f"{post_id}: date precedes calendar date_range.start.")
        if d and range_end and d > range_end:
            errors.append(f"{post_id}: date exceeds calendar date_range.end.")

        time_mode = entry.get("time_mode")
        if time_mode not in TIME_MODES:
            errors.append(
                f"{post_id}: `time_mode` must be one of {sorted(TIME_MODES)}."
            )

        time_value = entry.get("time")
        time_window = entry.get("time_window")

        if time_mode == "exact":
            if not _nonempty_str(time_value):
                errors.append(f"{post_id}: exact time_mode requires non-empty `time`.")
                if status == "scheduled":
                    exact_time_respected = False
            if time_window is not None:
                errors.append(f"{post_id}: exact time_mode must not also set time_window.")
            if status == "scheduled" and (not _nonempty_str(timezone) or timezone_required):
                errors.append(
                    f"{post_id}: scheduled exact time requires known timezone and timezone_required: false."
                )
                exact_time_respected = False

        elif time_mode == "window":
            if not _nonempty_str(time_window):
                errors.append(f"{post_id}: window time_mode requires non-empty `time_window`.")
            if time_value is not None:
                errors.append(f"{post_id}: window time_mode must not set exact `time`.")

        elif time_mode == "TBD":
            if time_value is not None:
                errors.append(f"{post_id}: TBD time_mode must not set exact `time`.")

        _string_list(errors, entry.get("pillar_ids"), f"{post_id}.pillar_ids")
        prereqs = _string_list(
            errors, entry.get("prerequisite_post_ids"), f"{post_id}.prerequisite_post_ids"
        )
        entry["_validator_prereqs"] = prereqs

        if not isinstance(entry.get("reader_job"), str):
            errors.append(f"{post_id}: `reader_job` must be a string.")
        if not isinstance(entry.get("format"), str):
            errors.append(f"{post_id}: `format` must be a string.")
        if not isinstance(entry.get("scheduling_rationale"), str):
            errors.append(f"{post_id}: `scheduling_rationale` must be a string.")
        _string_list(errors, entry.get("conflicts"), f"{post_id}.conflicts")

        sensitivity = entry.get("time_sensitivity")
        if sensitivity not in TIME_SENSITIVITY:
            errors.append(
                f"{post_id}: `time_sensitivity` must be one of {sorted(TIME_SENSITIVITY)}."
            )
        not_before = _parse_date(errors, entry.get("not_before"), f"{post_id}.not_before")
        not_after = _parse_date(errors, entry.get("not_after"), f"{post_id}.not_after")
        if not_before and not_after and not_after < not_before:
            errors.append(f"{post_id}: not_after cannot precede not_before.")

        if status == "scheduled":
            scheduled_dates.append(d) if d else None
            if approval != "qa_approved":
                only_approved_scheduled = False
                errors.append(
                    f"{post_id}: scheduled entry must have approval_status `qa_approved`."
                )
            if d and d in blackout_dates:
                blackout_respected = False
                errors.append(f"{post_id}: scheduled on blackout date {d.isoformat()}.")
            if sensitivity == "time_sensitive" and d:
                if not_before and d < not_before:
                    windows_respected = False
                    errors.append(f"{post_id}: scheduled before not_before.")
                if not_after and d > not_after:
                    windows_respected = False
                    errors.append(f"{post_id}: scheduled after not_after.")

        if status == "expired" and d is not None:
            # Date may be retained as metadata, but it must not be presented as an active slot.
            pass

        if status == "needs_decision":
            unresolved_decisions = True

    # Prerequisite existence + scheduled-order safety.
    for post_id, entry in entry_by_post.items():
        prereqs = entry.get("_validator_prereqs", [])
        status = entry.get("calendar_status")
        d = entry_date.get(post_id)

        for prereq_id in prereqs:
            if prereq_id not in entry_by_post:
                errors.append(f"{post_id}: prerequisite {prereq_id!r} is missing from entries.")
                if status == "scheduled":
                    dependencies_respected = False
                continue

            prereq = entry_by_post[prereq_id]
            prereq_status = prereq.get("calendar_status")
            prereq_date = entry_date.get(prereq_id)

            if status == "scheduled":
                if prereq_status != "scheduled":
                    dependencies_respected = False
                    errors.append(
                        f"{post_id}: scheduled while prerequisite {prereq_id} is not scheduled."
                    )
                elif d and prereq_date and prereq_date >= d:
                    dependencies_respected = False
                    errors.append(
                        f"{post_id}: scheduled on/before prerequisite {prereq_id}."
                    )

    # Scheduled posts-per-day capacity.
    counts = Counter(d for d in scheduled_dates if d is not None)
    capacity_violation = False
    for d, count in counts.items():
        if count > max_per_day:
            capacity_violation = True
            errors.append(
                f"Scheduled posts on {d.isoformat()} exceed maximum_posts_per_day "
                f"({count} > {max_per_day})."
            )

    # Experiments.
    experiments = cal.get("experiments")
    if not isinstance(experiments, list):
        errors.append("`experiments` must be a list.")
        experiments = []

    experiment_ids: set[str] = set()
    for i, exp in enumerate(experiments, start=1):
        prefix = f"experiments[{i}]"
        if not isinstance(exp, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue
        exp_id = exp.get("experiment_id")
        if not _nonempty_str(exp_id):
            errors.append(f"`{prefix}.experiment_id` must be a non-empty string.")
        elif exp_id in experiment_ids:
            errors.append(f"Duplicate experiment_id {exp_id!r}.")
        else:
            experiment_ids.add(exp_id)

        if not _nonempty_str(exp.get("hypothesis")):
            errors.append(f"`{prefix}.hypothesis` must be a non-empty string.")
        if not _nonempty_str(exp.get("variable")):
            errors.append(f"`{prefix}.variable` must be a non-empty string.")
        _string_list(errors, exp.get("variants"), f"{prefix}.variants", allow_empty=False)
        if not _nonempty_str(exp.get("interpretation_guard")):
            errors.append(f"`{prefix}.interpretation_guard` must be a non-empty string.")

    for post_id, entry in entry_by_post.items():
        exp_id = entry.get("experiment_id")
        if exp_id is not None and exp_id not in experiment_ids:
            errors.append(
                f"{post_id}: experiment_id {exp_id!r} is not defined in experiments."
            )

    # Collision review.
    collisions = cal.get("collision_review")
    if not isinstance(collisions, list):
        errors.append("`collision_review` must be a list.")
        collisions = []

    collision_ids: set[str] = set()
    hard_remaining = capacity_violation
    for i, col in enumerate(collisions, start=1):
        prefix = f"collision_review[{i}]"
        if not isinstance(col, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        cid = col.get("collision_id")
        if not _nonempty_str(cid):
            errors.append(f"`{prefix}.collision_id` must be a non-empty string.")
        elif cid in collision_ids:
            errors.append(f"Duplicate collision_id {cid!r}.")
        else:
            collision_ids.add(cid)

        ids = _string_list(errors, col.get("entry_ids"), f"{prefix}.entry_ids")
        for eid in ids:
            if eid not in entry_ids:
                errors.append(f"`{prefix}` references unknown calendar_entry_id {eid!r}.")

        level = col.get("collision_level")
        action = col.get("action")
        if level not in COLLISION_LEVELS:
            errors.append(
                f"`{prefix}.collision_level` must be one of {sorted(COLLISION_LEVELS)}."
            )
        if action not in COLLISION_ACTIONS:
            errors.append(
                f"`{prefix}.action` must be one of {sorted(COLLISION_ACTIONS)}."
            )
        if not _nonempty_str(col.get("collision_type")):
            errors.append(f"`{prefix}.collision_type` must be a non-empty string.")
        if not _nonempty_str(col.get("explanation")):
            errors.append(f"`{prefix}.explanation` must be a non-empty string.")

        if level == "hard" and action != "resolved":
            hard_remaining = True
        if action == "needs_decision":
            unresolved_decisions = True

    checks = cal.get("calendar_checks")
    if not isinstance(checks, dict):
        errors.append("`calendar_checks` must be a mapping.")
        checks = {}

    expected_checks = {
        "only_approved_posts_scheduled": only_approved_scheduled,
        "dependencies_respected": dependencies_respected,
        "hard_collisions_remaining": hard_remaining,
        "unresolved_decisions_remaining": unresolved_decisions,
        "blackout_dates_respected": blackout_respected,
        "time_sensitive_windows_respected": windows_respected,
        "exact_time_requirements_respected": exact_time_respected,
    }

    for field, expected in expected_checks.items():
        value = checks.get(field)
        if not isinstance(value, bool):
            errors.append(f"`calendar_checks.{field}` must be boolean.")
        elif value is not expected:
            errors.append(
                f"`calendar_checks.{field}` does not match calendar data "
                f"(expected {expected})."
            )

    explicit_dates = checks.get("explicit_user_dates_preserved")
    if not isinstance(explicit_dates, bool):
        errors.append("`calendar_checks.explicit_user_dates_preserved` must be boolean.")

    unsupported_timing = checks.get("unsupported_platform_timing_claims_used")
    if not isinstance(unsupported_timing, bool):
        errors.append(
            "`calendar_checks.unsupported_platform_timing_claims_used` must be boolean."
        )

    handoff = cal.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("`handoff` must be a mapping.")
        handoff = {}

    ready = handoff.get("ready_to_schedule")
    if not isinstance(ready, bool):
        errors.append("`handoff.ready_to_schedule` must be boolean.")
        ready = False

    any_scheduled = any(
        isinstance(e, dict) and e.get("calendar_status") == "scheduled"
        for e in entries
    )

    # Safety gate: false may be conservative; true must be mechanically safe.
    unsafe_for_ready = bool(
        not any_scheduled
        or not only_approved_scheduled
        or not dependencies_respected
        or hard_remaining
        or explicit_dates is not True
        or not blackout_respected
        or not windows_respected
        or not exact_time_respected
        or unsupported_timing is not False
    )

    if ready and unsafe_for_ready:
        errors.append(
            "`handoff.ready_to_schedule: true` is unsafe for the current calendar state."
        )

    if ready and handoff.get("lifecycle_transition") != "qa_approved -> scheduled":
        errors.append(
            "Ready handoff must use lifecycle_transition `qa_approved -> scheduled`."
        )

    notes = handoff.get("notes")
    if not isinstance(notes, list):
        errors.append("`handoff.notes` must be a list.")
    else:
        for i, note in enumerate(notes, start=1):
            if not _nonempty_str(note):
                errors.append(f"`handoff.notes[{i}]` must be a non-empty string.")

    # Remove private in-memory keys.
    for entry in entries:
        if isinstance(entry, dict):
            entry.pop("_validator_prereqs", None)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft LinkedIn calendar YAML."
    )
    parser.add_argument("calendar", help="Path to linkedin-calendar.yaml")
    args = parser.parse_args()

    path = Path(args.calendar).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    cal = load_yaml(path)["linkedin_calendar"]
    scheduled = sum(
        1
        for entry in cal.get("entries", [])
        if isinstance(entry, dict) and entry.get("calendar_status") == "scheduled"
    )
    print(
        "PASS: LinkedIn calendar validated "
        f"(entries={len(cal.get('entries', []))}, scheduled={scheduled}, "
        f"ready_to_schedule={cal.get('handoff', {}).get('ready_to_schedule')})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
