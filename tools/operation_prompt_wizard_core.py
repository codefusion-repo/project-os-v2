"""Pure business rules and state contracts for the operation prompt wizard.

This module deliberately has no terminal, prompt_toolkit, environment, or filesystem
operations. Catalog loading, interaction, and generated-artifact effects belong to
separate adapters.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Literal

LANGUAGE_CHOICES = ("es", "en")
DEFAULT_LANGUAGE = "es"
CUSTOM_SURFACE_LANGUAGE = "custom"
LANGUAGE_QUESTION = "Elige idioma / Choose language [es/en] (default: es): "
# The active Spanish catalog encodes its phase model in directory names.  An
# optional table can still override those labels for custom catalogs.
BLOCK_HEADER_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*:\s*$")
INPUT_VARIABLE_PATTERN = re.compile(
    r"^\s*(?P<name>[A-Z][A-Z0-9_]*)\s*=\s*(?P<placeholder><[^>\n]+>)?(?P<tail>.*)$"
)
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
POSITIVE_NUMBER_PATTERN = re.compile(r"^#?[1-9][0-9]*$")
AUDIT_SCOPE_PATTERN = re.compile(
    r"(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+|(?:issue|pr)\s+#?[1-9][0-9]*)$",
    re.IGNORECASE,
)
SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")
SECRET_LOOKING_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{12,})\b"
)

# Wizard-generated prompt artifacts are named "<stem>-<12 hex chars>.md" by
# generated_filename() and carry WIZARD_PROMPT_MARKER inside the file. Both
# signals must match before cleanup will ever remove a file, so arbitrary or
# hand-authored .md files are never touched.
WIZARD_PROMPT_MARKER = "<!-- project-os-operation-prompt-wizard: generated prompt artifact -->"
GENERATED_FILENAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?-[0-9a-f]{12}\.md$")

PHASE_TABLE_HEADER_PREFIX = "| Op | Phase"
MOS_CODE_PATTERN = re.compile(r"^(MOS-(?:\d+\.\d+|R\.\d+))(?=-|$)", re.IGNORECASE)

CANCEL_COMMANDS = {"c", "cancel", "q", "quit", "exit"}
HELP_COMMANDS = {"?", "h", "help"}
BACK_COMMANDS = {"b", "back"}
SEARCH_COMMANDS = {"s", "search", "again"}
WRITE_COMMANDS = {"w", "write", "y", "yes"}
EDIT_COMMANDS = {"e", "edit", "variables"}
OPERATION_COMMANDS = {"o", "operation", "operations", "choose"}
CLEAR_COMMANDS = {"/clear"}
# Slash-prefixed so a plain-text search for "phase" (e.g. operation 37's
# filename contains "phase") still filters normally instead of being
# swallowed as a grouping command.
PHASE_LIST_COMMANDS = {"/phase", "/phases"}
ENUMERATED_LIST_COMMANDS = {"/", "/enumerated", "/enumerator"}

POST_WRITE_NEW_COMMANDS = {"n", "new"}
POST_WRITE_SAME_COMMANDS = {"r", "reuse", "same"}
POST_WRITE_PATH_COMMANDS = {"p", "path", "current"}

PM_AUTHORIZATION_STATUS_NAME = "PM_AUTHORIZATION_STATUS"
PM_AUTHORIZATION_PENDING = "pending"
PM_AUTHORIZATION_GRANTED = "granted for this exact scope and mode"
PM_AUTHORIZATION_CHOICES = (PM_AUTHORIZATION_PENDING, PM_AUTHORIZATION_GRANTED)
PM_DECISION_ALREADY_MADE_NAME = "PM_DECISION_ALREADY_MADE"
PM_DECISION_NAME = "PM_DECISION"
PM_DECISION_TRUE_CHOICES = ("true", "1", "yes", "y", "si", "sí")
PM_DECISION_FALSE_CHOICES = ("false", "0", "no", "n")
# CHANGE_CLASS is derived metadata: browser chat reconstructs it from the unit's
# live evidence and renders it already resolved in the route prompt, so it is
# never captured as an input. HYDRATION_LEVEL is not derived from that class at
# all: the resolver defaults every class to compact, so the route prompt may omit
# it entirely. It keeps one PM-facing escape hatch: the opt-in /hydration command
# below records an explicit override the PM typed on purpose, which may select
# any of the three levels and never changes gates, report density, or authority.
HYDRATION_LEVEL_NAME = "HYDRATION_LEVEL"
HYDRATION_LEVEL_CHOICES = ("minimal", "compact", "full/debug")
HYDRATION_OVERRIDE_COMMANDS = {"/hydration", "/hydration-level"}

# Intent-first entry (OSIM.4): free text that names no catalog operation is
# PM intent, not a failed search. The wizard never decides which operation
# applies; it only transports the intent, verbatim, into MOS-R.2's own
# PM_QUESTION_HUMANO variable so the canonical routing capability resolves it
# from live evidence. Explicit selection (index, MOS code, filename, stem,
# path) always takes precedence and is checked first.
INTENT_ROUTING_MOS_CODE = "MOS-R.2"
PM_QUESTION_HUMANO_NAME = "PM_QUESTION_HUMANO"


def is_cancel_command(value: str) -> bool:
    return value.strip().lower() in CANCEL_COMMANDS


def is_help_command(value: str) -> bool:
    return value.strip().lower() in HELP_COMMANDS


def is_back_command(value: str) -> bool:
    return value.strip().lower() in BACK_COMMANDS


def is_search_command(value: str) -> bool:
    return value.strip().lower() in SEARCH_COMMANDS


def is_clear_command(value: str) -> bool:
    return value.strip().lower() in CLEAR_COMMANDS


def is_hydration_override_command(value: str) -> bool:
    return value.strip().split(maxsplit=1)[0].lower() in HYDRATION_OVERRIDE_COMMANDS if value.strip() else False


def parse_hydration_override(value: str) -> tuple[str | None, str | None]:
    """Parse the explicit hydration override without changing session state."""

    parts = value.strip().split(maxsplit=1)
    argument = parts[1].strip().lower() if len(parts) > 1 else ""
    if not argument:
        return "", None
    if argument not in HYDRATION_LEVEL_CHOICES:
        return None, (
            f"{HYDRATION_LEVEL_NAME} override must be one of: "
            f"{', '.join(HYDRATION_LEVEL_CHOICES)}; any of the three is allowed "
            "for any class, and none of them changes gates or authority."
        )
    return argument, None


def is_enumerated_view_command(value: str) -> bool:
    return value.strip().lower() in ENUMERATED_LIST_COMMANDS


def is_phase_view_command(value: str) -> bool:
    return value.strip().lower() in PHASE_LIST_COMMANDS


class WizardError(RuntimeError):
    """Raised when the local wizard cannot proceed safely."""


@dataclass(frozen=True)
class InputVariable:
    """A variable declared in an operation template ``INPUT:`` block."""

    name: str
    placeholder: str
    required: bool
    raw_line: str
    note: str = ""


@dataclass(frozen=True)
class SkillOption:
    """One active skill value and its catalog-owned display name."""

    key: str
    name: str


@dataclass(frozen=True)
class OperationTemplate:
    """A discovered operation template and parsed metadata."""

    index: int
    path: Path
    title: str
    description: str
    text: str
    variables: tuple[InputVariable, ...]
    catalog_root: Path | None = None
    canonical_code: str | None = None
    canonical_path: Path | None = None
    aliases: tuple[str, ...] = ()
    alias_of: str | None = None
    deprecation: str = "none"
    compatibility_reason: str = ""
    alias_focus_area: str = ""

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def mos_code(self) -> str | None:
        match = MOS_CODE_PATTERN.match(self.path.stem)
        return match.group(1).upper() if match else None

    @property
    def is_alias(self) -> bool:
        return self.alias_of is not None

    @property
    def resolved_canonical_code(self) -> str | None:
        return self.canonical_code or self.mos_code

    @property
    def relative_path(self) -> str:
        if self.catalog_root is not None:
            try:
                return self.path.relative_to(self.catalog_root).as_posix()
            except ValueError:
                pass
        return self.path.name

    @property
    def phase_path(self) -> str:
        parent = Path(self.relative_path).parent.as_posix()
        return "" if parent == "." else parent

    @property
    def phase_label(self) -> str:
        if not self.phase_path:
            return ""
        labels = []
        for part in self.phase_path.split("/"):
            if part in {"cross-fase", "cross-phase"}:
                labels.append("Cross-phase" if part == "cross-phase" else "Cross-fase")
            elif match := re.fullmatch(r"fase-(\d+)", part):
                labels.append(f"Fase {match.group(1)}")
            elif match := re.fullmatch(r"phase-(\d+)", part):
                labels.append(f"Phase {match.group(1)}")
            else:
                labels.append(part.replace("-", " ").title())
        return " / ".join(labels)

@dataclass(frozen=True)
class ValueCollectionResult:
    """Result of variable entry, including navigation requests."""

    action: str
    values: dict[str, str]


@dataclass(frozen=True)
class RoutePromptPathResult:
    """Result of multi-output route-prompt path selection."""

    action: str
    values: dict[str, str]
    include_pm_authorization_status: bool


@dataclass(frozen=True)
class SurfaceSelection:
    """One coherent session-only catalog bundle; never target adoption or permission.

    ``language`` is ``es``, ``en``, or ``custom`` for an explicit non-surface
    operations directory. ``kernel_dir`` is shown as local orientation only.
    """

    language: str
    operations_dir: Path
    skills_catalog_path: Path
    kernel_dir: Path | None


def canonical_operations(operations: list[OperationTemplate]) -> list[OperationTemplate]:
    """Return the normal catalog view, with aliases represented only on canonicals."""

    return [operation for operation in operations if not operation.is_alias]


def canonical_operation_for(
    operations: list[OperationTemplate], operation: OperationTemplate
) -> OperationTemplate:
    if not operation.is_alias:
        return operation
    return next(
        candidate
        for candidate in operations
        if not candidate.is_alias and candidate.mos_code == operation.resolved_canonical_code
    )


def alias_bound_values(operation: OperationTemplate) -> dict[str, str]:
    """Return the maintenance focus bound by one historical alias, if any."""

    return {"FOCUS_AREA": operation.alias_focus_area} if operation.alias_focus_area else {}


def extract_title(text: str, path: Path) -> str:
    """Return the first Markdown heading, falling back to the filename stem."""

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title
    return path.stem


def extract_description(text: str, path: Path) -> str:
    """Return concise catalog metadata for presentation, with a safe fallback."""

    match = re.search(r"^\*\*(?:Hace|Does):\*\*\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if match:
        return match.group(1)

    title = extract_title(text, path)
    return re.sub(r"^MOS-(?:\d+\.\d+|R\.\d+)\s*[—-]\s*", "", title, flags=re.IGNORECASE)


def parse_input_variables(text: str) -> tuple[InputVariable, ...]:
    """Parse variables from conventional INPUT or either compact catalog."""

    variables: list[InputVariable] = []
    for raw_line in input_block_lines(text):
        stripped = raw_line.strip()
        if not stripped or stripped == "(none)":
            continue

        match = INPUT_VARIABLE_PATTERN.match(raw_line)
        if not match:
            continue

        name = match.group("name")
        placeholder = match.group("placeholder") or f"<{name}>"
        tail = match.group("tail").strip()
        required = "optional" not in tail.lower()
        variables.append(
            InputVariable(
                name=name,
                placeholder=placeholder,
                required=required,
                raw_line=raw_line.rstrip(),
                note=tail,
            )
        )
    if variables:
        return tuple(variables)

    variables.extend(parse_compact_variables(text))
    return tuple(variables)


def parse_compact_variables(text: str) -> tuple[InputVariable, ...]:
    """Parse ``**Variables**`` from the compact Spanish or English catalog."""

    marker = "**Variables**"
    if marker not in text:
        return ()
    section = text.split(marker, 1)[1]
    section = re.split(r"\n\s*\n(?=\*\*)", section, maxsplit=1)[0]
    parsed: list[InputVariable] = []
    for labels, required in ((("Requeridas", "Required"), True), (("Opcionales", "Optional"), False)):
        label_pattern = "|".join(labels)
        match = re.search(
            rf"^-\s*(?:{label_pattern}):\s*(.*?)(?=^-\s*(?:Requeridas|Opcionales|Required|Optional):|\Z)",
            section,
            flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if not match:
            continue
        declaration = match.group(1).split("(", 1)[0]
        for name in re.findall(r"\b[A-Z][A-Z0-9_]+\b", declaration):
            if name in {variable.name for variable in parsed}:
                continue
            parsed.append(
                InputVariable(
                    name=name,
                    placeholder=f"<{name}>",
                    required=required,
                    raw_line="",
                    note=f"{labels[0].lower()} in the compact catalog",
                )
            )
    return tuple(parsed)


def input_block_lines(text: str) -> list[str]:
    """Return the raw lines inside the first ``INPUT:`` block."""

    return named_block_lines(text, "INPUT")


def named_block_lines(text: str, block_name: str) -> list[str]:
    """Return raw lines inside the first named all-caps operation block."""

    lines = text.splitlines()
    in_block = False
    block: list[str] = []
    header = f"{block_name}:"
    for line in lines:
        stripped = line.strip()
        if not in_block:
            if stripped == header:
                in_block = True
            continue
        if BLOCK_HEADER_PATTERN.match(stripped):
            break
        block.append(line)
    return block


def filter_operations(
    operations: list[OperationTemplate],
    query: str,
    phase_by_operation: dict[int, str] | None = None,
) -> list[OperationTemplate]:
    """Filter by active Spanish identity, relative context, or displayed index."""

    normalized = query.strip().lower()
    if not normalized:
        return list(operations)

    matches: list[OperationTemplate] = []
    for operation in operations:
        if normalized.isdigit():
            if operation.index == int(normalized):
                matches.append(operation)
            continue
        searchable = {
            operation.filename.lower(),
            operation.path.stem.lower(),
            operation.title.lower(),
            operation.description.lower(),
            operation.relative_path.lower(),
            operation.phase_path.lower(),
            operation.phase_label.lower(),
            (operation.mos_code or "").lower(),
        }
        phase = _operation_phase(operation, phase_by_operation or {})
        if phase:
            searchable.add(phase.lower())
        if any(normalized in value for value in searchable if value):
            matches.append(operation)
    canonical_matches: dict[Path, OperationTemplate] = {}
    for operation in matches:
        canonical = canonical_operation_for(operations, operation)
        canonical_matches[canonical.path] = canonical
    return list(canonical_matches.values())


def resolve_operation_selection(
    operations: list[OperationTemplate], selection: str
) -> OperationTemplate | None:
    """Resolve one exact active operation and fail safely on duplicate matches."""

    normalized = selection.strip().lower()
    if not normalized:
        return None

    explicit_index = re.fullmatch(r"(?:index|indice|índice):?(\d+)", normalized)
    if explicit_index:
        return _unique_operation(
            op for op in operations if not op.is_alias and op.index == int(explicit_index.group(1))
        )

    if normalized.isdigit():
        index_match = _unique_operation(
            op for op in operations if not op.is_alias and op.index == int(normalized)
        )
        return index_match

    return _unique_operation(
        operation
        for operation in operations
        if normalized in {
            operation.filename.lower(),
            operation.path.stem.lower(),
            operation.relative_path.lower(),
            (operation.mos_code or "").lower(),
        }
    )


def _unique_operation(candidates) -> OperationTemplate | None:
    unique = {operation.path: operation for operation in candidates}
    return next(iter(unique.values())) if len(unique) == 1 else None


def intent_routing_operation(operations: list[OperationTemplate]) -> OperationTemplate | None:
    """Return the active MOS-R.2 operation in this catalog, or None if absent."""

    return _unique_operation(
        operation
        for operation in operations
        if not operation.is_alias and operation.mos_code == INTENT_ROUTING_MOS_CODE
    )


def validate_variable_value(
    variable: InputVariable,
    value: str,
    skill_choices: tuple[str, ...] | None = None,
    current_values: dict[str, str] | None = None,
) -> str | None:
    """Return a validation error for common variable shapes, or ``None``."""

    stripped = value.strip()
    if variable.required and not stripped:
        return f"{variable.name} is required. {validation_example(variable)}"
    if variable.name == PM_DECISION_NAME and current_values is not None:
        decision_made = normalize_pm_decision_already_made(
            current_values.get(PM_DECISION_ALREADY_MADE_NAME, "")
        )
        if decision_made == "true" and not stripped:
            return f"{PM_DECISION_NAME} is required when {PM_DECISION_ALREADY_MADE_NAME}=true."
        if decision_made == "false" and stripped:
            return f"{PM_DECISION_NAME} must be empty when {PM_DECISION_ALREADY_MADE_NAME}=false."
    if not stripped:
        return None
    if SECRET_LOOKING_PATTERN.search(stripped):
        return f"{variable.name} looks like a secret and cannot be written to a prompt artifact."

    if is_pm_authorization_status_variable(variable.name):
        if normalize_pm_authorization_status(stripped) is None:
            return (
                f"{variable.name} must be 1, 2, pending, or "
                "granted for this exact scope and mode."
            )
        return None

    if variable.name == PM_DECISION_ALREADY_MADE_NAME:
        if normalize_pm_decision_already_made(stripped) is None:
            return (
                f"{PM_DECISION_ALREADY_MADE_NAME} must be true or false "
                "(local helpers: yes/no, si/sí/no, or 1/0)."
            )
        return None

    if is_optional_skill_variable(variable.name):
        choices = skill_choices or ()
        if stripped not in choices:
            return (
                f"{variable.name} must be an active skill or none: "
                f"{', '.join(choices)}."
            )
        return None

    choices = placeholder_choices(variable.placeholder)
    if choices is not None and stripped not in choices:
        return (
            f"{variable.name} must be one of the allowed placeholder choices: "
            f"{', '.join(choices)}. Example: {choices[0]}."
        )

    if is_issue_or_pr_number(variable.name) and not POSITIVE_NUMBER_PATTERN.fullmatch(stripped):
        return f"{variable.name} must be a positive issue/PR number. Examples: 123 or #123."

    if variable.name == "AUDIT_SCOPE" and not AUDIT_SCOPE_PATTERN.fullmatch(stripped):
        return (
            "AUDIT_SCOPE must be owner/repo, issue #N, or PR #N. "
            "Examples: codefusion-repo/project-os-v2, issue #465, or PR #467."
        )

    if is_repository_variable(variable.name) and not REPOSITORY_PATTERN.fullmatch(stripped):
        return f"{variable.name} must look like owner/repo. Example: codefusion-repo/project-os-v2."

    if is_positive_limit_variable(variable.name) and not re.fullmatch(r"[1-9][0-9]*", stripped):
        return f"{variable.name} must be a positive integer. Example: 3."

    return None


def validation_example(
    variable: InputVariable,
    skill_choices: tuple[str, ...] | None = None,
) -> str:
    """Return a concise example for the common validated variable shapes."""

    if is_pm_authorization_status_variable(variable.name):
        return "Choose 1 for pending or 2 for granted for this exact scope and mode."
    if variable.name == PM_DECISION_ALREADY_MADE_NAME:
        return "Use true or false; local yes/no, si/sí/no, and 1/0 are normalized."
    if variable.name == PM_DECISION_NAME:
        return f"Required only when {PM_DECISION_ALREADY_MADE_NAME}=true; otherwise leave it blank."
    if is_optional_skill_variable(variable.name):
        choices = skill_choices or ()
        return f"Use an active skill, none, or leave it blank: {', '.join(choices)}."
    choices = placeholder_choices(variable.placeholder)
    if choices is not None:
        return f"Use one of: {', '.join(choices)}."
    if is_issue_or_pr_number(variable.name):
        return "Example: 123 or #123."
    if variable.name == "AUDIT_SCOPE":
        return "Example: owner/repo, issue #465, or PR #467."
    if is_repository_variable(variable.name):
        return "Example: codefusion-repo/project-os-v2."
    if is_positive_limit_variable(variable.name):
        return "Example: 3."
    return "Enter a non-empty value."


def placeholder_choices(placeholder: str) -> tuple[str, ...] | None:
    """Extract simple ``<a|b>`` placeholder choices."""

    placeholder = placeholder.strip()
    if not (placeholder.startswith("<") and placeholder.endswith(">")):
        return None
    inner = placeholder[1:-1]
    if "|" not in inner:
        return None
    choices = tuple(part.strip() for part in inner.split("|") if part.strip())
    if not choices:
        return None
    if any(not re.fullmatch(r"[A-Za-z0-9_.-]+", choice) for choice in choices):
        return None
    return choices


def is_issue_or_pr_number(name: str) -> bool:
    """Identify variables that carry issue or PR numbers."""

    return name in {"ISSUE_NUMBER", "PR_NUMBER", "ROADMAP_ISSUE"} or name.endswith("_ISSUE_NUMBER")


def is_repository_variable(name: str) -> bool:
    """Identify repository-like variables such as TARGET_REPOSITORY."""

    return name.endswith("REPOSITORY") or name == "REPOSITORY_NAME"


def is_positive_limit_variable(name: str) -> bool:
    """Identify numeric limit variables without treating SCOPE_LIMIT as numeric."""

    return name.endswith("_COUNT_LIMIT") or name.endswith("_NUMBER_LIMIT")


def is_pm_authorization_status_variable(name: str) -> bool:
    """Identify the route-prompt authorization-status assistance variable."""

    return name == PM_AUTHORIZATION_STATUS_NAME


def is_optional_skill_variable(name: str) -> bool:
    """Identify the PM-selectable optional skill variable."""

    return name == "OPTIONAL_SKILL"


def is_carryover_variable(name: str) -> bool:
    """Identify stable context variables safe to offer for carry-over between prompts.

    ISSUE_NUMBER, PR_NUMBER, and other operation-specific result variables are
    deliberately excluded: they usually change per prompt and silently reusing
    them could route the PM to the wrong issue or PR.
    """

    return name == "ROADMAP_ISSUE" or is_repository_variable(name)


def carryover_values(values: dict[str, str]) -> dict[str, str]:
    """Return only the stable subset of values safe to carry over to the next prompt."""

    return {name: value for name, value in values.items() if value and is_carryover_variable(name)}


def normalize_pm_authorization_status(value: str) -> str | None:
    """Normalize explicit PM authorization-status choices without inferring approval."""

    normalized = value.strip().lower()
    if normalized in {"1", PM_AUTHORIZATION_PENDING}:
        return PM_AUTHORIZATION_PENDING
    if normalized in {"2", PM_AUTHORIZATION_GRANTED}:
        return PM_AUTHORIZATION_GRANTED
    return None


def normalize_pm_decision_already_made(value: str) -> str | None:
    """Normalize strict decision-state booleans from narrow local helpers."""

    normalized = value.strip().lower()
    if normalized in PM_DECISION_TRUE_CHOICES:
        return "true"
    if normalized in PM_DECISION_FALSE_CHOICES:
        return "false"
    return None


def normalize_variable_value(variable: InputVariable, value: str) -> str:
    """Normalize supported variable values after validation."""

    if is_pm_authorization_status_variable(variable.name):
        normalized = normalize_pm_authorization_status(value)
        if normalized is not None:
            return normalized
    if variable.name == PM_DECISION_ALREADY_MADE_NAME:
        normalized = normalize_pm_decision_already_made(value)
        if normalized is not None:
            return normalized
    return value


def operation_produces_route_prompt(operation: OperationTemplate) -> bool:
    """Return whether the operation's OUTPUT block can produce output.route_prompt."""

    return "output.route_prompt" in operation_output_refs(operation)


