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
LEGACY_PM_QUESTION_PATTERN = re.compile(r"\bPM_QUESTION\b")
HUMAN_CONTEXT_VARIABLES = {"PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"}
FLOW_DOC_PATH = "docs/OPERATION_FLOWS.md"
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
        "workflow.issue_implementation_manual",
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
        "output.manual_implementation_plan",
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


def _markdown_table(text: str, heading: str) -> list[dict[str, str]]:
    after_heading = text.split(heading, 1)[1]
    table_lines: list[str] = []
    for line in after_heading.splitlines():
        if line.startswith("|"):
            table_lines.append(line)
        elif table_lines and not line.strip():
            break
    assert len(table_lines) >= 3, f"missing markdown table after {heading}"
    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        assert len(cells) == len(headers), f"malformed table row: {line}"
        rows.append(dict(zip(headers, cells, strict=True)))
    return rows


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
    assert "Este catálogo contiene **36 templates** (`00`–`35`)" in catalog


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


def test_issue_343_manual_implementation_kernel_contract_is_no_write() -> None:
    workflow = _kernel_entry("workflows.json", "workflow.issue_implementation_manual")
    output = _kernel_entry("outputs.json", "output.manual_implementation_plan")
    workflow_text = " ".join([workflow["use_for"], *workflow["steps"]]).lower()
    output_rule = output["rule"].lower()

    assert workflow["required_evidence_refs"] == [
        "evidence.issue_scope",
        "evidence.source_basis",
        "evidence.repo_state",
    ]
    assert workflow["allowed_output_refs"] == ["output.manual_implementation_plan", "output.status_result"]
    assert "without repository or github mutation" in workflow_text
    assert "mode.review_only" in workflow_text
    assert "status.needs_context" in workflow_text
    assert "no code was edited" in workflow_text
    assert "no files were written" in workflow_text
    assert "no git or github mutation occurred" in workflow_text
    assert "evidence.branch_preflight" not in workflow["required_evidence_refs"]
    assert "evidence.pm_approval" not in workflow["required_evidence_refs"]
    assert "output.execution_report" not in workflow["allowed_output_refs"]

    required_sections = set(output["required_sections"])
    for section in {
        "objective",
        "files to inspect",
        "files to modify",
        "change plan by file/anchor/line where possible",
        "exact additions/removals in prose or patch-like snippets when safe",
        "reasoning for each change",
        "validation commands",
        "manual QA checklist",
        "risks and rollback",
        "recommended next Project OS operation",
        "no-write statement",
    }:
        assert section in required_sections
    assert "human-executable plan" in output_rule
    assert "not an execution report" in output_rule
    assert "must never claim code was edited or validated by browser chat" in output_rule
    assert "never grants write permission" in output_rule


def test_issue_343_manual_implementation_operation_template_is_no_write_plan() -> None:
    text = _operation_text("templates/operations/33-draft-manual-implementation-plan.md")
    lower_text = text.lower()
    variables = _input_variables(text)

    assert ("ISSUE_NUMBER", True) in variables
    for optional_var in ("TARGET_REPOSITORY", "PATH_SCOPE", "PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"):
        assert (optional_var, False) in variables
        assert f"{optional_var}=<{optional_var}>   # optional" in text
    assert "workflow.issue_implementation_manual" in text
    assert "mode.review_only" in text
    assert "output.manual_implementation_plan" in text
    assert "Do not emit output.execution_report." in text
    assert "Return status.needs_context" in text
    assert "Return status.blocked" in text
    assert "Browser chat drafts only; it never executes code, edits files, commits, pushes, opens PRs, merges, closes issues, labels, releases, changes settings, edits target repos, or mutates runtime state." in text
    assert "A manual implementation plan is not a claim that Project OS or browser chat implemented the issue." in text
    assert "did not edit code, did not write files, did not run validation, and did not mutate git or GitHub" in text
    assert "Use Operation 34 for result classification when needed." in text
    assert not LEGACY_PM_QUESTION_PATTERN.search(text)

    forbidden_claims = [
        "browser chat edited code",
        "browser chat applied",
        "i edited",
        "files changed by browser chat",
        "changes applied by browser chat",
    ]
    for claim in forbidden_claims:
        assert claim not in lower_text


