"""Workflow, boundary, output, and route-prompt behavior guards."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_ACTOR_IDS = {
    "actor.human_pm",
    "actor.terminal_agent",
    "actor.browser_chat",
    "actor.unknown",
}


def _kernel_entry(file_name: str, entry_id: str) -> dict:
    data = json.loads((REPO_ROOT / "kernel" / file_name).read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry["id"] == entry_id:
            return entry
    raise AssertionError(f"{entry_id} not found in {file_name}")


def _operation_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_browser_activation_uses_kernel_owned_references() -> None:
    text = (REPO_ROOT / "adapters" / "BROWSER_CHAT.target.md").read_text(encoding="utf-8")
    block = text.split("~~~text", 1)[1].split("~~~", 1)[0]

    assert "kernel/manifest.json in REPOSITORY_NAME" not in block
    assert "mark the output pending" not in block
    assert "KERNEL_REPOSITORY's `kernel/manifest.json`" in block
    assert "KERNEL_REPOSITORY's `docs/TRACEABILITY_PROTOCOL.md`" in block
    assert "KERNEL_REPOSITORY's `templates/route-prompt.md`" in block
    assert re.search(r"KERNEL_REPOSITORY's\s+`templates/pm-command-bundle\.md`", block)
    assert "`status.needs_context`" in block


def test_review_before_close_requires_code_backed_kernel_evidence() -> None:
    boundary = _kernel_entry("boundaries.json", "boundary.review_before_close")
    workflow = _kernel_entry("workflows.json", "workflow.review_before_close")
    evidence = _kernel_entry("evidence.json", "evidence.pr_diff")
    review_output = _kernel_entry("outputs.json", "output.review_result")
    closure_output = _kernel_entry("outputs.json", "output.closure_comment")

    boundary_rule = boundary["rule"].lower()
    assert "linked issue objective, scope, out-of-scope, and acceptance criteria" in boundary_rule
    assert "pr body, comments, and reports are claims/evidence leads, not proof" in boundary_rule
    assert "code/diff/final-file evidence cannot be inspected" in boundary_rule
    assert "no closure comment is drafted" in boundary_rule

    workflow_steps = " ".join(workflow["steps"]).lower()
    assert "changed-file list" in workflow_steps
    assert "pr diff" in workflow_steps
    assert "relevant final head files" in workflow_steps
    assert "compare implementation behavior and validation" in workflow_steps
    assert "return status.needs_context instead of go" in workflow_steps

    pr_diff_rule = evidence["satisfied_by"].lower()
    assert "changed-file list and diff" in pr_diff_rule
    assert "final head file content" in pr_diff_rule
    assert "terminal-agent reports" in pr_diff_rule
    assert "not proof of implementation" in pr_diff_rule
    assert "status.needs_context instead of go" in pr_diff_rule

    assert (
        "implementation comparison mapping issue objective/scope/out-of-scope/acceptance criteria to code evidence"
        in review_output["required_sections"]
    )
    assert "documentation-only review" in review_output["rule"].lower()
    assert "not go" in review_output["rule"].lower()
    assert "draft it only after code-backed review" in closure_output["rule"].lower()


def test_implementation_discipline_boundary_is_compact_and_scoped() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    boundary = _kernel_entry("boundaries.json", "boundary.implementation_discipline")
    issue_workflow = _kernel_entry("workflows.json", "workflow.issue_implementation")
    review_workflow = _kernel_entry("workflows.json", "workflow.review_before_close")
    execution_output = _kernel_entry("outputs.json", "output.execution_report")
    review_output = _kernel_entry("outputs.json", "output.review_result")

    assert {entry["id"] for entry in actors["entries"]} == CANONICAL_ACTOR_IDS
    terminal_agent = next(entry for entry in actors["entries"] if entry["id"] == "actor.terminal_agent")
    non_terminal_refs = {
        entry["id"]: entry.get("boundary_refs", [])
        for entry in actors["entries"]
        if entry["id"] != "actor.terminal_agent"
    }
    assert "boundary.implementation_discipline" in terminal_agent["boundary_refs"]
    assert all("boundary.implementation_discipline" not in refs for refs in non_terminal_refs.values())

    rule = boundary["rule"].lower()
    notes = boundary["notes"].lower()
    assert boundary["on_violation"] == "status.blocked"
    assert len(rule) < 800
    assert len(notes) < 400
    assert "complete change" in rule
    assert "satisfies the live issue scope" in rule
    assert "complete means" in rule
    assert "required behavior, validation, error handling, integration points, and tests" in rule
    assert "minimalism never permits missing required work" in rule
    assert "responsibilities separated" in rule
    assert "source of truth" in rule
    assert "duplicated logic unless explicitly justified" in rule
    assert "direct simple structure" in rule
    assert "speculative abstraction" in rule
    for forbidden in (
        "unrelated rewrites",
        "over-correction",
        "over-implementation",
        "scope expansion",
    ):
        assert forbidden in rule
    for review_example in (
        "duplicated logic introduced by the pr",
        "mixed responsibilities",
        "unnecessary monoliths",
        "speculative abstractions",
        "under-implementation disguised as minimalism",
    ):
        assert review_example in notes

    issue_steps = " ".join(issue_workflow["steps"]).lower()
    review_steps = " ".join(review_workflow["steps"]).lower()
    assert "boundary.implementation_discipline" in issue_steps
    assert "boundary.implementation_discipline" in review_steps
    assert "implementation-discipline violations when relevant" in review_steps
    assert "speculative abstractions" not in review_steps
    assert "unrelated rewrites" not in review_steps
    assert "implementation-discipline note when relevant" in execution_output["required_sections"]
    assert "implementation-discipline findings when relevant" in review_output["required_sections"]


def test_primary_path_discipline_boundary_is_compact_and_scoped() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    boundary = _kernel_entry("boundaries.json", "boundary.primary_path_discipline")
    impl_boundary = _kernel_entry("boundaries.json", "boundary.implementation_discipline")
    issue_workflow = _kernel_entry("workflows.json", "workflow.issue_implementation")
    review_workflow = _kernel_entry("workflows.json", "workflow.review_before_close")
    audit_workflow = _kernel_entry("workflows.json", "workflow.implementation_discipline_audit")

    rule = boundary["rule"].lower()
    assert boundary["on_violation"] == "status.blocked"
    # Keep it compact and non-duplicative: no notes field unless it adds non-duplicative context.
    assert "notes" not in boundary
    assert len(rule) < 600
    assert "primary path correct, explicit, and validated" in rule
    assert "hide, bypass, normalize, or avoid investigating errors" in rule
    assert "investigate and fix the root cause" in rule
    assert "real alternate path, graceful degradation, or compatibility behavior" in rule
    assert "preserve correctness and be validated when in scope" in rule

    # Must not duplicate or bloat boundary.implementation_discipline.
    assert "primary path" not in impl_boundary["rule"].lower()
    assert "fallback" not in impl_boundary["rule"].lower()
    assert "fallback" not in impl_boundary["notes"].lower()
    # No broad reliability manifesto: stay focused on primary-path vs fallback.
    for manifesto_term in ("reliability", "resilien", "retry", "circuit breaker", "availability"):
        assert manifesto_term not in rule

    # terminal_agent inherits it; no other actor does (it is write-capable only).
    terminal_agent = next(entry for entry in actors["entries"] if entry["id"] == "actor.terminal_agent")
    non_terminal_refs = [
        entry.get("boundary_refs", [])
        for entry in actors["entries"]
        if entry["id"] != "actor.terminal_agent"
    ]
    assert "boundary.primary_path_discipline" in terminal_agent["boundary_refs"]
    assert all("boundary.primary_path_discipline" not in refs for refs in non_terminal_refs)

    issue_steps = " ".join(issue_workflow["steps"]).lower()
    review_steps = " ".join(review_workflow["steps"]).lower()
    audit_text = " ".join([audit_workflow["use_for"], *audit_workflow["steps"]]).lower()
    assert "boundary.primary_path_discipline" in issue_steps
    assert "boundary.primary_path_discipline" in review_steps
    assert "unjustified fallback paths" in review_steps
    assert "boundary.primary_path_discipline" in audit_text
    assert "fallback abuse" in audit_text


def test_validation_discipline_boundary_is_compact_and_scoped() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    boundary = _kernel_entry("boundaries.json", "boundary.validation_discipline")
    impl_boundary = _kernel_entry("boundaries.json", "boundary.implementation_discipline")
    primary_boundary = _kernel_entry("boundaries.json", "boundary.primary_path_discipline")
    issue_workflow = _kernel_entry("workflows.json", "workflow.issue_implementation")
    review_workflow = _kernel_entry("workflows.json", "workflow.review_before_close")
    audit_workflow = _kernel_entry("workflows.json", "workflow.implementation_discipline_audit")
    execution_output = _kernel_entry("outputs.json", "output.execution_report")

    rule = boundary["rule"].lower()
    assert boundary["on_violation"] == "status.blocked"
    # Keep it compact and non-duplicative: no notes field; flagging language lives in workflows.
    assert "notes" not in boundary
    assert len(rule) < 700

    # Proportional automated tests, preserved for deterministic/regression/contract risk.
    assert "proportional validation" in rule
    assert "add or update automated tests" in rule
    assert (
        "deterministic behavior, regression risk, security/privacy boundaries, protocol contracts, "
        "billing/storage logic, routing, or stable ui state contracts" in rule
    )
    # No confidence theater.
    assert "broad, duplicated, brittle, or implementation-detail tests merely to create confidence theater" in rule
    # Distinguish automated validation from manual PM/user validation.
    assert "ux feel" in rule
    assert "ambiguous pm preference" in rule
    assert "report the required manual validation instead of pretending automated tests prove it" in rule

    # No broad QA/testing manifesto: stay focused on proportional validation, not a strategy doc.
    for manifesto_term in ("coverage", "test pyramid", "test strategy", "linter", "static analysis", "qa framework"):
        assert manifesto_term not in rule

    # Must not duplicate or bloat the sibling discipline boundaries.
    assert "proportional validation" not in impl_boundary["rule"].lower()
    assert "confidence theater" not in impl_boundary["rule"].lower()
    assert "confidence theater" not in impl_boundary["notes"].lower()
    assert "proportional validation" not in primary_boundary["rule"].lower()
    assert "confidence theater" not in primary_boundary["rule"].lower()

    # terminal_agent inherits it; no other actor does (it is write-capable only).
    assert {entry["id"] for entry in actors["entries"]} == CANONICAL_ACTOR_IDS
    terminal_agent = next(entry for entry in actors["entries"] if entry["id"] == "actor.terminal_agent")
    non_terminal_refs = [
        entry.get("boundary_refs", [])
        for entry in actors["entries"]
        if entry["id"] != "actor.terminal_agent"
    ]
    assert "boundary.validation_discipline" in terminal_agent["boundary_refs"]
    assert all("boundary.validation_discipline" not in refs for refs in non_terminal_refs)

    # Applied in issue_implementation; flaggable in review; auditable in the discipline audit.
    issue_steps = " ".join(issue_workflow["steps"]).lower()
    review_steps = " ".join(review_workflow["steps"]).lower()
    audit_text = " ".join([audit_workflow["use_for"], *audit_workflow["steps"]]).lower()
    assert "boundary.validation_discipline" in issue_steps
    assert "boundary.validation_discipline" in review_steps
    assert "confidence-theater tests" in review_steps
    assert "missing manual-validation reporting" in review_steps
    assert "boundary.validation_discipline" in audit_text
    assert "validation overreach or missing manual-validation reporting" in audit_text

    # Execution report distinguishes automated vs manual validation and accepted exceptions,
    # without duplicating the boundary text.
    sections = execution_output["required_sections"]
    validation_section = next(section for section in sections if "validation performed" in section)
    assert "automated validation with results" in validation_section
    assert "validation not run and why" in validation_section
    assert "manual PM/user validation required" in validation_section
    assert "accepted validation exceptions" in validation_section


def test_review_before_close_route_template_rejects_documentation_only_go() -> None:
    text = (REPO_ROOT / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    review_variant = text.split("**Review a PR before merge/close**", 1)[1].split(
        "- **Apply review corrections**", 1
    )[0]
    compact = " ".join(review_variant.split())

    assert "PR body/comments/reports only as claims" in review_variant
    assert "inspect changed files, PR diff" in review_variant
    assert "relevant final head files" in review_variant
    assert "Compare implementation behavior against issue objective/scope/out-of-scope/acceptance" in compact
    assert "return `status.needs_context`, not GO" in review_variant
    assert "explicit not-reviewed gaps" in compact


def test_design_asset_workflow_routes_to_prompt_without_write_authority() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    workflow = _kernel_entry("workflows.json", "workflow.design_asset")
    output = _kernel_entry("outputs.json", "output.asset_prompt")

    assert {entry["id"] for entry in actors["entries"]} == CANONICAL_ACTOR_IDS
    workflow_text = " ".join([workflow["use_for"], *workflow["steps"]]).lower()
    assert "recipient is not an actor surface" in workflow_text
    assert "creates no asset files" in workflow_text
    assert "read the current issue" in workflow_text
    assert "needed assets" in workflow_text
    assert "dimension" in workflow_text
    assert "accessibility" in workflow_text
    assert "file-format" in workflow_text
    assert "target product and design truth" in workflow_text
    assert "do not generate images" in workflow_text
    assert "create binary assets" in workflow_text
    assert workflow["allowed_output_refs"] == ["output.asset_prompt", "output.status_result"]

    sections = output["required_sections"]
    assert "recipient and non-actor decision" in sections
    assert "dimensions, format, and delivery constraints" in sections
    assert "brand/style/product constraints from target truth" in sections
    assert "accessibility notes" in sections
    assert "out of scope and authority limits" in sections
    assert "grants no write authority" in output["rule"].lower()
    assert "target product/design truth stays in the target repository" in output["rule"]


def test_security_revision_workflow_routes_to_owasp_prompt_without_secret_exposure() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    workflow = _kernel_entry("workflows.json", "workflow.security_revision")
    output = _kernel_entry("outputs.json", "output.security_review_prompt")

    assert {entry["id"] for entry in actors["entries"]} == CANONICAL_ACTOR_IDS
    workflow_text = " ".join([workflow["use_for"], *workflow["steps"]]).lower()
    assert "recipient is not an actor surface" in workflow_text
    assert "runs no scanner" in workflow_text
    assert "without exposing secrets" in workflow_text
    for area in (
        "auth",
        "authorization",
        "sessions/cookies",
        "input validation",
        "file uploads",
        "redirects",
        "dependencies",
        "admin paths",
        "secrets handling",
        "logging",
        "error exposure",
        "deployment/config risk",
    ):
        assert area in workflow_text
    for forbidden in (
        "print",
        "paste",
        "upload",
        "quote",
        "summarize",
        ".env",
        "jwt secrets",
        "database urls",
        "session tokens",
        "ci secrets",
        "hidden environment values",
    ):
        assert forbidden in workflow_text
    assert workflow["allowed_output_refs"] == ["output.security_review_prompt", "output.status_result"]

    sections = output["required_sections"]
    assert "recipient and non-actor decision" in sections
    assert "security-sensitive surfaces" in sections
    assert "OWASP areas to inspect" in sections
    assert "secret redaction requirements" in sections
    assert "out of scope and authority limits" in sections
    assert "grants no write authority" in output["rule"].lower()
    assert "runs no scanner" in output["rule"].lower()
    assert "hidden environment values" in output["rule"].lower()


def test_design_and_security_route_template_variants_are_draft_only() -> None:
    text = (REPO_ROOT / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    design_variant = text.split("**Design asset prompt**", 1)[1].split(
        "- **Security review prompt**", 1
    )[0]
    security_variant = text.split("**Security review prompt**", 1)[1].split(
        "- **Apply review corrections**", 1
    )[0]

    assert "`WORKFLOW = workflow.design_asset`" in design_variant
    assert "`OUTPUT_CONTRACT = output.asset_prompt`" in design_variant
    assert "graphic/design specialist is a recipient, not an actor" in design_variant
    assert "Do not generate or commit assets" in design_variant
    assert "Project OS owns target product/design truth" in design_variant

    assert "`WORKFLOW = workflow.security_revision`" in security_variant
    assert "`OUTPUT_CONTRACT = output.security_review_prompt`" in security_variant
    assert "security specialist is a recipient/focus, not an actor" in security_variant
    assert "OWASP-based prompt" in security_variant
    assert "Require redaction" in security_variant
    assert "never ask" in security_variant
    assert "hidden environment values" in security_variant


def test_target_adoption_kernel_guards_audit_draft_and_bootstrap_paths() -> None:
    workflow = _kernel_entry("workflows.json", "workflow.target_adoption")
    evidence = _kernel_entry("evidence.json", "evidence.target_adoption")
    output = _kernel_entry("outputs.json", "output.adoption_packet")
    delegated_pr = _kernel_entry("execution_modes.json", "mode.delegated_commit_pr")

    steps = " ".join(workflow["steps"]).lower()
    assert workflow["required_evidence_refs"] == ["evidence.target_adoption"]
    assert "inspect target adoption state first" in steps
    assert "agents.md" in steps
    assert "claude.md" in steps
    assert "gemini.md" in steps
    assert "browser-chat adapter" in steps
    assert "audit them against kernel_repository adapters/*.target.md" in steps
    assert "tools.audit_target_adapters" in steps
    assert "protected overlay removal risk" in steps
    assert "without overwriting target-owned notes" in steps
    assert "mode.review_only" in steps
    assert "draft adapter content and checklist only" in steps
    assert "do not edit files or mutate git/github" in steps
    assert "mode.delegated_commit_pr" in steps
    assert "exact pm approval" in steps
    assert "create only agents.md, claude.md, and gemini.md" in steps
    assert "adapter-only diff" in steps
    assert "no product code" in steps
    assert "secret-store authority" in steps

    evidence_text = evidence["satisfied_by"].lower()
    assert "agents.md/claude.md/gemini.md/browser-chat adapter presence" in evidence_text
    assert "project notes" in evidence_text
    assert "validation commands" in evidence_text
    assert "audit findings" in evidence_text

    assert "evidence.branch_preflight" in delegated_pr["required_evidence_refs"]
    assert "evidence.pm_approval" in delegated_pr["required_evidence_refs"]
    assert "evidence.validation_output" in delegated_pr["required_evidence_refs"]

    sections = output["required_sections"]
    assert "current adoption state" in sections
    assert "files missing/present" in sections
    assert "audit findings" in sections
    assert "exact write scope when applicable" in sections
    assert any("security/domain constraints" in section for section in sections)


def test_target_adoption_route_template_is_draft_or_adapter_only() -> None:
    text = (REPO_ROOT / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    variant = text.split("**Adopt target repository**", 1)[1].split(
        "- **Review a PR before merge/close**", 1
    )[0]
    compact = " ".join(variant.split())

    assert "`WORKFLOW = workflow.target_adoption`" in variant
    assert "`EXECUTION_MODE = mode.review_only | mode.delegated_commit_pr`" in variant
    assert "`EVIDENCE_REQUIRED = evidence.target_adoption` for review-only" in variant
    assert "evidence.branch_preflight" in variant
    assert "evidence.pm_approval" in variant
    assert "evidence.validation_output" in variant
    assert "for delegated_commit_pr" in variant
    assert "inspect TARGET_REPOSITORY first" in variant
    assert "whether `AGENTS.md` exists" in variant
    assert "whether `CLAUDE.md` exists" in variant
    assert "whether `GEMINI.md`" in variant
    assert "whether a browser-chat" in variant
    assert "adapter was supplied" in variant
    assert "audit/compare them against KERNEL_REPOSITORY's" in variant
    assert "`tools.audit_target_adapters`" in variant
    assert "preserve target-owned notes, security/domain constraints, and validation commands" in compact
    assert "review-only drafts only" in variant
    assert "may create only `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`" in compact
    assert "open a draft PR" in compact
    assert "Browser chat remains draft-only" in compact
    assert "Do not merge, close, label" in variant
    assert "touch secrets" in variant


def test_route_prompt_pm_authorization_status_choices_are_two_option_authority_values() -> None:
    text = (REPO_ROOT / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    variable_block = text.split("~~~text", 1)[1].split("~~~", 1)[0]

    assert (
        "PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}"
        in variable_block
    )
    assert "That status does not bypass required evidence" in text
    assert "branch preflight, validation, or\nfail-closed behavior" in text

    status_line = next(
        line for line in variable_block.splitlines() if line.startswith("PM_AUTHORIZATION_STATUS")
    )
    for invalid_value in (
        "draft",
        "read-only planning",
        "read_only",
        "planning",
        "approved",
        "{{granted |",
        "| granted}}",
    ):
        assert invalid_value not in status_line


def test_artifact_templates_mark_review_claims_and_closure_precondition() -> None:
    text = (REPO_ROOT / "templates" / "artifacts.md").read_text(encoding="utf-8")
    pull_request = text.split("## Pull request", 1)[1].split("## Closure comment", 1)[0]
    closure_comment = text.split("## Closure comment", 1)[1].split("~~~markdown", 1)[0]

    assert "records claims and validation leads" in pull_request
    assert "not proof of implementation" in pull_request
    assert "changed files, PR diff, and relevant final head files" in pull_request

    assert "Draft this from `workflow.review_before_close` only after" in closure_comment
    assert "linked issue objective, scope, out-of-scope, and acceptance criteria" in closure_comment
    assert "PR changed files, diff, and relevant final head files" in closure_comment
    assert "claims/evidence leads, not proof" in closure_comment