def operation_output_refs(operation: OperationTemplate) -> tuple[str, ...]:
    """Return distinct output refs from OUTPUT or compact bilingual delivery blocks."""

    refs: list[str] = []
    output_lines = named_block_lines(operation.text, "OUTPUT")
    if not output_lines:
        delivery_match = re.search(
            r"\*\*(?:Entrega|Deliver):\*\*\s*(.*?)(?=\.\s|\.$|\n|\Z)",
            operation.text,
            flags=re.IGNORECASE,
        )
        output_lines = [delivery_match.group(1)] if delivery_match else []
    for line in output_lines:
        for ref in re.findall(r"\boutput\.[A-Za-z0-9_.-]+\b", line):
            if ref not in refs:
                refs.append(ref)
    return tuple(refs)


def operation_requires_route_prompt_path_selection(operation: OperationTemplate) -> bool:
    """Return whether output.route_prompt is one of multiple possible output paths."""

    refs = operation_output_refs(operation)
    return "output.route_prompt" in refs and len(refs) > 1


def operation_keeps_hydration_override(
    operation: OperationTemplate,
    include_route_prompt_authorization: bool = False,
) -> bool:
    """Return whether this rendered path is a route prompt that may carry an override."""

    return operation_produces_route_prompt(operation) and (
        not operation_requires_route_prompt_path_selection(operation)
        or include_route_prompt_authorization
    )


