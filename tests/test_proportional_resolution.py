"""Behavioral guards for change-class coherence and density projection."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.project_os_resolve import resolve


REPO_ROOT = Path(__file__).resolve().parents[1]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
IMPLEMENTATION = {
    "actor_id": "actor.terminal_agent",
    "workflow_id": "workflow.issue_implementation",
    "mode_id": "mode.delegated_commit_pr",
}
LEVELS = ("minimal", "compact", "full/debug")


def execution_report(result: dict) -> dict:
    return next(
        output
        for output in result["resuelto"]["workflow"]["allowed_outputs"]
        if output["key"] == "output.execution_report"
    )


@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_declared_small_class_resolves_with_minimal_density_default(kernel_dir: Path) -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=kernel_dir, change_class="change_class.small")

    assert result["estado"] == "status.resolved"
    assert result["hydration_level"] == "minimal"
    selected = result["resuelto"]["change_class"]
    assert selected["key"] == "change_class.small"
    assert selected["contract_key"] == "proportionality.change_class"
    assert selected["formal_unit_required"] is False
    assert "source.live_pm_decision" in selected["unit_representations"]
    assert "workflow.issue_implementation" in selected["allowed_workflows"]


def test_each_class_selects_its_contractual_density_and_explicit_level_wins() -> None:
    critical = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.critical")
    standard = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.standard")
    overridden = resolve(
        **IMPLEMENTATION,
        kernel_dir=ES_KERNEL,
        change_class="change_class.critical",
        hydration_level="compact",
    )

    assert critical["hydration_level"] == "full/debug"
    assert standard["hydration_level"] == "compact"
    assert overridden["hydration_level"] == "compact"
    assert overridden["resuelto"]["change_class"]["key"] == "change_class.critical"


def test_read_class_cannot_select_a_mutating_workflow() -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.read")

    assert result["estado"] == "status.blocked"
    assert result["resuelto"] is None
    assert "change_class.read" in result["errores"][0]
    assert "workflow.issue_implementation" in result["errores"][0]


def test_unknown_class_fails_closed_listing_known_classes() -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.bogus")

    assert result["estado"] == "status.blocked"
    assert result["resuelto"] is None
    assert "change_class.bogus" in result["errores"][0]
    assert "change_class.small" in result["errores"][0]


def test_undeclared_class_keeps_existing_resolution_shape() -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL)

    assert result["estado"] == "status.resolved"
    assert result["hydration_level"] == "compact"
    assert "change_class" not in result["resuelto"]


def test_read_class_resolves_review_workflows_at_minimal_density() -> None:
    result = resolve(
        "actor.browser_chat",
        "workflow.review_only",
        "mode.review_only",
        kernel_dir=ES_KERNEL,
        change_class="change_class.read",
    )

    assert result["estado"] == "status.resolved"
    assert result["hydration_level"] == "minimal"
    assert result["resuelto"]["change_class"]["pr_required"] is False


@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_execution_report_projects_exactly_one_density_contract(kernel_dir: Path) -> None:
    reports = {
        level: execution_report(resolve(**IMPLEMENTATION, kernel_dir=kernel_dir, hydration_level=level))
        for level in LEVELS
    }

    for level, report in reports.items():
        assert isinstance(report["must_include"], list) and report["must_include"], level
        assert "must_include_by_density" not in report, level
    assert len(reports["minimal"]["must_include"]) == 4
    assert len(reports["compact"]["must_include"]) == 4
    assert len(reports["full/debug"]["must_include"]) == 9
    assert reports["minimal"]["must_include"] != reports["compact"]["must_include"]


def test_lower_densities_produce_materially_smaller_report_contracts() -> None:
    sizes = {
        level: len(
            json.dumps(
                execution_report(
                    resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, hydration_level=level)
                )["must_include"],
                ensure_ascii=False,
            )
        )
        for level in LEVELS
    }

    assert sizes["minimal"] < sizes["full/debug"] / 2
    assert sizes["compact"] < sizes["full/debug"] / 2


def test_full_debug_exposes_the_whole_proportionality_contract() -> None:
    full = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, hydration_level="full/debug")
    compact = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL)

    contract = full["resuelto"]["workflow"]["proportionality_contract"]
    assert contract["key"] == "proportionality.change_class"
    assert [entry["key"] for entry in contract["classes"]] == [
        "change_class.read",
        "change_class.small",
        "change_class.standard",
        "change_class.critical",
    ]
    assert "proportionality_contract" not in compact["resuelto"]["workflow"]
