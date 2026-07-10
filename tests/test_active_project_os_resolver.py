"""Focused guards for the active Project OS resolver path."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools.project_os_resolve import DEFAULT_KERNEL_DIR, resolve
from tools.validate_kernel import validate_kernel


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_principal_resolver_defaults_to_the_active_spanish_kernel() -> None:
    result = resolve(
        "actor.terminal_agent",
        "workflow.issue_implementation",
        "mode.delegated_commit_pr",
    )

    assert DEFAULT_KERNEL_DIR == REPO_ROOT / "project-os-es" / "kernel"
    assert result["estado"] == "status.resolved"
    assert result["resuelto"]["manifest"]["key"] == "manifest.kernel_es"
    assert result["autorizacion"]


def test_principal_resolver_supports_known_skills_and_fails_closed_for_unknown_skill() -> None:
    known = resolve(
        "actor.browser_chat",
        "workflow.pm_intake",
        "mode.review_only",
        skill="skill.arquitectura_backend",
    )
    unknown = resolve(
        "actor.browser_chat",
        "workflow.pm_intake",
        "mode.review_only",
        skill="skill.no_existe",
    )

    assert known["estado"] == "status.resolved"
    assert known["resuelto"]["requested_skills"][0]["key"] == "skill.arquitectura_backend"
    assert unknown["estado"] == "status.blocked"
    assert "skill desconocido" in unknown["errores"][0]


def test_active_kernel_validator_and_resolver_cli_pass() -> None:
    assert validate_kernel() == []
    command = [
        sys.executable,
        "tools/project_os_resolve.py",
        "--actor",
        "actor.browser_chat",
        "--workflow",
        "workflow.pm_intake",
        "--mode",
        "mode.review_only",
        "--compact",
    ]
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    assert completed.returncode == 0
    assert '"estado": "status.resolved"' in completed.stdout


def test_active_adapters_and_docs_do_not_name_the_removed_resolver() -> None:
    removed_resolver = "project-os-es/tools/" + "resolver.py"
    active_paths = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "GEMINI.md",
        REPO_ROOT / "README.md",
        *sorted((REPO_ROOT / "project-os-es").rglob("*.md")),
    ]

    assert not (REPO_ROOT / removed_resolver).exists()
    for path in active_paths:
        assert removed_resolver not in path.read_text(encoding="utf-8"), path
    assert "tools/project_os_resolve.py" in (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
