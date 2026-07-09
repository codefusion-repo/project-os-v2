"""Tests for the deterministic kernel resolver."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from tools.project_os_resolve import main, resolve

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = REPO_ROOT / "legacy-project-os" / "kernel"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_ok(actor: str, workflow: str, mode: str) -> dict:
    """Call resolve() against the real kernel and assert status=ok."""
    result = resolve(actor, workflow, mode, kernel_dir=KERNEL_DIR)
    assert result["status"] == "ok", f"Expected ok, got: {result['errors']}"
    assert result["errors"] == []
    assert result["resolved"] is not None
    return result


def _resolve_error(actor: str, workflow: str, mode: str) -> dict:
    """Call resolve() against the real kernel and assert status=error."""
    result = resolve(actor, workflow, mode, kernel_dir=KERNEL_DIR)
    assert result["status"] == "error", f"Expected error, got status={result['status']}"
    assert result["resolved"] is None
    assert len(result["errors"]) > 0
    return result


# ---------------------------------------------------------------------------
# Happy-path resolution tests against the real kernel
# ---------------------------------------------------------------------------

class TestHappyPath:
    """Successful resolution for known valid actor/workflow/mode combos."""

    def test_terminal_agent_issue_implementation(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        resolved = result["resolved"]

        # Actor is fully expanded.
        assert resolved["actor"]["id"] == "actor.terminal_agent"
        assert resolved["actor"]["surface"] == "terminal"
        assert "capabilities" in resolved["actor"]

        # Workflow is fully expanded.
        assert resolved["workflow"]["id"] == "workflow.issue_implementation"
        assert "steps" in resolved["workflow"]
        assert "required_evidence_refs" in resolved["workflow"]

        # Mode is fully expanded.
        assert resolved["execution_mode"]["id"] == "mode.delegated_commit_pr"
        assert "allowed_actions" in resolved["execution_mode"]
        assert "prohibited_actions" in resolved["execution_mode"]

        # Evidence is expanded from workflow + mode union.
        assert "evidence.issue_scope" in resolved["evidence"]
        assert "evidence.branch_preflight" in resolved["evidence"]
        assert "evidence.pm_approval" in resolved["evidence"]
        assert "evidence.validation_output" in resolved["evidence"]
        # Each evidence entry is fully expanded, not just a ref.
        for eid, entry in resolved["evidence"].items():
            assert entry["id"] == eid
            assert "satisfied_by" in entry

        # Outputs are expanded from workflow allowed_output_refs.
        assert "output.execution_report" in resolved["outputs"]
        for oid, entry in resolved["outputs"].items():
            assert entry["id"] == oid
            assert "use_for" in entry

        # Boundaries are expanded from actor boundary_refs.
        assert len(resolved["boundaries"]) > 0
        for bid, entry in resolved["boundaries"].items():
            assert entry["id"] == bid
            assert "rule" in entry

        # Non-authorization notice is present.
        assert "non_authorization" in result
        assert "operative task guidance" in result["non_authorization"]
        assert "never grants" in result["non_authorization"]

        guidance = result["operative_guidance"]
        assert guidance["role"] == "operative_task_guidance"
        assert "not merely informational context" in guidance["summary"]
        assert "workflow.issue_implementation" in " ".join(guidance["must_follow"])
        assert "mode.delegated_commit_pr" in " ".join(guidance["must_follow"])
        assert "operative task guidance" in guidance["authorization"]
        assert "never grants" in guidance["authorization"]

        traceability = result["live_traceability"]
        assert traceability["status"] == "required_preflight"
        assert traceability["resolver_role"] == "emit_obligations_only_no_github_or_git_fetch"
        assert traceability["protocol_ref"] == "docs/TRACEABILITY_PROTOCOL.md"
        assert "Before edits" in traceability["before_actions"]
        reads = " ".join(traceability["required_live_reads"])
        assert "current GitHub issue or PR live" in reads
        assert "local git branch" in reads
        assert "linked PRs live" in reads
        assert "canonical roadmap issue" in reads
        assert "docs/decisions ADRs" in reads
        assert "memory" in traceability["state_policy"]
        assert "durable files" in traceability["state_policy"]

    def test_browser_chat_review_before_close(self) -> None:
        result = _resolve_ok(
            "actor.browser_chat",
            "workflow.review_before_close",
            "mode.review_only",
        )
        resolved = result["resolved"]
        assert resolved["actor"]["id"] == "actor.browser_chat"
        assert resolved["workflow"]["id"] == "workflow.review_before_close"
        assert resolved["execution_mode"]["id"] == "mode.review_only"

        # Browser chat boundaries should include draft_only_browser.
        assert "boundary.draft_only_browser" in resolved["boundaries"]

        traceability = result["live_traceability"]
        assert "Before non-trivial analysis" in traceability["before_actions"]
        reads = " ".join(traceability["required_live_reads"])
        assert "linked issue objective" in reads
        assert "PR body, comments, reviews" in reads
        assert "real diff" in reads
        assert "code/diff/check evidence" in reads

    def test_pm_intake_traceability_is_visible(self) -> None:
        result = _resolve_ok(
            "actor.browser_chat",
            "workflow.pm_intake",
            "mode.review_only",
        )

        traceability = result["live_traceability"]
        assert traceability["status"] == "required_preflight"
        reads = " ".join(traceability["required_live_reads"])
        assert "source-basis issues" in reads
        assert "roadmap evidence" in reads
        assert "relevant ADRs" in reads
        assert "single evidence-backed next outcome" in reads
        assert "no_github_or_git_fetch" in traceability["resolver_role"]
        assert "durable files" in traceability["state_policy"]

    def test_browser_chat_manual_implementation_plan_is_review_only(self) -> None:
        result = _resolve_ok(
            "actor.browser_chat",
            "workflow.issue_implementation_manual",
            "mode.review_only",
        )
        resolved = result["resolved"]
        effective_refs = resolved["effective"]["effective_evidence_refs"]

        assert resolved["actor"]["id"] == "actor.browser_chat"
        assert resolved["workflow"]["id"] == "workflow.issue_implementation_manual"
        assert resolved["execution_mode"]["id"] == "mode.review_only"
        assert "output.manual_implementation_plan" in resolved["outputs"]
        assert "boundary.draft_only_browser" in resolved["boundaries"]
        assert "evidence.issue_scope" in effective_refs
        assert "evidence.source_basis" in effective_refs
        assert "evidence.repo_state" in effective_refs
        assert "evidence.branch_preflight" not in effective_refs
        assert "evidence.pm_approval" not in effective_refs

    def test_terminal_agent_review_only(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.review_only",
            "mode.review_only",
        )
        resolved = result["resolved"]
        assert resolved["actor"]["id"] == "actor.terminal_agent"
        assert resolved["execution_mode"]["id"] == "mode.review_only"

    def test_terminal_agent_local_implementation(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.local_implementation",
        )
        assert result["resolved"]["execution_mode"]["id"] == "mode.local_implementation"

    def test_human_pm_has_no_agent_modes(self) -> None:
        """Human PM has no allowed_mode_refs (not an agent surface)."""
        result = _resolve_error(
            "actor.human_pm", "workflow.review_only", "mode.review_only"
        )
        assert any("not in actor" in e for e in result["errors"])


class TestDeploymentResolution:
    """#376: internal deploy execution resolves only for the terminal agent."""

    def test_terminal_agent_deployment_resolves(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.deployment",
            "mode.delegated_deploy_execution",
        )
        resolved = result["resolved"]
        assert resolved["workflow"]["id"] == "workflow.deployment"
        assert resolved["execution_mode"]["id"] == "mode.delegated_deploy_execution"
        # The deploy mode runs target-owned commands but never edits the repo.
        actions = set(resolved["execution_mode"]["allowed_actions"])
        assert "run_target_owned_deploy_commands" in actions
        assert "edit_scoped_files" not in actions
        assert "commit" not in actions
        # Gated by exact approval, adoption, readiness, and validation evidence.
        for eid in (
            "evidence.pm_approval",
            "evidence.target_adoption",
            "evidence.deployment_readiness",
            "evidence.validation_output",
        ):
            assert eid in resolved["evidence"]

    def test_browser_chat_cannot_deploy(self) -> None:
        result = _resolve_error(
            "actor.browser_chat",
            "workflow.deployment",
            "mode.delegated_deploy_execution",
        )
        assert any("not in actor" in e for e in result["errors"])

    def test_deploy_workflow_refuses_read_only_mode(self) -> None:
        """workflow.deployment requires PM approval, so a read-only mode is refused."""
        result = _resolve_error(
            "actor.terminal_agent",
            "workflow.deployment",
            "mode.review_only",
        )
        assert any("read-only" in e for e in result["errors"])


