"""Enhanced prompt_toolkit parity tests over MOS-style Spanish catalogs."""

from __future__ import annotations

import asyncio
import shlex
import shutil
import subprocess
import sys
from contextlib import suppress
from io import StringIO
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import (
    DEFAULT_OPERATIONS_DIR,
    HYDRATION_LEVEL_NAME,
    HAVE_PROMPT_TOOLKIT,
    INTENT_ROUTING_MOS_CODE,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
    PM_AUTHORIZATION_STATUS_NAME,
    PM_QUESTION_HUMANO_NAME,
    REPO_ROOT,
    collect_values_with_controls,
    discover_operations,
    resolve_operation_selection,
    surface_selection_for_language,
)

if not HAVE_PROMPT_TOOLKIT:
    pytest.skip("prompt_toolkit not installed; enhanced wizard path unavailable", allow_module_level=True)

from tools.operation_prompt_wizard import (
    OperationCompleter,
    OperationValidator,
    PromptToolkitWizardAdapter,
    run_wizard_pt,
)
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import fragment_list_to_text, to_formatted_text
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.shortcuts import PromptSession


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


def setup_catalog_with_intent_router(tmp_path: Path) -> Path:
    operations = setup_catalog(tmp_path)
    write_operation(
        operations / "cross-fase" / f"{INTENT_ROUTING_MOS_CODE}-recomendar-siguiente-operacion.md",
        INTENT_ROUTING_MOS_CODE,
        "Recomendar la siguiente operación",
        "— (ninguna)",
        optional="ROUTING_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO",
    )
    return operations


def mock_prompt(inputs: list[str]):
    def replacement(*_args, **_kwargs):
        if not inputs:
            raise EOFError
        return inputs.pop(0)

    return replacement


def select_with_prompt_toolkit(
    operations,
    inputs: list[str],
    monkeypatch: pytest.MonkeyPatch,
):
    calls: list[str] = []

    def replacement(label: str, **_kwargs) -> str:
        calls.append(label)
        if not inputs:
            raise EOFError
        return inputs.pop(0)

    monkeypatch.setattr(
        "tools.operation_prompt_wizard_prompt_toolkit_ui.prompt", replacement
    )
    operation, captured_intent = PromptToolkitWizardAdapter(StringIO()).select(operations, {})
    return operation, captured_intent, calls


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


@pytest.mark.parametrize(
    ("language", "operations_dir"),
    (
        ("es", REPO_ROOT / "project-os-es" / "operaciones"),
        ("en", REPO_ROOT / "project-os-en" / "operations"),
    ),
)
def test_prompt_toolkit_dynamic_selection_resolves_maintenance_aliases(
    language: str, operations_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = discover_operations(operations_dir)

    alias, captured_intent, calls = select_with_prompt_toolkit(
        operations, ["MOS-6.3"], monkeypatch
    )

    assert alias is not None
    assert alias.mos_code == "MOS-6.3"
    assert alias.resolved_canonical_code == "MOS-6.13"
    assert alias.alias_focus_area == "performance"
    assert captured_intent == {}
    assert calls


def test_operation_validator_accepts_intent_text_when_catalog_has_intent_router(
    tmp_path: Path,
) -> None:
    operations = discover_operations(setup_catalog_with_intent_router(tmp_path))
    validator = OperationValidator(operations)

    validator.validate(Document("free-form intent that names no catalog operation"))


def test_operation_validator_still_rejects_unmatched_text_without_intent_router(
    tmp_path: Path,
) -> None:
    operations = discover_operations(setup_catalog(tmp_path))
    validator = OperationValidator(operations)

    with pytest.raises(Exception, match="Invalid or ambiguous selection"):
        validator.validate(Document("free-form intent that names no catalog operation"))


@pytest.mark.parametrize("selector", ["index", "mos", "filename", "relative_path"])
def test_prompt_toolkit_exact_selection_stays_a_single_direct_interaction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, selector: str
) -> None:
    operations = discover_operations(setup_catalog_with_intent_router(tmp_path))
    target = next(operation for operation in operations if operation.mos_code == "MOS-3.5")
    selection = {
        "index": str(target.index),
        "mos": target.mos_code,
        "filename": target.filename,
        "relative_path": target.relative_path,
    }[selector]
    monkeypatch.setattr(
        "tools.operation_prompt_wizard_prompt_toolkit_ui.line_ui.select_operation",
        lambda *_args, **_kwargs: pytest.fail("prompt_toolkit must not delegate selection to line UI"),
    )

    selected, captured_intent, calls = select_with_prompt_toolkit(
        operations, [selection], monkeypatch
    )

    assert selected is not None
    assert selected.mos_code == "MOS-3.5"
    assert captured_intent == {}
    assert len(calls) == 1


