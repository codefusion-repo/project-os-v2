"""Tests for the project-os-v2-min kernel validator and repo-shape guards."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pytest

from tools.validate_kernel import validate_kernel

REPO_ROOT = Path(__file__).resolve().parent.parent


def codes(findings) -> set[str]:
    return {finding.code for finding in findings}


@pytest.fixture()
def kernel_copy(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "kernel", tmp_path / "kernel")
    return tmp_path


def mutate(root: Path, name: str, fn) -> None:
    path = root / "kernel" / name
    data = json.loads(path.read_text(encoding="utf-8"))
    fn(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_real_kernel_passes() -> None:
    assert validate_kernel(REPO_ROOT) == []


def test_missing_kernel_dir_fails(tmp_path: Path) -> None:
    assert codes(validate_kernel(tmp_path)) == {"KMIN-001"}


def test_invalid_json_fails(kernel_copy: Path) -> None:
    (kernel_copy / "kernel" / "actors.json").write_text("{not json", encoding="utf-8")
    assert "KMIN-001" in codes(validate_kernel(kernel_copy))


def test_load_order_missing_file(kernel_copy: Path) -> None:
    (kernel_copy / "kernel" / "evidence.json").unlink()
    assert "KMIN-002" in codes(validate_kernel(kernel_copy))


def test_undeclared_kernel_file(kernel_copy: Path) -> None:
    (kernel_copy / "kernel" / "extra.json").write_text('{"id": "kernel.extra", "family": "extra"}', encoding="utf-8")
    assert "KMIN-002" in codes(validate_kernel(kernel_copy))


def test_missing_entry_key(kernel_copy: Path) -> None:
    mutate(kernel_copy, "boundaries.json", lambda d: d["entries"][0].pop("rule"))
    assert "KMIN-003" in codes(validate_kernel(kernel_copy))


def test_duplicate_id(kernel_copy: Path) -> None:
    mutate(kernel_copy, "evidence.json", lambda d: d["entries"].append(dict(d["entries"][0])))
    assert "KMIN-004" in codes(validate_kernel(kernel_copy))


def test_unresolved_reference(kernel_copy: Path) -> None:
    mutate(kernel_copy, "workflows.json", lambda d: d["entries"][0]["required_evidence_refs"].append("evidence.does_not_exist"))
    assert "KMIN-005" in codes(validate_kernel(kernel_copy))


def test_non_canonical_status_reference(kernel_copy: Path) -> None:
    mutate(kernel_copy, "boundaries.json", lambda d: d["entries"][0].update(on_violation="status.maybe"))
    assert "KMIN-006" in codes(validate_kernel(kernel_copy))


def test_fifth_status_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "statuses.json",
        lambda d: d["entries"].append({"id": "status.deferred", "meaning": "extra status"}),
    )
    assert "KMIN-007" in codes(validate_kernel(kernel_copy))


def test_permission_grant_key_rejected(kernel_copy: Path) -> None:
    mutate(kernel_copy, "actors.json", lambda d: d["entries"][1].update(can_push=True))
    assert "KMIN-008" in codes(validate_kernel(kernel_copy))


def test_live_state_sha_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "manifest.json",
        lambda d: d.update(description="baseline " + "a1" * 20),
    )
    assert "KMIN-009" in codes(validate_kernel(kernel_copy))


def test_github_url_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "evidence.json",
        lambda d: d["entries"][0].update(satisfied_by="see github.com/example/repo/issues/1"),
    )
    assert "KMIN-009" in codes(validate_kernel(kernel_copy))


def test_browser_actor_write_mode_rejected(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "actors.json",
        lambda d: d["entries"][2]["allowed_mode_refs"].append("mode.delegated_commit_pr"),
    )
    assert "KMIN-010" in codes(validate_kernel(kernel_copy))


def test_size_budget_enforced(kernel_copy: Path) -> None:
    mutate(
        kernel_copy,
        "manifest.json",
        lambda d: d["size_budget"].update(kernel_total_bytes_max=100),
    )
    assert "KMIN-011" in codes(validate_kernel(kernel_copy))


# --- Repo-shape guards (prevent regressing the #287 simplification) ---------
#
# Deterministic checks that keep project-os-v2 a compact, portable kernel:
# console planning docs stay out, the actor model stays surface-only, command
# bundles never emit unsupported gh --json fields, and the command-bundle source
# keeps its normalized location. They guard repo shape only; no writes, no
# authority.

FORBIDDEN_CONSOLE_DOCS = (
    "docs/OPERATIONS_CATALOG.md",
    "docs/OPERATIONS_CONSOLE_IMPLEMENTATION_PLAN.md",
)
CANONICAL_ACTOR_IDS = {
    "actor.human_pm",
    "actor.terminal_agent",
    "actor.browser_chat",
    "actor.unknown",
}
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
    assert (REPO_ROOT / "templates" / "pm-command-bundle.md").exists(), (
        "the single canonical command-bundle source must stay at templates/pm-command-bundle.md"
    )
    assert not (REPO_ROOT / "templates" / "commands").exists(), (
        "the single-file templates/commands/ folder was flattened; do not reintroduce it"
    )
