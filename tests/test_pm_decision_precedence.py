"""Behavior guards for the shared PM-decision precedence contract."""

import json
from pathlib import Path

from tools.pm_decision_precedence import (
    DecisionKey,
    PMDecision,
    RemainingGate,
    resolve_pm_decision_precedence,
)


KEY = DecisionKey(
    project="codefusion-repo/project-os-v2",
    work_unit="issue #424",
    action="create GitHub Release for the approved tag",
    scope="one exact release over project-os-internal-handoff-v1",
)
REPO_ROOT = Path(__file__).resolve().parents[1]


def decision(order: int | None, **overrides: object) -> PMDecision:
    values: dict[str, object] = {
        "key": KEY,
        "source": f"live PM source {order}",
        "chronological_order": order,
    }
    values.update(overrides)
    return PMDecision(**values)  # type: ignore[arg-type]


def test_exact_approved_publication_supersedes_earlier_decision_and_returns_drift() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(1), decision(2)),
        contradictory_durable_sources=("ADR 0005 Amendment 1", "issue #424"),
        remaining_gates=(RemainingGate("repository permission", "status.resolved", True),),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.resolved"
    assert result.superseded_decision == decision(1)
    assert result.current_pm_decision == decision(2)
    assert result.required_traceability_follow_up == ("ADR 0005 Amendment 1", "issue #424")
    assert result.safe_return_operation == "DECISION_SOURCE"


def test_material_decision_key_excludes_source_and_chronology() -> None:
    earlier = PMDecision(KEY, "issue #424 comment", 1)
    later = PMDecision(KEY, "PR #436 review", 2)

    result = resolve_pm_decision_precedence(KEY, (earlier, later))

    assert result.superseded_decision == earlier
    assert result.current_pm_decision == later
    assert result.resulting_status == "status.resolved"


def test_earlier_generic_message_is_not_a_superseded_decision() -> None:
    earlier_generic = decision(1, exact_action=False)
    later_exact = decision(2)

    result = resolve_pm_decision_precedence(
        KEY,
        (earlier_generic, later_exact),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.resolved"
    assert result.superseded_decision is None
    assert result.current_pm_decision == later_exact


def test_current_exact_decision_supersedes_the_latest_earlier_exact_decision() -> None:
    earlier_exact = decision(1)
    intermediate_generic = decision(2, sufficient_scope=False)
    current_exact = decision(3)

    result = resolve_pm_decision_precedence(
        KEY,
        (earlier_exact, intermediate_generic, current_exact),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.resolved"
    assert result.superseded_decision == earlier_exact
    assert result.current_pm_decision == current_exact


def test_tied_latest_exact_superseded_candidates_fail_closed_regardless_of_input_order() -> None:
    first_candidate = decision(2, source="live PM source first candidate")
    second_candidate = decision(2, source="live PM source second candidate")
    current_exact = decision(3)

    for decisions in (
        (first_candidate, second_candidate, current_exact),
        (second_candidate, first_candidate, current_exact),
    ):
        result = resolve_pm_decision_precedence(KEY, decisions, mutation_requested=True)

        assert result.resulting_status == "status.needs_pm_decision"
        assert result.superseded_decision is None
        assert result.current_pm_decision == current_exact


def test_unique_exact_candidate_wins_when_generic_messages_share_its_order() -> None:
    exact_candidate = decision(2, source="live PM source exact candidate")
    generic_message = decision(2, exact_action=False, source="live PM source continue")
    insufficient_message = decision(
        2,
        sufficient_scope=False,
        source="live PM source do it",
    )
    current_exact = decision(3)

    result = resolve_pm_decision_precedence(
        KEY,
        (generic_message, exact_candidate, insufficient_message, current_exact),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.resolved"
    assert result.superseded_decision == exact_candidate
    assert result.current_pm_decision == current_exact


def test_ambiguous_current_decision_needs_pm_decision_without_mutation() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(1), decision(2, exact_action=False)),
    )

    assert result.resulting_status == "status.needs_pm_decision"
    assert result.superseded_decision is None
    assert result.current_pm_decision is None


def test_later_ambiguous_decision_blocks_a_mutation() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(1), decision(2, sufficient_scope=False)),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.blocked"
    assert result.superseded_decision is None
    assert result.current_pm_decision is None


def test_current_decision_reports_durable_drift_even_without_an_earlier_pm_decision() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(2),),
        contradictory_durable_sources=("older handoff procedure",),
    )

    assert result.resulting_status == "status.resolved"
    assert result.superseded_decision is None
    assert result.current_pm_decision == decision(2)
    assert result.required_traceability_follow_up == ("older handoff procedure",)


