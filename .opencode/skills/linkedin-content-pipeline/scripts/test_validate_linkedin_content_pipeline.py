from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_linkedin_content_pipeline as v


def base_report():
    return {
        "linkedin_content_pipeline": {
            "run_id": "LCPIP-001",
            "requested_goal": "Get POST-001 ready to publish.",
            "mode": "qa_only",
            "inspected_state": {
                "source_ids": ["SRC-001"],
                "series_plan": None,
                "post_ids": ["POST-001"],
                "current_lifecycle_states": {"POST-001": "drafted"},
                "stale_artifacts": [],
            },
            "routing": [
                {
                    "step": 1,
                    "item_id": "POST-001",
                    "from_state": "drafted",
                    "required_skill": "linkedin-platform-review",
                    "reason": "LinkedIn presentation review required.",
                    "status": "completed",
                    "artifact": ".knowledgecraft/content/drafts/POST-001-platform-review.yaml",
                    "validator_required": True,
                    "validator_status": "pass",
                },
                {
                    "step": 2,
                    "item_id": "POST-001",
                    "from_state": "drafted",
                    "required_skill": "factuality-guard",
                    "reason": "Final factuality review required.",
                    "status": "completed",
                    "artifact": ".knowledgecraft/content/drafts/POST-001-factuality.yaml",
                    "validator_required": False,
                    "validator_status": "not_required",
                },
                {
                    "step": 3,
                    "item_id": "POST-001",
                    "from_state": "drafted",
                    "required_skill": "content-quality-gate",
                    "reason": "Final quality approval required.",
                    "status": "completed",
                    "artifact": ".knowledgecraft/content/drafts/POST-001-quality.yaml",
                    "validator_required": True,
                    "validator_status": "pass",
                },
            ],
            "item_states": [
                {
                    "item_id": "POST-001",
                    "item_type": "post",
                    "lifecycle_before": "drafted",
                    "lifecycle_after": "qa_approved",
                    "current_status": "approved",
                    "blockers": [],
                    "next_required_skill": None,
                    "artifact_refs": [
                        ".knowledgecraft/content/drafts/POST-001-platform-review.yaml"
                    ],
                }
            ],
            "qa": [
                {
                    "post_id": "POST-001",
                    "factuality_status": "pass",
                    "quality_status": "APPROVE",
                    "qa_approved": True,
                }
            ],
            "calendar": {
                "requested": False,
                "artifact": None,
                "ready_to_schedule": None,
            },
            "publication": {
                "authorized_workflow_present": False,
                "published_confirmed": False,
            },
            "performance_loop": {
                "requested": False,
                "reusable_learning_ids": [],
            },
            "summary": {
                "completed_steps": 3,
                "skipped_steps": 0,
                "blocked_items": 0,
                "failed_items": 0,
                "needs_input_items": 0,
            },
            "handoff": {
                "workflow_complete_for_requested_goal": True,
                "next_action": "Human may review/publish or request scheduling.",
                "notes": [],
            },
        }
    }


class PipelineValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "pipeline.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_report_passes(self):
        self.assertEqual(v.validate(self.write(base_report())), [])

    def test_invalid_mode_fails(self):
        data = base_report()
        data["linkedin_content_pipeline"]["mode"] = "everything"
        errors = v.validate(self.write(data))
        self.assertTrue(any("`mode`" in e for e in errors))

    def test_duplicate_routing_step_fails(self):
        data = base_report()
        data["linkedin_content_pipeline"]["routing"][1]["step"] = 1
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate routing step" in e for e in errors))

    def test_completed_required_validator_must_pass(self):
        data = base_report()
        data["linkedin_content_pipeline"]["routing"][0]["validator_status"] = "fail"
        errors = v.validate(self.write(data))
        self.assertTrue(any("cannot be completed" in e for e in errors))

    def test_required_validator_not_run_blocks_completion(self):
        data = base_report()
        data["linkedin_content_pipeline"]["routing"][0]["validator_status"] = "not_run"
        errors = v.validate(self.write(data))
        self.assertTrue(any("until its required validator passes" in e for e in errors))

    def test_unrequired_validator_cannot_claim_pass(self):
        data = base_report()
        data["linkedin_content_pipeline"]["routing"][1]["validator_status"] = "pass"
        errors = v.validate(self.write(data))
        self.assertTrue(any("does not require validation" in e for e in errors))

    def test_invalid_lifecycle_fails(self):
        data = base_report()
        data["linkedin_content_pipeline"]["item_states"][0]["lifecycle_after"] = "almost_done"
        errors = v.validate(self.write(data))
        self.assertTrue(any("lifecycle_after" in e for e in errors))

    def test_qa_approved_requires_both_gates(self):
        data = base_report()
        qa = data["linkedin_content_pipeline"]["qa"][0]
        qa["factuality_status"] = "block"
        errors = v.validate(self.write(data))
        self.assertTrue(any("qa_approved true requires" in e for e in errors))

    def test_lifecycle_qa_approved_requires_matching_record(self):
        data = base_report()
        data["linkedin_content_pipeline"]["qa"][0]["qa_approved"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("matching QA approval record" in e for e in errors))

    def test_publication_confirmation_requires_published_item(self):
        data = base_report()
        data["linkedin_content_pipeline"]["publication"]["published_confirmed"] = True
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires at least one post item" in e for e in errors))

    def test_confirmed_published_item_passes(self):
        data = base_report()
        pipe = data["linkedin_content_pipeline"]
        pipe["item_states"][0]["lifecycle_after"] = "published"
        pipe["publication"]["published_confirmed"] = True
        self.assertEqual(v.validate(self.write(data)), [])

    def test_summary_completed_steps_checked(self):
        data = base_report()
        data["linkedin_content_pipeline"]["summary"]["completed_steps"] = 2
        errors = v.validate(self.write(data))
        self.assertTrue(any("summary.completed_steps" in e for e in errors))

    def test_summary_failed_steps_checked(self):
        data = base_report()
        pipe = data["linkedin_content_pipeline"]
        pipe["routing"][0]["status"] = "failed"
        pipe["summary"]["completed_steps"] = 2
        pipe["summary"]["failed_items"] = 0
        pipe["handoff"]["workflow_complete_for_requested_goal"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("summary.failed_items" in e for e in errors))

    def test_complete_workflow_cannot_have_failed_step(self):
        data = base_report()
        pipe = data["linkedin_content_pipeline"]
        pipe["routing"][0]["status"] = "failed"
        pipe["summary"]["completed_steps"] = 2
        pipe["summary"]["failed_items"] = 1
        errors = v.validate(self.write(data))
        self.assertTrue(any("cannot be true while routing contains failed" in e for e in errors))

    def test_needs_input_only_cannot_be_complete(self):
        data = base_report()
        pipe = data["linkedin_content_pipeline"]
        pipe["routing"] = [{
            "step": 1,
            "item_id": "POST-001",
            "from_state": "drafted",
            "required_skill": "author-voice-profiler",
            "reason": "Genuine samples required.",
            "status": "needs_input",
            "artifact": None,
            "validator_required": False,
            "validator_status": "not_run",
        }]
        pipe["summary"] = {
            "completed_steps": 0,
            "skipped_steps": 0,
            "blocked_items": 0,
            "failed_items": 0,
            "needs_input_items": 1,
        }
        pipe["item_states"][0]["lifecycle_after"] = "drafted"
        pipe["qa"][0] = {
            "post_id": "POST-001",
            "factuality_status": "not_run",
            "quality_status": "not_run",
            "qa_approved": False,
        }
        errors = v.validate(self.write(data))
        self.assertTrue(any("only blocked/needs_input" in e for e in errors))

    def test_blocked_item_count_uses_unique_items(self):
        data = base_report()
        pipe = data["linkedin_content_pipeline"]
        pipe["routing"][0]["status"] = "blocked"
        pipe["summary"]["completed_steps"] = 2
        pipe["summary"]["blocked_items"] = 1
        pipe["item_states"][0]["blockers"] = ["factuality block"]
        pipe["handoff"]["workflow_complete_for_requested_goal"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_handoff_next_action_required(self):
        data = base_report()
        data["linkedin_content_pipeline"]["handoff"]["next_action"] = ""
        errors = v.validate(self.write(data))
        self.assertTrue(any("next_action" in e for e in errors))

    def test_duplicate_item_state_fails(self):
        data = base_report()
        pipe = data["linkedin_content_pipeline"]
        pipe["item_states"].append(dict(pipe["item_states"][0]))
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate item_state" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
