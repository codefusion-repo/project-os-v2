import io

import pytest
from pathlib import Path

from tools.operation_prompt_wizard import (
    HAVE_PROMPT_TOOLKIT,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_STATUS_NAME,
)

if not HAVE_PROMPT_TOOLKIT:
    pytest.skip("prompt_toolkit not installed, skipping enhanced interaction tests", allow_module_level=True)

from tools.operation_prompt_wizard import run_wizard_pt


def setup_mock_operations(tmp_path: Path):
    ops_dir = tmp_path / "operations"
    ops_dir.mkdir()
    (ops_dir / "01-test-op.md").write_text("# Test Operation\n\nINPUT:\n  TARGET_REPOSITORY=<owner/repo>\n\ncontent here")
    return ops_dir


def make_mock_prompt(inputs):
    """Return a prompt() replacement that raises EOFError once inputs run out."""

    def mock_prompt(*args, **kwargs):
        if not inputs:
            raise EOFError
        return inputs.pop(0)

    return mock_prompt


def test_run_wizard_pt_full_flow(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"

    inputs = [
        "01",  # select operation
        "codefusion-repo/project-os-v2",  # variable TARGET_REPOSITORY
        "write",  # write preview action
        "exit",  # end the session
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is not None
    assert result.exists()
    assert "TARGET_REPOSITORY=codefusion-repo/project-os-v2" in result.read_text()


def test_run_wizard_pt_cancel_selection(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"

    inputs = ["cancel"]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is None


def test_run_wizard_pt_cancel_variable_entry(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"

    inputs = [
        "01",  # select operation
        "cancel",  # variable TARGET_REPOSITORY
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is None


def test_run_wizard_pt_edit_flow(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    out_dir = tmp_path / "out"

    inputs = [
        "01",  # select operation
        "codefusion-repo/project-os-v2",  # variable TARGET_REPOSITORY
        "edit",  # choose edit
        "codefusion-repo/other-repo",  # edit TARGET_REPOSITORY
        "write",  # choose write
        "exit",
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is not None
    assert "TARGET_REPOSITORY=codefusion-repo/other-repo" in result.read_text()


def test_run_wizard_pt_back_flow(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    (ops_dir / "02-test-op.md").write_text("# Second Operation\n\nINPUT:\n  OTHER_VAR=<foo>\n\ncontent here")
    out_dir = tmp_path / "out"

    inputs = [
        "01",  # select operation
        "back",  # variable TARGET_REPOSITORY -> returns 'operation'
        "02",  # select second operation
        "myval",  # variable OTHER_VAR
        "write",  # choose write
        "exit",
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)
    assert result is not None
    text = result.read_text()
    assert "OTHER_VAR=myval" in text
    assert "Second Operation" in text


def test_run_wizard_pt_session_continues_with_new_action_for_multiple_prompts(tmp_path: Path, monkeypatch):
    ops_dir = setup_mock_operations(tmp_path)
    (ops_dir / "02-second-op.md").write_text("# Second Operation\n\nINPUT:\n  OTHER_VAR=<foo>\n\ncontent here")
    out_dir = tmp_path / "out"

    inputs = [
        "01", "codefusion-repo/project-os-v2", "write",  # first prompt
        "new",  # post-write: start another prompt in the same session
        "02", "myval", "write",  # second prompt
        "exit",
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)

    assert result is not None
    assert "Second Operation" in result.read_text()

    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) == 1
    assert md_files[0] == result


def test_run_wizard_pt_same_action_resets_issue_number_but_keeps_roadmap_issue(tmp_path: Path, monkeypatch):
    ops_dir = tmp_path / "operations"
    ops_dir.mkdir()
    (ops_dir / "07-route.md").write_text(
        "# Route\n\nINPUT:\n  ISSUE_NUMBER=<ISSUE_NUMBER>\n  ROADMAP_ISSUE=<ROADMAP_ISSUE> optional\n\ncontent here"
    )
    out_dir = tmp_path / "out"

    inputs = [
        "07", "100", "274", "write",  # first prompt
        "same",
        # ISSUE_NUMBER has no carried-over default (reset); ROADMAP_ISSUE's
        # prompt_toolkit default is the carried-over value, resubmitted here
        # since the mocked prompt() does not render defaults itself.
        "200", "274",
        "write",
        "exit",
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir)

    assert result is not None
    text = result.read_text()
    assert "ISSUE_NUMBER=200" in text
    assert "ROADMAP_ISSUE=274" in text

    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) == 1


def test_run_wizard_pt_route_prompt_auth_status_granted(tmp_path: Path, monkeypatch):
    ops_dir = tmp_path / "operations"
    ops_dir.mkdir()
    (ops_dir / "07-route.md").write_text(
        "# Route\n\n"
        "INPUT:\n"
        "  ISSUE_NUMBER=<ISSUE_NUMBER>\n\n"
        "OUTPUT:\n"
        "  output.route_prompt per templates/route-prompt.md.\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "out"
    stream = io.StringIO()

    inputs = [
        "07",
        "349",
        "2",
        "write",
        "exit",
    ]

    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", make_mock_prompt(inputs))

    result = run_wizard_pt(operations_dir=ops_dir, output_dir=out_dir, output_stream=stream)

    assert result is not None
    text = result.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in text
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted for this exact scope and mode." in stream.getvalue()
