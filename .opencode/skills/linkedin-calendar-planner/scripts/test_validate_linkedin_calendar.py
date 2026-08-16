from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_linkedin_calendar as v


def base_calendar():
    return {
        "linkedin_calendar": {
            "calendar_id": "LICAL-001",
            "timezone": "Europe/Helsinki",
            "timezone_required": False,
            "cadence": {
                "source": "user",
                "description": "Monday and Thursday",
            },
            "date_range": {
                "start": "2026-09-01",
                "end": "2026-09-30",
            },
            "constraints": {
                "fixed_dates": [],
                "blackout_dates": [],
                "allowed_days": ["Monday", "Thursday"],
                "minimum_spacing_days": None,
                "maximum_posts_per_day": 1,
            },
            "entries": [
                {
                    "calendar_entry_id": "CAL-001",
                    "post_id": "POST-001",
                    "approval_status": "qa_approved",
                    "calendar_status": "scheduled",
                    "slot_lock": "flexible",
                    "date": "2026-09-07",
                    "time_mode": "TBD",
                    "time": None,
                    "time_window": None,
                    "pillar_ids": [],
                    "reader_job": "evidence",
                    "format": "text",
                    "prerequisite_post_ids": [],
                    "time_sensitivity": "evergreen",
                    "not_before": None,
                    "not_after": None,
                    "time_sensitivity_reason": None,
                    "experiment_id": None,
                    "scheduling_rationale": "User cadence.",
                    "conflicts": [],
                }
            ],
            "experiments": [],
            "collision_review": [],
            "calendar_checks": {
                "only_approved_posts_scheduled": True,
                "dependencies_respected": True,
                "hard_collisions_remaining": False,
                "unresolved_decisions_remaining": False,
                "explicit_user_dates_preserved": True,
                "blackout_dates_respected": True,
                "time_sensitive_windows_respected": True,
                "exact_time_requirements_respected": True,
                "unsupported_platform_timing_claims_used": False,
            },
            "handoff": {
                "ready_to_schedule": True,
                "lifecycle_transition": "qa_approved -> scheduled",
                "notes": [],
            },
        }
    }


class CalendarValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "calendar.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_calendar_passes(self):
        self.assertEqual(v.validate(self.write(base_calendar())), [])

    def test_unapproved_scheduled_fails(self):
        data = base_calendar()
        data["linkedin_calendar"]["entries"][0]["approval_status"] = "drafted"
        errors = v.validate(self.write(data))
        self.assertTrue(any("qa_approved" in e for e in errors))

    def test_scheduled_requires_date(self):
        data = base_calendar()
        data["linkedin_calendar"]["entries"][0]["date"] = None
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires a YYYY-MM-DD date" in e for e in errors))

    def test_exact_scheduled_requires_timezone(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["timezone"] = None
        cal["timezone_required"] = True
        e = cal["entries"][0]
        e["time_mode"] = "exact"
        e["time"] = "09:00"
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires known timezone" in e for e in errors))

    def test_window_cannot_invent_exact_time(self):
        data = base_calendar()
        e = data["linkedin_calendar"]["entries"][0]
        e["time_mode"] = "window"
        e["time_window"] = "morning"
        e["time"] = "09:00"
        errors = v.validate(self.write(data))
        self.assertTrue(any("must not set exact `time`" in e for e in errors))

    def test_blackout_date_fails(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["constraints"]["blackout_dates"] = ["2026-09-07"]
        cal["calendar_checks"]["blackout_dates_respected"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("blackout date" in e for e in errors))

    def test_dependency_blocked_still_respected(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["entries"].append({
            "calendar_entry_id": "CAL-002",
            "post_id": "POST-002",
            "approval_status": "qa_approved",
            "calendar_status": "blocked_by_dependency",
            "slot_lock": "flexible",
            "date": None,
            "time_mode": "TBD",
            "time": None,
            "time_window": None,
            "pillar_ids": [],
            "reader_job": "synthesis",
            "format": "text",
            "prerequisite_post_ids": ["POST-001"],
            "time_sensitivity": "evergreen",
            "not_before": None,
            "not_after": None,
            "time_sensitivity_reason": None,
            "experiment_id": None,
            "scheduling_rationale": "Withheld until prerequisite condition is met.",
            "conflicts": [],
        })
        cal["handoff"]["ready_to_schedule"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_scheduled_dependent_requires_scheduled_prerequisite(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["entries"][0]["calendar_status"] = "provisional"
        cal["entries"].append({
            "calendar_entry_id": "CAL-002",
            "post_id": "POST-002",
            "approval_status": "qa_approved",
            "calendar_status": "scheduled",
            "slot_lock": "flexible",
            "date": "2026-09-10",
            "time_mode": "TBD",
            "time": None,
            "time_window": None,
            "pillar_ids": [],
            "reader_job": "synthesis",
            "format": "text",
            "prerequisite_post_ids": ["POST-001"],
            "time_sensitivity": "evergreen",
            "not_before": None,
            "not_after": None,
            "time_sensitivity_reason": None,
            "experiment_id": None,
            "scheduling_rationale": "Invalid dependency test.",
            "conflicts": [],
        })
        cal["calendar_checks"]["dependencies_respected"] = False
        cal["handoff"]["ready_to_schedule"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("prerequisite POST-001 is not scheduled" in e for e in errors))

    def test_missing_timezone_needs_decision_not_hard_collision(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["timezone"] = None
        cal["timezone_required"] = True
        e = cal["entries"][0]
        e["calendar_status"] = "needs_decision"
        e["date"] = "2026-09-10"
        e["time_mode"] = "TBD"
        e["time"] = None
        cal["calendar_checks"]["unresolved_decisions_remaining"] = True
        cal["handoff"]["ready_to_schedule"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_needs_decision_sets_unresolved_decisions(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["entries"][0]["calendar_status"] = "needs_decision"
        cal["calendar_checks"]["unresolved_decisions_remaining"] = False
        cal["handoff"]["ready_to_schedule"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("unresolved_decisions_remaining" in e for e in errors))

    def test_true_hard_collision_sets_hard_remaining(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["entries"][0]["calendar_status"] = "needs_decision"
        cal["entries"].append({
            **cal["entries"][0],
            "calendar_entry_id": "CAL-002",
            "post_id": "POST-002",
        })
        cal["collision_review"] = [{
            "collision_id": "COL-001",
            "entry_ids": ["CAL-001", "CAL-002"],
            "collision_level": "hard",
            "collision_type": "locked_same_day_capacity",
            "explanation": "Two locked posts require one slot.",
            "action": "needs_decision",
        }]
        cal["calendar_checks"]["hard_collisions_remaining"] = True
        cal["calendar_checks"]["unresolved_decisions_remaining"] = True
        cal["handoff"]["ready_to_schedule"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_ready_true_with_hard_collision_fails(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["collision_review"] = [{
            "collision_id": "COL-001",
            "entry_ids": ["CAL-001"],
            "collision_level": "hard",
            "collision_type": "synthetic",
            "explanation": "Unresolved hard collision.",
            "action": "needs_decision",
        }]
        cal["calendar_checks"]["hard_collisions_remaining"] = True
        cal["calendar_checks"]["unresolved_decisions_remaining"] = True
        errors = v.validate(self.write(data))
        self.assertTrue(any("ready_to_schedule: true" in e for e in errors))

    def test_safe_calendar_may_conservatively_be_not_ready(self):
        data = base_calendar()
        data["linkedin_calendar"]["handoff"]["ready_to_schedule"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_max_posts_per_day_capacity_fails(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["entries"].append({
            **cal["entries"][0],
            "calendar_entry_id": "CAL-002",
            "post_id": "POST-002",
        })
        cal["calendar_checks"]["hard_collisions_remaining"] = True
        cal["handoff"]["ready_to_schedule"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("exceed maximum_posts_per_day" in e for e in errors))

    def test_time_sensitive_window_violation_fails(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        e = cal["entries"][0]
        e["time_sensitivity"] = "time_sensitive"
        e["not_before"] = "2026-09-08"
        e["not_after"] = "2026-09-10"
        cal["calendar_checks"]["time_sensitive_windows_respected"] = False
        cal["handoff"]["ready_to_schedule"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("scheduled before not_before" in e for e in errors))

    def test_experiment_reference_must_exist(self):
        data = base_calendar()
        data["linkedin_calendar"]["entries"][0]["experiment_id"] = "EXP-999"
        errors = v.validate(self.write(data))
        self.assertTrue(any("not defined in experiments" in e for e in errors))

    def test_valid_experiment_passes(self):
        data = base_calendar()
        cal = data["linkedin_calendar"]
        cal["experiments"] = [{
            "experiment_id": "EXP-001",
            "hypothesis": "Opening approach may differ in save rate.",
            "variable": "opening approach",
            "variants": ["evidence-led", "application-led"],
            "success_metric": "save rate",
            "interpretation_guard": "Observational comparison; do not infer causality.",
        }]
        cal["entries"][0]["experiment_id"] = "EXP-001"
        self.assertEqual(v.validate(self.write(data)), [])

    def test_calendar_check_mismatch_fails(self):
        data = base_calendar()
        data["linkedin_calendar"]["calendar_checks"]["dependencies_respected"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("dependencies_respected" in e for e in errors))

    def test_ready_handoff_transition_must_match(self):
        data = base_calendar()
        data["linkedin_calendar"]["handoff"]["lifecycle_transition"] = "drafted -> scheduled"
        errors = v.validate(self.write(data))
        self.assertTrue(any("qa_approved -> scheduled" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
