"""Enhanced prompt_toolkit parity tests over MOS-style Spanish catalogs."""

from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import (
    DEFAULT_OPERATIONS_DIR,
    HYDRATION_LEVEL_DEFAULT,
    HYDRATION_LEVEL_NAME,
    HAVE_PROMPT_TOOLKIT,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
    PM_AUTHORIZATION_STATUS_NAME,
)

if not HAVE_PROMPT_TOOLKIT:
    pytest.skip("prompt_toolkit not installed; enhanced wizard path unavailable", allow_module_level=True)

from tools.operation_prompt_wizard import run_wizard_pt
from prompt_toolkit.formatted_text import fragment_list_to_text, to_formatted_text


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


@pytest.mark.parametrize(
    ("command", "confirmation"),
    [
        ("/enumerated", "View: enumerated operations"),
        ("/enumerator", "View: enumerated operations"),
        ("/", "View: enumerated operations"),
        ("/phases", "View: operations grouped by phase"),
        ("/phase", "View: operations grouped by phase"),
    ],
)
def test_prompt_toolkit_view_commands_render_and_allow_direct_selection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    confirmation: str,
) -> None:
    operations = setup_catalog(tmp_path)
    stream = StringIO()
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([command, "MOS-3.5", "codefusion-repo/project-os-v2", "write", "exit"]),
    )
    result = run_wizard_pt(
        operations_dir=operations,
        output_dir=tmp_path / "out",
        output_stream=stream,
    )

    assert result is not None
    assert confirmation in stream.getvalue()


def test_cancel_at_selection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = setup_catalog(tmp_path)
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt(["cancel"]))
    assert run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out") is None


def test_language_question_empty_answer_keeps_spanish_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt(["", "cancel"]))
    stream = StringIO()
    assert run_wizard_pt(output_dir=tmp_path / "out", output_stream=stream) is None
    transcript = stream.getvalue()
    assert "Session surface: es (session-only" in transcript
    assert "Operations catalog: project-os-es/operaciones" in transcript
    assert "Skills catalog: project-os-es/kernel/skills.json" in transcript


def test_language_question_rejects_unknown_then_selects_english(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt(["fr", "en", "cancel"]))
    stream = StringIO()
    assert run_wizard_pt(output_dir=tmp_path / "out", output_stream=stream) is None
    transcript = stream.getvalue()
    assert "Unknown language 'fr'" in transcript
    assert "Session surface: en (session-only" in transcript
    assert "Operations catalog: project-os-en/operations" in transcript
    assert "Skills catalog: project-os-en/kernel/skills.json" in transcript


def test_explicit_language_option_skips_the_question(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", mock_prompt(["cancel"]))
    stream = StringIO()
    assert run_wizard_pt(language="en", output_dir=tmp_path / "out", output_stream=stream) is None
    transcript = stream.getvalue()
    assert "Session surface: en (session-only" in transcript
    assert "Kernel (reference only, not applied): project-os-en/kernel" in transcript


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


def test_active_mos35_collects_authorization_and_never_requests_agent_family(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stream = StringIO()
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.5", "405", "", "none", "", "", "", "1", "write", "exit",
        ]),
    )
    result = run_wizard_pt(
        operations_dir=DEFAULT_OPERATIONS_DIR,
        output_dir=tmp_path / "out",
        output_stream=stream,
    )

    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert f"{HYDRATION_LEVEL_NAME}={HYDRATION_LEVEL_DEFAULT}" in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    transcript = stream.getvalue()
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted" in transcript
    assert "Optional (5): PR_NUMBER <PR_NUMBER>, OPTIONAL_SKILL <OPTIONAL_SKILL>, HYDRATION_LEVEL <HYDRATION_LEVEL>, PM_FEEDBACK_HUMANO <PM_FEEDBACK_HUMANO>, PM_QUESTION_HUMANO <PM_QUESTION_HUMANO>" in transcript
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY (" not in transcript


def test_active_mos34_collects_authorization_in_prompt_toolkit_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stream = StringIO()
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.4", "405", "274", "skill.arquitectura_backend", "", "", "", "2", "write", "exit",
        ]),
    )
    result = run_wizard_pt(
        operations_dir=DEFAULT_OPERATIONS_DIR,
        output_dir=tmp_path / "out",
        output_stream=stream,
    )

    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert f"{HYDRATION_LEVEL_NAME}={HYDRATION_LEVEL_DEFAULT}" in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "OPTIONAL_SKILL=skill.arquitectura_backend" in content
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted" in stream.getvalue()


