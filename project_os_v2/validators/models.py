"""Shared validator result types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    file: str
    pointer: str
    contract_id: str | None
    expected: Any
    actual: Any
    hint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "file": self.file,
            "pointer": self.pointer,
            "contract_id": self.contract_id,
            "expected": self.expected,
            "actual": self.actual,
            "remediation_hint": self.hint,
        }


class ToolingError(RuntimeError):
    """Tooling/configuration failure that should return exit code 2."""
