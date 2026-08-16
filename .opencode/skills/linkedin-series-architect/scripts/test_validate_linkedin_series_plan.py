from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_linkedin_series_plan as v


def base_plan():
    return {
        "linkedin_series_plan": {
            "series_id": "LIS-001",
            "title": None,
            "objective": "Synthetic test",
            "audience": "coaches",
            "series_status": "needs_input",
            "source_ids": ["SRC-1", "SRC-2"],
            "insight_ids": ["INS-1", "INS-2"],
            "claim_ids": ["CLM-1", "CLM-2"],
            "pillars": [],
            "posts": [
                {
                    "post_id": "POST-001",
                    "sequence": 1,
                    "working_title": "Evidence post",
                    "drafting_status": "ready",
                    "pillar_ids": [],
                    "audience": "coaches",
                    "audience_problem_or_question": "What does this finding mean?",
                    "reader_job": "evidence",
                    "evidence_mode": "evidence_grounded",
                    "primary_insight_ids": ["INS-1"],
                    "supporting_insight_ids": [],
                    "primary_claim_ids": ["CLM-1"],
                    "secondary_claim_ids": [],
                    "source_ids": ["SRC-1"],
                    "main_point": "A grounded finding.",
                    "why_separate_post": "Distinct evidence job.",
                    "prerequisite_post_ids": [],
                    "opening_mechanism": "evidence-led statement",
                    "ending_function": "takeaway",
                    "recommended_format": "text post",
                    "author_input_required": False,
                    "author_input_needed": [],
                    "drafting_constraints": [],
                },
                {
                    "post_id": "POST-002",
                    "sequence": 2,
                    "working_title": "Synthesis",
                    "drafting_status": "ready",
                    "pillar_ids": [],
                    "audience": "coaches",
                    "audience_problem_or_question": "How do the ideas connect?",
                    "reader_job": "synthesis",
                    "evidence_mode": "evidence_informed_interpretation",
                    "primary_insight_ids": ["INS-2"],
                    "supporting_insight_ids": ["INS-1"],
                    "primary_claim_ids": ["CLM-2"],
                    "secondary_claim_ids": ["CLM-1"],
                    "source_ids": ["SRC-1", "SRC-2"],
                    "main_point": "A synthesis.",
                    "why_separate_post": "Depends on POST-001.",
                    "prerequisite_post_ids": ["POST-001"],
                    "opening_mechanism": "conceptual tension",
                    "ending_function": "synthesis",
                    "recommended_format": "text post",
                    "author_input_required": False,
                    "author_input_needed": [],
                    "drafting_constraints": [],
                },
                {
                    "post_id": "POST-003",
                    "sequence": 3,
                    "working_title": "Story",
                    "drafting_status": "needs_input",
                    "pillar_ids": [],
                    "audience": "coaches",
                    "audience_problem_or_question": "What did this look like in practice?",
                    "reader_job": "story",
                    "evidence_mode": "story",
                    "primary_insight_ids": [],
                    "supporting_insight_ids": [],
                    "primary_claim_ids": [],
                    "secondary_claim_ids": [],
                    "source_ids": [],
                    "main_point": "A genuine story if supplied.",
                    "why_separate_post": "Narrative reader job.",
                    "prerequisite_post_ids": [],
                    "opening_mechanism": "real story",
                    "ending_function": "reflection",
                    "recommended_format": "narrative post",
                    "author_input_required": True,
                    "author_input_needed": ["A genuine coaching story."],
                    "drafting_constraints": ["Do not invent the story."],
                },
            ],
            "overlap_review": [
                {
                    "post_ids": ["POST-001", "POST-002"],
                    "overlap_level": "partial_overlap",
                    "overlap_dimensions": ["supporting evidence"],
                    "action": "none",
                    "note": "Distinct reader jobs.",
                }
            ],
            "series_checks": {
                "substantial_overlap_remaining": False,
                "prerequisite_order_valid": True,
                "every_post_has_distinct_reader_job_or_reason": True,
                "evidence_traceability_complete": True,
                "unsupported_story_material_required": False,
            },
            "handoff": {
                "ready_for_drafting": True,
                "next_skill": "linkedin-post-drafter",
                "notes": ["POST-003 needs author input."],
            },
        }
    }


class SeriesPlanValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "plan.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_plan_passes(self):
        self.assertEqual(v.validate(self.write(base_plan())), [])

    def test_duplicate_post_id_fails(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][1]["post_id"] = "POST-001"
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate post_id" in e for e in errors))

    def test_duplicate_sequence_fails(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][1]["sequence"] = 1
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate sequence" in e for e in errors))

    def test_ready_evidence_post_requires_insight(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][0]["primary_insight_ids"] = []
        errors = v.validate(self.write(data))
        self.assertTrue(any("missing insight traceability" in e for e in errors))

    def test_unknown_insight_id_fails(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][0]["primary_insight_ids"] = ["INS-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("not listed in plan-level insight_ids" in e for e in errors))

    def test_unknown_claim_id_fails(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][0]["primary_claim_ids"] = ["CLM-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("not listed in plan-level claim_ids" in e for e in errors))

    def test_unknown_source_id_fails(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][0]["source_ids"] = ["SRC-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("not listed in plan-level source_ids" in e for e in errors))

    def test_ready_cannot_require_author_input(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][0]["author_input_required"] = True
        data["linkedin_series_plan"]["posts"][0]["author_input_needed"] = ["Example"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("ready post cannot" in e for e in errors))

    def test_needs_input_requires_details(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][2]["author_input_needed"] = []
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires non-empty author_input_needed" in e for e in errors))

    def test_prerequisite_must_exist(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][1]["prerequisite_post_ids"] = ["POST-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("does not exist" in e for e in errors))

    def test_prerequisite_must_be_earlier(self):
        data = base_plan()
        data["linkedin_series_plan"]["posts"][0]["prerequisite_post_ids"] = ["POST-002"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("must occur earlier" in e for e in errors))

    def test_substantial_overlap_between_ready_posts_fails(self):
        data = base_plan()
        data["linkedin_series_plan"]["overlap_review"][0]["overlap_level"] = "substantial_overlap"
        data["linkedin_series_plan"]["overlap_review"][0]["action"] = "revise"
        data["linkedin_series_plan"]["series_checks"]["substantial_overlap_remaining"] = True
        data["linkedin_series_plan"]["handoff"]["ready_for_drafting"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("two ready posts" in e for e in errors))

    def test_series_check_traceability_must_match(self):
        data = base_plan()
        data["linkedin_series_plan"]["series_checks"]["evidence_traceability_complete"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("evidence_traceability_complete" in e for e in errors))

    def test_handoff_readiness_must_match(self):
        data = base_plan()
        data["linkedin_series_plan"]["handoff"]["ready_for_drafting"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("ready_for_drafting" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