def operation_needs_pm_authorization_assistance(operation: OperationTemplate) -> bool:
    """Return whether initial variable entry should ask for authorization status."""

    if operation_requires_route_prompt_path_selection(operation):
        return False
    return operation_produces_route_prompt(operation) or PM_AUTHORIZATION_STATUS_NAME in operation.text


def operation_declares_pm_authorization_status(operation: OperationTemplate) -> bool:
    """Return whether the operation already declares PM_AUTHORIZATION_STATUS in INPUT."""

    return any(is_pm_authorization_status_variable(variable.name) for variable in operation.variables)


def synthetic_pm_authorization_variable() -> InputVariable:
    """Build the local-only authorization-status variable offered by the wizard."""

    return InputVariable(
        PM_AUTHORIZATION_STATUS_NAME,
        "<pending | granted for this exact scope and mode>",
        True,
        "",
        "wizard route-prompt assistance",
    )


def wizard_variables(
    operation: OperationTemplate,
    include_route_prompt_authorization: bool = False,
) -> tuple[InputVariable, ...]:
    """Return operation INPUT variables plus any local wizard assistance variables."""

    needs_synthetic = (
        operation_needs_pm_authorization_assistance(operation)
        or include_route_prompt_authorization
    )
    if needs_synthetic and not operation_declares_pm_authorization_status(operation):
        return operation.variables + (synthetic_pm_authorization_variable(),)
    return operation.variables


