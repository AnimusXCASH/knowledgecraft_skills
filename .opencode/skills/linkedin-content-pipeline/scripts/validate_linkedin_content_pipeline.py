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


MODES = {
    "standalone_post",
    "series",
    "research_to_content",
    "qa_only",
    "calendar_only",
    "performance_learning",
}
ROUTING_STATUSES = {
    "pending",
    "completed",
    "skipped",
    "blocked",
    "needs_input",
    "failed",
}
VALIDATOR_STATUSES = {"not_required", "not_run", "pass", "fail"}
ITEM_TYPES = {"source", "series", "post", "calendar", "performance_review"}
LIFECYCLE = {
    "new",
    "extracted",
    "grounded",
    "ideas_created",
    "series_planned",
    "drafted",
    "qa_approved",
    "scheduled",
    "published",
    "failed",
    "ignored",
}
FACTUALITY = {"not_run", "pass", "block"}
QUALITY = {"not_run", "APPROVE", "REVISE", "BLOCK"}


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


def _string_list(errors: list[str], value: Any, field: str) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"`{field}` must be a list.")
        return []

    out: list[str] = []
    for i, item in enumerate(value, start=1):
        if not _nonempty_str(item):
            errors.append(f"`{field}[{i}]` must be a non-empty string.")
        else:
            out.append(item)
    return out