def test_issue_343_manual_implementation_docs_catalog_and_flow_are_aligned() -> None:
    catalog = _operation_text("docs/PM_OPERATIONS.md")
    flow_doc = _operation_text(FLOW_DOC_PATH)
    template = _operation_text("templates/operations/33-draft-manual-implementation-plan.md")
    rows = _markdown_table(flow_doc, "## Phase Flow Map")
    row_33 = next(row for row in rows if row["Op"] == "33")

    assert "templates/operations/33-draft-manual-implementation-plan.md" in catalog
    assert "issue_implementation_manual" in catalog
    assert "manual_implementation_plan" in catalog
    assert "Este catálogo contiene **36 templates** (`00`–`35`)" in catalog
    assert "| 33 | ISSUE_NUMBER | TARGET_REPOSITORY, PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO |" in catalog

    assert row_33["Phase"] == "Manual implementation planning"
    assert row_33["Template"] == "`templates/operations/33-draft-manual-implementation-plan.md`"
    assert row_33["Required evidence"] == "`evidence.issue_scope`, `evidence.source_basis`, `evidence.repo_state`"
    assert row_33["Variables"] == (
        "Req: `ISSUE_NUMBER`; Opt: `TARGET_REPOSITORY`, `PATH_SCOPE`, "
        "`PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO`"
    )
    assert row_33["Output contract"] == "`output.manual_implementation_plan`"
    assert "nunca afirma que browser chat edito codigo" in row_33["PM approval behavior"]
    assert "Operation 34" in template
    assert "Process manual implementation result" in flow_doc
    assert "New Operation 34" in flow_doc


def test_issue_346_operation_09_remains_execution_report_review_path() -> None:
    text = _operation_text("templates/operations/09-review-pr-before-close-and-draft-package.md")
    flow_doc = _operation_text(FLOW_DOC_PATH)

    assert "terminal-agent reports" in text
    assert "When a PR exists, this operation is the standard Project OS path for consuming terminal-agent execution reports before close." in text
    assert "Do not route a normal PR execution report to a separate processor" in text
    assert "Operation 09 is already the review-before-close path" in flow_doc
    assert "no new operation for the normal PR path" in flow_doc


def test_issue_346_manual_result_processing_operation_is_classification_only() -> None:
    text = _operation_text("templates/operations/34-process-manual-implementation-result.md")
    flow_doc = _operation_text(FLOW_DOC_PATH)
    catalog = _operation_text("docs/PM_OPERATIONS.md")
    variables = _input_variables(text)

    assert ("ISSUE_NUMBER", True) in variables
    assert ("MANUAL_IMPLEMENTATION_RESULT", True) in variables
    for optional_var in (
        "MANUAL_IMPLEMENTATION_PLAN",
        "PR_NUMBER",
        "TARGET_REPOSITORY",
        "PM_FEEDBACK_HUMANO",
        "PM_QUESTION_HUMANO",
    ):
        assert (optional_var, False) in variables
        assert f"{optional_var}=<{optional_var}>   # optional" in text
    assert "workflow.pm_intake" in text
    assert "mode.review_only" in text
    assert "output.status_result" in text
    assert "Recommend Operation 09 as the primary review-before-close path." in text
    assert "Do not duplicate Operation 09" in text
    assert "State explicitly that browser chat did not apply changes, did not validate changes" in text
    assert "Does not claim browser chat applied or validated changes." in text
    assert "Does not implement #344/TOOLS.6" in text
    assert not LEGACY_PM_QUESTION_PATTERN.search(text)

    lower_text = text.lower()
    forbidden_claims = [
        "browser chat applied changes",
        "browser chat validated changes",
        "changes applied by browser chat",
        "validated by browser chat",
    ]
    for claim in forbidden_claims:
        assert claim not in lower_text

    assert "templates/operations/34-process-manual-implementation-result.md" in catalog
    assert "New Operation 34" in flow_doc


def test_issue_346_next_lifecycle_operation_is_recommendation_only() -> None:
    text = _operation_text("templates/operations/35-recommend-next-lifecycle-operation.md")
    flow_doc = _operation_text(FLOW_DOC_PATH)
    variables = _input_variables(text)

    assert ("TARGET_REPOSITORY", False) in variables
    assert ("ISSUE_NUMBER", False) in variables
    assert ("PR_NUMBER", False) in variables
    assert ("ROADMAP_ISSUE", False) in variables
    assert ("CURRENT_STATUS", False) in variables
    assert "workflow.review_only" in text
    assert "mode.review_only" in text
    assert "output.status_result" in text
    assert "Recommendation-only; never execute the next step." in text
    assert "does not run, authorize, or draft the recommended operation's output" in text
    assert "Do not execute the recommended operation." in text
    assert "Do not emit output.route_prompt, output.pm_command_bundle, output.execution_report, or output.closure_comment." in text
    assert "Do not implement #344/TOOLS.6" in text
    assert "New Operation 35" in flow_doc
    assert "executes lifecycle transitions\nautomatically" in flow_doc
    assert not LEGACY_PM_QUESTION_PATTERN.search(text)


