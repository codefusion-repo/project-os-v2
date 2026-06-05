"""Validator regression tests."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from project_os_v2.validators import validate_all, validate_r1_10, validate_r1_11


REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_schemas(root: Path) -> None:
    shutil.copytree(REPO_ROOT / "schemas", root / "schemas")


def _contract_envelope(
    contract_id: str,
    entity_family: str,
    payload: dict[str, object],
    *,
    contract_kind: str = "entity",
) -> dict[str, object]:
    return {
        "id": contract_id,
        "entity_family": entity_family,
        "contract_kind": contract_kind,
        "version": {"major": 1},
        "status": "draft",
        "schema_ref": None,
        "descripcion": "test fixture",
        "source_refs": [],
        "payload": payload,
    }


def _resolver_output_payload() -> dict[str, object]:
    return {
        "allowed_output_contract_ref": None,
        "effective_limite_refs": [],
        "effective_regla_refs": [],
        "estado_ref": None,
        "fallback_estado_ref": None,
        "index_ref": None,
        "manifest_ref": None,
        "missing_evidence_refs": [],
        "output_template_ref": None,
        "policy_ref": None,
        "reasons": {
            "blocked": [],
            "needs_context": [],
            "needs_pm_decision": [],
        },
        "required_evidence_refs": [],
        "resolution_trace": [],
        "resolver_ref": None,
        "response_shape_ref": None,
        "selected_accion_refs": [],
        "selected_actor_refs": [],
        "selected_artefacto_refs": [],
        "selected_contrato_refs": [],
        "selected_estado_refs": [],
        "selected_evidencia_refs": [],
        "selected_fuente_refs": [],
        "selected_limite_refs": [],
        "selected_plantilla_refs": [],
        "selected_recurso_refs": [],
        "selected_regla_refs": [],
        "selected_relacion_refs": [],
        "selected_rol_refs": [],
        "selected_scope_refs": [],
        "selected_variable_refs": [],
        "selected_workflow_refs": [],
        "selected_workflow_step_refs": [],
        "selector_refs": [],
        "source_provenance_refs": {},
        "status": "resolved",
    }


class R110ValidatorTests(unittest.TestCase):
    def test_negative_fixture_reports_missing_required_id(self) -> None:
        root = Path(__file__).parent / "fixtures" / "r1_10_invalid_missing_id"
        findings = validate_r1_10(root)
        self.assertTrue(any(finding.code == "REQUIRED_FIELD_MISSING" for finding in findings))
        self.assertTrue(any(finding.pointer == "/id" for finding in findings))

    def test_resolver_output_family_contract_validates(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            _copy_schemas(root)
            _write_json(
                root / "contracts" / "resolver_output" / "resolver_output.test_resolution.v1.json",
                _contract_envelope(
                    "resolver_output.test_resolution.v1",
                    "resolver_output",
                    _resolver_output_payload(),
                ),
            )

            findings = validate_r1_10(root)

        self.assertEqual([], findings)

    def test_resolver_output_limite_refs_validate_all_as_reference_fields(self) -> None:
        payload = _resolver_output_payload()
        payload["selected_limite_refs"] = ["limite.actor_write_boundary.v1"]
        payload["effective_limite_refs"] = ["limite.actor_write_boundary.v1"]

        limite_payload = {
            "nombre": "actor write boundary",
            "severidad": "hard",
            "tipo": "write_boundary",
        }

        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            _copy_schemas(root)
            _write_json(
                root / "contracts" / "limite" / "limite.actor_write_boundary.v1.json",
                _contract_envelope("limite.actor_write_boundary.v1", "limite", limite_payload),
            )
            _write_json(
                root / "contracts" / "resolver_output" / "resolver_output.test_resolution.v1.json",
                _contract_envelope(
                    "resolver_output.test_resolution.v1",
                    "resolver_output",
                    payload,
                ),
            )

            findings = validate_all(root)

        self.assertEqual([], findings)

    def test_resolver_contract_rejects_selected_output_refs(self) -> None:
        payload = {
            "nombre": "test resolver",
            "manifest_ref": None,
            "policy_ref": None,
            "input_schema_ref": None,
            "output_schema_ref": None,
            "fallback_estado_id": None,
            "selected_plantilla_refs": [],
        }

        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            _copy_schemas(root)
            _write_json(
                root / "contracts" / "resolver" / "resolver.test_resolver.v1.json",
                _contract_envelope("resolver.test_resolver.v1", "resolver", payload),
            )

            findings = validate_r1_10(root)

        self.assertTrue(
            any(
                finding.code == "JSON_SCHEMA_ADDITIONAL_PROPERTY"
                and finding.pointer == "/payload/selected_plantilla_refs"
                for finding in findings
            )
        )

    def test_resolver_contract_rejects_selected_limite_refs(self) -> None:
        payload = {
            "nombre": "test resolver",
            "manifest_ref": None,
            "policy_ref": None,
            "input_schema_ref": None,
            "output_schema_ref": None,
            "fallback_estado_id": None,
            "selected_limite_refs": [],
        }

        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            _copy_schemas(root)
            _write_json(
                root / "contracts" / "resolver" / "resolver.test_resolver.v1.json",
                _contract_envelope("resolver.test_resolver.v1", "resolver", payload),
            )

            findings = validate_all(root)

        self.assertTrue(
            any(
                finding.code == "JSON_SCHEMA_ADDITIONAL_PROPERTY"
                and finding.pointer == "/payload/selected_limite_refs"
                for finding in findings
            )
        )
        self.assertTrue(
            any(
                finding.code == "ACTOR_HARD_LIMIT_DUPLICATED"
                and finding.pointer == "/payload/selected_limite_refs"
                for finding in findings
            )
        )


class R111ValidatorTests(unittest.TestCase):
    def test_negative_fixture_reports_actor_hard_limit_duplication(self) -> None:
        root = Path(__file__).parent / "fixtures" / "r1_11_invalid_actor_hard_limit_duplication"
        findings = validate_r1_11(root)
        self.assertTrue(any(finding.code == "ACTOR_HARD_LIMIT_DUPLICATED" for finding in findings))
        self.assertTrue(any(finding.code == "ENTITY_PAYLOAD_FIELD_NOT_OWNED" for finding in findings))

    def test_non_owner_entity_selected_limite_refs_still_duplicate_actor_hard_limits(self) -> None:
        payload = {
            "nombre": "test actor",
            "superficie_capacidad": "terminal",
            "selected_limite_refs": [],
        }

        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            _copy_schemas(root)
            _write_json(
                root / "contracts" / "actor" / "actor.test_actor.v1.json",
                _contract_envelope("actor.test_actor.v1", "actor", payload),
            )

            findings = validate_all(root)

        self.assertTrue(
            any(
                finding.code == "ACTOR_HARD_LIMIT_DUPLICATED"
                and finding.pointer == "/payload/selected_limite_refs"
                for finding in findings
            )
        )

    def test_resolver_output_owns_selected_cross_family_refs(self) -> None:
        payload = _resolver_output_payload()
        payload["allowed_output_contract_ref"] = "contrato.formaliza.plantilla.v1"
        payload["output_template_ref"] = "plantilla.project_os_v2_response.v1"
        payload["response_shape_ref"] = "artefacto.validation_report.v1"
        payload["selected_plantilla_refs"] = ["plantilla.project_os_v2_response.v1"]
        payload["selected_artefacto_refs"] = ["artefacto.validation_report.v1"]
        payload["selected_variable_refs"] = ["variable.issue.v1"]
        payload["selected_contrato_refs"] = ["contrato.formaliza.plantilla.v1"]

        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            _copy_schemas(root)
            _write_json(
                root / "contracts" / "resolver_output" / "resolver_output.test_resolution.v1.json",
                _contract_envelope(
                    "resolver_output.test_resolution.v1",
                    "resolver_output",
                    payload,
                ),
            )

            findings = validate_r1_11(root)

        ownership_codes = {
            "ENTITY_PAYLOAD_FIELD_NOT_OWNED",
            "ENTITY_PAYLOAD_CROSS_FAMILY_FACT",
        }
        self.assertFalse(any(finding.code in ownership_codes for finding in findings), findings)


if __name__ == "__main__":
    unittest.main()
