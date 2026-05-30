"""R1.10 validator regression tests."""

from __future__ import annotations

import unittest
from pathlib import Path

from project_os_v2.validators import validate_r1_10


class R110ValidatorTests(unittest.TestCase):
    def test_negative_fixture_reports_missing_required_id(self) -> None:
        root = Path(__file__).parent / "fixtures" / "r1_10_invalid_missing_id"
        findings = validate_r1_10(root)
        self.assertTrue(any(finding.code == "REQUIRED_FIELD_MISSING" for finding in findings))
        self.assertTrue(any(finding.pointer == "/id" for finding in findings))


if __name__ == "__main__":
    unittest.main()
