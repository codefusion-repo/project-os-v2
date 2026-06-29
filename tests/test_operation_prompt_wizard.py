"""Tests for the local operation prompt wizard."""

from __future__ import annotations

import io
from pathlib import Path

from tools.operation_prompt_wizard import (
    DEFAULT_OUTPUT_DIR,
    InputVariable,
    OperationTemplate,
    OUTPUT_DIR_ENV,
    collect_values,
    confirm_write,
    discover_operations,
    filter_operations,
    generated_filename,
    parse_input_variables,
    render_prompt,
    resolve_operation_selection,
    resolve_output_dir,
    run_wizard,
    validate_variable_value,
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
        ("ISSUE_NUMBER", True),
        ("ROADMAP_ISSUE", False),
    ]

    roadmap_vars = parse_input_variables(bounded_roadmap)
    assert [(variable.name, variable.required) for variable in roadmap_vars] == [
        ("ROADMAP_ISSUE", True),
        ("ISSUE_COUNT_LIMIT", False),
        ("SCOPE_LIMIT", False),
    ]

    audit_vars = parse_input_variables(audit)
    assert [(variable.name, variable.required) for variable in audit_vars] == [
        ("TARGET_REPOSITORY", True),
        ("PATH_SCOPE", False),
        ("FOCUS", False),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
    ]
    assert parse_input_variables(handoff) == ()


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


def test_validate_common_variable_shapes() -> None:
    required_issue = InputVariable("ISSUE_NUMBER", "<ISSUE_NUMBER>", True, "")
    optional_roadmap = InputVariable("ROADMAP_ISSUE", "<ROADMAP_ISSUE>", False, "")
    repository = InputVariable("TARGET_REPOSITORY", "<TARGET_REPOSITORY>", True, "")
    count_limit = InputVariable("ISSUE_COUNT_LIMIT", "<ISSUE_COUNT_LIMIT>", False, "")
    scope_limit = InputVariable("SCOPE_LIMIT", "<SCOPE_LIMIT>", False, "")
    action = InputVariable("ROADMAP_ACTION", "<create|update>", False, "")

    assert validate_variable_value(required_issue, "") == "ISSUE_NUMBER is required."
    assert validate_variable_value(required_issue, "#123") is None
    assert validate_variable_value(required_issue, "0") is not None
    assert validate_variable_value(optional_roadmap, "") is None
    assert validate_variable_value(repository, "codefusion-repo/project-os-v2") is None
    assert validate_variable_value(repository, "codefusion-repo") is not None
    assert validate_variable_value(count_limit, "3") is None
    assert validate_variable_value(count_limit, "0") is not None
    assert validate_variable_value(scope_limit, "docs only") is None
    assert validate_variable_value(action, "create") is None
    assert validate_variable_value(action, "delete") is not None


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


def test_render_prompt_includes_filled_input_and_template() -> None:
    text = "# Test Operation\n\nINPUT:\n  ISSUE_NUMBER=<ISSUE_NUMBER>\n"
    operation = OperationTemplate(
        index=1,
        path=Path("07-test.md"),
        title="Test Operation",
        text=text,
        variables=parse_input_variables(text),
    )

    rendered = render_prompt(operation, {"ISSUE_NUMBER": "123"})

    assert "# Generated Operation Prompt: Test Operation" in rendered
    assert "Source template: 07-test.md" in rendered
    assert "  ISSUE_NUMBER=123" in rendered
    assert "## Operation Template" in rendered
    assert text.rstrip() in rendered
    assert "does not execute the operation" in rendered


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

    confirmed = confirm_write(
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

    path = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers("", "1", "123", "", "y"),
        output_stream=io.StringIO(),
    )

    assert path is not None
    assert path.parent == output_dir
    assert path.suffix == ".md"
    text = path.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=123" in text
    assert "ROADMAP_ISSUE=(optional skipped)" in text


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


def test_wizard_source_has_no_command_or_network_execution_imports() -> None:
    source = (REPO_ROOT / "tools" / "operation_prompt_wizard.py").read_text(encoding="utf-8")

    assert "import subprocess" not in source
    assert "os.system" not in source
    assert "urllib.request" not in source
    assert "http.client" not in source
    assert "import socket" not in source
    assert "import requests" not in source