def test_issue_346_sdlc_fit_check_and_candidate_decisions_are_documented() -> None:
    flow_doc = _operation_text(FLOW_DOC_PATH)
    catalog = _operation_text("docs/PM_OPERATIONS.md")
    rows = _markdown_table(flow_doc, "## KOPS.3 Candidate Decisions")
    decisions = {row["Candidate"]: row["Decision"] for row in rows}

    assert "## SDLC Comparison and KOPS.3 Fit Check" in flow_doc
    for area in (
        "Intake/requirements",
        "Planning/design",
        "Implementation",
        "Manual implementation result processing",
        "Testing/QA/security/design gates",
        "PR review/acceptance",
        "Closeout/release",
        "Maintenance/follow-up",
        "Handoff/evaluation",
    ):
        assert area in flow_doc

    assert decisions == {
        "Process terminal-agent execution report outside PR review": (
            "Docs/template clarification plus test guard; no new operation for the normal PR path."
        ),
        "Process manual implementation result": "New Operation 34.",
        "Process `status.needs_pm_decision`": "Docs/test clarification; no named operation.",
        "Determine next lifecycle operation": "New Operation 35.",
        "Phase readiness review": "Deferred follow-up.",
    }
    assert "status.needs_pm_decision` no recibe una operacion propia" in catalog
    assert "Phase readiness review queda" in catalog
    assert "no requiere nuevos ids de kernel" in catalog


def test_issue_346_scope_does_not_implement_tools6_or_kernel_growth() -> None:
    import subprocess

    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    changed_files = {line for line in result.stdout.splitlines() if line}

    assert "tools/operation_prompt_wizard.py" not in changed_files
    assert "tools/operation_prompt_wizard_pt.py" not in changed_files
    assert not any(path.startswith("kernel/") for path in changed_files)
    assert "Does not implement #344/TOOLS.6" in _operation_text(
        "templates/operations/34-process-manual-implementation-result.md"
    )
    assert "Do not implement #344/TOOLS.6" in _operation_text(
        "templates/operations/35-recommend-next-lifecycle-operation.md"
    )


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
    checked_paths = [
        *list(_operation_paths()),
        REPO_ROOT / "docs" / "PM_OPERATIONS.md",
        REPO_ROOT / FLOW_DOC_PATH,
    ]
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


def test_operation_flow_doc_covers_every_operation_without_renumbering() -> None:
    flow_doc = _operation_text(FLOW_DOC_PATH)
    rows = _markdown_table(flow_doc, "## Phase Flow Map")
    operation_paths = _operation_paths()
    expected_ops = {f"{index:02d}" for index in range(36)}
    actual_ops = {row["Op"] for row in rows}

    assert len(rows) == 36
    assert actual_ops == expected_ops
    assert [path.name[:2] for path in operation_paths] == sorted(expected_ops)

    expected_templates = {path.name[:2]: f"`{path.relative_to(REPO_ROOT)}`" for path in operation_paths}
    for row in rows:
        assert row["Template"] == expected_templates[row["Op"]]
        assert row["Phase"]
        assert row["Trigger"]
        assert row["Safe next operation"]
        assert row["Fail-closed behavior"]
        assert row["PM approval behavior"]


def test_operation_flow_doc_variables_match_templates() -> None:
    flow_doc = _operation_text(FLOW_DOC_PATH)
    rows = _markdown_table(flow_doc, "## Phase Flow Map")
    rows_by_op = {row["Op"]: row for row in rows}

    for path in _operation_paths():
        op = path.name[:2]
        row = rows_by_op[op]
        variables = _input_variables(path.read_text(encoding="utf-8"))
        required = [name for name, is_required in variables if is_required]
        optional = [name for name, is_required in variables if not is_required]
        expected_req = "none" if not required else ", ".join(f"`{name}`" for name in required)
        expected_opt = "none" if not optional else ", ".join(f"`{name}`" for name in optional)

        assert row["Variables"] == f"Req: {expected_req}; Opt: {expected_opt}"


