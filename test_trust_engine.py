
import unittest

from trust_engine import make_decision
from permission_checker import check_permission
from risk_scorer import calculate_risk


class TestAgentTrust(unittest.TestCase):

    def test_supported_high_confidence_is_allowed(self):
        result = make_decision(0.95, "SUPPORTED")
        self.assertEqual(result["decision"], "ALLOW")

    def test_unverified_answer_needs_review(self):
        result = make_decision(0.95, "NOT_VERIFIED")
        self.assertEqual(result["decision"], "REVIEW")

    def test_contradicted_answer_is_blocked(self):
        result = make_decision(0.95, "CONTRADICTED")
        self.assertEqual(result["decision"], "BLOCK")

    def test_low_confidence_is_blocked(self):
        result = make_decision(0.2, "SUPPORTED")
        self.assertEqual(result["decision"], "BLOCK")

    def test_allowed_action(self):
        result = check_permission("draft_email")
        self.assertTrue(result["authorized"])

    def test_unauthorized_action(self):
        result = check_permission("delete_files")
        self.assertFalse(result["authorized"])

    def test_unauthorized_action_has_high_risk(self):
        result = calculate_risk("delete_files", False)
        self.assertEqual(result["risk_score"], 90)
        self.assertEqual(result["risk_level"], "HIGH")


if __name__ == "__main__":
    unittest.main()