# ---------------------------------------------------------------------------
# Effective resolution tests
# ---------------------------------------------------------------------------

class TestEffective:
    """Tests for the effective resolution summary."""

    def test_effective_evidence_is_union(self) -> None:
        """Evidence should be the union of workflow + mode refs."""
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        effective = result["resolved"]["effective"]
        refs = effective["effective_evidence_refs"]
        # Both workflow and mode require these.
        assert "evidence.issue_scope" in refs
        assert "evidence.branch_preflight" in refs
        assert "evidence.pm_approval" in refs
        assert "evidence.validation_output" in refs

    def test_effective_evidence_deduplicates(self) -> None:
        """Overlapping evidence refs should appear only once."""
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        refs = result["resolved"]["effective"]["effective_evidence_refs"]
        assert len(refs) == len(set(refs))

    def test_effective_allowed_actions(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        effective = result["resolved"]["effective"]
        assert "read" in effective["effective_allowed_actions"]
        assert "open_draft_pr" in effective["effective_allowed_actions"]

    def test_effective_prohibited_actions_include_actor_denied(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        effective = result["resolved"]["effective"]
        # Actor denied_actions should appear in effective prohibited.
        assert "merge" in effective["effective_prohibited_actions"]
        assert "close_issue" in effective["effective_prohibited_actions"]

    def test_missing_evidence_statuses(self) -> None:
        """Each evidence entry should list its missing_status for awareness."""
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        missing = result["resolved"]["effective"]["missing_evidence_statuses"]
        # pm_approval should have status.blocked as missing status.
        pm_entry = next(
            (e for e in missing if e["evidence_id"] == "evidence.pm_approval"),
            None,
        )
        assert pm_entry is not None
        assert pm_entry["missing_status"] == "status.blocked"

    def test_effective_boundaries_include_global(self) -> None:
        """Effective boundaries should include global/hard boundaries."""
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        effective = result["resolved"]["effective"]
        # boundary.fail_closed is a global boundary, not specifically
        # in actor.terminal_agent's boundary_refs.
        assert "boundary.fail_closed" in effective["effective_boundary_refs"]
        # And actor's specific boundaries should also be there.
        assert "boundary.no_main_edits" in effective["effective_boundary_refs"]

    def test_unresolved_actor_capabilities(self) -> None:
        """Effective summary should report unresolved actor capabilities."""
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        effective = result["resolved"]["effective"]
        assert "edit_scoped_files" in effective["unresolved_actor_capabilities"]

# ---------------------------------------------------------------------------
# Error case: unknown selectors
# ---------------------------------------------------------------------------

class TestUnknownSelectors:
    """Tests for unknown actor/workflow/mode selectors."""

    def test_unknown_actor(self) -> None:
        result = _resolve_error(
            "actor.does_not_exist",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        assert any("actor.does_not_exist" in e for e in result["errors"])

    def test_unknown_workflow(self) -> None:
        result = _resolve_error(
            "actor.terminal_agent",
            "workflow.does_not_exist",
            "mode.delegated_commit_pr",
        )
        assert any("workflow.does_not_exist" in e for e in result["errors"])

    def test_unknown_mode(self) -> None:
        result = _resolve_error(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.does_not_exist",
        )
        assert any("mode.does_not_exist" in e for e in result["errors"])

    def test_all_unknown(self) -> None:
        result = _resolve_error(
            "actor.nope",
            "workflow.nope",
            "mode.nope",
        )
        # Should report errors for all three.
        assert len(result["errors"]) == 3


# ---------------------------------------------------------------------------
# Error case: incompatible combos
# ---------------------------------------------------------------------------

class TestIncompatibleCombos:
    """Tests for valid selectors that are incompatible."""

    def test_browser_chat_cannot_use_delegated_commit_pr(self) -> None:
        """Browser chat only allows mode.review_only."""
        result = _resolve_error(
            "actor.browser_chat",
            "workflow.review_only",
            "mode.delegated_commit_pr",
        )
        assert any("not in actor" in e for e in result["errors"])
        assert any("browser_chat" in e for e in result["errors"])

    def test_unknown_actor_cannot_use_write_mode(self) -> None:
        """actor.unknown only allows mode.review_only."""
        result = _resolve_error(
            "actor.unknown",
            "workflow.review_only",
            "mode.local_implementation",
        )
        assert any("not in actor" in e for e in result["errors"])

    def test_terminal_agent_issue_implementation_review_only(self) -> None:
        """Write-capable workflow is incompatible with read-only mode."""
        result = _resolve_error(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.review_only",
        )
        assert any("requires write capabilities" in e for e in result["errors"])

# ---------------------------------------------------------------------------
# Kernel loading error tests
# ---------------------------------------------------------------------------

class TestKernelLoadErrors:
    """Tests for missing or malformed kernel files."""

    def test_missing_kernel_dir(self, tmp_path: Path) -> None:
        result = resolve(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
            kernel_dir=tmp_path / "nonexistent",
        )
        assert result["status"] == "error"
        assert any("not found" in e for e in result["errors"])

    def test_missing_manifest(self, tmp_path: Path) -> None:
        kernel = tmp_path / "kernel_nomanifest"
        kernel.mkdir()
        result = resolve(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
            kernel_dir=kernel,
        )
        assert result["status"] == "error"
        assert any("manifest" in e for e in result["errors"])

    def test_malformed_manifest(self, tmp_path: Path) -> None:
        kernel = tmp_path / "kernel_bad"
        kernel.mkdir()
        (kernel / "manifest.json").write_text("{invalid json", encoding="utf-8")
        result = resolve(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
            kernel_dir=kernel,
        )
        assert result["status"] == "error"
        assert any("invalid" in e.lower() for e in result["errors"])

    def test_missing_kernel_file_in_load_order(self, tmp_path: Path) -> None:
        """Manifest references a file that doesn't exist."""
        kernel = tmp_path / "kernel_partial"
        kernel.mkdir()
        manifest = {
            "id": "kernel.manifest",
            "family": "manifest",
            "kernel_version": "test",
            "load_order": ["actors.json", "missing_file.json"],
            "non_authorization": "test",
            "size_budget": {"kernel_total_bytes_max": 100000},
        }
        (kernel / "manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        actors = {
            "id": "kernel.actors",
            "family": "actors",
            "entries": [
                {
                    "id": "actor.test",
                    "surface": "terminal",
                    "summary": "test",
                    "capabilities": [],
                    "allowed_mode_refs": [],
                    "boundary_refs": [],
                }
            ],
        }
        (kernel / "actors.json").write_text(
            json.dumps(actors), encoding="utf-8"
        )
        result = resolve(
            "actor.test",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
            kernel_dir=kernel,
        )
        assert result["status"] == "error"
        assert any("missing_file.json" in e for e in result["errors"])


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

class TestCLI:
    """Tests for the CLI entry point (main function)."""

    def test_happy_path_exit_0(self, capsys) -> None:
        exit_code = main([
            "--actor", "actor.terminal_agent",
            "--workflow", "workflow.issue_implementation",
            "--mode", "mode.delegated_commit_pr",
            "--kernel-dir", str(KERNEL_DIR),
        ])
        assert exit_code == 0
        output = json.loads(capsys.readouterr().out)
        assert output["status"] == "ok"

    def test_error_exit_1(self, capsys) -> None:
        exit_code = main([
            "--actor", "actor.fake",
            "--workflow", "workflow.issue_implementation",
            "--mode", "mode.delegated_commit_pr",
            "--kernel-dir", str(KERNEL_DIR),
        ])
        assert exit_code == 1
        output = json.loads(capsys.readouterr().out)
        assert output["status"] == "error"

    def test_compact_output(self, capsys) -> None:
        exit_code = main([
            "--actor", "actor.terminal_agent",
            "--workflow", "workflow.review_only",
            "--mode", "mode.review_only",
            "--kernel-dir", str(KERNEL_DIR),
            "--compact",
        ])
        assert exit_code == 0
        raw = capsys.readouterr().out
        # Compact output should be a single line (no indentation).
        assert "\n" not in raw.strip()

    def test_missing_kernel_dir_exit_1(self, capsys) -> None:
        exit_code = main([
            "--actor", "actor.terminal_agent",
            "--workflow", "workflow.issue_implementation",
            "--mode", "mode.delegated_commit_pr",
            "--kernel-dir", "/nonexistent/path",
        ])
        assert exit_code == 1


# ---------------------------------------------------------------------------
# Output structure integrity
# ---------------------------------------------------------------------------

class TestOutputStructure:
    """Tests that output JSON has the expected structure."""

    def test_ok_result_keys(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.review_only",
            "mode.review_only",
        )
        assert set(result.keys()) == {
            "resolved",
            "status",
            "errors",
            "operative_guidance",
            "live_traceability",
            "non_authorization",
        }

    def test_resolved_keys(self) -> None:
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.review_only",
            "mode.review_only",
        )
        expected_keys = {
            "actor", "workflow", "execution_mode",
            "evidence", "outputs", "boundaries", "effective",
        }
        assert set(result["resolved"].keys()) == expected_keys

    def test_error_result_keys(self) -> None:
        result = _resolve_error(
            "actor.fake",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        assert "resolved" in result
        assert "status" in result
        assert "errors" in result

    def test_result_is_json_serializable(self) -> None:
        """Ensure the result can be serialized to JSON without error."""
        result = _resolve_ok(
            "actor.terminal_agent",
            "workflow.issue_implementation",
            "mode.delegated_commit_pr",
        )
        serialized = json.dumps(result)
        assert isinstance(serialized, str)
        roundtrip = json.loads(serialized)
        assert roundtrip["status"] == "ok"
