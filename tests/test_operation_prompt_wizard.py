"""Tests for the local operation prompt wizard."""

from __future__ import annotations

import io
from pathlib import Path

from tools.operation_prompt_wizard import (
    DEFAULT_OUTPUT_DIR,
    InputVariable,
    OperationTemplate,
    OUTPUT_DIR_ENV,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
    PM_AUTHORIZATION_STATUS_NAME,
    WIZARD_PROMPT_MARKER,
    carryover_values,
    cleanup_previous_generated_prompts,
    collect_values_with_controls,
    collect_values,
    confirm_write,
    discover_operations,
    filter_operations,
    find_replaceable_prompts,
    generated_filename,
    is_carryover_variable,
    is_wizard_generated_artifact,
    load_phase_map,
    operation_needs_pm_authorization_assistance,
    operation_output_refs,
    operation_produces_route_prompt,
    operation_requires_route_prompt_path_selection,
    parse_input_variables,
    print_pm_authorization_assistance,
    print_phase_groups,
    render_prompt,
    resolve_operation_selection,
    resolve_output_dir,
    run_wizard,
    normalize_pm_authorization_status,
    validate_variable_value,
    wizard_variables,
    write_prompt,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
OPERATIONS_DIR = REPO_ROOT / "templates" / "operations"


def write_operation(path: Path, title: str, input_block: str = "  (none)") -> None:
    path.write_text(
        f"# {title}\n\nOPERATION:\n  Test operation.\n\nINPUT:\n{input_block}\n\nKERNEL:\n  Test.\n",
        encoding="utf-8",
    )


def answers(*values: str):
    iterator = iter(values)
    return lambda _prompt: next(iterator)


def test_discover_operations_is_deterministic_by_filename(tmp_path: Path) -> None:
    write_operation(tmp_path / "02-beta.md", "Beta")
    write_operation(tmp_path / "01-alpha.md", "Alpha")

    operations = discover_operations(tmp_path)

    assert [operation.filename for operation in operations] == ["01-alpha.md", "02-beta.md"]
    assert [operation.index for operation in operations] == [1, 2]
    assert [operation.title for operation in operations] == ["Alpha", "Beta"]


def test_parse_required_and_optional_variables_from_representative_operations() -> None:
    issue_route = (OPERATIONS_DIR / "07-draft-issue-implementation-route-prompt.md").read_text(
        encoding="utf-8"
    )
    bounded_roadmap = (OPERATIONS_DIR / "29-draft-bounded-roadmap-issues-command.md").read_text(
        encoding="utf-8"
    )
    audit = (OPERATIONS_DIR / "25-audit-implementation-discipline-gaps.md").read_text(encoding="utf-8")
    handoff = (OPERATIONS_DIR / "17-draft-handoff-package-for-new-session.md").read_text(
        encoding="utf-8"
    )

    issue_vars = parse_input_variables(issue_route)
    assert [(variable.name, variable.required) for variable in issue_vars] == [
        ("ISSUE_NUMBER", False),
        ("ROADMAP_ISSUE", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]

    roadmap_vars = parse_input_variables(bounded_roadmap)
    assert [(variable.name, variable.required) for variable in roadmap_vars] == [
        ("ROADMAP_ISSUE", True),
        ("ISSUE_COUNT_LIMIT", False),
        ("SCOPE_LIMIT", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]

    audit_vars = parse_input_variables(audit)
    assert [(variable.name, variable.required) for variable in audit_vars] == [
        ("TARGET_REPOSITORY", True),
        ("PATH_SCOPE", False),
        ("FOCUS", False),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]
    assert [(variable.name, variable.required) for variable in parse_input_variables(handoff)] == [
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]


def test_parse_post_gate_operation_variables_without_aliases() -> None:
    qa = (OPERATIONS_DIR / "30-process-human-qa-results.md").read_text(encoding="utf-8")
    security = (OPERATIONS_DIR / "31-process-security-review-results.md").read_text(encoding="utf-8")
    design = (OPERATIONS_DIR / "32-process-design-asset-delivery.md").read_text(encoding="utf-8")

    assert [(variable.name, variable.required) for variable in parse_input_variables(qa)] == [
        ("QA_RESULT", True),
        ("ISSUE_NUMBER", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]
    assert [(variable.name, variable.required) for variable in parse_input_variables(security)] == [
        ("SECURITY_REVIEW_RESULT", True),
        ("PR_NUMBER", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]
    assert [(variable.name, variable.required) for variable in parse_input_variables(design)] == [
        ("DESIGN_DELIVERY", True),
        ("ISSUE_NUMBER", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]


def test_parse_operation_09_execution_report_input() -> None:
    review_pr = (OPERATIONS_DIR / "09-review-pr-before-close-and-draft-package.md").read_text(
        encoding="utf-8"
    )

    assert [(variable.name, variable.required) for variable in parse_input_variables(review_pr)] == [
        ("PR_NUMBER", True),
        ("EXECUTION_REPORT", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]


def test_parse_kops3_lifecycle_processing_operation_variables() -> None:
    manual_result = (OPERATIONS_DIR / "34-process-manual-implementation-result.md").read_text(
        encoding="utf-8"
    )
    next_operation = (OPERATIONS_DIR / "35-recommend-next-lifecycle-operation.md").read_text(
        encoding="utf-8"
    )
    pm_decision = (OPERATIONS_DIR / "36-process-needs-pm-decision.md").read_text(
        encoding="utf-8"
    )
    phase_readiness = (OPERATIONS_DIR / "37-review-phase-readiness.md").read_text(
        encoding="utf-8"
    )

    assert [(variable.name, variable.required) for variable in parse_input_variables(manual_result)] == [
        ("ISSUE_NUMBER", True),
        ("MANUAL_IMPLEMENTATION_RESULT", True),
        ("MANUAL_IMPLEMENTATION_PLAN", False),
        ("PR_NUMBER", False),
        ("TARGET_REPOSITORY", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]
    assert [(variable.name, variable.required) for variable in parse_input_variables(next_operation)] == [
        ("TARGET_REPOSITORY", False),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
        ("ROADMAP_ISSUE", False),
        ("CURRENT_STATUS", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]
    assert [(variable.name, variable.required) for variable in parse_input_variables(pm_decision)] == [
        ("ORIGINATING_OPERATION", True),
        ("STATUS_CONTEXT", True),
        ("OPTIONS_TRADEOFFS", True),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
        ("TARGET_REPOSITORY", False),
        ("ROADMAP_ISSUE", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]
    assert [(variable.name, variable.required) for variable in parse_input_variables(phase_readiness)] == [
        ("CURRENT_PHASE", False),
        ("TARGET_PHASE", False),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
        ("TARGET_REPOSITORY", False),
        ("ROADMAP_ISSUE", False),
        ("PM_FEEDBACK_HUMANO", False),
        ("PM_QUESTION_HUMANO", False),
    ]


def test_search_filter_matches_number_filename_and_title(tmp_path: Path) -> None:
    write_operation(tmp_path / "01-alpha.md", "Alpha Setup")
    write_operation(tmp_path / "02-beta.md", "Beta Review")
    operations = discover_operations(tmp_path)

    assert [operation.filename for operation in filter_operations(operations, "2")] == ["02-beta.md"]
    assert [operation.filename for operation in filter_operations(operations, "alpha")] == ["01-alpha.md"]
    assert [operation.filename for operation in filter_operations(operations, "review")] == ["02-beta.md"]
    assert resolve_operation_selection(operations, "02").filename == "02-beta.md"
    assert resolve_operation_selection(operations, "01-alpha.md").filename == "01-alpha.md"


def test_zero_padded_number_prefers_template_number_over_display_index(tmp_path: Path) -> None:
    write_operation(tmp_path / "00-activation.md", "Activation")
    write_operation(tmp_path / "01-adoption.md", "Adoption")
    operations = discover_operations(tmp_path)

    assert [operation.filename for operation in filter_operations(operations, "01")] == ["01-adoption.md"]
    assert resolve_operation_selection(operations, "1").filename == "00-activation.md"
    assert resolve_operation_selection(operations, "01").filename == "01-adoption.md"


def test_filter_operations_matches_by_phase(tmp_path: Path) -> None:
    write_operation(tmp_path / "01-alpha.md", "Alpha Setup")
    write_operation(tmp_path / "02-beta.md", "Beta Review")
    operations = discover_operations(tmp_path)
    phase_by_operation = {1: "Roadmap and issue planning", 2: "PR review and correction"}

    planning_matches = filter_operations(operations, "roadmap", phase_by_operation)
    assert [operation.filename for operation in planning_matches] == ["01-alpha.md"]

    review_matches = filter_operations(operations, "review and correction", phase_by_operation)
    assert [operation.filename for operation in review_matches] == ["02-beta.md"]

    # Existing filename/title search still works unaffected by the phase map.
    assert [operation.filename for operation in filter_operations(operations, "alpha", phase_by_operation)] == [
        "01-alpha.md"
    ]


def test_plain_text_phase_query_filters_instead_of_grouping(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-review-phase-readiness.md", "Review Phase Readiness")
    write_operation(operations_dir / "02-other.md", "Other")
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("phase", "1", "write", "exit"),
        output_stream=stream,
    )

    assert path is not None
    assert "# Review Phase Readiness" in path.read_text(encoding="utf-8")
    assert "Operations grouped by SDLC phase:" not in stream.getvalue()


def test_slash_phases_command_groups_operations(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-review-phase-readiness.md", "Review Phase Readiness")
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        # "/phases" groups and re-prompts for a query; "" keeps the list
        # before the selection prompt is reached.
        input_func=answers("/phases", "", "1", "write", "exit"),
        output_stream=stream,
    )

    assert path is not None
    assert "Operations grouped by SDLC phase:" in stream.getvalue()


def test_validate_common_variable_shapes() -> None:
    required_issue = InputVariable("ISSUE_NUMBER", "<ISSUE_NUMBER>", True, "")
    optional_roadmap = InputVariable("ROADMAP_ISSUE", "<ROADMAP_ISSUE>", False, "")
    repository = InputVariable("TARGET_REPOSITORY", "<TARGET_REPOSITORY>", True, "")
    count_limit = InputVariable("ISSUE_COUNT_LIMIT", "<ISSUE_COUNT_LIMIT>", False, "")
    scope_limit = InputVariable("SCOPE_LIMIT", "<SCOPE_LIMIT>", False, "")
    action = InputVariable("ROADMAP_ACTION", "<create|update>", False, "")

    assert validate_variable_value(required_issue, "") == (
        "ISSUE_NUMBER is required. Example: 123 or #123."
    )
    assert validate_variable_value(required_issue, "#123") is None
    assert validate_variable_value(required_issue, "0") == (
        "ISSUE_NUMBER must be a positive issue/PR number. Examples: 123 or #123."
    )
    assert validate_variable_value(optional_roadmap, "") is None
    assert validate_variable_value(repository, "codefusion-repo/project-os-v2") is None
    assert validate_variable_value(repository, "codefusion-repo") == (
        "TARGET_REPOSITORY must look like owner/repo. Example: codefusion-repo/project-os-v2."
    )
    assert validate_variable_value(count_limit, "3") is None
    assert validate_variable_value(count_limit, "0") == (
        "ISSUE_COUNT_LIMIT must be a positive integer. Example: 3."
    )
    assert validate_variable_value(scope_limit, "docs only") is None
    assert validate_variable_value(action, "create") is None
    assert validate_variable_value(action, "delete") == (
        "ROADMAP_ACTION must be one of the allowed placeholder choices: create, update. "
        "Example: create."
    )


def test_route_prompt_detection_uses_positive_output_block() -> None:
    route_text = "# Route\n\nINPUT:\n  (none)\n\nOUTPUT:\n  output.route_prompt for terminal work.\n"
    advisory_text = (
        "# Advisory\n\nINPUT:\n  (none)\n\nOUTPUT:\n  output.status_result.\n\n"
        "LIMITS:\n  Do not emit output.route_prompt.\n"
    )
    route_operation = OperationTemplate(1, Path("07-route.md"), "Route", route_text, ())
    advisory_operation = OperationTemplate(2, Path("35-advisory.md"), "Advisory", advisory_text, ())

    assert operation_produces_route_prompt(route_operation) is True
    assert operation_needs_pm_authorization_assistance(route_operation) is True
    assert operation_produces_route_prompt(advisory_operation) is False
    assert operation_needs_pm_authorization_assistance(advisory_operation) is False


def test_operation_30_defers_pm_authorization_status_at_initial_variable_entry() -> None:
    qa_text = (OPERATIONS_DIR / "30-process-human-qa-results.md").read_text(encoding="utf-8")
    operation = OperationTemplate(
        1,
        Path("30-process-human-qa-results.md"),
        "Procesar Resultados de QA Humano",
        qa_text,
        parse_input_variables(qa_text),
    )
    stream = io.StringIO()

    result = collect_values_with_controls(
        operation,
        input_func=answers("QA passed", "", "", ""),
        output_stream=stream,
    )

    assert result.action == "values"
    assert operation_output_refs(operation) == (
        "output.route_prompt",
        "output.pm_command_bundle",
        "output.status_result",
    )
    assert operation_requires_route_prompt_path_selection(operation) is True
    assert operation_needs_pm_authorization_assistance(operation) is False
    assert PM_AUTHORIZATION_STATUS_NAME not in [variable.name for variable in wizard_variables(operation)]
    assert PM_AUTHORIZATION_STATUS_NAME not in result.values
    assert "Required (1): QA_RESULT <QA_RESULT>" in stream.getvalue()
    assert "PM_AUTHORIZATION_STATUS" not in stream.getvalue()


def test_multi_output_route_prompt_path_can_include_pm_authorization_status() -> None:
    qa_text = (OPERATIONS_DIR / "30-process-human-qa-results.md").read_text(encoding="utf-8")
    operation = OperationTemplate(
        1,
        Path("30-process-human-qa-results.md"),
        "Procesar Resultados de QA Humano",
        qa_text,
        parse_input_variables(qa_text),
    )

    rendered = render_prompt(
        operation,
        {"QA_RESULT": "blocking failure", PM_AUTHORIZATION_STATUS_NAME: PM_AUTHORIZATION_GRANTED},
        include_route_prompt_authorization=True,
    )

    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in rendered


def test_multi_output_non_route_path_does_not_include_synthetic_pm_authorization_status() -> None:
    qa_text = (OPERATIONS_DIR / "30-process-human-qa-results.md").read_text(encoding="utf-8")
    operation = OperationTemplate(
        1,
        Path("30-process-human-qa-results.md"),
        "Procesar Resultados de QA Humano",
        qa_text,
        parse_input_variables(qa_text),
    )

    rendered = render_prompt(
        operation,
        {"QA_RESULT": "QA passed", PM_AUTHORIZATION_STATUS_NAME: PM_AUTHORIZATION_GRANTED},
    )

    assert PM_AUTHORIZATION_STATUS_NAME not in rendered


def test_pm_authorization_status_ui_text_is_compact_and_preserves_boundary_points() -> None:
    stream = io.StringIO()

    print_pm_authorization_assistance(stream)

    transcript = stream.getvalue()
    non_blank_lines = [line for line in transcript.splitlines() if line.strip()]
    assert non_blank_lines == [
        "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted for this exact scope and mode.",
        "Use 2 only for exact PM-approved scope/mode; generated prompt artifacts do not grant permission.",
        "Kernel evidence, branch preflight, validation, and fail-closed behavior still apply.",
    ]


def test_validate_pm_authorization_status_accepts_only_two_explicit_choices() -> None:
    variable = InputVariable(
        PM_AUTHORIZATION_STATUS_NAME,
        "<pending | granted for this exact scope and mode>",
        True,
        "",
    )

    assert validate_variable_value(variable, "") == (
        "PM_AUTHORIZATION_STATUS is required. "
        "Choose 1 for pending or 2 for granted for this exact scope and mode."
    )
    assert validate_variable_value(variable, "1") is None
    assert validate_variable_value(variable, "2") is None
    assert validate_variable_value(variable, PM_AUTHORIZATION_PENDING) is None
    assert validate_variable_value(variable, PM_AUTHORIZATION_GRANTED) is None

    invalid_values = [
        "draft",
        "read-only planning",
        "read_only",
        "planning",
        "approved",
        "granted",
    ]
    for value in invalid_values:
        assert normalize_pm_authorization_status(value) is None
        assert validate_variable_value(variable, value) == (
            "PM_AUTHORIZATION_STATUS must be 1, 2, pending, or "
            "granted for this exact scope and mode."
        )


def test_collect_values_reprompts_required_and_allows_optional_skip() -> None:
    operation = OperationTemplate(
        index=1,
        path=Path("01-test.md"),
        title="Test",
        text="",
        variables=(
            InputVariable("ISSUE_NUMBER", "<ISSUE_NUMBER>", True, ""),
            InputVariable("ROADMAP_ISSUE", "<ROADMAP_ISSUE>", False, ""),
        ),
    )
    stream = io.StringIO()

    values = collect_values(
        operation,
        input_func=answers("", "123", ""),
        output_stream=stream,
    )

    assert values == {"ISSUE_NUMBER": "123", "ROADMAP_ISSUE": ""}
    assert "Invalid value" in stream.getvalue()


def test_render_prompt_substitutes_values_inline_without_wrapper() -> None:
    text = "# Test Operation\n\nINPUT:\n  ISSUE_NUMBER=<ISSUE_NUMBER>\n\ncontent here\n"
    operation = OperationTemplate(
        index=1,
        path=Path("07-test.md"),
        title="Test Operation",
        text=text,
        variables=parse_input_variables(text),
    )

    rendered = render_prompt(operation, {"ISSUE_NUMBER": "123"})

    assert rendered == "# Test Operation\n\nINPUT:\n  ISSUE_NUMBER=123\n\ncontent here\n"


def test_generated_filename_is_deterministic_and_safe() -> None:
    operation = OperationTemplate(
        index=1,
        path=Path("01 Unsafe Name!.md"),
        title="Unsafe",
        text="",
        variables=(),
    )
    rendered = "prompt body"

    first = generated_filename(operation, rendered)
    second = generated_filename(operation, rendered)

    assert first == second
    assert first.endswith(".md")
    assert first.startswith("01-unsafe-name-")
    assert " " not in first
    assert "!" not in first


def test_output_dir_resolves_explicit_configured_and_default(tmp_path: Path, monkeypatch) -> None:
    explicit = tmp_path / "explicit"
    configured = tmp_path / "configured"

    assert resolve_output_dir(explicit) == explicit

    monkeypatch.setenv(OUTPUT_DIR_ENV, str(configured))
    assert resolve_output_dir(None) == configured

    monkeypatch.delenv(OUTPUT_DIR_ENV)
    assert resolve_output_dir(None) == DEFAULT_OUTPUT_DIR


def test_preview_confirmation_blocks_write_when_declined(tmp_path: Path) -> None:
    output_path = tmp_path / "prompt.md"
    operation = OperationTemplate(
        index=1, path=Path("01-test.md"), title="Test", text="", variables=()
    )

    confirmed = confirm_write(
        operation,
        {},
        "preview body",
        output_path,
        input_func=answers("n"),
        output_stream=io.StringIO(),
    )

    assert confirmed is False
    assert not output_path.exists()


def test_run_wizard_writes_only_after_preview_confirmation(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(
        operations_dir / "07-route.md",
        "Route",
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n  ROADMAP_ISSUE=<ROADMAP_ISSUE> optional",
    )
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "", "y", "exit"),
        output_stream=stream,
    )

    assert path is not None
    assert path.parent == output_dir
    assert path.suffix == ".md"
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=123" in text
    assert "ROADMAP_ISSUE=" in text
    assert "ROADMAP_ISSUE=(optional skipped)" not in text
    output = stream.getvalue()
    assert "[Step 1/3] Search and select an operation" in output
    assert "[Step 2/3] Fill INPUT variables" in output
    assert "[Step 3/3] Preview and choose next action" in output
    assert "Required (1): ISSUE_NUMBER <ISSUE_NUMBER>" in output
    assert "Optional (1): ROADMAP_ISSUE <ROADMAP_ISSUE>" in output
    assert "Actions: write, edit, operation, cancel, ? help." in output
    assert "Output mode: single latest prompt" in output
    assert "Exiting wizard session." in output


def test_run_wizard_route_prompt_auth_status_pending(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(
        operations_dir / "07-route.md",
        "Route",
        "  ISSUE_NUMBER=<ISSUE_NUMBER>",
    )
    operation_path = operations_dir / "07-route.md"
    operation_path.write_text(
        operation_path.read_text(encoding="utf-8")
        + "\nOUTPUT:\n  output.route_prompt per templates/route-prompt.md.\n",
        encoding="utf-8",
    )
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "1", "write", "exit"),
        output_stream=stream,
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=123" in text
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in text
    transcript = stream.getvalue()
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted for this exact scope and mode." in transcript
    assert "Kernel evidence, branch preflight, validation, and fail-closed behavior still apply." in transcript
    assert "generated prompt artifacts do not grant permission" in transcript


def test_run_wizard_route_prompt_auth_status_granted_exact_scope(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    (operations_dir / "08-route.md").write_text(
        "# Route\n\n"
        "INPUT:\n"
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n\n"
        "DO:\n  Set PM_AUTHORIZATION_STATUS per PM scope.\n\n"
        "OUTPUT:\n  output.route_prompt for scoped correction.\n",
        encoding="utf-8",
    )

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "2", "write", "exit"),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in text


def test_run_wizard_operation_30_route_path_requests_pm_authorization_status(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    (operations_dir / "30-process-human-qa-results.md").write_text(
        (OPERATIONS_DIR / "30-process-human-qa-results.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1",
            "Blocking QA failure",
            "",
            "",
            "",
            "1",
            "2",
            "write",
            "exit",
        ),
        output_stream=stream,
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "QA_RESULT=Blocking QA failure" in text
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in text
    transcript = stream.getvalue()
    assert "[Step 2b/3] Select output path" in transcript
    assert "This operation has multiple possible outputs" in transcript


def test_run_wizard_operation_30_non_route_path_omits_pm_authorization_status(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    (operations_dir / "30-process-human-qa-results.md").write_text(
        (OPERATIONS_DIR / "30-process-human-qa-results.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1",
            "QA passed",
            "",
            "",
            "",
            "2",
            "write",
            "exit",
        ),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "QA_RESULT=QA passed" in text
    assert PM_AUTHORIZATION_STATUS_NAME not in text


def test_run_wizard_does_not_infer_granted_authorization(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    (operations_dir / "07-route.md").write_text(
        "# Route\n\n"
        "INPUT:\n"
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n"
        "  BRANCH_NAME=<BRANCH_NAME>   # optional\n"
        "  PM_FEEDBACK_HUMANO=<PM_FEEDBACK_HUMANO>   # optional\n\n"
        "OUTPUT:\n  output.route_prompt per templates/route-prompt.md.\n",
        encoding="utf-8",
    )

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1",
            "349",
            "work/349-wizard-route-prompt-authorization-status",
            "PM previously discussed authorization",
            "1",
            "write",
            "exit",
        ),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in text
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" not in text


def test_run_wizard_can_search_again_before_write(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-alpha.md", "Alpha")
    write_operation(operations_dir / "02-beta.md", "Beta")

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("alpha", "s", "beta", "2", "write", "exit"),
        output_stream=io.StringIO(),
    )

    assert path is not None
    assert "# Beta" in path.read_text(encoding="utf-8")


def test_run_wizard_preview_can_return_to_edit_variables(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "07-route.md", "Route", "  ISSUE_NUMBER=<ISSUE_NUMBER>")

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "edit", "456", "write", "exit"),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=456" in text
    assert "ISSUE_NUMBER=123" not in text


def test_run_wizard_edit_can_clear_optional_variable(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(
        operations_dir / "07-route.md",
        "Route",
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n  ROADMAP_ISSUE=<ROADMAP_ISSUE> optional",
    )

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "274", "edit", "", "/clear", "write", "exit"),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=123" in text
    assert "ROADMAP_ISSUE=" in text
    assert "ROADMAP_ISSUE=274" not in text


def test_run_wizard_preview_can_return_to_operation_selection(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-alpha.md", "Alpha", "  ISSUE_NUMBER=<ISSUE_NUMBER>")
    write_operation(
        operations_dir / "02-beta.md",
        "Beta",
        "  TARGET_REPOSITORY=<TARGET_REPOSITORY>",
    )

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "operation", "", "2", "owner/repo", "write", "exit"),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "# Beta" in text
    assert "TARGET_REPOSITORY=owner/repo" in text
    assert "ISSUE_NUMBER=123" not in text


def test_run_wizard_does_not_write_when_preview_is_declined(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-test.md", "Test")

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "n"),
        output_stream=io.StringIO(),
    )

    assert path is None
    assert not output_dir.exists()


def test_run_wizard_cancel_during_variable_entry_writes_no_file(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-test.md", "Test", "  ISSUE_NUMBER=<ISSUE_NUMBER>")

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "cancel"),
        output_stream=io.StringIO(),
    )

    assert path is None
    assert not output_dir.exists()


def test_run_wizard_session_continues_after_write_until_explicit_exit(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-alpha.md", "Alpha", "  ISSUE_NUMBER=<ISSUE_NUMBER>")
    write_operation(
        operations_dir / "02-beta.md",
        "Beta",
        "  TARGET_REPOSITORY=<TARGET_REPOSITORY>",
    )
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1", "123", "write",  # write Alpha prompt
            "new",  # post-write: start another prompt
            "", "2", "owner/repo", "write",  # write Beta prompt
            "exit",
        ),
        output_stream=stream,
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "# Beta" in text

    md_files = list(output_dir.glob("*.md"))
    assert len(md_files) == 1
    assert md_files[0] == path
    assert "Removed previous generated prompt:" in stream.getvalue()


def test_run_wizard_same_action_resets_issue_number_but_keeps_stable_context(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(
        operations_dir / "07-route.md",
        "Route",
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n"
        "  ROADMAP_ISSUE=<ROADMAP_ISSUE> optional\n"
        "  TARGET_REPOSITORY=<TARGET_REPOSITORY> optional",
    )
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1",
            "100", "274", "codefusion-repo/project-os-v2", "write",  # first prompt
            "same",
            "200", "", "", "write",  # second prompt: ISSUE_NUMBER must be retyped
            "exit",
        ),
        output_stream=stream,
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=200" in text
    assert "ROADMAP_ISSUE=274" in text
    assert "TARGET_REPOSITORY=codefusion-repo/project-os-v2" in text

    md_files = list(output_dir.glob("*.md"))
    assert len(md_files) == 1


def test_run_wizard_edit_action_prefills_previous_values_including_reset_fields(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(
        operations_dir / "07-route.md",
        "Route",
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n  ROADMAP_ISSUE=<ROADMAP_ISSUE> optional",
    )

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1",
            "100", "274", "write",  # first prompt
            "edit",
            "", "", "write", "y",  # keep both values via Enter; same path exists, so confirm overwrite
            "exit",
        ),
        output_stream=io.StringIO(),
    )

    assert path is not None
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=100" in text
    assert "ROADMAP_ISSUE=274" in text

    md_files = list(output_dir.glob("*.md"))
    assert len(md_files) == 1


def test_run_wizard_post_write_path_action_shows_current_prompt(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-test.md", "Test")
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "write", "path", "exit"),
        output_stream=stream,
    )

    assert path is not None
    transcript = stream.getvalue()
    assert transcript.count(f"Current prompt: {path}") >= 2


def test_run_wizard_post_write_blank_enter_does_not_exit_session(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-test.md", "Test")
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "write", "", "path", "exit"),
        output_stream=stream,
    )

    assert path is not None
    # If blank Enter silently exited (the bug), "path" would never be
    # consumed and this line would only appear once, from the initial
    # session-state banner.
    transcript = stream.getvalue()
    assert transcript.count(f"Current prompt: {path}") >= 2


def test_run_wizard_cancel_during_second_attempt_returns_to_post_write_menu(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-test.md", "Test", "  ISSUE_NUMBER=<ISSUE_NUMBER>")

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1", "123", "write",  # first successful write
            "new",
            "", "1", "cancel",  # cancel the second attempt mid variable entry
            "exit",
        ),
        output_stream=io.StringIO(),
    )

    assert path is not None
    assert path.exists()
    md_files = list(output_dir.glob("*.md"))
    assert len(md_files) == 1
    assert md_files[0] == path


def test_carryover_values_keeps_only_stable_context() -> None:
    values = {
        "ISSUE_NUMBER": "123",
        "PR_NUMBER": "456",
        "PM_AUTHORIZATION_STATUS": PM_AUTHORIZATION_GRANTED,
        "ROADMAP_ISSUE": "274",
        "TARGET_REPOSITORY": "codefusion-repo/project-os-v2",
        "QA_RESULT": "pass",
    }

    assert carryover_values(values) == {
        "ROADMAP_ISSUE": "274",
        "TARGET_REPOSITORY": "codefusion-repo/project-os-v2",
    }
    assert is_carryover_variable("ROADMAP_ISSUE") is True
    assert is_carryover_variable("TARGET_REPOSITORY") is True
    assert is_carryover_variable("ISSUE_NUMBER") is False
    assert is_carryover_variable("PR_NUMBER") is False
    assert is_carryover_variable("PM_AUTHORIZATION_STATUS") is False
    assert is_carryover_variable("QA_RESULT") is False


def test_is_wizard_generated_artifact_requires_filename_and_marker(tmp_path: Path) -> None:
    genuine = tmp_path / "07-route-abcdef012345.md"
    genuine.write_text(f"content\n{WIZARD_PROMPT_MARKER}\n", encoding="utf-8")
    assert is_wizard_generated_artifact(genuine) is True

    looks_right_no_marker = tmp_path / "07-fake-abcdef012345.md"
    looks_right_no_marker.write_text("content without the marker\n", encoding="utf-8")
    assert is_wizard_generated_artifact(looks_right_no_marker) is False

    arbitrary = tmp_path / "notes.md"
    arbitrary.write_text(f"some notes\n{WIZARD_PROMPT_MARKER}\n", encoding="utf-8")
    assert is_wizard_generated_artifact(arbitrary) is False


def test_cleanup_only_removes_identifiable_wizard_artifacts(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    keep = output_dir / "07-route-111111111111.md"
    write_prompt(keep, "keep me")

    stale = output_dir / "07-route-222222222222.md"
    write_prompt(stale, "stale prompt")

    fake_pattern_no_marker = output_dir / "07-route-333333333333.md"
    fake_pattern_no_marker.write_text("looks generated but has no marker", encoding="utf-8")

    arbitrary_notes = output_dir / "notes.md"
    arbitrary_notes.write_text("arbitrary PM notes, do not delete", encoding="utf-8")

    removed = cleanup_previous_generated_prompts(output_dir, keep_path=keep)

    assert removed == [stale]
    assert keep.exists()
    assert not stale.exists()
    assert fake_pattern_no_marker.exists()
    assert arbitrary_notes.exists()


def test_find_replaceable_prompts_reports_every_stale_file_cleanup_will_remove(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    keep = output_dir / "07-route-111111111111.md"
    write_prompt(keep, "keep me")

    stale_one = output_dir / "07-route-222222222222.md"
    write_prompt(stale_one, "stale one")

    stale_two = output_dir / "07-route-333333333333.md"
    write_prompt(stale_two, "stale two")

    replacing = find_replaceable_prompts(output_dir, keep)
    assert sorted(replacing) == sorted([stale_one, stale_two])

    removed = cleanup_previous_generated_prompts(output_dir, keep_path=keep)
    assert sorted(removed) == sorted(replacing)
    assert keep.exists()
    assert not stale_one.exists()
    assert not stale_two.exists()


def test_cleanup_never_touches_files_outside_output_dir(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    sibling_dir = tmp_path / "sibling"
    sibling_dir.mkdir()

    keep = output_dir / "07-route-111111111111.md"
    write_prompt(keep, "keep me")

    outside = sibling_dir / "07-route-999999999999.md"
    write_prompt(outside, "outside prompt")

    removed = cleanup_previous_generated_prompts(output_dir, keep_path=keep)

    assert removed == []
    assert outside.exists()


def test_find_replaceable_prompt_reports_soft_notice_state(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    operations_dir.mkdir()
    write_operation(operations_dir / "01-alpha.md", "Alpha", "  ISSUE_NUMBER=<ISSUE_NUMBER>")
    write_operation(
        operations_dir / "02-beta.md",
        "Beta",
        "  TARGET_REPOSITORY=<TARGET_REPOSITORY>",
    )
    stream = io.StringIO()

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "", "1", "123", "write",
            "new",
            "", "2", "owner/repo", "write",
            "exit",
        ),
        output_stream=stream,
    )

    assert path is not None
    output = stream.getvalue()
    assert "No previous wizard-generated prompt exists to replace yet." in output
    assert "The previous prompt generated by this wizard in the output folder will be replaced." in output


def test_load_phase_map_parses_real_operation_flows_doc() -> None:
    phase_by_operation = load_phase_map()

    assert phase_by_operation[0] == "Activation and state review"
    assert phase_by_operation[7] == "Implementation routing"
    assert phase_by_operation[34] == "Manual implementation planning"


def test_print_phase_groups_groups_operations(tmp_path: Path) -> None:
    write_operation(tmp_path / "01-alpha.md", "Alpha")
    write_operation(tmp_path / "02-beta.md", "Beta")
    operations = discover_operations(tmp_path)
    phase_by_operation = {1: "Planning", 2: "Review"}
    stream = io.StringIO()

    print_phase_groups(operations, phase_by_operation, stream)

    output = stream.getvalue()
    assert "Planning:" in output
    assert "Review:" in output
    assert "01-alpha.md" in output
    assert "02-beta.md" in output


def test_wizard_source_has_no_command_or_network_execution_imports() -> None:
    source = (REPO_ROOT / "tools" / "operation_prompt_wizard.py").read_text(encoding="utf-8")

    assert "import subprocess" not in source
    assert "subprocess." not in source
    assert "os.system" not in source
    assert "os.popen" not in source
    assert "import git" not in source
    assert "from git" not in source
    assert "import shlex" not in source
    assert "urllib.request" not in source
    assert "http.client" not in source
    assert "import socket" not in source
    assert "import requests" not in source


def test_build_parser_adds_no_cleanup_or_session_flags() -> None:
    from tools.operation_prompt_wizard import build_parser

    parser = build_parser()
    dests = {action.dest for action in parser._actions}

    assert dests == {"help", "operations_dir", "output_dir"}
