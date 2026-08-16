from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_batch_report as v


def base_report():
    return {
        "batch_report": {
            "target_stage": "ideas_created",
            "sources": [
                {
                    "source_id": "SRC-A",
                    "start": "new",
                    "end": "ideas_created",
                    "disposition": "processed",
                    "actions": ["extract", "ground", "insights"],
                    "error": None,
                },
                {
                    "source_id": "SRC-B",
                    "start": "extracted",
                    "end": "ideas_created",
                    "disposition": "processed",
                    "actions": ["ground", "insights"],
                    "error": None,
                },
                {
                    "source_id": "SRC-C",
                    "start": "grounded",
                    "end": "ideas_created",
                    "disposition": "processed",
                    "actions": ["insights"],
                    "error": None,
                },
                {
                    "source_id": "SRC-D",
                    "start": "ideas_created",
                    "end": "ideas_created",
                    "disposition": "already_complete",
                    "actions": [],
                    "error": None,
                },
                {
                    "source_id": "SRC-E",
                    "start": "ignored",
                    "end": "ignored",
                    "disposition": "ignored",
                    "actions": [],
                    "error": None,
                },
            ],
            "summary": {
                "sources_inspected": 5,
                "sources_processed": 3,
                "sources_already_complete": 1,
                "sources_ignored": 1,
                "sources_failed": 0,
            },
            "forced_transitions_used": 0,
            "duplicate_source_records": 0,
            "second_run_idempotence": "PASS",
            "batch_result": "PASS",
        }
    }


class BatchReportValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "report.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_good_mixed_state_report_passes(self):
        path = self.write(base_report())
        self.assertEqual(v.validate(path), [])

    def test_ignored_source_cannot_be_counted_as_processed(self):
        data = base_report()
        data["batch_report"]["summary"]["sources_processed"] = 4
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(
            any("sources_processed" in e and "expected 3" in e for e in errors)
        )

    def test_ignored_source_cannot_have_actions(self):
        data = base_report()
        data["batch_report"]["sources"][4]["actions"] = ["extract"]
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("ignored" in e and "actions" in e for e in errors))

    def test_already_complete_cannot_have_actions(self):
        data = base_report()
        data["batch_report"]["sources"][3]["actions"] = ["insights"]
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("already_complete" in e for e in errors))

    def test_failed_source_requires_error_and_forces_fail_result(self):
        data = base_report()
        src = data["batch_report"]["sources"][0]
        src["disposition"] = "failed"
        src["end"] = "failed"
        src["error"] = "Extraction failed"
        data["batch_report"]["summary"]["sources_processed"] = 2
        data["batch_report"]["summary"]["sources_failed"] = 1
        data["batch_report"]["batch_result"] = "PASS"
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("batch_result" in e and "FAIL" in e for e in errors))

    def test_duplicate_source_ids_fail(self):
        data = base_report()
        data["batch_report"]["sources"][1]["source_id"] = "SRC-A"
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("duplicate source_id" in e for e in errors))

    def test_forced_transition_makes_result_fail(self):
        data = base_report()
        data["batch_report"]["forced_transitions_used"] = 1
        path = self.write(data)
        errors = v.validate(path)
        self.assertTrue(any("batch_result" in e and "FAIL" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
