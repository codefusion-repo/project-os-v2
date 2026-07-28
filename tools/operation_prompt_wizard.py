"""Local entrypoint and compatibility surface for the operation prompt wizard.

The entrypoint composes a pure shared core, one of two terminal adapters, and a
small generated-artifact filesystem boundary. It never executes operations or
uses network services.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, TextIO

# Keep the documented ``python tools/operation_prompt_wizard.py`` invocation
# working as well as package execution via ``python -m``.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import operation_prompt_wizard_core as _core
from tools import operation_prompt_wizard_prompt_toolkit_ui as _prompt_toolkit_ui
from tools.operation_prompt_wizard_catalog import (
    DEFAULT_OPERATION_FLOWS_PATH,
    DEFAULT_OPERATIONS_DIR,
    DEFAULT_SKILLS_CATALOG,
    REPO_ROOT,
    discover_operations,
    display_path,
    load_active_skill_choices,
    load_active_skill_options,
    load_phase_map,
    resolve_surface_selection,
    skill_choice_keys,
    surface_selection_for_language,
    surface_selection_for_surface,
)
from tools.operation_prompt_wizard_core import *  # noqa: F403 - stable compatibility re-exports.
from tools.operation_prompt_wizard_filesystem import (
    DEFAULT_OUTPUT_DIR,
    OUTPUT_DIR_ENV,
    cleanup_previous_generated_prompts,
    find_existing_generated_prompts,
    find_replaceable_prompts,
    is_wizard_generated_artifact,
    resolve_output_dir,
    write_prompt,
)
from tools.operation_prompt_wizard_line_ui import *  # noqa: F403 - stable line-UI compatibility re-exports.
from tools.operation_prompt_wizard_line_ui import LineWizardAdapter
from tools.operation_prompt_wizard_session import run_wizard_session

HAVE_PROMPT_TOOLKIT = _prompt_toolkit_ui.HAVE_PROMPT_TOOLKIT
if HAVE_PROMPT_TOOLKIT:
    prompt = _prompt_toolkit_ui.prompt
    OperationCompleter = _prompt_toolkit_ui.OperationCompleter
    OperationValidator = _prompt_toolkit_ui.OperationValidator
    PromptToolkitWizardAdapter = _prompt_toolkit_ui.PromptToolkitWizardAdapter


def validate_variable_value(
    variable: InputVariable,
    value: str,
    skill_choices: tuple[str, ...] | None = None,
    current_values: dict[str, str] | None = None,
) -> str | None:
    """Supply catalog choices only at the public compatibility boundary."""

    if skill_choices is None and is_optional_skill_variable(variable.name):
        skill_choices = load_active_skill_choices()
    return _core.validate_variable_value(variable, value, skill_choices, current_values)


def validation_example(
    variable: InputVariable,
    skill_choices: tuple[str, ...] | None = None,
) -> str:
    """Supply catalog choices only for the public optional-skill example."""

    if skill_choices is None and is_optional_skill_variable(variable.name):
        skill_choices = load_active_skill_choices()
    return _core.validation_example(variable, skill_choices)


def _run_with_adapter(
    adapter: object,
    *,
    selection: SurfaceSelection,
    output_dir: Path | None,
    operation_flows_path: Path | None,
) -> Path | None:
    operations = discover_operations(selection.operations_dir)
    output_directory = resolve_output_dir(output_dir)
    phase_by_operation = load_phase_map(operation_flows_path, operations)
    skill_options = load_active_skill_options(selection.skills_catalog_path)
    return run_wizard_session(
        adapter,
        selection=selection,
        operations=operations,
        output_directory=output_directory,
        phase_by_operation=phase_by_operation,
        skill_choices=skill_choice_keys(skill_options),
        skill_options=skill_options,
    )


def run_wizard(
    operations_dir: Path | None = None,
    output_dir: Path | None = None,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    operation_flows_path: Path | None = DEFAULT_OPERATION_FLOWS_PATH,
    skills_catalog_path: Path | None = None,
    language: str | None = None,
) -> Path | None:
    """Run the line-based adapter through the shared wizard session contract."""

    adapter = LineWizardAdapter(input_func=input_func, output_stream=output_stream)
    selection = resolve_surface_selection(
        language=language,
        operations_dir=operations_dir,
        skills_catalog_path=skills_catalog_path,
        input_func=input_func,
        output_stream=output_stream,
    )
    if selection is None:
        adapter.say("Cancelled before language selection. No file was created.")
        return None
    return _run_with_adapter(
        adapter,
        selection=selection,
        output_dir=output_dir,
        operation_flows_path=operation_flows_path,
    )


def run_wizard_pt(
    operations_dir: Path | None = None,
    output_dir: Path | None = None,
    output_stream: TextIO = sys.stdout,
    operation_flows_path: Path | None = DEFAULT_OPERATION_FLOWS_PATH,
    skills_catalog_path: Path | None = None,
    language: str | None = None,
) -> Path | None:
    """Run the prompt_toolkit adapter through the same shared session contract."""

    if not HAVE_PROMPT_TOOLKIT:
        raise WizardError("prompt_toolkit is unavailable; use the line-based wizard")
    _prompt_toolkit_ui.prompt = prompt
    adapter = PromptToolkitWizardAdapter(output_stream)
    selection = resolve_surface_selection(
        language=language,
        operations_dir=operations_dir,
        skills_catalog_path=skills_catalog_path,
        input_func=_prompt_toolkit_ui.ask_language_pt,
        output_stream=output_stream,
    )
    if selection is None:
        adapter.say("Cancelled before language selection. No file was created.")
        return None
    return _run_with_adapter(
        adapter,
        selection=selection,
        output_dir=output_dir,
        operation_flows_path=operation_flows_path,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--language",
        choices=LANGUAGE_CHOICES,
        default=None,
        help=(
            "Session-only surface selection: es loads project-os-es/operaciones with "
            "Spanish skills and en loads project-os-en/operations with English skills. "
            "Without it and without --operations-dir, the wizard asks once at session "
            "start and Enter keeps the Spanish default. The selection lives only in "
            "this session and never adopts, installs, or configures a target."
        ),
    )
    parser.add_argument(
        "--operations-dir",
        type=Path,
        default=None,
        help=(
            "Advanced: explicit operation catalog directory; Markdown files are "
            "discovered recursively. A directory matching a known es/en surface "
            "derives that same surface's skills catalog; any other directory is a "
            "custom catalog that keeps the default Spanish skills catalog and is not "
            "labeled es or en. Combined with a mismatched --language it fails closed "
            "instead of mixing surfaces. Without it, the session language selection "
            "decides the catalog."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Directory for generated .md prompts. Defaults to "
            f"${OUTPUT_DIR_ENV} or {DEFAULT_OUTPUT_DIR}."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = (
            run_wizard_pt(
                operations_dir=args.operations_dir,
                output_dir=args.output_dir,
                language=args.language,
            )
            if HAVE_PROMPT_TOOLKIT
            else run_wizard(
                operations_dir=args.operations_dir,
                output_dir=args.output_dir,
                language=args.language,
            )
        )
    except WizardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.", file=sys.stderr)
        return 1
    return 0 if result is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
