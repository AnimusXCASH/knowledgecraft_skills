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


PLATFORM_STATUSES = {"pass", "revise", "needs_current_verification"}
SEVERITIES = {"low", "medium", "high"}
ISSUE_STATUSES = {"open", "resolved", "advisory"}
LOCATIONS = {
    "opening", "body", "ending", "hashtags", "mentions", "link", "format", "series"
}
ISSUE_TYPES = {
    "opening_unclear",
    "opening_overclaim",
    "mobile_density",
    "over_fragmented",
    "list_misuse",
    "cta_forced",
    "engagement_bait",
    "hashtag_irrelevant",
    "hashtag_excessive",
    "mention_irrelevant",
    "mention_unverified",
    "link_interrupts_flow",
    "format_mismatch",
    "platform_claim_unverified",
    "series_presentation_repetition",
    "substance_change_required",
}
VERIFICATION_STATUSES = {"not_needed", "verified", "needs_current_verification"}

PLATFORM_CHECKS = (
    "first_screen_clear",
    "mobile_readable",
    "paragraphing_appropriate",
    "lists_content_shaped",
    "cta_appropriate",
    "engagement_bait_absent",
    "hashtags_relevant_or_absent",
    "mentions_relevant_or_absent",
    "link_treatment_reasonable",
    "format_fit_reasonable",
)

