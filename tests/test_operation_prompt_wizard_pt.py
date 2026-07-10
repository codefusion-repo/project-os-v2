"""Enhanced prompt_toolkit parity tests over MOS-style Spanish catalogs."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import (
    HAVE_PROMPT_TOOLKIT,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_STATUS_NAME,
)

if not HAVE_PROMPT_TOOLKIT:
    pytest.skip("prompt_toolkit not installed; enhanced wizard path unavailable", allow_module_level=True)

from tools.operation_prompt_wizard import run_wizard_pt


def write_operation(
    path: Path,
    code: str,
    title: str,
    required: str,
    optional: str = "— (ninguna)",
    delivery: str = "output.status_result",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# {code} — {title}\n\n"
        "**Variables**\n"
        f"- Requeridas: {required}\n"
        f"- Opcionales: {optional}\n\n"
        f"**Entrega:** {delivery}.\n",
        encoding="utf-8",
    )


def setup_catalog(tmp_path: Path) -> Path:
    operations = tmp_path / "operaciones"
    write_operation(
        operations / "fase-3" / "MOS-3.5-correccion.md",
        "MOS-3.5",
        "Corrección",
        "TARGET_REPOSITORY",
    )
    return operations


def mock_prompt(inputs: list[str]):
    def replacement(*_args, **_kwargs):
        if not inputs:
            raise EOFError
        return inputs.pop(0)

    return replacement


def test_full_flow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt(["MOS-3.5", "codefusion-repo/project-os-v2", "write", "exit"]),
    )
    result = run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out")

    assert result is not None
    assert "TARGET_REPOSITORY=codefusion-repo/project-os-v2" in result.read_text(encoding="utf-8")


def test_cancel_at_selection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt(["cancel"]))
    assert run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out") is None


def test_cancel_during_value_entry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt(["MOS-3.5", "cancel"]))
    assert run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out") is None


def test_edit_flow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.5", "codefusion-repo/project-os-v2", "edit",
            "codefusion-repo/otro", "write", "exit",
        ]),
    )
    result = run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out")

    assert result is not None
    assert "TARGET_REPOSITORY=codefusion-repo/otro" in result.read_text(encoding="utf-8")


def test_back_flow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    write_operation(
        operations / "fase-4" / "MOS-4.1-qa.md", "MOS-4.1", "QA", "PR_NUMBER"
    )
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt(["MOS-3.5", "back", "MOS-4.1", "406", "write", "exit"]),
    )
    result = run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out")

    assert result is not None
    assert "PR_NUMBER=406" in result.read_text(encoding="utf-8")


def test_session_new_keeps_only_latest_prompt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    write_operation(
        operations / "fase-4" / "MOS-4.1-qa.md", "MOS-4.1", "QA", "PR_NUMBER"
    )
    output_dir = tmp_path / "out"
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.5", "codefusion-repo/project-os-v2", "write", "new",
            "MOS-4.1", "406", "write", "exit",
        ]),
    )
    result = run_wizard_pt(operations_dir=operations, output_dir=output_dir)

    assert result is not None
    assert "MOS-4.1" in result.read_text(encoding="utf-8")
    assert list(output_dir.glob("*.md")) == [result]


def test_same_resets_issue_and_keeps_roadmap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = tmp_path / "operaciones"
    write_operation(
        operations / "fase-3" / "MOS-3.4-route.md",
        "MOS-3.4",
        "Route",
        "ISSUE_NUMBER",
        "ROADMAP_ISSUE",
    )
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.4", "100", "274", "write", "same",
            "200", "274", "write", "exit",
        ]),
    )
    result = run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out")

    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=200" in content
    assert "ROADMAP_ISSUE=274" in content


def test_route_prompt_authorization_granted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = tmp_path / "operaciones"
    write_operation(
        operations / "fase-3" / "MOS-3.5-route.md",
        "MOS-3.5",
        "Route",
        "ISSUE_NUMBER",
        delivery="output.route_prompt",
    )
    stream = StringIO()
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt(["MOS-3.5", "405", "2", "write", "exit"]),
    )
    result = run_wizard_pt(
        operations_dir=operations,
        output_dir=tmp_path / "out",
        output_stream=stream,
    )

    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted" in stream.getvalue()