def test_prompt_toolkit_partial_and_ambiguous_search_keep_completions_and_route_directly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations_path = setup_catalog_with_intent_router(tmp_path)
    write_operation(
        operations_path / "fase-3" / "MOS-3.6-correccion-extra.md",
        "MOS-3.6",
        "Corrección extra",
        "PR_NUMBER",
    )
    operations = discover_operations(operations_path)
    completion_codes = {
        completion.text
        for completion in OperationCompleter(operations).get_completions(Document("MOS-3"), None)
    }

    assert {"MOS-3.5", "MOS-3.6"} <= completion_codes
    for query in ("MOS-3", "corrección"):
        selected, captured_intent, calls = select_with_prompt_toolkit(
            operations, [query], monkeypatch
        )
        assert selected is not None
        assert selected.mos_code == INTENT_ROUTING_MOS_CODE
        assert captured_intent == {PM_QUESTION_HUMANO_NAME: query}
        assert len(calls) == 1


def test_prompt_toolkit_option_selectors_preserve_live_session_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations_path = setup_catalog(tmp_path)
    write_operation(
        operations_path / "fase-3" / "MOS-3.6-output-path.md",
        "MOS-3.6",
        "Output path",
        "PR_NUMBER",
        delivery="output.route_prompt, output.status_result",
    )
    operations = discover_operations(operations_path)
    selected_operation = next(operation for operation in operations if operation.mos_code == "MOS-3.5")
    route_operation = next(operation for operation in operations if operation.mos_code == "MOS-3.6")
    calls: list[tuple[str, dict]] = []
    inputs = iter(["MOS-3.5", "1", "2", "cancel", "exit"])

    def recording_prompt(label: str, **kwargs) -> str:
        calls.append((label, kwargs))
        return next(inputs)

    monkeypatch.setattr("tools.operation_prompt_wizard_prompt_toolkit_ui.prompt", recording_prompt)
    adapter = PromptToolkitWizardAdapter(StringIO())

    selected, _ = adapter.select(operations, {})
    assert selected == selected_operation
    assert adapter.choose_route_path(route_operation, {}).action == "preview"
    assert adapter.choose_preview(
        selected_operation,
        {},
        "rendered prompt",
        tmp_path / "out" / "generated.md",
        [],
        False,
    ) == "cancel"
    assert adapter.choose_post_write(tmp_path / "out" / "generated.md") == "exit"

    option_prompts = {
        "Describe your intent, or search/select operation: ",
        "Selected output path [1 route-prompt / 2 non-route]: ",
        "Choose action [write/edit/operation/cancel]: ",
        "Choose action [new/same/edit/path/exit]: ",
    }
    live_calls = [kwargs for label, kwargs in calls if label in option_prompts]
    assert len(live_calls) == len(option_prompts)
    assert all(kwargs["complete_while_typing"] is None for kwargs in live_calls)
    authorization_calls = [
        kwargs for label, kwargs in calls if label.startswith(f"{PM_AUTHORIZATION_STATUS_NAME} ")
    ]
    assert len(authorization_calls) == 1
    assert authorization_calls[0]["complete_while_typing"] is None


def test_prompt_toolkit_live_operation_dropdown_filters_with_pipe_input(tmp_path: Path) -> None:
    operations_path = setup_catalog(tmp_path)
    write_operation(
        operations_path / "fase-3" / "MOS-3.51-correccion-extra.md",
        "MOS-3.51",
        "Corrección extra",
        "PR_NUMBER",
    )
    write_operation(
        operations_path / "fase-3" / "MOS-3.52-correccion-final.md",
        "MOS-3.52",
        "Corrección final",
        "SOURCE_REVIEW",
    )
    write_operation(
        operations_path / "fase-3" / "MOS-3.6-other.md",
        "MOS-3.6",
        "Other",
        "WORK_UNIT",
    )
    completer = OperationCompleter(discover_operations(operations_path))

    async def verify_dropdown() -> None:
        with create_pipe_input() as pipe_input:
            session = PromptSession(
                completer=completer,
                input=pipe_input,
                output=DummyOutput(),
            )
            prompt_task = asyncio.create_task(session.prompt_async("Search: "))
            await asyncio.sleep(0.05)
            pipe_input.send_text("MOS-3")
            await asyncio.sleep(0.05)
            menu = session.default_buffer.complete_state
            assert menu is not None
            assert {completion.text for completion in menu.completions} == {
                "MOS-3.5",
                "MOS-3.51",
                "MOS-3.52",
                "MOS-3.6",
            }

            pipe_input.send_text(".5")
            await asyncio.sleep(0.05)
            filtered_menu = session.default_buffer.complete_state
            assert filtered_menu is not None
            assert {completion.text for completion in filtered_menu.completions} == {
                "MOS-3.5",
                "MOS-3.51",
                "MOS-3.52",
            }

            prompt_task.cancel()
            with suppress(asyncio.CancelledError):
                await prompt_task

    asyncio.run(verify_dropdown())


