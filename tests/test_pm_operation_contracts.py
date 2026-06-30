"""PM operation template and catalog contract guards."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

KERNEL_ID_PATTERN = re.compile(
    r"\b(?:status|actor|mode|boundary|evidence|workflow|output)\."
    r"(?!json\b|get\b|append\b)[A-Za-z0-9_*]+"
)
LIVE_GITHUB_OBJECT_PATTERN = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/(?:issues|pull)/\d+")
SECRET_LOOKING_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
CANONICAL_KERNEL_ENTRY_IDS = {
    "actors.json": {
        "actor.human_pm",
        "actor.terminal_agent",
        "actor.browser_chat",
        "actor.unknown",
    },
    "execution_modes.json": {
        "mode.review_only",
        "mode.local_implementation",
        "mode.delegated_commit_push",
        "mode.delegated_commit_pr",
    },
    "statuses.json": {
        "status.resolved",
        "status.needs_context",
        "status.needs_pm_decision",
        "status.blocked",
    },
    "boundaries.json": {
        "boundary.branch_preflight",
        "boundary.no_main_edits",
        "boundary.draft_only_browser",
        "boundary.separate_pm_approval",
        "boundary.review_before_close",
        "boundary.no_live_state_durable",
        "boundary.no_invented_state",
        "boundary.security_privacy",
        "boundary.fail_closed",
        "boundary.output_not_permission",
        "boundary.implementation_discipline",
        "boundary.primary_path_discipline",
        "boundary.validation_discipline",
        "boundary.code_clarity",
        "boundary.copy_safe_commands",
    },
    "evidence.json": {
        "evidence.issue_scope",
        "evidence.source_basis",
        "evidence.branch_preflight",
        "evidence.repo_state",
        "evidence.pm_approval",
        "evidence.validation_output",
        "evidence.pr_diff",
        "evidence.review_evidence",
        "evidence.closure_evidence",
        "evidence.target_adoption",
    },
    "workflows.json": {
        "workflow.review_only",
        "workflow.issue_implementation",
        "workflow.review_before_close",
        "workflow.implementation_discipline_audit",
        "workflow.pm_intake",
        "workflow.design_asset",
        "workflow.security_revision",
        "workflow.release_readiness",
        "workflow.handoff",
        "workflow.target_adoption",
    },
    "outputs.json": {
        "output.execution_report",
        "output.review_result",
        "output.closure_comment",
        "output.draft_issue",
        "output.route_prompt",
        "output.pm_command_bundle",
        "output.asset_prompt",
        "output.security_review_prompt",
        "output.handoff_packet",
        "output.adoption_packet",
        "output.status_result",
    },
}

TRANSFORMATION_OPERATIONS = {
    "conversation_to_docs": {
        "path": "templates/operations/26-draft-docs-from-conversation.md",
        "required": {
            "workflow.pm_intake",
            "mode.review_only",
            "output.route_prompt",
            "output.draft_issue",
            "output.status_result",
            "evidence.source_basis",
        },
    },
    "docs_to_roadmap": {
        "path": "templates/operations/27-draft-roadmap-from-docs.md",
        "required": {
            "workflow.pm_intake",
            "mode.review_only",
            "output.draft_issue",
            "output.pm_command_bundle",
            "output.status_result",
            "evidence.source_basis",
            "evidence.repo_state",
        },
    },
    "docs_from_description": {
        "path": "templates/operations/28-draft-docs-from-description.md",
        "required": {
            "workflow.pm_intake",
            "mode.review_only",
            "output.route_prompt",
            "output.draft_issue",
            "output.status_result",
            "evidence.source_basis",
        },
    },
    "bounded_roadmap_to_issues": {
        "path": "templates/operations/29-draft-bounded-roadmap-issues-command.md",
        "required": {
            "workflow.pm_intake",
            "mode.review_only",
            "output.pm_command_bundle",
            "output.status_result",
            "evidence.source_basis",
            "evidence.repo_state",
        },
    },
}


def _kernel_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted((REPO_ROOT / "kernel").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data.get("id"), str):
            ids.add(data["id"])
        for entry in data.get("entries", []):
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                ids.add(entry["id"])
    return ids


def _kernel_entry(file_name: str, entry_id: str) -> dict:
    data = json.loads((REPO_ROOT / "kernel" / file_name).read_text(encoding="utf-8"))
    for entry in data["entries"]:
        if entry["id"] == entry_id:
            return entry
    raise AssertionError(f"{entry_id} not found in {file_name}")


def _operation_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _operation_paths() -> list[Path]:
    return sorted((REPO_ROOT / "templates" / "operations").glob("*.md"), key=lambda path: path.name)


def _input_variables(text: str) -> list[tuple[str, bool]]:
    match = re.search(r"INPUT:\n(.*?)(?:\n\n[A-Z_]+:|\Z)", text, re.DOTALL)
    assert match, "operation template has no INPUT block"
    variables: list[tuple[str, bool]] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line == "(none)":
            continue
        variable_match = re.search(r"([A-Z][A-Z0-9_]*)=", line)
        if variable_match:
            variables.append((variable_match.group(1), "# optional" not in line))
    return variables


def test_implementation_discipline_audit_workflow_and_operation_are_read_only() -> None:
    workflow = _kernel_entry("workflows.json", "workflow.implementation_discipline_audit")
    template = (REPO_ROOT / "templates" / "operations" / "25-audit-implementation-discipline-gaps.md").read_text(
        encoding="utf-8"
    )
    catalog = (REPO_ROOT / "docs" / "PM_OPERATIONS.md").read_text(encoding="utf-8")

    workflow_text = " ".join([workflow["use_for"], *workflow["steps"]]).lower()
    assert workflow["required_evidence_refs"] == ["evidence.repo_state"]
    assert workflow["allowed_output_refs"] == ["output.review_result", "output.status_result", "output.draft_issue"]
    assert "read-only" in workflow_text
    assert "boundary.implementation_discipline" in workflow_text
    assert "file/line references" in workflow_text
    assert "severity or follow-up priority" in workflow_text
    assert "acceptable local tradeoffs" in workflow_text
    assert "without mutating github" in workflow_text
    assert "never refactor" in workflow_text
    assert "style manifesto" in workflow_text

    assert "workflow.implementation_discipline_audit" in template
    assert "mode.review_only" in template
    assert "TARGET_REPOSITORY=<TARGET_REPOSITORY>" in template
    for optional_var in ("PATH_SCOPE", "FOCUS", "ISSUE_NUMBER", "PR_NUMBER"):
        assert f"{optional_var}=<{optional_var}>   # optional" in template
    assert "Use boundary.implementation_discipline as the canonical audit rule." in template
    assert "Return status.needs_context" in template
    assert "Draft output.draft_issue content for PM review only. Do not create issues." in template
    assert "never refactor, edit files, commit, push, merge, close, label, or mutate GitHub" in template
    assert "Do not duplicate a Clean Code manifesto" in template
    assert "smallest" not in template

    assert "templates/operations/25-audit-implementation-discipline-gaps.md" in catalog
    assert "implementation_discipline_audit" in catalog
    assert "`repo_state`" in catalog
    assert "Este catálogo contiene **33 templates** (`00`–`32`)" in catalog


def test_issue_324_transformation_operations_exist_and_use_existing_kernel_ids() -> None:
    kernel_ids = _kernel_ids()
    for operation_name, spec in TRANSFORMATION_OPERATIONS.items():
        path = REPO_ROOT / spec["path"]
        assert path.exists(), f"{operation_name} operation is missing"
        text = path.read_text(encoding="utf-8")
        for required_ref in spec["required"]:
            assert required_ref in text, f"{operation_name} missing {required_ref}"
            assert required_ref in kernel_ids, f"{operation_name} references non-kernel id {required_ref}"
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            assert ref in kernel_ids, f"{operation_name} references unresolved kernel id {ref}"


def test_issue_324_single_next_issue_operation_remains_available() -> None:
    text = _operation_text("templates/operations/06-draft-create-next-issue-command-from-traceability.md")
    assert "single next real outcome" in text
    assert "OUTPUT:\n  output.pm_command_bundle for exactly one issue" in text
    assert "One outcome per issue" in text
    assert "ISSUE_COUNT_LIMIT" not in text
    assert "SCOPE_LIMIT" not in text


def test_issue_324_bounded_roadmap_to_issues_requires_explicit_bound() -> None:
    text = _operation_text("templates/operations/29-draft-bounded-roadmap-issues-command.md")
    assert "ISSUE_COUNT_LIMIT=<ISSUE_COUNT_LIMIT>   # optional" in text
    assert "SCOPE_LIMIT=<SCOPE_LIMIT>   # optional" in text
    assert "Require at least one explicit bound: ISSUE_COUNT_LIMIT or SCOPE_LIMIT." in text
    assert "IF neither ISSUE_COUNT_LIMIT nor SCOPE_LIMIT is provided:" in text
    assert "Return status.needs_pm_decision requesting one explicit bound" in text
    assert "one `gh issue create`" in text
    assert "One issue per outcome" in text


def test_issue_324_command_bundle_docs_include_review_before_close() -> None:
    text = _operation_text("templates/pm-command-bundle.md")
    examples_intro = text.split("## Examples", 1)[1].split("### Closeout", 1)[0]
    compact = " ".join(examples_intro.split())
    assert "`workflow.pm_intake`" in examples_intro
    assert "`workflow.review_before_close`" in examples_intro
    assert "`workflow.release_readiness`" in examples_intro
    assert "only `workflow.pm_intake` and" not in examples_intro
    assert "reviewed closeout" in compact


def test_issue_324_preserves_design_asset_operation_workflow_and_output() -> None:
    template = _operation_text("templates/operations/19-request-external-design-assets.md")
    workflow = _kernel_entry("workflows.json", "workflow.design_asset")
    output = _kernel_entry("outputs.json", "output.asset_prompt")

    assert "workflow.design_asset" in template
    assert "output.asset_prompt" in template
    assert workflow["allowed_output_refs"] == ["output.asset_prompt", "output.status_result"]
    assert output["id"] == "output.asset_prompt"
    assert "asset objective" in output["required_sections"]


def test_issue_324_kernel_entry_ids_are_unchanged() -> None:
    for file_name, expected_ids in CANONICAL_KERNEL_ENTRY_IDS.items():
        data = json.loads((REPO_ROOT / "kernel" / file_name).read_text(encoding="utf-8"))
        actual_ids = {entry["id"] for entry in data["entries"]}
        assert actual_ids == expected_ids, f"{file_name} kernel ids changed"


def test_issue_324_transformation_docs_do_not_embed_live_state_or_secret_examples() -> None:
    checked_paths = [spec["path"] for spec in TRANSFORMATION_OPERATIONS.values()]
    checked_paths.append("docs/PM_OPERATIONS.md")
    offenders: list[str] = []
    for rel in checked_paths:
        text = _operation_text(rel)
        if LIVE_GITHUB_OBJECT_PATTERN.search(text):
            offenders.append(f"{rel}: live GitHub object URL")
        if SECRET_LOOKING_PATTERN.search(text):
            offenders.append(f"{rel}: secret-looking value")
    assert offenders == [], f"durable live state or secret-looking examples found: {offenders}"


def test_operation_templates_reference_only_valid_kernel_ids_and_no_live_state() -> None:
    kernel_ids = _kernel_ids()
    checked_paths = [*list(_operation_paths()), REPO_ROOT / "docs" / "PM_OPERATIONS.md"]
    offenders: list[str] = []
    for path in checked_paths:
        text = path.read_text(encoding="utf-8")
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            if ref not in kernel_ids:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: invalid kernel id {ref}")
        if LIVE_GITHUB_OBJECT_PATTERN.search(text):
            offenders.append(f"{path.relative_to(REPO_ROOT)}: durable live GitHub object URL")
        if SECRET_LOOKING_PATTERN.search(text):
            offenders.append(f"{path.relative_to(REPO_ROOT)}: secret-looking value")
    assert offenders == []


def test_operation_templates_do_not_duplicate_input_variables() -> None:
    offenders: list[str] = []
    for path in _operation_paths():
        variables = [name for name, _required in _input_variables(path.read_text(encoding="utf-8"))]
        if len(variables) != len(set(variables)):
            offenders.append(f"{path.name}: {variables}")
    assert offenders == []


def test_pm_question_and_feedback_variables_are_scoped_to_justified_operations() -> None:
    allowed_pm_question = {"00", "05", "30", "31", "32"}
    allowed_optional_feedback = {"30", "31", "32"}
    allowed_required_feedback = {"08"}

    for path in _operation_paths():
        idx = path.name[:2]
        variables = _input_variables(path.read_text(encoding="utf-8"))
        for name, required in variables:
            if name == "PM_QUESTION":
                assert not required, f"{path.name}: PM_QUESTION must be optional"
                assert idx in allowed_pm_question, f"{path.name}: PM_QUESTION is not justified"
            if name == "PM_FEEDBACK_HUMANO":
                if required:
                    assert idx in allowed_required_feedback, (
                        f"{path.name}: PM_FEEDBACK_HUMANO may be required only for correction routing"
                    )
                else:
                    assert idx in allowed_optional_feedback, f"{path.name}: optional PM feedback is not justified"


def test_operation_templates_keep_external_recipients_distinct_from_kernel_actors() -> None:
    forbidden_actor_ids = {
        "actor." + suffix
        for suffix in (
            "qa",
            "human_qa",
            "security_reviewer",
            "designer",
            "asset_creator",
            "reviewer",
        )
    }
    for path in _operation_paths():
        text = path.read_text(encoding="utf-8")
        for forbidden in forbidden_actor_ids:
            assert forbidden not in text, f"{path.name}: external recipient drifted into kernel actor {forbidden}"


def test_issue_336_post_gate_result_variables_have_no_unjustified_aliases() -> None:
    template_paths = [
        REPO_ROOT / "templates" / "operations" / "30-process-human-qa-results.md",
        REPO_ROOT / "templates" / "operations" / "31-process-security-review-results.md",
        REPO_ROOT / "templates" / "operations" / "32-process-design-asset-delivery.md",
    ]
    forbidden_aliases = {"QA_RESULTS", "SECURITY_RESULTS", "ASSET_FEEDBACK", "DESIGN_FEEDBACK"}
    for path in template_paths:
        variables = {name for name, _required in _input_variables(path.read_text(encoding="utf-8"))}
        assert variables.isdisjoint(forbidden_aliases), (
            f"{path.relative_to(REPO_ROOT)} keeps unjustified alias variables: {variables & forbidden_aliases}"
        )

    docs = _operation_text("docs/PM_OPERATIONS.md")
    matrix = docs.split("| 30 |", 1)[1].split("## Cobertura de operaciones", 1)[0]
    for alias in forbidden_aliases:
        assert alias not in matrix, f"docs matrix keeps unjustified alias {alias}"


def test_issue_336_lifecycle_coverage_or_follow_up_decision_is_documented() -> None:
    docs = _operation_text("docs/PM_OPERATIONS.md")
    required_fragments = [
        "### Cobertura Post-Gate",
        "QA humano (`18` → `30`)",
        "revisión de seguridad\n(`20` → `31`)",
        "assets/diseño (`19` → `32`)",
        "implementación y reportes se revisan en `09`",
        "findings de review se convierten\nen corrección con `08` o follow-up con `21`",
        "fallas de validación bloqueantes\nvuelven por `08`",
        "post-merge y release\nviven en `11`/`12`/`13`/`24`",
        "debe decidirse como follow-up PM",
    ]
    for fragment in required_fragments:
        assert fragment in docs, f"missing lifecycle coverage fragment: {fragment}"


def test_issue_336_post_gate_operations_exist_and_conform() -> None:
    ops = [
        "templates/operations/30-process-human-qa-results.md",
        "templates/operations/31-process-security-review-results.md",
        "templates/operations/32-process-design-asset-delivery.md",
    ]
    kernel_ids = _kernel_ids()
    for op_path in ops:
        text = _operation_text(op_path)

        # Valid kernel ids
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(text))):
            assert ref in kernel_ids, f"{op_path} references unresolved kernel id {ref}"

        # No role-actor drift and no write authority
        assert "actor.browser_chat" in text, f"{op_path} must be executed by actor.browser_chat"
        assert "mode.review_only" in text, f"{op_path} must run in mode.review_only (no write authority)"
        delegated_mode_prefix = "mode." + "delegated_commit"
        assert delegated_mode_prefix not in text, f"{op_path} must not imply delegated write mode"
        assert "Draft only. No mutation." in text, f"{op_path} must explicitly declare no mutation"

        # No durable live state
        assert LIVE_GITHUB_OBJECT_PATTERN.search(text) is None, f"{op_path} must not embed durable live state (URLs)"

        # Recommended next operation guidance
        assert "RECOMMENDED_NEXT_OPERATION:" in text, f"{op_path} must have recommended next operation"

        # Specific variable checks
        assert "PM_QUESTION=<PM_QUESTION>   # optional" in text
        assert "PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional" in text
        if "30" in op_path:
            assert "QA_RESULT=<QA_RESULT>" in text
            assert "ISSUE_NUMBER=<ISSUE_NUMBER>   # optional" in text
        elif "31" in op_path:
            assert "SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>" in text
            assert "PR_NUMBER=<PR_NUMBER>   # optional" in text
        elif "32" in op_path:
            assert "DESIGN_DELIVERY=<DESIGN_DELIVERY>" in text
            assert "ISSUE_NUMBER=<ISSUE_NUMBER>   # optional" in text
