"""Behavioral guards for change-class enforcement and density projection.

These cover only executable resolver behavior: fail-closed coherence, mutation
requiring a declared class, the material gates the class keeps, and the report
density projected from the class independently of hydration. They intentionally
do not assert configured prose.
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
@pytest.mark.parametrize(
    "change_class", ("change_class.small", "change_class.standard", "change_class.critical")
)
def test_every_class_resolves_at_the_compact_hydration_default(
    kernel_dir: Path, change_class: str
) -> None:
    result = resolve(**IMPLEMENTATION, kernel_dir=kernel_dir, change_class=change_class)

    assert result["estado"] == "status.resolved"
    assert result["hydration_level"] == "compact"
    selected = result["resuelto"]["change_class"]
    assert selected["key"] == change_class
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


@pytest.mark.parametrize("level", LEVELS)
def test_any_level_resolves_for_a_critical_class_without_a_ranking(level: str) -> None:
    result = resolve(
        **IMPLEMENTATION,
        kernel_dir=ES_KERNEL,
        change_class="change_class.critical",
        hydration_level=level,
    )

    assert result["estado"] == "status.resolved"
    assert result["hydration_level"] == level


def test_critical_class_keeps_its_gates_and_report_at_the_compact_default() -> None:
    default = resolve(**IMPLEMENTATION, kernel_dir=ES_KERNEL, change_class="change_class.critical")
    audited = resolve(
        **IMPLEMENTATION,
        kernel_dir=ES_KERNEL,
        change_class="change_class.critical",
        hydration_level="full/debug",
    )

    assert default["hydration_level"] == "compact"
    gates = {gate["gate"]: gate["required"] for gate in default["resuelto"]["change_class"]["remaining_gates"]}
    assert gates == {
        "formal_unit_required": True,
        "pr_required": True,
        "review_level": "review.independent",
        "validation_level": "validation.broad",
        "prior_docs": "expected",
    }
    # A lower hydration never degrades the class's material contract.
    assert execution_report(default)["must_include"] == execution_report(audited)["must_include"]
    assert default["resuelto"]["change_class"] == audited["resuelto"]["change_class"]


@pytest.mark.parametrize("level", LEVELS)
def test_report_density_follows_the_class_not_the_hydration_level(level: str) -> None:
    small = execution_report(
        resolve(
            **IMPLEMENTATION,
            kernel_dir=ES_KERNEL,
            change_class="change_class.small",
            hydration_level=level,
        )
    )
    critical = execution_report(
        resolve(
            **IMPLEMENTATION,
            kernel_dir=ES_KERNEL,
            change_class="change_class.critical",
            hydration_level=level,
        )
    )

    assert len(small["must_include"]) == 4
    assert len(critical["must_include"]) == 10
    assert small["must_include"] != critical["must_include"]


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
    assert review["hydration_level"] == "compact"
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
        change_class: execution_report(
            resolve(**IMPLEMENTATION, kernel_dir=kernel_dir, change_class=change_class)
        )
        for change_class in (
            "change_class.small",
            "change_class.standard",
            "change_class.critical",
        )
    }

    for change_class, report in reports.items():
        assert isinstance(report["must_include"], list) and report["must_include"], change_class
        assert "must_include_by_density" not in report, change_class
    assert len(reports["change_class.small"]["must_include"]) == 4
    assert len(reports["change_class.standard"]["must_include"]) == 4
    assert (
        reports["change_class.small"]["must_include"]
        != reports["change_class.standard"]["must_include"]
    )
    assert len(reports["change_class.critical"]["must_include"]) > len(
        reports["change_class.standard"]["must_include"]
    )
