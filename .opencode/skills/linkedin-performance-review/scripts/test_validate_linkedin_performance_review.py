from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_linkedin_performance_review as v


def base_review():
    return {
        "linkedin_performance_review": {
            "review_id": "LPRF-001",
            "analysis_scope": {
                "start_date": "2026-09-01",
                "end_date": "2026-09-08",
                "post_count": 2,
                "objective": "save/reference value",
            },
            "metric_definitions": [
                {
                    "metric": "save_rate",
                    "numerator": "saves",
                    "denominator": "impressions",
                    "formula": "saves / impressions",
                }
            ],
            "posts": [
                {
                    "post_id": "POST-001",
                    "published_at": "2026-09-01T08:00:00",
                    "observed_at": "2026-09-08T08:00:00",
                    "observation_window_hours": 168,
                    "comparability": "comparable",
                    "paid_status": "organic",
                    "metadata": {
                        "pillar": "evidence",
                        "reader_job": "evidence",
                        "format": "text",
                        "opening_type": "evidence-led",
                        "cta_type": "none",
                        "experiment_id": "EXP-1",
                        "experiment_variant": "evidence-led",
                    },
                    "raw_metrics": {
                        "impressions": 2000,
                        "reactions": 80,
                        "comments": 10,
                        "shares": 5,
                        "saves": 20,
                        "clicks": 15,
                        "profile_views": 8,
                        "follows": 2,
                        "leads": 0,
                    },
                    "derived_metrics": {
                        "save_rate": {
                            "numerator": 20,
                            "denominator": 2000,
                            "denominator_name": "impressions",
                            "proportion": 0.01,
                            "percent": 1.0,
                        }
                    },
                    "data_quality_flags": [],
                },
                {
                    "post_id": "POST-002",
                    "published_at": "2026-09-01T08:00:00",
                    "observed_at": "2026-09-08T08:00:00",
                    "observation_window_hours": 168,
                    "comparability": "comparable",
                    "paid_status": "organic",
                    "metadata": {
                        "pillar": "application",
                        "reader_job": "application",
                        "format": "text",
                        "opening_type": "application-led",
                        "cta_type": "none",
                        "experiment_id": "EXP-1",
                        "experiment_variant": "application-led",
                    },
                    "raw_metrics": {
                        "impressions": 1000,
                        "reactions": 30,
                        "comments": 5,
                        "shares": 2,
                        "saves": 5,
                        "clicks": None,
                        "profile_views": None,
                        "follows": None,
                        "leads": None,
                    },
                    "derived_metrics": {
                        "save_rate": {
                            "numerator": 5,
                            "denominator": 1000,
                            "denominator_name": "impressions",
                            "proportion": 0.005,
                            "percent": 0.5,
                        },
                        "click_through_rate": {
                            "numerator": None,
                            "denominator": 1000,
                            "denominator_name": "impressions",
                            "proportion": None,
                            "percent": None,
                        },
                    },
                    "data_quality_flags": [],
                },
            ],
            "comparisons": [
                {
                    "comparison_id": "CMP-001",
                    "question": "Do opening variants differ in save rate?",
                    "groups": [
                        {
                            "label": "evidence-led",
                            "post_ids": ["POST-001"],
                            "n": 1,
                            "summary_metrics": {"median_save_rate_percent": 1.0},
                        },
                        {
                            "label": "application-led",
                            "post_ids": ["POST-002"],
                            "n": 1,
                            "summary_metrics": {"median_save_rate_percent": 0.5},
                        },
                    ],
                    "comparability": "comparable",
                    "descriptive_result": "Evidence-led was higher in this two-post sample.",
                    "caveats": ["n=1 per group"],
                }
            ],
            "learnings": [
                {
                    "learning_id": "LRN-001",
                    "classification": "test_next",
                    "statement": "The opening difference is worth testing with more posts.",
                    "supporting_post_ids": ["POST-001", "POST-002"],
                    "supporting_comparison_ids": ["CMP-001"],
                    "evidence_basis": "One post per variant.",
                    "confounders_or_alternatives": ["small group n"],
                    "reusable": True,
                }
            ],
            "future_tests": [
                {
                    "test_id": "TEST-001",
                    "question": "Does opening approach coincide with save-rate differences?",
                    "major_variable": "opening approach",
                    "variants": ["evidence-led", "application-led"],
                    "primary_metric": "save_rate",
                    "controls_or_constants": ["topic family", "format", "observation window"],
                    "interpretation_guard": "Observational content test; do not infer causality from post-to-post differences alone.",
                }
            ],
            "global_data_quality": {
                "issues": ["small_group_n"],
                "overall_comparability": "comparable",
            },
            "summary": {
                "strongest_observation": None,
                "most_useful_tentative_pattern": None,
                "highest_priority_test_next": "TEST-001",
                "insufficient_data_questions": [],
            },
            "handoff": {
                "ready_for_reuse": True,
                "next_skill": "linkedin-series-architect",
                "notes": ["Retain small-sample caveat."],
            },
        }
    }


class PerformanceReviewValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "review.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_review_passes(self):
        self.assertEqual(v.validate(self.write(base_review())), [])

    def test_post_count_must_match(self):
        data = base_review()
        data["linkedin_performance_review"]["analysis_scope"]["post_count"] = 3
        errors = v.validate(self.write(data))
        self.assertTrue(any("post_count" in e for e in errors))

    def test_raw_metric_cannot_be_negative(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][0]["raw_metrics"]["saves"] = -1
        errors = v.validate(self.write(data))
        self.assertTrue(any("raw_metrics.saves" in e for e in errors))

    def test_missing_raw_metric_stays_missing(self):
        data = base_review()
        p = data["linkedin_performance_review"]["posts"][1]
        p["derived_metrics"]["click_through_rate"]["numerator"] = 0
        errors = v.validate(self.write(data))
        self.assertTrue(any("raw clicks is null" in e for e in errors))

    def test_zero_denominator_cannot_have_numeric_rate(self):
        data = base_review()
        p = data["linkedin_performance_review"]["posts"][0]
        p["raw_metrics"]["impressions"] = 0
        p["derived_metrics"]["save_rate"] = {
            "numerator": 20,
            "denominator": 0,
            "denominator_name": "impressions",
            "proportion": 0.0,
            "percent": 0.0,
        }
        errors = v.validate(self.write(data))
        self.assertTrue(any("numeric rate is invalid" in e for e in errors))

    def test_numerator_must_match_raw(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][0]["derived_metrics"]["save_rate"]["numerator"] = 19
        errors = v.validate(self.write(data))
        self.assertTrue(any("numerator does not match" in e for e in errors))

    def test_denominator_must_match_impressions(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][0]["derived_metrics"]["save_rate"]["denominator"] = 1900
        errors = v.validate(self.write(data))
        self.assertTrue(any("denominator does not match" in e for e in errors))

    def test_proportion_arithmetic_checked(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][0]["derived_metrics"]["save_rate"]["proportion"] = 0.02
        errors = v.validate(self.write(data))
        self.assertTrue(any("proportion is mathematically inconsistent" in e for e in errors))

    def test_percent_arithmetic_checked(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][0]["derived_metrics"]["save_rate"]["percent"] = 2.0
        errors = v.validate(self.write(data))
        self.assertTrue(any("percent is mathematically inconsistent" in e for e in errors))

    def test_observation_window_checked(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][0]["observation_window_hours"] = 24
        errors = v.validate(self.write(data))
        self.assertTrue(any("observation_window_hours does not match" in e for e in errors))

    def test_duplicate_post_id_fails(self):
        data = base_review()
        data["linkedin_performance_review"]["posts"][1]["post_id"] = "POST-001"
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate post_id" in e for e in errors))

    def test_comparison_group_n_must_match(self):
        data = base_review()
        data["linkedin_performance_review"]["comparisons"][0]["groups"][0]["n"] = 2
        errors = v.validate(self.write(data))
        self.assertTrue(any(".n` does not match" in e for e in errors))

    def test_unknown_comparison_post_fails(self):
        data = base_review()
        data["linkedin_performance_review"]["comparisons"][0]["groups"][0]["post_ids"] = ["POST-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("unknown post_id" in e for e in errors))

    def test_unknown_learning_support_post_fails(self):
        data = base_review()
        data["linkedin_performance_review"]["learnings"][0]["supporting_post_ids"] = ["POST-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("unknown supporting post_id" in e for e in errors))

    def test_strong_observation_requires_two_posts(self):
        data = base_review()
        l = data["linkedin_performance_review"]["learnings"][0]
        l["classification"] = "strong_observation"
        l["supporting_post_ids"] = ["POST-001"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("strong_observation requires at least two" in e for e in errors))

    def test_future_test_needs_two_variants(self):
        data = base_review()
        data["linkedin_performance_review"]["future_tests"][0]["variants"] = ["evidence-led"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("at least two variants" in e for e in errors))

    def test_ready_handoff_skill_must_match(self):
        data = base_review()
        data["linkedin_performance_review"]["handoff"]["next_skill"] = "wrong-skill"
        errors = v.validate(self.write(data))
        self.assertTrue(any("linkedin-series-architect" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
