"""Single executable source for the terminal fast path (issue #487, OSIM.5).

Bootloaders, adapters, and docs used to each carry a full copy of the upward
``AGENTS.md`` search plus its defensive validation. This module is that one
executable source, used two ways:

- ``--start-dir DIR`` (the short daily command): walk up from ``DIR`` fully
  internally and, on the first coherent candidate, invoke
  ``tools/project_os_resolve.py`` exactly once and return its exit code
  unchanged. Fail closed with exit ``1`` and no resolver invocation when no
  ancestor validates.
- ``--agents-file PATH`` (one step of the debugging-reference shell loop):
  validate exactly that one candidate. An incoherent candidate returns
  ``NOT_A_CANDIDATE`` so the caller's own loop keeps walking up and lands the
  ``cd`` continuation on the same directory this module accepted, instead of
  each side re-deriving the target independently and risking disagreement. A
  coherent candidate invokes the resolver exactly once and returns its exit
  code unchanged.

This performs no network or git access, grants no permission, and is not a
trust anchor: it only proves local structural coherence, the same scope the
retired inline block covered.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

try:
    from tools.project_os_surfaces import SURFACES
except ModuleNotFoundError:  # Direct ``python tools/project_os_fast_path.py`` execution.
    from project_os_surfaces import SURFACES  # type: ignore[no-redef]

# Distinct from every real exit code project_os_resolve.py can produce (0, 1,
# or 2 on an unexpected internal error), so a per-candidate caller can tell
# "not a coherent candidate, keep walking" apart from a real resolver verdict.
NOT_A_CANDIDATE = 111

_TARGET_ENV_VAR = "PROJECT_OS_TARGET_ROOT"
_KERNEL_ENV_VAR = "PROJECT_OS_KERNEL_DIR"
_KERNEL_SUFFIX_LANGUAGE = {surface.root_name: surface.language for surface in SURFACES}


class _Candidate(NamedTuple):
    target_root: Path
    kernel_dir: Path


def _field(text: str, name: str) -> str | None:
    match = re.search(rf"^{name}[ \t]*=[ \t]*(.*)$", text, re.M)
    return match.group(1).strip() if match else None


def _resolve_reference(value: str | None, env_var: str, environ: dict[str, str]) -> str | None:
    """Accept only the exact portable reference or an absolute literal.

    Mirrors the retired shell ``case`` statement: no ``eval``, no expansion of
    arbitrary names, and a literal containing ``$`` is rejected rather than
    partially interpreted.
    """

    if value is None:
        return None
    if value in (f"${env_var}", f"${{{env_var}}}"):
        resolved = environ.get(env_var)
        return resolved or None
    if value.startswith("/") and "$" not in value:
        return value
    return None


def _manifest_is_active_and_coherent(manifest_path: Path, language: str) -> bool:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return False
    entries = payload.get("manifest") if isinstance(payload, dict) else None
    return (
        isinstance(entries, list)
        and len(entries) == 1
        and isinstance(entries[0], dict)
        and entries[0].get("key") == "manifest.kernel_es"
        and entries[0].get("language") == language
        and entries[0].get("active") is True
    )


def validate_candidate(
    agents_file: Path, environ: dict[str, str] | None = None
) -> _Candidate | None:
    """Validate one ``AGENTS.md`` candidate without invoking the resolver.

    Returns the resolved ``(target_root, kernel_dir)`` pair only when every
    structural check passes; otherwise ``None`` so the caller keeps walking
    up. These checks are structural and demonstrable, not a trust anchor: a
    local directory reproducing this shape remains executable.
    """

    environ = environ if environ is not None else dict(os.environ)
    try:
        text = agents_file.read_text(encoding="utf-8")
    except OSError:
        return None

    target_value = _resolve_reference(_field(text, "REPOSITORY_LOCAL_PATH"), _TARGET_ENV_VAR, environ)
    kernel_value = _resolve_reference(_field(text, "KERNEL_LOCAL_PATH"), _KERNEL_ENV_VAR, environ)
    if target_value is None or kernel_value is None:
        return None

    target_root = Path(target_value)
    kernel_dir = Path(kernel_value)
    if not target_root.is_absolute() or not kernel_dir.is_absolute():
        return None
    if not target_root.is_dir():
        return None
    try:
        if not agents_file.samefile(target_root / "AGENTS.md"):
            return None
    except OSError:
        return None

    if len(kernel_dir.parts) < 2 or kernel_dir.parts[-1] != "kernel":
        return None
    language = _KERNEL_SUFFIX_LANGUAGE.get(kernel_dir.parts[-2])
    if language is None:
        return None

    manifest_path = kernel_dir / "manifest.json"
    if not manifest_path.is_file():
        return None
    if not _manifest_is_active_and_coherent(manifest_path, language):
        return None

    project_os_root = kernel_dir.parent.parent
    if not (project_os_root / "tools" / "project_os_resolve.py").is_file():
        return None

    return _Candidate(target_root=target_root, kernel_dir=kernel_dir)


def locate_target(start_dir: Path, environ: dict[str, str] | None = None) -> _Candidate | None:
    """Walk up from ``start_dir``, skipping any incoherent intermediate ``AGENTS.md``."""

    probe = start_dir.resolve()
    while True:
        candidate_file = probe / "AGENTS.md"
        if candidate_file.is_file():
            candidate = validate_candidate(candidate_file, environ)
            if candidate is not None:
                return candidate
        parent = probe.parent
        if parent == probe:
            return None
        probe = parent


def _invoke_resolver(candidate: _Candidate, args: argparse.Namespace) -> int:
    resolver_path = candidate.kernel_dir.parent.parent / "tools" / "project_os_resolve.py"
    resolver_argv = [
        sys.executable,
        str(resolver_path),
        "--actor",
        args.actor,
        "--workflow",
        args.workflow,
        "--kernel-dir",
        str(candidate.kernel_dir),
    ]
    if args.mode is not None:
        resolver_argv += ["--mode", args.mode]
    if args.change_class is not None:
        resolver_argv += ["--change-class", args.change_class]
    for skill in args.skill or []:
        resolver_argv += ["--skill", skill]
    if args.hydration_level is not None:
        resolver_argv += ["--hydration-level", args.hydration_level]
    if args.compact:
        resolver_argv.append("--compact")
    completed = subprocess.run(resolver_argv, check=False)
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Terminal fast path: locate and validate the root AGENTS.md, then "
            "invoke tools/project_os_resolve.py exactly once."
        )
    )
    location = parser.add_mutually_exclusive_group()
    location.add_argument(
        "--start-dir",
        default=None,
        help="walk up from this directory (default: cwd) and dispatch on the first coherent candidate",
    )
    location.add_argument(
        "--agents-file",
        default=None,
        help=(
            "validate exactly this one AGENTS.md candidate; exits with "
            f"{NOT_A_CANDIDATE} when it is not coherent, for a caller-driven "
            "upward loop"
        ),
    )
    parser.add_argument("--actor", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--mode", default=None)
    parser.add_argument("--change-class", default=None, metavar="CLASS")
    parser.add_argument("--skill", action="append", default=None)
    parser.add_argument("--hydration-level", default=None, metavar="LEVEL")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args(argv)

    if args.agents_file is not None:
        candidate = validate_candidate(Path(args.agents_file))
        if candidate is None:
            return NOT_A_CANDIDATE
        return _invoke_resolver(candidate, args)

    start_dir = Path(args.start_dir) if args.start_dir else Path.cwd()
    candidate = locate_target(start_dir)
    if candidate is None:
        print(
            "sin AGENTS.md raiz coherente con el target adoptado / "
            "no root AGENTS.md coherent with the adopted target",
            file=sys.stderr,
        )
        return 1
    return _invoke_resolver(candidate, args)


if __name__ == "__main__":
    raise SystemExit(main())