def render_prompt(
    operation: OperationTemplate,
    values: dict[str, str],
    include_route_prompt_authorization: bool = False,
) -> str:
    """Render the filled local prompt artifact inline."""

    lines = operation.text.splitlines()
    if operation.is_alias:
        notice = (
            f"> Alias requested: `{operation.mos_code}`; canonical operation resolved: "
            f"`{operation.resolved_canonical_code}`. The canonical prompt below is the "
            "single operational source of truth."
        )
        insert_at = 1 if lines and lines[0].lstrip().startswith("#") else 0
        lines[insert_at:insert_at] = ["", notice]
    variables = wizard_variables(
        operation,
        include_route_prompt_authorization=include_route_prompt_authorization,
    )
    rendered_values = dict(values)
    # A historical maintenance alias owns selection compatibility, not a second
    # prompt. Its metadata therefore wins over any stale carried-over value.
    rendered_values.update(alias_bound_values(operation))
    for variable in variables:
        if variable.name in rendered_values:
            rendered_values[variable.name] = normalize_variable_value(
                variable, rendered_values[variable.name]
            )
    for i, line in enumerate(lines):
        for variable in variables:
            if variable.raw_line and line.rstrip() == variable.raw_line:
                value = rendered_values.get(variable.name, "").strip()
                if value:
                    lines[i] = f"  {variable.name}={single_line(value)}"
                else:
                    lines[i] = f"  {variable.name}="
                break
    needs_synthetic = (
        operation_needs_pm_authorization_assistance(operation)
        or include_route_prompt_authorization
    )
    has_input_block = any(line.strip() == "INPUT:" for line in lines)
    if not has_input_block:
        lines.extend(["", "INPUT:"])
        for variable in variables:
            value = rendered_values.get(variable.name, "").strip()
            lines.append(f"  {variable.name}={single_line(value) if value else ''}")
    elif needs_synthetic and not operation_declares_pm_authorization_status(operation):
        lines = insert_input_variable_line(
            lines,
            PM_AUTHORIZATION_STATUS_NAME,
            values.get(PM_AUTHORIZATION_STATUS_NAME, "").strip(),
        )
    hydration_override = values.get(HYDRATION_LEVEL_NAME, "").strip()
    if (
        hydration_override
        and operation_keeps_hydration_override(
            operation,
            include_route_prompt_authorization=include_route_prompt_authorization,
        )
        and not any(
            variable.name == HYDRATION_LEVEL_NAME for variable in variables
        )
    ):
        lines = insert_input_variable_line(lines, HYDRATION_LEVEL_NAME, hydration_override)
    return "\n".join(lines) + "\n"


