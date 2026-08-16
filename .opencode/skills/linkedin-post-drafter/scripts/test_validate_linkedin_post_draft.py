from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_linkedin_post_draft as v


def base_draft():
    return {
        "linkedin_post_draft": {
            "draft_id": "DRAFT-001",
            "post_id": "POST-001",
            "draft_status": "ready_for_editing",
            "destination": "LinkedIn",
            "audience": "youth-sport coaches",
            "reader_job": "evidence",
            "evidence_mode": "evidence_grounded",
            "main_point": "A grounded finding.",
            "source_ids": ["SRC-1"],
            "claim_ids_available": ["CLM-1", "CLM-2"],
            "insight_ids_available": ["INS-1"],
            "claim_ids_used": ["CLM-1", "CLM-2"],
            "insight_ids_used": ["INS-1"],
            "author_input_required": False,
            "author_input_needed": [],
            "drafting_constraints": ["Do not claim causality."],
            "draft_text": "A complete but synthetic LinkedIn draft.",
            "omitted_or_deferred": [],
            "preservation_checks": {
                "no_new_claims": True,
                "relationship_language_preserved": True,
                "causal_status_preserved": True,
                "uncertainty_preserved": True,
                "unsupported_mechanism_added": False,
                "personal_experience_invented": False,
                "unsupported_story_invented": False,
                "source_traceability_preserved": True,
            },
            "handoff": {
                "ready_for_author_voice_edit": True,
                "next_skill": "author-voice-editor",
                "notes": [],
            },
        }
    }


class DraftValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "draft.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_ready_draft_passes(self):
        self.assertEqual(v.validate(self.write(base_draft())), [])

    def test_used_claim_must_be_available(self):
        data = base_draft()
        data["linkedin_post_draft"]["claim_ids_used"] = ["CLM-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("not in claim_ids_available" in e for e in errors))

    def test_used_insight_must_be_available(self):
        data = base_draft()
        data["linkedin_post_draft"]["insight_ids_used"] = ["INS-999"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("not in insight_ids_available" in e for e in errors))

    def test_ready_requires_draft_text(self):
        data = base_draft()
        data["linkedin_post_draft"]["draft_text"] = ""
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires non-empty draft_text" in e for e in errors))

    def test_ready_evidence_requires_used_claim(self):
        data = base_draft()
        data["linkedin_post_draft"]["claim_ids_used"] = []
        errors = v.validate(self.write(data))
        self.assertTrue(any("must use at least one allowed claim" in e for e in errors))

    def test_ready_evidence_requires_available_insight(self):
        data = base_draft()
        data["linkedin_post_draft"]["insight_ids_available"] = []
        data["linkedin_post_draft"]["insight_ids_used"] = []
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires insight_ids_available" in e for e in errors))

    def test_ready_cannot_require_author_input(self):
        data = base_draft()
        data["linkedin_post_draft"]["author_input_required"] = True
        data["linkedin_post_draft"]["author_input_needed"] = ["A real story"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("cannot have author_input_required" in e for e in errors))

    def test_needs_input_requires_empty_draft(self):
        data = base_draft()
        d = data["linkedin_post_draft"]
        d["draft_status"] = "needs_input"
        d["author_input_required"] = True
        d["author_input_needed"] = ["A genuine story."]
        d["handoff"]["ready_for_author_voice_edit"] = False
        d["handoff"]["next_skill"] = "author-voice-editor"
        errors = v.validate(self.write(data))
        self.assertTrue(any("must leave draft_text empty" in e for e in errors))

    def test_valid_needs_input_passes(self):
        data = base_draft()
        d = data["linkedin_post_draft"]
        d["draft_status"] = "needs_input"
        d["reader_job"] = "story"
        d["evidence_mode"] = "story"
        d["source_ids"] = []
        d["claim_ids_available"] = []
        d["insight_ids_available"] = []
        d["claim_ids_used"] = []
        d["insight_ids_used"] = []
        d["author_input_required"] = True
        d["author_input_needed"] = ["A genuine coaching story."]
        d["draft_text"] = ""
        d["handoff"]["ready_for_author_voice_edit"] = False
        d["handoff"]["next_skill"] = "author-voice-editor"
        self.assertEqual(v.validate(self.write(data)), [])

    def test_blocked_requires_empty_draft(self):
        data = base_draft()
        d = data["linkedin_post_draft"]
        d["draft_status"] = "blocked"
        d["handoff"]["ready_for_author_voice_edit"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("blocked draft must leave draft_text empty" in e for e in errors))

    def test_valid_blocked_passes(self):
        data = base_draft()
        d = data["linkedin_post_draft"]
        d["draft_status"] = "blocked"
        d["draft_text"] = ""
        d["handoff"]["ready_for_author_voice_edit"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_ready_preservation_checks_must_be_safe(self):
        data = base_draft()
        data["linkedin_post_draft"]["preservation_checks"]["causal_status_preserved"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("causal_status_preserved: true" in e for e in errors))

    def test_handoff_must_match_status(self):
        data = base_draft()
        data["linkedin_post_draft"]["handoff"]["ready_for_author_voice_edit"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("does not match draft state" in e for e in errors))

    def test_ready_handoff_skill_must_match(self):
        data = base_draft()
        data["linkedin_post_draft"]["handoff"]["next_skill"] = "wrong-skill"
        errors = v.validate(self.write(data))
        self.assertTrue(any("author-voice-editor" in e for e in errors))

    def test_duplicate_ids_fail(self):
        data = base_draft()
        data["linkedin_post_draft"]["source_ids"] = ["SRC-1", "SRC-1"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("duplicate ID/value" in e for e in errors))

    def test_omitted_item_requires_reason(self):
        data = base_draft()
        data["linkedin_post_draft"]["omitted_or_deferred"] = [
            {"item": "personal story", "reason": ""}
        ]
        errors = v.validate(self.write(data))
        self.assertTrue(any("reason" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
