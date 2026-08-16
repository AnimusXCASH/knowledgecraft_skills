from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "ERROR: PyYAML is required. Install with: py -m pip install pyyaml"
    ) from exc


PROFILE_CONFIDENCE = {"provisional", "moderate", "strong"}
TRAIT_CONFIDENCE = {"high", "medium", "low"}
AUTHORSHIP = {"confirmed", "probable", "uncertain"}
UNCERTAIN_STATUS = {"not_observed", "uncertain", "contradicted"}
LANGUAGE_STABILITY = {"recurring", "occasional", "not_stable"}

SAMPLE_ID_RE = re.compile(r"^VOICE-S\d{3,}$")


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


def _validate_id_list(
    errors: list[str],
    value: Any,
    field: str,
    known_ids: set[str],
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"`{field}` must be a list.")
        return []

    out: list[str] = []
    for idx, item in enumerate(value, start=1):
        if not _nonempty_string(item):
            errors.append(f"`{field}[{idx}]` must be a non-empty sample ID.")
            continue
        out.append(item)
        if item not in known_ids:
            errors.append(f"`{field}` references unknown sample ID {item!r}.")
    return out


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    profile = data.get("author_voice_profile")
    if not isinstance(profile, dict):
        return ["Top-level `author_voice_profile` mapping is required."]

    samples = profile.get("samples")
    if not isinstance(samples, list):
        errors.append("`samples` must be a list.")
        samples = []

    sample_by_id: dict[str, dict[str, Any]] = {}
    eligible_count = 0
    uncertain_count = 0

    for idx, sample in enumerate(samples, start=1):
        prefix = f"samples[{idx}]"
        if not isinstance(sample, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        sample_id = sample.get("sample_id")
        authorship = sample.get("authorship")
        eligible = sample.get("eligible_for_inference")

        if not _nonempty_string(sample_id):
            errors.append(f"`{prefix}.sample_id` must be a non-empty string.")
            continue

        if not SAMPLE_ID_RE.match(sample_id):
            errors.append(
                f"`{prefix}.sample_id` {sample_id!r} must match VOICE-S###."
            )

        if sample_id in sample_by_id:
            errors.append(f"Duplicate sample ID {sample_id!r}.")
        else:
            sample_by_id[sample_id] = sample

        if authorship not in AUTHORSHIP:
            errors.append(
                f"`{prefix}.authorship` must be one of {sorted(AUTHORSHIP)}."
            )

        if not isinstance(eligible, bool):
            errors.append(f"`{prefix}.eligible_for_inference` must be boolean.")
        elif eligible:
            eligible_count += 1

        if authorship == "uncertain":
            uncertain_count += 1

    known_ids = set(sample_by_id)

    count = profile.get("sample_count")
    if not isinstance(count, dict):
        errors.append("`sample_count` must be a mapping.")
    else:
        expected_total = len(samples)
        if count.get("total") != expected_total:
            errors.append(
                f"`sample_count.total` is {count.get('total')!r}; "
                f"expected {expected_total}."
            )
        if count.get("eligible") != eligible_count:
            errors.append(
                f"`sample_count.eligible` is {count.get('eligible')!r}; "
                f"expected {eligible_count}."
            )
        if count.get("uncertain") != uncertain_count:
            errors.append(
                f"`sample_count.uncertain` is {count.get('uncertain')!r}; "
                f"expected {uncertain_count}."
            )

    profile_confidence = profile.get("profile_confidence")
    if profile_confidence not in PROFILE_CONFIDENCE:
        errors.append(
            f"`profile_confidence` must be one of {sorted(PROFILE_CONFIDENCE)}."
        )
    else:
        expected_confidence = (
            "provisional"
            if eligible_count < 3
            else "moderate"
            if eligible_count < 8
            else "strong"
        )
        if profile_confidence != expected_confidence:
            errors.append(
                f"`profile_confidence` is {profile_confidence!r}; "
                f"expected {expected_confidence!r} from {eligible_count} "
                "eligible sample(s)."
            )

    # Stable traits.
    stable_traits = profile.get("stable_traits")
    if not isinstance(stable_traits, list):
        errors.append("`stable_traits` must be a list.")
        stable_traits = []

    for idx, trait in enumerate(stable_traits, start=1):
        prefix = f"stable_traits[{idx}]"
        if not isinstance(trait, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        confidence = trait.get("confidence")
        if confidence not in TRAIT_CONFIDENCE:
            errors.append(
                f"`{prefix}.confidence` must be one of "
                f"{sorted(TRAIT_CONFIDENCE)}."
            )

        supporting = _validate_id_list(
            errors,
            trait.get("supporting_sample_ids"),
            f"{prefix}.supporting_sample_ids",
            known_ids,
        )
        _validate_id_list(
            errors,
            trait.get("counterexample_sample_ids"),
            f"{prefix}.counterexample_sample_ids",
            known_ids,
        )

        if confidence == "high" and len(set(supporting)) < 2:
            errors.append(
                f"`{prefix}` has high confidence but fewer than two "
                "supporting samples."
            )

        if confidence == "high":
            for sample_id in supporting:
                sample = sample_by_id.get(sample_id, {})
                if sample.get("authorship") == "uncertain":
                    errors.append(
                        f"`{prefix}` high-confidence trait cites uncertain "
                        f"authorship sample {sample_id!r}."
                    )
                if sample.get("eligible_for_inference") is not True:
                    errors.append(
                        f"`{prefix}` high-confidence trait cites ineligible "
                        f"sample {sample_id!r}."
                    )

    # Context profiles and traits.
    context_profiles = profile.get("context_profiles")
    if not isinstance(context_profiles, list):
        errors.append("`context_profiles` must be a list.")
        context_profiles = []

    for cidx, context in enumerate(context_profiles, start=1):
        prefix = f"context_profiles[{cidx}]"
        if not isinstance(context, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        if context.get("confidence") not in TRAIT_CONFIDENCE:
            errors.append(
                f"`{prefix}.confidence` must be one of "
                f"{sorted(TRAIT_CONFIDENCE)}."
            )

        traits = context.get("traits")
        if not isinstance(traits, list):
            errors.append(f"`{prefix}.traits` must be a list.")
            continue

        for tidx, trait in enumerate(traits, start=1):
            tprefix = f"{prefix}.traits[{tidx}]"
            if not isinstance(trait, dict):
                errors.append(f"`{tprefix}` must be a mapping.")
                continue

            confidence = trait.get("confidence")
            if confidence not in TRAIT_CONFIDENCE:
                errors.append(
                    f"`{tprefix}.confidence` must be one of "
                    f"{sorted(TRAIT_CONFIDENCE)}."
                )

            supporting = _validate_id_list(
                errors,
                trait.get("supporting_sample_ids"),
                f"{tprefix}.supporting_sample_ids",
                known_ids,
            )
            _validate_id_list(
                errors,
                trait.get("counterexample_sample_ids"),
                f"{tprefix}.counterexample_sample_ids",
                known_ids,
            )

            if confidence == "high" and len(set(supporting)) < 2:
                errors.append(
                    f"`{tprefix}` has high confidence but fewer than two "
                    "supporting samples."
                )

            if confidence == "high":
                for sample_id in supporting:
                    sample = sample_by_id.get(sample_id, {})
                    if sample.get("authorship") == "uncertain":
                        errors.append(
                            f"`{tprefix}` high-confidence trait cites uncertain "
                            f"authorship sample {sample_id!r}."
                        )
                    if sample.get("eligible_for_inference") is not True:
                        errors.append(
                            f"`{tprefix}` high-confidence trait cites ineligible "
                            f"sample {sample_id!r}."
                        )

    recurring = profile.get("recurring_language")
    if not isinstance(recurring, list):
        errors.append("`recurring_language` must be a list.")
        recurring = []
    else:
        for idx, item in enumerate(recurring, start=1):
            prefix = f"recurring_language[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"`{prefix}` must be a mapping.")
                continue

            if item.get("stability") not in LANGUAGE_STABILITY:
                errors.append(
                    f"`{prefix}.stability` must be one of "
                    f"{sorted(LANGUAGE_STABILITY)}."
                )

            _validate_id_list(
                errors,
                item.get("supporting_sample_ids"),
                f"{prefix}.supporting_sample_ids",
                known_ids,
            )

    uncertain = profile.get("not_observed_or_uncertain")
    if not isinstance(uncertain, list):
        errors.append("`not_observed_or_uncertain` must be a list.")
    else:
        for idx, item in enumerate(uncertain, start=1):
            prefix = f"not_observed_or_uncertain[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"`{prefix}` must be a mapping.")
                continue
            if item.get("status") not in UNCERTAIN_STATUS:
                errors.append(
                    f"`{prefix}.status` must be one of "
                    f"{sorted(UNCERTAIN_STATUS)}."
                )

    downstream = profile.get("downstream_guidance")
    if not isinstance(downstream, dict):
        errors.append("`downstream_guidance` must be a mapping.")
    else:
        for key in ("preserve", "use_selectively", "avoid_overfitting"):
            value = downstream.get(key)
            if not isinstance(value, list):
                errors.append(f"`downstream_guidance.{key}` must be a list.")

    limitations = profile.get("limitations")
    if not isinstance(limitations, list):
        errors.append("`limitations` must be a list.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate KnowledgeCraft author voice profile structure."
    )
    parser.add_argument("profile", help="Path to author voice profile YAML.")
    args = parser.parse_args()

    path = Path(args.profile).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    data = load_yaml(path)
    profile = data["author_voice_profile"]
    eligible = profile["sample_count"]["eligible"]
    print(
        "PASS: author voice profile validated "
        f"(confidence={profile['profile_confidence']}, eligible={eligible})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