def test_operation_flow_doc_uses_valid_kernel_ids_and_template_references() -> None:
    flow_doc = _operation_text(FLOW_DOC_PATH)
    kernel_ids = _kernel_ids()
    valid_templates = {str(path.relative_to(REPO_ROOT)) for path in _operation_paths()}
    rows = _markdown_table(flow_doc, "## Phase Flow Map")
    offenders: list[str] = []

    for ref in sorted(set(KERNEL_ID_PATTERN.findall(flow_doc))):
        if ref not in kernel_ids:
            offenders.append(f"invalid kernel id {ref}")
    for row in rows:
        template = row["Template"].strip("`")
        if template not in valid_templates:
            offenders.append(f"invalid template reference {template}")
    if LIVE_GITHUB_OBJECT_PATTERN.search(flow_doc):
        offenders.append("durable live GitHub object URL")
    if SECRET_LOOKING_PATTERN.search(flow_doc):
        offenders.append("secret-looking value")

    assert offenders == []


def test_operation_flow_doc_preserves_phase_and_gap_decisions() -> None:
    flow_doc = _operation_text(FLOW_DOC_PATH)
    catalog_doc = _operation_text("docs/PM_OPERATIONS.md")
    rows = _markdown_table(flow_doc, "## Phase Flow Map")
    phases = {row["Phase"] for row in rows}
    required_phases = {
        "Activation and state review",
        "Idea intake and requirements",
        "Roadmap and issue planning",
        "Implementation routing",
        "Manual implementation planning",
        "PR review and correction",
        "QA, security and design gates",
        "Follow-up and maintenance",
        "Closeout and verification",
        "Release and handoff",
    }
    required_gap_fragments = [
        "manual PM-facing de flujo por fase",
        "`docs/PM_OPERATIONS.md`: indice canonico, matriz de variables",
        "`docs/OPERATION_FLOWS.md`: manual PM-facing",
        "que template existe y que contrato\ntiene",
        "cuando lo uso y que sigue",
        "## SDLC Comparison and KOPS.3 Fit Check",
        "Manual implementation result processing",
        "Handoff/evaluation",
        "templates/operations/33-draft-manual-implementation-plan.md",
        "output.manual_implementation_plan",
        "New Operation 34",
        "New Operation 35",
        "Process terminal-agent execution report outside PR review",
        "Process manual implementation result",
        "Process `status.needs_pm_decision`",
        "Determine next lifecycle operation",
        "Phase readiness review",
        "Docs/test clarification; no named operation.",
        "Deferred follow-up.",
        "authorization granted for this exact scope and mode",
        "pending/draft/read-only planning first",
        "The prompt artifact itself never grants",
        "Browser chat: siempre draft-only",
        "GitHub/git: source of truth para estado vivo",
    ]
    catalog_fragments = [
        "Arquitectura final de docs de operaciones",
        "`docs/PM_OPERATIONS.md` es el índice canónico",
        "`docs/OPERATION_FLOWS.md` es el manual PM-facing",
        "Ambos docs apuntan a las mismas operaciones `00`–`35`",
        "manual_implementation_plan",
        "aprobación exacta otorgada vs pendiente/draft/read-only planning",
        "Manual-result processing",
        "Next lifecycle operation recommendation",
    ]

    assert required_phases.issubset(phases)
    for fragment in required_gap_fragments:
        assert fragment in flow_doc, f"missing flow/gap decision fragment: {fragment}"
    for fragment in catalog_fragments:
        assert fragment in catalog_doc, f"missing catalog docs-architecture fragment: {fragment}"


def test_issue_346_candidate_decision_table_is_pm_actionable() -> None:
    flow_doc = _operation_text(FLOW_DOC_PATH)
    rows = _markdown_table(flow_doc, "## KOPS.3 Candidate Decisions")
    expected_decisions = {
        "Process terminal-agent execution report outside PR review": (
            "Docs/template clarification plus test guard; no new operation for the normal PR path."
        ),
        "Process manual implementation result": "New Operation 34.",
        "Process `status.needs_pm_decision`": "Docs/test clarification; no named operation.",
        "Determine next lifecycle operation": "New Operation 35.",
        "Phase readiness review": "Deferred follow-up.",
    }

    assert {row["Candidate"] for row in rows} == set(expected_decisions)
    for row in rows:
        assert row["Decision"] == expected_decisions[row["Candidate"]]
        assert row["Rationale"]
        assert row["Durable change"]

    deferred_rows = _markdown_table(flow_doc, "## Deferred Lifecycle Follow-up Candidates")
    assert {row["Deferred candidate"] for row in deferred_rows} == {
        "Phase readiness review",
        "Terminal execution report outside PR review",
    }
    for row in deferred_rows:
        assert row["Why deferred"]
        assert row["Required evidence before adding"]

    assert "Manual implementation planning is covered by operation `33`" in flow_doc
    assert "workflow.issue_implementation_manual" in _operation_text(
        "templates/operations/33-draft-manual-implementation-plan.md"
    )


