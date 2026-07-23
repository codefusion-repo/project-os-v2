"""Behavioral guards for change-class enforcement and density projection.

These cover only executable resolver behavior: fail-closed coherence, the
non-downgradable critical gate, mutation requiring a declared class, and the
per-density field projection. They intentionally do not assert configured prose.
"""

from __future__ import annotations

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
    assert "workflow.issue_implementation" in selected["allowed_workflows"]


def test_mutation_requires_a_declared_change_class() -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL)

    assert result["estado"] == "status.blocked"
    assert result["resuelto"] is None
    assert "workflow.issue_implementation" in result["errores"][0]


def test_read_only_stage_needs_no_class_but_the_write_stage_does() -> None:
    # target_adoption can emit a mutable output, but its browser draft runs in the
    # read-only mode and never mutates, so it needs no class; the terminal write
    # stage does mutate and must declare one.
    draft = resolve(
        "actor.browser_chat",
        "workflow.target_adoption",
        "mode.review_only",
        kernel_dir=ES_KERNEL,
    )
    write_without_class = resolve(
        "actor.terminal_agent",
        "workflow.target_adoption",
        "mode.delegated_commit_pr",
        kernel_dir=ES_KERNEL,
    )

    assert draft["estado"] == "status.resolved"
    assert "change_class" not in draft["resuelto"]
    assert write_without_class["estado"] == "status.blocked"
    assert write_without_class["resuelto"] is None


def test_critical_density_is_full_debug_and_cannot_be_downgraded() -> None:
    default = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.critical")
    kept = resolve(
        **IMPLEMENTATION,
        kernel_dir=ES_KERNEL,
        change_class="change_class.critical",
        hydration_level="full/debug",
    )
    downgraded = resolve(
        **IMPLEMENTATION,
        kernel_dir=ES_KERNEL,
        change_class="change_class.critical",
        hydration_level="compact",
    )

    assert default["hydration_level"] == "full/debug"
    assert kept["estado"] == "status.resolved" and kept["hydration_level"] == "full/debug"
    assert downgraded["estado"] == "status.blocked"
    assert downgraded["resuelto"] is None


def test_explicit_level_may_raise_but_not_lower_the_class_density() -> None:
    elevated = resolve(
        **IMPLEMENTATION,
        kernel_dir=ES_KERNEL,
        change_class="change_class.small",
        hydration_level="full/debug",
    )

    assert elevated["estado"] == "status.resolved"
    assert elevated["hydration_level"] == "full/debug"


def test_critical_class_surfaces_the_unverifiable_gates_as_remaining_gates() -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.critical")

    gates = {gate["gate"]: gate for gate in result["resuelto"]["change_class"]["remaining_gates"]}
    assert set(gates) == {
        "formal_unit_required",
        "pr_required",
        "review_level",
        "validation_level",
        "prior_docs",
    }
    assert gates["review_level"]["required"] == "review.independent"
    assert gates["pr_required"]["required"] is True


def test_critical_class_survives_the_review_of_the_unit() -> None:
    review = resolve(
        "actor.terminal_agent",
        "workflow.review_before_close",
        "mode.review_only",
        kernel_dir=ES_KERNEL,
        change_class="change_class.critical",
    )

    assert review["estado"] == "status.resolved"
    assert review["hydration_level"] == "full/debug"
    assert review["resuelto"]["change_class"]["review_level"] == "review.independent"


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


@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_execution_report_projects_exactly_one_density_contract(kernel_dir: Path) -> None:
    reports = {
        level: execution_report(
            resolve(
                **IMPLEMENTATION,
                kernel_dir=kernel_dir,
                change_class="change_class.small",
                hydration_level=level,
            )
        )
        for level in LEVELS
    }

    for level, report in reports.items():
        assert isinstance(report["must_include"], list) and report["must_include"], level
        assert "must_include_by_density" not in report, level
    assert len(reports["minimal"]["must_include"]) == 4
    assert len(reports["compact"]["must_include"]) == 4
    assert reports["minimal"]["must_include"] != reports["compact"]["must_include"]
    assert len(reports["full/debug"]["must_include"]) > len(reports["compact"]["must_include"])
