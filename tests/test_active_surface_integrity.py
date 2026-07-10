"""Repository-shape, path, durable-state, and secret-safety guards."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def active_files() -> list[Path]:
    roots = [
        REPO_ROOT / "project-os-es",
        REPO_ROOT / "tools",
        REPO_ROOT / "tests",
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


def test_single_active_resolver_and_nonoperative_future_english_surface() -> None:
    assert (REPO_ROOT / "tools/project_os_resolve.py").is_file()
    assert not (REPO_ROOT / "project-os-es/tools/resolver.py").exists()
    assert not list((REPO_ROOT / "project-os-en").glob("*"))

    tool_sources = "\n".join(path.read_text(encoding="utf-8") for path in (REPO_ROOT / "tools").glob("*.py"))
    assert "DEFAULT_KERNEL_DIR = REPO_ROOT / \"project-os-es\" / \"kernel\"" in tool_sources
    assert "DEFAULT_OPERATIONS_DIR = REPO_ROOT / \"project-os-es\" / \"operaciones\"" in tool_sources
    assert "DEFAULT_KERNEL_DIR = REPO_ROOT / \"legacy-project-os\"" not in tool_sources


def test_active_markdown_relative_links_resolve() -> None:
    missing: list[str] = []
    markdown_files = [REPO_ROOT / "README.md", *sorted((REPO_ROOT / "project-os-es").rglob("*.md"))]
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
            target = raw_target.strip().split()[0].strip("<>").split("#", 1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")) or "{{" in target:
                continue
            candidate = (REPO_ROOT / target) if target.startswith("project-os-es/") else (source.parent / target)
            if not candidate.resolve().exists():
                missing.append(f"{source.relative_to(REPO_ROOT)} -> {raw_target}")
    assert missing == []


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
        if "project-os-es/kernel" in str(path) and sha_pattern.search(text):
            sha_hits.append(str(path.relative_to(REPO_ROOT)))
    assert secret_hits == []
    assert sha_hits == []


def test_wizard_has_no_legacy_catalog_or_number_aliases() -> None:
    source = (REPO_ROOT / "tools/operation_prompt_wizard.py").read_text(encoding="utf-8")
    assert "LEGACY_OPERATION_ALIASES" not in source
    assert "legacy:" not in source
    assert "project-os-es\" / \"operaciones" in source
