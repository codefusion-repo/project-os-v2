"""Validator regression tests."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from project_os_v2.validators import validate_all, validate_r1_10, validate_r1_11


REPO_ROOT = Path(__file__).resolve().parents[1]
RELATIONSHIP_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "validators"
SUPPORT_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "validators"
SUPPORT_SELECTOR_DIMENSIONS = {
    "actor_type": ["actor"],
    "role": ["rol"],
    "workflow": ["workflow", "workflow_step"],
    "action": ["accion"],
    "resource": ["recurso"],
    "scope": ["scope"],
    "evidence_requirement": ["evidencia"],
    "source_authority": ["fuente"],
    "output_artifact": ["artefacto"],
    "template": ["plantilla"],
    "variable": ["variable"],
    "state": ["estado"],
    "limit": ["limite"],
    "rule": ["regla"],
    "policy_ref": ["policy"],
}
SUPPORT_OUTPUT_GROUPS = [
    "estado_ref",
    "fallback_estado_ref",
    "selected_estado_refs",
    "selected_actor_refs",
    "selected_rol_refs",
    "selected_workflow_refs",
    "selected_workflow_step_refs",
    "selected_accion_refs",
    "selected_recurso_refs",
    "selected_scope_refs",
    "selected_fuente_refs",
    "selected_evidencia_refs",
    "selected_limite_refs",
    "selected_regla_refs",
    "selected_variable_refs",
    "selected_plantilla_refs",
    "selected_artefacto_refs",
    "selected_relacion_refs",
    "selected_contrato_refs",
    "allowed_output_contract_ref",
    "required_evidence_refs",
    "missing_evidence_refs",
    "output_template_ref",
    "response_shape_ref",
]


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


def _support_envelope(contract_id: str, contract_kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "id": contract_id,
        "classification": "non_entity_static_reference_bundle",
        "contract_kind": contract_kind,
        "version": {"major": 1},
        "status": "draft",
        "schema_ref": None,
        "descripcion": "support fixture",
        "source_refs": [],
        "payload": payload,
    }


def _relationship_contract(
    contract_id: str,
    payload: dict[str, object],
    *,
    status: str = "draft",
) -> dict[str, object]:
    return _contract_envelope(
        contract_id,
        "relacion",
        payload,
        contract_kind="relationship",
    ) | {"status": status}


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


def _relationship_payload(
    origen_entidad: object,
    origen_id: object,
    tipo_relacion: object,
    destino_entidad: object,
    destino_id: object,
    cardinalidad: object = "N:M",
    requerido: object = True,
    orden: object = None,
) -> dict[str, object]:
    return {
        "origen_entidad": origen_entidad,
        "origen_id": origen_id,
        "destino_entidad": destino_entidad,
        "destino_id": destino_id,
        "tipo_relacion": tipo_relacion,
        "cardinalidad": cardinalidad,
        "requerido": requerido,
        "orden": orden,
    }


def _relationship_type_payload(
    origen_entidad: object = "actor",
    tipo_relacion: object = "aplica",
    destino_entidad: object = "regla",
    cardinalidad: object = "N:M",
    requerido: object = None,
    orden: object = None,
) -> dict[str, object]:
    return _relationship_payload(
        origen_entidad,
        None,
        tipo_relacion,
        destino_entidad,
        None,
        cardinalidad,
        requerido,
        orden,
    )


def _placeholder_relationship_payload() -> dict[str, object]:
    return _relationship_payload(None, None, None, None, None, None, None, None)


def _minimal_entity_contracts() -> dict[str, dict[str, object]]:
    return {
        "contracts/actor/actor.test_actor.v1.json": _contract_envelope(
            "actor.test_actor.v1",
            "actor",
            {"nombre": "test actor", "superficie_capacidad": "test"},
        ),
        "contracts/regla/regla.test_rule.v1.json": _contract_envelope(
            "regla.test_rule.v1",
            "regla",
            {
                "nombre": "test rule",
                "condicion": "test",
                "comportamiento_esperado": "does not grant write permission",
            },
        ),
        "contracts/resolver/resolver.test_resolver.v1.json": _contract_envelope(
            "resolver.test_resolver.v1",
            "resolver",
            {
                "nombre": "test resolver",
                "manifest_ref": None,
                "policy_ref": None,
                "input_schema_ref": None,
                "output_schema_ref": None,
                "fallback_estado_id": None,
            },
        ),
        "contracts/estado/estado.first.v1.json": _contract_envelope(
            "estado.first.v1",
            "estado",
            {"nombre": "first"},
        ),
        "contracts/estado/estado.second.v1.json": _contract_envelope(
            "estado.second.v1",
            "estado",
            {"nombre": "second"},
        ),
    }


def _base_actor_rule_relationship_contracts() -> dict[str, dict[str, object]]:
    contracts = _minimal_entity_contracts()
    contracts["contracts/relacion/relacion.actor.aplica.regla.v1.json"] = _relationship_contract(
        "relacion.actor.aplica.regla.v1",
        _relationship_type_payload(),
    )
    contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"] = _relationship_contract(
        "relacion.actor.test_actor.aplica.regla.test_rule.v1",
        _relationship_payload("actor", "actor.test_actor.v1", "aplica", "regla", "regla.test_rule.v1"),
    )
    return contracts


def _add_resolver_support_contracts(contracts: dict[str, dict[str, object]]) -> None:
    contracts["contracts/relacion/relacion.resolver.usa.relacion.v1.json"] = _relationship_contract(
        "relacion.resolver.usa.relacion.v1",
        _relationship_type_payload("resolver", "usa", "relacion", "1:N"),
    )
    contracts[
        "contracts/relacion/relacion.resolver.test_resolver.usa.relacion.actor_test_actor_aplica_regla_test_rule.v1.json"
    ] = _relationship_contract(
        "relacion.resolver.test_resolver.usa.relacion.actor_test_actor_aplica_regla_test_rule.v1",
        _relationship_payload(
            "resolver",
            "resolver.test_resolver.v1",
            "usa",
            "relacion",
            "relacion.actor.test_actor.aplica.regla.test_rule.v1",
            "1:N",
        ),
    )


def _add_resolver_output(contracts: dict[str, dict[str, object]], selected_relacion_refs: list[str]) -> None:
    payload = _resolver_output_payload()
    payload["resolver_ref"] = "resolver.test_resolver.v1"
    payload["selected_relacion_refs"] = selected_relacion_refs
    contracts["contracts/resolver_output/resolver_output.test_resolution.v1.json"] = _contract_envelope(
        "resolver_output.test_resolution.v1",
        "resolver_output",
        payload,
    )


def _ordered_workflow_contracts(
    *,
    duplicate: bool = False,
    gap: bool = False,
    missing_order: bool = False,
) -> dict[str, dict[str, object]]:
    contracts = {
        "contracts/workflow/workflow.test_workflow.v1.json": _contract_envelope(
            "workflow.test_workflow.v1",
            "workflow",
            {"nombre": "test workflow", "etapa_ciclo_vida": "test"},
        ),
        "contracts/workflow_step/workflow_step.first.v1.json": _contract_envelope(
            "workflow_step.first.v1",
            "workflow_step",
            {
                "nombre": "first",
                "objetivo": "first",
                "condicion_base_avance": None,
                "condicion_base_bloqueo": None,
                "condicion_base_repeticion": None,
            },
        ),
        "contracts/workflow_step/workflow_step.second.v1.json": _contract_envelope(
            "workflow_step.second.v1",
            "workflow_step",
            {
                "nombre": "second",
                "objetivo": "second",
                "condicion_base_avance": None,
                "condicion_base_bloqueo": None,
                "condicion_base_repeticion": None,
            },
        ),
        "contracts/relacion/relacion.workflow.compone.workflow_step.v1.json": _relationship_contract(
            "relacion.workflow.compone.workflow_step.v1",
            _relationship_type_payload("workflow", "compone", "workflow_step"),
        ),
    }
    second_order = None if missing_order else 1 if duplicate else 3 if gap else 2
    contracts["contracts/relacion/relacion.workflow.test_workflow.compone.workflow_step.first.v1.json"] = _relationship_contract(
        "relacion.workflow.test_workflow.compone.workflow_step.first.v1",
        _relationship_payload("workflow", "workflow.test_workflow.v1", "compone", "workflow_step", "workflow_step.first.v1", orden=1),
    )
    contracts["contracts/relacion/relacion.workflow.test_workflow.compone.workflow_step.second.v1.json"] = _relationship_contract(
        "relacion.workflow.test_workflow.compone.workflow_step.second.v1",
        _relationship_payload(
            "workflow",
            "workflow.test_workflow.v1",
            "compone",
            "workflow_step",
            "workflow_step.second.v1",
            orden=second_order,
        ),
    )
    return contracts


def _contracts_for_relationship_scenario(scenario: str) -> dict[str, dict[str, object]]:
    if scenario == "valid_relationship_type":
        return {
            "contracts/relacion/relacion.actor.aplica.regla.v1.json": _relationship_contract(
                "relacion.actor.aplica.regla.v1",
                _relationship_type_payload(),
            )
        }
    if scenario == "valid_relationship_instance":
        return _base_actor_rule_relationship_contracts()
    if scenario == "valid_placeholder_relationship":
        return {
            "contracts/relacion/relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1.json": _relationship_contract(
                "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1",
                _placeholder_relationship_payload(),
            )
        }
    if scenario == "valid_ordered_relationship_group":
        return _ordered_workflow_contracts()
    if scenario == "valid_resolver_relationship_support_links":
        contracts = _base_actor_rule_relationship_contracts()
        _add_resolver_support_contracts(contracts)
        _add_resolver_output(contracts, ["relacion.actor.test_actor.aplica.regla.test_rule.v1"])
        return contracts
    if scenario == "safe_denial_reference_only_wording":
        return {
            "contracts/regla/regla.safe_denial_wording.v1.json": _contract_envelope(
                "regla.safe_denial_wording.v1",
                "regla",
                {
                    "nombre": "safe denial wording",
                    "condicion": "reference only",
                    "comportamiento_esperado": "does not create runtime behavior, command execution, permission grants, or write authorization",
                },
            )
        }

    contracts = _base_actor_rule_relationship_contracts()
    if scenario == "missing_endpoint":
        contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.missing_rule.v1.json"] = _relationship_contract(
            "relacion.actor.test_actor.aplica.regla.missing_rule.v1",
            _relationship_payload("actor", "actor.test_actor.v1", "aplica", "regla", "regla.missing_rule.v1"),
        )
        del contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"]
    elif scenario == "endpoint_family_mismatch":
        contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"]["payload"]["destino_entidad"] = "actor"
    elif scenario == "relationship_type_tuple_mismatch":
        contracts["contracts/relacion/relacion.actor.aplica.regla.v1.json"]["payload"]["destino_entidad"] = "actor"
    elif scenario == "missing_relationship_type":
        contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"]["payload"]["tipo_relacion"] = "usa"
    elif scenario == "deprecated_type_use":
        contracts["contracts/relacion/relacion.actor.aplica.regla.v1.json"]["status"] = "deprecated"
    elif scenario == "cardinality_mismatch":
        contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"]["payload"]["cardinalidad"] = "N:1"
    elif scenario == "duplicate_instance_triple":
        contracts["contracts/relacion/relacion.actor.test_actor.duplicate_aplica.regla.test_rule.v1.json"] = _relationship_contract(
            "relacion.actor.test_actor.duplicate_aplica.regla.test_rule.v1",
            _relationship_payload("actor", "actor.test_actor.v1", "aplica", "regla", "regla.test_rule.v1"),
        )
    elif scenario == "duplicate_type_tuple":
        contracts["contracts/relacion/relacion.actor.duplicate_aplica.regla.v1.json"] = _relationship_contract(
            "relacion.actor.duplicate_aplica.regla.v1",
            _relationship_type_payload(),
        )
    elif scenario == "cardinality_constraint_violation":
        contracts = _minimal_entity_contracts()
        contracts["contracts/relacion/relacion.actor.falla_en.estado.v1.json"] = _relationship_contract(
            "relacion.actor.falla_en.estado.v1",
            _relationship_type_payload("actor", "falla_en", "estado", "N:1"),
        )
        contracts["contracts/relacion/relacion.actor.test_actor.falla_en.estado.first.v1.json"] = _relationship_contract(
            "relacion.actor.test_actor.falla_en.estado.first.v1",
            _relationship_payload("actor", "actor.test_actor.v1", "falla_en", "estado", "estado.first.v1", "N:1"),
        )
        contracts["contracts/relacion/relacion.actor.test_actor.falla_en.estado.second.v1.json"] = _relationship_contract(
            "relacion.actor.test_actor.falla_en.estado.second.v1",
            _relationship_payload("actor", "actor.test_actor.v1", "falla_en", "estado", "estado.second.v1", "N:1"),
        )
    elif scenario == "invalid_requerido":
        contracts["contracts/relacion/relacion.actor.aplica.regla.v1.json"]["payload"]["requerido"] = True
    elif scenario == "duplicate_order_slot":
        return _ordered_workflow_contracts(duplicate=True)
    elif scenario == "order_gap":
        return _ordered_workflow_contracts(gap=True)
    elif scenario == "order_required":
        return _ordered_workflow_contracts(missing_order=True)
    elif scenario == "order_not_allowed":
        contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"]["payload"]["orden"] = 1
    elif scenario == "selected_placeholder_ref":
        contracts["contracts/relacion/relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1.json"] = _relationship_contract(
            "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1",
            _placeholder_relationship_payload(),
        )
        _add_resolver_output(contracts, ["relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1"])
    elif scenario == "selected_deprecated_ref":
        contracts["contracts/relacion/relacion.actor.test_actor.aplica.regla.test_rule.v1.json"]["status"] = "deprecated"
        _add_resolver_output(contracts, ["relacion.actor.test_actor.aplica.regla.test_rule.v1"])
    elif scenario == "selected_type_ref":
        _add_resolver_output(contracts, ["relacion.actor.aplica.regla.v1"])
    elif scenario == "missing_resolver_support_link":
        _add_resolver_output(contracts, ["relacion.actor.test_actor.aplica.regla.test_rule.v1"])
    elif scenario == "support_link_target_invalid":
        _add_resolver_support_contracts(contracts)
        support_path = (
            "contracts/relacion/"
            "relacion.resolver.test_resolver.usa.relacion.actor_test_actor_aplica_regla_test_rule.v1.json"
        )
        contracts[support_path]["payload"]["destino_id"] = "relacion.actor.aplica.regla.v1"
    else:
        raise AssertionError(f"unknown relationship fixture scenario: {scenario}")
    return contracts


def _materialize_relationship_fixture(root: Path, metadata: dict[str, object]) -> None:
    _copy_schemas(root)
    scenario = metadata.get("scenario")
    if not isinstance(scenario, str):
        raise AssertionError(f"fixture missing scenario: {metadata.get('fixture_id')}")
    for relative_path, data in _contracts_for_relationship_scenario(scenario).items():
        _write_json(root / relative_path, data)


def _support_boundary_policy(*, generated: bool = False, generator_ref: object = None) -> dict[str, object]:
    policy = {
        "generated": generated,
        "static_curated": True,
        "complete_inventory": False,
        "loader_behavior": False,
        "runtime_behavior": False,
        "selector_runtime_behavior": False,
        "resolver_behavior": False,
        "write_authorization_behavior": False,
    }
    if generator_ref is not None:
        policy["generator_ref"] = generator_ref
    return policy


def _support_discovery_policy(*, complete_inventory: bool = False) -> dict[str, object]:
    return {
        "curated_support_discovery_only": True,
        "complete_inventory": complete_inventory,
        "loader_behavior": False,
        "runtime_behavior": False,
        "selector_runtime_behavior": False,
        "resolver_behavior": False,
        "write_authorization_behavior": False,
    }


def _support_contract_entries() -> list[dict[str, object]]:
    entries = [
        ("resolver.test_resolver.v1", "contracts/resolver/resolver.test_resolver.v1.json", "resolver", "entity"),
        ("manifest.test_support.v1", "contracts/manifest.json", "manifest", "manifest"),
        ("index.test_support.v1", "contracts/index.json", "index", "index"),
        ("policy.test_support.v1", "contracts/policy/policy.test_support.v1.json", "policy", "reference_bundle"),
        ("selector.test_support.v1", "contracts/selector/selector.test_support.v1.json", "selector", "selector"),
        (
            "resolver_output.test_support.v1",
            "contracts/resolver_output/resolver_output.test_support.v1.json",
            "resolver_output",
            "entity",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "path": path,
            "entity_family": family,
            "contract_kind": kind,
            "version": {"major": 1},
            "status": "draft",
        }
        for contract_id, path, family, kind in entries
    ]


def _support_contract_family_entries() -> list[dict[str, object]]:
    families = [
        ("resolver", "contracts/resolver/", "entity"),
        ("resolver_output", "contracts/resolver_output/", "entity"),
        ("actor", "contracts/actor/", "entity"),
        ("estado", "contracts/estado/", "entity"),
        ("relacion", "contracts/relacion/", "relationship"),
        ("policy", "contracts/policy/", "reference_bundle"),
        ("manifest", "contracts/", "manifest"),
        ("index", "contracts/", "index"),
        ("selector", "contracts/selector/", "selector"),
    ]
    return [
        {
            "entity_family": family,
            "directory_path": directory,
            "contract_kind": kind,
            "status_policy": "draft_static_reference_only",
        }
        for family, directory, kind in families
    ]


def _index_lookup_groups() -> list[dict[str, object]]:
    entries = _support_contract_entries()
    return [
        {
            "lookup_group": "by_contract_id",
            "lookup_source_ref": "manifest.contract_entries.contract_id",
            "entries": [
                {"lookup_key": entry["contract_id"], "contract_refs": [entry["contract_id"]]}
                for entry in entries
            ],
        },
        {
            "lookup_group": "by_path",
            "lookup_source_ref": "manifest.contract_entries.path",
            "entries": [
                {"lookup_key": entry["path"], "contract_refs": [entry["contract_id"]]}
                for entry in entries
            ],
        },
        {
            "lookup_group": "by_selector_dimension",
            "lookup_source_ref": "selector.dimension_contract_family_map",
            "entries": [
                {"lookup_key": dimension, "contract_family_refs": families}
                for dimension, families in SUPPORT_SELECTOR_DIMENSIONS.items()
            ],
        },
    ]


def _base_support_contracts() -> dict[str, dict[str, object]]:
    manifest_payload = {
        "nombre": "test support manifest",
        "manifest_kind": "curated_static_support_discovery_bundle",
        "contract_root_path": "contracts/",
        "inventory_scope": "curated_support_discovery_subset_not_complete_inventory",
        "support_discovery_policy": _support_discovery_policy(),
        "deprecated_reserved_relationship_refs": [],
        "resolver_refs": ["resolver.test_resolver.v1"],
        "policy_bundle_refs": ["policy.test_support.v1"],
        "index_refs": ["index.test_support.v1"],
        "selector_refs": ["selector.test_support.v1"],
        "represented_entity_families": ["resolver", "resolver_output", "actor", "estado", "relacion"],
        "represented_static_reference_sets": ["policy", "manifest", "index", "selector"],
        "contract_family_entries": _support_contract_family_entries(),
        "contract_entries": _support_contract_entries(),
        "relationship_family_entries": [],
        "relationship_contract_entries": [],
        "body_inclusion_policy": "references_only_no_contract_bodies",
        "live_evidence_policy": "github_live_evidence_not_copied",
        "curation_policy": _support_boundary_policy(),
    }
    index_payload = {
        "nombre": "test support index",
        "index_kind": "static_curated_discoverability_index",
        "source_of_truth_policy": "curated_from_manifest_support_entries_not_complete_inventory_not_canonical",
        "manifest_ref": "manifest.test_support.v1",
        "policy_ref": "policy.test_support.v1",
        "selector_refs": ["selector.test_support.v1"],
        "resolver_refs": ["resolver.test_resolver.v1"],
        "index_scope_policy": _support_discovery_policy(),
        "deprecated_reserved_relationship_refs": [],
        "lookup_groups": _index_lookup_groups(),
        "body_inclusion_policy": "references_only_no_payload_duplication",
        "generation_policy": _support_boundary_policy() | {"generator_ref": None},
    }
    policy_payload = {
        "nombre": "test support policy",
        "bundle_kind": "policy_reference_bundle",
        "applies_to_resolver_refs": ["resolver.test_resolver.v1"],
        "allowed_actor_refs": ["actor.test_actor.v1"],
        "limit_refs": [],
        "rule_refs": [],
        "state_refs": ["estado.resolved.v1", "estado.blocked.v1"],
        "source_authority_refs": [],
        "evidence_category_refs": [],
        "relationship_type_refs": [],
        "relationship_instance_refs": {
            "actor_limit_refs": [],
            "role_rule_refs": [],
            "limit_failure_state_refs": [],
            "rule_failure_state_refs": [],
        },
        "tooling_gate_refs": [],
        "fallback_estado_ref": "estado.blocked.v1",
        "schema_ref_policy": {"input_schema_ref": None, "output_schema_ref": None},
        "static_data_refs": {
            "manifest_ref": "manifest.test_support.v1",
            "index_ref": "index.test_support.v1",
            "selector_refs": ["selector.test_support.v1"],
        },
    }
    selector_entries = [
        {
            "dimension": dimension,
            "candidate_contract_family_refs": families,
            "candidate_output_ref_groups": ["selected_actor_refs"] if dimension == "actor_type" else ["selected_relacion_refs"],
        }
        for dimension, families in SUPPORT_SELECTOR_DIMENSIONS.items()
    ]
    selector_payload = {
        "nombre": "test support selector",
        "selector_kind": "static_candidate_reference_selector",
        "manifest_ref": "manifest.test_support.v1",
        "index_ref": "index.test_support.v1",
        "policy_ref": "policy.test_support.v1",
        "resolver_ref": "resolver.test_resolver.v1",
        "allowed_dimensions": list(SUPPORT_SELECTOR_DIMENSIONS),
        "dimension_contract_family_map": {dimension: list(families) for dimension, families in SUPPORT_SELECTOR_DIMENSIONS.items()},
        "selector_entries": selector_entries,
        "output_ref_groups": list(SUPPORT_OUTPUT_GROUPS),
        "body_inclusion_policy": "references_only_no_entity_or_relationship_payloads",
        "execution_policy": "no_runtime_no_permission_no_tool_execution",
    }
    resolver_output_payload = _resolver_output_payload()
    resolver_output_payload.update(
        {
            "resolver_ref": "resolver.test_resolver.v1",
            "manifest_ref": "manifest.test_support.v1",
            "index_ref": "index.test_support.v1",
            "policy_ref": "policy.test_support.v1",
            "selector_refs": ["selector.test_support.v1"],
            "estado_ref": "estado.resolved.v1",
            "fallback_estado_ref": "estado.blocked.v1",
            "selected_estado_refs": ["estado.resolved.v1", "estado.blocked.v1"],
            "selected_actor_refs": ["actor.test_actor.v1"],
        }
    )

    return {
        "contracts/manifest.json": _support_envelope("manifest.test_support.v1", "manifest", manifest_payload),
        "contracts/index.json": _support_envelope("index.test_support.v1", "index", index_payload),
        "contracts/policy/policy.test_support.v1.json": _support_envelope("policy.test_support.v1", "reference_bundle", policy_payload),
        "contracts/selector/selector.test_support.v1.json": _support_envelope("selector.test_support.v1", "selector", selector_payload),
        "contracts/resolver/resolver.test_resolver.v1.json": _contract_envelope(
            "resolver.test_resolver.v1",
            "resolver",
            {
                "nombre": "test resolver",
                "manifest_ref": "manifest.test_support.v1",
                "policy_ref": "policy.test_support.v1",
                "input_schema_ref": None,
                "output_schema_ref": None,
                "fallback_estado_id": "estado.blocked.v1",
            },
        ),
        "contracts/actor/actor.test_actor.v1.json": _contract_envelope(
            "actor.test_actor.v1",
            "actor",
            {"nombre": "test actor", "superficie_capacidad": "terminal"},
        ),
        "contracts/estado/estado.resolved.v1.json": _contract_envelope("estado.resolved.v1", "estado", {"nombre": "resolved"}),
        "contracts/estado/estado.blocked.v1.json": _contract_envelope("estado.blocked.v1", "estado", {"nombre": "blocked"}),
        "contracts/resolver_output/resolver_output.test_support.v1.json": _contract_envelope(
            "resolver_output.test_support.v1",
            "resolver_output",
            resolver_output_payload,
        ),
    }


def _mutate_support_contracts(contracts: dict[str, dict[str, object]], scenario: str) -> None:
    manifest = contracts["contracts/manifest.json"]["payload"]
    index = contracts["contracts/index.json"]["payload"]
    policy = contracts["contracts/policy/policy.test_support.v1.json"]["payload"]
    selector = contracts["contracts/selector/selector.test_support.v1.json"]["payload"]

    if scenario in {
        "valid_minimal_support_bundle",
        "valid_deprecated_provenance_refs",
        "valid_selector_output_groups",
        "valid_resolver_output_support_refs",
        "safe_support_denial_reference_only_wording",
    }:
        if scenario == "valid_deprecated_provenance_refs":
            contracts["contracts/relacion/relacion.plantilla.compone.artefacto.v1.json"] = _relationship_contract(
                "relacion.plantilla.compone.artefacto.v1",
                _relationship_type_payload("plantilla", "compone", "artefacto"),
            )
            contracts["contracts/relacion/relacion.plantilla.genera.artefacto.v1.json"] = _relationship_contract(
                "relacion.plantilla.genera.artefacto.v1",
                _relationship_type_payload("plantilla", "genera", "artefacto"),
                status="deprecated",
            )
            manifest["deprecated_reserved_relationship_refs"] = [
                {
                    "relationship_type_ref": "relacion.plantilla.genera.artefacto.v1",
                    "provenance_discoverable_only": True,
                    "active_resolver_candidate": False,
                    "canonical_replacement_ref": "relacion.plantilla.compone.artefacto.v1",
                }
            ]
        return

    if scenario == "manifest_index_parity_drift":
        index["lookup_groups"][0]["entries"] = index["lookup_groups"][0]["entries"][1:]
    elif scenario == "generated_inventory_claim":
        manifest["support_discovery_policy"]["complete_inventory"] = True
    elif scenario == "generated_index_claim":
        index["generation_policy"]["generated"] = True
    elif scenario == "active_deprecated_ref":
        contracts["contracts/actor/actor.test_actor.v1.json"]["status"] = "deprecated"
    elif scenario == "missing_support_ref":
        policy["allowed_actor_refs"][0] = "actor.missing.v1"
    elif scenario == "placeholder_support_ref":
        contracts["contracts/relacion/relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1.json"] = _relationship_contract(
            "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1",
            _placeholder_relationship_payload(),
        )
        policy["relationship_instance_refs"]["actor_limit_refs"] = [
            "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1"
        ]
    elif scenario == "selector_output_group_drift":
        selector["output_ref_groups"].append("rendered_output_body")
    elif scenario == "selector_dimension_index_drift":
        index["lookup_groups"][2]["entries"][0]["contract_family_refs"] = ["rol"]
    elif scenario == "policy_static_data_ref_drift":
        policy["static_data_refs"]["index_ref"] = "index.other.v1"
    elif scenario == "invalid_policy_fallback_estado":
        policy["state_refs"] = ["estado.blocked.v1"]
        policy["fallback_estado_ref"] = "estado.resolved.v1"
    elif scenario == "copied_relationship_payload_body":
        manifest["relationship_payload"] = {
            "origen_entidad": "actor",
            "origen_id": "actor.test_actor.v1",
            "tipo_relacion": "tiene",
            "destino_entidad": "limite",
            "destino_id": "limite.test.v1",
        }
    elif scenario == "template_execution_claim":
        selector["execution_policy"] = "template execution renders generated output"
    elif scenario == "command_execution_claim":
        selector["execution_policy"] = "command execution runs shell"
    elif scenario == "permission_write_claim":
        selector["execution_policy"] = "write authorization grants permission"
    else:
        raise AssertionError(f"unknown support fixture scenario: {scenario}")


def _materialize_support_fixture(root: Path, metadata: dict[str, object]) -> None:
    _copy_schemas(root)
    scenario = metadata.get("scenario")
    if not isinstance(scenario, str):
        raise AssertionError(f"fixture missing scenario: {metadata.get('fixture_id')}")
    contracts = _base_support_contracts()
    _mutate_support_contracts(contracts, scenario)
    for relative_path, data in contracts.items():
        _write_json(root / relative_path, data)


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


class RelationshipSemanticFixtureTests(unittest.TestCase):
    def test_positive_relationship_semantic_fixtures_pass(self) -> None:
        fixture_root = RELATIONSHIP_FIXTURE_ROOT / "positive" / "relationship_semantics"
        metadata_files = sorted(fixture_root.glob("*/metadata.json"))
        self.assertTrue(metadata_files, "expected positive relationship semantic fixtures")

        for metadata_path in metadata_files:
            with self.subTest(fixture=metadata_path.parent.name):
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                with tempfile.TemporaryDirectory() as raw_root:
                    root = Path(raw_root)
                    _materialize_relationship_fixture(root, metadata)

                    findings = validate_all(root)

                self.assertEqual([], findings)

    def test_negative_relationship_semantic_fixtures_report_expected_primary_finding(self) -> None:
        fixture_root = RELATIONSHIP_FIXTURE_ROOT / "negative" / "relationship_semantics"
        metadata_files = sorted(fixture_root.glob("*/*/metadata.json"))
        self.assertTrue(metadata_files, "expected negative relationship semantic fixtures")

        for metadata_path in metadata_files:
            with self.subTest(fixture=metadata_path.parent.name):
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                expected = metadata["expected_primary_finding"]
                expected_code = expected["code"]
                allowed_codes = {expected_code, *metadata.get("allowed_collateral_findings", [])}
                forbidden_codes = set(metadata.get("forbidden_finding_codes", []))

                with tempfile.TemporaryDirectory() as raw_root:
                    root = Path(raw_root)
                    _materialize_relationship_fixture(root, metadata)

                    findings = validate_all(root)

                finding_dicts = [finding.as_dict() for finding in findings]
                primary_matches = [
                    finding
                    for finding in finding_dicts
                    if finding["code"] == expected_code
                    and finding["severity"] == expected["severity"]
                    and finding["file"] == expected["file"]
                    and finding["pointer"] == expected["pointer"]
                    and finding["contract_id"] == expected["contract_id"]
                ]
                self.assertTrue(primary_matches, finding_dicts)
                self.assertFalse(forbidden_codes & {finding.code for finding in findings}, finding_dicts)
                unexpected_codes = {finding.code for finding in findings} - allowed_codes
                self.assertFalse(unexpected_codes, finding_dicts)


class SupportBundleFixtureTests(unittest.TestCase):
    def test_positive_support_bundle_fixtures_pass(self) -> None:
        fixture_root = SUPPORT_FIXTURE_ROOT / "positive" / "support_bundle"
        metadata_files = sorted(fixture_root.glob("*/metadata.json"))
        self.assertTrue(metadata_files, "expected positive support-bundle fixtures")

        for metadata_path in metadata_files:
            with self.subTest(fixture=metadata_path.parent.name):
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                with tempfile.TemporaryDirectory() as raw_root:
                    root = Path(raw_root)
                    _materialize_support_fixture(root, metadata)

                    findings = validate_all(root)

                self.assertEqual([], findings)

    def test_negative_support_bundle_fixtures_report_expected_primary_finding(self) -> None:
        fixture_root = SUPPORT_FIXTURE_ROOT / "negative" / "support_bundle"
        metadata_files = sorted(fixture_root.glob("*/*/metadata.json"))
        self.assertTrue(metadata_files, "expected negative support-bundle fixtures")

        for metadata_path in metadata_files:
            with self.subTest(fixture=metadata_path.parent.name):
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                expected = metadata["expected_primary_finding"]
                expected_code = expected["code"]
                allowed_codes = {expected_code, *metadata.get("allowed_collateral_findings", [])}
                forbidden_codes = set(metadata.get("forbidden_finding_codes", []))

                with tempfile.TemporaryDirectory() as raw_root:
                    root = Path(raw_root)
                    _materialize_support_fixture(root, metadata)

                    findings = validate_all(root)

                finding_dicts = [finding.as_dict() for finding in findings]
                primary_matches = [
                    finding
                    for finding in finding_dicts
                    if finding["code"] == expected_code
                    and finding["severity"] == expected["severity"]
                    and finding["file"] == expected["file"]
                    and finding["pointer"] == expected["pointer"]
                    and finding["contract_id"] == expected["contract_id"]
                ]
                self.assertTrue(primary_matches, finding_dicts)
                self.assertFalse(forbidden_codes & {finding.code for finding in findings}, finding_dicts)
                unexpected_codes = {finding.code for finding in findings} - allowed_codes
                self.assertFalse(unexpected_codes, finding_dicts)


if __name__ == "__main__":
    unittest.main()
