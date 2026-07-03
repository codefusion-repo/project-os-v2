"""Context-economy and subagent-discipline guards (#382).

Narrow deterministic guards: the kernel keeps the context-economy hard floor,
both agent surfaces inherit it, the resolver surfaces it, the canonical doc
keeps the context classes and subagent rules, and the route-prompt contract
stays compact and issue-referential. No behavior simulation, no broad sweeps.
"""

from __future__ import annotations

import json
from pathlib import Path

from tools.project_os_resolve import resolve

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = REPO_ROOT / "kernel"
DOC_PATH = REPO_ROOT / "docs" / "CONTEXT_ECONOMY.md"
ROUTE_PROMPT_PATH = REPO_ROOT / "templates" / "route-prompt.md"


def _kernel_entry(filename: str, entry_id: str) -> dict:
    data = json.loads((KERNEL_DIR / filename).read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry.get("id") == entry_id:
            return entry
    raise AssertionError(f"{entry_id} not found in kernel/{filename}")


class TestContextEconomyBoundary:
    """The kernel owns a compact context-economy hard floor."""

    def test_boundary_exists_with_canonical_violation_status(self) -> None:
        boundary = _kernel_entry("boundaries.json", "boundary.context_economy")
        assert boundary["on_violation"] == "status.needs_pm_decision"

    def test_rule_keeps_the_hard_floor(self) -> None:
        rule = _kernel_entry("boundaries.json", "boundary.context_economy")["rule"]
        # Live reads and citations beat pasted repetition.
        assert "live reads" in rule
        assert "full issue bodies" in rule
        assert "full diffs" in rule
        assert "full logs" in rule
        # Subagents need a scoped reason and compact packets.
        assert "Subagents are never the default" in rule
        assert "scoped reason" in rule
        assert "compact task-relevant evidence packet" in rule
        assert "claims or evidence leads" in rule
        # High-risk work justifies larger context; gates always win.
        assert "high-risk" in rule
        assert "Economy never drops" in rule
        assert "exact PM approval" in rule

    def test_notes_point_to_single_canonical_doc(self) -> None:
        notes = _kernel_entry("boundaries.json", "boundary.context_economy")["notes"]
        assert "docs/CONTEXT_ECONOMY.md" in notes
        assert "never restate" in notes


class TestAgentSurfacesInheritBoundary:
    """Both agent surfaces inherit context economy; the resolver surfaces it."""

    def test_agent_actors_reference_context_economy(self) -> None:
        for actor_id in ("actor.terminal_agent", "actor.browser_chat"):
            actor = _kernel_entry("actors.json", actor_id)
            assert "boundary.context_economy" in actor["boundary_refs"], actor_id

    def test_resolver_surfaces_context_economy(self) -> None:
        result = resolve(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
            kernel_dir=KERNEL_DIR,
        )
        assert result["status"] == "ok"
        resolved = result["resolved"]
        assert "boundary.context_economy" in resolved["effective"]["effective_boundary_refs"]
        assert "boundary.context_economy" in resolved["boundaries"]


class TestCanonicalDoc:
    """docs/CONTEXT_ECONOMY.md keeps the context classes and subagent rules."""

    def test_doc_distinguishes_the_four_context_classes(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        assert "Read live; never from memory or paste." in text
        assert "Cite or summarize." in text
        assert "Do not paste repeatedly." in text
        assert "Justified larger context." in text

    def test_doc_keeps_subagent_discipline(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        assert "Subagents are not the default." in text
        assert "compact evidence packet" in text
        assert "claims or evidence" in text
        assert "hidden workflow engine" in text

    def test_economy_stays_subordinate_to_gates(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        assert "the gate wins" in text
        assert "never suppress context that high-risk work needs" in text


class TestRoutePromptStaysIssueReferential:
    """The handoff contract stays compact and never carries pasted bodies."""

    def test_route_prompt_references_context_economy(self) -> None:
        text = ROUTE_PROMPT_PATH.read_text(encoding="utf-8")
        assert "boundary.context_economy" in text
        assert "never paste a full issue body" in text

    def test_scope_lines_stay_short_and_issue_referential(self) -> None:
        text = ROUTE_PROMPT_PATH.read_text(encoding="utf-8")
        assert "SCOPE = {{1-3 lines, never the full issue body}}" in text
