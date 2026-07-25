"""Stable safety and shape guards for resolver hydration levels."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from tools.project_os_resolve import (
    DEFAULT_HYDRATION_LEVEL,
    HYDRATION_LEVEL_VALUES,
    HydrationLevel,
    resolve,
    resolver,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
# A non-mutating workflow keeps these generic hydration-projection guards free of
# a declared change class; mutation + class coverage lives in
# test_proportional_resolution.py.
SELECTOR = {
    "actor_id": "actor.terminal_agent",
    "workflow_id": "workflow.review_before_close",
    "mode_id": "mode.review_only",
}
LEVELS = ("minimal", "compact", "full/debug")
SAFETY_LIMITS = {
    "boundary.branch_preflight",
    "boundary.separate_pm_approval",
    "boundary.no_live_state_durable",
    "boundary.no_invented_state",
    "boundary.security_privacy",
    "boundary.fail_closed",
    "boundary.output_not_permission",
    "boundary.validation_discipline",
}


def resolve_level(level: str | None, kernel_dir: Path = ES_KERNEL, **kwargs: Any) -> dict[str, Any]:
    return resolve(
        **SELECTOR,
        kernel_dir=kernel_dir,
        hydration_level=level,
        **kwargs,
    )


def item_keys(items: list[dict[str, Any]]) -> set[str]:
    return {item["key"] for item in items}


def structural_shape(value: Any) -> Any:
    """Compare fields and collection structure while ignoring translated prose."""

    if isinstance(value, dict):
        return {key: structural_shape(item) for key, item in value.items()}
    if isinstance(value, list):
        return [structural_shape(item) for item in value]
    return type(value).__name__


@pytest.mark.parametrize("level", LEVELS)
def test_public_hydration_values_parse_through_canonical_and_issue_aliases(level: str) -> None:
    canonical = resolve_level(level)
    alias = resolver(
        SELECTOR["actor_id"],
        SELECTOR["mode_id"],
        SELECTOR["workflow_id"],
        kernel_dir=ES_KERNEL,
        compact=level,
    )

    assert canonical["estado"] == alias["estado"] == "status.resolved"
    assert canonical["hydration_level"] == alias["hydration_level"] == level


def test_default_is_compact_and_existing_callers_keep_the_compact_result() -> None:
    existing_call = resolve(**SELECTOR, kernel_dir=ES_KERNEL)
    explicit = resolve_level(DEFAULT_HYDRATION_LEVEL.value)

    assert DEFAULT_HYDRATION_LEVEL is HydrationLevel.COMPACT
    assert HYDRATION_LEVEL_VALUES == LEVELS
    assert existing_call == explicit
    assert existing_call["hydration_level"] == "compact"


@pytest.mark.parametrize("invalid", ("", "debug", "full_debug", "COMPACT"))
def test_unknown_hydration_values_fail_closed_without_a_fallback(invalid: str) -> None:
    result = resolve_level(invalid)

    assert result["estado"] == "status.blocked"
    assert result["resuelto"] is None
    assert result["errores"] == [
        "unknown hydration level; expected exactly one of: minimal, compact, full/debug"
    ]
    assert "hydration_level" not in result


def test_conflicting_hydration_parameter_spellings_fail_closed() -> None:
    result = resolver(
        SELECTOR["actor_id"],
        SELECTOR["mode_id"],
        SELECTOR["workflow_id"],
        hydration_level="minimal",
        compact="minimal",
    )

    assert result["estado"] == "status.blocked"
    assert result["resuelto"] is None
    assert result["errores"] == ["hydration_level and compact cannot be supplied together"]


def test_cli_keeps_legacy_compact_formatting_and_accepts_hydration_levels() -> None:
    command = [
        sys.executable,
        "tools/project_os_resolve.py",
        "--actor",
        SELECTOR["actor_id"],
        "--workflow",
        SELECTOR["workflow_id"],
        "--mode",
        SELECTOR["mode_id"],
        "--hydration-level",
        "full/debug",
        "--compact",
    ]
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False, capture_output=True, text=True)

    assert completed.returncode == 0
    assert len(completed.stdout.strip().splitlines()) == 1
    assert json.loads(completed.stdout)["hydration_level"] == "full/debug"

    invalid_command = command[: command.index("--hydration-level")] + [
        "--hydration-level",
        "verbose",
    ]
    invalid = subprocess.run(
        invalid_command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert invalid.returncode == 1
    assert json.loads(invalid.stdout)["estado"] == "status.blocked"


def test_levels_have_deterministic_monotonic_contract_shapes_and_keep_safety() -> None:
    results = {level: resolve_level(level) for level in LEVELS}
    minimal = results["minimal"]["resuelto"]
    compact = results["compact"]["resuelto"]
    full_debug = results["full/debug"]["resuelto"]

    assert resolve_level("minimal") == results["minimal"]
    assert set(minimal) < set(compact)
    assert "reglas_operativas" not in minimal
    assert "artefactos" not in minimal["workflow"]
    assert "artefactos" in compact["workflow"]
    assert set(compact["manifest"]) < set(full_debug["manifest"])
    assert "active" not in compact["manifest"]
    assert full_debug["manifest"]["active"] is True

    expected_limits = item_keys(full_debug["limites"])
    expected_evidence = item_keys(full_debug["workflow"]["required_evidence"])
    expected_outputs = item_keys(full_debug["workflow"]["allowed_outputs"])
    expected_statuses = item_keys(full_debug["estados_permitidos"])
    expected_prohibited_actions = full_debug["mode"]["prohibited_actions"]

    for level, result in results.items():
        resolved = result["resuelto"]
        assert result["estado"] == "status.resolved", level
        # No level pays for provenance; raising density never turns it back on.
        assert "context_plan" not in result, level
        contract = resolved["workflow"]["context_receipt_contract"]
        assert contract["detailed_provenance_default"] == "omitted"
        assert contract["pm_facing_traceability"] == "reviewed_evidence"
        assert contract["stores_source_bodies"] is False
        assert contract["stores_durable_live_state"] is False
        assert "nunca concede permisos" in result["autorizacion"]
        assert item_keys(resolved["limites"]) == expected_limits
        assert SAFETY_LIMITS <= item_keys(resolved["limites"])
        assert item_keys(resolved["workflow"]["required_evidence"]) == expected_evidence
        assert item_keys(resolved["workflow"]["allowed_outputs"]) == expected_outputs
        assert item_keys(resolved["estados_permitidos"]) == expected_statuses
        assert resolved["mode"]["prohibited_actions"] == expected_prohibited_actions
        assert all("meaning" in status for status in resolved["estados_permitidos"])
        security_limit = next(
            limit for limit in resolved["limites"] if limit["key"] == "boundary.security_privacy"
        )
        assert security_limit["on_violation"] == "status.blocked"
        assert security_limit["rule"]


@pytest.mark.parametrize("level", LEVELS)
def test_spanish_and_english_keep_the_same_relevant_hydration_structure(level: str) -> None:
    spanish = resolve_level(level, kernel_dir=ES_KERNEL, skill="skill.arquitectura_backend")
    english = resolve_level(level, kernel_dir=EN_KERNEL, skill="skill.arquitectura_backend")

    assert spanish["estado"] == english["estado"] == "status.resolved"
    assert spanish["hydration_level"] == english["hydration_level"] == level
    assert structural_shape(spanish["resuelto"]) == structural_shape(english["resuelto"])
    for result in (spanish, english):
        resolved = result["resuelto"]
        assert item_keys(resolved["limites"]) >= SAFETY_LIMITS
        assert resolved["requested_skills"][0]["key"] == "skill.arquitectura_backend"
        if level != "minimal":
            for artifact in resolved["workflow"]["artefactos"]:
                assert (REPO_ROOT / artifact["required_template"]).is_file()

    assert all(
        item["required_template"].startswith("project-os-es/templates/")
        for item in spanish["resuelto"]["workflow"].get("artefactos", [])
    )
    assert all(
        item["required_template"].startswith("project-os-en/templates/")
        for item in english["resuelto"]["workflow"].get("artefactos", [])
    )


@pytest.mark.parametrize("level", LEVELS)
def test_requested_skills_and_existing_fail_closed_boundaries_survive_each_level(level: str) -> None:
    known = resolve_level(level, skill="skill.arquitectura_backend")
    unknown = resolve_level(level, skill="skill.unknown")
    invalid_kernel = resolve_level(level, kernel_dir=REPO_ROOT / "project-os-en")

    assert known["estado"] == "status.resolved"
    skill = known["resuelto"]["requested_skills"][0]
    assert skill["key"] == "skill.arquitectura_backend"
    assert (REPO_ROOT / skill["required_skill"]).is_file()
    assert unknown["estado"] == "status.blocked"
    assert invalid_kernel["estado"] == "status.blocked"
    assert invalid_kernel["resuelto"] is None
