"""Repo-shape and durable-state guards for the Project OS kernel."""

from __future__ import annotations

import json
import re
import subprocess
from fnmatch import fnmatch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_CONSOLE_DOCS = (
    "docs/OPERATIONS_CATALOG.md",
    "docs/OPERATIONS_CONSOLE_IMPLEMENTATION_PLAN.md",
)
FORBIDDEN_BROWSER_COMPANION_PACKAGE_PATHS = (
    "browser-companion",
    "browser_companion",
    "packages/browser-companion",
    "packages/browser_companion",
    "apps/browser-companion",
    "apps/browser_companion",
)
CANONICAL_ACTOR_IDS = {
    "actor.human_pm",
    "actor.terminal_agent",
    "actor.browser_chat",
    "actor.unknown",
}
FORBIDDEN_GH_JSON_FIELDS = {"stateReason", "merged", "isLatest"}
GH_JSON_PATTERN = re.compile(r"--json\s+([A-Za-z0-9_,]+)")
KERNEL_ID_PATTERN = re.compile(
    r"\b(?:status|actor|mode|boundary|evidence|workflow|output)\."
    r"(?!json\b|get\b|append\b)[A-Za-z0-9_*]+"
)
ROLE_ACTOR_ID_PATTERN = re.compile(
    r"\bactor\.(?:reviewer|qa|security|security_reviewer|owasp_security_reviewer|security_expert|asset|"
    r"asset_creator|design_asset_creator|graphic_artist|gpt|llm|api|api_bridge|github_connector)\b"
)
MARKDOWN_PATH_PATTERN = re.compile(r"`([^`\n]+)`")
SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", "node_modules", ".venv"}

