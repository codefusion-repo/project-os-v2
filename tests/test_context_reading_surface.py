"""Focused guards for the minimum reading surface and canonical source receipt."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import pytest

from tools.project_os_resolve import resolve
from tools.project_os_surfaces import SURFACES
from tools.validate_kernel import CONTEXT_RECEIPT_FIELDS, CONTEXT_RECEIPT_KEY, validate_kernel


REPO_ROOT = Path(__file__).resolve().parents[1]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
LEVELS = ("minimal", "compact", "full/debug")
REPORT_TEMPLATES = (
    "project-os-es/templates/reporte-ejecucion.md",
    "project-os-en/templates/execution-report.md",
    "project-os-es/templates/resultado-revision.md",
    "project-os-en/templates/review-result.md",
    "project-os-es/templates/resultado-estado.md",
    "project-os-en/templates/status-result.md",
    "project-os-es/templates/plan-implementacion-manual.md",
    "project-os-en/templates/manual-implementation-plan.md",
    "project-os-es/templates/pull-request.md",
    "project-os-en/templates/pull-request.md",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_surface(tmp_path: Path, language: str = "es") -> Path:
    root = tmp_path / "repo"
    surface = "project-os-es" if language == "es" else "project-os-en"
    skill_dir = "habilidades" if language == "es" else "skills"
    shutil.copytree(REPO_ROOT / surface / "kernel", root / surface / "kernel")
    shutil.copytree(REPO_ROOT / surface / "templates", root / surface / "templates")
    shutil.copytree(REPO_ROOT / surface / skill_dir, root / surface / skill_dir)
    return root / surface / "kernel"


def test_bilingual_kernel_has_one_canonical_context_receipt_for_every_output() -> None:
    spanish = load(ES_KERNEL / "salidas.json")
    english = load(EN_KERNEL / "outputs.json")

    assert spanish["context_receipt_contract"] == english["context_receipt_contract"]
    contract = spanish["context_receipt_contract"]
    assert contract["key"] == CONTEXT_RECEIPT_KEY
    assert contract["default_hydration_level"] == "compact"
    assert contract["fields"] == CONTEXT_RECEIPT_FIELDS
    assert contract["output_placement"] == "output_envelope"
    assert contract["source_reference_format"] == (
        "repository_relative_path_or_live_identifier"
    )
    assert contract["reason_format"] == "short_non_sensitive_identifier"
    assert contract["stores_source_bodies"] is False
    assert contract["stores_secret_values"] is False
    assert contract["stores_durable_live_state"] is False
    assert contract["resolver_external_access"] is False
    assert contract["additional_context_reason_values"] == [
        "full/debug",
        "audit",
        "debugging",
        "security_or_authorization_review",
        "complex_architecture",
        "pm_decision",
    ]
    for document in (spanish, english):
        assert document["outputs"]
        assert {
            output["context_receipt_key"] for output in document["outputs"]
        } == {CONTEXT_RECEIPT_KEY}


@pytest.mark.parametrize("level", LEVELS)
@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_resolver_reports_observable_context_plan_without_claiming_model_delivery(
    level: str, kernel_dir: Path
) -> None:
    result = resolve(
        "actor.terminal_agent",
        "workflow.issue_implementation",
        "mode.delegated_commit_pr",
        kernel_dir=kernel_dir,
        hydration_level=level,
    )

    assert result["estado"] == "status.resolved"
    workflow = result["resuelto"]["workflow"]
    plan = result["context_plan"]
    assert workflow["context_receipt_contract"]["key"] == CONTEXT_RECEIPT_KEY
    assert {
        output["context_receipt_key"] for output in workflow["allowed_outputs"]
    } == {CONTEXT_RECEIPT_KEY}
    assert plan["contract_key"] == CONTEXT_RECEIPT_KEY
    assert plan["hydration_level"] == level
    assert plan["receipt_fields"] == CONTEXT_RECEIPT_FIELDS
    assert plan["model_context_sources"] == []
    assert plan["model_context_observation"] == "executor_report_required"
    assert plan["resolver_external_access"] is False
    assert plan["additional_context_reason"] == (
        "full/debug" if level == "full/debug" else None
    )
    expected_kernel_sources = {
        f"{kernel_dir.parent.name}/kernel/{filename}"
        for filename, _ in next(
            surface.kernel_files.values()
            for surface in SURFACES
            if surface.kernel_dir == kernel_dir
        )
    }
    assert set(plan["tool_internal_sources"]) == expected_kernel_sources
    assert all(
        not Path(source).is_absolute() and "github.com/" not in source
        for source in (
            plan["tool_internal_sources"]
            + [
                source
                for sources in plan["resolver_projected_metadata"].values()
                for source in sources
            ]
        )
    )
    assert all(
        field.startswith("resuelto.")
        for field in plan["resolver_projected_metadata"]
    )
    assert plan["resolved_templates"]
    assert all(
        (REPO_ROOT / item["source"]).is_file()
        for item in plan["resolved_templates"]
    )
    assert plan["requested_skills"] == []


@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_requested_skill_and_templates_are_paths_and_metadata_without_bodies(
    kernel_dir: Path,
) -> None:
    result = resolve(
        "actor.browser_chat",
        "workflow.pm_intake",
        "mode.review_only",
        kernel_dir=kernel_dir,
        skill="skill.arquitectura_backend",
        hydration_level="compact",
    )

    plan = result["context_plan"]
    assert plan["requested_skills"] == [
        {
            "key": "skill.arquitectura_backend",
            "source": result["resuelto"]["requested_skills"][0]["required_skill"],
        }
    ]
    serialized = json.dumps(result, ensure_ascii=False)
    skill_body = (REPO_ROOT / plan["requested_skills"][0]["source"]).read_text(
        encoding="utf-8"
    )
    assert skill_body not in serialized
    for template in plan["resolved_templates"]:
        assert (REPO_ROOT / template["source"]).read_text(encoding="utf-8") not in serialized


def test_adapters_require_actual_receipts_and_forbid_recursive_project_os_crawls() -> None:
    adapter_expectations = {
        "project-os-es/adapters/AGENTS.target.md": (
            "`context_plan`",
            "recibo canónico de fuentes",
            "no recorras recursivamente Project OS",
            "contenido entregado al modelo",
        ),
        "project-os-es/adapters/BROWSER_CHAT.target.md": (
            "contexto del modelo",
            "recibo canónico de fuentes",
            "no recorras Project OS recursivamente",
            "razón admitida",
        ),
        "project-os-en/adapters/AGENTS.target.md": (
            "`context_plan`",
            "canonical source receipt",
            "do not recursively crawl Project OS",
            "content delivered to the model",
        ),
        "project-os-en/adapters/BROWSER_CHAT.target.md": (
            "model context",
            "canonical source receipt",
            "do not recursively crawl Project OS",
            "reason allowed",
        ),
    }
    for relative_path, clauses in adapter_expectations.items():
        text = " ".join(
            (REPO_ROOT / relative_path).read_text(encoding="utf-8").split()
        )
        for clause in clauses:
            assert clause in text, relative_path


def test_report_templates_expose_the_complete_receipt_without_source_bodies() -> None:
    for relative_path in REPORT_TEMPLATES:
        text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for field in CONTEXT_RECEIPT_FIELDS:
            assert field in text, relative_path
        assert "source + reason" in text
        assert "source + incorporation" in text


@pytest.mark.parametrize(
    ("relative_path", "no_close_clause"),
    (
        (
            "project-os-es/templates/pull-request.md",
            "Merge y cierre no se solicitan por este PR.",
        ),
        (
            "project-os-en/templates/pull-request.md",
            "Merge and closure are not requested by this PR.",
        ),
    ),
)
def test_pull_request_templates_without_close_requests_avoid_closing_keywords(
    relative_path: str,
    no_close_clause: str,
) -> None:
    text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    assert no_close_clause in text
    assert not re.search(
        r"(?im)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\{\{issue\}\}",
        text,
    )
    assert text.rstrip().endswith("Related to #{{issue}}.\n```")


@pytest.mark.parametrize(
    "mutate",
    (
        lambda payload: payload["context_receipt_contract"].__setitem__(
            "default_hydration_level", "minimal"
        ),
        lambda payload: payload["outputs"][0].pop("context_receipt_key"),
    ),
)
def test_validator_fails_closed_on_context_receipt_drift(
    tmp_path: Path,
    mutate: Any,
) -> None:
    kernel_dir = copy_surface(tmp_path)
    output_path = kernel_dir / "salidas.json"
    payload = load(output_path)
    mutate(payload)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    assert any(finding.code == "KES-017" for finding in validate_kernel(kernel_dir))