@pytest.mark.parametrize("language", ("es", "en"))
@pytest.mark.parametrize(
    ("mos_code", "focus"),
    (("MOS-6.3", "performance"), ("MOS-6.4", "product"), ("MOS-6.5", "code_quality")),
)
@pytest.mark.parametrize("selector", ("filename", "relative_path"))
def test_prompt_toolkit_alias_dropdown_acceptance_preserves_linked_focus(
    language: str, mos_code: str, focus: str, selector: str
) -> None:
    operations = discover_operations(surface_selection_for_language(language).operations_dir)
    alias = next(operation for operation in operations if operation.mos_code == mos_code)
    completer = OperationCompleter(operations)

    async def accept_dropdown_completion() -> str:
        with create_pipe_input() as pipe_input:
            session = PromptSession(completer=completer, input=pipe_input, output=DummyOutput())
            prompt_task = asyncio.create_task(session.prompt_async("Search: "))
            await asyncio.sleep(0.05)
            pipe_input.send_text(getattr(alias, selector)[:-1])
            await asyncio.sleep(0.05)
            menu = session.default_buffer.complete_state
            assert menu is not None
            assert [completion.text for completion in menu.completions] == [mos_code]
            pipe_input.send_text("\t\r")
            return await prompt_task

    selected = resolve_operation_selection(operations, asyncio.run(accept_dropdown_completion()))
    assert selected == alias
    prompts: list[str] = []
    values = collect_values_with_controls(
        selected,
        input_func=lambda prompt: (prompts.append(prompt), {
            "TARGET_REPOSITORY": "codefusion-repo/project-os-v2",
            "PATH_SCOPE": "",
            "PM_FEEDBACK_HUMANO": "",
            "PM_QUESTION_HUMANO": "",
        }[prompt.split(" ", 1)[0]])[1],
        output_stream=StringIO(),
    ).values
    assert values["FOCUS_AREA"] == focus
    assert all(not prompt.startswith("FOCUS_AREA ") for prompt in prompts)


@pytest.mark.parametrize("language", ("es", "en"))
@pytest.mark.parametrize("mos_code", ("MOS-6.3", "MOS-6.4", "MOS-6.5"))
def test_prompt_toolkit_specific_alias_code_completion_keeps_its_identity(
    language: str, mos_code: str
) -> None:
    operations = discover_operations(surface_selection_for_language(language).operations_dir)
    alias = next(operation for operation in operations if operation.mos_code == mos_code)

    completions = list(OperationCompleter(operations).get_completions(Document(mos_code), None))

    assert [completion.text for completion in completions] == [mos_code]
    assert resolve_operation_selection(operations, completions[0].text) == alias


def test_prompt_toolkit_intent_and_navigation_preserve_prompt_sequence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = discover_operations(setup_catalog_with_intent_router(tmp_path))
    intent = "necesito decidir el siguiente paso"
    selected, captured_intent, calls = select_with_prompt_toolkit(
        operations, [intent], monkeypatch
    )

    assert selected is not None
    assert selected.mos_code == INTENT_ROUTING_MOS_CODE
    assert captured_intent == {PM_QUESTION_HUMANO_NAME: intent}
    assert len(calls) == 1

    for command in ("/enumerated", "/phases", "?"):
        selected, captured_intent, calls = select_with_prompt_toolkit(
            operations, [command, "MOS-3.5"], monkeypatch
        )
        assert selected is not None
        assert selected.mos_code == "MOS-3.5"
        assert captured_intent == {}
        assert len(calls) == 2


@pytest.mark.parametrize("language", ["es", "en"])
def test_prompt_toolkit_selection_semantics_are_equal_for_es_and_en(
    language: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    selection = surface_selection_for_language(language)
    operations = discover_operations(selection.operations_dir)
    target = next(operation for operation in operations if operation.mos_code == "MOS-3.5")

    selected, captured_intent, calls = select_with_prompt_toolkit(
        operations, [target.mos_code or ""], monkeypatch
    )

    assert selected is not None
    assert selected.mos_code == target.mos_code
    assert captured_intent == {}
    assert len(calls) == 1


def test_intent_first_text_with_no_catalog_match_routes_via_mos_r2_pt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = setup_catalog_with_intent_router(tmp_path)
    intent_text = "quiero saber que operacion sigue para el issue 500 del roadmap"
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([intent_text, "write", "exit"]),
    )
    stream = StringIO()
    result = run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out", output_stream=stream)

    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert f"PM_QUESTION_HUMANO={intent_text}" in content
    assert INTENT_ROUTING_MOS_CODE in stream.getvalue()


