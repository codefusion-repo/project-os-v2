"""Line-based local wizard for generating filled operation prompts.

The wizard reads operation templates from ``templates/operations`` and writes a
local Markdown prompt artifact. It does not execute operations, run commands, or
call GitHub, git, or network services.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OPERATIONS_DIR = REPO_ROOT / "templates" / "operations"
DEFAULT_OUTPUT_DIR = REPO_ROOT / ".local" / "operation-prompts"
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
class OperationTemplate:
    """A discovered operation template and parsed metadata."""

    index: int
    path: Path
    title: str
    text: str
    variables: tuple[InputVariable, ...]

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def file_number(self) -> int | None:
        match = re.match(r"^(\d+)", self.path.name)
        return int(match.group(1)) if match else None


def discover_operations(operations_dir: Path = DEFAULT_OPERATIONS_DIR) -> list[OperationTemplate]:
    """Discover Markdown operation templates in deterministic filename order."""

    operations_dir = operations_dir.expanduser()
    if not operations_dir.is_dir():
        raise WizardError(f"operations directory not found: {operations_dir}")

    paths = sorted(operations_dir.glob("*.md"), key=lambda path: path.name)
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
                text=text,
                variables=parse_input_variables(text),
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


def parse_input_variables(text: str) -> tuple[InputVariable, ...]:
    """Parse required and optional variables from the template ``INPUT:`` block."""

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
    return tuple(variables)


def input_block_lines(text: str) -> list[str]:
    """Return the raw lines inside the first ``INPUT:`` block."""

    lines = text.splitlines()
    in_input = False
    block: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not in_input:
            if stripped == "INPUT:":
                in_input = True
            continue
        if BLOCK_HEADER_PATTERN.match(stripped):
            break
        block.append(line)
    return block


def filter_operations(operations: list[OperationTemplate], query: str) -> list[OperationTemplate]:
    """Filter operations by displayed number, filename number, filename, or title."""

    normalized = query.strip().lower()
    if not normalized:
        return list(operations)

    numeric_query = int(normalized) if normalized.isdigit() else None
    prefer_file_number = normalized.startswith("0") and len(normalized) > 1
    matches: list[OperationTemplate] = []
    for operation in operations:
        if numeric_query is not None:
            if prefer_file_number and operation.file_number == numeric_query:
                matches.append(operation)
                continue
            if not prefer_file_number and operation.index == numeric_query:
                matches.append(operation)
                continue
            if not prefer_file_number and operation.file_number == numeric_query:
                matches.append(operation)
                continue
        if normalized in operation.filename.lower() or normalized in operation.title.lower():
            matches.append(operation)
    return matches


def resolve_operation_selection(
    operations: list[OperationTemplate], selection: str
) -> OperationTemplate | None:
    """Resolve a selection by displayed number, filename number, filename, or stem."""

    normalized = selection.strip().lower()
    if not normalized:
        return None

    if normalized.isdigit():
        number = int(normalized)
        if normalized.startswith("0") and len(normalized) > 1:
            for operation in operations:
                if operation.file_number == number:
                    return operation
        for operation in operations:
            if operation.index == number or operation.file_number == number:
                return operation

    for operation in operations:
        filename = operation.filename.lower()
        if normalized == filename or normalized == operation.path.stem.lower():
            return operation
    return None


def validate_variable_value(variable: InputVariable, value: str) -> str | None:
    """Return a validation error for common variable shapes, or ``None``."""

    stripped = value.strip()
    if variable.required and not stripped:
        return f"{variable.name} is required."
    if not stripped:
        return None
    if SECRET_LOOKING_PATTERN.search(stripped):
        return f"{variable.name} looks like a secret and cannot be written to a prompt artifact."

    choices = placeholder_choices(variable.placeholder)
    if choices is not None and stripped not in choices:
        return f"{variable.name} must be one of: {', '.join(choices)}."

    if is_issue_or_pr_number(variable.name) and not POSITIVE_NUMBER_PATTERN.fullmatch(stripped):
        return f"{variable.name} must be a positive issue/PR number, optionally prefixed with #."

    if is_repository_variable(variable.name) and not REPOSITORY_PATTERN.fullmatch(stripped):
        return f"{variable.name} must look like owner/name."

    if is_positive_limit_variable(variable.name) and not re.fullmatch(r"[1-9][0-9]*", stripped):
        return f"{variable.name} must be a positive integer."

    return None


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


def render_prompt(operation: OperationTemplate, values: dict[str, str]) -> str:
    """Render the filled local prompt artifact."""

    lines = [
        f"# Generated Operation Prompt: {operation.title}",
        "",
        f"Source template: {operation.filename}",
        "",
        "This local artifact fills INPUT values only. It does not execute the operation,",
        "call GitHub/git/network services, or grant authorization.",
        "",
        "## Filled INPUT",
        "",
        "```text",
        *filled_input_lines(operation, values),
        "```",
        "",
        "## Operation Template",
        "",
        operation.text.rstrip(),
        "",
    ]
    return "\n".join(lines)


def filled_input_lines(operation: OperationTemplate, values: dict[str, str]) -> list[str]:
    """Format filled variables as a reusable ``INPUT:`` block."""

    if not operation.variables:
        return ["  (none)"]

    lines: list[str] = []
    for variable in operation.variables:
        value = values.get(variable.name, "").strip()
        if value:
            lines.append(f"  {variable.name}={single_line(value)}")
        elif variable.required:
            lines.append(f"  {variable.name}=")
        else:
            lines.append(f"  {variable.name}=(optional skipped)")
    return lines


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


def display_operations(operations: list[OperationTemplate], output_stream: TextIO) -> None:
    """Print an ordered numbered operation list."""

    print("", file=output_stream)
    print("Available operations:", file=output_stream)
    for operation in operations:
        print(
            f"  {operation.index:>2}. {operation.filename} - {operation.title}",
            file=output_stream,
        )


def select_operation(
    operations: list[OperationTemplate],
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> OperationTemplate | None:
    """Interactively search/filter and select one operation."""

    filtered = list(operations)
    while True:
        display_operations(filtered, output_stream)
        query = input_func(
            "\nSearch by number, filename, or title "
            "(Enter to keep list, / to reset, q to quit): "
        ).strip()
        if query.lower() in {"q", "quit", "exit"}:
            return None
        if query == "/":
            filtered = list(operations)
            continue
        if query:
            matches = filter_operations(operations, query)
            if not matches:
                print("No matching operations.", file=output_stream)
                continue
            filtered = matches
            display_operations(filtered, output_stream)

        selection = input_func("Select operation by listed number or filename (s to search again): ").strip()
        if selection.lower() in {"s", "search"}:
            continue
        if selection.lower() in {"q", "quit", "exit"}:
            return None
        operation = resolve_operation_selection(filtered, selection)
        if operation is not None:
            return operation
        print("Invalid selection.", file=output_stream)


def collect_values(
    operation: OperationTemplate,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> dict[str, str]:
    """Prompt for required and optional variable values with validation."""

    values: dict[str, str] = {}
    if not operation.variables:
        print("This operation declares no INPUT variables.", file=output_stream)
        return values

    print("", file=output_stream)
    print("Fill INPUT variables. Optional values may be left blank.", file=output_stream)
    for variable in operation.variables:
        label = "required" if variable.required else "optional"
        while True:
            raw_value = input_func(f"{variable.name} ({label}, {variable.placeholder}): ")
            value = raw_value.strip()
            error = validate_variable_value(variable, value)
            if error is None:
                values[variable.name] = value
                break
            print(f"Invalid value: {error}", file=output_stream)
    return values


def confirm_write(
    rendered_prompt: str,
    output_path: Path,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> bool:
    """Show a preview and ask before writing the generated prompt."""

    print("", file=output_stream)
    print("Preview:", file=output_stream)
    print("=" * 72, file=output_stream)
    print(rendered_prompt.rstrip(), file=output_stream)
    print("=" * 72, file=output_stream)
    answer = input_func(f"Write this prompt to {output_path}? [y/N]: ").strip().lower()
    if answer not in {"y", "yes"}:
        return False
    if output_path.exists():
        overwrite = input_func(f"{output_path} exists. Overwrite? [y/N]: ").strip().lower()
        return overwrite in {"y", "yes"}
    return True


def write_prompt(output_path: Path, rendered_prompt: str) -> Path:
    """Write the prompt artifact after confirmation."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_prompt, encoding="utf-8")
    return output_path


def run_wizard(
    operations_dir: Path = DEFAULT_OPERATIONS_DIR,
    output_dir: Path | None = None,
    input_func: Callable[[str], str] = input,
    output_stream: TextIO = sys.stdout,
) -> Path | None:
    """Run the interactive operation prompt wizard."""

    operations = discover_operations(operations_dir)
    operation = select_operation(operations, input_func=input_func, output_stream=output_stream)
    if operation is None:
        print("Cancelled before operation selection.", file=output_stream)
        return None

    values = collect_values(operation, input_func=input_func, output_stream=output_stream)
    rendered = render_prompt(operation, values)
    output_directory = resolve_output_dir(output_dir)
    output_path = output_directory / generated_filename(operation, rendered)

    if not confirm_write(rendered, output_path, input_func=input_func, output_stream=output_stream):
        print("Cancelled before write. No file was created.", file=output_stream)
        return None

    path = write_prompt(output_path, rendered)
    print(f"Wrote generated prompt: {path}", file=output_stream)
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--operations-dir",
        type=Path,
        default=DEFAULT_OPERATIONS_DIR,
        help="Directory containing operation .md templates.",
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