def insert_input_variable_line(lines: list[str], name: str, value: str) -> list[str]:
    """Insert a synthetic INPUT line into the first INPUT block."""

    rendered_line = f"  {name}={single_line(value)}" if value else f"  {name}="
    rendered_lines = list(lines)
    for index, line in enumerate(rendered_lines):
        if line.strip() != "INPUT:":
            continue
        insert_at = len(rendered_lines)
        for candidate in range(index + 1, len(rendered_lines)):
            if BLOCK_HEADER_PATTERN.match(rendered_lines[candidate].strip()):
                insert_at = candidate
                break
        while insert_at > index + 1 and not rendered_lines[insert_at - 1].strip():
            insert_at -= 1
        rendered_lines.insert(insert_at, rendered_line)
        return rendered_lines
    if rendered_lines and rendered_lines[-1].strip():
        rendered_lines.append("")
    rendered_lines.extend(["INPUT:", rendered_line])
    return rendered_lines


def single_line(value: str) -> str:
    """Keep rendered INPUT lines one-line without hiding the supplied value."""

    return value.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")


def generated_filename(operation: OperationTemplate, rendered_prompt: str) -> str:
    """Build a deterministic safe filename without exposing variable values."""

    stem = safe_filename_stem(operation.path.stem)
    digest = hashlib.sha256(rendered_prompt.encode("utf-8")).hexdigest()[:12]
    return f"{stem}-{digest}.md"


