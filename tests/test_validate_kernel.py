"""Tests for the project-os-v2-min kernel integrity validator."""

from __future__ import annotations

import json
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
