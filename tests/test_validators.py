"""Validator regression tests."""

from __future__ import annotations

import unittest
from pathlib import Path

from project_os_v2.validators import validate_r1_10, validate_r1_11


class R110ValidatorTests(unittest.TestCase):
    def test_negative_fixture_reports_missing_required_id(self) -> None:
        root = Path(__file__).parent / "fixtures" / "r1_10_invalid_missing_id"
        findings = validate_r1_10(root)
        self.assertTrue(any(finding.code == "REQUIRED_FIELD_MISSING" for finding in findings))
        self.assertTrue(any(finding.pointer == "/id" for finding in findings))


class R111ValidatorTests(unittest.TestCase):
    def test_negative_fixture_reports_actor_hard_limit_duplication(self) -> None:
        root = Path(__file__).parent / "fixtures" / "r1_11_invalid_actor_hard_limit_duplication"
        findings = validate_r1_11(root)
        self.assertTrue(any(finding.code == "ACTOR_HARD_LIMIT_DUPLICATED" for finding in findings))
        self.assertTrue(any(finding.code == "ENTITY_PAYLOAD_FIELD_NOT_OWNED" for finding in findings))


if __name__ == "__main__":
    unittest.main()
