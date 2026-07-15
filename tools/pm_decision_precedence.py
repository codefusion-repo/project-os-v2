"""Deterministic resolution of explicit PM-decision precedence.

This is a small reference implementation of the common kernel contract. It
does not read live evidence or grant permission: callers supply verified
decision facts and the remaining action gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence


Status = Literal[
    "status.resolved",
    "status.needs_context",
    "status.needs_pm_decision",
    "status.blocked",
]

STATUS_PRECEDENCE: dict[Status, int] = {
    "status.resolved": 0,
    "status.needs_context": 1,
    "status.needs_pm_decision": 2,
    "status.blocked": 3,
}


@dataclass(frozen=True)
class DecisionKey:
    """The exact material action governed by a PM decision."""

    project: str
    work_unit: str
    action: str
    scope: str


@dataclass(frozen=True)
class PMDecision:
    """Verified facts about one explicit PM decision."""

    key: DecisionKey
    source: str
    chronological_order: int | None
    source_verified: bool = True
    exact_action: bool = True
    sufficient_scope: bool = True


@dataclass(frozen=True)
class RemainingGate:
    """An action gate independent from PM-decision precedence."""

    name: str
    status: Status
    satisfied: bool = False


@dataclass(frozen=True)
class DecisionResolution:
    """The canonical result fields delivered by MOS-R.3."""

    decision_key: DecisionKey
    superseded_decision: PMDecision | None
    current_pm_decision: PMDecision | None
    required_traceability_follow_up: tuple[str, ...]
    remaining_gates: tuple[RemainingGate, ...]
    resulting_status: Status
    safe_return_operation: str


def _highest_status(gates: Sequence[RemainingGate]) -> Status:
    unsatisfied = [gate.status for gate in gates if not gate.satisfied]
    return max(unsatisfied, key=STATUS_PRECEDENCE.get, default="status.resolved")


def resolve_pm_decision_precedence(
    decision_key: DecisionKey,
    decisions: Sequence[PMDecision],
    *,
    contradictory_durable_sources: Sequence[str] = (),
    remaining_gates: Sequence[RemainingGate] = (),
    mutation_requested: bool = False,
    safe_return_operation: str = "DECISION_SOURCE",
) -> DecisionResolution:
    """Resolve the current PM decision without relaxing independent gates.

    Only verified, chronologically ordered, exact decisions for ``decision_key``
    can supersede one another. A durable contradiction becomes a traceability
    follow-up after a current decision is established; it never changes status
    by itself. Independent gates retain their own status precedence.
    """

    gates = tuple(remaining_gates)
    gate_status = _highest_status(gates)
    matching = tuple(decision for decision in decisions if decision.key == decision_key)

    if gate_status == "status.blocked":
        return DecisionResolution(
            decision_key, None, None, (), gates, gate_status, safe_return_operation
        )

    if not matching:
        status: Status = "status.blocked" if mutation_requested else "status.needs_context"
        return DecisionResolution(decision_key, None, None, (), gates, status, safe_return_operation)

    if any(
        not decision.source_verified or decision.chronological_order is None
        for decision in matching
    ):
        return DecisionResolution(
            decision_key, None, None, (), gates, "status.needs_context", safe_return_operation
        )

    if any(not decision.exact_action or not decision.sufficient_scope for decision in matching):
        status = "status.blocked" if mutation_requested else "status.needs_pm_decision"
        return DecisionResolution(decision_key, None, None, (), gates, status, safe_return_operation)

    ordered = sorted(matching, key=lambda decision: decision.chronological_order or 0, reverse=True)
    current = ordered[0]
    if len(ordered) > 1 and ordered[0].chronological_order == ordered[1].chronological_order:
        return DecisionResolution(
            decision_key, None, None, (), gates, "status.needs_pm_decision", safe_return_operation
        )

    superseded = ordered[1] if len(ordered) > 1 else None
    follow_up = tuple(contradictory_durable_sources)
    return DecisionResolution(
        decision_key,
        superseded,
        current,
        follow_up,
        gates,
        gate_status,
        safe_return_operation,
    )
