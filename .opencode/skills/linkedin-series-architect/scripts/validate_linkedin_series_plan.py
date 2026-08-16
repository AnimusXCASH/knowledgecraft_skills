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


READER_JOBS = {
    "setup", "teach", "challenge", "evidence",
    "application", "synthesis", "conversation", "story",
}

EVIDENCE_MODES = {
    "evidence_grounded",
    "evidence_informed_interpretation",
    "author_opinion",
    "application_question",
    "story",
}

DRAFTING_STATUSES = {"ready", "needs_input", "blocked"}
OVERLAP_LEVELS = {"distinct", "partial_overlap", "substantial_overlap"}
OVERLAP_ACTIONS = {"none", "revise", "merge", "drop"}

TRACEABILITY_REQUIRED_MODES = {
    "evidence_grounded",
    "evidence_informed_interpretation",
    "application_question",
}


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


def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(errors: list[str], value: Any, field: str) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"`{field}` must be a list.")
        return []
    out: list[str] = []
    for i, item in enumerate(value, start=1):
        if not _is_nonempty_str(item):
            errors.append(f"`{field}[{i}]` must be a non-empty string.")
        else:
            out.append(item)
    return out


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    plan = data.get("linkedin_series_plan")
    if not isinstance(plan, dict):
        return ["Top-level `linkedin_series_plan` mapping is required."]

    plan_sources = set(_string_list(errors, plan.get("source_ids"), "source_ids"))
    plan_claims = set(_string_list(errors, plan.get("claim_ids"), "claim_ids"))
    plan_insights = set(_string_list(errors, plan.get("insight_ids"), "insight_ids"))

    posts = plan.get("posts")
    if not isinstance(posts, list):
        errors.append("`posts` must be a list.")
        posts = []

    post_by_id: dict[str, dict[str, Any]] = {}
    seq_by_id: dict[str, int] = {}
    seen_sequences: set[int] = set()

    ready_traceability_fail = False
    ready_valid_count = 0

    for i, post in enumerate(posts, start=1):
        prefix = f"posts[{i}]"
        if not isinstance(post, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        post_id = post.get("post_id")
        if not _is_nonempty_str(post_id):
            errors.append(f"`{prefix}.post_id` must be a non-empty string.")
            post_id = prefix
        elif post_id in post_by_id:
            errors.append(f"Duplicate post_id {post_id!r}.")
        else:
            post_by_id[post_id] = post

        sequence = post.get("sequence")
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
            errors.append(f"{post_id}: `sequence` must be a positive integer.")
        else:
            if sequence in seen_sequences:
                errors.append(f"Duplicate sequence number {sequence}.")
            seen_sequences.add(sequence)
            seq_by_id[post_id] = sequence

        reader_job = post.get("reader_job")
        if reader_job not in READER_JOBS:
            errors.append(
                f"{post_id}: invalid reader_job {reader_job!r}; "
                f"expected one of {sorted(READER_JOBS)}."
            )

        evidence_mode = post.get("evidence_mode")
        if evidence_mode not in EVIDENCE_MODES:
            errors.append(
                f"{post_id}: invalid evidence_mode {evidence_mode!r}; "
                f"expected one of {sorted(EVIDENCE_MODES)}."
            )

        drafting_status = post.get("drafting_status")
        if drafting_status not in DRAFTING_STATUSES:
            errors.append(
                f"{post_id}: invalid drafting_status {drafting_status!r}; "
                f"expected one of {sorted(DRAFTING_STATUSES)}."
            )

        author_input_required = post.get("author_input_required")
        if not isinstance(author_input_required, bool):
            errors.append(f"{post_id}: `author_input_required` must be boolean.")
            author_input_required = False

        author_input_needed = _string_list(
            errors, post.get("author_input_needed"), f"{post_id}.author_input_needed"
        )

        if drafting_status == "ready" and author_input_required:
            errors.append(
                f"{post_id}: ready post cannot have `author_input_required: true`."
            )

        if drafting_status == "needs_input":
            if not author_input_required:
                errors.append(
                    f"{post_id}: `needs_input` requires `author_input_required: true`."
                )
            if not author_input_needed:
                errors.append(
                    f"{post_id}: `needs_input` requires non-empty author_input_needed."
                )

        if evidence_mode == "story" and author_input_required and drafting_status == "ready":
            errors.append(
                f"{post_id}: story with missing genuine author input cannot be ready."
            )

        primary_insights = _string_list(
            errors, post.get("primary_insight_ids"), f"{post_id}.primary_insight_ids"
        )
        supporting_insights = _string_list(
            errors, post.get("supporting_insight_ids"), f"{post_id}.supporting_insight_ids"
        )
        primary_claims = _string_list(
            errors, post.get("primary_claim_ids"), f"{post_id}.primary_claim_ids"
        )
        secondary_claims = _string_list(
            errors, post.get("secondary_claim_ids"), f"{post_id}.secondary_claim_ids"
        )
        source_ids = _string_list(
            errors, post.get("source_ids"), f"{post_id}.source_ids"
        )
        prerequisite_ids = _string_list(
            errors, post.get("prerequisite_post_ids"), f"{post_id}.prerequisite_post_ids"
        )

        for sid in source_ids:
            if sid not in plan_sources:
                errors.append(
                    f"{post_id}: source_id {sid!r} is not listed in plan-level source_ids."
                )

        for cid in primary_claims + secondary_claims:
            if cid not in plan_claims:
                errors.append(
                    f"{post_id}: claim_id {cid!r} is not listed in plan-level claim_ids."
                )

        for iid in primary_insights + supporting_insights:
            if iid not in plan_insights:
                errors.append(
                    f"{post_id}: insight_id {iid!r} is not listed in plan-level insight_ids."
                )

        if drafting_status == "ready" and evidence_mode in TRACEABILITY_REQUIRED_MODES:
            has_sources = bool(source_ids)
            has_claims = bool(primary_claims or secondary_claims)
            has_insights = bool(primary_insights or supporting_insights)
            if not (has_sources and has_claims and has_insights):
                ready_traceability_fail = True
                missing = []
                if not has_sources:
                    missing.append("source")
                if not has_claims:
                    missing.append("claim")
                if not has_insights:
                    missing.append("insight")
                errors.append(
                    f"{post_id}: ready evidence-bearing post missing "
                    + ", ".join(missing)
                    + " traceability."
                )

        if drafting_status == "ready" and not author_input_required:
            ready_valid_count += 1

        # Store prerequisites for second pass.
        post["_validator_prerequisite_ids"] = prerequisite_ids

    # Prerequisite existence and ordering.
    prerequisite_order_valid = True
    for post_id, post in post_by_id.items():
        current_seq = seq_by_id.get(post_id)
        prereqs = post.get("_validator_prerequisite_ids", [])
        for prereq_id in prereqs:
            if prereq_id not in post_by_id:
                prerequisite_order_valid = False
                errors.append(
                    f"{post_id}: prerequisite {prereq_id!r} does not exist in posts."
                )
                continue
            prereq_seq = seq_by_id.get(prereq_id)
            if (
                current_seq is not None
                and prereq_seq is not None
                and prereq_seq >= current_seq
            ):
                prerequisite_order_valid = False
                errors.append(
                    f"{post_id}: prerequisite {prereq_id!r} must occur earlier "
                    f"(prerequisite sequence={prereq_seq}, current={current_seq})."
                )

    # Overlap review.
    overlap_review = plan.get("overlap_review")
    if not isinstance(overlap_review, list):
        errors.append("`overlap_review` must be a list.")
        overlap_review = []

    substantial_ready_overlap = False
    for i, item in enumerate(overlap_review, start=1):
        prefix = f"overlap_review[{i}]"
        if not isinstance(item, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        pair = _string_list(errors, item.get("post_ids"), f"{prefix}.post_ids")
        if len(pair) != 2:
            errors.append(f"`{prefix}.post_ids` must contain exactly two IDs.")

        level = item.get("overlap_level")
        action = item.get("action")
        if level not in OVERLAP_LEVELS:
            errors.append(
                f"`{prefix}.overlap_level` must be one of {sorted(OVERLAP_LEVELS)}."
            )
        if action not in OVERLAP_ACTIONS:
            errors.append(
                f"`{prefix}.action` must be one of {sorted(OVERLAP_ACTIONS)}."
            )

        if level == "substantial_overlap":
            if action == "none":
                errors.append(
                    f"`{prefix}` has substantial_overlap but action is `none`."
                )
            if len(pair) == 2 and all(pid in post_by_id for pid in pair):
                if all(post_by_id[pid].get("drafting_status") == "ready" for pid in pair):
                    substantial_ready_overlap = True
                    errors.append(
                        f"`{prefix}` leaves substantial overlap between two ready posts: "
                        f"{pair[0]} and {pair[1]}."
                    )

    checks = plan.get("series_checks")
    if not isinstance(checks, dict):
        errors.append("`series_checks` must be a mapping.")
        checks = {}

    expected_traceability_complete = not ready_traceability_fail
    if checks.get("substantial_overlap_remaining") is not substantial_ready_overlap:
        errors.append(
            "`series_checks.substantial_overlap_remaining` does not match "
            f"ready-post overlap state (expected {substantial_ready_overlap})."
        )

    if checks.get("prerequisite_order_valid") is not prerequisite_order_valid:
        errors.append(
            "`series_checks.prerequisite_order_valid` does not match "
            f"actual prerequisite order (expected {prerequisite_order_valid})."
        )

    if checks.get("evidence_traceability_complete") is not expected_traceability_complete:
        errors.append(
            "`series_checks.evidence_traceability_complete` does not match "
            f"ready-post traceability state (expected {expected_traceability_complete})."
        )

    handoff = plan.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("`handoff` must be a mapping.")
        handoff = {}

    expected_ready = (
        ready_valid_count > 0
        and not ready_traceability_fail
        and not substantial_ready_overlap
        and prerequisite_order_valid
    )

    if handoff.get("ready_for_drafting") is not expected_ready:
        errors.append(
            "`handoff.ready_for_drafting` does not match actual ready-post state "
            f"(expected {expected_ready})."
        )

    if expected_ready and handoff.get("next_skill") != "linkedin-post-drafter":
        errors.append(
            "Ready handoff must set `next_skill: linkedin-post-drafter`."
        )

    # Remove private validator keys in-memory (no file mutation).
    for post in posts:
        if isinstance(post, dict):
            post.pop("_validator_prerequisite_ids", None)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft LinkedIn series-plan YAML."
    )
    parser.add_argument("plan", help="Path to linkedin-series-plan.yaml")
    args = parser.parse_args()

    path = Path(args.plan).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    data = load_yaml(path)
    plan = data["linkedin_series_plan"]
    ready = sum(
        1
        for post in plan.get("posts", [])
        if isinstance(post, dict) and post.get("drafting_status") == "ready"
    )
    print(
        "PASS: LinkedIn series plan validated "
        f"(posts={len(plan.get('posts', []))}, ready={ready})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
