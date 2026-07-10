"""Local wizard for generating filled operation prompts.

If prompt_toolkit is importable, the wizard uses an enhanced interactive mode.
If unavailable, it falls back to a standard line-based flow.
The wizard reads the active operation catalog from ``project-os-es/operaciones``
and only writes local Markdown prompt artifacts. It does not execute
operations, run commands, or call GitHub, git, or network services.

The wizard stays open across multiple generated prompts in one session until
the PM explicitly exits, and keeps only the single latest wizard-generated
prompt in its resolved output folder.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import Completer, Completion, WordCompleter
    from prompt_toolkit.validation import Validator, ValidationError
    from prompt_toolkit.styles import Style
    from prompt_toolkit.formatted_text import HTML
    HAVE_PROMPT_TOOLKIT = True
except ImportError:
    HAVE_PROMPT_TOOLKIT = False

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OPERATIONS_DIR = REPO_ROOT / "project-os-es" / "operaciones"
DEFAULT_SKILLS_CATALOG = REPO_ROOT / "project-os-es" / "kernel" / "skills.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / ".local" / "operation-prompts"
# The active Spanish catalog encodes its phase model in directory names.  An
# optional table can still override those labels for custom catalogs.
DEFAULT_OPERATION_FLOWS_PATH: Path | None = None
OUTPUT_DIR_ENV = "PROJECT_OS_OPERATION_PROMPT_OUTPUT_DIR"

BLOCK_HEADER_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*:\s*$")
INPUT_VARIABLE_PATTERN = re.compile(
    r"^\s*(?P<name>[A-Z][A-Z0-9_]*)\s*=\s*(?P<placeholder><[^>\n]+>)?(?P<tail>.*)$"
)
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
POSITIVE_NUMBER_PATTERN = re.compile(r"^#?[1-9][0-9]*$")
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

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def mos_code(self) -> str | None:
        match = MOS_CODE_PATTERN.match(self.path.stem)
        return match.group(1).upper() if match else None

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
            if part == "cross-fase":
                labels.append("Cross-fase")
            elif match := re.fullmatch(r"fase-(\d+)", part):
                labels.append(f"Fase {match.group(1)}")
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


def discover_operations(operations_dir: Path = DEFAULT_OPERATIONS_DIR) -> list[OperationTemplate]:
    """Discover active operation Markdown files recursively and deterministically."""

    operations_dir = operations_dir.expanduser()
    if not operations_dir.is_dir():
        raise WizardError(f"operations directory not found: {operations_dir}")

    paths = sorted(
        (path for path in operations_dir.rglob("*.md") if path.name != "README.md"),
        key=lambda path: path.relative_to(operations_dir).as_posix(),
    )
    if not paths:
        raise WizardError(f"no .md operation templates found in: {operations_dir}")

    operations: list[OperationTemplate] = []
    for index, path in enumerate(paths, start=1):
        text = path.read_text(encoding="utf-8")
        operations.append(
            OperationTemplate(
                index=index,
                path=path,
                title=extract_title(text, path),
                description=extract_description(text, path),
                text=text,
                variables=parse_input_variables(text),
                catalog_root=operations_dir,
            )
        )
    return operations


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

    match = re.search(r"^\*\*Hace:\*\*\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if match:
        return match.group(1)

    title = extract_title(text, path)
    return re.sub(r"^MOS-(?:\d+\.\d+|R\.\d+)\s*[—-]\s*", "", title, flags=re.IGNORECASE)


def parse_input_variables(text: str) -> tuple[InputVariable, ...]:
    """Parse variables from conventional INPUT or active Spanish Variables blocks."""

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

    variables.extend(parse_spanish_variables(text))
    return tuple(variables)


def parse_spanish_variables(text: str) -> tuple[InputVariable, ...]:
    """Parse ``**Variables**`` from the compact active Spanish catalog."""

    marker = "**Variables**"
    if marker not in text:
        return ()
    section = text.split(marker, 1)[1]
    section = re.split(r"\n\s*\n(?=\*\*)", section, maxsplit=1)[0]
    parsed: list[InputVariable] = []
    for label, required in (("Requeridas", True), ("Opcionales", False)):
        match = re.search(
            rf"^-\s*{label}:\s*(.*?)(?=^-\s*(?:Requeridas|Opcionales):|\Z)",
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
                    note=f"{label.lower()} en catálogo español",
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
    return matches


def resolve_operation_selection(
    operations: list[OperationTemplate], selection: str
) -> OperationTemplate | None:
    """Resolve one exact active operation and fail safely on duplicate matches."""

    normalized = selection.strip().lower()
    if not normalized:
        return None

    explicit_index = re.fullmatch(r"(?:index|indice|índice):?(\d+)", normalized)
    if explicit_index:
        return _unique_operation(op for op in operations if op.index == int(explicit_index.group(1)))

    if normalized.isdigit():
        index_match = _unique_operation(op for op in operations if op.index == int(normalized))
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
    unique = {operation.path.resolve(): operation for operation in candidates}
    return next(iter(unique.values())) if len(unique) == 1 else None


def validate_variable_value(
    variable: InputVariable,
    value: str,
    skill_choices: tuple[str, ...] | None = None,
) -> str | None:
    """Return a validation error for common variable shapes, or ``None``."""

    stripped = value.strip()
    if variable.required and not stripped:
        return f"{variable.name} is required. {validation_example(variable)}"
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

    if is_optional_skill_variable(variable.name):
        choices = skill_choices or load_active_skill_choices()
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
    if is_optional_skill_variable(variable.name):
        choices = skill_choices or load_active_skill_choices()
        return f"Use an active skill, none, or leave it blank: {', '.join(choices)}."
    choices = placeholder_choices(variable.placeholder)
    if choices is not None:
        return f"Use one of: {', '.join(choices)}."
    if is_issue_or_pr_number(variable.name):
        return "Example: 123 or #123."
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
        name = entry.get("nombre")
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
                "key skill.*, non-empty nombre, and boolean active"
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


def normalize_variable_value(variable: InputVariable, value: str) -> str:
    """Normalize supported variable values after validation."""

    if is_pm_authorization_status_variable(variable.name):
        normalized = normalize_pm_authorization_status(value)
        if normalized is not None:
            return normalized
    return value


def operation_produces_route_prompt(operation: OperationTemplate) -> bool:
    """Return whether the operation's OUTPUT block can produce output.route_prompt."""

    return "output.route_prompt" in operation_output_refs(operation)


