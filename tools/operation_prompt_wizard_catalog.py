"""Filesystem-backed catalog adapter for the operation prompt wizard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, TextIO
import sys

try:
    from tools.operation_catalog import load_operation_sources, validate_operation_catalog
    from tools.project_os_surfaces import ProjectOSSurface, surface_for_language, surface_for_operations_dir
    from tools.operation_prompt_wizard_core import (
        CUSTOM_SURFACE_LANGUAGE,
        DEFAULT_LANGUAGE,
        LANGUAGE_CHOICES,
        LANGUAGE_QUESTION,
        OperationTemplate,
        PHASE_TABLE_HEADER_PREFIX,
        SkillOption,
        SurfaceSelection,
        WizardError,
        canonical_operations,
        extract_description,
        extract_title,
        is_cancel_command,
        parse_input_variables,
    )
except ModuleNotFoundError:  # Direct execution from tools/.
    from operation_catalog import load_operation_sources, validate_operation_catalog  # type: ignore[no-redef]
    from project_os_surfaces import ProjectOSSurface, surface_for_language, surface_for_operations_dir  # type: ignore[no-redef]
    from operation_prompt_wizard_core import (  # type: ignore[no-redef]
        CUSTOM_SURFACE_LANGUAGE, DEFAULT_LANGUAGE, LANGUAGE_CHOICES, LANGUAGE_QUESTION,
        OperationTemplate, PHASE_TABLE_HEADER_PREFIX, SkillOption, SurfaceSelection, WizardError, canonical_operations,
        extract_description, extract_title, is_cancel_command, parse_input_variables,
    )

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OPERATIONS_DIR = REPO_ROOT / "project-os-es" / "operaciones"
DEFAULT_SKILLS_CATALOG = REPO_ROOT / "project-os-es" / "kernel" / "skills.json"
DEFAULT_OPERATION_FLOWS_PATH: Path | None = None

def surface_selection_for_surface(surface: ProjectOSSurface) -> SurfaceSelection:
    """Bundle one allowed surface's operations, skills, and reference kernel."""

    return SurfaceSelection(
        language=surface.language,
        operations_dir=surface.operations_dir,
        skills_catalog_path=surface.skills_catalog_path,
        kernel_dir=surface.kernel_dir,
    )


def surface_selection_for_language(language: str) -> SurfaceSelection:
    """Resolve one full surface bundle for an explicit language, failing closed."""

    surface = surface_for_language(language)
    if surface is None:
        raise WizardError(
            f"unknown wizard language {language!r}; choose one of: {', '.join(LANGUAGE_CHOICES)}"
        )
    return surface_selection_for_surface(surface)


