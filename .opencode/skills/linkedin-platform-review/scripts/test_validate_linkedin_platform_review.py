from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import validate_linkedin_platform_review as v


def base_review():
    return {
        "linkedin_platform_review": {
            "review_id": "LPR-001",
            "post_id": "POST-001",
            "platform_status": "pass",
            "destination": "LinkedIn",
            "original_text": "A synthetic LinkedIn post.",
            "revised_text": "A synthetic LinkedIn post.",
            "issues": [],
            "platform_checks": {
                "first_screen_clear": True,
                "mobile_readable": True,
                "paragraphing_appropriate": True,
                "lists_content_shaped": True,
                "cta_appropriate": True,
                "engagement_bait_absent": True,
                "hashtags_relevant_or_absent": True,
                "mentions_relevant_or_absent": True,
                "link_treatment_reasonable": True,
                "format_fit_reasonable": True,
            },
            "current_platform_claims": [],
            "preservation_checks": {
                "substantive_meaning_preserved": True,
                "names_dates_numbers_preserved": True,
                "technical_terms_preserved": True,
                "relationship_language_preserved": True,
                "causal_status_preserved": True,
                "uncertainty_preserved": True,
                "limitations_preserved": True,
                "citations_preserved": True,
                "no_new_claims": True,
                "no_personal_experience_invented": True,
            },
            "handoff": {
                "ready_for_factuality_review": True,
                "next_skill": "factuality-guard",
                "notes": [],
            },
        }
    }


class PlatformReviewValidatorTests(unittest.TestCase):
    def write(self, data):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "review.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def test_valid_pass_review(self):
        self.assertEqual(v.validate(self.write(base_review())), [])

    def test_duplicate_issue_id_fails(self):
        data = base_review()
        issue = {
            "issue_id": "LPRI-001",
            "issue_type": "mobile_density",
            "severity": "medium",
            "location": "body",
            "issue_status": "resolved",
            "explanation": "Dense.",
            "change_required": True,
            "suggested_action": "Split paragraph.",
        }
        data["linkedin_platform_review"]["issues"] = [issue, dict(issue)]
        errors = v.validate(self.write(data))
        self.assertTrue(any("Duplicate issue_id" in e for e in errors))

    def test_pass_cannot_have_open_required_issue(self):
        data = base_review()
        data["linkedin_platform_review"]["issues"] = [{
            "issue_id": "LPRI-001",
            "issue_type": "cta_forced",
            "severity": "medium",
            "location": "ending",
            "issue_status": "open",
            "explanation": "CTA is forced.",
            "change_required": True,
            "suggested_action": "Remove CTA.",
        }]
        errors = v.validate(self.write(data))
        self.assertTrue(any("cannot retain open issues" in e for e in errors))

    def test_revise_requires_open_required_issue(self):
        data = base_review()
        data["linkedin_platform_review"]["platform_status"] = "revise"
        data["linkedin_platform_review"]["handoff"]["ready_for_factuality_review"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires at least one open issue" in e for e in errors))

    def test_valid_revise_review(self):
        data = base_review()
        r = data["linkedin_platform_review"]
        r["platform_status"] = "revise"
        r["issues"] = [{
            "issue_id": "LPRI-001",
            "issue_type": "mobile_density",
            "severity": "medium",
            "location": "body",
            "issue_status": "open",
            "explanation": "Paragraph is too dense.",
            "change_required": True,
            "suggested_action": "Split into logical paragraphs.",
        }]
        r["handoff"]["ready_for_factuality_review"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_advisory_cannot_require_change(self):
        data = base_review()
        data["linkedin_platform_review"]["issues"] = [{
            "issue_id": "LPRI-001",
            "issue_type": "format_mismatch",
            "severity": "low",
            "location": "format",
            "issue_status": "advisory",
            "explanation": "Could also work as a document.",
            "change_required": True,
            "suggested_action": "Consider document format.",
        }]
        errors = v.validate(self.write(data))
        self.assertTrue(any("cannot be advisory" in e for e in errors))

    def test_pass_requires_platform_checks_true(self):
        data = base_review()
        data["linkedin_platform_review"]["platform_checks"]["mobile_readable"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("mobile_readable: true" in e for e in errors))

    def test_pass_requires_safe_preservation(self):
        data = base_review()
        data["linkedin_platform_review"]["preservation_checks"]["causal_status_preserved"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("causal_status_preserved: true" in e for e in errors))

    def test_material_unverified_claim_prevents_pass(self):
        data = base_review()
        data["linkedin_platform_review"]["current_platform_claims"] = [{
            "claim": "Ten hashtags increase reach.",
            "material_to_decision": True,
            "verification_status": "needs_current_verification",
            "source_note": None,
        }]
        errors = v.validate(self.write(data))
        self.assertTrue(any("cannot have unresolved material" in e for e in errors))

    def test_needs_verification_requires_unresolved_material_claim(self):
        data = base_review()
        r = data["linkedin_platform_review"]
        r["platform_status"] = "needs_current_verification"
        r["handoff"]["ready_for_factuality_review"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("requires at least one material claim" in e for e in errors))

    def test_valid_needs_verification_review(self):
        data = base_review()
        r = data["linkedin_platform_review"]
        r["platform_status"] = "needs_current_verification"
        r["current_platform_claims"] = [{
            "claim": "A current platform feature has a specific limit.",
            "material_to_decision": True,
            "verification_status": "needs_current_verification",
            "source_note": None,
        }]
        r["handoff"]["ready_for_factuality_review"] = False
        self.assertEqual(v.validate(self.write(data)), [])

    def test_verified_claim_requires_source_note(self):
        data = base_review()
        data["linkedin_platform_review"]["current_platform_claims"] = [{
            "claim": "Current platform rule.",
            "material_to_decision": False,
            "verification_status": "verified",
            "source_note": None,
        }]
        errors = v.validate(self.write(data))
        self.assertTrue(any("source_note" in e for e in errors))

    def test_handoff_must_match_state(self):
        data = base_review()
        data["linkedin_platform_review"]["handoff"]["ready_for_factuality_review"] = False
        errors = v.validate(self.write(data))
        self.assertTrue(any("does not match review state" in e for e in errors))

    def test_ready_handoff_must_point_to_factuality_guard(self):
        data = base_review()
        data["linkedin_platform_review"]["handoff"]["next_skill"] = "wrong-skill"
        errors = v.validate(self.write(data))
        self.assertTrue(any("factuality-guard" in e for e in errors))

    def test_original_text_required(self):
        data = base_review()
        data["linkedin_platform_review"]["original_text"] = ""
        errors = v.validate(self.write(data))
        self.assertTrue(any("original_text" in e for e in errors))

    def test_revised_text_required(self):
        data = base_review()
        data["linkedin_platform_review"]["revised_text"] = ""
        errors = v.validate(self.write(data))
        self.assertTrue(any("revised_text" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
