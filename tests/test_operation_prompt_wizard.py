"""Behavior guards for the active Spanish operation-prompt wizard."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import (
    DEFAULT_OPERATIONS_DIR,
    DEFAULT_SKILLS_CATALOG,
    LANGUAGE_QUESTION,
    REPO_ROOT,
    HYDRATION_LEVEL_DEFAULT,
    HYDRATION_LEVEL_NAME,
    InputVariable,
    PM_AUTHORIZATION_GRANTED,
    PM_AUTHORIZATION_PENDING,
    PM_AUTHORIZATION_STATUS_NAME,
    WIZARD_PROMPT_MARKER,
    WizardError,
    cleanup_previous_generated_prompts,
    discover_operations,
    display_operation_summary,
    display_operations,
    extract_description,
    filter_operations,
    generated_filename,
    load_active_skill_choices,
    load_active_skill_options,
    load_phase_map,
    collect_values_with_controls,
    normalize_variable_value,
    operation_needs_pm_authorization_assistance,
    operation_output_refs,
    build_parser,
    parse_input_variables,
    print_phase_groups,
    render_prompt,
    resolve_operation_selection,
    resolve_surface_selection,
    run_wizard,
    select_operation,
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


def write_skill_catalog(path: Path, entries: list[dict[str, object]]) -> Path:
    path.write_text(json.dumps({"skills": entries}), encoding="utf-8")
    return path


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


def test_display_and_phase_grouping_are_compact_and_keep_distinct_descriptions() -> None:
    operations = discover_operations()
    stream = StringIO()
    display_operations(operations[:2], stream)
    print_phase_groups(operations, load_phase_map(operations=operations), stream)
    transcript = stream.getvalue()

    assert "Available operations:" in transcript
    first = operations[0]
    assert first.description in transcript
    assert first.relative_path not in transcript
    assert transcript.count(f" {first.mos_code} —") == 2
    assert "Operations grouped by SDLC phase:" in transcript
    assert "Cross-fase:" in transcript
    assert "Fase 3:" in transcript


def test_description_comes_from_hace_with_title_fallback(tmp_path: Path) -> None:
    path = tmp_path / "MOS-9.1-ejemplo.md"
    text = "# MOS-9.1 — Título repetido\n\n**Hace:** Explica un resultado útil y distinto.\n"
    assert extract_description(text, path) == "Explica un resultado útil y distinto."
    assert extract_description("# MOS-9.1 — Título repetido\n", path) == "Título repetido"


def test_selection_supports_index_filename_stem_mos_code_and_relative_path() -> None:
    operations = discover_operations()
    target = next(operation for operation in operations if operation.mos_code == "MOS-3.5")

    assert resolve_operation_selection(operations, str(target.index)) == target
    assert resolve_operation_selection(operations, target.filename) == target
    assert resolve_operation_selection(operations, target.path.stem) == target
    assert resolve_operation_selection(operations, "mos-3.5") == target
    assert resolve_operation_selection(operations, target.relative_path) == target


def test_line_view_commands_render_confirmation_and_allow_direct_selection() -> None:
    operations = discover_operations()
    phases = load_phase_map(operations=operations)
    target = next(operation for operation in operations if operation.mos_code == "MOS-3.5")

    for command in ("/enumerated", "/enumerator", "/"):
        stream = StringIO()
        selected = select_operation(
            operations,
            input_func=answers(command, str(target.index)),
            output_stream=stream,
            phase_by_operation=phases,
        )
        assert selected == target
        assert stream.getvalue().count("View: enumerated operations") >= 2

    for command in ("/phases", "/phase"):
        stream = StringIO()
        selected = select_operation(
            operations,
            input_func=answers(command, "MOS-3.5"),
            output_stream=stream,
            phase_by_operation=phases,
        )
        assert selected == target
        transcript = stream.getvalue()
        assert "View: operations grouped by phase" in transcript
        assert "Operations grouped by SDLC phase:" in transcript


def test_selection_help_announces_only_supported_view_commands() -> None:
    operations = discover_operations()
    stream = StringIO()
    assert select_operation(operations, input_func=answers("?", "cancel"), output_stream=stream) is None
    transcript = stream.getvalue()
    for command in ("/enumerated", "/enumerator", "/phases", "/phase"):
        assert command in transcript


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
        target.description,
    ):
        assert target in filter_operations(operations, query, phases)


def test_selected_summary_exposes_relative_path_without_repeating_it_in_main_list() -> None:
    stream = StringIO()
    operation = next(op for op in discover_operations() if op.mos_code == "MOS-6.9")
    display_operation_summary(operation, stream)

    transcript = stream.getvalue()
    compact = "MOS-6.9 — Procesa las mejoras de rendimiento recomendadas."
    assert compact in transcript
    assert "Path: fase-6/MOS-6.9-procesar-mejoras-de-rendimiento.md" in transcript


def test_active_route_operations_expose_hydration_and_required_authorization() -> None:
    operations = discover_operations()
    expected_variables = {
        "MOS-3.4": [
            ("ISSUE_NUMBER", False),
            ("ROADMAP_ISSUE", False),
            ("OPTIONAL_SKILL", False),
            (HYDRATION_LEVEL_NAME, False),
            ("PM_FEEDBACK_HUMANO", False),
            ("PM_QUESTION_HUMANO", False),
        ],
        "MOS-3.5": [
            ("ISSUE_NUMBER", True),
            ("PR_NUMBER", False),
            ("OPTIONAL_SKILL", False),
            (HYDRATION_LEVEL_NAME, False),
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
            {
                "ISSUE_NUMBER": "405",
                HYDRATION_LEVEL_NAME: "full/debug",
                PM_AUTHORIZATION_STATUS_NAME: PM_AUTHORIZATION_GRANTED,
            },
        )
        assert rendered.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
        assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in rendered
        assert f"{HYDRATION_LEVEL_NAME}=full/debug" in rendered


def test_mos_r3_exposes_only_the_six_decision_variables_in_both_languages() -> None:
    expected = [
        ("DECISION_SOURCE", True),
        ("PM_DECISION_ALREADY_MADE", True),
        ("ISSUE_NUMBER", False),
        ("PR_NUMBER", False),
        ("DECISION_OPTIONS", False),
        ("PM_DECISION", False),
    ]
    for operations_dir in (
        REPO_ROOT / "project-os-es" / "operaciones",
        REPO_ROOT / "project-os-en" / "operations",
    ):
        operation = next(
            item for item in discover_operations(operations_dir) if item.mos_code == "MOS-R.3"
        )
        assert [(variable.name, variable.required) for variable in operation.variables] == expected
        assert [(variable.name, variable.required) for variable in wizard_variables(operation)] == expected


def test_mos_r3_validates_numeric_references_and_decision_state() -> None:
    operation = next(item for item in discover_operations() if item.mos_code == "MOS-R.3")
    variables = {variable.name: variable for variable in operation.variables}

    issue_number = variables["ISSUE_NUMBER"]
    pr_number = variables["PR_NUMBER"]
    assert validate_variable_value(issue_number, "429") is None
    assert validate_variable_value(pr_number, "#431") is None
    for invalid in ("issue #429", "PR #431", "0", "-429", "429, 431"):
        assert "positive issue/PR number" in (validate_variable_value(issue_number, invalid) or "")
    assert "At least one" in (
        validate_variable_value(
            pr_number,
            "",
            current_values={"ISSUE_NUMBER": ""},
            requires_mos_r3_reference=True,
        )
        or ""
    )
    assert validate_variable_value(
        pr_number,
        "",
        current_values={"ISSUE_NUMBER": "429"},
        requires_mos_r3_reference=True,
    ) is None

    decision_made = variables["PM_DECISION_ALREADY_MADE"]
    for supplied, expected in (("true", "true"), ("sí", "true"), ("1", "true"), ("false", "false"), ("no", "false"), ("0", "false")):
        assert validate_variable_value(decision_made, supplied) is None
        assert normalize_variable_value(decision_made, supplied) == expected
    assert "must be true or false" in (validate_variable_value(decision_made, "maybe") or "")

    pm_decision = variables["PM_DECISION"]
    assert "is required" in (
        validate_variable_value(
            pm_decision,
            "",
            current_values={"PM_DECISION_ALREADY_MADE": "true"},
        )
        or ""
    )
    assert "must be empty" in (
        validate_variable_value(
            pm_decision,
            "Implement option A",
            current_values={"PM_DECISION_ALREADY_MADE": "false"},
        )
        or ""
    )
    assert validate_variable_value(
        pm_decision,
        "Implement option A",
        current_values={"PM_DECISION_ALREADY_MADE": "true"},
    ) is None
    assert validate_variable_value(
        pm_decision,
        "",
        current_values={"PM_DECISION_ALREADY_MADE": "false"},
    ) is None


def test_mos_r3_display_description_names_the_pending_pm_decision_in_both_languages() -> None:
    expected = {
        "es": "Procesa una decisión PM pendiente desde evidencia viva hacia una salida segura.",
        "en": "Process a pending PM decision from live evidence into a safe output.",
    }
    for language, operations_dir in (
        ("es", REPO_ROOT / "project-os-es" / "operaciones"),
        ("en", REPO_ROOT / "project-os-en" / "operations"),
    ):
        operation = next(
            item for item in discover_operations(operations_dir) if item.mos_code == "MOS-R.3"
        )
        stream = StringIO()
        display_operation_summary(operation, stream)

        assert operation.description == expected[language]
        assert expected[language] in stream.getvalue()


def test_mos_r3_line_collection_covers_issue_only_pr_only_both_and_neither() -> None:
    operation = next(item for item in discover_operations() if item.mos_code == "MOS-R.3")

    decided_stream = StringIO()
    decided = collect_values_with_controls(
        operation,
        input_func=answers(
            "security review", "sí", "429", "", "", "/clear", "Apply option A"
        ),
        output_stream=decided_stream,
    )
    assert decided.values == {
        "DECISION_SOURCE": "security review",
        "PM_DECISION_ALREADY_MADE": "true",
        "ISSUE_NUMBER": "429",
        "PR_NUMBER": "",
        "DECISION_OPTIONS": "",
        "PM_DECISION": "Apply option A",
    }
    assert "PM_DECISION is required" in decided_stream.getvalue()

    options_needed = collect_values_with_controls(
        operation,
        input_func=answers("QA result", "no", "", "428", "", ""),
        output_stream=StringIO(),
    )
    assert options_needed.values == {
        "DECISION_SOURCE": "QA result",
        "PM_DECISION_ALREADY_MADE": "false",
        "ISSUE_NUMBER": "",
        "PR_NUMBER": "428",
        "DECISION_OPTIONS": "",
        "PM_DECISION": "",
    }

    both = collect_values_with_controls(
        operation,
        input_func=answers("release review", "false", "429", "431", "", ""),
        output_stream=StringIO(),
    )
    assert both.values["ISSUE_NUMBER"] == "429"
    assert both.values["PR_NUMBER"] == "431"

    neither_stream = StringIO()
    neither = collect_values_with_controls(
        operation,
        input_func=answers("QA result", "false", "", "", "431", "", ""),
        output_stream=neither_stream,
    )
    assert neither.values["PR_NUMBER"] == "431"
    assert "At least one of ISSUE_NUMBER or PR_NUMBER is required" in neither_stream.getvalue()


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_r3_wizard_generates_canonical_artifact_for_decision_already_made(
    tmp_path: Path, language: str
) -> None:
    output = run_wizard(
        language=language,
        output_dir=tmp_path,
        input_func=answers(
            "MOS-R.3",
            "MOS-3.7 review",
            "yes",
            "429",
            "",
            "",
            "Apply the scoped correction",
            "2",
            "write",
            "exit",
        ),
        output_stream=StringIO(),
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=429" in content
    assert "PR_NUMBER=" in content
    assert "PM_DECISION_ALREADY_MADE=true" in content
    assert "PM_DECISION=Apply the scoped correction" in content


def test_mos_r3_wizard_rejects_contradictory_false_decision_and_allows_empty_options(
    tmp_path: Path,
) -> None:
    stream = StringIO()
    output = run_wizard(
        language="es",
        output_dir=tmp_path,
        input_func=answers(
            "MOS-R.3",
            "QA result",
            "false",
            "",
            "",
            "431",
            "",
            "Contradictory decision",
            "",
            "2",
            "write",
            "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert "ISSUE_NUMBER=" in content
    assert "PR_NUMBER=431" in content
    assert "PM_DECISION_ALREADY_MADE=false" in content
    assert "DECISION_OPTIONS=" in content
    assert "PM_DECISION=" in content
    assert "At least one of ISSUE_NUMBER or PR_NUMBER is required" in stream.getvalue()
    assert "must be empty" in stream.getvalue()


def test_line_wizard_active_mos35_generates_pending_route_prompt(tmp_path: Path) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "",
            "/phases",
            "MOS-3.5",
            "405", "", "none", "", "", "", "1",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None and output.is_file()
    transcript = stream.getvalue()
    content = output.read_text(encoding="utf-8")
    assert "Session surface: es (session-only" in transcript
    assert "Operations catalog: project-os-es/operaciones" in transcript
    assert "Kernel (reference only, not applied): project-os-es/kernel" in transcript
    assert "Operations grouped by SDLC phase:" in transcript
    assert "Fase 3:" in transcript
    assert "ISSUE_NUMBER=405" in content
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert f"{HYDRATION_LEVEL_NAME}={HYDRATION_LEVEL_DEFAULT}" in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted for this exact scope and mode." in transcript
    assert WIZARD_PROMPT_MARKER in content


def test_line_wizard_active_mos34_generates_granted_route_prompt(tmp_path: Path) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "es",
            "MOS-3.4",
            "405", "274", "skill.arquitectura_backend", "", "", "", "2",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert f"{HYDRATION_LEVEL_NAME}={HYDRATION_LEVEL_DEFAULT}" in content
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY=" not in content
    assert "OPTIONAL_SKILL=skill.arquitectura_backend" in content
    transcript = stream.getvalue()
    assert "OPTIONAL_SKILL (optional)" in transcript
    assert "skill.arquitectura_backend — Arquitectura backend" in transcript


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
        input_func=answers("MOS-3.5", "405", "", "granted", "2", "write", "exit"),
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
            "MOS-3.4", "100", "274", "write",
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
            "MOS-3.1", "back",
            "MOS-4.1", "406", "write",
            "new", "MOS-3.1", "405", "write", "exit",
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
            "MOS-3.5", "100", "2", "write",
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
            "MOS-3.5", "405", "2", "write",
            "new", "MOS-4.1", "406", "write", "exit",
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
            "MOS-3.5", "405", "2", "write",
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
            "MOS-3.1", "405", "1", "2", "edit", "", "2", "write", "exit"
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


def test_modified_skill_catalog_controls_visible_options_and_validation(tmp_path: Path) -> None:
    catalog = write_skill_catalog(
        tmp_path / "skills.json",
        [
            {"key": "skill.nueva", "nombre": "Skill nueva", "active": True},
            {"key": "skill.inactiva", "nombre": "Skill inactiva", "active": False},
        ],
    )
    options = load_active_skill_options(catalog)
    assert [(option.key, option.name) for option in options] == [("skill.nueva", "Skill nueva")]
    assert load_active_skill_choices(catalog) == ("skill.nueva", "none")

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
        skills_catalog_path=catalog,
        input_func=answers("MOS-3.1", "skill.inactiva", "skill.nueva", "write", "exit"),
        output_stream=stream,
    )

    assert output is not None
    assert "OPTIONAL_SKILL=skill.nueva" in output.read_text(encoding="utf-8")
    transcript = stream.getvalue()
    assert "skill.nueva — Skill nueva" in transcript
    assert "skill.inactiva — Skill inactiva" not in transcript
    assert "OPTIONAL_SKILL must be an active skill or none" in transcript


def test_operation_without_optional_skill_does_not_show_skill_menu(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
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
        input_func=answers("MOS-4.1", "406", "write", "exit"),
        output_stream=stream,
    )
    assert output is not None
    assert "OPTIONAL_SKILL (optional)" not in stream.getvalue()


def test_line_wizard_shows_dynamic_skill_choices_and_rejects_unknown_value(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.1-skill.md",
        "MOS-3.1",
        "Skill",
        optional="OPTIONAL_SKILL",
    )
    stream = StringIO()
    supplied = iter(("MOS-3.1", "skill.inactiva", "skill.desarrollo_frontend", "write", "exit"))
    prompts: list[str] = []

    def recording_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(supplied)

    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=recording_input,
        output_stream=stream,
    )

    assert output is not None
    assert "OPTIONAL_SKILL=skill.desarrollo_frontend" in output.read_text(encoding="utf-8")
    transcript = stream.getvalue()
    assert "OPTIONAL_SKILL (optional)" in transcript
    assert "skill.arquitectura_backend — Arquitectura backend" in transcript
    assert "skill.desarrollo_frontend — Desarrollo frontend" in transcript
    assert "none — Sin skill opcional" in transcript
    assert "Enter — Dejar vacío" in transcript
    assert "OPTIONAL_SKILL must be an active skill or none" in transcript
    assert prompts.count("Select OPTIONAL_SKILL: ") == 2


def test_route_prompt_template_keeps_ai_advisory_field_without_pm_input() -> None:
    template = (DEFAULT_OPERATIONS_DIR.parent / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}" in template
    assert "HYDRATION_LEVEL = {{minimal | compact | full/debug}}" in template
    assert "`compact` es el valor predeterminado práctico" in template
    assert "browser chat infiere" in template
    assert "feedback explícito\ndel PM puede reemplazar" in template

    for mos_code in ("MOS-3.4", "MOS-3.5"):
        operation = next(candidate for candidate in discover_operations() if candidate.mos_code == mos_code)
        assert "RECOMMENDED_TERMINAL_AGENT_FAMILY" not in [variable.name for variable in operation.variables]
        assert HYDRATION_LEVEL_NAME in [variable.name for variable in operation.variables]
        assert "browser chat" in operation.text


def test_hydration_level_rejects_unknown_values_and_is_absent_from_unrelated_operations() -> None:
    level = InputVariable(HYDRATION_LEVEL_NAME, "<minimal|compact|full/debug>", False, "")
    assert validate_variable_value(level, HYDRATION_LEVEL_DEFAULT) is None
    assert validate_variable_value(level, "full/debug") is None
    assert "exactly one of" in (validate_variable_value(level, "verbose") or "")

    implementation_route = next(
        operation for operation in discover_operations() if operation.mos_code == "MOS-3.4"
    )
    assert f"{HYDRATION_LEVEL_NAME}={HYDRATION_LEVEL_DEFAULT}" in render_prompt(
        implementation_route, {}
    )

    unrelated = next(operation for operation in discover_operations() if operation.mos_code == "MOS-4.1")
    assert HYDRATION_LEVEL_NAME not in [variable.name for variable in unrelated.variables]


def test_line_wizard_rejects_invalid_hydration_before_rendering_full_debug(tmp_path: Path) -> None:
    operations_dir = tmp_path / "operations"
    write_spanish_operation(
        operations_dir / "fase-3" / "MOS-3.4-route.md",
        "MOS-3.4",
        "Route",
        optional=HYDRATION_LEVEL_NAME,
    )
    stream = StringIO()
    output = run_wizard(
        operations_dir=operations_dir,
        output_dir=tmp_path / "out",
        input_func=answers("MOS-3.4", "verbose", "full/debug", "write", "exit"),
        output_stream=stream,
    )

    assert output is not None
    assert f"{HYDRATION_LEVEL_NAME}=full/debug" in output.read_text(encoding="utf-8")
    assert "HYDRATION_LEVEL must be exactly one of" in stream.getvalue()


def test_language_selector_defaults_rejects_unknown_and_selects_each_surface() -> None:
    questions: list[str] = []

    def ask(factory):
        iterator = iter(factory)

        def _ask(question: str) -> str:
            questions.append(question)
            return next(iterator)

        return _ask

    stream = StringIO()
    spanish = resolve_surface_selection(input_func=ask([""]), output_stream=stream)
    assert spanish.language == "es"
    assert spanish.operations_dir == REPO_ROOT / "project-os-es" / "operaciones"
    assert spanish.skills_catalog_path == REPO_ROOT / "project-os-es" / "kernel" / "skills.json"
    assert spanish.kernel_dir == REPO_ROOT / "project-os-es" / "kernel"

    explicit_spanish = resolve_surface_selection(input_func=ask(["es"]), output_stream=stream)
    assert explicit_spanish == spanish

    english = resolve_surface_selection(input_func=ask(["fr", "en"]), output_stream=stream)
    assert english.language == "en"
    assert english.operations_dir == REPO_ROOT / "project-os-en" / "operations"
    assert english.skills_catalog_path == REPO_ROOT / "project-os-en" / "kernel" / "skills.json"
    assert english.kernel_dir == REPO_ROOT / "project-os-en" / "kernel"
    assert "Unknown language 'fr'" in stream.getvalue()
    assert questions == [LANGUAGE_QUESTION] * 4
    assert resolve_surface_selection(input_func=ask(["cancel"]), output_stream=stream) is None


def test_explicit_language_never_asks_and_invalid_language_fails_closed() -> None:
    def never_ask(_question: str) -> str:
        raise AssertionError("explicit --language must not prompt interactively")

    english = resolve_surface_selection(language="en", input_func=never_ask)
    assert english.language == "en"
    assert english.operations_dir == REPO_ROOT / "project-os-en" / "operations"

    with pytest.raises(WizardError, match="unknown wizard language"):
        resolve_surface_selection(language="fr", input_func=never_ask)
    assert build_parser().parse_args(["--language", "en"]).language == "en"
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--language", "fr"])


def test_operations_dir_matching_a_surface_derives_that_surface_and_custom_stays_custom(tmp_path: Path) -> None:
    def never_ask(_question: str) -> str:
        raise AssertionError("an explicit operations dir must not prompt interactively")

    english = resolve_surface_selection(
        operations_dir=REPO_ROOT / "project-os-en" / "operations", input_func=never_ask
    )
    assert english.language == "en"
    assert english.skills_catalog_path == REPO_ROOT / "project-os-en" / "kernel" / "skills.json"

    custom = resolve_surface_selection(operations_dir=tmp_path / "operations", input_func=never_ask)
    assert custom.language == "custom"
    assert custom.kernel_dir is None
    assert custom.skills_catalog_path == DEFAULT_SKILLS_CATALOG

    injected = resolve_surface_selection(
        operations_dir=tmp_path / "operations",
        skills_catalog_path=tmp_path / "skills.json",
        input_func=never_ask,
    )
    assert injected.skills_catalog_path == tmp_path / "skills.json"


def test_incompatible_language_and_operations_dir_fail_closed(tmp_path: Path) -> None:
    for language, operations_dir in (
        ("en", DEFAULT_OPERATIONS_DIR),
        ("es", REPO_ROOT / "project-os-en" / "operations"),
        ("es", tmp_path / "operations"),
    ):
        with pytest.raises(WizardError, match="never mixes operations and skills"):
            resolve_surface_selection(language=language, operations_dir=operations_dir)


def test_known_surface_rejects_skills_catalog_from_another_surface(tmp_path: Path) -> None:
    def never_ask(_question: str) -> str:
        raise AssertionError("explicit selections must not prompt interactively")

    es_catalog = REPO_ROOT / "project-os-es" / "kernel" / "skills.json"
    en_catalog = REPO_ROOT / "project-os-en" / "kernel" / "skills.json"
    for kwargs in (
        {"language": "en", "skills_catalog_path": es_catalog},
        {"language": "es", "skills_catalog_path": en_catalog},
        {
            "operations_dir": REPO_ROOT / "project-os-en" / "operations",
            "skills_catalog_path": es_catalog,
        },
        {
            "operations_dir": REPO_ROOT / "project-os-es" / "operaciones",
            "skills_catalog_path": en_catalog,
        },
        {"language": "es", "skills_catalog_path": tmp_path / "skills.json"},
    ):
        with pytest.raises(WizardError, match="never mixes operations and skills"):
            resolve_surface_selection(input_func=never_ask, **kwargs)


def test_known_surface_accepts_its_own_canonical_skills_catalog() -> None:
    def never_ask(_question: str) -> str:
        raise AssertionError("explicit selections must not prompt interactively")

    en_catalog = REPO_ROOT / "project-os-en" / "kernel" / "skills.json"
    english = resolve_surface_selection(
        language="en", skills_catalog_path=en_catalog, input_func=never_ask
    )
    assert english.language == "en"
    assert english.skills_catalog_path == en_catalog

    unnormalized = REPO_ROOT / "tools" / ".." / "project-os-en" / "kernel" / "skills.json"
    assert resolve_surface_selection(
        language="en", skills_catalog_path=unnormalized, input_func=never_ask
    ).skills_catalog_path == en_catalog

    spanish = resolve_surface_selection(
        operations_dir=REPO_ROOT / "project-os-es" / "operaciones",
        skills_catalog_path=REPO_ROOT / "project-os-es" / "kernel" / "skills.json",
        input_func=never_ask,
    )
    assert spanish.language == "es"
    assert spanish.skills_catalog_path == REPO_ROOT / "project-os-es" / "kernel" / "skills.json"


def test_language_question_is_asked_once_per_session(tmp_path: Path) -> None:
    asked: list[str] = []
    values = iter(
        (
            "",
            "MOS-3.5",
            "405", "", "none", "", "", "", "1",
            "write",
            "new",
            "cancel",
            "exit",
        )
    )

    def input_func(question: str) -> str:
        if question == LANGUAGE_QUESTION:
            asked.append(question)
        return next(values)

    stream = StringIO()
    output = run_wizard(output_dir=tmp_path, input_func=input_func, output_stream=stream)

    assert output is not None
    assert asked == [LANGUAGE_QUESTION]
    assert stream.getvalue().count("Session surface: es (session-only") >= 2


def test_english_language_loads_coherent_english_bundle(tmp_path: Path) -> None:
    stream = StringIO()
    output = run_wizard(
        language="en",
        output_dir=tmp_path,
        input_func=answers("MOS-3.5", "405", "", "none", "", "", "", "1", "write", "exit"),
        output_stream=stream,
    )

    assert output is not None
    transcript = stream.getvalue()
    content = output.read_text(encoding="utf-8")
    assert "Session surface: en (session-only" in transcript
    assert "Operations catalog: project-os-en/operations" in transcript
    assert "Skills catalog: project-os-en/kernel/skills.json" in transcript
    assert "Kernel (reference only, not applied): project-os-en/kernel" in transcript
    assert "skill.arquitectura_backend — Backend architecture" in transcript
    assert "skill.desarrollo_frontend — Frontend development" in transcript
    assert "MOS-3.5 — Draft correction route prompt" in content
    assert "project-os-en/operations/README.md" in content
    assert "project-os-es" not in content


def test_english_skills_catalog_loads_names_from_name_field() -> None:
    options = load_active_skill_options(REPO_ROOT / "project-os-en" / "kernel" / "skills.json")
    assert [option.key for option in options] == [
        "skill.arquitectura_backend",
        "skill.desarrollo_frontend",
    ]
    assert [option.name for option in options] == ["Backend architecture", "Frontend development"]


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
