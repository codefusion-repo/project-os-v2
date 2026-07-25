"""Repository-shape, path, durable-state, and secret-safety guards."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SECRET_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def active_files() -> list[Path]:
    roots = [
        REPO_ROOT / "project-os-es",
        REPO_ROOT / "project-os-en",
        REPO_ROOT / "tools",
        REPO_ROOT / "tests",
        REPO_ROOT / "dogfooding",
        REPO_ROOT / "README.md",
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "GEMINI.md",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        else:
            files.extend(path for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    return files


def test_single_resolver_and_two_allowed_language_surfaces() -> None:
    assert (REPO_ROOT / "tools/project_os_resolve.py").is_file()
    assert not (REPO_ROOT / "project-os-es" / "tools" / "resolver.py").exists()
    assert (REPO_ROOT / "project-os-en/kernel/manifest.json").is_file()
    assert not (REPO_ROOT / "project-os-en/tools").exists()


def test_active_markdown_relative_links_resolve() -> None:
    missing: list[str] = []
    markdown_files = [
        REPO_ROOT / "README.md",
        *sorted((REPO_ROOT / "project-os-es").rglob("*.md")),
        *sorted((REPO_ROOT / "project-os-en").rglob("*.md")),
    ]
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
            target = raw_target.strip().split()[0].strip("<>").split("#", 1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")) or "{{" in target:
                continue
            candidate = (
                REPO_ROOT / target
                if target.startswith(("project-os-es/", "project-os-en/"))
                else source.parent / target
            )
            if not candidate.resolve().exists():
                missing.append(f"{source.relative_to(REPO_ROOT)} -> {raw_target}")
    assert missing == []


def test_portable_surfaces_never_depend_on_the_dogfooding_surface() -> None:
    """Core tooling, core tests, and both language surfaces stay dogfooding-free.

    A target adopts ``project-os-es``/``project-os-en`` plus ``tools/``; nothing
    there may import from or point into ``dogfooding/``, which owns only the
    maintenance surface of ``project-os-v2`` itself.
    """
    dependency_pattern = re.compile(
        r"from dogfooding\b|import dogfooding\b|dogfooding/[A-Za-z]|dogfooding\.(?:tools|tests|docs)\b"
    )
    hits: list[str] = []
    portable_roots = (
        REPO_ROOT / "tools",
        REPO_ROOT / "tests",
        REPO_ROOT / "project-os-es",
        REPO_ROOT / "project-os-en",
        REPO_ROOT / "AGENTS.md",
    )
    for root in portable_roots:
        paths = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in paths:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            if path.suffix not in {".py", ".md", ".json", ".yml", ".yaml"}:
                continue
            if dependency_pattern.search(path.read_text(encoding="utf-8")):
                hits.append(str(path.relative_to(REPO_ROOT)))
    assert hits == []


def test_active_surface_has_no_secret_values_or_durable_commit_state() -> None:
    secret_hits: list[str] = []
    sha_hits: list[str] = []
    sha_pattern = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
    for path in active_files():
        if path.suffix not in {".md", ".py", ".json", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        if SECRET_PATTERN.search(text):
            secret_hits.append(str(path.relative_to(REPO_ROOT)))
        if any(root in str(path) for root in ("project-os-es/kernel", "project-os-en/kernel")) and sha_pattern.search(text):
            sha_hits.append(str(path.relative_to(REPO_ROOT)))
    assert secret_hits == []
    assert sha_hits == []


def test_active_pm_command_bundle_preserves_copy_safe_shell_contract() -> None:
    """The bundle commands are PM-executed shell; guard the copy-safe patterns only."""
    assert not (REPO_ROOT / "templates/pm-command-bundle.md").exists()
    for template_path in (
        REPO_ROOT / "project-os-es/templates/pm-command-bundle.md",
        REPO_ROOT / "project-os-en/templates/pm-command-bundle.md",
    ):
        template = template_path.read_text(encoding="utf-8")
        assert "```sh" in template or "```bash" in template
        assert "--body-file" in template
        assert "<<'PR_COMMENT_END'" in template
        assert "--match-head-commit <reviewed-head-sha>" in template
        assert "gh pr view <pr-number> --repo <owner/repo> --json state,mergedAt,headRefOid" in template