def test_prompt_toolkit_skill_completion_uses_active_catalog(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    operations = tmp_path / "operaciones"
    write_operation(
        operations / "fase-3" / "MOS-3.1-skill.md",
        "MOS-3.1",
        "Skill",
        "— (ninguna)",
        "OPTIONAL_SKILL",
    )
    completers = []
    toolbars = []
    skill_completion_is_live = []

    def recording_prompt(*_args, **kwargs):
        completer = kwargs.get("completer")
        if completer is not None:
            completers.append(completer)
            if kwargs.get("complete_while_typing"):
                skill_completion_is_live.append(True)
        toolbar = kwargs.get("bottom_toolbar")
        if toolbar is not None:
            rendered = toolbar() if callable(toolbar) else toolbar
            toolbars.append(fragment_list_to_text(to_formatted_text(rendered)))
        inputs = recording_prompt.inputs
        if not inputs:
            raise EOFError
        return inputs.pop(0)

    recording_prompt.inputs = ["MOS-3.1", "skill.desarrollo_frontend", "write", "exit"]
    monkeypatch.setattr("tools.operation_prompt_wizard.prompt", recording_prompt)
    stream = StringIO()
    result = run_wizard_pt(
        operations_dir=operations,
        output_dir=tmp_path / "out",
        output_stream=stream,
    )

    assert result is not None
    assert "OPTIONAL_SKILL=skill.desarrollo_frontend" in result.read_text(encoding="utf-8")
    assert any(
        {"skill.arquitectura_backend", "skill.desarrollo_frontend", "none"}
        <= set(getattr(completer, "words", []))
        for completer in completers
    )
    assert skill_completion_is_live == [True]
    transcript = stream.getvalue()
    assert "OPTIONAL_SKILL (optional)" in transcript
    assert "skill.arquitectura_backend — Arquitectura backend" in transcript
    assert "skill.desarrollo_frontend — Desarrollo frontend" in transcript
    assert "none — Sin skill opcional" in transcript
    selection_toolbar = next(text for text in toolbars if "/enumerated" in text)
    for command in ("/enumerated", "/enumerator", "/phases", "/phase"):
        assert command in selection_toolbar


def test_prompt_toolkit_pseudo_tty_keeps_views_and_skill_options_visible(tmp_path: Path) -> None:
    script = shutil.which("script")
    if script is None:
        pytest.skip("script utility is required for the pseudo-TTY black-box")

    output_dir = tmp_path / "out"
    command = (
        f"{shlex.quote(sys.executable)} -m tools.operation_prompt_wizard "
        f"--output-dir {shlex.quote(str(output_dir))}"
    )
    completed = subprocess.run(
        [script, "-qec", command, "/dev/null"],
        cwd=Path(__file__).resolve().parents[1],
        input="\n/enumerator\n/phases\nMOS-3.4\n405\n274\ncancel\n",
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )

    transcript = completed.stdout
    assert "View: enumerated operations" in transcript
    assert "View: operations grouped by phase" in transcript
    assert "OPTIONAL_SKILL (optional)" in transcript
    assert "skill.arquitectura_backend — Arquitectura backend" in transcript
    assert "skill.desarrollo_frontend — Desarrollo frontend" in transcript
    assert "Select OPTIONAL_SKILL:" in transcript
    assert not list(output_dir.glob("*.md"))


def test_mos_r3_prompt_toolkit_pseudo_tty_recovers_after_invalid_numeric_reference(
    tmp_path: Path,
) -> None:
    script = shutil.which("script")
    if script is None:
        pytest.skip("script utility is required for the pseudo-TTY black-box")

    output_dir = tmp_path / "out"
    command = (
        f"{shlex.quote(sys.executable)} -m tools.operation_prompt_wizard "
        f"--language es --output-dir {shlex.quote(str(output_dir))}"
    )
    completed = subprocess.run(
        [script, "-qec", command, "/dev/null"],
        cwd=Path(__file__).resolve().parents[1],
        input="MOS-R.3\nMOS-3.7 review\nfalse\nissue #429\n429\ncancel\n",
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )

    assert completed.returncode == 1
    assert "Invalid value: ISSUE_NUMBER must be a positive issue/PR number" in completed.stdout
    assert "PR_NUMBER (optional, <PR_NUMBER>):" in completed.stdout
    assert not list(output_dir.glob("*.md"))
