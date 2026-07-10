"""Active Spanish template/skill path validation guards."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_kernel import DEFAULT_KERNEL_DIR, validate_kernel


REPO_ROOT = Path(__file__).resolve().parents[1]


def copy_active_surface(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for source in ("kernel", "templates", "habilidades"):
        shutil.copytree(REPO_ROOT / "project-os-es" / source, root / "project-os-es" / source)
    return root / "project-os-es/kernel"


def test_default_validator_checks_active_spanish_required_paths() -> None:
    assert DEFAULT_KERNEL_DIR == REPO_ROOT / "project-os-es/kernel"
    assert validate_kernel() == []

    artifacts = json.loads((DEFAULT_KERNEL_DIR / "artefactos.json").read_text(encoding="utf-8"))
    skills = json.loads((DEFAULT_KERNEL_DIR / "skills.json").read_text(encoding="utf-8"))
    assert all(
        item["required_template"].startswith("project-os-es/templates/")
        for item in artifacts["artefactos"] if item.get("active")
    )
    assert all(
        item["required_skill"].startswith("project-os-es/habilidades/")
        for item in skills["skills"] if item.get("active")
    )


def test_validator_fails_closed_on_missing_active_markdown_reference(tmp_path: Path) -> None:
    kernel = copy_active_surface(tmp_path)
    path = kernel / "artefactos.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["artefactos"][0]["required_template"] = "project-os-es/templates/no-existe.md"
    path.write_text(json.dumps(payload), encoding="utf-8")

    findings = validate_kernel(kernel)
    assert any(finding.code == "KES-006" and finding.file == "artefactos.json" for finding in findings)
