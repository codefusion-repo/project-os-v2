"""Focused guards for the compact Spanish resolver surface."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ES_KERNEL_DIR = REPO_ROOT / "project-os-es" / "kernel"
ES_RESOLVER_PATH = REPO_ROOT / "project-os-es" / "tools" / "resolver.py"


def _load_resolver():
    spec = importlib.util.spec_from_file_location(
        "project_os_es_resolver", ES_RESOLVER_PATH
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_spanish_resolver_hydrates_artefact_template_refs_only() -> None:
    resolver = _load_resolver()

    result = resolver.resolver(
        "actor.terminal_agent",
        "mode.delegated_commit_pr",
        "workflow.issue_implementation",
        kernel_dir=ES_KERNEL_DIR,
    )

    assert result["estado"] == "status.resolved"
    artefactos = result["resuelto"]["workflow"]["artefactos"]
    by_key = {entry["key"]: entry for entry in artefactos}

    assert by_key["artefacto.reporte_ejecucion"]["required_template"] == (
        "project-os-es/templates/reporte-ejecucion.md"
    )
    assert by_key["artefacto.pull_request_body"]["required_template"] == (
        "project-os-es/templates/pull-request.md"
    )
    assert "workflow_key" not in by_key["artefacto.reporte_ejecucion"]
    assert "template_content" not in json.dumps(artefactos, ensure_ascii=False)


def test_spanish_resolver_selects_workflow_specific_artefacts() -> None:
    resolver = _load_resolver()

    pm_intake = resolver.resolver(
        "actor.browser_chat",
        "mode.review_only",
        "workflow.pm_intake",
        kernel_dir=ES_KERNEL_DIR,
    )
    closeout = resolver.resolver(
        "actor.browser_chat",
        "mode.review_only",
        "workflow.review_before_close",
        kernel_dir=ES_KERNEL_DIR,
    )

    assert pm_intake["estado"] == "status.resolved"
    pm_keys = {
        entry["key"] for entry in pm_intake["resuelto"]["workflow"]["artefactos"]
    }
    assert "artefacto.route_prompt" in pm_keys
    assert "artefacto.route_prompt_correccion" in pm_keys
    assert "artefacto.adr" in pm_keys
    assert "artefacto.roadmap" in pm_keys

    assert closeout["estado"] == "status.resolved"
    closeout_keys = {
        entry["key"] for entry in closeout["resuelto"]["workflow"]["artefactos"]
    }
    assert "artefacto.comentario_cierre" in closeout_keys
    assert "artefacto.closeout_command_bundle" in closeout_keys
    assert "artefacto.adr" not in closeout_keys


def test_spanish_artefact_catalog_has_single_existing_markdown_template() -> None:
    data = json.loads((ES_KERNEL_DIR / "artefactos.json").read_text(encoding="utf-8"))

    seen: set[str] = set()
    for artefacto in data["artefactos"]:
        key = artefacto["key"]
        assert key not in seen
        seen.add(key)
        assert artefacto["responsabilidad"]
        required_template = artefacto["required_template"]
        assert isinstance(required_template, str)
        assert required_template.endswith(".md")
        assert not isinstance(required_template, list)
        assert (REPO_ROOT / required_template).is_file()
