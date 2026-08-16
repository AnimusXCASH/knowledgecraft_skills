from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

import research_library as rl


class ResearchLibraryRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.registry_path = self.root / ".knowledgecraft" / "research" / "registry.json"

    def tearDown(self):
        self.tmp.cleanup()

    def scan(self, *roots: Path):
        args = argparse.Namespace(
            registry=str(self.registry_path),
            roots=[str(p) for p in roots],
            extensions=".txt,.md",
        )
        rl.scan(args)
        return rl.load(self.registry_path)

    def test_repeated_scan_same_file_is_idempotent(self):
        papers = self.root / "papers"
        papers.mkdir()
        file = papers / "paper.txt"
        file.write_text("alpha", encoding="utf-8")

        first = self.scan(papers)
        second = self.scan(papers)

        self.assertEqual(len(first["sources"]), 1)
        self.assertEqual(len(second["sources"]), 1)
        source = next(iter(second["sources"].values()))
        self.assertEqual(source["paths"], [str(file.resolve())])

    def test_same_content_different_filename_is_same_source(self):
        papers = self.root / "papers"
        papers.mkdir()
        a = papers / "a.txt"
        b = papers / "renamed.txt"
        a.write_text("same content", encoding="utf-8")
        b.write_text("same content", encoding="utf-8")

        reg = self.scan(papers)

        self.assertEqual(len(reg["sources"]), 1)
        source = next(iter(reg["sources"].values()))
        self.assertEqual(
            set(source["paths"]),
            {str(a.resolve()), str(b.resolve())},
        )

    def test_same_content_different_folder_is_same_source(self):
        a_dir = self.root / "a"
        b_dir = self.root / "b"
        a_dir.mkdir()
        b_dir.mkdir()
        a = a_dir / "paper.txt"
        b = b_dir / "copy.txt"
        a.write_text("same content", encoding="utf-8")
        b.write_text("same content", encoding="utf-8")

        reg = self.scan(a_dir, b_dir)

        self.assertEqual(len(reg["sources"]), 1)

    def test_changed_content_same_path_creates_revision_lineage(self):
        papers = self.root / "papers"
        papers.mkdir()
        file = papers / "paper.txt"
        file.write_text("version one", encoding="utf-8")

        first = self.scan(papers)
        first_id = next(iter(first["sources"]))

        file.write_text("version two", encoding="utf-8")
        second = self.scan(papers)

        self.assertEqual(len(second["sources"]), 2)

        new_ids = set(second["sources"]) - {first_id}
        self.assertEqual(len(new_ids), 1)
        second_id = next(iter(new_ids))

        new_source = second["sources"][second_id]
        old_source = second["sources"][first_id]

        self.assertEqual(new_source["revision_of"], first_id)
        self.assertEqual(new_source["revision_number"], 2)
        self.assertIn(second_id, old_source["revised_by"])
        self.assertIn(str(file.resolve()), old_source["stale_paths"])

    def test_collision_safe_source_id_extends_prefix(self):
        digest = "a" * 64
        other_digest = ("a" * 12) + ("b" * 52)
        reg = {
            "version": 2,
            "sources": {
                "SRC-" + ("a" * 12): {
                    "source_id": "SRC-" + ("a" * 12),
                    "sha256": other_digest,
                }
            },
        }

        source_id = rl.allocate_source_id(reg, digest)

        self.assertEqual(source_id, "SRC-" + ("a" * 13))

    def test_deleted_primary_path_falls_back_to_valid_duplicate(self):
        a_dir = self.root / "a"
        b_dir = self.root / "b"
        a_dir.mkdir()
        b_dir.mkdir()
        a = a_dir / "paper.txt"
        b = b_dir / "copy.txt"
        a.write_text("same content", encoding="utf-8")
        b.write_text("same content", encoding="utf-8")

        reg = self.scan(a_dir, b_dir)
        source_id = next(iter(reg["sources"]))
        source = reg["sources"][source_id]

        # Force the soon-to-be-missing path to be primary.
        source["primary_path"] = str(a.resolve())
        rl.save(self.registry_path, reg)

        a.unlink()

        reg = rl.load(self.registry_path)
        source = reg["sources"][source_id]
        selected = rl.resolve_source_path(source)

        self.assertEqual(selected, b.resolve())
        self.assertEqual(source["primary_path"], str(b.resolve()))
        self.assertIn(str(a.resolve()), source["missing_paths"])

    def test_reextract_processed_source_preserves_later_status(self):
        papers = self.root / "papers"
        papers.mkdir()
        file = papers / "paper.txt"
        file.write_text("alpha", encoding="utf-8")

        reg = self.scan(papers)
        source_id = next(iter(reg["sources"]))
        reg["sources"][source_id]["status"] = "grounded"
        rl.save(self.registry_path, reg)

        args = argparse.Namespace(
            registry=str(self.registry_path),
            pending=False,
            source_id=source_id,
            out=str(self.root / ".knowledgecraft" / "research" / "extracted"),
        )
        rl.extract(args)

        updated = rl.load(self.registry_path)
        source = updated["sources"][source_id]
        self.assertEqual(source["status"], "grounded")
        self.assertTrue(Path(source["extracted_path"]).exists())
        self.assertEqual(source["history"][-1]["event"], "extraction_refreshed")
        self.assertEqual(source["history"][-1]["status_preserved"], "grounded")

    def test_ignored_source_cannot_be_extracted_implicitly(self):
        papers = self.root / "papers"
        papers.mkdir()
        file = papers / "paper.txt"
        file.write_text("alpha", encoding="utf-8")

        reg = self.scan(papers)
        source_id = next(iter(reg["sources"]))
        reg["sources"][source_id]["status"] = "ignored"
        rl.save(self.registry_path, reg)

        args = argparse.Namespace(
            registry=str(self.registry_path),
            pending=False,
            source_id=source_id,
            out=str(self.root / ".knowledgecraft" / "research" / "extracted"),
        )
        rl.extract(args)

        updated = rl.load(self.registry_path)
        source = updated["sources"][source_id]
        self.assertEqual(source["status"], "failed")
        self.assertIn("Cannot extract source", source["error"])

    def test_invalid_lifecycle_jump_is_rejected(self):
        record = {"status": "new", "history": []}

        with self.assertRaises(ValueError):
            rl.set_status(record, "published")

        self.assertEqual(record["status"], "new")

    def test_valid_lifecycle_progression_records_from_and_to(self):
        record = {"status": "new", "history": []}

        changed = rl.set_status(record, "extracted")
        self.assertTrue(changed)
        self.assertEqual(record["status"], "extracted")

        event = record["history"][-1]
        self.assertEqual(event["from"], "new")
        self.assertEqual(event["to"], "extracted")
        self.assertFalse(event["forced"])

        rl.set_status(record, "grounded")
        self.assertEqual(record["status"], "grounded")

    def test_force_allows_explicit_status_override(self):
        record = {"status": "new", "history": []}

        rl.set_status(record, "published", force=True)

        self.assertEqual(record["status"], "published")
        self.assertTrue(record["history"][-1]["forced"])

    def test_multiple_artifacts_per_stage(self):
        a = self.root / "source-card.md"
        b = self.root / "claim-ledger.yaml"
        a.write_text("card", encoding="utf-8")
        b.write_text("ledger", encoding="utf-8")

        record = {"artifacts": {}, "history": []}

        rl.add_artifacts(record, "grounded", [a, b])
        rl.add_artifacts(record, "grounded", [a])

        self.assertEqual(
            record["artifacts"]["grounded"],
            sorted([str(a.resolve()), str(b.resolve())]),
        )

    def test_v1_registry_artifact_string_migrates_to_list(self):
        old = {
            "version": 1,
            "updated_at": rl.now(),
            "sources": {
                "SRC-test": {
                    "source_id": "SRC-test",
                    "sha256": "f" * 64,
                    "primary_path": str(self.root / "paper.txt"),
                    "paths": [str(self.root / "paper.txt")],
                    "status": "grounded",
                    "artifacts": {
                        "grounded": str(self.root / "source-card.md")
                    },
                    "history": [],
                }
            },
        }

        migrated = rl.migrate_registry(old)

        self.assertEqual(migrated["version"], 2)
        self.assertEqual(
            migrated["sources"]["SRC-test"]["artifacts"]["grounded"],
            [str(self.root / "source-card.md")],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
