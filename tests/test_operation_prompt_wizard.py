"""Behavior guards for the active Spanish operation-prompt wizard."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

import pytest

from tools.operation_prompt_wizard import (
    DEFAULT_OPERATIONS_DIR,
    DEFAULT_SKILLS_CATALOG,
    HYDRATION_LEVEL_CHOICES,
    HYDRATION_LEVEL_NAME,
    LANGUAGE_QUESTION,
    REPO_ROOT,
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
    is_hydration_override_command,
    normalize_variable_value,
    parse_hydration_override,
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


def test_duplicate_mos_code_fails_catalog_discovery_closed(tmp_path: Path) -> None:
    write_spanish_operation(tmp_path / "fase-1" / "MOS-1.1-duplicada.md", "MOS-1.1", "Uno")
    write_spanish_operation(tmp_path / "fase-2" / "MOS-1.1-duplicada.md", "MOS-1.1", "Dos")

    with pytest.raises(WizardError, match="OPS-002.*status.needs_pm_decision"):
        discover_operations(tmp_path)


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


# Identifiers a live locator can always reconstruct. They may never be captured
# next to the locator that already resolves them.
DERIVED_IDENTIFIERS = (
    "ISSUE_NUMBER",
    "PR_NUMBER",
    "ROADMAP_ISSUE",
    "SOURCE_REVIEW",
    "CHANGE_CLASS",
    "HYDRATION_LEVEL",
    "BRANCH_NAME",
)

# Primary locators: a live reference that identifies its own evidence chain.
PRIMARY_LOCATORS = (
    "WORK_UNIT",
    "FOLLOW_UP_SOURCE",
    "DECISION_SOURCE",
    "QA_SOURCE",
    "QA_RESULT",
    "AUDIT_RESULT",
    "SECURITY_REVIEW_RESULT",
    "DESIGN_DELIVERY",
    "CHECKLIST_RESULT",
    "MANUAL_IMPLEMENTATION_RESULT",
    "ROUTING_SOURCE",
    "READINESS_SOURCE",
    "AUDIT_SCOPE",
    "EXECUTION_REPORT",
    "VALIDATION_FINDINGS",
    "DEPLOYMENT_RESULT",
    "ROLLBACK_RESULT",
)


def operations_for(language: str):
    return discover_operations(
        REPO_ROOT
        / ("project-os-es/operaciones" if language == "es" else "project-os-en/operations")
    )


# The only operations allowed to carry a locator next to an identifier that
# usually derives from it, each for a contractual reason:
#   MOS-3.7  — PR_NUMBER locates the PR under review; EXECUTION_REPORT is report
#              text the PM pastes, not a reference the PR resolves.
#   MOS-3.31 — the change class requires a formal unit, so the issue stays even
#              though the live manual result also identifies the work.
DOCUMENTED_LOCATOR_EXCEPTIONS = {
    "MOS-3.7": {"PR_NUMBER"},
    "MOS-3.31": {"ISSUE_NUMBER"},
}


@pytest.mark.parametrize("language", ("es", "en"))
def test_no_active_operation_captures_a_locator_and_its_derived_identifiers(
    language: str,
) -> None:
    offenders = {}
    for operation in operations_for(language):
        names = {variable.name for variable in operation.variables}
        if not names & set(PRIMARY_LOCATORS):
            continue
        derived = names & set(DERIVED_IDENTIFIERS)
        derived -= DOCUMENTED_LOCATOR_EXCEPTIONS.get(operation.mos_code, set())
        if derived:
            offenders[operation.mos_code] = sorted(derived)

    assert offenders == {}


@pytest.mark.parametrize("language", ("es", "en"))
def test_route_operations_ask_one_locator_and_keep_authorization_explicit(language: str) -> None:
    for mos_code, locator_required in (("MOS-3.4", False), ("MOS-3.5", True)):
        operation = next(
            candidate for candidate in operations_for(language) if candidate.mos_code == mos_code
        )
        variables = {variable.name: variable for variable in operation.variables}

        # One primary locator, the optional skill the PM chooses, and nothing the
        # live unit already resolves.
        assert variables["WORK_UNIT"].required is locator_required
        assert "OPTIONAL_SKILL" in variables
        assert operation_output_refs(operation) == ("output.route_prompt",)
        assert "RECOMMENDED_TERMINAL_AGENT_FAMILY" not in variables

        # Authorization stays explicit and is the wizard's own required variable.
        assert operation_needs_pm_authorization_assistance(operation) is True
        assert [(variable.name, variable.required) for variable in wizard_variables(operation)][-1] == (
            PM_AUTHORIZATION_STATUS_NAME,
            True,
        )

        rendered = render_prompt(
            operation,
            {
                "WORK_UNIT": "issue #405",
                PM_AUTHORIZATION_STATUS_NAME: PM_AUTHORIZATION_GRANTED,
            },
        )
        assert "WORK_UNIT=issue #405" in rendered
        assert rendered.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
        assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in rendered
        for derived in DERIVED_IDENTIFIERS:
            assert f"{derived}=" not in rendered


@pytest.mark.parametrize("language", ("es", "en"))
def test_follow_up_asks_one_optional_locator_without_related_identifiers(language: str) -> None:
    follow_up = next(
        operation for operation in operations_for(language) if operation.mos_code == "MOS-3.3"
    )
    variables = {variable.name: variable for variable in follow_up.variables}

    # The locator is optional because a source already selected in the session is
    # never asked for again.
    assert variables["FOLLOW_UP_SOURCE"].required is False
    # A bundle draft never carries an authorization variable, and the related
    # issue, PR, and review are derived from the single live source.
    assert operation_needs_pm_authorization_assistance(follow_up) is False
    assert [variable.name for variable in wizard_variables(follow_up)] == list(variables)

    rendered = render_prompt(follow_up, {"FOLLOW_UP_SOURCE": "review de PR #463"})
    assert "FOLLOW_UP_SOURCE=review de PR #463" in rendered
    for derived in DERIVED_IDENTIFIERS:
        assert f"{derived}=" not in rendered
    assert PM_AUTHORIZATION_STATUS_NAME not in rendered


def test_target_repository_uses_generic_repository_validation() -> None:
    variable = InputVariable("TARGET_REPOSITORY", "<TARGET_REPOSITORY>", True, "")

    error = validate_variable_value(variable, "")
    assert error is not None and "TARGET_REPOSITORY is required" in error
    for invalid in ("owner", "owner/", "/repo", "owner repo", "https://github.com/o/r", "o/r/extra"):
        error = validate_variable_value(variable, invalid)
        assert error is not None and "must look like owner/repo" in error
    assert validate_variable_value(variable, "codefusion-repo/project-os-v2") is None


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_0_1_binds_a_declared_target_and_still_rejects_a_malformed_one(
    tmp_path: Path, language: str
) -> None:
    stream = StringIO()
    output = run_wizard(
        language=language,
        output_dir=tmp_path,
        input_func=answers(
            "MOS-0.1",
            "not a repo",
            "codefusion-repo/project-os-v2",
            "",
            "",
            "write",
            "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    # A declared target is still validated: only the requirement to declare one
    # was dropped, never the exact-identity check.
    assert "must look like owner/repo" in stream.getvalue()
    content = output.read_text(encoding="utf-8")
    assert content.count("TARGET_REPOSITORY=") == 1
    assert "TARGET_REPOSITORY=codefusion-repo/project-os-v2" in content
    assert f"{PM_AUTHORIZATION_STATUS_NAME}=" not in content


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_0_1_activates_an_unbound_session_without_a_target(
    tmp_path: Path, language: str
) -> None:
    stream = StringIO()
    output = run_wizard(
        language=language,
        output_dir=tmp_path,
        input_func=answers("MOS-0.1", "", "", "", "write", "exit"),
        output_stream=stream,
    )

    assert output is not None
    transcript = stream.getvalue()
    # Starting without a repository is a supported session state, not a gap: the
    # wizard neither demands the target nor fills one in.
    assert "TARGET_REPOSITORY is required" not in transcript
    content = output.read_text(encoding="utf-8")
    assert "TARGET_REPOSITORY=\n" in content
    assert content.count("TARGET_REPOSITORY=") == 1
    assert f"{PM_AUTHORIZATION_STATUS_NAME}=" not in content


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_3_24_accepts_one_locator_without_a_redundant_repository(
    tmp_path: Path, language: str
) -> None:
    operation = next(
        item for item in operations_for(language) if item.mos_code == "MOS-3.24"
    )
    variables = {variable.name: variable for variable in operation.variables}

    assert variables["AUDIT_SCOPE"].required is False
    assert variables["PATH_SCOPE"].required is False
    assert variables["FOCUS"].required is False
    assert set(variables) == {
        "AUDIT_SCOPE",
        "PATH_SCOPE",
        "FOCUS",
        "PM_FEEDBACK_HUMANO",
        "PM_QUESTION_HUMANO",
    }

    audit_scopes = ("codefusion-repo/project-os-v2", "issue #465", "PR #467")
    for index, audit_scope in enumerate(audit_scopes):
        stream = StringIO()
        prompts: list[str] = []
        responses = iter(
            (
                "MOS-3.24",
                audit_scope,
                "src",
                "single locator",
                "",
                "",
                "write",
                "exit",
            )
        )

        def input_func(prompt: str) -> str:
            prompts.append(prompt)
            return next(responses)

        output = run_wizard(
            language=language,
            output_dir=tmp_path / str(index),
            input_func=input_func,
            output_stream=stream,
        )

        assert output is not None
        assert "TARGET_REPOSITORY" not in stream.getvalue()
        assert sum(prompt.startswith("AUDIT_SCOPE (optional") for prompt in prompts) == 1
        content = output.read_text(encoding="utf-8")
        assert "TARGET_REPOSITORY=" not in content
        assert content.count("AUDIT_SCOPE=") == 1
        assert f"AUDIT_SCOPE={audit_scope}" in content
        assert "PATH_SCOPE=src" in content
        assert "FOCUS=single locator" in content


def test_audit_scope_rejects_unverifiable_locator_formats() -> None:
    variable = InputVariable("AUDIT_SCOPE", "<AUDIT_SCOPE>", False, "")

    for valid in ("", "codefusion-repo/project-os-v2", "issue #465", "PR 467"):
        assert validate_variable_value(variable, valid) is None
    for invalid in ("owner", "issue", "#465", "review #467", "https://github.com/o/r"):
        error = validate_variable_value(variable, invalid)
        assert error is not None and "AUDIT_SCOPE must be owner/repo, issue #N, or PR #N" in error


@pytest.mark.parametrize("language", ("es", "en"))
def test_hydration_override_never_contaminates_non_route_or_non_route_paths(
    tmp_path: Path, language: str
) -> None:
    no_route_stream = StringIO()
    no_route = run_wizard(
        language=language,
        output_dir=tmp_path / "no-route",
        input_func=answers(
            "MOS-0.1",
            "/hydration full/debug",
            "",
            "",
            "",
            "write",
            "exit",
        ),
        output_stream=no_route_stream,
    )

    assert no_route is not None
    assert f"{HYDRATION_LEVEL_NAME}=" not in no_route.read_text(encoding="utf-8")
    assert "only for an output.route_prompt path" in no_route_stream.getvalue()

    arbitrary_non_route = next(
        item for item in operations_for(language) if item.mos_code == "MOS-3.24"
    )
    assert f"{HYDRATION_LEVEL_NAME}=" not in render_prompt(
        arbitrary_non_route, {HYDRATION_LEVEL_NAME: "full/debug"}
    )

    multi_output_stream = StringIO()
    multi_output = run_wizard(
        language=language,
        output_dir=tmp_path / "multi-output",
        input_func=answers(
            "MOS-3.14",
            "/hydration full/debug",
            "audit result",
            "",
            "",
            "2",
            "write",
            "exit",
        ),
        output_stream=multi_output_stream,
    )

    assert multi_output is not None
    assert f"{HYDRATION_LEVEL_NAME}=" not in multi_output.read_text(encoding="utf-8")
    assert "override dropped because the selected output is non-route" in multi_output_stream.getvalue()


@pytest.mark.parametrize("language", ("es", "en"))
def test_route_surfaces_separate_human_inputs_metadata_and_inferred_recommendation(
    language: str,
) -> None:
    root = REPO_ROOT / ("project-os-es" if language == "es" else "project-os-en")
    template = (root / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    labels = (
        ("inputs humanos", "metadata derivada", "recomendación inferida")
        if language == "es"
        else ("Human inputs", "Derived metadata", "inferred recommendation")
    )
    assert all(label in template for label in labels)
    for field in (
        "OPTIONAL_SKILL",
        "PM_FEEDBACK_HUMANO",
        "PM_QUESTION_HUMANO",
        "PM_AUTHORIZATION_STATUS",
        "HYDRATION_LEVEL",
        "RECOMMENDED_TERMINAL_AGENT_FAMILY",
    ):
        assert field in template

    for mos_code in ("MOS-3.4", "MOS-3.5"):
        operation = next(item for item in operations_for(language) if item.mos_code == mos_code)
        variables = {variable.name for variable in operation.variables}
        assert {"OPTIONAL_SKILL", "PM_FEEDBACK_HUMANO", "PM_QUESTION_HUMANO"} <= variables
        assert "RECOMMENDED_TERMINAL_AGENT_FAMILY" not in variables


@pytest.mark.parametrize("language", ("es", "en"))
def test_mos_6_11_resolves_as_the_supported_mos_3_14_alias(language: str) -> None:
    operations = operations_for(language)
    canonical = next(item for item in operations if item.mos_code == "MOS-3.14")
    alias = next(item for item in operations if item.mos_code == "MOS-6.11")

    assert canonical.aliases == ("MOS-6.11",)
    assert alias.is_alias is True
    assert alias.resolved_canonical_code == "MOS-3.14"
    rendered = render_prompt(alias, {"AUDIT_RESULT": "code audit"})
    assert "Alias requested: `MOS-6.11`; canonical operation resolved: `MOS-3.14`" in rendered
    assert "Process audit result" in rendered or "Procesar el resultado de una auditoría" in rendered


def test_mos_r3_asks_one_locator_and_derives_the_related_identifiers() -> None:
    for operations_dir in (
        REPO_ROOT / "project-os-es" / "operaciones",
        REPO_ROOT / "project-os-en" / "operations",
    ):
        operation = next(
            item for item in discover_operations(operations_dir) if item.mos_code == "MOS-R.3"
        )
        names = [variable.name for variable in operation.variables]
        # DECISION_SOURCE is the single primary locator; the issue and the PR it
        # points at are derived, so neither is captured or rendered.
        assert names[0] == "DECISION_SOURCE"
        assert "ISSUE_NUMBER" not in names
        assert "PR_NUMBER" not in names
        assert [variable.name for variable in wizard_variables(operation)] == names

        rendered = render_prompt(operation, {"DECISION_SOURCE": "review de PR #463"})
        assert "DECISION_SOURCE=review de PR #463" in rendered
        assert "ISSUE_NUMBER=" not in rendered
        assert "PR_NUMBER=" not in rendered


def test_mos_r3_validates_the_decision_state_pair() -> None:
    operation = next(item for item in discover_operations() if item.mos_code == "MOS-R.3")
    variables = {variable.name: variable for variable in operation.variables}

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


def test_mos_r3_line_collection_keeps_the_decision_pair_consistent() -> None:
    operation = next(item for item in discover_operations() if item.mos_code == "MOS-R.3")

    decided_stream = StringIO()
    decided = collect_values_with_controls(
        operation,
        input_func=answers("security review", "sí", "", "/clear", "Apply option A"),
        output_stream=decided_stream,
    )
    assert decided.values == {
        "DECISION_SOURCE": "security review",
        "PM_DECISION_ALREADY_MADE": "true",
        "DECISION_OPTIONS": "",
        "PM_DECISION": "Apply option A",
    }
    assert "PM_DECISION is required" in decided_stream.getvalue()

    options_needed = collect_values_with_controls(
        operation,
        input_func=answers("QA result", "no", "", ""),
        output_stream=StringIO(),
    )
    assert options_needed.values == {
        "DECISION_SOURCE": "QA result",
        "PM_DECISION_ALREADY_MADE": "false",
        "DECISION_OPTIONS": "",
        "PM_DECISION": "",
    }


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
    assert "DECISION_SOURCE=MOS-3.7 review" in content
    assert "ISSUE_NUMBER=" not in content
    assert "PR_NUMBER=" not in content
    assert "PM_DECISION_ALREADY_MADE=true" in content
    assert "PM_DECISION=Apply the scoped correction" in content


def test_mos_r3_wizard_generates_artifact_without_references_and_rejects_contradictory_decision(
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
    assert "DECISION_SOURCE=QA result" in content
    assert "ISSUE_NUMBER=" not in content
    assert "PR_NUMBER=" not in content
    assert "PM_DECISION_ALREADY_MADE=false" in content
    assert "DECISION_OPTIONS=" in content
    assert "PM_DECISION=" in content
    assert "must be empty" in stream.getvalue()


def test_line_wizard_active_mos35_generates_pending_route_prompt(tmp_path: Path) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "",
            "/phases",
            "MOS-3.5",
            "405", "none", "", "", "1",
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
    assert "WORK_UNIT=405" in content
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_PENDING}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    # Derived metadata is reconstructed by browser chat, never a manual wizard
    # input, so none of it renders as an INPUT variable.
    for derived in DERIVED_IDENTIFIERS:
        assert f"{derived}=" not in content
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
            "405", "skill.arquitectura_backend", "", "", "2",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    content = output.read_text(encoding="utf-8")
    assert f"{PM_AUTHORIZATION_STATUS_NAME}={PM_AUTHORIZATION_GRANTED}" in content
    assert content.count(f"{PM_AUTHORIZATION_STATUS_NAME}=") == 1
    assert "WORK_UNIT=405" in content
    # The class, density, roadmap, and branch travel as derived metadata, so the
    # PM is never asked to retype them.
    for derived in DERIVED_IDENTIFIERS:
        assert f"{derived}=" not in content
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
        "skill.desarrollo_mobile",
        "skill.desarrollo_videojuegos",
        "none",
    )
    variable = InputVariable("OPTIONAL_SKILL", "<OPTIONAL_SKILL>", False, "")
    assert validate_variable_value(variable, "") is None
    assert validate_variable_value(variable, "skill.arquitectura_backend") is None
    assert validate_variable_value(variable, "skill.desarrollo_frontend") is None
    assert validate_variable_value(variable, "skill.desarrollo_mobile") is None
    assert validate_variable_value(variable, "skill.desarrollo_videojuegos") is None
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
    assert "skill.desarrollo_mobile — Desarrollo mobile" in transcript
    assert "skill.desarrollo_videojuegos — Desarrollo de videojuegos" in transcript
    assert "none — Sin skill opcional" in transcript
    assert "Enter — Dejar vacío" in transcript
    assert "OPTIONAL_SKILL must be an active skill or none" in transcript
    assert prompts.count("Select OPTIONAL_SKILL: ") == 2


def test_route_prompt_template_keeps_ai_advisory_field_without_pm_input() -> None:
    template = (DEFAULT_OPERATIONS_DIR.parent / "templates" / "route-prompt.md").read_text(encoding="utf-8")
    assert "RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}" in template
    assert (
        "HYDRATION_LEVEL = {{opcional; omitir salvo override explícito: "
        "minimal | compact | full/debug}}" in template
    )
    assert "`compact` es el valor predeterminado global" in template
    assert "browser chat infiere" in template
    assert "feedback explícito\ndel PM puede reemplazar" in template

    for mos_code in ("MOS-3.4", "MOS-3.5"):
        operation = next(candidate for candidate in discover_operations() if candidate.mos_code == mos_code)
        assert "RECOMMENDED_TERMINAL_AGENT_FAMILY" not in [variable.name for variable in operation.variables]
        assert "browser chat" in operation.text

    # Neither route prompt captures the class or the density: both are derived
    # from the unit's live evidence.
    for mos_code in ("MOS-3.4", "MOS-3.5"):
        operation = next(
            candidate for candidate in discover_operations() if candidate.mos_code == mos_code
        )
        names = [variable.name for variable in operation.variables]
        assert HYDRATION_LEVEL_NAME not in names
        assert "CHANGE_CLASS" not in names


def test_hydration_override_is_never_prompted_and_renders_only_when_declared(
    tmp_path: Path,
) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "es",
            "MOS-3.4",
            "405", "none", "", "", "2",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    transcript = stream.getvalue()
    # The density is derived, so the wizard never asks for it and never emits it.
    assert f"{HYDRATION_LEVEL_NAME} (" not in transcript
    assert f"{HYDRATION_LEVEL_NAME}=" not in output.read_text(encoding="utf-8")


def test_hydration_override_records_an_explicit_level_and_can_be_dropped(
    tmp_path: Path,
) -> None:
    stream = StringIO()
    output = run_wizard(
        output_dir=tmp_path,
        input_func=answers(
            "es",
            "MOS-3.4",
            "/hydration verbose",
            "/hydration full/debug",
            "405", "none", "", "", "2",
            "write", "exit",
        ),
        output_stream=stream,
    )

    assert output is not None
    transcript = stream.getvalue()
    assert f"{HYDRATION_LEVEL_NAME} override must be one of" in transcript
    assert f"{HYDRATION_LEVEL_NAME} override recorded: full/debug" in transcript
    content = output.read_text(encoding="utf-8")
    assert f"{HYDRATION_LEVEL_NAME}=full/debug" in content
    assert content.count(f"{HYDRATION_LEVEL_NAME}=") == 1

    dropped_stream = StringIO()
    dropped = run_wizard(
        output_dir=tmp_path / "dropped",
        input_func=answers(
            "es",
            "MOS-3.4",
            "/hydration full/debug",
            "/hydration",
            "405", "none", "", "", "2",
            "write", "exit",
        ),
        output_stream=dropped_stream,
    )

    assert dropped is not None
    assert f"{HYDRATION_LEVEL_NAME} override dropped" in dropped_stream.getvalue()
    assert f"{HYDRATION_LEVEL_NAME}=" not in dropped.read_text(encoding="utf-8")


def test_hydration_override_parsing_accepts_every_level_and_rejects_unknown_ones() -> None:
    for level in HYDRATION_LEVEL_CHOICES:
        assert parse_hydration_override(f"/hydration {level}") == (level, None)
    assert parse_hydration_override("/hydration-level FULL/DEBUG") == ("full/debug", None)
    assert parse_hydration_override("/hydration") == ("", None)

    _, error = parse_hydration_override("/hydration verbose")
    assert error is not None
    # Hydration is independent of the class, so the wizard offers all three
    # levels without ranking them and without implying any authority.
    assert "any of the three is allowed for any class" in error

    assert is_hydration_override_command("/hydration full/debug") is True
    assert is_hydration_override_command("405") is False
    assert is_hydration_override_command("") is False


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
            "405", "#5054784601", "463", "change_class.standard", "none", "", "", "", "1",
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
        input_func=answers("MOS-3.5", "405", "#5054784601", "463", "change_class.standard", "none", "", "", "", "1", "write", "exit"),
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
    assert "skill.desarrollo_mobile — Mobile development" in transcript
    assert "skill.desarrollo_videojuegos — Game development" in transcript
    assert "MOS-3.5 — Draft correction route prompt" in content
    assert "project-os-en/operations/README.md" in content
    assert "project-os-es" not in content


def test_english_skills_catalog_loads_names_from_name_field() -> None:
    options = load_active_skill_options(REPO_ROOT / "project-os-en" / "kernel" / "skills.json")
    assert [option.key for option in options] == [
        "skill.arquitectura_backend",
        "skill.desarrollo_frontend",
        "skill.desarrollo_mobile",
        "skill.desarrollo_videojuegos",
    ]
    assert [option.name for option in options] == [
        "Backend architecture",
        "Frontend development",
        "Mobile development",
        "Game development",
    ]


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