def test_intent_first_rejects_secret_looking_text_before_write_pt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = setup_catalog_with_intent_router(tmp_path)
    # Split so this fixture never contains a contiguous secret-shaped literal
    # in the repo's own source text (the same pattern guards this file too).
    fake_key = "AKIA" + "ABCDEFGHIJKLMNOP"
    secret_intent = f"usa AWS_SECRET_ACCESS_KEY={fake_key} para continuar"
    clean_intent = "texto limpio sin secretos para describir mi intencion"
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt(
            [
                secret_intent,
                "",  # ROUTING_SOURCE blank
                "",  # PM_FEEDBACK_HUMANO blank
                "",  # PM_QUESTION_HUMANO attempt 1: reuses the secret-looking captured intent
                clean_intent,  # PM_QUESTION_HUMANO attempt 2: accepted
                "write",
                "exit",
            ]
        ),
    )
    stream = StringIO()
    result = run_wizard_pt(operations_dir=operations, output_dir=tmp_path / "out", output_stream=stream)

    assert result is not None
    content = result.read_text(encoding="utf-8")
    assert fake_key not in content
    assert f"PM_QUESTION_HUMANO={clean_intent}" in content


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
            "MOS-3.5", "405", "none", "", "", "1", "write", "exit",
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
    # The source review, PR, class, and density are reconstructed by browser
    # chat, never manual wizard inputs, so none render as INPUT variables.
    for derived in ("SOURCE_REVIEW=", "PR_NUMBER=", "CHANGE_CLASS=", f"{HYDRATION_LEVEL_NAME}="):
        assert derived not in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY (" not in stream.getvalue()


def test_active_mos34_collects_authorization_in_prompt_toolkit_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stream = StringIO()
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.4", "405", "skill.arquitectura_backend", "", "", "2", "write", "exit",
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
    assert "WORK_UNIT=405" in content
    # The class and the density are derived, so neither is asked for nor carried
    # unless the PM records an explicit override.
    assert f"{HYDRATION_LEVEL_NAME}=" not in content
    assert "CHANGE_CLASS=" not in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "OPTIONAL_SKILL=skill.arquitectura_backend" in content
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted" in stream.getvalue()


def test_hydration_override_is_opt_in_in_prompt_toolkit_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stream = StringIO()
    monkeypatch.setattr(
        "tools.operation_prompt_wizard.prompt",
        mock_prompt([
            "MOS-3.4", "/hydration full/debug", "405", "none", "", "", "2", "write", "exit",
        ]),
    )
    result = run_wizard_pt(
        operations_dir=DEFAULT_OPERATIONS_DIR,
        output_dir=tmp_path / "out",
        output_stream=stream,
    )

    assert result is not None
    content = result.read_text(encoding="utf-8")
    # The override is never prompted for; typing it records it and it then
    # travels as an explicit INPUT value alongside the derived metadata.
    assert f"{HYDRATION_LEVEL_NAME}=full/debug" in content
    assert "WORK_UNIT=405" in content
    assert f"{HYDRATION_LEVEL_NAME} (" not in stream.getvalue()


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
        {
            "skill.arquitectura_backend",
            "skill.desarrollo_frontend",
            "skill.desarrollo_mobile",
            "skill.desarrollo_videojuegos",
            "none",
        }
        <= set(getattr(completer, "words", []))
        for completer in completers
    )
    assert skill_completion_is_live == [True]
    transcript = stream.getvalue()
    assert "OPTIONAL_SKILL (optional)" in transcript
    assert "skill.arquitectura_backend — Arquitectura backend" in transcript
    assert "skill.desarrollo_frontend — Desarrollo frontend" in transcript
    assert "skill.desarrollo_mobile — Desarrollo mobile" in transcript
    assert "skill.desarrollo_videojuegos — Desarrollo de videojuegos" in transcript
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
        input="\n/enumerator\n/phases\nMOS-3.4\n405\ncancel\n",
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
    assert "skill.desarrollo_mobile — Desarrollo mobile" in transcript
    assert "skill.desarrollo_videojuegos — Desarrollo de videojuegos" in transcript
    assert "Select OPTIONAL_SKILL:" in transcript
    assert not list(output_dir.glob("*.md"))


def test_mos_r3_prompt_toolkit_pseudo_tty_asks_only_source_and_decision_fields(
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
        input="MOS-R.3\nMOS-3.7 review\nfalse\n\ncancel\n",
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )

    assert completed.returncode == 1
    # DECISION_SOURCE is the single primary locator; the related issue and PR are
    # derived from it, so neither is ever prompted for.
    assert "ISSUE_NUMBER (" not in completed.stdout
    assert "PR_NUMBER (" not in completed.stdout
    assert "DECISION_OPTIONS (optional, <DECISION_OPTIONS>):" in completed.stdout
    assert not list(output_dir.glob("*.md"))
