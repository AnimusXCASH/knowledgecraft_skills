from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_content_quality_gate as v


def base_gate():
    return {
        "content_quality_gate": {
            "content_id": "CQ-TEST",
            "destination": "LinkedIn",
            "audience": "youth-sport coaches",
            "upstream_checks": {
                "factuality": {
                    "required": True,
                    "status": "PASS",
                }
            },
            "blockers": [],
            "scores": {
                "clarity_coherence": {"score": 3, "reason": "Clear."},
                "specificity_concreteness": {"score": 2, "reason": "Specific enough."},
                "usefulness_reader_value": {"score": 3, "reason": "Useful."},
                "audience_fit": {"score": 3, "reason": "Audience fit is strong."},
                "voice_naturalness": {"score": 3, "reason": "Natural."},
                "destination_format_fit": {"score": 3, "reason": "Fits destination."},
                "distinctiveness_nonredundancy": {"score": 3, "reason": "Distinct."},
            },
            "total_score": 20,
            "decision": "APPROVE",
            "required_revisions": [],
            "strengths": ["Central point is clear."],
        }
    }


class ContentQualityGateValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "quality.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_approve_passes(self):
        path = self.write(base_gate())
        self.assertEqual(v.validate(path), [])

    def test_wrong_total_fails(self):
        data = base_gate()
        data["content_quality_gate"]["total_score"] = 19
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("total_score" in e and "expected 20" in e for e in errors))

    def test_low_score_cannot_approve(self):
        data = base_gate()
        data["content_quality_gate"]["scores"]["specificity_concreteness"]["score"] = 1
        data["content_quality_gate"]["total_score"] = 19
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("expected REVISE" in e for e in errors))

    def test_total_below_17_cannot_approve(self):
        data = base_gate()
        for key in data["content_quality_gate"]["scores"]:
            data["content_quality_gate"]["scores"][key]["score"] = 2
        data["content_quality_gate"]["total_score"] = 14
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("expected REVISE" in e for e in errors))

    def test_revise_requires_revision(self):
        data = base_gate()
        data["content_quality_gate"]["scores"]["specificity_concreteness"]["score"] = 1
        data["content_quality_gate"]["total_score"] = 19
        data["content_quality_gate"]["decision"] = "REVISE"
        data["content_quality_gate"]["required_revisions"] = []
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("REVISE requires" in e for e in errors))

    def test_blocker_forces_block(self):
        data = base_gate()
        data["content_quality_gate"]["blockers"] = ["Misleading headline."]
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("expected BLOCK" in e for e in errors))

    def test_factuality_block_forces_block_and_requires_blocker(self):
        data = base_gate()
        fact = data["content_quality_gate"]["upstream_checks"]["factuality"]
        fact["status"] = "BLOCK"
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("expected BLOCK" in e for e in errors))
        self.assertTrue(any("must be represented in `blockers`" in e for e in errors))

    def test_factuality_not_run_when_required_forces_block(self):
        data = base_gate()
        fact = data["content_quality_gate"]["upstream_checks"]["factuality"]
        fact["status"] = "NOT_RUN"
        data["content_quality_gate"]["decision"] = "BLOCK"
        data["content_quality_gate"]["blockers"] = ["factuality_review_required"]
        path = self.write(data)
        self.assertEqual(v.validate(path), [])

    def test_approve_cannot_have_required_revisions(self):
        data = base_gate()
        data["content_quality_gate"]["required_revisions"] = [
            {
                "location": "opening",
                "issue": "weak opening",
                "smallest_change": "Make the opening more direct.",
            }
        ]
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("APPROVE requires" in e for e in errors))

    def test_block_requires_blocker(self):
        data = base_gate()
        data["content_quality_gate"]["decision"] = "BLOCK"
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("BLOCK requires" in e for e in errors))

    def test_score_out_of_range_fails(self):
        data = base_gate()
        data["content_quality_gate"]["scores"]["clarity_coherence"]["score"] = 4
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("0 to 3" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
