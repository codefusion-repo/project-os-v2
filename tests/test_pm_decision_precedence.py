"""Behavior guards for the shared PM-decision precedence contract."""

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


def decision(order: int | None, **overrides: object) -> PMDecision:
    values: dict[str, object] = {
        "key": KEY,
        "source": f"live PM source {order}",
        "chronological_order": order,
    }
    values.update(overrides)
    return PMDecision(**values)  # type: ignore[arg-type]


def test_later_exact_decision_supersedes_earlier_one_and_returns_traceability_drift() -> None:
    result = resolve_pm_decision_precedence(
        KEY,
        (decision(1), decision(2)),
        contradictory_durable_sources=("ADR 0005 Amendment 1", "issue #424"),
        remaining_gates=(RemainingGate("repository permission", "status.resolved", True),),
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


def test_ambiguous_or_unverifiable_decisions_fail_closed_with_the_specific_status() -> None:
    ambiguous = resolve_pm_decision_precedence(KEY, (decision(2), decision(2)))
    missing_context = resolve_pm_decision_precedence(KEY, (decision(None),))

    assert ambiguous.resulting_status == "status.needs_pm_decision"
    assert missing_context.resulting_status == "status.needs_context"


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
