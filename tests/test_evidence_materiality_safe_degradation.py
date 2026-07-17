"""Focused guards for evidence materiality and canonical safe degradation."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path
from typing import Any, Callable

import pytest

from tools.project_os_resolve import resolve
from tools.validate_kernel import validate_kernel


REPO_ROOT = Path(__file__).resolve().parents[1]
ES_KERNEL = REPO_ROOT / "project-os-es/kernel"
EN_KERNEL = REPO_ROOT / "project-os-en/kernel"
GAP_FIELDS = [
    "verified_evidence",
    "unavailable_evidence",
    "materiality",
    "decision_impact",
    "equivalent_source_used",
    "revalidation_required_before_write",
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_surface(tmp_path: Path, language: str = "es") -> Path:
    root = tmp_path / "repo"
    if language == "es":
        surface, support = "project-os-es", ("templates", "habilidades")
    else:
        surface, support = "project-os-en", ("templates", "skills")
    shutil.copytree(REPO_ROOT / surface / "kernel", root / surface / "kernel")
    for directory in support:
        shutil.copytree(REPO_ROOT / surface / directory, root / surface / directory)
    return root / surface / "kernel"


def test_kernel_contract_has_one_safe_gap_representation_and_non_degradable_hard_gates() -> None:
    evidence_doc = load(ES_KERNEL / "evidencia.json")
    workflows_doc = load(ES_KERNEL / "workflows.json")
    outputs_doc = load(ES_KERNEL / "salidas.json")
    evidence = {item["key"]: item for item in evidence_doc["evidence"]}
    outputs = {item["key"]: item for item in outputs_doc["outputs"]}

    contract = evidence_doc["materiality_contract"]
    assert contract["allowed_values"] == ["material", "auxiliary"]
    assert contract["hard_gates_degradable"] is False
    assert contract["source_error_target_state_inference"] is False
    assert contract["source_unavailability_signals"][-3:] == ["http.404", "http.422", "http.502"]
    assert contract["truncation_material_impacts"] == [
        "impact.authority",
        "impact.scope",
        "impact.decision",
    ]
    assert contract["unclassified_truncation_fails_closed"] is True

    safe = outputs_doc["safe_degradation_contract"]
    assert safe["status_key"] == "status.resolved"
    assert safe["gap_fields"] == GAP_FIELDS
    assert safe["completion_claim_with_gaps"] is False
    assert safe["revalidation_required_before_write"] is True

    for item in evidence.values():
        assert item["materiality"] in contract["allowed_values"]
        assert isinstance(item["hard_gate"], bool)
        assert item["revalidation_required_before_write"] is True
        assert item["source"]["primary"].startswith("source.")
    assert evidence["evidence.pm_approval"]["hard_gate"] is True
    assert evidence["evidence.pm_approval"]["materiality"] == "material"
    assert evidence["evidence.branch_preflight"]["hard_gate"] is True
    assert evidence["evidence.validation_output"]["hard_gate"] is True
    assert evidence["evidence.exact_ref"]["hard_gate"] is True

    for workflow in workflows_doc["workflows"]:
        required = set(workflow["required_evidence"])
        minimum = set(workflow["minimum_evidence"])
        assert minimum <= required
        assert all(evidence[key]["materiality"] == "material" for key in minimum)
        assert all(evidence[key]["materiality"] == "auxiliary" for key in required - minimum)

    for output in outputs.values():
        if output["allows_non_material_gaps"]:
            assert output["action_class"] in safe["allowed_action_classes"]
            assert output["safe_degradation_key"] == safe["key"]
        if output["action_class"] == "action.mutable":
            assert output["allows_non_material_gaps"] is False
            assert output["safe_degradation_key"] is None


@pytest.mark.parametrize("level", ("minimal", "compact", "full/debug"))
@pytest.mark.parametrize("kernel_dir", (ES_KERNEL, EN_KERNEL))
def test_resolver_hydrates_classification_minimums_and_gap_policy_at_every_level(
    level: str, kernel_dir: Path
) -> None:
    result = resolve(
        "actor.browser_chat",
        "workflow.review_only",
        "mode.review_only",
        kernel_dir=kernel_dir,
        hydration_level=level,
    )

    assert result["estado"] == "status.resolved"
    workflow = result["resuelto"]["workflow"]
    assert workflow["materiality_contract"]["safe_gap_materiality"] == "auxiliary"
    assert workflow["safe_degradation_contract"]["gap_fields"] == GAP_FIELDS
    assert {item["key"] for item in workflow["minimum_evidence"]} == {"evidence.repo_state"}
    auxiliary = next(
        item for item in workflow["required_evidence"] if item["key"] == "evidence.auxiliary_context"
    )
    assert auxiliary["materiality"] == "auxiliary"
    assert auxiliary["source"]["equivalents"][0]["key"] == "source.verified_auxiliary_context"
    review = next(item for item in workflow["allowed_outputs"] if item["key"] == "output.review_result")
    assert review["action_class"] == "action.read_only"
    assert review["allows_non_material_gaps"] is True


def test_partial_draft_can_degrade_but_issue_implementation_cannot() -> None:
    draft = resolve(
        "actor.browser_chat",
        "workflow.issue_implementation_manual",
        "mode.review_only",
    )["resuelto"]["workflow"]
    mutable = resolve(
        "actor.terminal_agent",
        "workflow.issue_implementation",
        "mode.delegated_commit_pr",
    )["resuelto"]["workflow"]

    assert "evidence.auxiliary_context" in {item["key"] for item in draft["required_evidence"]}
    assert "evidence.auxiliary_context" not in {item["key"] for item in draft["minimum_evidence"]}
    plan = next(item for item in draft["allowed_outputs"] if item["key"] == "output.manual_implementation_plan")
    assert plan["allows_non_material_gaps"] is True

    assert {item["key"] for item in mutable["required_evidence"]} == {
        item["key"] for item in mutable["minimum_evidence"]
    }
    report = next(item for item in mutable["allowed_outputs"] if item["key"] == "output.execution_report")
    assert report["action_class"] == "action.mutable"
    assert report["allows_non_material_gaps"] is False


@pytest.mark.parametrize(
    ("readme", "clauses"),
    (
        (
            "project-os-es/operaciones/README.md",
            (
                "evidencia mínima o material faltante",
                "hard gates no satisfechos",
                "autoridad ambigua o validación requerida faltante o fallida",
                "La evidencia auxiliar faltante no bloquea por sí sola",
                "outputs read-only o draft-only que declaren degradación segura",
                "Antes de toda mutación, revalida completamente cualquier gap",
            ),
        ),
        (
            "project-os-en/operations/README.md",
            (
                "missing minimum or material evidence",
                "unsatisfied hard gates",
                "ambiguous authority, or missing or failed required validation",
                "Missing auxiliary evidence does not block by itself",
                "declared read-only or draft-only outputs that allow safe degradation",
                "Before any mutation, fully revalidate every gap",
            ),
        ),
    ),
)
def test_bilingual_operation_contract_keeps_safe_degradation_fail_closed(
    readme: str, clauses: tuple[str, ...]
) -> None:
    text = " ".join((REPO_ROOT / readme).read_text(encoding="utf-8").split())

    for clause in clauses:
        assert clause in text


def test_resolver_keeps_the_primary_file_only_path_without_external_access() -> None:
    tree = ast.parse((REPO_ROOT / "tools/project_os_resolve.py").read_text(encoding="utf-8"))
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in (
            node.names
            if isinstance(node, ast.Import)
            else [ast.alias(name=node.module or "")]
        )
    }

    assert imported_roots.isdisjoint(
        {"git", "github", "http", "os", "requests", "socket", "subprocess", "urllib"}
    )


def test_equivalent_ci_requires_the_exact_ref_and_tag_readiness_cannot_omit_sha() -> None:
    evidence = {item["key"]: item for item in load(ES_KERNEL / "evidencia.json")["evidence"]}
    workflows = {item["key"]: item for item in load(ES_KERNEL / "workflows.json")["workflows"]}
    ci = next(
        item
        for item in evidence["evidence.validation_output"]["source"]["equivalents"]
        if item["key"] == "source.ci_validation_output"
    )

    assert "SHA" in ci["verification"] and "ref exacta" in ci["verification"]
    assert "evidence.exact_ref" in workflows["workflow.release_readiness"]["minimum_evidence"]
    assert evidence["evidence.exact_ref"]["missing_status"] == "status.blocked"
    assert evidence["evidence.exact_ref"]["source"]["equivalents"] == []


def test_gap_capable_output_templates_expose_every_canonical_field() -> None:
    outputs = {item["key"]: item for item in load(ES_KERNEL / "salidas.json")["outputs"]}
    artifacts = load(ES_KERNEL / "artefactos.json")["artefactos"]
    templates = {
        item["output_key"]: REPO_ROOT / item["required_template"]
        for item in artifacts
        if item.get("output_key") in outputs and outputs[item["output_key"]]["allows_non_material_gaps"]
    }

    assert set(templates) == {
        key for key, output in outputs.items() if output["allows_non_material_gaps"]
    }
    for path in templates.values():
        text = path.read_text(encoding="utf-8")
        for field in GAP_FIELDS:
            assert field in text, path


Mutation = Callable[[dict[str, Any]], None]


@pytest.mark.parametrize(
    ("filename", "mutate", "code"),
    (
        (
            "evidencia.json",
            lambda payload: payload["evidence"][0].__setitem__("materiality", "unknown"),
            "KES-013",
        ),
        (
            "evidencia.json",
            lambda payload: payload["evidence"][0].pop("materiality"),
            "KES-013",
        ),
        (
            "evidencia.json",
            lambda payload: payload["evidence"][0]["source"].__setitem__(
                "equivalents", [{"key": "source.unknown", "verification": "claimed equivalent"}]
            ),
            "KES-013",
        ),
        (
            "workflows.json",
            lambda payload: payload["workflows"][0].__setitem__(
                "minimum_evidence", ["evidence.auxiliary_context"]
            ),
            "KES-014",
        ),
        (
            "salidas.json",
            lambda payload: payload["safe_degradation_contract"]["gap_fields"].remove(
                "decision_impact"
            ),
            "KES-015",
        ),
        (
            "salidas.json",
            lambda payload: payload["safe_degradation_contract"].__setitem__(
                "revalidation_required_before_write", False
            ),
            "KES-015",
        ),
        (
            "salidas.json",
            lambda payload: payload["safe_degradation_contract"].__setitem__(
                "status_key", "status.needs_context"
            ),
            "KES-015",
        ),
        (
            "salidas.json",
            lambda payload: payload["outputs"][0].update(
                {
                    "allows_non_material_gaps": True,
                    "safe_degradation_key": "safe_degradation.non_material_gaps",
                }
            ),
            "KES-015",
        ),
    ),
)
def test_validator_rejects_unsafe_materiality_and_gap_schema(
    tmp_path: Path, filename: str, mutate: Mutation, code: str
) -> None:
    kernel = copy_surface(tmp_path)
    path = kernel / filename
    payload = load(path)
    mutate(payload)
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert any(finding.code == code for finding in validate_kernel(kernel))


def test_validator_rejects_es_en_materiality_drift(tmp_path: Path) -> None:
    es_kernel = copy_surface(tmp_path, "es")
    en_kernel = copy_surface(tmp_path, "en")
    path = en_kernel / "evidence.json"
    payload = load(path)
    payload["evidence"][0]["hard_gate"] = False
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert any(finding.code == "KES-016" for finding in validate_kernel(es_kernel))