def resolve_surface_selection(
    language: str | None = None,
    operations_dir: Path | None = None,
    skills_catalog_path: Path | None = None,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> SurfaceSelection | None:
    """Resolve the session surface bundle once, before any catalog is read.

    Precedence: an explicit ``language`` and an explicit ``operations_dir``
    must name the same surface (no silent mixing); an ``operations_dir`` that
    exactly matches a known surface derives that surface's skills catalog; any
    other ``operations_dir`` stays a custom catalog that keeps the existing
    programmatic ``skills_catalog_path`` API and is not labeled es or en; with
    neither, one interactive question selects the surface (Enter keeps
    Spanish). An explicit ``skills_catalog_path`` only replaces the catalog of
    a custom ``operations_dir``; on a known es/en surface it must point to that
    surface's canonical catalog or the resolution fails closed (no mixing).
    Returns ``None`` when the interactive question is cancelled.
    """

    if language is not None:
        language = language.strip().lower()
        if language not in LANGUAGE_CHOICES:
            raise WizardError(
                f"unknown wizard language {language!r}; choose one of: {', '.join(LANGUAGE_CHOICES)}"
            )

    if operations_dir is not None:
        surface = surface_for_operations_dir(operations_dir)
        if language is not None:
            if surface is None or surface.language != language:
                raise WizardError(
                    f"--language {language} is incompatible with --operations-dir "
                    f"{operations_dir}; the wizard never mixes operations and skills "
                    "from different surfaces. Drop one option or make them match."
                )
            selection = surface_selection_for_surface(surface)
        elif surface is not None:
            selection = surface_selection_for_surface(surface)
        else:
            selection = SurfaceSelection(
                language=CUSTOM_SURFACE_LANGUAGE,
                operations_dir=Path(operations_dir).expanduser(),
                skills_catalog_path=DEFAULT_SKILLS_CATALOG,
                kernel_dir=None,
            )
    elif language is not None:
        selection = surface_selection_for_language(language)
    else:
        selection = None
        while selection is None:
            answer = input_func(LANGUAGE_QUESTION).strip().lower()
            if is_cancel_command(answer):
                return None
            if not answer:
                answer = DEFAULT_LANGUAGE
            if answer in LANGUAGE_CHOICES:
                selection = surface_selection_for_language(answer)
                break
            print(
                f"Unknown language {answer!r}. Use es, en, or Enter for the Spanish default.",
                file=output_stream,
            )

    if skills_catalog_path is not None:
        if selection.language == CUSTOM_SURFACE_LANGUAGE:
            selection = SurfaceSelection(
                language=selection.language,
                operations_dir=selection.operations_dir,
                skills_catalog_path=skills_catalog_path,
                kernel_dir=selection.kernel_dir,
            )
        else:
            supplied = Path(skills_catalog_path).expanduser()
            supplied_abs = supplied if supplied.is_absolute() else Path.cwd() / supplied
            canonical = selection.skills_catalog_path
            if supplied_abs != canonical and supplied_abs.resolve() != canonical:
                raise WizardError(
                    f"skills catalog {skills_catalog_path} does not belong to the "
                    f"{selection.language} surface; the wizard never mixes operations "
                    "and skills from different surfaces. Drop the override or use "
                    f"{display_path(canonical)}."
                )
    return selection


def display_path(path: Path) -> str:
    """Show repository paths relative to the repo root and others as given."""

    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def discover_operations(operations_dir: Path = DEFAULT_OPERATIONS_DIR) -> list[OperationTemplate]:
    """Discover canonical operations plus explicit historical alias selectors."""

    operations_dir = operations_dir.expanduser()
    if not operations_dir.is_dir():
        raise WizardError(f"operations directory not found: {operations_dir}")

    try:
        sources = load_operation_sources(operations_dir)
    except (OSError, ValueError) as exc:
        raise WizardError(str(exc)) from exc
    findings = validate_operation_catalog(sources)
    if findings:
        raise WizardError("operation catalog validation failed:\n" + "\n".join(item.render() for item in findings))

    source_by_code = {source.code: source for source in sources}
    index_by_code: dict[str, int] = {}
    operations: list[OperationTemplate] = []
    for source in (item for item in sources if not item.is_alias):
        index = len(index_by_code) + 1
        index_by_code[source.code] = index
        operations.append(
            OperationTemplate(
                index=index,
                path=source.path,
                title=extract_title(source.text, source.path),
                description=extract_description(source.text, source.path),
                text=source.text,
                variables=parse_input_variables(source.text),
                catalog_root=operations_dir,
                canonical_code=source.code,
                canonical_path=source.path,
                aliases=source.metadata.aliases,
                deprecation=source.metadata.deprecation,
                compatibility_reason=source.metadata.compatibility_reason,
                alias_focus_area=source.metadata.alias_focus_area,
            )
        )
    for source in (item for item in sources if item.is_alias):
        canonical = source_by_code[source.metadata.alias_of or ""]
        operations.append(
            OperationTemplate(
                index=index_by_code[canonical.code],
                path=source.path,
                title=extract_title(source.text, source.path),
                description=extract_description(canonical.text, canonical.path),
                text=canonical.text,
                variables=parse_input_variables(canonical.text),
                catalog_root=operations_dir,
                canonical_code=canonical.code,
                canonical_path=canonical.path,
                alias_of=canonical.code,
                deprecation=source.metadata.deprecation,
                compatibility_reason=source.metadata.compatibility_reason,
                alias_focus_area=source.metadata.alias_focus_area,
            )
        )
    return operations

def load_active_skill_options(skills_catalog_path: Path = DEFAULT_SKILLS_CATALOG) -> tuple[SkillOption, ...]:
    """Load active skill keys and display names from the canonical catalog.

    The catalog is authoritative. Invalid or unreadable catalog data stops the
    wizard rather than falling back to stale hard-coded values or labels.
    """

    try:
        content = json.loads(skills_catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WizardError(f"cannot read active skills catalog {skills_catalog_path}: {exc}") from exc
    if not isinstance(content, dict) or not isinstance(content.get("skills"), list):
        raise WizardError(f"invalid active skills catalog {skills_catalog_path}: expected object with skills list")

    options: list[SkillOption] = []
    for index, entry in enumerate(content["skills"]):
        if not isinstance(entry, dict):
            raise WizardError(f"invalid active skills catalog {skills_catalog_path}: skills[{index}] is not an object")
        key = entry.get("key")
        # The Spanish catalog names skills with "nombre" and the English one
        # with "name"; both surfaces stay catalog-owned and authoritative.
        name = entry.get("nombre") if isinstance(entry.get("nombre"), str) else entry.get("name")
        active = entry.get("active")
        if (
            not isinstance(key, str)
            or not key.startswith("skill.")
            or not isinstance(name, str)
            or not name.strip()
            or not isinstance(active, bool)
        ):
            raise WizardError(
                f"invalid active skills catalog {skills_catalog_path}: skills[{index}] needs "
                "key skill.*, non-empty nombre or name, and boolean active"
            )
        if active:
            if key in {option.key for option in options}:
                raise WizardError(f"invalid active skills catalog {skills_catalog_path}: duplicate active skill {key}")
            options.append(SkillOption(key=key, name=name.strip()))
    if "none" in {option.key for option in options}:
        raise WizardError(f"invalid active skills catalog {skills_catalog_path}: active skill key none is reserved")
    return tuple(options)


def skill_choice_keys(skill_options: tuple[SkillOption, ...]) -> tuple[str, ...]:
    """Return accepted stored values for active options plus explicit ``none``."""

    return tuple((*[option.key for option in skill_options], "none"))


def load_active_skill_choices(skills_catalog_path: Path = DEFAULT_SKILLS_CATALOG) -> tuple[str, ...]:
    """Load accepted OPTIONAL_SKILL values from the canonical catalog."""

    return skill_choice_keys(load_active_skill_options(skills_catalog_path))


def load_phase_map(
    flows_path: Path | None = DEFAULT_OPERATION_FLOWS_PATH,
    operations: list[OperationTemplate] | None = None,
) -> dict[int, str]:
    """Derive phases from the active catalog, with an optional table override.

    Directory-derived labels keep ``/phases`` useful for the canonical Spanish
    tree without consulting historical flow documentation.
    """

    phase_by_operation = {
        operation.index: operation.phase_label
        for operation in canonical_operations(operations or [])
        if operation.phase_label
    }
    if flows_path is not None:
        flows_path = flows_path.expanduser()
        if flows_path.is_file():
            in_table = False
            for line in flows_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not in_table:
                    if stripped.startswith(PHASE_TABLE_HEADER_PREFIX):
                        in_table = True
                    continue
                if not stripped.startswith("|"):
                    break
                cells = [cell.strip() for cell in stripped.strip("|").split("|")]
                if len(cells) < 2:
                    continue
                op_number_text, phase = cells[0], cells[1]
                if op_number_text.isdigit() and phase:
                    phase_by_operation[int(op_number_text)] = phase
    return phase_by_operation
