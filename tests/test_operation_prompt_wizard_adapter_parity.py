"""Semantic parity between the two wizard adapters over the shared session core."""

from __future__ import annotations

from pathlib import Path
from io import StringIO
import subprocess
import sys

import pytest

import tools.operation_prompt_wizard as wizard


def write_route_operation(path: Path) -> Path:
    path.mkdir()
    (path / "MOS-3.5-route.md").write_text(
        "# MOS-3.5 — Route\n\n**Variables**\n"
        "- Required: ISSUE_NUMBER\n"
        "- Optional: — (none)\n\n"
        "**Deliver:** output.route_prompt.\n",
        encoding="utf-8",
    )
    return path


def answers(*values: str):
    iterator = iter(values)
    return lambda _prompt: next(iterator)


@pytest.mark.skipif(not wizard.HAVE_PROMPT_TOOLKIT, reason="prompt_toolkit is unavailable")
def test_line_and_prompt_toolkit_adapters_render_the_same_route_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = write_route_operation(tmp_path / "operations")
    line_path = wizard.run_wizard(
        operations_dir=operations,
        output_dir=tmp_path / "line-output",
        input_func=answers("MOS-3.5", "490", "1", "write", "exit"),
    )

    prompt_values = ["MOS-3.5", "490", "1", "write", "exit"]

    def prompt(*_args, **_kwargs):
        if not prompt_values:
            raise EOFError
        return prompt_values.pop(0)

    monkeypatch.setattr(wizard, "prompt", prompt)
    prompt_toolkit_path = wizard.run_wizard_pt(
        operations_dir=operations,
        output_dir=tmp_path / "prompt-toolkit-output",
    )

    assert line_path is not None
    assert prompt_toolkit_path is not None
    assert line_path.read_text(encoding="utf-8") == prompt_toolkit_path.read_text(encoding="utf-8")


def test_import_without_site_packages_uses_the_line_based_fallback() -> None:
    """The optional prompt_toolkit adapter must not make the entrypoint unavailable."""

    completed = subprocess.run(
        [
            sys.executable,
            "-S",
            "-c",
            (
                "from io import StringIO; "
                "from tools.operation_prompt_wizard import HAVE_PROMPT_TOOLKIT, run_wizard; "
                "assert not HAVE_PROMPT_TOOLKIT; "
                "assert run_wizard(language='es', input_func=lambda _: 'cancel', "
                "output_stream=StringIO()) is None"
            ),
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr


def test_documented_direct_script_entrypoint_resolves_its_package() -> None:
    completed = subprocess.run(
        [sys.executable, "-S", "tools/operation_prompt_wizard.py", "--language", "es"],
        cwd=Path(__file__).resolve().parents[1],
        input="cancel\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    assert "ModuleNotFoundError" not in completed.stderr
    assert "Session surface: es" in completed.stdout


@pytest.mark.skipif(not wizard.HAVE_PROMPT_TOOLKIT, reason="prompt_toolkit is unavailable")
@pytest.mark.parametrize("language", ("es", "en"))
@pytest.mark.parametrize("intent", (
    "Implement the live issue example/target#42 within its scope; no merge or close.",
    "Prepare implementation of the next roadmap outcome in example/target; a formal unit is still needed.",
    "I want to proceed but have not decided which of two outcomes to prioritize.",
))
def test_intent_uses_one_capture_and_one_preview_in_both_adapters(
    language: str, intent: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    artifacts = []
    for adapter in ("line", "prompt_toolkit"):
        remaining = [intent, "write", "exit"]
        calls = []

        def answer(*args, **kwargs):
            calls.append(args)
            assert remaining, "Unexpected recapture or selection question"
            return remaining.pop(0)

        kwargs = dict(language=language, output_dir=tmp_path / adapter, output_stream=StringIO())
        if adapter == "line":
            path = wizard.run_wizard(input_func=answer, **kwargs)
        else:
            monkeypatch.setattr(wizard, "prompt", answer)
            path = wizard.run_wizard_pt(**kwargs)
        assert path is not None
        assert len(calls) == 3
        assert remaining == []
        content = path.read_text(encoding="utf-8")
        assert f"PM_QUESTION_HUMANO={intent}\n" in content
        assert "PM_AUTHORIZATION_STATUS=" not in content
        artifacts.append(content)
    assert artifacts[0] == artifacts[1]
