"""Small, explicit filesystem boundary for generated wizard artifacts."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from tools.operation_prompt_wizard_core import (
    GENERATED_FILENAME_PATTERN,
    WIZARD_PROMPT_MARKER,
    WizardError,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = REPO_ROOT / ".local" / "operation-prompts"
OUTPUT_DIR_ENV = "PROJECT_OS_OPERATION_PROMPT_OUTPUT_DIR"


def resolve_output_dir(output_dir: Path | None) -> Path:
    """Resolve explicit, configured, or default output directory."""

    if output_dir is not None:
        return output_dir.expanduser()
    configured = os.environ.get(OUTPUT_DIR_ENV)
    if configured:
        return Path(configured).expanduser()
    return DEFAULT_OUTPUT_DIR


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


def _resolved_output_dir(output_dir: Path) -> Path:
    return output_dir.expanduser().resolve()


def _ensure_output_child(output_dir: Path, path: Path) -> None:
    if path.resolve().parent != _resolved_output_dir(output_dir):
        raise WizardError("generated prompt paths must be direct children of the resolved output directory")


def find_replaceable_prompts(output_dir: Path, output_path: Path) -> list[Path]:
    """Return every previous wizard-generated prompt a new write would replace.

    May be more than one file, since cleanup_previous_generated_prompts()
    removes all matches other than the new output path; the pre-write notice
    must name all of them, not just the first, so it never understates what
    the write is about to delete.
    """

    _ensure_output_child(output_dir, output_path)
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

    _ensure_output_child(output_dir, keep_path)
    keep_resolved = keep_path.resolve()
    removed: list[Path] = []
    for existing in find_existing_generated_prompts(output_dir):
        if existing.resolve() == keep_resolved:
            continue
        existing.unlink()
        removed.append(existing)
    return removed


def write_prompt(output_path: Path, rendered_prompt: str) -> Path:
    """Atomically write one marked prompt artifact inside its selected folder."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = rendered_prompt if rendered_prompt.endswith("\n") else rendered_prompt + "\n"
    content += WIZARD_PROMPT_MARKER + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.", suffix=".tmp", dir=output_path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, output_path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise
    return output_path
