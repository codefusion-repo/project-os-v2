"""Focused guards for the active Spanish operation-prompt wizard."""

from __future__ import annotations

from pathlib import Path
from io import StringIO

from tools.operation_prompt_wizard import (
    DEFAULT_OPERATION_FLOWS_PATH,
    DEFAULT_OPERATIONS_DIR,
    InputVariable,
    discover_operations,
    generated_filename,
    load_phase_map,
    render_prompt,
    run_wizard,
    validate_variable_value,
    write_prompt,
)


def test_default_catalog_is_the_active_spanish_operations_tree() -> None:
    operations = discover_operations()
    names = {operation.path.name for operation in operations}

    assert DEFAULT_OPERATIONS_DIR.parts[-2:] == ("project-os-es", "operaciones")
    assert DEFAULT_OPERATION_FLOWS_PATH is None
    assert len(operations) > 100
    assert "README.md" not in names
    assert {
        "MOS-3.4-draftear-route-prompt-de-implementacion.md",
        "MOS-3.5-draftear-route-prompt-de-correccion.md",
        "MOS-3.7-revisar-pr-antes-de-cerrar.md",
    } <= names


def test_spanish_operation_can_generate_a_marked_local_prompt_safely(tmp_path: Path) -> None:
    operation = next(
        item
        for item in discover_operations()
        if item.path.name == "MOS-3.5-draftear-route-prompt-de-correccion.md"
    )
    rendered = render_prompt(operation, {})
    output = write_prompt(tmp_path / generated_filename(operation, rendered), rendered)

    assert output.is_file()
    assert "MOS-3.5" in output.read_text(encoding="utf-8")
    assert "project-os-operation-prompt-wizard" in output.read_text(encoding="utf-8")
    secret_error = validate_variable_value(
        InputVariable("PM_FEEDBACK_HUMANO", "<PM_FEEDBACK_HUMANO>", False, ""),
        "gh" + "p_" + "abcdefghijklmnop",
    )
    assert secret_error is not None
    assert load_phase_map() == {}


def test_wizard_lists_and_generates_a_spanish_operation(tmp_path: Path) -> None:
    answers = iter(
        (
            "MOS-3.5-draftear-route-prompt-de-correccion.md",
            "MOS-3.5-draftear-route-prompt-de-correccion.md",
            "w",
            "exit",
        )
    )
    output_stream = StringIO()

    output = run_wizard(
        output_dir=tmp_path,
        input_func=lambda _prompt: next(answers),
        output_stream=output_stream,
    )

    assert output is not None and output.is_file()
    assert "Available operations:" in output_stream.getvalue()
    assert "MOS-3.5-draftear-route-prompt-de-correccion.md" in output_stream.getvalue()
