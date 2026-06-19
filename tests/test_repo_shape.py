"""Repo-shape guards that prevent regressing the KMIN.5 (#287) simplification.

These deterministic checks keep project-os-v2 a compact, portable kernel:
- console implementation/planning docs do not return as durable repo surface;
- the actor model stays surface-only, with no role-based actors;
- PM command bundles never emit unsupported GitHub CLI ``--json`` pseudo-fields;
- the single canonical command-bundle source keeps its normalized location.

They guard repo shape only; they grant no authority and run no writes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Console build-planning docs removed in #287; they belong in the console repo
# / roadmap issue, not in this kernel's durable surface.
FORBIDDEN_CONSOLE_DOCS = (
    "docs/OPERATIONS_CATALOG.md",
    "docs/OPERATIONS_CONSOLE_IMPLEMENTATION_PLAN.md",
)

# Capability comes from the execution surface, never a role (ADR-0001).
CANONICAL_ACTOR_IDS = {
    "actor.human_pm",
    "actor.terminal_agent",
    "actor.browser_chat",
    "actor.unknown",
}

# Pseudo-fields the GitHub CLI does not support; emitting them breaks bundles.
FORBIDDEN_GH_JSON_FIELDS = {"stateReason", "merged"}
GH_JSON_PATTERN = re.compile(r"--json\s+([A-Za-z0-9_,]+)")

SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", "node_modules", ".venv"}


def _markdown_files() -> list[Path]:
    return [p for p in REPO_ROOT.rglob("*.md") if not (set(p.parts) & SKIP_DIRS)]


def test_no_console_planning_docs() -> None:
    present = [rel for rel in FORBIDDEN_CONSOLE_DOCS if (REPO_ROOT / rel).exists()]
    assert present == [], f"console planning docs must not return: {present}"


def test_actor_model_is_surface_only() -> None:
    actors = json.loads((REPO_ROOT / "kernel" / "actors.json").read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in actors["entries"]}
    assert ids == CANONICAL_ACTOR_IDS, (
        f"actor set drifted from the four surfaces: {sorted(ids)}. "
        "Adding an actor requires a new execution surface and ADR-0001 update."
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
    assert (REPO_ROOT / "templates" / "pm-command-bundle.md").exists(), (
        "the single canonical command-bundle source must stay at templates/pm-command-bundle.md"
    )
    assert not (REPO_ROOT / "templates" / "commands").exists(), (
        "the single-file templates/commands/ folder was flattened; do not reintroduce it"
    )