def test_later_exact_closure_keeps_review_before_close_as_an_independent_gate() -> None:
    close_key = DecisionKey(KEY.project, KEY.work_unit, "close issue #424", "close after review")
    result = resolve_pm_decision_precedence(
        close_key,
        (PMDecision(close_key, "live PM source 1", 1), PMDecision(close_key, "live PM source 2", 2)),
        remaining_gates=(RemainingGate("review-before-close", "status.blocked"),),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.blocked"
    assert result.current_pm_decision == PMDecision(close_key, "live PM source 2", 2)
    assert result.superseded_decision == PMDecision(close_key, "live PM source 1", 1)


def test_ambiguous_current_decision_remains_unresolved() -> None:
    earlier_exact = decision(2)
    first_current_candidate = decision(3, source="live PM source first current candidate")
    second_current_candidate = decision(3, source="live PM source second current candidate")

    result = resolve_pm_decision_precedence(
        KEY,
        (earlier_exact, first_current_candidate, second_current_candidate),
    )

    assert result.resulting_status == "status.needs_pm_decision"
    assert result.superseded_decision is None
    assert result.current_pm_decision is None


def test_unverifiable_decision_needs_context_without_mutation() -> None:
    result = resolve_pm_decision_precedence(KEY, (decision(None),))

    assert result.resulting_status == "status.needs_context"


def test_mutation_with_unverifiable_pm_approval_is_blocked() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(2, source_verified=False),),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.blocked"


def test_insufficient_or_different_action_cannot_authorize_a_mutation() -> None:
    insufficient = resolve_pm_decision_precedence(
        KEY, (decision(1, sufficient_scope=False),), mutation_requested=True
    )
    different_action = resolve_pm_decision_precedence(
        KEY,
        (PMDecision(DecisionKey(KEY.project, KEY.work_unit, "close issue #424", "close only"), "live PM source", 1),),
        mutation_requested=True,
    )

    assert insufficient.resulting_status == "status.blocked"
    assert different_action.resulting_status == "status.blocked"


def test_related_approved_action_does_not_authorize_settings_mutation() -> None:
    settings_key = DecisionKey(KEY.project, KEY.work_unit, "change repository settings", "visibility")
    result = resolve_pm_decision_precedence(
        settings_key,
        (decision(2),),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.blocked"
    assert result.current_pm_decision is None


def test_generic_pm_approval_does_not_authorize_a_mutation() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(2, exact_action=False),),
        mutation_requested=True,
    )

    assert result.resulting_status == "status.blocked"


def test_status_result_contract_supports_the_canonical_mos_r3_resolution_in_both_languages() -> None:
    expected = (
        (
            "project-os-es/kernel/salidas.json",
            "project-os-es/templates/resultado-estado.md",
            "project-os-es/operaciones/cross-fase/MOS-R.3-procesar-decision-pm-pendiente.md",
            "cuando MOS-R.3 procese una decision PM",
        ),
        (
            "project-os-en/kernel/outputs.json",
            "project-os-en/templates/status-result.md",
            "project-os-en/operations/cross-phase/MOS-R.3-process-needs-pm-decision.md",
            "when MOS-R.3 processes a PM decision",
        ),
    )
    fields = (
        "decision_key",
        "superseded_decision",
        "current_pm_decision",
        "required_traceability_follow_up",
        "remaining_gates",
        "resulting_status",
        "safe_return_operation",
    )

    for output_path, template_path, operation_path, prefix in expected:
        outputs = json.loads((REPO_ROOT / output_path).read_text(encoding="utf-8"))["outputs"]
        status_result = next(output for output in outputs if output["key"] == "output.status_result")
        contract = " ".join((status_result["use_for"], *status_result["must_include"]))
        template = (REPO_ROOT / template_path).read_text(encoding="utf-8")
        operation = (REPO_ROOT / operation_path).read_text(encoding="utf-8")

        assert prefix in contract
        assert all(field in contract for field in fields)
        assert all(field in template for field in fields)
        assert all(field in operation for field in fields)


def test_non_delegable_limits_keep_precedence_over_a_current_pm_decision() -> None:
    for gate_name in (
        "boundary.draft_only_browser",
        "real repository permission",
        "secret safety",
        "required validation",
    ):
        result = resolve_pm_decision_precedence(
            KEY,
            (decision(1), decision(2)),
            remaining_gates=(RemainingGate(gate_name, "status.blocked"),),
        )

        assert result.resulting_status == "status.blocked"
        assert result.current_pm_decision == decision(2)
        assert result.superseded_decision == decision(1)
