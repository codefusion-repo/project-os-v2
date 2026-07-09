"""Proportional validation policy guards for #380.

These are narrow contract checks. They protect the global validation policy
without adding phase-by-phase boilerplate tests.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "legacy-project-os" / "docs" / "VALIDATION_POLICY.md"


def _text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _kernel_entry(filename: str, entry_id: str) -> dict:
    data = json.loads((REPO_ROOT / "legacy-project-os" / "kernel" / filename).read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry.get("id") == entry_id:
            return entry
    raise AssertionError(f"{entry_id} not found in kernel/{filename}")


def test_validation_policy_defines_global_categories_and_mandatory_gates() -> None:
    text = POLICY_PATH.read_text(encoding="utf-8")

    assert "Project OS uses proportional validation everywhere" in text
    for category in (
        "Agent-run required validation",
        "PM-run drafted validation commands",
        "Manual PM validation or checklist",
        "No automated validation needed",
    ):
        assert category in text

    for mandatory in (
        "kernel JSON",
        "resolver or tooling behavior",
        "command-bundle safety",
        "traceability protocol behavior",
        "authorization",
        "security, privacy, secret handling",
        "deployment, external services",
        "production-impacting",
        "deterministic workflow, output, evidence",
    ):
        assert mandatory in text

    assert "Do not add tests merely because a new phase" in text
    assert "Target repositories own their product" in text
    assert "must not impose Project OS-specific test suites" in text
    assert "Review-before-close compares validation evidence" in text


def test_kernel_and_agents_surface_the_global_policy() -> None:
    boundary = _kernel_entry("boundaries.json", "boundary.validation_discipline")
    assert "All Project OS agents and target repositories use proportional validation" in boundary["rule"]
    assert "docs/VALIDATION_POLICY.md" in boundary["notes"]

    refs_by_actor = {
        entry["id"]: set(entry.get("boundary_refs", []))
        for entry in json.loads((REPO_ROOT / "legacy-project-os" / "kernel" / "actors.json").read_text(encoding="utf-8"))["entries"]
    }
    assert "boundary.validation_discipline" in refs_by_actor["actor.terminal_agent"]
    assert "boundary.validation_discipline" in refs_by_actor["actor.browser_chat"]


def test_route_and_review_prompts_classify_validation_without_blanket_defaults() -> None:
    route = _text("legacy-project-os/templates/route-prompt.md")
    op07 = _text("legacy-project-os/templates/operations/07-draft-issue-implementation-route-prompt.md")
    op09 = _text("legacy-project-os/templates/operations/09-review-pr-before-close-and-draft-package.md")
    mos34 = _text("legacy-project-os/templates/mosdlc/operations/fase-3/MOS-3.4-draft-implementation-route-prompt.md")
    mos37 = _text("legacy-project-os/templates/mosdlc/operations/fase-3/MOS-3.7-review-pr-before-close.md")

    assert "docs/VALIDATION_POLICY.md" in route
    assert "PM-run draft commands | manual validation | no automated validation" in route
    assert "does not default to a full suite or new tests" in " ".join(route.split())

    for text in (op07, mos34):
        assert "docs/VALIDATION_POLICY.md" in text
        assert "agent-run" in text
        assert "PM-run" in text
        assert "manual PM validation" in text
        assert "no automated validation" in text

    for text in (op09, mos37):
        assert "docs/VALIDATION_POLICY.md" in text
        assert "PM-run" in text
        assert "manual PM validation" in text
        assert "Fail closed when mandatory validation is missing" in text


def test_target_adapters_do_not_impose_project_os_tests_on_targets() -> None:
    # The active self adapter points to the Spanish proportional-validation
    # policy; archived target adapters keep the English policy reference.
    active = _text("AGENTS.md")
    assert "project-os-es/docs/reglas.md" in active
    assert re.search(r"do not impose\s+Project\s+OS-specific tests", active, re.IGNORECASE)
    for relative_path in (
        "legacy-project-os/adapters/AGENTS.target.md",
        "legacy-project-os/adapters/BROWSER_CHAT.target.md",
        "legacy-project-os/adapters/CLAUDE.target.md",
        "legacy-project-os/adapters/GEMINI.target.md",
    ):
        text = _text(relative_path)
        assert "VALIDATION_POLICY.md" in text, relative_path
        assert re.search(r"do not impose\s+Project\s+OS-specific tests", text, re.IGNORECASE), relative_path


def test_mosdlc_docs_remove_new_phase_requires_tests_assumption() -> None:
    combined = "\n".join(
        _text(path)
        for path in (
            "legacy-project-os/docs/MOSDLC_TEMPLATE_STANDARD.md",
            "legacy-project-os/docs/PM_OPERATIONS.md",
            "legacy-project-os/docs/OPERATION_FLOWS.md",
            "legacy-project-os/docs/MOSDLC_OPERATION_MAP.md",
        )
    )

    assert "Una fase MOSDLC nueva no implica por\n  si misma un archivo de tests nuevo." in combined
    assert "tests solo cuando protegen" in combined
    assert "no exige full suite ni tests nuevos\npor defecto" in combined
    assert "docs y tests" not in combined
    assert "and tests" not in combined
