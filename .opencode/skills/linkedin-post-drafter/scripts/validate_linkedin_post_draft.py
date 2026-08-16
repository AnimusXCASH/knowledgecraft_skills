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

TRACEABILITY_REQUIRED_MODES = {
    "evidence_grounded",
    "evidence_informed_interpretation",
    "application_question",
}

DRAFT_STATUSES = {"ready_for_editing", "needs_input", "blocked"}

PRESERVATION_EXPECTED_READY = {
    "no_new_claims": True,
    "relationship_language_preserved": True,
    "causal_status_preserved": True,
    "uncertainty_preserved": True,
    "unsupported_mechanism_added": False,
    "personal_experience_invented": False,
    "unsupported_story_invented": False,
    "source_traceability_preserved": True,
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


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list_of_strings(
    errors: list[str],
    value: Any,
    field: str,
    *,
    unique: bool = True,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"`{field}` must be a list.")
        return []

    out: list[str] = []
    seen: set[str] = set()
    for i, item in enumerate(value, start=1):
        if not _nonempty_str(item):
            errors.append(f"`{field}[{i}]` must be a non-empty string.")
            continue
        if unique and item in seen:
            errors.append(f"`{field}` contains duplicate ID/value {item!r}.")
        seen.add(item)
        out.append(item)
    return out


def _validate_omitted(errors: list[str], value: Any) -> None:
    if not isinstance(value, list):
        errors.append("`omitted_or_deferred` must be a list.")
        return
    for i, entry in enumerate(value, start=1):
        prefix = f"omitted_or_deferred[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue
        if not _nonempty_str(entry.get("item")):
            errors.append(f"`{prefix}.item` must be a non-empty string.")
        if not _nonempty_str(entry.get("reason")):
            errors.append(f"`{prefix}.reason` must be a non-empty string.")


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    draft = data.get("linkedin_post_draft")
    if not isinstance(draft, dict):
        return ["Top-level `linkedin_post_draft` mapping is required."]

    for field in ("draft_id", "post_id", "audience", "main_point"):
        if not _nonempty_str(draft.get(field)):
            errors.append(f"`{field}` must be a non-empty string.")

    if draft.get("destination") != "LinkedIn":
        errors.append("`destination` must be exactly `LinkedIn`.")

    status = draft.get("draft_status")
    if status not in DRAFT_STATUSES:
        errors.append(
            f"`draft_status` must be one of {sorted(DRAFT_STATUSES)}."
        )

    reader_job = draft.get("reader_job")
    if reader_job not in READER_JOBS:
        errors.append(
            f"`reader_job` must be one of {sorted(READER_JOBS)}."
        )

    evidence_mode = draft.get("evidence_mode")
    if evidence_mode not in EVIDENCE_MODES:
        errors.append(
            f"`evidence_mode` must be one of {sorted(EVIDENCE_MODES)}."
        )

    source_ids = _list_of_strings(errors, draft.get("source_ids"), "source_ids")
    claims_available = _list_of_strings(
        errors, draft.get("claim_ids_available"), "claim_ids_available"
    )
    insights_available = _list_of_strings(
        errors, draft.get("insight_ids_available"), "insight_ids_available"
    )
    claims_used = _list_of_strings(
        errors, draft.get("claim_ids_used"), "claim_ids_used"
    )
    insights_used = _list_of_strings(
        errors, draft.get("insight_ids_used"), "insight_ids_used"
    )

    for cid in claims_used:
        if cid not in claims_available:
            errors.append(
                f"claim_ids_used contains {cid!r}, which is not in claim_ids_available."
            )

    for iid in insights_used:
        if iid not in insights_available:
            errors.append(
                f"insight_ids_used contains {iid!r}, which is not in insight_ids_available."
            )

    author_required = draft.get("author_input_required")
    if not isinstance(author_required, bool):
        errors.append("`author_input_required` must be boolean.")
        author_required = False

    author_needed = _list_of_strings(
        errors,
        draft.get("author_input_needed"),
        "author_input_needed",
        unique=False,
    )

    constraints = _list_of_strings(
        errors,
        draft.get("drafting_constraints"),
        "drafting_constraints",
        unique=False,
    )
    _ = constraints

    draft_text = draft.get("draft_text")
    if not isinstance(draft_text, str):
        errors.append("`draft_text` must be a string.")
        draft_text = ""

    _validate_omitted(errors, draft.get("omitted_or_deferred"))

    if status == "ready_for_editing":
        if not draft_text.strip():
            errors.append("ready_for_editing requires non-empty draft_text.")
        if author_required:
            errors.append(
                "ready_for_editing cannot have author_input_required: true."
            )
        if author_needed:
            errors.append(
                "ready_for_editing should not retain unresolved author_input_needed."
            )

        if evidence_mode in TRACEABILITY_REQUIRED_MODES:
            if not source_ids:
                errors.append(
                    "ready evidence-bearing draft requires at least one source_id."
                )
            if not claims_available:
                errors.append(
                    "ready evidence-bearing draft requires claim_ids_available."
                )
            if not claims_used:
                errors.append(
                    "ready evidence-bearing draft must use at least one allowed claim."
                )
            if not insights_available:
                errors.append(
                    "ready evidence-bearing draft requires insight_ids_available."
                )

    if status == "needs_input":
        if not author_required:
            errors.append(
                "needs_input requires author_input_required: true."
            )
        if not author_needed:
            errors.append(
                "needs_input requires non-empty author_input_needed."
            )
        if draft_text.strip():
            errors.append(
                "needs_input must leave draft_text empty until required input is supplied."
            )

    if status == "blocked":
        if draft_text.strip():
            errors.append(
                "blocked draft must leave draft_text empty."
            )

    checks = draft.get("preservation_checks")
    if not isinstance(checks, dict):
        errors.append("`preservation_checks` must be a mapping.")
        checks = {}

    checks_complete = True
    checks_safe = True
    for field, expected in PRESERVATION_EXPECTED_READY.items():
        value = checks.get(field)
        if not isinstance(value, bool):
            errors.append(f"`preservation_checks.{field}` must be boolean.")
            checks_complete = False
            checks_safe = False
            continue
        if status == "ready_for_editing" and value is not expected:
            errors.append(
                f"ready_for_editing requires preservation_checks.{field}: "
                f"{str(expected).lower()}."
            )
            checks_safe = False

    handoff = draft.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("`handoff` must be a mapping.")
        handoff = {}

    handoff_ready = handoff.get("ready_for_author_voice_edit")
    if not isinstance(handoff_ready, bool):
        errors.append("`handoff.ready_for_author_voice_edit` must be boolean.")
        handoff_ready = False

    traceability_ready = True
    if evidence_mode in TRACEABILITY_REQUIRED_MODES:
        traceability_ready = bool(
            source_ids and claims_available and claims_used and insights_available
        )

    expected_handoff_ready = bool(
        status == "ready_for_editing"
        and draft_text.strip()
        and not author_required
        and checks_complete
        and checks_safe
        and traceability_ready
    )

    if handoff_ready is not expected_handoff_ready:
        errors.append(
            "`handoff.ready_for_author_voice_edit` does not match draft state "
            f"(expected {expected_handoff_ready})."
        )

    if expected_handoff_ready and handoff.get("next_skill") != "author-voice-editor":
        errors.append(
            "Ready handoff must set `next_skill: author-voice-editor`."
        )

    if not expected_handoff_ready and handoff_ready:
        errors.append(
            "Non-ready draft cannot hand off to author-voice-editor."
        )

    notes = handoff.get("notes")
    if not isinstance(notes, list):
        errors.append("`handoff.notes` must be a list.")
    else:
        for i, note in enumerate(notes, start=1):
            if not _nonempty_str(note):
                errors.append(f"`handoff.notes[{i}]` must be a non-empty string.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft LinkedIn post-draft YAML."
    )
    parser.add_argument("draft", help="Path to a LinkedIn post draft YAML file")
    args = parser.parse_args()

    path = Path(args.draft).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    draft = load_yaml(path)["linkedin_post_draft"]
    print(
        "PASS: LinkedIn post draft validated "
        f"(post_id={draft.get('post_id')}, status={draft.get('draft_status')})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
