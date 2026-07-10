"""Behavior guards for the active Spanish operation-prompt wizard."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

from tools.operation_prompt_wizard import (
    DEFAULT_OPERATIONS_DIR,
    InputVariable,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
    PM_AUTHORIZATION_STATUS_NAME,
    WIZARD_PROMPT_MARKER,
    WizardError,
    cleanup_previous_generated_prompts,
    discover_operations,
    display_operations,
    filter_operations,
    generated_filename,
    load_active_skill_choices,
    load_phase_map,
    operation_needs_pm_authorization_assistance,
    operation_output_refs,
    parse_input_variables,
    print_phase_groups,
    render_prompt,
    resolve_operation_selection,
    run_wizard,
    validate_variable_value,
    wizard_variables,
    write_prompt,
)


def answers(*values: str):
    iterator = iter(values)
    return lambda _prompt: next(iterator)


def write_spanish_operation(
    path: Path,
    code: str,
    title: str,
    required: str = "— (ninguna)",
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


def test_active_catalog_is_recursive_excludes_readme_and_derives_phase_context() -> None:
    operations = discover_operations()
    names = {operation.filename for operation in operations}
    correction = next(operation for operation in operations if operation.mos_code == "MOS-3.5")
    phases = load_phase_map(operations=operations)

    assert DEFAULT_OPERATIONS_DIR.parts[-2:] == ("project-os-es", "operaciones")
    assert len(operations) > 100
    assert "README.md" not in names
    assert correction.relative_path == "fase-3/MOS-3.5-draftear-route-prompt-de-correccion.md"
    assert correction.phase_path == "fase-3"
    assert correction.phase_label == "Fase 3"
    assert phases[correction.index] == "Fase 3"


def test_display_and_phase_grouping_show_relative_spanish_context() -> None:
    operations = discover_operations()
    stream = StringIO()
    display_operations(operations[:2], stream)
    print_phase_groups(operations, load_phase_map(operations=operations), stream)
    transcript = stream.getvalue()

    assert "Available operations:" in transcript
    assert "cross-fase/MOS-R.2-recomendar-siguiente-operacion.md" in transcript
    assert "Operations grouped by SDLC phase:" in transcript
    assert "Cross-fase:" in transcript
    assert "Fase 3:" in transcript


def test_selection_supports_index_filename_stem_mos_code_and_relative_path() -> None:
    operations = discover_operations()
    target = next(operation for operation in operations if operation.mos_code == "MOS-3.5")

    assert resolve_operation_selection(operations, str(target.index)) == target
    assert resolve_operation_selection(operations, target.filename) == target
    assert resolve_operation_selection(operations, target.path.stem) == target
    assert resolve_operation_selection(operations, "mos-3.5") == target
    assert resolve_operation_selection(operations, target.relative_path) == target


def test_duplicate_filename_or_stem_fails_safely_but_relative_path_selects(tmp_path: Path) -> None:
    write_spanish_operation(tmp_path / "fase-1" / "MOS-1.1-duplicada.md", "MOS-1.1", "Uno")
    write_spanish_operation(tmp_path / "fase-2" / "MOS-1.1-duplicada.md", "MOS-1.1", "Dos")
    operations = discover_operations(tmp_path)

    assert resolve_operation_selection(operations, "MOS-1.1-duplicada.md") is None
    assert resolve_operation_selection(operations, "MOS-1.1-duplicada") is None
    assert resolve_operation_selection(operations, "MOS-1.1") is None
    assert resolve_operation_selection(operations, "fase-2/MOS-1.1-duplicada.md") == operations[1]


def test_filter_matches_active_spanish_search_surface() -> None:
    operations = discover_operations()
    target = next(operation for operation in operations if operation.mos_code == "MOS-3.5")
    phases = load_phase_map(operations=operations)

    for query in (
        str(target.index),
        "MOS-3.5",
        "draftear-route-prompt-de-correccion",
        "fase-3/MOS-3.5",
        "Fase 3",
        "corrección",
    ):
        assert target in filter_operations(operations, query, phases)


def test_active_route_operations_expose_required_authorization_and_no_pm_agent_family() -> None:
    operations = discover_operations()
    expected_variables = {
        "MOS-3.4": [
            ("ISSUE_NUMBER", False),
            ("ROADMAP_ISSUE", False),
            ("OPTIONAL_SKILL", False),
            ("PM_FEEDBACK_HUMANO", False),
            ("PM_QUESTION_HUMANO", False),
        ],
        "MOS-3.5": [
            ("ISSUE_NUMBER", True),
            ("PR_NUMBER", False),
            ("OPTIONAL_SKILL", False),
            ("PM_FEEDBACK_HUMANO", False),
            ("PM_QUESTION_HUMANO", False),
        ],
    }

    for mos_code, expected in expected_variables.items():
        operation = next(candidate for candidate in operations if candidate.mos_code == mos_code)
        assert [(variable.name, variable.required) for variable in operation.variables] == expected
        assert operation_output_refs(operation) == ("output.route_prompt",)
        assert operation_needs_pm_authorization_assistance(operation) is True
        assert [(variable.name, variable.required) for variable in wizard_variables(operation)][-1] == (
            PM_AUTHORIZATION_STATUS_NAME,
            True,
        )
        assert "RECOMMENDED_TERMINAL_AGENT_FAMILY" not in [variable.name for variable in operation.variables]

        rendered = render_prompt(
            operation,
            {"ISSUE_NUMBER": "405", PM_AUTHORIZATION_STATUS_NAME: PM_AUTHORIZATION_GRANTED},
        )
        assert rendered.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
        assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in rendered


def test_line_wizard_active_mos35_generates_pending_route_prompt(tmp_path: Path) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "/phases",
            "MOS-3.5",
            "MOS-3.5",
            "405", "", "none", "", "", "1",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None and output.is_file()
    transcript = stream.getvalue()
    content = output.read_text(encoding="utf-8")
    assert "Operations grouped by SDLC phase:" in transcript
    assert "Fase 3:" in transcript
    assert "ISSUE_NUMBER=405" in content
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted for this exact scope and mode." in transcript
    assert WIZARD_PROMPT_MARKER in content


def test_line_wizard_active_mos34_generates_granted_route_prompt(tmp_path: Path) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "MOS-3.4", "MOS-3.4",
            "405", "274", "skill.arquitectura_backend", "", "", "2",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "OPTIONAL_SKILL=skill.arquitectura_backend" in content
    assert "OPTIONAL_SKILL choices:" in stream.getvalue()


def test_line_wizard_rejects_blank_and_invalid_route_authorization_then_normalizes(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.5-route.md",
        "MOS-3.5",
        "Route",
        required="ISSUE_NUMBER",
        delivery="output.route_prompt",
    )
    stream = StringIO()
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers("MOS-3.5", "MOS-3.5", "405", "", "granted", "2", "write", "exit"),
        output_stream=stream,
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content
    assert stream.getvalue().count("Invalid value: PM_AUTHORIZATION_STATUS") == 2


def test_same_resets_issue_keeps_roadmap_and_edit_reopens_values(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.4-route.md",
        "MOS-3.4",
        "Route",
        required="ISSUE_NUMBER",
        optional="ROADMAP_ISSUE",
    )
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "MOS-3.4", "MOS-3.4", "100", "274", "write",
            "same", "200", "", "write",
            "edit", "300", "", "write", "exit",
        ),
        output_stream=StringIO(),
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=300" in content
    assert "ROADMAP_ISSUE=274" in content
    assert len(list(output_dir.glob("*.md"))) == 1


def test_back_and_new_continue_session_and_keep_only_latest_prompt(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    output_dir = tmp_path / "out"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.1-uno.md", "MOS-3.1", "Uno", required="ISSUE_NUMBER"
    )
    write_spanish_operation(
        operations_dir / "fase-4" / "MOS-4.1-dos.md", "MOS-4.1", "Dos", required="PR_NUMBER"
    )
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=output_dir,
        input_func=answers(
            "MOS-3.1", "MOS-3.1", "back",
            "MOS-4.1", "MOS-4.1", "406", "write",
            "new", "MOS-3.1", "MOS-3.1", "405", "write", "exit",
        ),
        output_stream=StringIO(),
    )

    assert output is not None
    assert "MOS-3.1" in output.read_text(encoding="utf-8")
    assert len(list(output_dir.glob("*.md"))) == 1


def test_same_reasks_authorization_and_never_carries_a_grant(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.5-route.md",
        "MOS-3.5",
        "Route",
        required="ISSUE_NUMBER",
        delivery="output.route_prompt",
    )
    stream = StringIO()
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers(
            "MOS-3.5", "MOS-3.5", "100", "2", "write",
            "same", "200", "1", "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=200" in content
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in content
    assert PM_AUTHORIZATION_GRANTED not in content
    assert stream.getvalue().count("PM_AUTHORIZATION_STATUS: 1=pending") == 2


def test_new_does_not_carry_authorization_into_another_operation(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.5-route.md",
        "MOS-3.5",
        "Route",
        required="ISSUE_NUMBER",
        delivery="output.route_prompt",
    )
    write_spanish_operation(
        operations_dir / "fase-4" / "MOS-4.1-status.md",
        "MOS-4.1",
        "Status",
        required="PR_NUMBER",
    )
    stream = StringIO()
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers(
            "MOS-3.5", "MOS-3.5", "405", "2", "write",
            "new", "MOS-4.1", "MOS-4.1", "406", "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    assert PM_AUTHORIZATION_STATUS_NAME not in output.read_text(encoding="utf-8")
    assert stream.getvalue().count("PM_AUTHORIZATION_STATUS: 1=pending") == 1


def test_edit_shows_the_exact_scope_warning_before_reusing_current_status(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.5-route.md",
        "MOS-3.5",
        "Route",
        required="ISSUE_NUMBER",
        delivery="output.route_prompt",
    )
    stream = StringIO()
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers(
            "MOS-3.5", "MOS-3.5", "405", "2", "write",
            "edit", "", "", "write", "y", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in output.read_text(encoding="utf-8")
    assert stream.getvalue().count("Use 2 only for exact PM-approved scope/mode") == 2


def test_multi_output_back_then_non_route_removes_stale_authorization(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.1-multi.md",
        "MOS-3.1",
        "Multi",
        required="ISSUE_NUMBER",
        delivery="output.route_prompt, output.status_result",
    )
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers(
            "MOS-3.1", "MOS-3.1", "405", "1", "2", "edit", "", "2", "write", "exit"
        ),
        output_stream=StringIO(),
    )

    assert output is not None
    assert PM_AUTHORIZATION_STATUS_NAME not in output.read_text(encoding="utf-8")


def test_optional_skill_choices_are_dynamic_and_fail_closed(tmp_path: Path) -> None:
    assert load_active_skill_choices() == (
        "skill.arquitectura_backend",
        "skill.desarrollo_frontend",
        "none",
    )
    variable = InputVariable("OPTIONAL_SKILL", "<OPTIONAL_SKILL>", False, "")
    assert validate_variable_value(variable, "") is None
    assert validate_variable_value(variable, "skill.arquitectura_backend") is None
    assert validate_variable_value(variable, "skill.desarrollo_frontend") is None
    assert validate_variable_value(variable, "none") is None
    assert "active skill or none" in (validate_variable_value(variable, "skill.inactiva") or "")

    invalid_catalog = tmp_path / "skills.json"
    invalid_catalog.write_text('{"skills": [{"key": "skill.incompleta"}]}', encoding="utf-8")
    try:
        load_active_skill_choices(invalid_catalog)
    except WizardError as exc:
        assert "invalid active skills catalog" in str(exc)
    else:
        raise AssertionError("invalid skill catalog must fail closed")


def test_line_wizard_shows_dynamic_skill_choices_and_rejects_unknown_value(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.1-skill.md",
        "MOS-3.1",
        "Skill",
        optional="OPTIONAL_SKILL",
    )
    stream = StringIO()
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers(
            "MOS-3.1", "MOS-3.1", "skill.inactiva", "skill.desarrollo_frontend", "write", "exit"
        ),
        output_stream=stream,
    )

    assert output is not None
    assert "OPTIONAL_SKILL=skill.desarrollo_frontend" in output.read_text(encoding="utf-8")
    transcript = stream.getvalue()
    assert "OPTIONAL_SKILL choices: skill.arquitectura_backend, skill.desarrollo_frontend, none" in transcript
    assert "OPTIONAL_SKILL must be an active skill or none" in transcript


def test_route_prompt_template_keeps_ai_advisory_field_without_pm_input() -> None:
    template = (DEFAULT_OPERATIONS_DIR.parent / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}" in template
    assert "browser chat infiere" in template
    assert "feedback explícito\ndel PM puede reemplazar" in template

    for mos_code in ("MOS-3.4", "MOS-3.5"):
        operation = next(candidate for candidate in discover_operations() if candidate.mos_code == mos_code)
        assert "RECOMMENDED_TERMINAL_AGENT_FAMILY" not in [variable.name for variable in operation.variables]
        assert "browser chat" in operation.text


def test_cleanup_never_removes_unmarked_file_and_secret_looking_input_is_rejected(tmp_path: Path) -> None:
    operation = next(operation for operation in discover_operations() if operation.mos_code == "MOS-3.5")
    rendered = render_prompt(operation, {})
    generated = write_prompt(tmp_path / generated_filename(operation, rendered), rendered)
    handwritten = tmp_path / "notes.md"
    handwritten.write_text("keep", encoding="utf-8")

    assert cleanup_previous_generated_prompts(tmp_path, keep_path=handwritten) == [generated]
    assert handwritten.read_text(encoding="utf-8") == "keep"
    error = validate_variable_value(
        InputVariable("PM_FEEDBACK_HUMANO", "<PM_FEEDBACK_HUMANO>", False, ""),
        "gh" + "p_" + "abcdefghijklmnop",
    )
    assert error is not None