def test_operation_templates_do_not_duplicate_input_variables() -> None:
    offenders: list[str] = []
    for path in _operation_paths():
        variables = [name for name, _required in _input_variables(path.read_text(encoding="utf-8"))]
        if len(variables) != len(set(variables)):
            offenders.append(f"{path.name}: {variables}")
    assert offenders == []


def test_human_context_variables_are_optional_and_universal_in_operations() -> None:
    for path in _operation_paths():
        text = path.read_text(encoding="utf-8")
        variables = _input_variables(text)
        variable_names = {name for name, _required in variables}

        assert not LEGACY_PM_QUESTION_PATTERN.search(text), f"{path.name}: legacy PM_QUESTION token remains"
        assert HUMAN_CONTEXT_VARIABLES.issubset(variable_names), f"{path.name}: missing human context vars"
        for name, required in variables:
            if name in HUMAN_CONTEXT_VARIABLES:
                assert not required, f"{path.name}: {name} must be optional context"


def test_human_context_variables_do_not_replace_authority_or_live_evidence() -> None:
    docs = _operation_text("docs/PM_OPERATIONS.md")
    variables = _operation_text("docs/PM_VARIABLES.md")

    required_fragments = [
        "Nunca reemplaza evidencia viva requerida ni otorga\n  permiso de escritura.",
        "no reemplaza issue/PR/docs/evidencia viva requerida y no\n  autoriza mutaciones.",
        "`PM_FEEDBACK_HUMANO`: contexto, criterio o interpretación adicional del PM. Es opcional y nunca reemplaza evidencia viva requerida.",
        "`PM_QUESTION_HUMANO`: pregunta del PM",
        "Es opcional y nunca otorga autorización.",
    ]
    combined = docs + "\n" + variables
    for fragment in required_fragments:
        assert fragment in combined, f"missing human context boundary fragment: {fragment}"


def test_legacy_pm_question_token_is_not_an_accepted_variable_anywhere() -> None:
    allowed_fragments = {
        "docs/PM_OPERATIONS.md": [
            "`PM_QUESTION` no es alias ni variable legacy aceptada.",
        ],
        "docs/PM_VARIABLES.md": [
            "`PM_QUESTION` es inválida y fue removida.",
        ],
        "tests/test_operations_catalog.py": [
            "LEGACY_PM_QUESTION_PATTERN",
            "legacy PM_QUESTION token remains",
        ],
        "tests/test_pm_operation_contracts.py": [
            "LEGACY_PM_QUESTION_PATTERN",
            "`PM_QUESTION` no es alias ni variable legacy aceptada.",
            "`PM_QUESTION` es inválida y fue removida.",
            "legacy PM_QUESTION token remains",
        ],
    }
    offenders: list[str] = []
    for root in ("templates", "docs", "tests", "tools"):
        for path in sorted((REPO_ROOT / root).rglob("*")):
            if not path.is_file():
                continue
            if path.suffix not in {".md", ".py", ".json"}:
                continue
            text = path.read_text(encoding="utf-8")
            rel = str(path.relative_to(REPO_ROOT))
            for line_number, line in enumerate(text.splitlines(), start=1):
                if not LEGACY_PM_QUESTION_PATTERN.search(line):
                    continue
                allowed = any(fragment in line for fragment in allowed_fragments.get(rel, []))
                if not allowed:
                    offenders.append(f"{rel}:{line_number}: {line.strip()}")
    assert offenders == []


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
        "### Cobertura KOPS.3",
        "QA humano (`18` → `30`)",
        "revision de seguridad\n(`20` → `31`)",
        "assets/diseno (`19` → `32`)",
        "KOPS.3 agrega solo lo que no\nduplicaba rutas existentes",
        "la implementacion manual se planifica con `33`",
        "resultado aplicado por humano se clasifica con `34`",
        "la proxima operacion se\nrecomienda con `35` sin ejecutar nada",
        "reportes de terminal agent y PRs se\nrevisan en `09`",
        "findings de review se convierten en correccion con `08` o\nfollow-up con `21`",
        "fallas de validacion bloqueantes vuelven por `08`",
        "post-merge y release viven en `11`/`12`/`13`/`24`",
        "`status.needs_pm_decision` no recibe una operacion propia",
        "Phase readiness review queda\ndiferido",
    ]
    for fragment in required_fragments:
        assert fragment in docs, f"missing lifecycle coverage fragment: {fragment}"


