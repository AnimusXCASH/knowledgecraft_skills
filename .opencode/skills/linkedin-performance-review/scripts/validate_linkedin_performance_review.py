from __future__ import annotations

import argparse
from datetime import datetime
from math import isclose
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "ERROR: PyYAML is required. Install with: py -m pip install pyyaml"
    ) from exc


COMPARABILITY = {
    "comparable",
    "partially_comparable",
    "not_comparable",
    "unknown",
}
PAID_STATUS = {"organic", "paid", "mixed", "unknown"}
LEARNING_CLASSES = {
    "strong_observation",
    "tentative_pattern",
    "test_next",
    "insufficient_data",
}

KNOWN_RATE_NUMERATORS = {
    "reaction_rate": "reactions",
    "comment_rate": "comments",
    "share_rate": "shares",
    "save_rate": "saves",
    "click_through_rate": "clicks",
    "profile_view_rate": "profile_views",
    "follow_rate": "follows",
    "lead_rate": "leads",
}

RAW_METRICS = (
    "impressions",
    "reactions",
    "comments",
    "shares",
    "saves",
    "clicks",
    "profile_views",
    "follows",
    "leads",
)


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


def _parse_dt(value: Any) -> datetime | None:
    if not _nonempty_str(value):
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _valid_count(value: Any) -> bool:
    return value is None or (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= 0
    )


def _number_or_none(value: Any) -> bool:
    return value is None or (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    )


