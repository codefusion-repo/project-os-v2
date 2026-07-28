"""Direct unit and end-to-end coverage for the terminal fast path (issue #487).

These tests exercise ``tools/project_os_fast_path.py`` as real, importable
Python -- not by extracting and running shell text -- so parsing, allowlists,
identity checks, and the exactly-once resolver dispatch are protected by
ordinary pytest assertions. ``tests/test_adapter_contract.py`` only checks
that the five documented consumers stay thin pass-throughs to this module.

Subprocess cases that walk the real repository's ``AGENTS.md`` (which uses
the portable ``$PROJECT_OS_TARGET_ROOT`` / ``$PROJECT_OS_KERNEL_DIR``
references) set those two variables explicitly via ``_repo_env`` instead of
inheriting whatever a developer's shell happens to export, so the same
assertions hold on a clean CI runner.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tools.project_os_fast_path import NOT_A_CANDIDATE, locate_target, main, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_KERNEL_DIR = REPO_ROOT / "project-os-es" / "kernel"


def _repo_env(**overrides: str) -> dict[str, str]:
    """A hermetic subprocess environment for real-repository fast-path runs.

    Explicitly sets the two portable references to this checkout's own
    absolute paths -- never inferred or left to inheritance -- so these tests
    fail closed the same way on a developer machine and on a clean CI runner.
    """

    env = {
        "PROJECT_OS_TARGET_ROOT": str(REPO_ROOT),
        "PROJECT_OS_KERNEL_DIR": str(REPO_KERNEL_DIR),
    }
    env.update(overrides)
    return env


def _write_manifest(kernel_dir: Path, *, language: str, active: bool = True, key: str = "manifest.kernel_es") -> None:
    kernel_dir.mkdir(parents=True, exist_ok=True)
    payload = {"manifest": [{"key": key, "language": language, "active": active}]}
    (kernel_dir / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")


def _write_resolver_stub(project_os_root: Path) -> None:
    tools_dir = project_os_root / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    (tools_dir / "project_os_resolve.py").write_text("raise SystemExit(0)\n", encoding="utf-8")


def _coherent_target(tmp_path: Path, *, surface: str = "project-os-es", language: str = "es") -> tuple[Path, Path]:
    project_os_root = tmp_path / "project-os"
    kernel_dir = project_os_root / surface / "kernel"
    _write_manifest(kernel_dir, language=language)
    _write_resolver_stub(project_os_root)
    target = tmp_path / "target"
    target.mkdir()
    (target / "AGENTS.md").write_text(
        f"REPOSITORY_LOCAL_PATH = {target}\nKERNEL_LOCAL_PATH = {kernel_dir}\n",
        encoding="utf-8",
    )
    return target, kernel_dir


# --- validate_candidate ------------------------------------------------


def test_validate_candidate_accepts_a_fully_coherent_literal_target(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)

    result = validate_candidate(target / "AGENTS.md", environ={})

    assert result is not None
    assert result.target_root == target
    assert result.kernel_dir == kernel_dir


def test_validate_candidate_accepts_portable_references(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    (target / "AGENTS.md").write_text(
        "REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT\n"
        "KERNEL_LOCAL_PATH = ${PROJECT_OS_KERNEL_DIR}\n",
        encoding="utf-8",
    )
    environ = {"PROJECT_OS_TARGET_ROOT": str(target), "PROJECT_OS_KERNEL_DIR": str(kernel_dir)}

    result = validate_candidate(target / "AGENTS.md", environ=environ)

    assert result == (target, kernel_dir)


def test_validate_candidate_rejects_unset_portable_variable(tmp_path: Path) -> None:
    target, _kernel_dir = _coherent_target(tmp_path)
    (target / "AGENTS.md").write_text(
        "REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT\nKERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR\n",
        encoding="utf-8",
    )

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_a_literal_containing_a_dollar_sign(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    (target / "AGENTS.md").write_text(
        f"REPOSITORY_LOCAL_PATH = {target}$(whoami)\nKERNEL_LOCAL_PATH = {kernel_dir}\n",
        encoding="utf-8",
    )

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_a_relative_reference(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    (target / "AGENTS.md").write_text(
        f"REPOSITORY_LOCAL_PATH = ./relative\nKERNEL_LOCAL_PATH = {kernel_dir}\n",
        encoding="utf-8",
    )

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_an_agents_file_that_names_another_directory(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    (foreign / "AGENTS.md").write_text(
        f"REPOSITORY_LOCAL_PATH = {target}\nKERNEL_LOCAL_PATH = {kernel_dir}\n",
        encoding="utf-8",
    )

    assert validate_candidate(foreign / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_a_kernel_dir_outside_the_language_allowlist(tmp_path: Path) -> None:
    target, _kernel_dir = _coherent_target(tmp_path, surface="unexpected-surface", language="es")

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_a_manifest_language_mismatch(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path, surface="project-os-es", language="es")
    _write_manifest(kernel_dir, language="en")

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_an_inactive_manifest(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    _write_manifest(kernel_dir, language="es", active=False)

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_a_missing_resolver_file(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    (kernel_dir.parent.parent / "tools" / "project_os_resolve.py").unlink()

    assert validate_candidate(target / "AGENTS.md", environ={}) is None


def test_validate_candidate_rejects_a_missing_target_directory(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    agents_file = target / "AGENTS.md"
    text = agents_file.read_text(encoding="utf-8")
    missing = tmp_path / "does-not-exist"
    agents_file.write_text(text.replace(str(target), str(missing)), encoding="utf-8")

    assert validate_candidate(agents_file, environ={}) is None


# --- locate_target -------------------------------------------------------


def test_locate_target_walks_up_from_a_nested_subdirectory(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    nested = target / "docs" / "decisions"
    nested.mkdir(parents=True)

    assert locate_target(nested, environ={}) == (target, kernel_dir)


def test_locate_target_skips_an_incoherent_intermediate_agents_file(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    component = target / "packages" / "component"
    nested = component / "src"
    nested.mkdir(parents=True)
    (component / "AGENTS.md").write_text("# component notes\n", encoding="utf-8")

    assert locate_target(nested, environ={}) == (target, kernel_dir)


def test_locate_target_returns_none_when_no_ancestor_is_coherent(tmp_path: Path) -> None:
    lonely = tmp_path / "lonely"
    lonely.mkdir()

    assert locate_target(lonely, environ={}) is None


# --- main(): exactly-once dispatch and exit code propagation -------------


def test_main_dispatches_to_the_real_repository_resolver_and_matches_it() -> None:
    direct = subprocess.run(
        [
            sys.executable,
            "tools/project_os_resolve.py",
            "--actor",
            "actor.terminal_agent",
            "--workflow",
            "workflow.issue_implementation",
            "--mode",
            "mode.delegated_commit_pr",
            "--change-class",
            "change_class.critical",
            "--compact",
        ],
        cwd=REPO_ROOT,
        env=_repo_env(),
        capture_output=True,
        text=True,
        check=False,
    )
    via_fast_path = subprocess.run(
        [
            sys.executable,
            "tools/project_os_fast_path.py",
            "--actor",
            "actor.terminal_agent",
            "--workflow",
            "workflow.issue_implementation",
            "--mode",
            "mode.delegated_commit_pr",
            "--change-class",
            "change_class.critical",
            "--compact",
        ],
        cwd=REPO_ROOT,
        env=_repo_env(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert via_fast_path.returncode == direct.returncode == 0
    assert via_fast_path.stdout == direct.stdout


def test_documented_short_command_runs_from_the_repository_root_and_a_subdirectory() -> None:
    """Run the exact documented invocation, not a test-built script path.

    The daily command is ``python "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py" ...``:
    location-safe because it derives the script's path from the already-known
    kernel reference instead of a path relative to the current directory.
    """

    for cwd in (REPO_ROOT, REPO_ROOT / "docs" / "decisions"):
        completed = subprocess.run(
            [
                "/bin/sh",
                "-c",
                '"$PYTHON" "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py" '
                "--actor actor.browser_chat --workflow workflow.pm_intake "
                "--mode mode.review_only --compact",
            ],
            cwd=cwd,
            env=_repo_env(PYTHON=sys.executable),
            capture_output=True,
            text=True,
            check=False,
        )

        assert completed.returncode == 0
        assert '"estado": "status.resolved"' in completed.stdout


def test_main_runs_from_a_real_subdirectory_of_this_repository() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "project_os_fast_path.py"),
            "--actor",
            "actor.browser_chat",
            "--workflow",
            "workflow.pm_intake",
            "--mode",
            "mode.review_only",
            "--compact",
        ],
        cwd=REPO_ROOT / "docs" / "decisions",
        env=_repo_env(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert '"estado": "status.resolved"' in completed.stdout


def test_main_propagates_a_blocked_resolver_exit_code_and_body() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "tools/project_os_fast_path.py",
            "--actor",
            "actor.no_existe",
            "--workflow",
            "workflow.pm_intake",
            "--mode",
            "mode.review_only",
            "--compact",
        ],
        cwd=REPO_ROOT,
        env=_repo_env(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    assert '"estado": "status.blocked"' in completed.stdout
    assert "actor desconocido" in completed.stdout


def test_main_propagates_an_arbitrary_nonzero_resolver_exit_code_exactly(tmp_path: Path) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    resolver_path = kernel_dir.parent.parent / "tools" / "project_os_resolve.py"
    resolver_path.write_text("raise SystemExit(7)\n", encoding="utf-8")

    exit_code = main(
        [
            "--start-dir",
            str(target),
            "--actor",
            "actor.terminal_agent",
            "--workflow",
            "workflow.issue_implementation",
        ]
    )

    assert exit_code == 7


def test_main_fails_closed_with_no_coherent_ancestor(tmp_path: Path) -> None:
    lonely = tmp_path / "lonely"
    lonely.mkdir()

    assert main(["--start-dir", str(lonely), "--actor", "actor.terminal_agent", "--workflow", "workflow.issue_implementation"]) == 1


# --- main(): --agents-file per-candidate mode ----------------------------


def test_main_agents_file_mode_returns_not_a_candidate_for_an_incoherent_file(tmp_path: Path) -> None:
    lonely = tmp_path / "lonely"
    lonely.mkdir()
    agents_file = lonely / "AGENTS.md"
    agents_file.write_text("# no fields here\n", encoding="utf-8")

    exit_code = main(
        ["--agents-file", str(agents_file), "--actor", "actor.terminal_agent", "--workflow", "workflow.issue_implementation"]
    )

    assert exit_code == NOT_A_CANDIDATE


def test_main_agents_file_mode_dispatches_for_a_coherent_file(tmp_path: Path) -> None:
    target, _kernel_dir = _coherent_target(tmp_path)

    exit_code = main(
        [
            "--agents-file",
            str(target / "AGENTS.md"),
            "--actor",
            "actor.terminal_agent",
            "--workflow",
            "workflow.issue_implementation",
        ]
    )

    assert exit_code == 0


def test_main_agents_file_mode_and_start_dir_are_mutually_exclusive() -> None:
    try:
        main(["--agents-file", "x", "--start-dir", "y", "--actor", "a", "--workflow", "b"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected argparse to reject combining --agents-file and --start-dir")


def test_main_invokes_the_resolver_exactly_once(tmp_path: Path, monkeypatch) -> None:
    target, kernel_dir = _coherent_target(tmp_path)
    resolver_path = kernel_dir.parent.parent / "tools" / "project_os_resolve.py"
    sentinel = tmp_path / "invocations.log"
    resolver_path.write_text(
        "import pathlib, sys\n"
        f"pathlib.Path(r'{sentinel}').open('a').write('invoked\\n')\n"
        "raise SystemExit(0)\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(target)

    exit_code = main(["--actor", "actor.terminal_agent", "--workflow", "workflow.issue_implementation"])

    assert exit_code == 0
    assert sentinel.read_text(encoding="utf-8") == "invoked\n"
