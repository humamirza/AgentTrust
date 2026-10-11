
import unittest

from evidence_checker import check_evidence


class TestEvidenceChecker(unittest.TestCase):

    def test_correct_answer_is_supported(self):
        result = check_evidence(
            "What is the capital of France?",
            "Paris",
            ["The capital of France is Paris."]
        )
        self.assertEqual(result, "SUPPORTED")

    def test_wrong_answer_is_contradicted(self):
        result = check_evidence(
            "What is the capital of France?",
            "Lyon",
            ["The capital of France is Paris."]
        )
        self.assertEqual(result, "CONTRADICTED")

    def test_missing_evidence_is_not_verified(self):
        result = check_evidence(
            "What is the capital of France?",
            "Paris",
            []
        )
        self.assertEqual(result, "NOT_VERIFIED")

    def test_unknown_question_is_not_verified(self):
        result = check_evidence(
            "What will happen in 2035?",
            "Something might happen",
            ["An unrelated fact."]
        )
        self.assertEqual(result, "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