def test_issue_336_operation_07_issue_number_is_optional_with_live_traceability_fallback() -> None:
    text = _operation_text("templates/operations/07-draft-issue-implementation-route-prompt.md")
    variables = _input_variables(text)

    assert ("ISSUE_NUMBER", False) in variables
    assert ("ROADMAP_ISSUE", False) in variables
    assert "PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional" in text
    assert "PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional" in text
    assert not LEGACY_PM_QUESTION_PATTERN.search(text)

    required_fragments = [
        "If ISSUE_NUMBER is provided, read that issue scope and source basis live",
        "If ISSUE_NUMBER is omitted, derive exactly one next issue from live traceability",
        "ROADMAP_ISSUE when provided",
        "IF ISSUE_NUMBER omitted and zero candidate issues can be derived:",
        "Return status.needs_context naming the missing live evidence.",
        "IF ISSUE_NUMBER omitted and multiple plausible candidate issues exist:",
        "Return status.needs_pm_decision asking the PM to choose exactly one ISSUE_NUMBER.",
        "Never invent the target issue.",
        "A route prompt never grants write authority",
    ]
    for fragment in required_fragments:
        assert fragment in text, f"operation 07 missing fallback contract: {fragment}"


def test_issue_336_post_gate_optional_identifiers_have_fail_closed_rules() -> None:
    specs = {
        "templates/operations/30-process-human-qa-results.md": [
            "If ISSUE_NUMBER is provided, use that issue as the target evidence basis.",
            "If ISSUE_NUMBER is omitted, derive exactly one target issue from QA_RESULT",
            "IF ISSUE_NUMBER omitted and no target issue can be derived:",
            "Return status.needs_context naming the missing issue or traceability evidence.",
            "IF ISSUE_NUMBER omitted and multiple plausible target issues exist:",
            "Return status.needs_pm_decision asking the PM to choose exactly one ISSUE_NUMBER.",
        ],
        "templates/operations/31-process-security-review-results.md": [
            "If PR_NUMBER is provided, read that PR diff and linked issue.",
            "If PR_NUMBER is omitted, derive exactly one target PR and linked issue from",
            "IF PR_NUMBER omitted and no target PR can be derived:",
            "Return status.needs_context naming the missing PR, issue, or traceability evidence.",
            "IF PR_NUMBER omitted and multiple plausible target PRs or linked issues exist:",
            "Return status.needs_pm_decision asking the PM to choose exactly one PR_NUMBER.",
        ],
        "templates/operations/32-process-design-asset-delivery.md": [
            "If ISSUE_NUMBER is provided, use that issue as the target evidence basis.",
            "If ISSUE_NUMBER is omitted, derive exactly one target issue from DESIGN_DELIVERY",
            "IF ISSUE_NUMBER omitted and no target issue can be derived:",
            "Return status.needs_context naming the missing issue or traceability evidence.",
            "IF ISSUE_NUMBER omitted and multiple plausible target issues or product routes exist:",
            "Return status.needs_pm_decision asking the PM to choose exactly one ISSUE_NUMBER",
        ],
    }

    for path, fragments in specs.items():
        text = _operation_text(path)
        for fragment in fragments:
            assert fragment in text, f"{path} missing fail-closed rule: {fragment}"


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
        assert "PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional" in text
        assert "PM_QUESTION_HUMANO=<PM_QUESTION_HUMANO>   # optional" in text
        assert not LEGACY_PM_QUESTION_PATTERN.search(text)
        if "30" in op_path:
            assert "QA_RESULT=<QA_RESULT>" in text
            assert "ISSUE_NUMBER=<ISSUE_NUMBER>   # optional" in text
        elif "31" in op_path:
            assert "SECURITY_REVIEW_RESULT=<SECURITY_REVIEW_RESULT>" in text
            assert "PR_NUMBER=<PR_NUMBER>   # optional" in text
        elif "32" in op_path:
            assert "DESIGN_DELIVERY=<DESIGN_DELIVERY>" in text
            assert "ISSUE_NUMBER=<ISSUE_NUMBER>   # optional" in text