def operation_output_refs(operation: OperationTemplate) -> tuple[str, ...]:
    """Return distinct output refs from OUTPUT or active Spanish Entrega blocks."""

    refs: list[str] = []
    output_lines = named_block_lines(operation.text, "OUTPUT")
    if not output_lines:
        delivery_match = re.search(
            r"\*\*Entrega:\*\*\s*(.*?)(?=\.\s|\.$|\n|\Z)",
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
    variables = wizard_variables(
        operation,
        include_route_prompt_authorization=include_route_prompt_authorization,
    )
    for i, line in enumerate(lines):
        for variable in variables:
            if variable.raw_line and line.rstrip() == variable.raw_line:
                value = values.get(variable.name, "").strip()
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
            value = values.get(variable.name, "").strip()
            lines.append(f"  {variable.name}={single_line(value) if value else ''}")
    elif needs_synthetic and not operation_declares_pm_authorization_status(operation):
        lines = insert_input_variable_line(
            lines,
            PM_AUTHORIZATION_STATUS_NAME,
            values.get(PM_AUTHORIZATION_STATUS_NAME, "").strip(),
        )
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


def resolve_output_dir(output_dir: Path | None) -> Path:
    """Resolve explicit, configured, or default output directory."""

    if output_dir is not None:
        return output_dir.expanduser()
    configured = os.environ.get(OUTPUT_DIR_ENV)
    if configured:
        return Path(configured).expanduser()
    return DEFAULT_OUTPUT_DIR


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
        for operation in operations or []
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


def _operation_phase(
    operation: OperationTemplate,
    phase_by_operation: dict[int, str],
) -> str:
    return phase_by_operation.get(operation.index) or operation.phase_label or "Sin fase"


def is_wizard_generated_artifact(path: Path) -> bool:
    """Identify a file as a wizard-generated prompt using filename shape and marker.

    Both signals must agree before a file is considered wizard-generated, so
    arbitrary or hand-authored ``.md`` files are never mistaken for cleanup
    candidates.
    """

    if not GENERATED_FILENAME_PATTERN.fullmatch(path.name):
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return WIZARD_PROMPT_MARKER in content


def find_existing_generated_prompts(output_dir: Path) -> list[Path]:
    """Return existing wizard-generated prompt artifacts already in the output folder."""

    if not output_dir.is_dir():
        return []
    return sorted(
        path
        for path in output_dir.iterdir()
        if path.is_file() and path.suffix == ".md" and is_wizard_generated_artifact(path)
    )


def find_replaceable_prompts(output_dir: Path, output_path: Path) -> list[Path]:
    """Return every previous wizard-generated prompt a new write would replace.

    May be more than one file, since cleanup_previous_generated_prompts()
    removes all matches other than the new output path; the pre-write notice
    must name all of them, not just the first, so it never understates what
    the write is about to delete.
    """

    output_resolved = output_path.resolve()
    return [
        existing
        for existing in find_existing_generated_prompts(output_dir)
        if existing.resolve() != output_resolved
    ]


def cleanup_previous_generated_prompts(output_dir: Path, keep_path: Path) -> list[Path]:
    """Remove wizard-generated prompt artifacts other than keep_path from output_dir only.

    Cleanup is limited to direct children of output_dir and only removes files
    identified by is_wizard_generated_artifact; nothing outside output_dir and
    no non-wizard file is ever touched.
    """

    keep_resolved = keep_path.resolve()
    removed: list[Path] = []
    for existing in find_existing_generated_prompts(output_dir):
        if existing.resolve() == keep_resolved:
            continue
        existing.unlink()
        removed.append(existing)
    return removed


def display_operations(operations: list[OperationTemplate], output_stream: TextIO) -> None:
    """Print one compact, non-duplicative line for each operation."""

    print("", file=output_stream)
    print("Available operations:", file=output_stream)
    for operation in operations:
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
    return f"{operation.index:>3}. {phase_part}{identity} — {operation.description}"


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
    for operation in operations:
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


def print_session_state(output_stream: TextIO, current_prompt_path: Path | None) -> None:
    """Print visible output-mode and current-prompt session state."""

    print("", file=output_stream)
    print("Output mode: single latest prompt", file=output_stream)
    if current_prompt_path is not None:
        print(f"Current prompt: {current_prompt_path}", file=output_stream)
    else:
        print("Current prompt: none yet.", file=output_stream)


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


def is_enumerated_view_command(value: str) -> bool:
    return value.strip().lower() in ENUMERATED_LIST_COMMANDS


def is_phase_view_command(value: str) -> bool:
    return value.strip().lower() in PHASE_LIST_COMMANDS


def print_selection_help(output_stream: TextIO) -> None:
    """Print operation-selection help without leaving the current flow."""

    print("", file=output_stream)
    print("Selection help:", file=output_stream)
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
    print("  - none — Sin skill opcional", file=output_stream)
    print("  - Enter — Dejar vacío", file=output_stream)


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


def print_value_help(output_stream: TextIO) -> None:
    """Print variable-entry help without leaving the current flow."""

    print("", file=output_stream)
    print("Variable entry help:", file=output_stream)
    print("  Required values must be filled; optional values may be left blank.", file=output_stream)
    print("  During edits, pressing Enter keeps the current value.", file=output_stream)
    print("  Use /clear to blank the current optional value.", file=output_stream)
    print("  Use back to choose another operation, cancel to exit, or ? for this help.", file=output_stream)


def select_operation(
    operations: list[OperationTemplate],
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    phase_by_operation: dict[int, str] | None = None,
) -> OperationTemplate | None:
    """Interactively search/filter/group and select one operation."""

    phase_by_operation = phase_by_operation or {}
    filtered = list(operations)
    print_stage("Step 1/3", "Search and select an operation", output_stream)
    print(
        "Commands: /enumerated (aliases /enumerator, /), /phases (alias /phase), "
        "s search, ? help, cancel exit.",
        file=output_stream,
    )
    print_enumerated_view(filtered, output_stream)
    while True:
        query = input_func(
            "\nSearch by index, MOS code, filename, title, relative path, or phase "
            "(Enter keeps view; /enumerated; /phases; ? help; cancel): "
        ).strip()
        if is_cancel_command(query):
            return None
        if is_help_command(query):
            print_selection_help(output_stream)
            continue
        if is_phase_view_command(query):
            filtered = list(operations)
            print_phase_groups(operations, phase_by_operation, output_stream)
            continue
        if is_enumerated_view_command(query):
            filtered = list(operations)
            print_enumerated_view(filtered, output_stream)
            continue
        if is_search_command(query):
            filtered = list(operations)
            print_enumerated_view(filtered, output_stream)
            continue
        if query:
            operation = resolve_operation_selection(filtered, query)
            if operation is not None:
                return operation
            matches = filter_operations(operations, query, phase_by_operation)
            if not matches:
                print(
                    "No matching operations. Try a title, MOS code, filename, relative path, phase, or index.",
                    file=output_stream,
                )
                continue
            filtered = matches
            display_operations(filtered, output_stream)

        selection = input_func(
            "Select by displayed index, MOS code, exact filename/stem/path (s search again, ? help, cancel): "
        ).strip()
        if is_search_command(selection):
            display_operations(filtered, output_stream)
            continue
        if is_phase_view_command(selection):
            filtered = list(operations)
            print_phase_groups(operations, phase_by_operation, output_stream)
            continue
        if is_enumerated_view_command(selection):
            filtered = list(operations)
            print_enumerated_view(filtered, output_stream)
            continue
        if is_help_command(selection):
            print_selection_help(output_stream)
            continue
        if is_cancel_command(selection):
            return None
        operation = resolve_operation_selection(filtered, selection)
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
) -> ValueCollectionResult:
    """Prompt for variable values and return navigation decisions."""

    values = dict(initial_values or {})
    print_stage("Step 2/3", "Fill INPUT variables", output_stream)
    display_operation_summary(operation, output_stream)
    variables = wizard_variables(operation)
    if not variables:
        print("This operation declares no INPUT variables.", file=output_stream)
        return ValueCollectionResult("values", values)

    print("", file=output_stream)
    print(
        "Optional values may be left blank. Commands: back, cancel, /clear optional, ? help.",
        file=output_stream,
    )
    for variable in variables:
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
                print_value_help(output_stream)
                continue
            if is_cancel_command(raw_value):
                return ValueCollectionResult("cancel", values)
            if is_back_command(raw_value):
                return ValueCollectionResult("operation", values)
            if is_clear_command(raw_value):
                if variable.required:
                    print(
                        f"Invalid value: {variable.name} is required. {validation_example(variable)}",
                        file=output_stream,
                    )
                    continue
                values[variable.name] = ""
                break

            value = raw_value.strip()
            if not value and current:
                value = current
            error = validate_variable_value(variable, value, skill_choices=skill_choices)
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
        error = validate_variable_value(variable, value)
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