def validate(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []

    review = data.get("linkedin_performance_review")
    if not isinstance(review, dict):
        return ["Top-level `linkedin_performance_review` mapping is required."]

    if not _nonempty_str(review.get("review_id")):
        errors.append("`review_id` must be a non-empty string.")

    scope = review.get("analysis_scope")
    if not isinstance(scope, dict):
        errors.append("`analysis_scope` must be a mapping.")
        scope = {}

    post_count = scope.get("post_count")
    if isinstance(post_count, bool) or not isinstance(post_count, int) or post_count < 0:
        errors.append("`analysis_scope.post_count` must be a non-negative integer.")

    metric_defs = review.get("metric_definitions")
    if not isinstance(metric_defs, list):
        errors.append("`metric_definitions` must be a list.")
        metric_defs = []

    metric_names: set[str] = set()
    for i, item in enumerate(metric_defs, start=1):
        prefix = f"metric_definitions[{i}]"
        if not isinstance(item, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue
        name = item.get("metric")
        if not _nonempty_str(name):
            errors.append(f"`{prefix}.metric` must be a non-empty string.")
        elif name in metric_names:
            errors.append(f"Duplicate metric definition {name!r}.")
        else:
            metric_names.add(name)
        for field in ("numerator", "denominator", "formula"):
            if not _nonempty_str(item.get(field)):
                errors.append(f"`{prefix}.{field}` must be a non-empty string.")

    posts = review.get("posts")
    if not isinstance(posts, list):
        errors.append("`posts` must be a list.")
        posts = []

    if isinstance(post_count, int) and not isinstance(post_count, bool):
        if post_count != len(posts):
            errors.append(
                "`analysis_scope.post_count` does not match number of post records "
                f"({post_count} != {len(posts)})."
            )

    post_ids: set[str] = set()
    experiment_ids_seen: set[str] = set()

    for i, post in enumerate(posts, start=1):
        prefix = f"posts[{i}]"
        if not isinstance(post, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        post_id = post.get("post_id")
        if not _nonempty_str(post_id):
            errors.append(f"`{prefix}.post_id` must be a non-empty string.")
            post_id = prefix
        elif post_id in post_ids:
            errors.append(f"Duplicate post_id {post_id!r}.")
        else:
            post_ids.add(post_id)

        comparability = post.get("comparability")
        if comparability not in COMPARABILITY:
            errors.append(
                f"{post_id}: `comparability` must be one of {sorted(COMPARABILITY)}."
            )

        paid = post.get("paid_status")
        if paid not in PAID_STATUS:
            errors.append(
                f"{post_id}: `paid_status` must be one of {sorted(PAID_STATUS)}."
            )

        window = post.get("observation_window_hours")
        if window is not None and (
            isinstance(window, bool)
            or not isinstance(window, (int, float))
            or window < 0
        ):
            errors.append(
                f"{post_id}: `observation_window_hours` must be null or non-negative numeric."
            )

        published = _parse_dt(post.get("published_at"))
        observed = _parse_dt(post.get("observed_at"))
        if published and observed:
            delta_hours = (observed - published).total_seconds() / 3600
            if delta_hours < 0:
                errors.append(f"{post_id}: observed_at precedes published_at.")
            elif isinstance(window, (int, float)) and not isinstance(window, bool):
                if not isclose(float(window), delta_hours, rel_tol=1e-9, abs_tol=1e-6):
                    errors.append(
                        f"{post_id}: observation_window_hours does not match timestamps "
                        f"(expected {delta_hours:g})."
                    )

        metadata = post.get("metadata")
        if not isinstance(metadata, dict):
            errors.append(f"{post_id}: `metadata` must be a mapping.")
            metadata = {}
        exp_id = metadata.get("experiment_id")
        if exp_id is not None:
            if not _nonempty_str(exp_id):
                errors.append(f"{post_id}: metadata.experiment_id must be null or non-empty.")
            else:
                experiment_ids_seen.add(exp_id)

        raw = post.get("raw_metrics")
        if not isinstance(raw, dict):
            errors.append(f"{post_id}: `raw_metrics` must be a mapping.")
            raw = {}

        for metric in RAW_METRICS:
            if metric not in raw:
                errors.append(f"{post_id}: raw_metrics.{metric} is required (use null if missing).")
                continue
            value = raw.get(metric)
            if not _valid_count(value):
                errors.append(
                    f"{post_id}: raw_metrics.{metric} must be a non-negative integer or null."
                )

        derived = post.get("derived_metrics")
        if not isinstance(derived, dict):
            errors.append(f"{post_id}: `derived_metrics` must be a mapping.")
            derived = {}

        for metric_name, metric in derived.items():
            m_prefix = f"{post_id}.derived_metrics.{metric_name}"
            if not isinstance(metric, dict):
                errors.append(f"`{m_prefix}` must be a mapping.")
                continue

            numerator = metric.get("numerator")
            denominator = metric.get("denominator")
            denominator_name = metric.get("denominator_name")
            proportion = metric.get("proportion")
            percent = metric.get("percent")

            for field, value in (
                ("numerator", numerator),
                ("denominator", denominator),
            ):
                if value is not None and (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or value < 0
                ):
                    errors.append(f"`{m_prefix}.{field}` must be null or non-negative numeric.")

            if not _nonempty_str(denominator_name):
                errors.append(f"`{m_prefix}.denominator_name` must be a non-empty string.")

            if not _number_or_none(proportion):
                errors.append(f"`{m_prefix}.proportion` must be numeric or null.")
            if not _number_or_none(percent):
                errors.append(f"`{m_prefix}.percent` must be numeric or null.")

            raw_num_name = KNOWN_RATE_NUMERATORS.get(metric_name)
            if raw_num_name is not None:
                raw_num = raw.get(raw_num_name)
                if raw_num is None:
                    if numerator is not None:
                        errors.append(
                            f"{m_prefix}: raw {raw_num_name} is null, so numerator must remain null."
                        )
                elif numerator is not None and float(numerator) != float(raw_num):
                    errors.append(
                        f"{m_prefix}: numerator does not match raw_metrics.{raw_num_name} "
                        f"({numerator} != {raw_num})."
                    )

            if denominator_name == "impressions":
                raw_imp = raw.get("impressions")
                if raw_imp is None:
                    if denominator is not None:
                        errors.append(
                            f"{m_prefix}: raw impressions are null, so denominator must remain null."
                        )
                elif denominator is not None and float(denominator) != float(raw_imp):
                    errors.append(
                        f"{m_prefix}: denominator does not match raw_metrics.impressions "
                        f"({denominator} != {raw_imp})."
                    )

            if numerator is None or denominator is None or denominator == 0:
                if proportion is not None or percent is not None:
                    errors.append(
                        f"{m_prefix}: numeric rate is invalid when numerator/denominator is missing "
                        "or denominator is zero."
                    )
            else:
                expected_prop = float(numerator) / float(denominator)
                expected_pct = expected_prop * 100.0
                if proportion is None or not isclose(
                    float(proportion), expected_prop, rel_tol=1e-9, abs_tol=1e-9
                ):
                    errors.append(
                        f"{m_prefix}: proportion is mathematically inconsistent "
                        f"(expected {expected_prop:g})."
                    )
                if percent is None or not isclose(
                    float(percent), expected_pct, rel_tol=1e-9, abs_tol=1e-7
                ):
                    errors.append(
                        f"{m_prefix}: percent is mathematically inconsistent "
                        f"(expected {expected_pct:g})."
                    )

        _string_list(errors, post.get("data_quality_flags"), f"{post_id}.data_quality_flags")

    comparisons = review.get("comparisons")
    if not isinstance(comparisons, list):
        errors.append("`comparisons` must be a list.")
        comparisons = []

    comparison_ids: set[str] = set()
    for i, comp in enumerate(comparisons, start=1):
        prefix = f"comparisons[{i}]"
        if not isinstance(comp, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        comp_id = comp.get("comparison_id")
        if not _nonempty_str(comp_id):
            errors.append(f"`{prefix}.comparison_id` must be a non-empty string.")
            comp_id = prefix
        elif comp_id in comparison_ids:
            errors.append(f"Duplicate comparison_id {comp_id!r}.")
        else:
            comparison_ids.add(comp_id)

        if not _nonempty_str(comp.get("question")):
            errors.append(f"{comp_id}: `question` must be a non-empty string.")

        if comp.get("comparability") not in COMPARABILITY:
            errors.append(
                f"{comp_id}: `comparability` must be one of {sorted(COMPARABILITY)}."
            )

        groups = comp.get("groups")
        if not isinstance(groups, list):
            errors.append(f"{comp_id}: `groups` must be a list.")
            groups = []

        for j, group in enumerate(groups, start=1):
            g_prefix = f"{comp_id}.groups[{j}]"
            if not isinstance(group, dict):
                errors.append(f"`{g_prefix}` must be a mapping.")
                continue
            if not _nonempty_str(group.get("label")):
                errors.append(f"`{g_prefix}.label` must be a non-empty string.")
            ids = _string_list(errors, group.get("post_ids"), f"{g_prefix}.post_ids")
            for pid in ids:
                if pid not in post_ids:
                    errors.append(f"{g_prefix}: unknown post_id {pid!r}.")
            n = group.get("n")
            if isinstance(n, bool) or not isinstance(n, int) or n < 0:
                errors.append(f"`{g_prefix}.n` must be a non-negative integer.")
            elif n != len(ids):
                errors.append(
                    f"`{g_prefix}.n` does not match listed post_ids ({n} != {len(ids)})."
                )
            if not isinstance(group.get("summary_metrics"), dict):
                errors.append(f"`{g_prefix}.summary_metrics` must be a mapping.")

        if not isinstance(comp.get("descriptive_result"), str):
            errors.append(f"{comp_id}: `descriptive_result` must be a string.")
        _string_list(errors, comp.get("caveats"), f"{comp_id}.caveats")

    learnings = review.get("learnings")
    if not isinstance(learnings, list):
        errors.append("`learnings` must be a list.")
        learnings = []

    learning_ids: set[str] = set()
    for i, learning in enumerate(learnings, start=1):
        prefix = f"learnings[{i}]"
        if not isinstance(learning, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        learning_id = learning.get("learning_id")
        if not _nonempty_str(learning_id):
            errors.append(f"`{prefix}.learning_id` must be a non-empty string.")
            learning_id = prefix
        elif learning_id in learning_ids:
            errors.append(f"Duplicate learning_id {learning_id!r}.")
        else:
            learning_ids.add(learning_id)

        classification = learning.get("classification")
        if classification not in LEARNING_CLASSES:
            errors.append(
                f"{learning_id}: `classification` must be one of {sorted(LEARNING_CLASSES)}."
            )

        if not _nonempty_str(learning.get("statement")):
            errors.append(f"{learning_id}: `statement` must be a non-empty string.")

        supporting_posts = _string_list(
            errors, learning.get("supporting_post_ids"), f"{learning_id}.supporting_post_ids"
        )
        for pid in supporting_posts:
            if pid not in post_ids:
                errors.append(f"{learning_id}: unknown supporting post_id {pid!r}.")

        supporting_comps = _string_list(
            errors,
            learning.get("supporting_comparison_ids"),
            f"{learning_id}.supporting_comparison_ids",
        )
        for cid in supporting_comps:
            if cid not in comparison_ids:
                errors.append(f"{learning_id}: unknown supporting comparison_id {cid!r}.")

        if classification == "strong_observation" and len(set(supporting_posts)) < 2:
            errors.append(
                f"{learning_id}: strong_observation requires at least two supporting posts."
            )

        if not _nonempty_str(learning.get("evidence_basis")):
            errors.append(f"{learning_id}: `evidence_basis` must be a non-empty string.")

        _string_list(
            errors,
            learning.get("confounders_or_alternatives"),
            f"{learning_id}.confounders_or_alternatives",
        )

        if not isinstance(learning.get("reusable"), bool):
            errors.append(f"{learning_id}: `reusable` must be boolean.")

    future_tests = review.get("future_tests")
    if not isinstance(future_tests, list):
        errors.append("`future_tests` must be a list.")
        future_tests = []

    test_ids: set[str] = set()
    for i, test in enumerate(future_tests, start=1):
        prefix = f"future_tests[{i}]"
        if not isinstance(test, dict):
            errors.append(f"`{prefix}` must be a mapping.")
            continue

        test_id = test.get("test_id")
        if not _nonempty_str(test_id):
            errors.append(f"`{prefix}.test_id` must be a non-empty string.")
        elif test_id in test_ids:
            errors.append(f"Duplicate test_id {test_id!r}.")
        else:
            test_ids.add(test_id)

        for field in ("question", "major_variable", "interpretation_guard"):
            if not _nonempty_str(test.get(field)):
                errors.append(f"`{prefix}.{field}` must be a non-empty string.")

        variants = _string_list(errors, test.get("variants"), f"{prefix}.variants")
        if len(variants) < 2:
            errors.append(f"`{prefix}.variants` must contain at least two variants.")

        _string_list(
            errors,
            test.get("controls_or_constants"),
            f"{prefix}.controls_or_constants",
        )

    global_quality = review.get("global_data_quality")
    if not isinstance(global_quality, dict):
        errors.append("`global_data_quality` must be a mapping.")
        global_quality = {}
    _string_list(errors, global_quality.get("issues"), "global_data_quality.issues")
    if global_quality.get("overall_comparability") not in COMPARABILITY:
        errors.append(
            "`global_data_quality.overall_comparability` must use allowed comparability vocabulary."
        )

    summary = review.get("summary")
    if not isinstance(summary, dict):
        errors.append("`summary` must be a mapping.")
        summary = {}
    _string_list(
        errors,
        summary.get("insufficient_data_questions"),
        "summary.insufficient_data_questions",
    )

    handoff = review.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("`handoff` must be a mapping.")
        handoff = {}

    ready = handoff.get("ready_for_reuse")
    if not isinstance(ready, bool):
        errors.append("`handoff.ready_for_reuse` must be boolean.")
        ready = False

    if ready and handoff.get("next_skill") != "linkedin-series-architect":
        errors.append(
            "Ready handoff must set `next_skill: linkedin-series-architect`."
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
        description="Validate KnowledgeCraft LinkedIn performance-review YAML."
    )
    parser.add_argument("review", help="Path to linkedin-performance-review.yaml")
    args = parser.parse_args()

    path = Path(args.review).resolve()
    errors = validate(path)

    if errors:
        print(f"FAIL: {len(errors)} validation issue(s)")
        for idx, error in enumerate(errors, start=1):
            print(f"{idx}. {error}")
        print(f"File: {path}")
        return 1

    review = load_yaml(path)["linkedin_performance_review"]
    print(
        "PASS: LinkedIn performance review validated "
        f"(posts={len(review.get('posts', []))}, "
        f"comparisons={len(review.get('comparisons', []))}, "
        f"learnings={len(review.get('learnings', []))}, "
        f"ready_for_reuse={review.get('handoff', {}).get('ready_for_reuse')})"
    )
    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
