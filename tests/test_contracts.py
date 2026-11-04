import importlib
import importlib.util
import unittest
from pathlib import Path

from shared.contracts import validate_expected_counts, decision_from_counts
from members.member07_app.cli import model_registry

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.counts = {str(i): 2 for i in range(1,6)}

    def test_unknown_forces_fail_even_when_target_counts_match(self):
        self.assertEqual(decision_from_counts(self.counts,self.counts,1)["predicted_label"], "FAIL")

    def test_changing_requirement_changes_only_decision(self):
        observed = dict(self.counts)
        self.assertEqual(decision_from_counts(observed,self.counts,0)["predicted_label"], "PASS")
        expected = dict(self.counts, **{"1":3})
        self.assertEqual(decision_from_counts(observed,expected,0)["predicted_label"], "FAIL")
        self.assertEqual(observed,self.counts)

    def test_review_cannot_pass(self):
        self.assertIsNone(decision_from_counts(self.counts,self.counts,0,True)["predicted_label"])

    def test_invalid_counts(self):
        for value in (-1,True,2.5,"2"):
            with self.subTest(value=value),self.assertRaises(ValueError):
                validate_expected_counts(dict(self.counts, **{"1":value}))
        with self.assertRaises(ValueError):
            validate_expected_counts({"1":2})

    def test_registered_modules_have_predict(self):
        for module in model_registry().values():
            self.assertTrue(callable(getattr(importlib.import_module(module),"predict",None)))

    def test_member_and_integration_scope(self):
        path=Path(__file__).resolve().parents[1]/".github"/"check_scope.py"
        spec=importlib.util.spec_from_file_location("scope",path)
        scope=importlib.util.module_from_spec(spec);spec.loader.exec_module(scope)
        self.assertTrue(scope.allowed_paths("member04/hog","student","owner",["members/member04_hog/model.py"]))
        self.assertFalse(scope.allowed_paths("member04/hog","student","owner",["shared/catalogue.json"]))
        self.assertFalse(scope.allowed_paths("integration/change","student","owner",["README.md"]))
        self.assertTrue(scope.allowed_paths("integration/change","owner","owner",["README.md"]))

if __name__ == "__main__":
    unittest.main()
