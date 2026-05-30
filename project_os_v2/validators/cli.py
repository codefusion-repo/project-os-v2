"""Command line interface for Project OS v2 validators."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .core import validate_r1_10
from .models import Finding, ToolingError


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m project_os_v2.validators")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Run read-only validators")
    validate_parser.add_argument("--phase", choices=("r1.10", "all"), required=True)
    validate_parser.add_argument("--root", type=Path, default=Path("."))
    validate_parser.add_argument("--report-format", choices=("text", "json"), default="text")

    args = parser.parse_args(argv)
    if args.command != "validate":
        parser.error("unsupported command")

    try:
        findings = _run_phase(args.phase, args.root)
    except ToolingError as exc:
        print(f"TOOLING_ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"TOOLING_ERROR: {exc}", file=sys.stderr)
        return 2

    _print_report(findings, args.report_format, args.phase, args.root)
    return 1 if findings else 0


def _run_phase(phase: str, root: Path) -> list[Finding]:
    if phase in {"r1.10", "all"}:
        return validate_r1_10(root)
    raise ToolingError(f"unsupported phase: {phase}")


def _print_report(findings: list[Finding], report_format: str, phase: str, root: Path) -> None:
    if report_format == "json":
        payload = {
            "phase": phase,
            "root": str(root),
            "status": "fail" if findings else "pass",
            "finding_count": len(findings),
            "findings": [finding.as_dict() for finding in findings],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print(f"Project OS v2 validator phase: {phase}")
    print(f"Root: {root}")
    if not findings:
        print("Status: pass")
        print("Findings: 0")
        return

    print("Status: fail")
    print(f"Findings: {len(findings)}")
    for index, finding in enumerate(findings, start=1):
        print(f"\n[{index}] {finding.code} ({finding.severity})")
        print(f"file: {finding.file}")
        print(f"pointer: {finding.pointer}")
        print(f"contract_id: {finding.contract_id if finding.contract_id is not None else '-'}")
        print(f"expected: {finding.expected}")
        print(f"actual: {finding.actual}")
        print(f"remediation_hint: {finding.hint}")