def safe_filename_stem(value: str) -> str:
    """Return a conservative filename stem."""

    stem = SAFE_FILENAME_PATTERN.sub("-", value.strip().lower())
    stem = stem.strip(".-_")
    return stem or "operation-prompt"



SessionStage = Literal["select_operation", "collect_values", "route_prompt_path", "preview", "post_write", "exit"]


@dataclass(frozen=True)
class WizardSession:
    """Pure session state shared by every interactive adapter."""

    stage: SessionStage = "select_operation"
    operation: OperationTemplate | None = None
    values: dict[str, str] = field(default_factory=dict)
    include_route_prompt_authorization: bool = False
    current_prompt_path: Path | None = None
    written_operation: OperationTemplate | None = None
    written_values: dict[str, str] = field(default_factory=dict)


def transition_session(
    session: WizardSession,
    event: str,
    *,
    operation: OperationTemplate | None = None,
    values: dict[str, str] | None = None,
    captured_intent: dict[str, str] | None = None,
    include_route_prompt_authorization: bool = False,
    current_prompt_path: Path | None = None,
) -> WizardSession:
    """Advance the one wizard state machine without performing any side effect."""

    next_values = dict(session.values if values is None else values)
    if event == "selected":
        next_values = carryover_values(session.values)
        next_values.update(captured_intent or {})
        if operation is not None:
            next_values.update(alias_bound_values(operation))
        return replace(session, stage="collect_values", operation=operation, values=next_values,
                       include_route_prompt_authorization=False)
    if event == "selection_cancel":
        return replace(session, stage="post_write" if session.current_prompt_path else "exit")
    if event == "values_cancel":
        return replace(session, values=next_values,
                       stage="post_write" if session.current_prompt_path else "exit")
    if event == "values_operation":
        return replace(session, stage="select_operation", values=next_values,
                       include_route_prompt_authorization=False)
    if event == "values_complete":
        stage: SessionStage = (
            "route_prompt_path"
            if operation is not None and operation_requires_route_prompt_path_selection(operation)
            else "preview"
        )
        return replace(session, stage=stage, values=next_values,
                       include_route_prompt_authorization=False)
    if event == "route_cancel":
        return replace(session, values=next_values,
                       stage="post_write" if session.current_prompt_path else "exit")
    if event == "route_values":
        return replace(session, stage="collect_values", values=next_values,
                       include_route_prompt_authorization=False)
    if event == "route_preview":
        return replace(session, stage="preview", values=next_values,
                       include_route_prompt_authorization=include_route_prompt_authorization)
    if event == "preview_edit":
        return replace(session, stage="collect_values")
    if event == "preview_operation":
        return replace(session, stage="select_operation", include_route_prompt_authorization=False)
    if event == "preview_cancel":
        return replace(session, stage="post_write" if session.current_prompt_path else "exit")
    if event == "written":
        return replace(session, stage="post_write", current_prompt_path=current_prompt_path,
                       written_operation=session.operation, written_values=dict(session.values))
    if event == "post_exit":
        return replace(session, stage="exit")
    if event == "post_new":
        return replace(session, stage="select_operation", values=carryover_values(session.written_values),
                       include_route_prompt_authorization=False)
    if event == "post_same":
        return replace(session, stage="collect_values", operation=session.written_operation,
                       values=carryover_values(session.written_values), include_route_prompt_authorization=False)
    if event == "post_edit":
        return replace(session, stage="collect_values", operation=session.written_operation,
                       values=dict(session.written_values), include_route_prompt_authorization=False)
    raise AssertionError(f"unreachable wizard session event: {event!r}")


def _operation_phase(operation: OperationTemplate, phase_by_operation: dict[int, str]) -> str:
    return phase_by_operation.get(operation.index) or operation.phase_label or "Sin fase"