# Narrow allowlists for intentional negative fixtures, target-owned optional
# paths in copy-in adapters, and historical recovery references.
KERNEL_ID_REFERENCE_ALLOWLIST = {
    ("docs/MOSDLC_OPERATION_MAP.md", "workflow.deployment"): "MOSDLC kernel-change candidate, identified but not applied",
    ("docs/MOSDLC_OPERATION_MAP.md", "mode.delegated_deploy_execution"): "MOSDLC kernel-change candidate, identified but not applied",
    ("docs/MOSDLC_OPERATION_MAP.md", "evidence.deployment_readiness"): "MOSDLC kernel-change candidate, identified but not applied",
    ("tests/test_mosdlc_operation_map.py", "workflow.deployment"): "MOSDLC kernel-change candidate guard",
    ("tests/test_mosdlc_operation_map.py", "mode.delegated_deploy_execution"): "MOSDLC kernel-change candidate guard",
    ("tests/test_mosdlc_operation_map.py", "evidence.deployment_readiness"): "MOSDLC kernel-change candidate guard",
    ("tests/test_mosdlc_fase4_templates.py", "workflow.deployment"): "Fase 4 no-deployment migration guard",
    ("tests/test_mosdlc_fase4_templates.py", "mode.delegated_deploy_execution"): "Fase 4 no-deployment migration guard",
    ("tests/test_mosdlc_fase4_templates.py", "evidence.deployment_readiness"): "Fase 4 no-deployment migration guard",
    ("tests/test_validate_kernel.py", "evidence.does_not_exist"): "negative unresolved-reference fixture",
    ("tests/test_validate_kernel.py", "status.deferred"): "negative fifth-status fixture",
    ("tests/test_validate_kernel.py", "status.maybe"): "negative non-canonical-status fixture",
    ("tests/test_resolver.py", "actor.does_not_exist"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "actor.fake"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "actor.nope"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "actor.test"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "actor.nonexistent"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "mode.does_not_exist"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "mode.nope"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "mode.imaginary"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "workflow.does_not_exist"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "workflow.nope"): "negative unknown-selector fixture",
    ("tests/test_resolver.py", "workflow.fake"): "negative unknown-selector fixture",
    ("tests/test_kernel_repo_shape_guards.py", "workflow.deployment"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "mode.delegated_deploy_execution"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "evidence.deployment_readiness"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "evidence.does_not_exist"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "status.deferred"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "status.maybe"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "actor.does_not_exist"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "actor.fake"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "actor.nope"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "actor.test"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "actor.nonexistent"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "mode.does_not_exist"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "mode.nope"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "mode.imaginary"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "workflow.does_not_exist"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "workflow.nope"): "allowlist declaration",
    ("tests/test_kernel_repo_shape_guards.py", "workflow.fake"): "allowlist declaration",
}
MARKDOWN_PATH_REFERENCE_ALLOWLIST = {
    ("AGENTS.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("legacy-project-os/adapters/AGENTS.target.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("legacy-project-os/adapters/BROWSER_CHAT.target.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("project-os-es/adapters/AGENTS.target.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("project-os-es/docs/reglas.md", "docs/decisions/"): "target-owned optional ADR directory",
    ("legacy-project-os/docs/DESIGN.md", "fuentes/"): "historical path recoverable from git history",
}


def _markdown_files() -> list[Path]:
    return [p for p in REPO_ROOT.rglob("*.md") if not (set(p.parts) & SKIP_DIRS)]


def _tracked_paths() -> set[str]:
    proc = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    return set(proc.stdout.splitlines())


def _tracked_text_files() -> list[Path]:
    suffixes = {".json", ".md", ".py", ".yml", ".yaml"}
    return [REPO_ROOT / rel for rel in sorted(_tracked_paths()) if Path(rel).suffix in suffixes]


def _kernel_ids() -> set[str]:
    """Union of active Spanish kernel keys and archived English kernel ids."""
    ids: set[str] = set()
    for path in sorted((REPO_ROOT / "legacy-project-os" / "kernel").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data.get("id"), str):
            ids.add(data["id"])
        for entry in data.get("entries", []):
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                ids.add(entry["id"])
    for path in sorted((REPO_ROOT / "project-os-es" / "kernel").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for family in data.values():
            if not isinstance(family, list):
                continue
            for entry in family:
                if isinstance(entry, dict) and isinstance(entry.get("key"), str):
                    ids.add(entry["key"])
    return ids


def _normalize_markdown_path_ref(token: str) -> str | None:
    value = token.strip().strip(",;:()[]{}\"'")
    if value.endswith(".") and not value.startswith("."):
        value = value[:-1]
    if (
        not value
        or " " in value
        or "{{" in value
        or "}}" in value
        or "<" in value
        or ">" in value
        or "$HOME" in value
        or "..." in value
        or value.startswith(("#", "/", "http://", "https://"))
    ):
        return None
    if value == "README":
        return "README.md"
    if value == "manifest.json":
        return "kernel/manifest.json"
    if value in {"artifacts.md", "route-prompt.md", "pm-command-bundle.md"}:
        return f"templates/{value}"
    if "/" not in value and (value.startswith(".") or Path(value).stem.isupper()):
        return None
    if re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", value) and "." not in value.rsplit("/", 1)[-1]:
        return None
    if value.startswith("tools.") and "/" not in value:
        return f"{value.replace('.', '/')}.py"
    if "/" not in value and not value.endswith((".md", ".json", ".py", ".yml", ".yaml")):
        return None
    if value.startswith(("work/", "org/", "owner/", "repo/")):
        return None
    return value


def _tracked_ref_exists(ref: str, tracked: set[str]) -> bool:
    if "*" in ref:
        return any(fnmatch(path, ref) for path in tracked)
    if ref.endswith("/"):
        return any(path.startswith(ref) for path in tracked)
    return ref in tracked or any(path.startswith(ref.rstrip("/") + "/") for path in tracked)


def test_no_console_planning_docs() -> None:
    present = [rel for rel in FORBIDDEN_CONSOLE_DOCS if (REPO_ROOT / rel).exists()]
    assert present == [], f"console planning docs must not return: {present}"


def test_no_browser_companion_package_created() -> None:
    present = [rel for rel in FORBIDDEN_BROWSER_COMPANION_PACKAGE_PATHS if (REPO_ROOT / rel).exists()]
    assert present == [], f"#309 Browser Companion package is out of scope: {present}"


def test_actor_model_is_surface_only() -> None:
    actors = json.loads((REPO_ROOT / "legacy-project-os" / "kernel" / "actors.json").read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in actors["entries"]}
    assert ids == CANONICAL_ACTOR_IDS, (
        f"actor set drifted from the four surfaces: {sorted(ids)}. "
        "A new actor requires a new execution surface (docs/DESIGN.md, Actor model)."
    )
    assert actors.get("actor_model_note"), "actors.json must keep the canonical actor_model_note"


def test_no_unsupported_gh_json_fields() -> None:
    offenders: list[str] = []
    for path in _markdown_files():
        for field_list in GH_JSON_PATTERN.findall(path.read_text(encoding="utf-8")):
            bad = FORBIDDEN_GH_JSON_FIELDS & set(field_list.split(","))
            if bad:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: {sorted(bad)}")
    assert offenders == [], f"unsupported gh --json fields found: {offenders}"


def test_canonical_command_bundle_source_normalized() -> None:
    assert (REPO_ROOT / "legacy-project-os" / "templates" / "pm-command-bundle.md").exists(), (
        "the single canonical command-bundle source must stay at templates/pm-command-bundle.md"
    )
    assert not (REPO_ROOT / "legacy-project-os" / "templates" / "commands").exists(), (
        "the single-file templates/commands/ folder was flattened; do not reintroduce it"
    )


def test_kernel_id_references_resolve_or_are_allowlisted() -> None:
    ids = _kernel_ids()
    offenders: list[str] = []
    for path in _tracked_text_files():
        rel = str(path.relative_to(REPO_ROOT))
        for ref in sorted(set(KERNEL_ID_PATTERN.findall(path.read_text(encoding="utf-8")))):
            if (rel, ref) in KERNEL_ID_REFERENCE_ALLOWLIST:
                continue
            if "*" in ref:
                offenders.append(f"{rel}: pseudo kernel id {ref}")
            elif ref not in ids:
                offenders.append(f"{rel}: unresolved kernel id {ref}")
    assert offenders == [], f"kernel id reference drift found: {offenders}"


def test_no_role_actor_ids_in_durable_text() -> None:
    offenders: list[str] = []
    for path in _tracked_text_files():
        rel = str(path.relative_to(REPO_ROOT))
        for match in ROLE_ACTOR_ID_PATTERN.finditer(path.read_text(encoding="utf-8")):
            offenders.append(f"{rel}: {match.group(0)}")
    assert offenders == [], f"role-based actor ids found: {offenders}"


def test_positive_markdown_paths_resolve_or_are_allowlisted() -> None:
    tracked = _tracked_paths()
    offenders: list[str] = []
    for path in _markdown_files():
        rel = str(path.relative_to(REPO_ROOT))
        for token in sorted(set(MARKDOWN_PATH_PATTERN.findall(path.read_text(encoding="utf-8")))):
            ref = _normalize_markdown_path_ref(token)
            if ref is None or (rel, ref) in MARKDOWN_PATH_REFERENCE_ALLOWLIST:
                continue
            candidates = [ref]
            if rel.startswith(("legacy-project-os/", "docs/decisions/")):
                # Archived files and decision records keep their historical
                # pre-migration references; resolve those against the archive.
                candidates.append(f"legacy-project-os/{ref}")
            if not any(_tracked_ref_exists(c, tracked) for c in candidates):
                offenders.append(f"{rel}: {ref}")
    assert offenders == [], f"positive Markdown path references must resolve or be allowlisted: {offenders}"
