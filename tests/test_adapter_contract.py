"""Semantic guards for the compact self and target adapter contract."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import pytest


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


def resolver_fast_path(surface: str, source_kind: str) -> str:
    relative_path = {
        ("project-os-es", "adapter"): "adapters/AGENTS.target.md",
        ("project-os-es", "docs"): "docs/empezar.md",
        ("project-os-en", "adapter"): "adapters/AGENTS.target.md",
        ("project-os-en", "docs"): "docs/getting-started.md",
    }[(surface, source_kind)]
    source = (REPO_ROOT / surface / relative_path).read_text(
        encoding="utf-8"
    )
    blocks = re.findall(r"```sh\n(.*?)\n```", source, re.S)
    block = next(item for item in blocks if "TARGET_REF=$(sed" in item)
    return (
        block.replace("<actor>", "actor.browser_chat")
        .replace("<workflow>", "workflow.pm_intake")
        .replace("<mode>", "mode.review_only")
        .replace(" [--skill skill.<id>]", "")
    )


def write_fast_path_kernel(
    root: Path,
    surface: str,
    language: str,
    *,
    manifest_text: str | None = None,
    with_manifest: bool = True,
    with_resolver: bool = True,
) -> Path:
    kernel = root / surface / "kernel"
    kernel.mkdir(parents=True)
    if with_manifest:
        payload = manifest_text
        if payload is None:
            payload = json.dumps(
                {
                    "manifest": [
                        {
                            "key": "manifest.kernel_es",
                            "language": language,
                            "active": True,
                        }
                    ]
                }
            )
        (kernel / "manifest.json").write_text(payload, encoding="utf-8")
    if with_resolver:
        resolver = root / "tools" / "project_os_resolve.py"
        resolver.parent.mkdir(parents=True)
        resolver.write_text(
            "import os\nfrom pathlib import Path\n"
            "Path(os.environ['RESOLVER_SENTINEL']).touch()\n",
            encoding="utf-8",
        )
    return kernel


def run_resolver_fast_path(
    target: Path,
    surface: str,
    source_kind: str,
    target_ref: str,
    kernel_ref: str,
    *,
    target_variable: str | None = None,
    kernel_variable: str | None = None,
) -> tuple[subprocess.CompletedProcess[str], Path]:
    (target / "AGENTS.md").write_text(
        f"REPOSITORY_LOCAL_PATH = {target_ref}\nKERNEL_LOCAL_PATH = {kernel_ref}\n",
        encoding="utf-8",
    )
    sentinel = target / "resolver-invoked"
    env = os.environ.copy()
    env.pop("PROJECT_OS_TARGET_ROOT", None)
    env.pop("PROJECT_OS_KERNEL_DIR", None)
    if target_variable is not None:
        env["PROJECT_OS_TARGET_ROOT"] = target_variable
    if kernel_variable is not None:
        env["PROJECT_OS_KERNEL_DIR"] = kernel_variable
    env["RESOLVER_SENTINEL"] = str(sentinel)
    result = subprocess.run(
        ["sh", "-c", resolver_fast_path(surface, source_kind)],
        cwd=target,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    return result, sentinel


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
    assert "eval" in target_adapter
    assert "no usa `eval`" in target_adapter
    assert 'python "$PROJECT_OS_ROOT/tools/project_os_resolve.py"' in target_adapter


@pytest.mark.parametrize(
    ("surface", "language"),
    (("project-os-es", "es"), ("project-os-en", "en")),
)
@pytest.mark.parametrize("source_kind", ("adapter", "docs"))
@pytest.mark.parametrize("reference_mode", ("portable", "literal"))
def test_resolver_fast_path_supports_portable_and_literal_paths(
    tmp_path: Path,
    surface: str,
    language: str,
    source_kind: str,
    reference_mode: str,
) -> None:
    target = tmp_path / "target"
    target.mkdir()
    kernel = write_fast_path_kernel(tmp_path / "project-os", surface, language)
    if reference_mode == "portable":
        result, sentinel = run_resolver_fast_path(
            target,
            surface,
            source_kind,
            "$PROJECT_OS_TARGET_ROOT",
            "$PROJECT_OS_KERNEL_DIR",
            target_variable=str(target),
            kernel_variable=str(kernel),
        )
    else:
        result, sentinel = run_resolver_fast_path(
            target,
            surface,
            source_kind,
            str(target),
            str(kernel),
        )

    assert result.returncode == 0
    assert sentinel.is_file()


@pytest.mark.parametrize(
    ("surface", "language"),
    (("project-os-es", "es"), ("project-os-en", "en")),
)
@pytest.mark.parametrize("source_kind", ("adapter", "docs"))
@pytest.mark.parametrize(
    "invalid_kernel",
    ("wrong-surface", "missing-manifest", "invalid-manifest", "wrong-identity", "invalid-root"),
)
def test_resolver_fast_path_never_invokes_lure_before_invalid_kernel_preconditions(
    tmp_path: Path,
    surface: str,
    language: str,
    source_kind: str,
    invalid_kernel: str,
) -> None:
    target = tmp_path / "target"
    target.mkdir()
    root = tmp_path / "project-os"
    if invalid_kernel == "wrong-surface":
        kernel = write_fast_path_kernel(root, "unexpected-surface", language)
    elif invalid_kernel == "missing-manifest":
        kernel = write_fast_path_kernel(root, surface, language, with_manifest=False)
    elif invalid_kernel == "invalid-manifest":
        kernel = write_fast_path_kernel(root, surface, language, manifest_text="{")
    elif invalid_kernel == "wrong-identity":
        opposite = "en" if language == "es" else "es"
        kernel = write_fast_path_kernel(root, surface, opposite)
    else:
        kernel = Path(f"/{surface}/kernel")

    result, sentinel = run_resolver_fast_path(
        target,
        surface,
        source_kind,
        "$PROJECT_OS_TARGET_ROOT",
        "$PROJECT_OS_KERNEL_DIR",
        target_variable=str(target),
        kernel_variable=str(kernel),
    )

    assert result.returncode != 0
    assert not sentinel.exists()


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
