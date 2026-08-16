from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_author_voice_profile as v


def make_sample(i, authorship="confirmed", eligible=True):
    return {
        "sample_id": f"VOICE-S{i:03d}",
        "label": None,
        "genre": "LinkedIn",
        "approximate_length": "substantial",
        "authorship": authorship,
        "eligible_for_inference": eligible,
        "notes": None,
    }


def base_profile():
    samples = [make_sample(i) for i in range(1, 9)]
    return {
        "author_voice_profile": {
            "profile_id": "VOICE-P001",
            "profile_confidence": "strong",
            "sample_count": {
                "total": 8,
                "eligible": 8,
                "uncertain": 0,
            },
            "coverage": {
                "genres": ["LinkedIn"],
                "notes": [],
            },
            "samples": samples,
            "stable_traits": [
                {
                    "trait": "direct openings",
                    "pattern": "Often opens directly with the topic.",
                    "confidence": "high",
                    "supporting_sample_ids": ["VOICE-S001", "VOICE-S002"],
                    "counterexample_sample_ids": [],
                    "context_scope": "cross-context",
                    "evidence_note": "Repeated across samples.",
                }
            ],
            "context_profiles": [
                {
                    "context": "LinkedIn",
                    "confidence": "high",
                    "traits": [
                        {
                            "trait": "short paragraphs",
                            "pattern": "Uses short visually separated paragraphs.",
                            "confidence": "high",
                            "supporting_sample_ids": ["VOICE-S003", "VOICE-S004"],
                            "counterexample_sample_ids": [],
                            "evidence_note": "Repeated in LinkedIn samples.",
                        }
                    ],
                }
            ],
            "recurring_language": [
                {
                    "expression_or_pattern": "observation to practical question",
                    "stability": "recurring",
                    "supporting_sample_ids": ["VOICE-S001", "VOICE-S003"],
                    "usage_note": "Preserve function, not exact phrase.",
                }
            ],
            "not_observed_or_uncertain": [
                {
                    "feature": "emoji",
                    "status": "not_observed",
                    "note": "Not observed in supplied eligible samples.",
                }
            ],
            "downstream_guidance": {
                "preserve": ["Direct openings."],
                "use_selectively": ["Questions."],
                "avoid_overfitting": ["Exact recurring phrases."],
            },
            "limitations": ["Only LinkedIn represented."],
        }
    }


class AuthorVoiceValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "profile.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_profile_passes(self):
        path = self.write(base_profile())
        self.assertEqual(v.validate(path), [])

    def test_sample_count_total_mismatch_fails(self):
        data = base_profile()
        data["author_voice_profile"]["sample_count"]["total"] = 9
        errors = v.validate(self.write(data))
        self.assertTrue(any("sample_count.total" in e for e in errors))

    def test_eligible_count_mismatch_fails(self):
        data = base_profile()
        data["author_voice_profile"]["samples"][0]["eligible_for_inference"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("sample_count.eligible" in e for e in errors))

    def test_uncertain_count_mismatch_fails(self):
        data = base_profile()
        data["author_voice_profile"]["samples"][0]["authorship"] = "uncertain"
        errors = v.validate(self.write(data))
        self.assertTrue(any("sample_count.uncertain" in e for e in errors))

    def test_profile_confidence_band_fails(self):
        data = base_profile()
        data["author_voice_profile"]["profile_confidence"] = "moderate"
        errors = v.validate(self.write(data))
        self.assertTrue(any("expected 'strong'" in e for e in errors))

    def test_duplicate_sample_id_fails(self):
        data = base_profile()
        data["author_voice_profile"]["samples"][1]["sample_id"] = "VOICE-S001"
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate sample ID" in e for e in errors))

    def test_unknown_trait_sample_id_fails(self):
        data = base_profile()
        trait = data["author_voice_profile"]["stable_traits"][0]
        trait["supporting_sample_ids"] = ["VOICE-S999", "VOICE-S002"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("unknown sample ID" in e for e in errors))

    def test_high_confidence_requires_two_supporting_samples(self):
        data = base_profile()
        trait = data["author_voice_profile"]["stable_traits"][0]
        trait["supporting_sample_ids"] = ["VOICE-S001"]
        errors = v.validate(self.write(data))
        self.assertTrue(any("fewer than two" in e for e in errors))

    def test_high_confidence_cannot_use_uncertain_authorship(self):
        data = base_profile()
        data["author_voice_profile"]["samples"][0]["authorship"] = "uncertain"
        data["author_voice_profile"]["sample_count"]["uncertain"] = 1
        errors = v.validate(self.write(data))
        self.assertTrue(any("uncertain authorship sample" in e for e in errors))

    def test_high_confidence_cannot_use_ineligible_sample(self):
        data = base_profile()
        data["author_voice_profile"]["samples"][0]["eligible_for_inference"] = False
        data["author_voice_profile"]["sample_count"]["eligible"] = 7
        data["author_voice_profile"]["profile_confidence"] = "moderate"
        errors = v.validate(self.write(data))
        self.assertTrue(any("ineligible sample" in e for e in errors))

    def test_bad_recurring_stability_fails(self):
        data = base_profile()
        data["author_voice_profile"]["recurring_language"][0]["stability"] = "always"
        errors = v.validate(self.write(data))
        self.assertTrue(any("recurring_language" in e and "stability" in e for e in errors))

    def test_bad_uncertain_status_fails(self):
        data = base_profile()
        data["author_voice_profile"]["not_observed_or_uncertain"][0]["status"] = "never"
        errors = v.validate(self.write(data))
        self.assertTrue(any("not_observed_or_uncertain" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