PRESERVATION_EXPECTED_PASS = {
    "substantive_meaning_preserved": True,
    "names_dates_numbers_preserved": True,
    "technical_terms_preserved": True,
    "relationship_language_preserved": True,
    "causal_status_preserved": True,
    "uncertainty_preserved": True,
    "limitations_preserved": True,
    "citations_preserved": True,
    "no_new_claims": True,
    "no_personal_experience_invented": True,
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


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    review = data.get("linkedin_platform_review")
    if not isinstance(review, dict):
        return ["Top-level `linkedin_platform_review` mapping is required."]

    for field in ("review_id", "post_id"):
        if not _nonempty_str(review.get(field)):
            errors.append(f"`{field}` must be a non-empty string.")

    if review.get("destination") != "LinkedIn":
        errors.append("`destination` must be exactly `LinkedIn`.")

    status = review.get("platform_status")
    if status not in PLATFORM_STATUSES:
        errors.append(
            f"`platform_status` must be one of {sorted(PLATFORM_STATUSES)}."
        )

    original = review.get("original_text")
    revised = review.get("revised_text")
    if not _nonempty_str(original):
        errors.append("`original_text` must be a non-empty string.")
    if not _nonempty_str(revised):
        errors.append("`revised_text` must be a non-empty string.")

    issues = review.get("issues")
    if not isinstance(issues, list):
        errors.append("`issues` must be a list.")
        issues = []

    issue_ids: set[str] = set()
    open_required = 0
    for i, issue in enumerate(issues, start=1):
        prefix = f"issues[{i}]"
        if not isinstance(issue, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        issue_id = issue.get("issue_id")
        if not _nonempty_str(issue_id):
            errors.append(f"`{prefix}.issue_id` must be a non-empty string.")
        elif issue_id in issue_ids:
            errors.append(f"Duplicate issue_id {issue_id!r}.")
        else:
            issue_ids.add(issue_id)

        issue_type = issue.get("issue_type")
        if issue_type not in ISSUE_TYPES:
            errors.append(
                f"`{prefix}.issue_type` must be one of {sorted(ISSUE_TYPES)}."
            )

        severity = issue.get("severity")
        if severity not in SEVERITIES:
            errors.append(
                f"`{prefix}.severity` must be one of {sorted(SEVERITIES)}."
            )

        location = issue.get("location")
        if location not in LOCATIONS:
            errors.append(
                f"`{prefix}.location` must be one of {sorted(LOCATIONS)}."
            )

        issue_status = issue.get("issue_status")
        if issue_status not in ISSUE_STATUSES:
            errors.append(
                f"`{prefix}.issue_status` must be one of {sorted(ISSUE_STATUSES)}."
            )

        change_required = issue.get("change_required")
        if not isinstance(change_required, bool):
            errors.append(f"`{prefix}.change_required` must be boolean.")
            change_required = False

        if change_required and issue_status == "advisory":
            errors.append(
                f"`{prefix}` cannot be advisory when change_required is true."
            )

        if change_required and issue_status == "open":
            open_required += 1

        if not _nonempty_str(issue.get("explanation")):
            errors.append(f"`{prefix}.explanation` must be a non-empty string.")

        if change_required and not _nonempty_str(issue.get("suggested_action")):
            errors.append(
                f"`{prefix}.suggested_action` must be non-empty when change_required is true."
            )

    if status == "pass" and open_required:
        errors.append(
            "`platform_status: pass` cannot retain open issues with change_required: true."
        )

    if status == "revise" and open_required == 0:
        errors.append(
            "`platform_status: revise` requires at least one open issue with change_required: true."
        )

    checks = review.get("platform_checks")
    if not isinstance(checks, dict):
        errors.append("`platform_checks` must be a mapping.")
        checks = {}

    platform_safe = True
    for field in PLATFORM_CHECKS:
        value = checks.get(field)
        if not isinstance(value, bool):
            errors.append(f"`platform_checks.{field}` must be boolean.")
            platform_safe = False
        elif status == "pass" and value is not True:
            errors.append(
                f"`platform_status: pass` requires platform_checks.{field}: true."
            )
            platform_safe = False

    current_claims = review.get("current_platform_claims")
    if not isinstance(current_claims, list):
        errors.append("`current_platform_claims` must be a list.")
        current_claims = []

    unresolved_material = 0
    for i, claim in enumerate(current_claims, start=1):
        prefix = f"current_platform_claims[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        if not _nonempty_str(claim.get("claim")):
            errors.append(f"`{prefix}.claim` must be a non-empty string.")

        material = claim.get("material_to_decision")
        if not isinstance(material, bool):
            errors.append(f"`{prefix}.material_to_decision` must be boolean.")
            material = False

        verification = claim.get("verification_status")
        if verification not in VERIFICATION_STATUSES:
            errors.append(
                f"`{prefix}.verification_status` must be one of "
                f"{sorted(VERIFICATION_STATUSES)}."
            )

        source_note = claim.get("source_note")
        if verification == "verified" and not _nonempty_str(source_note):
            errors.append(
                f"`{prefix}.source_note` must be non-empty when verification_status is verified."
            )

        if material and verification == "needs_current_verification":
            unresolved_material += 1

    if status == "pass" and unresolved_material:
        errors.append(
            "`platform_status: pass` cannot have unresolved material current-platform claims."
        )

    if status == "needs_current_verification" and unresolved_material == 0:
        errors.append(
            "`platform_status: needs_current_verification` requires at least one "
            "material claim with verification_status: needs_current_verification."
        )

    preservation = review.get("preservation_checks")
    if not isinstance(preservation, dict):
        errors.append("`preservation_checks` must be a mapping.")
        preservation = {}

    preservation_complete = True
    preservation_safe = True
    for field, expected in PRESERVATION_EXPECTED_PASS.items():
        value = preservation.get(field)
        if not isinstance(value, bool):
            errors.append(f"`preservation_checks.{field}` must be boolean.")
            preservation_complete = False
            preservation_safe = False
        elif value is not expected:
            preservation_safe = False
            if status == "pass":
                errors.append(
                    f"`platform_status: pass` requires preservation_checks.{field}: "
                    f"{str(expected).lower()}."
                )

    handoff = review.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("`handoff` must be a mapping.")
        handoff = {}

    ready = handoff.get("ready_for_factuality_review")
    if not isinstance(ready, bool):
        errors.append("`handoff.ready_for_factuality_review` must be boolean.")
        ready = False

    expected_ready = bool(
        status == "pass"
        and open_required == 0
        and unresolved_material == 0
        and platform_safe
        and preservation_complete
        and preservation_safe
        and _nonempty_str(revised)
    )

    if ready is not expected_ready:
        errors.append(
            "`handoff.ready_for_factuality_review` does not match review state "
            f"(expected {expected_ready})."
        )

    if expected_ready and handoff.get("next_skill") != "factuality-guard":
        errors.append(
            "Ready handoff must set `next_skill: factuality-guard`."
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
        description="Validate KnowledgeCraft LinkedIn platform-review YAML."
    )
    parser.add_argument("review", help="Path to a LinkedIn platform-review YAML file")
    args = parser.parse_args()

    path = Path(args.review).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    review = load_yaml(path)["linkedin_platform_review"]
    print(
        "PASS: LinkedIn platform review validated "
        f"(post_id={review.get('post_id')}, status={review.get('platform_status')})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