def write_prompt(output_path: Path, rendered_prompt: str) -> Path:
    """Write the prompt artifact, tagged with the wizard-generated marker, after confirmation."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = rendered_prompt if rendered_prompt.endswith("\n") else rendered_prompt + "\n"
    content += WIZARD_PROMPT_MARKER + "\n"
    output_path.write_text(content, encoding="utf-8")
    return output_path


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


def run_wizard(
    operations_dir: Path = DEFAULT_OPERATIONS_DIR,
    output_dir: Path | None = None,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
    operation_flows_path: Path | None = DEFAULT_OPERATION_FLOWS_PATH,
    skills_catalog_path: Path = DEFAULT_SKILLS_CATALOG,
) -> Path | None:
    """Run the interactive operation prompt wizard for one or more prompts in one session."""

    operations = discover_operations(operations_dir)
    output_directory = resolve_output_dir(output_dir)
    phase_by_operation = load_phase_map(operation_flows_path, operations)
    skill_options = load_active_skill_options(skills_catalog_path)
    skill_choices = skill_choice_keys(skill_options)

    written_operation: OperationTemplate | None = None
    written_values: dict[str, str] = {}
    current_prompt_path: Path | None = None

    operation: OperationTemplate | None = None
    values: dict[str, str] = {}
    include_route_prompt_authorization = False
    stage = "select_operation"

    while True:
        if stage == "select_operation":
            print_session_state(output_stream, current_prompt_path)
            picked = select_operation(
                operations,
                input_func=input_func,
                output_stream=output_stream,
                phase_by_operation=phase_by_operation,
            )
            if picked is None:
                if current_prompt_path is not None:
                    stage = "post_write"
                    continue
                print("Cancelled before operation selection. No file was created.", file=output_stream)
                return None
            operation = picked
            values = carryover_values(values)
            include_route_prompt_authorization = False
            stage = "collect_values"
            continue

        elif stage == "collect_values":
            result = collect_values_with_controls(
                operation,
                input_func=input_func,
                output_stream=output_stream,
                initial_values=values,
                skill_choices=skill_choices,
                skill_options=skill_options,
            )
            if result.action == "cancel":
                if current_prompt_path is not None:
                    stage = "post_write"
                    continue
                print("Cancelled before write. No file was created.", file=output_stream)
                return None
            if result.action == "operation":
                print("Returning to operation selection.", file=output_stream)
                values = result.values
                include_route_prompt_authorization = False
                stage = "select_operation"
                continue
            values = result.values
            include_route_prompt_authorization = False
            if operation_requires_route_prompt_path_selection(operation):
                stage = "route_prompt_path"
                continue
            stage = "preview"
            continue

        elif stage == "route_prompt_path":
            result = collect_route_prompt_path_with_controls(
                operation,
                input_func=input_func,
                output_stream=output_stream,
                initial_values=values,
            )
            if result.action == "cancel":
                if current_prompt_path is not None:
                    stage = "post_write"
                    continue
                print("Cancelled before write. No file was created.", file=output_stream)
                return None
            if result.action == "values":
                print("Returning to variable entry.", file=output_stream)
                values = result.values
                include_route_prompt_authorization = False
                stage = "collect_values"
                continue
            values = result.values
            include_route_prompt_authorization = result.include_pm_authorization_status
            stage = "preview"
            continue

        elif stage == "preview":
            rendered = render_prompt(
                operation,
                values,
                include_route_prompt_authorization=include_route_prompt_authorization,
            )
            output_path = output_directory / generated_filename(operation, rendered)
            replacing = find_replaceable_prompts(output_directory, output_path)
            action = choose_preview_action(
                operation,
                values,
                rendered,
                output_path,
                replacing,
                input_func=input_func,
                output_stream=output_stream,
                include_route_prompt_authorization=include_route_prompt_authorization,
            )
            if action == "write":
                path = write_prompt(output_path, rendered)
                removed = cleanup_previous_generated_prompts(output_directory, keep_path=path)
                current_prompt_path = path
                written_operation = operation
                written_values = dict(values)
                print(f"Wrote generated prompt: {path}", file=output_stream)
                for removed_path in removed:
                    print(f"Removed previous generated prompt: {removed_path}", file=output_stream)
                stage = "post_write"
                continue
            if action == "edit":
                print("Returning to variable entry.", file=output_stream)
                stage = "collect_values"
                continue
            if action == "operation":
                print("Returning to operation selection.", file=output_stream)
                include_route_prompt_authorization = False
                stage = "select_operation"
                continue
            if current_prompt_path is not None:
                stage = "post_write"
                continue
            print("Cancelled before write. No file was created.", file=output_stream)
            return None

        elif stage == "post_write":
            post_action = choose_post_write_action(
                current_prompt_path, input_func=input_func, output_stream=output_stream
            )
            if post_action == "exit":
                print("Exiting wizard session.", file=output_stream)
                return current_prompt_path
            if post_action == "new":
                values = carryover_values(written_values)
                include_route_prompt_authorization = False
                stage = "select_operation"
                continue
            if post_action == "same":
                operation = written_operation
                values = carryover_values(written_values)
                include_route_prompt_authorization = False
                stage = "collect_values"
                continue
            if post_action == "edit":
                operation = written_operation
                values = dict(written_values)
                include_route_prompt_authorization = False
                stage = "collect_values"
                continue

        else:
            raise AssertionError(f"unreachable wizard stage: {stage!r}")


if HAVE_PROMPT_TOOLKIT:
    class OperationCompleter(Completer):
        def __init__(self, operations, phase_by_operation=None):
            self.operations = operations
            self.phase_by_operation = phase_by_operation or {}

        def get_completions(self, document, complete_event):
            text = document.text.lower()
            for op in self.operations:
                phase = _operation_phase(op, self.phase_by_operation)
                if (
                    text in op.filename.lower()
                    or text in op.path.stem.lower()
                    or text in op.title.lower()
                    or text in op.description.lower()
                    or text in op.relative_path.lower()
                    or text in op.phase_path.lower()
                    or text in (op.mos_code or "").lower()
                    or text == str(op.index)
                    or (phase and text in phase.lower())
                ):
                    display_text = operation_display_line(op)
                    yield Completion(
                        op.mos_code or op.relative_path,
                        start_position=-len(document.text),
                        display=display_text,
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
                raise ValidationError(
                    message=(
                        "Invalid or ambiguous selection. Use a displayed index, MOS code, "
                        "exact filename/stem/path, or cancel."
                    ),
                    cursor_position=len(document.text)
                )

    def select_operation_pt(
        operations: list[OperationTemplate],
        output_stream: TextIO,
        phase_by_operation: dict[int, str] | None = None,
    ) -> OperationTemplate | None:
        phase_by_operation = phase_by_operation or {}
        print_stage("Step 1/3", "Search and select an operation", output_stream)
        print_enumerated_view(operations, output_stream)
        style = Style.from_dict({
            'bottom-toolbar': 'bg:#333333 #ffffff',
        })
        def bottom_toolbar():
            return HTML(
                ' <b>Commands</b>: index/MOS/path, /enumerated (/enumerator, /), '
                '/phases (/phase), cancel, ? help.'
            )

        completer = OperationCompleter(operations, phase_by_operation)
        validator = OperationValidator(operations)

        while True:
            try:
                selection = prompt(
                    "Search/select operation: ",
                    completer=completer,
                    validator=validator,
                    style=style,
                    bottom_toolbar=bottom_toolbar
                ).strip()
            except (EOFError, KeyboardInterrupt):
                return None

            if is_cancel_command(selection):
                return None
            if is_help_command(selection):
                print_selection_help(output_stream)
                continue
            if is_phase_view_command(selection):
                print_phase_groups(operations, phase_by_operation, output_stream)
                continue
            if is_enumerated_view_command(selection) or is_search_command(selection):
                print_enumerated_view(operations, output_stream)
                continue

            operation = resolve_operation_selection(operations, selection)
            if operation is not None:
                return operation

    def collect_values_with_controls_pt(
        operation: OperationTemplate,
        output_stream: TextIO,
        initial_values: dict[str, str] | None = None,
        skill_choices: tuple[str, ...] | None = None,
        skill_options: tuple[SkillOption, ...] | None = None,
    ) -> ValueCollectionResult:
        values = dict(initial_values or {})
        print_stage("Step 2/3", "Fill INPUT variables", output_stream)
        display_operation_summary(operation, output_stream)
        variables = wizard_variables(operation)
        if not variables:
            print("This operation declares no INPUT variables.", file=output_stream)
            return ValueCollectionResult("values", values)

        print("", file=output_stream)

        style = Style.from_dict({
            'bottom-toolbar': 'bg:#333333 #ffffff',
        })

        for variable in variables:
            if is_pm_authorization_status_variable(variable.name):
                print_pm_authorization_assistance(output_stream)
            if is_optional_skill_variable(variable.name):
                print_optional_skill_options(output_stream, skill_options=skill_options)
            label = "required" if variable.required else "optional"

            def bottom_toolbar():
                return HTML(f' <b>{variable.name}</b> ({label}) | Commands: back, cancel, /clear, ? help')

            class VariableValidator(Validator):
                def validate(self, document):
                    text = document.text.strip()
                    if is_cancel_command(text) or is_back_command(text) or is_clear_command(text) or is_help_command(text):
                        return
                    if not text:
                        if variable.required:
                            raise ValidationError(message=f"Required. {validation_example(variable)}", cursor_position=len(document.text))
                        return
                    error = validate_variable_value(variable, text, skill_choices=skill_choices)
                    if error is not None:
                        raise ValidationError(message=error, cursor_position=len(document.text))

            completer = None
            if is_pm_authorization_status_variable(variable.name):
                completer = WordCompleter(["1", "2", *PM_AUTHORIZATION_CHOICES], ignore_case=True)
            elif is_optional_skill_variable(variable.name):
                completer = WordCompleter(list(skill_choices or load_active_skill_choices()), ignore_case=True)
            else:
                choices = placeholder_choices(variable.placeholder)
                if choices:
                    completer = WordCompleter(list(choices), ignore_case=True)

            while True:
                current = values.get(variable.name, "")
                try:
                    prompt_label = (
                        "Select OPTIONAL_SKILL: "
                        if is_optional_skill_variable(variable.name)
                        else f"{variable.name} ({label}, {variable.placeholder}): "
                    )
                    raw_value = prompt(
                        prompt_label,
                        default=current,
                        validator=VariableValidator(),
                        completer=completer,
                        complete_while_typing=is_optional_skill_variable(variable.name),
                        style=style,
                        bottom_toolbar=bottom_toolbar
                    )
                except (EOFError, KeyboardInterrupt):
                    return ValueCollectionResult("cancel", values)

                if is_help_command(raw_value):
                    print_value_help(output_stream)
                    continue
                if is_cancel_command(raw_value):
                    return ValueCollectionResult("cancel", values)
                if is_back_command(raw_value):
                    return ValueCollectionResult("operation", values)
                if is_clear_command(raw_value):
                    if variable.required:
                        print(
                            f"Invalid value: {variable.name} is required. {validation_example(variable)}",
                            file=output_stream,
                        )
                        continue
                    values[variable.name] = ""
                    break

                value = raw_value.strip()
                values[variable.name] = normalize_variable_value(variable, value)
                break

        return ValueCollectionResult("values", values)

    def collect_route_prompt_path_with_controls_pt(
        operation: OperationTemplate,
        output_stream: TextIO,
        initial_values: dict[str, str] | None = None,
    ) -> RoutePromptPathResult:
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

        style = Style.from_dict({
            'bottom-toolbar': 'bg:#333333 #ffffff',
        })

        def bottom_toolbar():
            return HTML(' <b>Output path</b>: 1 route-prompt, 2 non-route, back, cancel, ? help')

        path_choices = {
            "1",
            "2",
            "route",
            "route-prompt",
            "route_prompt",
            "output.route_prompt",
            "non-route",
            "nonroute",
            "status",
            "status_result",
            "pm_command_bundle",
        }
        completer = WordCompleter(sorted(path_choices | BACK_COMMANDS | CANCEL_COMMANDS | HELP_COMMANDS), ignore_case=True)

        class OutputPathValidator(Validator):
            def validate(self, document):
                text = document.text.strip().lower()
                if text in path_choices or is_help_command(text) or is_back_command(text) or is_cancel_command(text):
                    return
                raise ValidationError(
                    message="Choose 1 route-prompt, 2 non-route, back, or cancel.",
                    cursor_position=len(document.text),
                )

        while True:
            try:
                answer = prompt(
                    "Selected output path [1 route-prompt / 2 non-route]: ",
                    completer=completer,
                    validator=OutputPathValidator(),
                    style=style,
                    bottom_toolbar=bottom_toolbar,
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                return RoutePromptPathResult("cancel", values, False)

            if is_help_command(answer):
                print_output_path_help(output_stream)
                continue
            if is_cancel_command(answer):
                return RoutePromptPathResult("cancel", values, False)
            if is_back_command(answer):
                return RoutePromptPathResult("values", values, False)
            if answer in {"2", "non-route", "nonroute", "status", "status_result", "pm_command_bundle"}:
                values.pop(PM_AUTHORIZATION_STATUS_NAME, None)
                return RoutePromptPathResult("preview", values, False)
            return collect_route_prompt_authorization_status_pt(values, output_stream)

    def collect_route_prompt_authorization_status_pt(
        values: dict[str, str],
        output_stream: TextIO,
    ) -> RoutePromptPathResult:
        variable = synthetic_pm_authorization_variable()
        print_pm_authorization_assistance(output_stream)

        style = Style.from_dict({
            'bottom-toolbar': 'bg:#333333 #ffffff',
        })

        def bottom_toolbar():
            return HTML(' <b>PM_AUTHORIZATION_STATUS</b> | Commands: back, cancel, ? help')

        class RouteAuthorizationValidator(Validator):
            def validate(self, document):
                text = document.text.strip()
                if is_cancel_command(text) or is_back_command(text) or is_help_command(text):
                    return
                error = validate_variable_value(variable, text)
                if error is not None:
                    raise ValidationError(message=error, cursor_position=len(document.text))

        completer = WordCompleter(["1", "2", *PM_AUTHORIZATION_CHOICES], ignore_case=True)
        while True:
            current = values.get(variable.name, "")
            try:
                raw_value = prompt(
                    f"{variable.name} (required, {variable.placeholder}): ",
                    default=current,
                    validator=RouteAuthorizationValidator(),
                    completer=completer,
                    style=style,
                    bottom_toolbar=bottom_toolbar,
                )
            except (EOFError, KeyboardInterrupt):
                return RoutePromptPathResult("cancel", values, True)

            if is_help_command(raw_value):
                print_output_path_help(output_stream)
                print_pm_authorization_assistance(output_stream)
                continue
            if is_cancel_command(raw_value):
                return RoutePromptPathResult("cancel", values, True)
            if is_back_command(raw_value):
                values.pop(PM_AUTHORIZATION_STATUS_NAME, None)
                return RoutePromptPathResult("values", values, False)
            values[variable.name] = normalize_variable_value(variable, raw_value.strip())
            return RoutePromptPathResult("preview", values, True)

    def choose_preview_action_pt(
        operation: OperationTemplate,
        values: dict[str, str],
        rendered_prompt: str,
        output_path: Path,
        replacing: list[Path],
        output_stream: TextIO,
        include_route_prompt_authorization: bool = False,
    ) -> str:
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

        style = Style.from_dict({
            'bottom-toolbar': 'bg:#333333 #ffffff',
        })
        def bottom_toolbar():
            return HTML(' <b>Actions</b>: write, edit, operation, cancel, ? help')

        completer = WordCompleter(["write", "edit", "operation", "cancel", "help", "?"], ignore_case=True)

        class ActionValidator(Validator):
            def validate(self, document):
                val = document.text.strip().lower()
                if not val or val in {"n", "no"}:
                    return
                if val in CANCEL_COMMANDS or val in WRITE_COMMANDS or val in EDIT_COMMANDS or val in OPERATION_COMMANDS or val in HELP_COMMANDS:
                    return
                raise ValidationError(message="Choose write, edit, operation, cancel, or ? help.", cursor_position=len(document.text))

        while True:
            try:
                answer = prompt(
                    "Choose action [write/edit/operation/cancel]: ",
                    completer=completer,
                    validator=ActionValidator(),
                    style=style,
                    bottom_toolbar=bottom_toolbar
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                return "cancel"

            if not answer or answer in {"n", "no"} or answer in CANCEL_COMMANDS:
                return "cancel"
            if answer in WRITE_COMMANDS:
                if output_path.exists():
                    try:
                        overwrite = prompt(
                            f"{output_path} exists. Overwrite? [y/N]: ",
                            style=style
                        ).strip().lower()
                    except (EOFError, KeyboardInterrupt):
                        return "cancel"
                    if overwrite not in {"y", "yes"}:
                        print("Overwrite declined. Choose another preview action.", file=output_stream)
                        continue
                return "write"
            if answer in EDIT_COMMANDS:
                return "edit"
            if answer in OPERATION_COMMANDS:
                return "operation"
            if answer in HELP_COMMANDS:
                print_preview_help(output_stream)
                continue

    def choose_post_write_action_pt(current_prompt_path: Path, output_stream: TextIO) -> str:
        print_session_state(output_stream, current_prompt_path)
        print("Post-write actions: new, same, edit, path, exit, ? help.", file=output_stream)

        style = Style.from_dict({
            'bottom-toolbar': 'bg:#333333 #ffffff',
        })
        def bottom_toolbar():
            return HTML(' <b>Post-write</b>: new, same, edit, path, exit, ? help')

        completer = WordCompleter(["new", "same", "edit", "path", "exit", "help", "?"], ignore_case=True)
        allowed = (
            POST_WRITE_NEW_COMMANDS
            | POST_WRITE_SAME_COMMANDS
            | POST_WRITE_PATH_COMMANDS
            | EDIT_COMMANDS
            | CANCEL_COMMANDS
            | HELP_COMMANDS
        )

        class PostWriteValidator(Validator):
            def validate(self, document):
                val = document.text.strip().lower()
                if not val:
                    return
                if val not in allowed:
                    raise ValidationError(
                        message="Choose new, same, edit, path, exit, or ? help.",
                        cursor_position=len(document.text),
                    )

        while True:
            try:
                answer = prompt(
                    "Choose action [new/same/edit/path/exit]: ",
                    completer=completer,
                    validator=PostWriteValidator(),
                    style=style,
                    bottom_toolbar=bottom_toolbar,
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                return "exit"

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

    def run_wizard_pt(
        operations_dir: Path = DEFAULT_OPERATIONS_DIR,
        output_dir: Path | None = None,
        output_stream: TextIO = sys.stdout,
        operation_flows_path: Path | None = DEFAULT_OPERATION_FLOWS_PATH,
        skills_catalog_path: Path = DEFAULT_SKILLS_CATALOG,
    ) -> Path | None:
        operations = discover_operations(operations_dir)
        output_directory = resolve_output_dir(output_dir)
        phase_by_operation = load_phase_map(operation_flows_path, operations)
        skill_options = load_active_skill_options(skills_catalog_path)
        skill_choices = skill_choice_keys(skill_options)

        written_operation: OperationTemplate | None = None
        written_values: dict[str, str] = {}
        current_prompt_path: Path | None = None

        operation: OperationTemplate | None = None
        values: dict[str, str] = {}
        include_route_prompt_authorization = False
        stage = "select_operation"

        while True:
            if stage == "select_operation":
                print_session_state(output_stream, current_prompt_path)
                picked = select_operation_pt(
                    operations, output_stream=output_stream, phase_by_operation=phase_by_operation
                )
                if picked is None:
                    if current_prompt_path is not None:
                        stage = "post_write"
                        continue
                    print("Cancelled before operation selection. No file was created.", file=output_stream)
                    return None
                operation = picked
                values = carryover_values(values)
                include_route_prompt_authorization = False
                stage = "collect_values"
                continue

            elif stage == "collect_values":
                result = collect_values_with_controls_pt(
                    operation,
                    output_stream=output_stream,
                    initial_values=values,
                    skill_choices=skill_choices,
                    skill_options=skill_options,
                )
                if result.action == "cancel":
                    if current_prompt_path is not None:
                        stage = "post_write"
                        continue
                    print("Cancelled before write. No file was created.", file=output_stream)
                    return None
                if result.action == "operation":
                    print("Returning to operation selection.", file=output_stream)
                    values = result.values
                    include_route_prompt_authorization = False
                    stage = "select_operation"
                    continue
                values = result.values
                include_route_prompt_authorization = False
                if operation_requires_route_prompt_path_selection(operation):
                    stage = "route_prompt_path"
                    continue
                stage = "preview"
                continue

            elif stage == "route_prompt_path":
                result = collect_route_prompt_path_with_controls_pt(
                    operation,
                    output_stream=output_stream,
                    initial_values=values,
                )
                if result.action == "cancel":
                    if current_prompt_path is not None:
                        stage = "post_write"
                        continue
                    print("Cancelled before write. No file was created.", file=output_stream)
                    return None
                if result.action == "values":
                    print("Returning to variable entry.", file=output_stream)
                    values = result.values
                    include_route_prompt_authorization = False
                    stage = "collect_values"
                    continue
                values = result.values
                include_route_prompt_authorization = result.include_pm_authorization_status
                stage = "preview"
                continue

            elif stage == "preview":
                rendered = render_prompt(
                    operation,
                    values,
                    include_route_prompt_authorization=include_route_prompt_authorization,
                )
                output_path = output_directory / generated_filename(operation, rendered)
                replacing = find_replaceable_prompts(output_directory, output_path)
                action = choose_preview_action_pt(
                    operation,
                    values,
                    rendered,
                    output_path,
                    replacing,
                    output_stream=output_stream,
                    include_route_prompt_authorization=include_route_prompt_authorization,
                )
                if action == "write":
                    path = write_prompt(output_path, rendered)
                    removed = cleanup_previous_generated_prompts(output_directory, keep_path=path)
                    current_prompt_path = path
                    written_operation = operation
                    written_values = dict(values)
                    print(f"Wrote generated prompt: {path}", file=output_stream)
                    for removed_path in removed:
                        print(f"Removed previous generated prompt: {removed_path}", file=output_stream)
                    stage = "post_write"
                    continue
                if action == "edit":
                    print("Returning to variable entry.", file=output_stream)
                    stage = "collect_values"
                    continue
                if action == "operation":
                    print("Returning to operation selection.", file=output_stream)
                    include_route_prompt_authorization = False
                    stage = "select_operation"
                    continue
                if current_prompt_path is not None:
                    stage = "post_write"
                    continue
                print("Cancelled before write. No file was created.", file=output_stream)
                return None

            elif stage == "post_write":
                post_action = choose_post_write_action_pt(current_prompt_path, output_stream=output_stream)
                if post_action == "exit":
                    print("Exiting wizard session.", file=output_stream)
                    return current_prompt_path
                if post_action == "new":
                    values = carryover_values(written_values)
                    include_route_prompt_authorization = False
                    stage = "select_operation"
                    continue
                if post_action == "same":
                    operation = written_operation
                    values = carryover_values(written_values)
                    include_route_prompt_authorization = False
                    stage = "collect_values"
                    continue
                if post_action == "edit":
                    operation = written_operation
                    values = dict(written_values)
                    include_route_prompt_authorization = False
                    stage = "collect_values"
                    continue

            else:
                raise AssertionError(f"unreachable wizard stage: {stage!r}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--operations-dir",
        type=Path,
        default=DEFAULT_OPERATIONS_DIR,
        help="Active operation catalog directory; Markdown files are discovered recursively.",
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
        if HAVE_PROMPT_TOOLKIT:
            result = run_wizard_pt(operations_dir=args.operations_dir, output_dir=args.output_dir)
        else:
            result = run_wizard(operations_dir=args.operations_dir, output_dir=args.output_dir)
    except WizardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.", file=sys.stderr)
        return 1
    return 0 if result is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
