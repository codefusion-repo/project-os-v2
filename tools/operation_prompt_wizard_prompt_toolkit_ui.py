"""prompt_toolkit controls over the shared wizard interaction contract."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, TextIO

from tools import operation_prompt_wizard_line_ui as line_ui
from tools.operation_prompt_wizard_core import *  # noqa: F403 - this adapter consumes the full pure contract.

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import Completer, Completion, WordCompleter
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.styles import Style
    from prompt_toolkit.validation import ValidationError, Validator

    HAVE_PROMPT_TOOLKIT = True
except ImportError:
    HAVE_PROMPT_TOOLKIT = False


if HAVE_PROMPT_TOOLKIT:

    class OperationCompleter(Completer):
        def __init__(self, operations, phase_by_operation=None):
            self.operations = operations
            self.phase_by_operation = phase_by_operation or {}

        def get_completions(self, document, complete_event):
            text = document.text.lower()
            visible_operations = (
                filter_operations(self.operations, text, self.phase_by_operation)
                if text
                else canonical_operations(self.operations)
            )
            for operation in visible_operations:
                yield Completion(
                    operation.mos_code or operation.relative_path,
                    start_position=-len(document.text),
                    display=line_ui.operation_display_line(operation),
                )


    class OperationValidator(Validator):
        def __init__(self, operations):
            self.operations = operations

        def validate(self, document):
            text = document.text.strip().lower()
            if not text:
                return
            if (
                is_cancel_command(text)
                or is_search_command(text)
                or is_help_command(text)
                or is_enumerated_view_command(text)
                or is_phase_view_command(text)
            ):
                return
            if resolve_operation_selection(self.operations, text) is None:
                if intent_routing_operation(self.operations) is None:
                    raise ValidationError(
                        message=(
                            "Invalid or ambiguous selection. Use a displayed index, MOS code, "
                            "exact filename/stem/path, or cancel."
                        ),
                        cursor_position=len(document.text),
                    )


    class PromptToolkitWizardAdapter:
        """Render prompt_toolkit widgets over the shared pure decision rules."""

        def __init__(self, output_stream: TextIO):
            self.output_stream = output_stream
            self.style = Style.from_dict({"bottom-toolbar": "bg:#333333 #ffffff"})

        def _ask(
            self,
            label: str,
            *,
            completer=None,
            validator=None,
            default: str = "",
            complete_while_typing: bool | None = None,
            toolbar: str | None = None,
        ) -> str:
            return prompt(
                label,
                default=default,
                completer=completer,
                validator=validator,
                complete_while_typing=complete_while_typing,
                style=self.style,
                bottom_toolbar=(
                    (lambda: HTML(toolbar)) if toolbar is not None else None
                ),
            )

        def show_session(
            self,
            current_prompt_path: Path | None,
            selection: SurfaceSelection,
            output_directory: Path,
        ) -> None:
            line_ui.print_session_state(
                self.output_stream, current_prompt_path, selection, output_directory
            )

        def select(
            self, operations: list[OperationTemplate], phase_by_operation: dict[int, str]
        ) -> tuple[OperationTemplate | None, dict[str, str]]:
            completer = OperationCompleter(operations, phase_by_operation)
            validator = OperationValidator(operations)
            captured_intent: dict[str, str] = {}
            line_ui.print_stage(
                "Step 1/3", "Search and select an operation", self.output_stream
            )
            print(
                "Describe what you want (target, outcome, constraints) to route via "
                f"{INTENT_ROUTING_MOS_CODE}, or select explicitly by index, MOS code, "
                "filename, title, relative path, or phase.",
                file=self.output_stream,
            )
            line_ui.print_enumerated_view(operations, self.output_stream)

            while True:
                try:
                    selection = self._ask(
                        "Describe your intent, or search/select operation: ",
                        completer=completer,
                        validator=validator,
                        toolbar=(
                            " <b>Commands</b>: intent text, index/MOS/path, /enumerated "
                            "(/enumerator, /), /phases (/phase), cancel, ? help."
                        ),
                    ).strip()
                except (EOFError, KeyboardInterrupt):
                    return None, captured_intent

                if is_cancel_command(selection):
                    return None, captured_intent
                if is_help_command(selection):
                    line_ui.print_selection_help(self.output_stream)
                    continue
                if is_phase_view_command(selection):
                    line_ui.print_phase_groups(
                        operations, phase_by_operation, self.output_stream
                    )
                    continue
                if is_enumerated_view_command(selection) or is_search_command(selection):
                    line_ui.print_enumerated_view(operations, self.output_stream)
                    continue

                operation = resolve_operation_selection(operations, selection)
                if operation is not None:
                    return operation, captured_intent
                if not selection:
                    continue

                recommended = intent_routing_operation(operations)
                if recommended is not None:
                    captured_intent[PM_QUESTION_HUMANO_NAME] = selection
                    print(
                        f"No catalog match for that text. Treating it as your intent and "
                        f"routing via {recommended.mos_code} — {recommended.title}.",
                        file=self.output_stream,
                    )
                    return recommended, captured_intent

        def collect_values(
            self,
            operation: OperationTemplate,
            values: dict[str, str],
            skill_choices: tuple[str, ...],
            skill_options: tuple[SkillOption, ...],
        ) -> ValueCollectionResult:
            variables = {variable.name: variable for variable in wizard_variables(operation)}

            def ask(label: str) -> str:
                name_match = re.match(r"^([A-Z][A-Z0-9_]*) \(", label)
                name = "OPTIONAL_SKILL" if label.startswith("Select OPTIONAL_SKILL") else (
                    name_match.group(1) if name_match else None
                )
                variable = variables.get(name or "")
                if variable is None:
                    return self._ask(label)
                choices = placeholder_choices(variable.placeholder)
                completer = None
                live_completion = False
                if is_pm_authorization_status_variable(variable.name):
                    completer = WordCompleter(
                        ["1", "2", *PM_AUTHORIZATION_CHOICES], ignore_case=True
                    )
                elif variable.name == PM_DECISION_ALREADY_MADE_NAME:
                    completer = WordCompleter(
                        [*PM_DECISION_TRUE_CHOICES, *PM_DECISION_FALSE_CHOICES],
                        ignore_case=True,
                    )
                elif is_optional_skill_variable(variable.name):
                    completer = WordCompleter(list(skill_choices), ignore_case=True)
                    live_completion = True
                elif choices:
                    completer = WordCompleter(list(choices), ignore_case=True)

                class ValueValidator(Validator):
                    def validate(self, document):
                        text = document.text.strip()
                        if (
                            is_cancel_command(text)
                            or is_back_command(text)
                            or is_clear_command(text)
                            or is_help_command(text)
                            or is_hydration_override_command(text)
                        ):
                            return
                        error = validate_variable_value(
                            variable,
                            text,
                            skill_choices=skill_choices,
                            current_values=values,
                        )
                        if error is not None:
                            raise ValidationError(
                                message=error, cursor_position=len(document.text)
                            )

                label_kind = "required" if variable.required else "optional"
                commands = "back, cancel, /clear"
                if operation_produces_route_prompt(operation):
                    commands += ", /hydration"
                return self._ask(
                    label,
                    completer=completer,
                    validator=ValueValidator(),
                    default=values.get(variable.name, ""),
                    complete_while_typing=live_completion,
                    toolbar=(
                        f" <b>{variable.name}</b> ({label_kind}) | Commands: {commands}, ? help"
                    ),
                )

            return line_ui.collect_values_with_controls(
                operation,
                input_func=ask,
                output_stream=self.output_stream,
                initial_values=values,
                skill_choices=skill_choices,
                skill_options=skill_options,
                show_command_hints=False,
            )

        def choose_route_path(
            self, operation: OperationTemplate, values: dict[str, str]
        ) -> RoutePromptPathResult:
            path_choices = [
                "1", "2", "route", "route-prompt", "route_prompt", "output.route_prompt",
                "non-route", "nonroute", "status", "status_result", "pm_command_bundle",
            ]

            def ask(label: str) -> str:
                if label.startswith(PM_AUTHORIZATION_STATUS_NAME):
                    return self._ask(
                        label,
                        completer=WordCompleter(
                            ["1", "2", *PM_AUTHORIZATION_CHOICES], ignore_case=True
                        ),
                        default=values.get(PM_AUTHORIZATION_STATUS_NAME, ""),
                        toolbar=(
                            " <b>PM_AUTHORIZATION_STATUS</b> | Commands: back, cancel, ? help"
                        ),
                    )
                return self._ask(
                    label,
                    completer=WordCompleter(path_choices, ignore_case=True),
                    toolbar=(
                        " <b>Output path</b>: 1 route-prompt, 2 non-route, back, cancel, ? help"
                    ),
                )

            return line_ui.collect_route_prompt_path_with_controls(
                operation,
                input_func=ask,
                output_stream=self.output_stream,
                initial_values=values,
                show_command_hints=False,
            )

        def choose_preview(
            self,
            operation: OperationTemplate,
            values: dict[str, str],
            rendered_prompt: str,
            output_path: Path,
            replacing: list[Path],
            include_route_prompt_authorization: bool,
        ) -> str:
            def ask(label: str) -> str:
                if label.startswith("Choose action"):
                    return self._ask(
                        label,
                        completer=WordCompleter(
                            ["write", "edit", "operation", "cancel", "help", "?"],
                            ignore_case=True,
                        ),
                        toolbar=" <b>Actions</b>: write, edit, operation, cancel, ? help",
                    )
                return self._ask(label)

            return line_ui.choose_preview_action(
                operation,
                values,
                rendered_prompt,
                output_path,
                replacing,
                input_func=ask,
                output_stream=self.output_stream,
                include_route_prompt_authorization=include_route_prompt_authorization,
                show_command_hints=False,
            )

        def choose_post_write(self, current_prompt_path: Path) -> str:
            return line_ui.choose_post_write_action(
                current_prompt_path,
                input_func=lambda label: self._ask(
                    label,
                    completer=WordCompleter(
                        ["new", "same", "edit", "path", "exit", "help", "?"],
                        ignore_case=True,
                    ),
                    toolbar=" <b>Post-write</b>: new, same, edit, path, exit, ? help",
                ),
                output_stream=self.output_stream,
            )

        def say(self, message: str) -> None:
            print(message, file=self.output_stream)


    def ask_language_pt(question: str) -> str:
        try:
            return prompt(question, completer=WordCompleter(list(LANGUAGE_CHOICES), ignore_case=True))
        except (EOFError, KeyboardInterrupt):
            return "cancel"