def _nullable_lifecycle(
    errors: list[str],
    value: Any,
    field: str,
) -> str | None:
    if value is None:
        return None
    if value not in LIFECYCLE:
        errors.append(f"`{field}` must be null or one of {sorted(LIFECYCLE)}.")
        return None
    return value


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    pipe = data.get("linkedin_content_pipeline")
    if not isinstance(pipe, dict):
        return ["Top-level `linkedin_content_pipeline` mapping is required."]

    if not _nonempty_str(pipe.get("run_id")):
        errors.append("`run_id` must be a non-empty string.")
    if not _nonempty_str(pipe.get("requested_goal")):
        errors.append("`requested_goal` must be a non-empty string.")
    if pipe.get("mode") not in MODES:
        errors.append(f"`mode` must be one of {sorted(MODES)}.")

    inspected = pipe.get("inspected_state")
    if not isinstance(inspected, dict):
        errors.append("`inspected_state` must be a mapping.")
        inspected = {}
    _string_list(errors, inspected.get("source_ids"), "inspected_state.source_ids")
    _string_list(errors, inspected.get("post_ids"), "inspected_state.post_ids")
    _string_list(errors, inspected.get("stale_artifacts"), "inspected_state.stale_artifacts")
    states = inspected.get("current_lifecycle_states")
    if not isinstance(states, dict):
        errors.append("`inspected_state.current_lifecycle_states` must be a mapping.")
    else:
        for item_id, state in states.items():
            if not _nonempty_str(item_id):
                errors.append("Lifecycle-state map keys must be non-empty strings.")
            if state not in LIFECYCLE:
                errors.append(
                    f"Lifecycle state for {item_id!r} must be one of {sorted(LIFECYCLE)}."
                )

    routing = pipe.get("routing")
    if not isinstance(routing, list):
        errors.append("`routing` must be a list.")
        routing = []

    steps_seen: set[int] = set()
    route_item_ids: set[str] = set()
    completed_steps = 0
    skipped_steps = 0
    failed_steps = 0
    blocked_steps = 0
    needs_input_steps = 0

    for i, step in enumerate(routing, start=1):
        prefix = f"routing[{i}]"
        if not isinstance(step, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        number = step.get("step")
        if isinstance(number, bool) or not isinstance(number, int) or number < 1:
            errors.append(f"`{prefix}.step` must be a positive integer.")
        elif number in steps_seen:
            errors.append(f"Duplicate routing step number {number}.")
        else:
            steps_seen.add(number)

        item_id = step.get("item_id")
        if not _nonempty_str(item_id):
            errors.append(f"`{prefix}.item_id` must be a non-empty string.")
        else:
            route_item_ids.add(item_id)

        if not _nonempty_str(step.get("required_skill")):
            errors.append(f"`{prefix}.required_skill` must be a non-empty string.")
        if not _nonempty_str(step.get("reason")):
            errors.append(f"`{prefix}.reason` must be a non-empty string.")

        status = step.get("status")
        if status not in ROUTING_STATUSES:
            errors.append(
                f"`{prefix}.status` must be one of {sorted(ROUTING_STATUSES)}."
            )

        validator_required = step.get("validator_required")
        if not isinstance(validator_required, bool):
            errors.append(f"`{prefix}.validator_required` must be boolean.")
            validator_required = False

        validator_status = step.get("validator_status")
        if validator_status not in VALIDATOR_STATUSES:
            errors.append(
                f"`{prefix}.validator_status` must be one of {sorted(VALIDATOR_STATUSES)}."
            )

        if validator_required and validator_status == "not_required":
            errors.append(
                f"`{prefix}` requires validation but validator_status is `not_required`."
            )
        if not validator_required and validator_status not in {"not_required", "not_run"}:
            errors.append(
                f"`{prefix}` does not require validation but reports validator execution status "
                f"{validator_status!r}."
            )
        if status == "completed" and validator_required and validator_status != "pass":
            errors.append(
                f"`{prefix}` cannot be completed until its required validator passes."
            )
        if status == "completed" and validator_status == "fail":
            errors.append(f"`{prefix}` cannot be completed with validator_status `fail`.")
        if status == "skipped" and validator_status == "fail":
            errors.append(f"`{prefix}` cannot be skipped while retaining validator_status `fail`.")

        completed_steps += status == "completed"
        skipped_steps += status == "skipped"
        failed_steps += status == "failed"
        blocked_steps += status == "blocked"
        needs_input_steps += status == "needs_input"

    item_states = pipe.get("item_states")
    if not isinstance(item_states, list):
        errors.append("`item_states` must be a list.")
        item_states = []

    item_ids_seen: set[str] = set()
    lifecycle_after_by_item: dict[str, str | None] = {}
    blockers_by_item: dict[str, list[str]] = {}

    for i, item in enumerate(item_states, start=1):
        prefix = f"item_states[{i}]"
        if not isinstance(item, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        item_id = item.get("item_id")
        if not _nonempty_str(item_id):
            errors.append(f"`{prefix}.item_id` must be a non-empty string.")
            item_id = prefix
        elif item_id in item_ids_seen:
            errors.append(f"Duplicate item_state item_id {item_id!r}.")
        else:
            item_ids_seen.add(item_id)

        if item.get("item_type") not in ITEM_TYPES:
            errors.append(
                f"{item_id}: `item_type` must be one of {sorted(ITEM_TYPES)}."
            )

        before = _nullable_lifecycle(
            errors, item.get("lifecycle_before"), f"{item_id}.lifecycle_before"
        )
        after = _nullable_lifecycle(
            errors, item.get("lifecycle_after"), f"{item_id}.lifecycle_after"
        )
        lifecycle_after_by_item[item_id] = after

        if not _nonempty_str(item.get("current_status")):
            errors.append(f"{item_id}: `current_status` must be a non-empty string.")

        blockers = _string_list(errors, item.get("blockers"), f"{item_id}.blockers")
        blockers_by_item[item_id] = blockers
        _string_list(errors, item.get("artifact_refs"), f"{item_id}.artifact_refs")

        next_skill = item.get("next_required_skill")
        if next_skill is not None and not _nonempty_str(next_skill):
            errors.append(
                f"{item_id}: `next_required_skill` must be null or a non-empty string."
            )

        if after == "published" and item.get("item_type") != "post":
            errors.append(f"{item_id}: only post items may advance to `published`.")

    qa = pipe.get("qa")
    if not isinstance(qa, list):
        errors.append("`qa` must be a list.")
        qa = []

    qa_by_post: dict[str, dict[str, Any]] = {}
    for i, record in enumerate(qa, start=1):
        prefix = f"qa[{i}]"
        if not isinstance(record, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        post_id = record.get("post_id")
        if not _nonempty_str(post_id):
            errors.append(f"`{prefix}.post_id` must be a non-empty string.")
            continue
        if post_id in qa_by_post:
            errors.append(f"Duplicate QA record for post_id {post_id!r}.")
        qa_by_post[post_id] = record

        factuality = record.get("factuality_status")
        quality = record.get("quality_status")
        approved = record.get("qa_approved")

        if factuality not in FACTUALITY:
            errors.append(
                f"{post_id}: factuality_status must be one of {sorted(FACTUALITY)}."
            )
        if quality not in QUALITY:
            errors.append(
                f"{post_id}: quality_status must be one of {sorted(QUALITY)}."
            )
        if not isinstance(approved, bool):
            errors.append(f"{post_id}: qa_approved must be boolean.")
        elif approved and not (factuality == "pass" and quality == "APPROVE"):
            errors.append(
                f"{post_id}: qa_approved true requires factuality pass + quality APPROVE."
            )

    for item_id, after in lifecycle_after_by_item.items():
        if after == "qa_approved":
            record = qa_by_post.get(item_id)
            if not record or record.get("qa_approved") is not True:
                errors.append(
                    f"{item_id}: lifecycle_after qa_approved requires matching QA approval record."
                )

    calendar = pipe.get("calendar")
    if not isinstance(calendar, dict):
        errors.append("`calendar` must be a mapping.")
        calendar = {}
    if not isinstance(calendar.get("requested"), bool):
        errors.append("`calendar.requested` must be boolean.")
    ready_to_schedule = calendar.get("ready_to_schedule")
    if ready_to_schedule is not None and not isinstance(ready_to_schedule, bool):
        errors.append("`calendar.ready_to_schedule` must be boolean or null.")

    publication = pipe.get("publication")
    if not isinstance(publication, dict):
        errors.append("`publication` must be a mapping.")
        publication = {}

    authorized = publication.get("authorized_workflow_present")
    confirmed = publication.get("published_confirmed")
    if not isinstance(authorized, bool):
        errors.append("`publication.authorized_workflow_present` must be boolean.")
        authorized = False
    if not isinstance(confirmed, bool):
        errors.append("`publication.published_confirmed` must be boolean.")
        confirmed = False

    # A verified platform record may be represented as confirmed even without an automated
    # publishing workflow; therefore authorization is not required for confirmation.
    # However, if no published item exists, confirmation is mechanically inconsistent.
    if confirmed and not any(v == "published" for v in lifecycle_after_by_item.values()):
        errors.append(
            "`publication.published_confirmed: true` requires at least one post item "
            "with lifecycle_after `published`."
        )

    perf = pipe.get("performance_loop")
    if not isinstance(perf, dict):
        errors.append("`performance_loop` must be a mapping.")
        perf = {}
    if not isinstance(perf.get("requested"), bool):
        errors.append("`performance_loop.requested` must be boolean.")
    _string_list(
        errors,
        perf.get("reusable_learning_ids"),
        "performance_loop.reusable_learning_ids",
    )

    summary = pipe.get("summary")
    if not isinstance(summary, dict):
        errors.append("`summary` must be a mapping.")
        summary = {}

    expected_summary = {
        "completed_steps": completed_steps,
        "skipped_steps": skipped_steps,
        "failed_items": failed_steps,
        "needs_input_items": needs_input_steps,
    }

    for field, expected in expected_summary.items():
        value = summary.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"`summary.{field}` must be a non-negative integer.")
        elif value != expected:
            errors.append(
                f"`summary.{field}` does not match routing data "
                f"(expected {expected}, got {value})."
            )

    blocked_items_value = summary.get("blocked_items")
    if isinstance(blocked_items_value, bool) or not isinstance(blocked_items_value, int) or blocked_items_value < 0:
        errors.append("`summary.blocked_items` must be a non-negative integer.")
    else:
        # Count unique blocked routing items, plus item states carrying blockers but not already counted.
        blocked_route_ids = {
            step.get("item_id")
            for step in routing
            if isinstance(step, dict) and step.get("status") == "blocked" and _nonempty_str(step.get("item_id"))
        }
        blocked_state_ids = {
            item_id for item_id, blockers in blockers_by_item.items() if blockers
        }
        expected_blocked = len(blocked_route_ids | blocked_state_ids)
        if blocked_items_value != expected_blocked:
            errors.append(
                "`summary.blocked_items` does not match unique blocked items "
                f"(expected {expected_blocked}, got {blocked_items_value})."
            )

    handoff = pipe.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("`handoff` must be a mapping.")
        handoff = {}

    complete = handoff.get("workflow_complete_for_requested_goal")
    if not isinstance(complete, bool):
        errors.append("`handoff.workflow_complete_for_requested_goal` must be boolean.")
        complete = False

    if not _nonempty_str(handoff.get("next_action")):
        errors.append("`handoff.next_action` must be a non-empty string.")

    _string_list(errors, handoff.get("notes"), "handoff.notes")

    # Conservative mechanical completion rule.
    # A workflow with explicit failed routing cannot be complete.
    if complete and failed_steps > 0:
        errors.append(
            "workflow_complete_for_requested_goal cannot be true while routing contains failed steps."
        )

    # A blocked step may still be outside the completed goal in some semantic cases,
    # so do not categorically forbid completion. But if every item is blocked/needs input
    # and nothing completed/skipped, completion is mechanically implausible.
    if (
        complete
        and completed_steps == 0
        and skipped_steps == 0
        and (blocked_steps > 0 or needs_input_steps > 0)
    ):
        errors.append(
            "workflow_complete_for_requested_goal is inconsistent: no completed/skipped work "
            "and only blocked/needs_input routing remains."
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft LinkedIn content-pipeline report YAML."
    )
    parser.add_argument("report", help="Path to linkedin-pipeline-report.yaml")
    args = parser.parse_args()

    path = Path(args.report).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    pipe = load_yaml(path)["linkedin_content_pipeline"]
    print(
        "PASS: LinkedIn content pipeline report validated "
        f"(routing_steps={len(pipe.get('routing', []))}, "
        f"item_states={len(pipe.get('item_states', []))}, "
        f"goal_complete={pipe.get('handoff', {}).get('workflow_complete_for_requested_goal')})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
