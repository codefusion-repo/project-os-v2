"""Focused guards for the resolver's provenance route and receipt safety contract.

Reduced to executable behavior only: a normal resolution carries no provenance at
any level, an explicit allowed reason returns relative-path metadata with no
source bodies, no secrets, no durable live state and no external access, an
unknown reason fails closed, and the validator fails closed on receipt-contract
drift. Editorial template wording and PM-facing rendering are not tested here;
there is no production renderer to protect.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from tools.project_os_resolve import resolve
from tools.project_os_surfaces import SURFACES
from tools.validate_kernel import (
    CONTEXT_PROVENANCE_REASONS,
    CONTEXT_RECEIPT_EXECUTOR_FIELDS,
    CONTEXT_RECEIPT_KEY,
    validate_kernel,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
LEVELS = ("minimal", "compact", "full/debug")


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


def test_context_receipt_contract_is_bilingual_and_stores_nothing_sensitive() -> None:
    spanish = load(ES_KERNEL / "salidas.json")["context_receipt_contract"]
    english = load(EN_KERNEL / "outputs.json")["context_receipt_contract"]

    assert spanish == english
    assert spanish["key"] == CONTEXT_RECEIPT_KEY
    assert spanish["executor_reported_fields"] == CONTEXT_RECEIPT_EXECUTOR_FIELDS
    assert spanish["detailed_provenance_default"] == "omitted"
    assert spanish["detailed_provenance_reasons"] == CONTEXT_PROVENANCE_REASONS
    assert spanish["pm_facing_traceability"] == "reviewed_evidence"
    assert spanish["stores_source_bodies"] is False
    assert spanish["stores_secret_values"] is False
    assert spanish["stores_durable_live_state"] is False
    assert spanish["resolver_external_access"] is False
    assert spanish["source_reference_format"] == "repository_relative_path_or_live_identifier"
    # The resolver-known provenance lives in context_plan and must not be
    # duplicated into the fields the executor reports.
    assert "resolved_template" not in spanish["executor_reported_fields"]
    assert "tool_internal_sources" not in spanish["executor_reported_fields"]


@pytest.mark.parametrize("level", LEVELS)
@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_normal_resolution_carries_no_provenance_at_any_level(
    level: str, kernel_dir: Path
) -> None:
    result = resolve(
        "actor.terminal_agent",
        "workflow.issue_implementation",
        "mode.delegated_commit_pr",
        kernel_dir=kernel_dir,
        change_class="change_class.small",
        hydration_level=level,
    )

    assert result["estado"] == "status.resolved"
    assert "context_plan" not in result
    contract = result["resuelto"]["workflow"]["context_receipt_contract"]
    assert contract["detailed_provenance_default"] == "omitted"


@pytest.mark.parametrize("reason", CONTEXT_PROVENANCE_REASONS)
@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_requested_provenance_reports_relative_metadata_without_bodies_or_external_access(
    reason: str, kernel_dir: Path
) -> None:
    result = resolve(
        "actor.terminal_agent",
        "workflow.issue_implementation",
        "mode.delegated_commit_pr",
        kernel_dir=kernel_dir,
        change_class="change_class.small",
        context_provenance=reason,
    )

    assert result["estado"] == "status.resolved"
    plan = result["context_plan"]
    assert plan["provenance_reason"] == reason
    assert plan["model_context_observation"] == "executor_report_required"
    assert result["resuelto"]["workflow"]["context_receipt_contract"][
        "resolver_external_access"
    ] is False

    expected_kernel_sources = {
        f"{kernel_dir.parent.name}/kernel/{filename}"
        for filename, _ in next(
            surface.kernel_files.values()
            for surface in SURFACES
            if surface.kernel_dir == kernel_dir
        )
    }
    assert set(plan["tool_internal_sources"]) == expected_kernel_sources
    metadata_sources = [
        source
        for sources in plan["resolver_projected_metadata"].values()
        for source in sources
    ]
    assert all(
        not Path(source).is_absolute() and "github.com/" not in source
        for source in plan["tool_internal_sources"] + metadata_sources
    )
    assert all(field.startswith("resuelto.") for field in plan["resolver_projected_metadata"])
    assert plan["resolved_templates"]
    assert all((REPO_ROOT / item["source"]).is_file() for item in plan["resolved_templates"])


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
        context_provenance="audit",
    )

    plan = result["context_plan"]
    assert plan["requested_skills"] == [
        {
            "key": "skill.arquitectura_backend",
            "source": result["resuelto"]["requested_skills"][0]["required_skill"],
        }
    ]
    serialized = json.dumps(result, ensure_ascii=False)
    skill_body = (REPO_ROOT / plan["requested_skills"][0]["source"]).read_text(encoding="utf-8")
    assert skill_body not in serialized
    for template in plan["resolved_templates"]:
        assert (REPO_ROOT / template["source"]).read_text(encoding="utf-8") not in serialized


@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_unknown_provenance_reason_fails_closed_without_leaking_a_plan(
    kernel_dir: Path,
) -> None:
    result = resolve(
        "actor.terminal_agent",
        "workflow.issue_implementation",
        "mode.delegated_commit_pr",
        kernel_dir=kernel_dir,
        change_class="change_class.small",
        context_provenance="curiosity",
    )

    assert result["estado"] == "status.blocked"
    assert result["resuelto"] is None
    assert "context_plan" not in result
    assert result["errores"]


@pytest.mark.parametrize(
    "mutate",
    (
        lambda payload: payload["context_receipt_contract"].__setitem__(
            "detailed_provenance_default", "included"
        ),
        lambda payload: payload["context_receipt_contract"].pop("stores_secret_values"),
        lambda payload: payload["context_receipt_contract"]["detailed_provenance_reasons"].append(
            "any_reason"
        ),
        lambda payload: payload["outputs"][0].pop("context_receipt_key"),
    ),
)
def test_validator_fails_closed_on_context_receipt_drift(tmp_path: Path, mutate: Any) -> None:
    kernel_dir = copy_surface(tmp_path)
    output_path = kernel_dir / "salidas.json"
    payload = load(output_path)
    mutate(payload)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    assert any(finding.code == "KES-017" for finding in validate_kernel(kernel_dir))
