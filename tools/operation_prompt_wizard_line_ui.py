"""Line-based UI adapter for the operation prompt wizard."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

from tools.operation_prompt_wizard_catalog import display_path, load_active_skill_choices, load_active_skill_options
from tools.operation_prompt_wizard_core import *  # noqa: F403 - this adapter consumes the full pure contract.
from tools.operation_prompt_wizard_core import _operation_phase


def _validate_variable_value(
    variable: InputVariable,
    value: str,
    skill_choices: tuple[str, ...] | None = None,
    current_values: dict[str, str] | None = None,
) -> str | None:
    """Keep programmatic line-adapter calls compatible with catalog-backed skills."""

    if skill_choices is None and is_optional_skill_variable(variable.name):
        skill_choices = load_active_skill_choices()
    return validate_variable_value(variable, value, skill_choices, current_values)

def display_operations(
    operations: list[OperationTemplate], output_stream: TextIO, *, canonicalize: bool = True
) -> None:
    """Print the canonical catalog view or an explicit filtered result set."""

    print("", file=output_stream)
    print("Available operations:", file=output_stream)
    visible_operations = canonical_operations(operations) if canonicalize else operations
    for operation in visible_operations:
        print(f"  {operation_display_line(operation)}", file=output_stream)


def print_enumerated_view(operations: list[OperationTemplate], output_stream: TextIO) -> None:
    """Confirm and render the compact enumerated operation view."""

    print("", file=output_stream)
    print("View: enumerated operations", file=output_stream)
    display_operations(operations, output_stream)


def operation_display_line(operation: OperationTemplate, include_phase: bool = True) -> str:
    """Build the shared compact list/completion representation."""

    phase = operation.phase_label or operation.phase_path or "Catálogo"
    phase_part = f"[{phase}] " if include_phase else ""
    identity = operation.mos_code or operation.path.stem
    if operation.is_alias:
        identity = f"{identity} → canonical {operation.resolved_canonical_code}"
    alias_part = f" [aliases: {', '.join(operation.aliases)}]" if operation.aliases else ""
    return f"{operation.index:>3}. {phase_part}{identity} — {operation.description}{alias_part}"


def print_phase_groups(
    operations: list[OperationTemplate],
    phase_by_operation: dict[int, str],
    output_stream: TextIO,
) -> None:
    """Print operations grouped by an optional active phase map."""

    print("", file=output_stream)
    print("View: operations grouped by phase", file=output_stream)
    if not phase_by_operation:
        print("Phase information is unavailable; showing the ungrouped operation list.", file=output_stream)
        display_operations(operations, output_stream)
        return

    print("Operations grouped by SDLC phase:", file=output_stream)
    grouped: dict[str, list[OperationTemplate]] = {}
    ordered_phases: list[str] = []
    for operation in canonical_operations(operations):
        phase = _operation_phase(operation, phase_by_operation)
        if phase not in grouped:
            grouped[phase] = []
            ordered_phases.append(phase)
        grouped[phase].append(operation)

    for phase in ordered_phases:
        print(f"  {phase}:", file=output_stream)
        for operation in grouped[phase]:
            print(f"    {operation_display_line(operation, include_phase=False)}", file=output_stream)


def print_stage(label: str, title: str, output_stream: TextIO) -> None:
    """Print a compact stage marker for the line-based flow."""

    print("", file=output_stream)
    print(f"[{label}] {title}", file=output_stream)


def print_session_surface(
    selection: SurfaceSelection,
    output_directory: Path,
    output_stream: TextIO,
) -> None:
    """Print the session-only surface bundle as local orientation, never adoption."""

    print("", file=output_stream)
    print(
        f"Session surface: {selection.language} (session-only; does not configure or adopt the target)",
        file=output_stream,
    )
    print(f"  Operations catalog: {display_path(selection.operations_dir)}", file=output_stream)
    print(f"  Skills catalog: {display_path(selection.skills_catalog_path)}", file=output_stream)
    if selection.kernel_dir is not None:
        print(
            f"  Kernel (reference only, not applied): {display_path(selection.kernel_dir)}",
            file=output_stream,
        )
    else:
        print("  Kernel (reference only, not applied): none for a custom catalog", file=output_stream)
    print(f"  Output directory: {output_directory}", file=output_stream)


def print_session_state(
    output_stream: TextIO,
    current_prompt_path: Path | None,
    selection: SurfaceSelection | None = None,
    output_directory: Path | None = None,
) -> None:
    """Print visible surface, output-mode, and current-prompt session state."""

    if selection is not None and output_directory is not None:
        print_session_surface(selection, output_directory, output_stream)
    else:
        print("", file=output_stream)
    print("Output mode: single latest prompt", file=output_stream)
    if current_prompt_path is not None:
        print(f"Current prompt: {current_prompt_path}", file=output_stream)
    else:
        print("Current prompt: none yet.", file=output_stream)


def apply_hydration_override(
    raw_value: str, values: dict[str, str], output_stream: TextIO
) -> None:
    """Record or drop the opt-in HYDRATION_LEVEL override without asking for it."""

    level, error = parse_hydration_override(raw_value)
    if error is not None:
        print(f"Invalid value: {error}", file=output_stream)
        return
    if level:
        values[HYDRATION_LEVEL_NAME] = level
        print(
            f"{HYDRATION_LEVEL_NAME} override recorded: {level}. It only changes how "
            "much resolved contract the agent receives, and it authorizes nothing.",
            file=output_stream,
        )
        return
    values.pop(HYDRATION_LEVEL_NAME, None)
    print(
        f"{HYDRATION_LEVEL_NAME} override dropped; the resolver applies its compact "
        "default.",
        file=output_stream,
    )


def print_selection_help(output_stream: TextIO) -> None:
    """Print operation-selection help without leaving the current flow."""

    print("", file=output_stream)
    print("Selection help:", file=output_stream)
    print(
        f"  Describe your intent in your own words; text that names no catalog entry "
        f"routes via {INTENT_ROUTING_MOS_CODE}, which recommends one operation from live "
        "evidence. This never authorizes anything.",
        file=output_stream,
    )
    print(
        "  Filter by title, filename, stem, relative path, phase directory, MOS code, "
        "or displayed index.",
        file=output_stream,
    )
    print(
        "  Select by displayed index, exact filename/stem/path, or MOS code.",
        file=output_stream,
    )
    print(
        "  Compact list lines show phase, MOS code, and purpose. The exact relative path "
        "appears after selection and remains searchable.",
        file=output_stream,
    )
    print(
        "  Use /enumerated (aliases: /enumerator, /) for the enumerated view; "
        "/phases (alias: /phase) for the grouped view; s to search again; or cancel to exit.",
        file=output_stream,
    )


def variable_summary_lines(operation: OperationTemplate) -> list[str]:
    """Return a compact selected-operation summary for variable entry."""

    lines = [f"Selected: {operation_display_line(operation).strip()}"]
    if operation.is_alias:
        lines.append(
            f"Canonical resolution: {operation.mos_code} -> {operation.resolved_canonical_code} "
            f"({operation.deprecation})"
        )
        if operation.canonical_path is not None and operation.catalog_root is not None:
            lines.append(
                f"Canonical path: {operation.canonical_path.relative_to(operation.catalog_root).as_posix()}"
            )
        if operation.alias_focus_area:
            lines.append(f"Linked focus: FOCUS_AREA={operation.alias_focus_area}")
    lines.append(f"Path: {operation.relative_path}")
    variables = wizard_variables(operation)
    required = [variable for variable in variables if variable.required]
    optional = [variable for variable in variables if not variable.required]
    lines.append(f"Required ({len(required)}): {format_variable_list(required)}")
    lines.append(f"Optional ({len(optional)}): {format_variable_list(optional)}")
    return lines


def format_variable_list(variables: list[InputVariable]) -> str:
    """Format variables compactly for the selected-operation summary."""

    if not variables:
        return "none"
    return ", ".join(f"{variable.name} {variable.placeholder}" for variable in variables)


def display_operation_summary(
    operation: OperationTemplate,
    output_stream: TextIO,
) -> None:
    """Print the selected operation and its INPUT variable summary."""

    for line in variable_summary_lines(operation):
        print(line, file=output_stream)


def print_optional_skill_options(
    output_stream: TextIO,
    skill_options: tuple[SkillOption, ...] | None = None,
) -> None:
    """Show every accepted OPTIONAL_SKILL choice immediately before its prompt."""

    options = skill_options if skill_options is not None else load_active_skill_options()
    print("", file=output_stream)
    print("OPTIONAL_SKILL (optional)", file=output_stream)
    for option in options:
        print(f"  - {option.key} — {option.name}", file=output_stream)
    print("  - none — Sin skill opcional / No optional skill", file=output_stream)
    print("  - Enter — Dejar vacío / Leave blank", file=output_stream)


def print_pm_authorization_assistance(output_stream: TextIO) -> None:
    """Explain route-prompt authorization-status assistance before asking."""

    print("", file=output_stream)
    print(
        "PM_AUTHORIZATION_STATUS: 1=pending; 2=granted for this exact scope and mode.",
        file=output_stream,
    )
    print(
        "Use 2 only for exact PM-approved scope/mode; generated prompt artifacts do not grant permission.",
        file=output_stream,
    )
    print(
        "Kernel evidence, branch preflight, validation, and fail-closed behavior still apply.",
        file=output_stream,
    )


def print_output_path_help(output_stream: TextIO) -> None:
    """Print multi-output route-prompt path help."""

    print("", file=output_stream)
    print("Output path help:", file=output_stream)
    print("  Choose route-prompt only when this prompt should emit output.route_prompt.", file=output_stream)
    print("  Choose non-route for status_result, pm_command_bundle, draft_issue, or other outputs.", file=output_stream)
    print("  A route-prompt path requires explicit PM_AUTHORIZATION_STATUS entry.", file=output_stream)


def print_value_help(output_stream: TextIO, allows_hydration_override: bool) -> None:
    """Print variable-entry help without leaving the current flow."""

    print("", file=output_stream)
    print("Variable entry help:", file=output_stream)
    print("  Required values must be filled; optional values may be left blank.", file=output_stream)
    print("  During edits, pressing Enter keeps the current value.", file=output_stream)
    print("  Use /clear to blank the current optional value.", file=output_stream)
    if allows_hydration_override:
        print(
            f"  Use /hydration <{' | '.join(HYDRATION_LEVEL_CHOICES)}> only to record an "
            f"explicit PM override of {HYDRATION_LEVEL_NAME}; /hydration with no level "
            "drops it and the resolver applies its compact default.",
            file=output_stream,
        )
        print(
            "  Any level is allowed for any class; the override only changes how much "
            "resolved contract the agent receives and never authorizes anything.",
            file=output_stream,
        )
    print("  Use back to choose another operation, cancel to exit, or ? for this help.", file=output_stream)


def select_operation(
    operations: list[OperationTemplate],
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    phase_by_operation: dict[int, str] | None = None,
    captured_intent: dict[str, str] | None = None,
    show_command_hints: bool = True,
) -> OperationTemplate | None:
    """Interactively search/filter/group and select one operation.

    A query that names no catalog entry at all (no exact match, no title/
    filename/path/phase match) is never a dead end: it is PM intent. When
    this catalog carries MOS-R.2, that intent is captured verbatim into
    ``captured_intent`` and MOS-R.2 is returned so the canonical routing
    capability -- not this wizard -- resolves it from live evidence.
    """

    phase_by_operation = phase_by_operation or {}
    filtered = canonical_operations(operations)
    print_stage("Step 1/3", "Search and select an operation", output_stream)
    print(
        "Describe what you want (target, outcome, constraints) to route via "
        f"{INTENT_ROUTING_MOS_CODE}, or select explicitly by index, MOS code, "
        "filename, title, relative path, or phase.",
        file=output_stream,
    )
    if show_command_hints:
        print(
            "Commands: /enumerated (aliases /enumerator, /), /phases (alias /phase), "
            "s search, ? help, cancel exit.",
            file=output_stream,
        )
    print_enumerated_view(filtered, output_stream)
    while True:
        query = input_func(
            "\nDescribe your intent, or search by index, MOS code, filename, title, "
            "relative path, or phase (Enter keeps view; /enumerated; /phases; ? help; cancel): "
        ).strip()
        if is_cancel_command(query):
            return None
        if is_help_command(query):
            print_selection_help(output_stream)
            continue
        if is_phase_view_command(query):
            filtered = canonical_operations(operations)
            print_phase_groups(operations, phase_by_operation, output_stream)
            continue
        if is_enumerated_view_command(query):
            filtered = canonical_operations(operations)
            print_enumerated_view(filtered, output_stream)
            continue
        if is_search_command(query):
            filtered = canonical_operations(operations)
            print_enumerated_view(filtered, output_stream)
            continue
        if query:
            operation = resolve_operation_selection(operations, query)
            if operation is not None:
                return operation
            matches = filter_operations(operations, query, phase_by_operation)
            if not matches:
                recommended = intent_routing_operation(operations)
                if recommended is not None:
                    if captured_intent is not None:
                        captured_intent[PM_QUESTION_HUMANO_NAME] = query
                    print(
                        f"No catalog match for that text. Treating it as your intent and "
                        f"routing via {recommended.mos_code} — {recommended.title}.",
                        file=output_stream,
                    )
                    return recommended
                print(
                    "No matching operations. Try a title, MOS code, filename, relative path, phase, or index.",
                    file=output_stream,
                )
                continue
            filtered = matches
            # A filtered alias is an explicit compatibility selection, not a
            # general catalog view: preserve it so its linked values survive.
            display_operations(filtered, output_stream, canonicalize=False)

        selection = input_func(
            "Select by displayed index, MOS code, exact filename/stem/path (s search again, ? help, cancel): "
        ).strip()
        if is_search_command(selection):
            display_operations(filtered, output_stream, canonicalize=False)
            continue
        if is_phase_view_command(selection):
            filtered = canonical_operations(operations)
            print_phase_groups(operations, phase_by_operation, output_stream)
            continue
        if is_enumerated_view_command(selection):
            filtered = canonical_operations(operations)
            print_enumerated_view(filtered, output_stream)
            continue
        if is_help_command(selection):
            print_selection_help(output_stream)
            continue
        if is_cancel_command(selection):
            return None
        # A displayed alias shares its canonical operation's catalog index.
        # Resolve numeric choices against the visible results so the index the
        # UI advertises cannot silently discard its linked compatibility data.
        normalized_selection = (
            selection.lower()
            .removeprefix("index:")
            .removeprefix("indice:")
            .removeprefix("índice:")
        )
        if normalized_selection.isdigit():
            displayed_matches = [
                operation for operation in filtered if operation.index == int(normalized_selection)
            ]
            operation = displayed_matches[0] if len(displayed_matches) == 1 else None
        else:
            operation = resolve_operation_selection(operations, selection)
        if operation is not None:
            return operation
        print(
            "Invalid or ambiguous selection. Use a displayed index, MOS code, or exact filename/stem/path.",
            file=output_stream,
        )


def collect_values(
    operation: OperationTemplate,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> dict[str, str]:
    """Prompt for required and optional variable values with validation."""

    result = collect_values_with_controls(
        operation,
        input_func=input_func,
        output_stream=output_stream,
    )
    return result.values


def collect_values_with_controls(
    operation: OperationTemplate,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    initial_values: dict[str, str] | None = None,
    skill_choices: tuple[str, ...] | None = None,
    skill_options: tuple[SkillOption, ...] | None = None,
    show_command_hints: bool = True,
) -> ValueCollectionResult:
    """Prompt for variable values and return navigation decisions."""

    values = dict(initial_values or {})
    print_stage("Step 2/3", "Fill INPUT variables", output_stream)
    display_operation_summary(operation, output_stream)
    variables = wizard_variables(operation)
    allows_hydration_override = operation_produces_route_prompt(operation)
    if not variables:
        print("This operation declares no INPUT variables.", file=output_stream)
        return ValueCollectionResult("values", values)

    print("", file=output_stream)
    if show_command_hints:
        commands = "Optional values may be left blank. Commands: back, cancel, /clear optional"
        if allows_hydration_override:
            commands += ", /hydration override"
        print(f"{commands}, ? help.", file=output_stream)
    for variable in variables:
        bound_value = alias_bound_values(operation).get(variable.name)
        if bound_value is not None:
            values[variable.name] = bound_value
            continue
        if is_pm_authorization_status_variable(variable.name):
            print_pm_authorization_assistance(output_stream)
        if is_optional_skill_variable(variable.name):
            print_optional_skill_options(output_stream, skill_options=skill_options)
        label = "required" if variable.required else "optional"
        while True:
            current = values.get(variable.name, "")
            current_hint = f", current: {single_line(current)}" if current else ""
            prompt_label = (
                f"Select OPTIONAL_SKILL{current_hint}: "
                if is_optional_skill_variable(variable.name)
                else f"{variable.name} ({label}, {variable.placeholder}{current_hint}): "
            )
            raw_value = input_func(prompt_label)
            if is_help_command(raw_value):
                print_value_help(output_stream, allows_hydration_override)
                continue
            if is_hydration_override_command(raw_value):
                if not allows_hydration_override:
                    print(
                        "Invalid command: /hydration is available only for an output.route_prompt path.",
                        file=output_stream,
                    )
                    continue
                apply_hydration_override(raw_value, values, output_stream)
                continue
            if is_cancel_command(raw_value):
                return ValueCollectionResult("cancel", values)
            if is_back_command(raw_value):
                return ValueCollectionResult("operation", values)
            if is_clear_command(raw_value):
                error = _validate_variable_value(
                    variable,
                    "",
                    skill_choices=skill_choices,
                    current_values=values,
                )
                if error is not None:
                    print(
                        f"Invalid value: {error}",
                        file=output_stream,
                    )
                    continue
                values[variable.name] = ""
                break

            value = raw_value.strip()
            if not value and current:
                value = current
            error = _validate_variable_value(
                variable,
                value,
                skill_choices=skill_choices,
                current_values=values,
            )
            if error is None:
                values[variable.name] = normalize_variable_value(variable, value)
                break
            print(f"Invalid value: {error}", file=output_stream)
    return ValueCollectionResult("values", values)


def collect_route_prompt_path_with_controls(
    operation: OperationTemplate,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    initial_values: dict[str, str] | None = None,
    show_command_hints: bool = True,
) -> RoutePromptPathResult:
    """Ask whether a multi-output operation is taking the route-prompt path."""

    values = dict(initial_values or {})
    print_stage("Step 2b/3", "Select output path", output_stream)
    refs = operation_output_refs(operation)
    non_route_refs = [ref for ref in refs if ref != "output.route_prompt"]
    print(
        "This operation has multiple possible outputs, including output.route_prompt.",
        file=output_stream,
    )
    if non_route_refs:
        print(f"Non-route outputs: {', '.join(non_route_refs)}.", file=output_stream)
    if show_command_hints:
        print("Commands: back, cancel, ? help.", file=output_stream)

    while True:
        answer = input_func(
            "Selected output path [1 route-prompt / 2 non-route]: "
        ).strip().lower()
        if is_help_command(answer):
            print_output_path_help(output_stream)
            continue
        if is_cancel_command(answer):
            return RoutePromptPathResult("cancel", values, False)
        if is_back_command(answer):
            return RoutePromptPathResult("values", values, False)
        if answer in {"2", "non-route", "nonroute", "status", "status_result", "pm_command_bundle"}:
            values.pop(PM_AUTHORIZATION_STATUS_NAME, None)
            if values.pop(HYDRATION_LEVEL_NAME, None) is not None:
                print(
                    f"{HYDRATION_LEVEL_NAME} override dropped because the selected output is non-route.",
                    file=output_stream,
                )
            return RoutePromptPathResult("preview", values, False)
        if answer in {"1", "route", "route-prompt", "route_prompt", "output.route_prompt"}:
            return collect_route_prompt_authorization_status(
                values,
                input_func=input_func,
                output_stream=output_stream,
            )
        print("Invalid output path. Choose 1 route-prompt, 2 non-route, back, or cancel.", file=output_stream)


def collect_route_prompt_authorization_status(
    values: dict[str, str],
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> RoutePromptPathResult:
    """Collect the authorization-status value for a confirmed route-prompt path."""

    variable = synthetic_pm_authorization_variable()
    print_pm_authorization_assistance(output_stream)
    while True:
        current = values.get(variable.name, "")
        current_hint = f", current: {single_line(current)}" if current else ""
        raw_value = input_func(
            f"{variable.name} (required, {variable.placeholder}{current_hint}): "
        )
        if is_help_command(raw_value):
            print_output_path_help(output_stream)
            print_pm_authorization_assistance(output_stream)
            continue
        if is_cancel_command(raw_value):
            return RoutePromptPathResult("cancel", values, True)
        if is_back_command(raw_value):
            values.pop(PM_AUTHORIZATION_STATUS_NAME, None)
            return RoutePromptPathResult("values", values, False)
        value = raw_value.strip()
        if not value and current:
            value = current
        error = _validate_variable_value(variable, value)
        if error is None:
            values[variable.name] = normalize_variable_value(variable, value)
            return RoutePromptPathResult("preview", values, True)
        print(f"Invalid value: {error}", file=output_stream)


def print_preview_help(output_stream: TextIO) -> None:
    """Print preview-action help without leaving the current flow."""

    print("", file=output_stream)
    print("Preview help:", file=output_stream)
    print(
        "  write: create the local .md prompt artifact and replace the previous "
        "wizard-generated prompt in this output folder.",
        file=output_stream,
    )
    print("  edit: return to variable entry and keep current values.", file=output_stream)
    print("  operation: choose another operation from the list.", file=output_stream)
    print("  cancel: exit without creating an output file.", file=output_stream)


def print_pre_write_summary(
    operation: OperationTemplate,
    values: dict[str, str],
    output_path: Path,
    replacing: list[Path],
    output_stream: TextIO,
    include_route_prompt_authorization: bool = False,
) -> None:
    """Print the selected operation, filled variables, output path, and replacement state."""

    print("", file=output_stream)
    print("Ready to write:", file=output_stream)
    print(f"  Operation: {operation_display_line(operation).strip()}", file=output_stream)
    print(f"  Source: {operation.relative_path}", file=output_stream)
    variables = wizard_variables(
        operation,
        include_route_prompt_authorization=include_route_prompt_authorization,
    )
    if variables:
        print("  Variables:", file=output_stream)
        for variable in variables:
            value = values.get(variable.name, "")
            shown = single_line(value) if value else "(empty)"
            print(f"    {variable.name}={shown}", file=output_stream)
    else:
        print("  Variables: none", file=output_stream)
    hydration_override = values.get(HYDRATION_LEVEL_NAME, "").strip()
    if hydration_override and not any(
        variable.name == HYDRATION_LEVEL_NAME for variable in variables
    ):
        print(
            f"  Explicit PM override: {HYDRATION_LEVEL_NAME}={hydration_override}",
            file=output_stream,
        )
    print(f"  Output path: {output_path}", file=output_stream)
    if replacing:
        print(
            "The previous prompt generated by this wizard in the output folder will be replaced.",
            file=output_stream,
        )
        for stale_path in replacing:
            print(f"  Replacing: {stale_path}", file=output_stream)
    else:
        print("  No previous wizard-generated prompt exists to replace yet.", file=output_stream)


def choose_preview_action(
    operation: OperationTemplate,
    values: dict[str, str],
    rendered_prompt: str,
    output_path: Path,
    replacing: list[Path],
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    include_route_prompt_authorization: bool = False,
    show_command_hints: bool = True,
) -> str:
    """Show a pre-write summary and preview, then return the selected next action."""

    print_stage("Step 3/3", "Preview and choose next action", output_stream)
    print_pre_write_summary(
        operation,
        values,
        output_path,
        replacing,
        output_stream,
        include_route_prompt_authorization=include_route_prompt_authorization,
    )
    print("Preview:", file=output_stream)
    print("=" * 72, file=output_stream)
    print(rendered_prompt.rstrip(), file=output_stream)
    print("=" * 72, file=output_stream)
    if show_command_hints:
        print("Actions: write, edit, operation, cancel, ? help.", file=output_stream)

    while True:
        answer = input_func("Choose action [write/edit/operation/cancel]: ").strip().lower()
        if not answer or answer in {"n", "no"} or answer in CANCEL_COMMANDS:
            return "cancel"
        if answer in WRITE_COMMANDS:
            if confirm_overwrite(output_path, input_func=input_func, output_stream=output_stream):
                return "write"
            print("Overwrite declined. Choose another preview action.", file=output_stream)
            continue
        if answer in EDIT_COMMANDS:
            return "edit"
        if answer in OPERATION_COMMANDS:
            return "operation"
        if answer in HELP_COMMANDS:
            print_preview_help(output_stream)
            continue
        print("Invalid action. Choose write, edit, operation, cancel, or ? help.", file=output_stream)


def confirm_overwrite(
    output_path: Path,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> bool:
    """Ask before overwriting an existing deterministic output path."""

    if not output_path.exists():
        return True
    overwrite = input_func(f"{output_path} exists. Overwrite? [y/N]: ").strip().lower()
    return overwrite in {"y", "yes"}


def confirm_write(
    operation: OperationTemplate,
    values: dict[str, str],
    rendered_prompt: str,
    output_path: Path,
    replacing: list[Path] | None = None,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    include_route_prompt_authorization: bool = False,
) -> bool:
    """Show a pre-write summary and preview, then ask before writing the generated prompt."""

    return (
        choose_preview_action(
            operation,
            values,
            rendered_prompt,
            output_path,
            replacing if replacing is not None else [],
            input_func=input_func,
            output_stream=output_stream,
            include_route_prompt_authorization=include_route_prompt_authorization,
        )
        == "write"
    )


def print_post_write_help(output_stream: TextIO) -> None:
    """Print post-write menu help without leaving the current session."""

    print("", file=output_stream)
    print("Post-write help:", file=output_stream)
    print("  new: pick another operation and start a fresh prompt.", file=output_stream)
    print(
        "  same: reuse the same operation with a fresh required-value slate "
        "(stable context such as ROADMAP_ISSUE/TARGET_REPOSITORY may carry over).",
        file=output_stream,
    )
    print("  edit: return to the current operation's values to adjust them.", file=output_stream)
    print("  path: show the current generated prompt path.", file=output_stream)
    print("  exit: end the wizard session.", file=output_stream)


def choose_post_write_action(
    current_prompt_path: Path,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> str:
    """Show session state and the post-write menu, then return the chosen action."""

    print_session_state(output_stream, current_prompt_path)
    print("Post-write actions: new, same, edit, path, exit, ? help.", file=output_stream)

    while True:
        answer = input_func("Choose action [new/same/edit/path/exit]: ").strip().lower()
        if is_cancel_command(answer):
            return "exit"
        if not answer:
            print("Choose an action, or ? for help. The session stays open until you type exit.", file=output_stream)
            continue
        if is_help_command(answer):
            print_post_write_help(output_stream)
            continue
        if answer in POST_WRITE_PATH_COMMANDS:
            print(f"Current prompt: {current_prompt_path}", file=output_stream)
            continue
        if answer in POST_WRITE_NEW_COMMANDS:
            return "new"
        if answer in POST_WRITE_SAME_COMMANDS:
            return "same"
        if answer in EDIT_COMMANDS:
            return "edit"
        print("Invalid action. Choose new, same, edit, path, exit, or ? help.", file=output_stream)




@dataclass
class LineWizardAdapter:
    """Bind the line-based terminal primitives to the shared session driver."""

    input_func: Callable[[str], str] = input
    output_stream: TextIO = sys.stdout

    def show_session(self, current_prompt_path: Path | None, selection: SurfaceSelection, output_directory: Path) -> None:
        print_session_state(self.output_stream, current_prompt_path, selection, output_directory)

    def select(self, operations: list[OperationTemplate], phase_by_operation: dict[int, str]) -> tuple[OperationTemplate | None, dict[str, str]]:
        captured_intent: dict[str, str] = {}
        operation = select_operation(operations, self.input_func, self.output_stream, phase_by_operation, captured_intent)
        return operation, captured_intent

    def collect_values(self, operation: OperationTemplate, values: dict[str, str], skill_choices: tuple[str, ...], skill_options: tuple[SkillOption, ...]) -> ValueCollectionResult:
        return collect_values_with_controls(operation, self.input_func, self.output_stream, values, skill_choices, skill_options)

    def choose_route_path(self, operation: OperationTemplate, values: dict[str, str]) -> RoutePromptPathResult:
        return collect_route_prompt_path_with_controls(operation, self.input_func, self.output_stream, values)

    def choose_preview(self, operation: OperationTemplate, values: dict[str, str], rendered_prompt: str, output_path: Path, replacing: list[Path], include_route_prompt_authorization: bool) -> str:
        return choose_preview_action(operation, values, rendered_prompt, output_path, replacing, self.input_func, self.output_stream, include_route_prompt_authorization)

    def choose_post_write(self, current_prompt_path: Path) -> str:
        return choose_post_write_action(current_prompt_path, self.input_func, self.output_stream)

    def say(self, message: str) -> None:
        print(message, file=self.output_stream)
