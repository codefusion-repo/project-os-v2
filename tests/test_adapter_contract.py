"""Semantic guards for the compact self and target adapter contract."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_FIELDS = (
    "PROJECT_NAME",
    "REPOSITORY_NAME",
    "REPOSITORY_LOCAL_PATH",
    "DEFAULT_BRANCH",
    "WORK_BRANCH_PATTERN",
    "PM_FACING_LANGUAGE",
    "KERNEL_REPOSITORY",
    "KERNEL_LOCAL_PATH",
    "KERNEL_VERSION_ADOPTED",
)
MAIN_BOOTLOADERS = (
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "project-os-es/adapters/AGENTS.target.md",
    REPO_ROOT / "project-os-es/adapters/BROWSER_CHAT.target.md",
)
SHIMS = (
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "GEMINI.md",
    REPO_ROOT / "project-os-es/adapters/CLAUDE.target.md",
    REPO_ROOT / "project-os-es/adapters/GEMINI.target.md",
)


def metadata_fields(path: Path) -> list[str]:
    return [
        match.group(1)
        for match in re.finditer(r"^([A-Z][A-Z0-9_]*)\s*=", path.read_text(encoding="utf-8"), re.M)
        if match.group(1) in METADATA_FIELDS
    ]


def test_main_adapters_share_the_standard_metadata_block_in_order() -> None:
    for path in MAIN_BOOTLOADERS:
        assert metadata_fields(path) == list(METADATA_FIELDS), path


def test_agents_is_the_only_complete_terminal_bootloader() -> None:
    self_adapter = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    target_adapter = (REPO_ROOT / "project-os-es/adapters/AGENTS.target.md").read_text(encoding="utf-8")

    for text in (self_adapter, target_adapter):
        assert "project-os-es/kernel/manifest.json" in text
        assert "tools/project_os_resolve.py" in text
        assert "nunca autorizan" in text
        assert "Evidencia viva" in text

    for path in SHIMS:
        text = path.read_text(encoding="utf-8")
        assert "AGENTS.md" in text
        assert metadata_fields(path) == []
        assert "tools/project_os_resolve.py" not in text
        assert "--actor" not in text


def test_target_terminal_adapter_uses_only_portable_allowlisted_path_references() -> None:
    target_adapter = (REPO_ROOT / "project-os-es/adapters/AGENTS.target.md").read_text(
        encoding="utf-8"
    )

    assert "REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT" in target_adapter
    assert "KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR" in target_adapter
    assert "$PWD" not in target_adapter
    assert 'python "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py"' in target_adapter
    assert "tools/project_os_resolve.py" in target_adapter
    assert "select_target_bootloader" not in target_adapter


def test_no_consumer_reimplements_the_upward_agents_search() -> None:
    consumers = (
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "project-os-es/adapters/AGENTS.target.md",
        REPO_ROOT / "project-os-en/adapters/AGENTS.target.md",
        REPO_ROOT / "project-os-es/docs/empezar.md",
        REPO_ROOT / "project-os-en/docs/getting-started.md",
    )
    for path in consumers:
        text = path.read_text(encoding="utf-8")
        assert "select_target_bootloader" not in text, path
        assert "KERNEL_REF=$(sed" not in text, path
        assert "while test" not in text, path
        assert 'python "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py"' in text, path


def test_terminal_bootloaders_exclude_internal_fast_path_debugging_details() -> None:
    bootloaders = (
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "project-os-es/adapters/AGENTS.target.md",
        REPO_ROOT / "project-os-en/adapters/AGENTS.target.md",
    )
    internal_details = (
        "--agents-file",
        "111",
        "select_target_bootloader",
        "KERNEL_REF=$(sed",
        "while test",
    )
    for path in bootloaders:
        text = path.read_text(encoding="utf-8")
        assert not any(detail in text for detail in internal_details), path


def test_browser_adapter_keeps_its_read_only_manual_resolution_boundary() -> None:
    browser = (REPO_ROOT / "project-os-es/adapters/BROWSER_CHAT.target.md").read_text(encoding="utf-8")

    assert "read-only" in browser
    assert "draft-only" in browser
    assert "no ejecuta\nPython local" in browser
    assert "status.needs_context" in browser
    assert "project-os-es/templates/pm-command-bundle.md" in browser
    assert "tools/project_os_resolve.py" not in browser


def test_adapters_reserve_target_owned_constraints_without_kernel_contracts() -> None:
    self_adapter = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    target_adapter = (REPO_ROOT / "project-os-es/adapters/AGENTS.target.md").read_text(encoding="utf-8")
    browser = (REPO_ROOT / "project-os-es/adapters/BROWSER_CHAT.target.md").read_text(encoding="utf-8")

    assert "Notas propias del repositorio" in self_adapter
    assert "Notas propias del target" in target_adapter
    assert "Notas propias del target" in browser
    assert "## Outputs y artefactos" not in target_adapter
    assert "## Seguridad y validacion" not in target_adapter


def test_spanish_adapters_do_not_cross_surfaces_and_forbid_live_state() -> None:
    cross_surface_or_removed_references = ("project-os-en", "project-os-es/" + "tools/resolver.py")
    sha_pattern = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
    adapter_paths = [*MAIN_BOOTLOADERS, *SHIMS, REPO_ROOT / "project-os-es/adapters/README.md"]

    for path in adapter_paths:
        text = path.read_text(encoding="utf-8")
        assert not any(reference in text for reference in cross_surface_or_removed_references), path
        assert not sha_pattern.search(text), path
        assert "estado vivo" in text, path
