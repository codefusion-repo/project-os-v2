"""Read-only Project OS v2 schema, reference, and ownership validators."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .jsonschema_subset import (
    Draft202012SubsetValidator,
    SchemaRegistry,
    escape_pointer_token,
    iter_refs,
    join_pointer,
)
from .models import Finding, ToolingError


SCHEMA_ID_PREFIX = "https://schemas.project-os-v2.local/"
DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
STABLE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+\.v[0-9]+$")
WORKFLOW_STEP_REGLA_ID_RE = re.compile(r"^regla\.workflow_step_[a-z0-9_]+_.*\.v1$")
ENTITY_FAMILIES = {
    "accion",
    "actor",
    "artefacto",
    "contrato",
    "estado",
    "evidencia",
    "fuente",
    "limite",
    "plantilla",
    "recurso",
    "regla",
    "relacion",
    "resolver",
    "resolver_output",
    "rol",
    "scope",
    "variable",
    "workflow",
    "workflow_step",
}
SUPPORT_KINDS = {
    "manifest": "https://schemas.project-os-v2.local/support/manifest.bundle.v1.schema.json",
    "index": "https://schemas.project-os-v2.local/support/index.bundle.v1.schema.json",
    "reference_bundle": "https://schemas.project-os-v2.local/support/policy.bundle.v1.schema.json",
    "selector": "https://schemas.project-os-v2.local/support/selector.bundle.v1.schema.json",
}
REF_FIELD_EXCLUSIONS = {
    "schema_ref",
    "input_schema_ref",
    "output_schema_ref",
    "source_refs",
    "lookup_source_ref",
    "relationship_type_refs_source",
}
FORBIDDEN_TRUE_FIELDS = {
    "complete_inventory",
    "loader_behavior",
    "runtime_behavior",
    "selector_runtime_behavior",
    "resolver_behavior",
    "write_authorization_behavior",
    "generated",
}
STATIC_TRUE_FIELDS = {"curated_support_discovery_only", "static_curated"}
ENTITY_PAYLOAD_ALLOWED_KEYS = {
    "accion": {"nombre", "tipo"},
    "actor": {"nombre", "superficie_capacidad"},
    "artefacto": {"nombre", "referencia", "tipo"},
    "contrato": {"entidad_tipo", "nombre"},
    "estado": {"nombre"},
    "evidencia": {"referencia", "tipo"},
    "fuente": {"frescura_requerida", "nivel_autoridad", "nombre", "tipo", "ubicacion"},
    "limite": {"nombre", "severidad", "tipo"},
    "plantilla": {"formato", "nombre", "secciones_requeridas", "tipo"},
    "recurso": {"nombre", "tipo", "ubicacion"},
    "regla": {"comportamiento_esperado", "condicion", "nombre"},
    "resolver": {"fallback_estado_id", "input_schema_ref", "manifest_ref", "nombre", "output_schema_ref", "policy_ref"},
    "resolver_output": {
        "allowed_output_contract_ref",
        "effective_limite_refs",
        "effective_regla_refs",
        "estado_ref",
        "fallback_estado_ref",
        "index_ref",
        "manifest_ref",
        "missing_evidence_refs",
        "output_template_ref",
        "policy_ref",
        "reasons",
        "required_evidence_refs",
        "resolution_trace",
        "resolver_ref",
        "response_shape_ref",
        "selected_accion_refs",
        "selected_actor_refs",
        "selected_artefacto_refs",
        "selected_contrato_refs",
        "selected_estado_refs",
        "selected_evidencia_refs",
        "selected_fuente_refs",
        "selected_limite_refs",
        "selected_plantilla_refs",
        "selected_recurso_refs",
        "selected_regla_refs",
        "selected_relacion_refs",
        "selected_rol_refs",
        "selected_scope_refs",
        "selected_variable_refs",
        "selected_workflow_refs",
        "selected_workflow_step_refs",
        "selector_refs",
        "source_provenance_refs",
        "status",
    },
    "rol": {"lente_profesional", "nombre"},
    "scope": {"nombre"},
    "variable": {"nombre", "tipo", "valor_default", "valores_permitidos"},
    "workflow": {"etapa_ciclo_vida", "nombre"},
    "workflow_step": {
        "condicion_base_avance",
        "condicion_base_bloqueo",
        "condicion_base_repeticion",
        "nombre",
        "objetivo",
    },
}
ENTITY_CROSS_FAMILY_REF_EXCEPTIONS = {
    "resolver": {"fallback_estado_id", "manifest_ref", "policy_ref"},
    "resolver_output": ENTITY_PAYLOAD_ALLOWED_KEYS["resolver_output"],
}
RELATIONSHIP_OWNED_KEYS = {
    "cardinalidad",
    "destino_entidad",
    "destino_id",
    "orden",
    "origen_entidad",
    "origen_id",
    "requerido",
    "tipo_relacion",
}
SUPPORT_PAYLOAD_ALLOWED_KEYS = {
    "manifest": {
        "body_inclusion_policy",
        "contract_entries",
        "contract_family_entries",
        "contract_root_path",
        "curation_policy",
        "deprecated_reserved_relationship_refs",
        "index_refs",
        "inventory_scope",
        "live_evidence_policy",
        "manifest_kind",
        "nombre",
        "policy_bundle_refs",
        "relationship_contract_entries",
        "relationship_family_entries",
        "represented_entity_families",
        "represented_static_reference_sets",
        "resolver_refs",
        "selector_refs",
        "support_discovery_policy",
    },
    "index": {
        "body_inclusion_policy",
        "deprecated_reserved_relationship_refs",
        "generation_policy",
        "index_kind",
        "index_scope_policy",
        "lookup_groups",
        "manifest_ref",
        "nombre",
        "policy_ref",
        "resolver_refs",
        "selector_refs",
        "source_of_truth_policy",
    },
    "reference_bundle": {
        "allowed_actor_refs",
        "applies_to_resolver_refs",
        "bundle_kind",
        "evidence_category_refs",
        "fallback_estado_ref",
        "limit_refs",
        "nombre",
        "relationship_instance_refs",
        "relationship_type_refs",
        "rule_refs",
        "schema_ref_policy",
        "source_authority_refs",
        "state_refs",
        "static_data_refs",
        "tooling_gate_refs",
    },
    "selector": {
        "allowed_dimensions",
        "body_inclusion_policy",
        "dimension_contract_family_map",
        "execution_policy",
        "index_ref",
        "manifest_ref",
        "nombre",
        "output_ref_groups",
        "policy_ref",
        "resolver_ref",
        "selector_entries",
        "selector_kind",
    },
}
SUPPORT_REQUIRED_OWNER_KEYS = {
    "manifest": {"contract_entries", "contract_family_entries", "support_discovery_policy"},
    "index": {"generation_policy", "index_scope_policy", "lookup_groups"},
    "reference_bundle": {"bundle_kind", "static_data_refs"},
    "selector": {"dimension_contract_family_map", "execution_policy", "selector_entries"},
}
SUPPORT_BODY_COPY_KEYS = {
    "body",
    "bodies",
    "contract_body",
    "contract_bodies",
    "content",
    "contents",
    "entity_payload",
    "generated_output",
    "payload_body",
    "payload_copy",
    "payloads",
    "rendered_template",
    "relationship_payload",
}
LIVE_STATE_KEYS = {
    "actual_head",
    "base_ref",
    "branch_name",
    "branch_ref",
    "branch_sha",
    "branch_state",
    "check_run_status",
    "check_suite_status",
    "closed",
    "closed_at",
    "closure_state",
    "current_branch",
    "current_head",
    "current_sha",
    "github_issue_number",
    "github_issue_state",
    "github_pr_number",
    "github_pr_state",
    "head_branch",
    "head_ref",
    "head_sha",
    "is_draft",
    "issue_number",
    "issue_state",
    "latest_commit",
    "merge_commit",
    "merge_state",
    "mergeable",
    "merged",
    "merged_at",
    "pr_number",
    "pr_state",
    "pull_request_number",
    "pull_request_state",
    "release_state",
    "release_status",
    "review_decision",
    "review_state",
    "review_status",
    "review_verdict",
    "tag_name",
    "validation_exit_code",
    "validation_output",
    "validation_result",
    "validation_results",
    "validation_status",
    "workflow_run_status",
}
LIVE_STATE_VALUE_PATTERNS = (
    re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/(issues|pull)/[0-9]+"),
    re.compile(r"\b[0-9a-f]{40}\b"),
)
ACTOR_HARD_LIMIT_DUPLICATION_KEYS = {
    "actor_hard_limit",
    "actor_hard_limits",
    "actor_limit_refs",
    "blocked_actions",
    "denied_actions",
    "hard_limit",
    "hard_limits",
    "limit_refs",
    "limite_refs",
    "no_write_boundary",
    "prohibited_actions",
    "write_boundary",
}
RESOLVER_OUTPUT_LIMITE_REF_REFERENCE_KEYS = {
    "effective_limite_refs",
    "selected_limite_refs",
}
ROLE_PERMISSION_KEYS = {
    "allowed_actions",
    "authority",
    "can_close",
    "can_commit",
    "can_merge",
    "can_push",
    "can_write",
    "capabilities",
    "grant",
    "grants",
    "permission",
    "permissions",
    "write_authorization",
    "write_permission",
}
ROLE_PERMISSION_VALUE_RE = re.compile(
    r"\b(can|may|grant|grants|permission|permissions|authorize|authorized|allowed_to|write_access|commit|push|merge|close_issue)\b"
)
BEHAVIOR_SCHEMA_DENIAL_FIELDS = FORBIDDEN_TRUE_FIELDS | {
    "command_execution_behavior",
    "policy_execution",
    "selector_behavior",
}
RELATIONSHIP_RETIRED_STATUSES = {"deprecated", "retired"}
ORDERED_RELATIONSHIP_TYPE_TUPLES = {
    ("fuente", "informa", "estado"),
    ("resolver", "determina", "estado"),
    ("workflow", "compone", "workflow_step"),
}
SUPPORT_ACTIVE_STATUSES = {"active", "draft"}
RESOLVER_OUTPUT_SELECTOR_GROUPS = {
    key
    for key in ENTITY_PAYLOAD_ALLOWED_KEYS["resolver_output"]
    if (key.endswith("_ref") or key.endswith("_refs"))
    and key
    not in {
        "effective_limite_refs",
        "effective_regla_refs",
        "index_ref",
        "manifest_ref",
        "policy_ref",
        "resolver_ref",
        "selector_refs",
        "source_provenance_refs",
    }
}
SUPPORT_GENERATED_INDEX_KEYS = {
    "build_metadata",
    "cache_key",
    "generated_at",
    "generated_by",
    "generator_ref",
    "hash",
    "scan_root",
    "source_command",
}
SUPPORT_COMMAND_KEYS = {
    "argv",
    "command",
    "command_bundle",
    "command_bundles",
    "commands",
    "execute",
    "script",
    "shell",
    "source_command",
    "tool_execution",
}
SUPPORT_PERMISSION_KEYS = {
    "allowed_write_actions",
    "can_close",
    "can_commit",
    "can_merge",
    "can_push",
    "can_write",
    "permission_grant",
    "permission_grants",
    "permissions",
    "write_authorization",
    "write_authorization_behavior",
    "write_permission",
}
SUPPORT_TEMPLATE_EXECUTION_KEYS = {
    "body_file_generation",
    "generated_body",
    "generated_output",
    "interpolation",
    "rendered_template",
    "template_execution",
}
SUPPORT_COMMAND_CLAIM_RE = re.compile(r"\b(command|shell|argv|script|tool)\s+(execution|execute|run|runs|invoke|invocation)\b")
SUPPORT_TEMPLATE_CLAIM_RE = re.compile(
    r"\b(generated output|generated body|rendered template|template execution|interpolation|body file|body generation)\b"
)
SUPPORT_PERMISSION_CLAIM_RE = re.compile(
    r"\b(permission grant|write authorization|write permission|can write|can commit|can push|can merge|can close|merge authority|release authority|settings authority)\b"
)
SUPPORT_GENERATED_INVENTORY_CLAIM_RE = re.compile(
    r"\b(complete inventory|generated inventory|generated manifest|automatic discovery|filesystem scan|full repository inventory)\b"
)
SUPPORT_GENERATED_INDEX_CLAIM_RE = re.compile(
    r"\b(generated index|generator|command derived|scan output|build artifact|cache metadata)\b"
)


def validate_r1_10(root: Path | str) -> list[Finding]:
    root = Path(root)
    if not root.exists():
        raise ToolingError(f"root does not exist: {root}")
    if not root.is_dir():
        raise ToolingError(f"root is not a directory: {root}")

    findings: list[Finding] = []
    parsed: dict[Path, Any] = {}
    schema_files = _json_files(root / "schemas")
    contract_files = _json_files(root / "contracts")

    for path in [*schema_files, *contract_files]:
        try:
            parsed[path] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(
                _finding(
                    "JSON_SYNTAX_INVALID",
                    path,
                    "/",
                    None,
                    "valid JSON",
                    f"{exc.msg} at line {exc.lineno} column {exc.colno}",
                    "Fix JSON syntax so the file can be parsed.",
                    root,
                )
            )

    schema_registry, schema_findings = _build_schema_registry(root, schema_files, parsed)
    findings.extend(schema_findings)
    contract_index, path_by_id = _build_contract_index(root, contract_files, parsed, findings)

    _validate_required_fields(root, contract_files, parsed, findings)
    _validate_stable_ids(root, contract_files, parsed, findings)
    _validate_path_family_kind(root, contract_files, parsed, findings)
    _validate_schema_refs(root, contract_files, parsed, schema_registry, findings)
    _validate_contracts_against_schemas(root, contract_files, parsed, schema_registry, findings)
    _validate_contract_references(root, contract_files, parsed, contract_index, path_by_id, findings)
    _validate_relationships(root, contract_files, parsed, contract_index, findings)
    _validate_support_boundaries(root, schema_files, contract_files, parsed, contract_index, findings)
    _validate_deprecated_relationships(root, contract_files, parsed, contract_index, findings)
    _validate_support_bundle_semantics(root, contract_files, parsed, contract_index, path_by_id, findings)

    return sorted(findings, key=lambda item: (item.file, item.pointer, item.code))


def validate_r1_11(root: Path | str) -> list[Finding]:
    root = Path(root)
    if not root.exists():
        raise ToolingError(f"root does not exist: {root}")
    if not root.is_dir():
        raise ToolingError(f"root is not a directory: {root}")

    findings: list[Finding] = []
    parsed: dict[Path, Any] = {}
    schema_files = _json_files(root / "schemas")
    contract_files = _json_files(root / "contracts")

    for path in [*schema_files, *contract_files]:
        try:
            parsed[path] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(
                _finding(
                    "JSON_SYNTAX_INVALID",
                    path,
                    "/",
                    None,
                    "valid JSON",
                    f"{exc.msg} at line {exc.lineno} column {exc.colno}",
                    "Fix JSON syntax so semantic ownership validators can inspect the file.",
                    root,
                )
            )

    contract_index, _path_by_id = _build_contract_index(root, contract_files, parsed, findings)

    _validate_entity_payload_ownership(root, contract_files, parsed, findings)
    _validate_relationship_ownership(root, contract_files, parsed, findings)
    _validate_support_reference_only_ownership(root, contract_files, parsed, findings)
    _validate_durable_live_state_boundary(root, schema_files, contract_files, parsed, findings)
    _validate_actor_hard_limit_duplication(root, contract_files, parsed, findings)
    _validate_role_permission_boundary(root, contract_files, parsed, findings)
    _validate_workflow_step_rule_ownership(root, contract_files, parsed, findings)
    _validate_deprecated_relationship_active_candidates(root, contract_files, parsed, contract_index, findings)
    _validate_behavior_claim_boundaries(root, schema_files, contract_files, parsed, findings)

    return sorted(findings, key=lambda item: (item.file, item.pointer, item.code))


def validate_all(root: Path | str) -> list[Finding]:
    root = Path(root)
    findings = [*validate_r1_10(root), *validate_r1_11(root)]
    return sorted(findings, key=lambda item: (item.file, item.pointer, item.code))


def _json_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def _build_schema_registry(
    root: Path,
    schema_files: list[Path],
    parsed: dict[Path, Any],
) -> tuple[SchemaRegistry, list[Finding]]:
    registry = SchemaRegistry()
    findings: list[Finding] = []
    seen: dict[str, Path] = {}

    for path in schema_files:
        schema = parsed.get(path)
        if not isinstance(schema, dict):
            continue
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            findings.append(
                _finding(
                    "SCHEMA_ID_REQUIRED",
                    path,
                    "/$id",
                    None,
                    "schema $id string",
                    schema_id,
                    "Add a stable absolute schema $id.",
                    root,
                )
            )
            continue
        if schema_id in seen:
            findings.append(
                _finding(
                    "SCHEMA_ID_DUPLICATE",
                    path,
                    "/$id",
                    None,
                    f"unique schema $id not already used by {_rel(root, seen[schema_id])}",
                    schema_id,
                    "Give each schema file a unique $id.",
                    root,
                )
            )
        seen[schema_id] = path
        registry.add(schema_id, schema)

        if schema.get("$schema") != DRAFT_2020_12:
            findings.append(
                _finding(
                    "SCHEMA_DRAFT_MISMATCH",
                    path,
                    "/$schema",
                    None,
                    DRAFT_2020_12,
                    schema.get("$schema"),
                    "Declare JSON Schema Draft 2020-12 for schema files.",
                    root,
                )
            )
        if not schema_id.startswith(SCHEMA_ID_PREFIX):
            findings.append(
                _finding(
                    "SCHEMA_ID_PREFIX",
                    path,
                    "/$id",
                    None,
                    f"{SCHEMA_ID_PREFIX}...",
                    schema_id,
                    "Use the canonical Project OS v2 schema $id prefix.",
                    root,
                )
            )
        expected_suffix = _rel(root, path).removeprefix("schemas/")
        if schema_id.startswith(SCHEMA_ID_PREFIX) and not schema_id.endswith(expected_suffix):
            findings.append(
                _finding(
                    "SCHEMA_ID_PATH_MISMATCH",
                    path,
                    "/$id",
                    None,
                    f"{SCHEMA_ID_PREFIX}{expected_suffix}",
                    schema_id,
                    "Keep schema $id aligned with its path under schemas/.",
                    root,
                )
            )

    for path in schema_files:
        schema = parsed.get(path)
        if not isinstance(schema, dict):
            continue
        for pointer, ref in iter_refs(schema):
            try:
                registry.resolve(ref)
            except KeyError:
                findings.append(
                    _finding(
                        "SCHEMA_REF_UNRESOLVED",
                        path,
                        pointer,
                        None,
                        "resolvable schema $ref",
                        ref,
                        "Reference an existing schema $id and JSON pointer fragment.",
                        root,
                    )
                )

    return registry, findings


def _build_contract_index(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> tuple[dict[str, Any], dict[str, Path]]:
    contract_index: dict[str, Any] = {}
    path_by_id: dict[str, Path] = {}
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        contract_id = data.get("id")
        if not isinstance(contract_id, str):
            continue
        if contract_id in contract_index:
            findings.append(
                _finding(
                    "STABLE_ID_DUPLICATE",
                    path,
                    "/id",
                    contract_id,
                    f"unique id not already used by {_rel(root, path_by_id[contract_id])}",
                    contract_id,
                    "Make contract IDs unique across contracts/**.",
                    root,
                )
            )
        contract_index[contract_id] = data
        path_by_id[contract_id] = path
    return contract_index, path_by_id


def _validate_required_fields(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    base_required = [
        "id",
        "contract_kind",
        "version",
        "status",
        "schema_ref",
        "descripcion",
        "source_refs",
        "payload",
    ]
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        contract_id = _contract_id(data)
        required = list(base_required)
        kind = data.get("contract_kind")
        if kind in {"entity", "relationship"} or path.parent.name in ENTITY_FAMILIES:
            required.insert(1, "entity_family")
        if kind in {"manifest", "index", "reference_bundle", "selector"}:
            required.insert(1, "classification")
        for key in required:
            if key not in data:
                findings.append(
                    _finding(
                        "REQUIRED_FIELD_MISSING",
                        path,
                        "/" + escape_pointer_token(key),
                        contract_id,
                        "present required field",
                        "missing",
                        "Add the required field at the reported JSON pointer.",
                        root,
                    )
                )

        if data.get("contract_kind") == "relationship":
            payload = data.get("payload")
            if isinstance(payload, dict):
                for key in [
                    "origen_entidad",
                    "origen_id",
                    "destino_entidad",
                    "destino_id",
                    "tipo_relacion",
                    "cardinalidad",
                    "requerido",
                    "orden",
                ]:
                    if key not in payload:
                        findings.append(
                            _finding(
                                "REQUIRED_FIELD_MISSING",
                                path,
                                "/payload/" + escape_pointer_token(key),
                                contract_id,
                                "present required relationship payload field",
                                "missing",
                                "Add the required relationship payload field.",
                                root,
                            )
                        )


def _validate_stable_ids(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        contract_id = data.get("id")
        if not isinstance(contract_id, str):
            continue
        if STABLE_ID_RE.fullmatch(contract_id) is None:
            findings.append(
                _finding(
                    "STABLE_ID_GRAMMAR",
                    path,
                    "/id",
                    contract_id,
                    "family.slug.vN stable id",
                    contract_id,
                    "Use lowercase dot-separated stable IDs ending in .vN.",
                    root,
                )
            )


def _validate_path_family_kind(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        rel = _rel(root, path)
        contract_id = _contract_id(data)
        kind = data.get("contract_kind")
        id_value = data.get("id")
        id_family = id_value.split(".", 1)[0] if isinstance(id_value, str) and "." in id_value else None

        expected_family: str | None = None
        expected_kind: str | None = None
        expected_stem: str | None = None
        parts = rel.split("/")
        if len(parts) >= 3 and parts[0] == "contracts" and parts[1] in ENTITY_FAMILIES:
            expected_family = parts[1]
            expected_kind = "relationship" if expected_family == "relacion" else "entity"
            expected_stem = Path(rel).stem
        elif rel == "contracts/manifest.json":
            expected_family = "manifest"
            expected_kind = "manifest"
        elif rel == "contracts/index.json":
            expected_family = "index"
            expected_kind = "index"
        elif rel.startswith("contracts/policy/"):
            expected_family = "policy"
            expected_kind = "reference_bundle"
            expected_stem = Path(rel).stem
        elif rel.startswith("contracts/selector/"):
            expected_family = "selector"
            expected_kind = "selector"
            expected_stem = Path(rel).stem

        if expected_stem and isinstance(id_value, str) and expected_stem != id_value:
            findings.append(
                _finding(
                    "PATH_ID_MISMATCH",
                    path,
                    "/id",
                    contract_id,
                    expected_stem,
                    id_value,
                    "Keep contract id equal to the filename stem.",
                    root,
                )
            )
        if expected_family and id_family != expected_family:
            findings.append(
                _finding(
                    "PATH_FAMILY_MISMATCH",
                    path,
                    "/id",
                    contract_id,
                    f"id prefix {expected_family}",
                    id_family,
                    "Keep the id prefix aligned with the contract family path.",
                    root,
                )
            )
        if expected_kind and kind != expected_kind:
            findings.append(
                _finding(
                    "PATH_KIND_MISMATCH",
                    path,
                    "/contract_kind",
                    contract_id,
                    expected_kind,
                    kind,
                    "Use the contract_kind required by this contract path.",
                    root,
                )
            )
        if expected_family in ENTITY_FAMILIES and data.get("entity_family") != expected_family:
            findings.append(
                _finding(
                    "ENTITY_FAMILY_MISMATCH",
                    path,
                    "/entity_family",
                    contract_id,
                    expected_family,
                    data.get("entity_family"),
                    "Use the entity_family required by this contract path.",
                    root,
                )
            )


def _validate_schema_refs(
    root: Path,
    files: list[Path],
    parsed: dict[Path, Any],
    registry: SchemaRegistry,
    findings: list[Finding],
) -> None:
    for path in files:
        data = parsed.get(path)
        for pointer, key, value in _walk_key_values(data):
            if key not in {"schema_ref", "input_schema_ref", "output_schema_ref"}:
                continue
            if value is None:
                continue
            if not isinstance(value, str) or not registry.has(value):
                findings.append(
                    _finding(
                        "SCHEMA_REF_INVALID",
                        path,
                        pointer,
                        _contract_id(data),
                        "null or existing schema $id",
                        value,
                        "Keep the schema ref null until it is explicitly populated with an existing schema $id.",
                        root,
                    )
                )


def _validate_contracts_against_schemas(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    registry: SchemaRegistry,
    findings: list[Finding],
) -> None:
    if not registry.ids:
        return
    validator = Draft202012SubsetValidator(registry)
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        schema_id = _schema_id_for_contract(data)
        if schema_id is None:
            findings.append(
                _finding(
                    "JSON_SCHEMA_TARGET_UNKNOWN",
                    path,
                    "/contract_kind",
                    _contract_id(data),
                    "contract kind/family with an R1.10 schema",
                    data.get("contract_kind"),
                    "Use a supported contract_kind and entity_family.",
                    root,
                )
            )
            continue
        if not registry.has(schema_id):
            findings.append(
                _finding(
                    "JSON_SCHEMA_TARGET_MISSING",
                    path,
                    "/",
                    _contract_id(data),
                    schema_id,
                    "missing schema",
                    "Add the required schema in a scoped schema issue.",
                    root,
                )
            )
            continue
        schema = registry.resolve(schema_id)
        for issue in validator.validate(data, schema):
            findings.append(
                _finding(
                    issue.code,
                    path,
                    issue.pointer,
                    _contract_id(data),
                    issue.expected,
                    issue.actual,
                    issue.hint,
                    root,
                )
            )


def _schema_id_for_contract(data: dict[str, Any]) -> str | None:
    kind = data.get("contract_kind")
    if kind == "entity":
        family = data.get("entity_family")
        if isinstance(family, str):
            return f"{SCHEMA_ID_PREFIX}families/{family}.contract.v1.schema.json"
    if kind == "relationship":
        return f"{SCHEMA_ID_PREFIX}families/relacion.contract.v1.schema.json"
    if isinstance(kind, str) and kind in SUPPORT_KINDS:
        return SUPPORT_KINDS[kind]
    return None


def _validate_contract_references(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    path_by_id: dict[str, Path],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        for pointer, key, value in _walk_key_values(data):
            if key in REF_FIELD_EXCLUSIONS:
                continue
            values: list[str]
            if key == "contract_id" and isinstance(value, str):
                values = [value]
            elif (key.endswith("_ref") or key.endswith("_refs") or key == "contract_refs") and isinstance(value, str):
                values = [value]
            elif (key.endswith("_refs") or key == "contract_refs") and isinstance(value, list):
                values = [item for item in value if isinstance(item, str)]
            elif key in {"origen_id", "destino_id", "fallback_estado_id"} and isinstance(value, str):
                values = [value]
            else:
                continue
            for item in values:
                if STABLE_ID_RE.fullmatch(item) is None:
                    continue
                if item not in contract_index:
                    findings.append(
                        _finding(
                            "CONTRACT_REF_NOT_FOUND",
                            path,
                            pointer,
                            _contract_id(data),
                            "existing contract id",
                            item,
                            "Reference an existing contract id or leave the ref empty if current policy allows.",
                            root,
                        )
                    )

        payload = data.get("payload")
        if isinstance(payload, dict):
            for entry_pointer, entry in _iter_support_entries(payload):
                _validate_support_entry_path(root, path, data, entry_pointer, entry, contract_index, path_by_id, findings)


def _iter_support_entries(payload: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for key in ("contract_entries", "relationship_contract_entries"):
        entries = payload.get(key)
        if isinstance(entries, list):
            for index, entry in enumerate(entries):
                if isinstance(entry, dict):
                    yield f"/payload/{key}/{index}", entry


def _validate_support_entry_path(
    root: Path,
    source_path: Path,
    source_data: dict[str, Any],
    pointer: str,
    entry: dict[str, Any],
    contract_index: dict[str, Any],
    path_by_id: dict[str, Path],
    findings: list[Finding],
) -> None:
    path_value = entry.get("path")
    entry_id = entry.get("contract_id") or entry.get("relationship_type_ref")
    if isinstance(path_value, str):
        target_path = root / path_value
        if not target_path.exists():
            findings.append(
                _finding(
                    "CONTRACT_PATH_NOT_FOUND",
                    source_path,
                    f"{pointer}/path",
                    _contract_id(source_data),
                    "existing contract path",
                    path_value,
                    "Reference an existing contracts/** JSON path.",
                    root,
                )
            )
        elif isinstance(entry_id, str) and entry_id in path_by_id and path_by_id[entry_id] != target_path:
            findings.append(
                _finding(
                    "CONTRACT_REF_PATH_MISMATCH",
                    source_path,
                    f"{pointer}/path",
                    _contract_id(source_data),
                    _rel(root, path_by_id[entry_id]),
                    path_value,
                    "Keep support bundle paths aligned with the referenced contract id.",
                    root,
                )
            )
    if isinstance(entry_id, str) and entry_id not in contract_index:
        findings.append(
            _finding(
                "CONTRACT_REF_NOT_FOUND",
                source_path,
                pointer + ("/contract_id" if "contract_id" in entry else "/relationship_type_ref"),
                _contract_id(source_data),
                "existing contract id",
                entry_id,
                "Reference an existing contract id.",
                root,
            )
        )


def _validate_relationships(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    relationship_records: list[dict[str, Any]] = []
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "relationship":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        contract_id = _contract_id(data)
        origin_family = payload.get("origen_entidad")
        origin_id = payload.get("origen_id")
        dest_family = payload.get("destino_entidad")
        dest_id = payload.get("destino_id")
        relation_type = payload.get("tipo_relacion")
        payload_values = [origin_family, origin_id, dest_family, dest_id, relation_type, payload.get("cardinalidad"), payload.get("requerido"), payload.get("orden")]
        record = {
            "path": path,
            "data": data,
            "payload": payload,
            "contract_id": contract_id,
            "origin_family": origin_family,
            "origin_id": origin_id,
            "dest_family": dest_family,
            "dest_id": dest_id,
            "relation_type": relation_type,
            "cardinality": payload.get("cardinalidad"),
            "required": payload.get("requerido"),
            "order": payload.get("orden"),
            "kind": "invalid",
        }
        if all(value is None for value in payload_values):
            record["kind"] = "placeholder"
            relationship_records.append(record)
            if data.get("id") != "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1":
                findings.append(
                    _finding(
                        "RELATIONSHIP_PLACEHOLDER_ID_MISMATCH",
                        path,
                        "/id",
                        contract_id,
                        "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1",
                        data.get("id"),
                        "Use the canonical placeholder relationship id.",
                        root,
                    )
                )
            continue

        type_record = origin_id is None and dest_id is None
        instance_record = isinstance(origin_id, str) and isinstance(dest_id, str)
        if type_record:
            record["kind"] = "type"
        elif instance_record:
            record["kind"] = "instance"
        relationship_records.append(record)
        if not type_record and not instance_record:
            findings.append(
                _finding(
                    "RELATIONSHIP_ENDPOINT_SHAPE_INVALID",
                    path,
                    "/payload",
                    contract_id,
                    "both endpoint IDs null for type records, or both populated for instance records",
                    {"origen_id": origin_id, "destino_id": dest_id},
                    "Populate both endpoint IDs for instances, or leave both null for relationship type records.",
                    root,
                )
            )
            continue

        if not isinstance(origin_family, str) or not isinstance(dest_family, str) or not isinstance(relation_type, str):
            continue

        if type_record:
            if payload.get("requerido") is not None:
                findings.append(
                    _finding(
                        "RELATIONSHIP_REQUIRED_FLAG_INVALID",
                        path,
                        "/payload/requerido",
                        contract_id,
                        "null for relationship type contracts",
                        payload.get("requerido"),
                        "Keep requerido null on relationship type contracts; only concrete relationship instances may set it.",
                        root,
                    )
                )
            expected_id = f"relacion.{origin_family}.{relation_type}.{dest_family}.v1"
            if data.get("id") != expected_id:
                findings.append(
                    _finding(
                        "RELATIONSHIP_TYPE_ID_MISMATCH",
                        path,
                        "/id",
                        contract_id,
                        expected_id,
                        data.get("id"),
                        "Align relationship type IDs with origin family, relation type, and destination family.",
                        root,
                    )
                )
            continue

        if not isinstance(payload.get("requerido"), bool):
            findings.append(
                _finding(
                    "RELATIONSHIP_REQUIRED_FLAG_INVALID",
                    path,
                    "/payload/requerido",
                    contract_id,
                    "boolean for relationship instance contracts",
                    payload.get("requerido"),
                    "Set requerido to true or false on relationship instances.",
                    root,
                )
            )

        for endpoint_key, family_key, endpoint_id, family in (
            ("origen_id", "origen_entidad", origin_id, origin_family),
            ("destino_id", "destino_entidad", dest_id, dest_family),
        ):
            if endpoint_id not in contract_index:
                findings.append(
                    _finding(
                        "RELATIONSHIP_ENDPOINT_NOT_FOUND",
                        path,
                        f"/payload/{endpoint_key}",
                        contract_id,
                        "existing endpoint contract id",
                        endpoint_id,
                        "Reference an existing endpoint contract.",
                        root,
                    )
                )
                continue
            endpoint_prefix = endpoint_id.split(".", 1)[0]
            if endpoint_prefix != family:
                findings.append(
                    _finding(
                        "RELATIONSHIP_ENDPOINT_FAMILY_MISMATCH",
                        path,
                        f"/payload/{family_key}",
                        contract_id,
                        endpoint_prefix,
                        family,
                        "Keep endpoint family aligned with the endpoint id prefix.",
                        root,
                    )
                )

        type_id = f"relacion.{origin_family}.{relation_type}.{dest_family}.v1"
        type_contract = contract_index.get(type_id)
        type_payload = type_contract.get("payload") if isinstance(type_contract, dict) else None
        if type_contract is None:
            findings.append(
                _finding(
                    "RELATIONSHIP_TYPE_NOT_FOUND",
                    path,
                    "/payload/tipo_relacion",
                    contract_id,
                    type_id,
                    relation_type,
                    "Create or reference an existing relationship type contract.",
                    root,
                )
            )
        elif type_contract.get("status") in RELATIONSHIP_RETIRED_STATUSES:
            findings.append(
                _finding(
                    "RELATIONSHIP_DEPRECATED_TYPE_USED",
                    path,
                    "/payload/tipo_relacion",
                    contract_id,
                    "active relationship type",
                    type_id,
                    "Use the canonical replacement relationship type instead of a deprecated one.",
                    root,
                )
            )
        elif isinstance(type_payload, dict):
            expected_tuple = (origin_family, relation_type, dest_family)
            actual_tuple = (
                type_payload.get("origen_entidad"),
                type_payload.get("tipo_relacion"),
                type_payload.get("destino_entidad"),
            )
            if actual_tuple != expected_tuple:
                findings.append(
                    _finding(
                        "RELATIONSHIP_TYPE_TUPLE_MISMATCH",
                        path,
                        "/payload/tipo_relacion",
                        contract_id,
                        expected_tuple,
                        actual_tuple,
                        "Keep relationship instance endpoint families aligned with its relationship type contract tuple.",
                        root,
                    )
                )
            if payload.get("cardinalidad") != type_payload.get("cardinalidad"):
                findings.append(
                    _finding(
                        "RELATIONSHIP_CARDINALITY_MISMATCH",
                        path,
                        "/payload/cardinalidad",
                        contract_id,
                        type_payload.get("cardinalidad"),
                        payload.get("cardinalidad"),
                        "Relationship instance cardinality must equal its relationship type contract cardinality.",
                        root,
                    )
                )

        expected_instance_id = f"relacion.{_embedded_contract_id(origin_id)}.{relation_type}.{_embedded_contract_id(dest_id)}.v1"
        if data.get("id") != expected_instance_id:
            findings.append(
                _finding(
                    "RELATIONSHIP_INSTANCE_ID_MISMATCH",
                    path,
                    "/id",
                    contract_id,
                    expected_instance_id,
                    data.get("id"),
                    "Align relationship instance IDs with endpoint IDs and relationship type.",
                    root,
                )
            )

    _validate_relationship_duplicates(root, relationship_records, findings)
    _validate_relationship_cardinality_constraints(root, relationship_records, findings)
    _validate_relationship_ordering(root, relationship_records, findings)
    _validate_resolver_output_relationship_refs(root, contract_files, parsed, contract_index, relationship_records, findings)


def _validate_relationship_duplicates(
    root: Path,
    records: list[dict[str, Any]],
    findings: list[Finding],
) -> None:
    type_tuples: dict[tuple[Any, Any, Any], list[dict[str, Any]]] = {}
    instance_triples: dict[tuple[Any, Any, Any], list[dict[str, Any]]] = {}
    for record in records:
        if record["kind"] == "type":
            key = (record["origin_family"], record["relation_type"], record["dest_family"])
            type_tuples.setdefault(key, []).append(record)
        if record["kind"] == "instance":
            key = (record["origin_id"], record["relation_type"], record["dest_id"])
            instance_triples.setdefault(key, []).append(record)

    for duplicate_records in type_tuples.values():
        if len(duplicate_records) < 2:
            continue
        first = duplicate_records[0]["contract_id"]
        for record in duplicate_records[1:]:
            findings.append(
                _finding(
                    "RELATIONSHIP_DUPLICATE_TYPE",
                    record["path"],
                    "/payload/tipo_relacion",
                    record["contract_id"],
                    f"unique relationship type tuple first declared by {first}",
                    {
                        "origen_entidad": record["origin_family"],
                        "tipo_relacion": record["relation_type"],
                        "destino_entidad": record["dest_family"],
                    },
                    "Keep exactly one relationship type contract per origin family, relation type, and destination family tuple.",
                    root,
                )
            )

    for duplicate_records in instance_triples.values():
        if len(duplicate_records) < 2:
            continue
        first = duplicate_records[0]["contract_id"]
        for record in duplicate_records[1:]:
            findings.append(
                _finding(
                    "RELATIONSHIP_DUPLICATE_INSTANCE",
                    record["path"],
                    "/payload/destino_id",
                    record["contract_id"],
                    f"unique relationship instance triple first declared by {first}",
                    {
                        "origen_id": record["origin_id"],
                        "tipo_relacion": record["relation_type"],
                        "destino_id": record["dest_id"],
                    },
                    "Keep exactly one relationship instance per origin id, relation type, and destination id triple.",
                    root,
                )
            )


def _validate_relationship_cardinality_constraints(
    root: Path,
    records: list[dict[str, Any]],
    findings: list[Finding],
) -> None:
    grouped: dict[tuple[Any, Any, Any, Any], list[dict[str, Any]]] = {}
    for record in records:
        if record["kind"] != "instance" or record["data"].get("status") in RELATIONSHIP_RETIRED_STATUSES:
            continue
        key = (record["origin_family"], record["relation_type"], record["dest_family"], record["cardinality"])
        grouped.setdefault(key, []).append(record)

    for (_origin_family, _relation_type, _dest_family, cardinality), group in grouped.items():
        if not isinstance(cardinality, str) or ":" not in cardinality:
            continue
        origin_side, dest_side = cardinality.split(":", 1)
        if dest_side == "1":
            by_origin: dict[str, list[dict[str, Any]]] = {}
            for record in group:
                if isinstance(record["origin_id"], str):
                    by_origin.setdefault(record["origin_id"], []).append(record)
            _emit_cardinality_constraint_findings(root, by_origin, "origin endpoint with at most one destination", findings)
        if origin_side == "1":
            by_dest: dict[str, list[dict[str, Any]]] = {}
            for record in group:
                if isinstance(record["dest_id"], str):
                    by_dest.setdefault(record["dest_id"], []).append(record)
            _emit_cardinality_constraint_findings(root, by_dest, "destination endpoint with at most one origin", findings)


def _emit_cardinality_constraint_findings(
    root: Path,
    grouped: dict[str, list[dict[str, Any]]],
    expected: str,
    findings: list[Finding],
) -> None:
    for records in grouped.values():
        endpoint_pairs = {(record["origin_id"], record["dest_id"]) for record in records}
        if len(endpoint_pairs) < 2:
            continue
        for record in records[1:]:
            findings.append(
                _finding(
                    "RELATIONSHIP_CARDINALITY_CONSTRAINT_VIOLATION",
                    record["path"],
                    "/payload/cardinalidad",
                    record["contract_id"],
                    expected,
                    {
                        "origen_id": record["origin_id"],
                        "tipo_relacion": record["relation_type"],
                        "destino_id": record["dest_id"],
                        "cardinalidad": record["cardinality"],
                    },
                    "Relationship instances must not violate the relationship type cardinality constraint.",
                    root,
                )
            )


def _validate_relationship_ordering(
    root: Path,
    records: list[dict[str, Any]],
    findings: list[Finding],
) -> None:
    ordered_groups: dict[tuple[Any, Any, Any], list[dict[str, Any]]] = {}
    for record in records:
        if record["kind"] != "instance" or record["data"].get("status") in RELATIONSHIP_RETIRED_STATUSES:
            continue
        type_tuple = (record["origin_family"], record["relation_type"], record["dest_family"])
        order = record["order"]
        if type_tuple in ORDERED_RELATIONSHIP_TYPE_TUPLES:
            if not isinstance(order, int):
                findings.append(
                    _finding(
                        "RELATIONSHIP_ORDER_REQUIRED",
                        record["path"],
                        "/payload/orden",
                        record["contract_id"],
                        "integer order for ordered relationship type tuple",
                        order,
                        "Set orden for every instance in ordered relationship groups.",
                        root,
                    )
                )
                continue
            group_key = _relationship_order_group_key(record)
            ordered_groups.setdefault(group_key, []).append(record)
        elif order is not None:
            findings.append(
                _finding(
                    "RELATIONSHIP_ORDER_NOT_ALLOWED",
                    record["path"],
                    "/payload/orden",
                    record["contract_id"],
                    "null for unordered relationship type tuple",
                    order,
                    "Use orden only for currently ordered relationship groups.",
                    root,
                )
            )

    for group in ordered_groups.values():
        by_order: dict[int, list[dict[str, Any]]] = {}
        for record in group:
            by_order.setdefault(record["order"], []).append(record)
        for slot_records in by_order.values():
            if len(slot_records) < 2:
                continue
            first = slot_records[0]["contract_id"]
            for record in slot_records[1:]:
                findings.append(
                    _finding(
                        "RELATIONSHIP_ORDER_DUPLICATE",
                        record["path"],
                        "/payload/orden",
                        record["contract_id"],
                        f"unique order slot first declared by {first}",
                        record["order"],
                        "Use each orden value once per ordered relationship group.",
                        root,
                    )
                )
        unique_orders = sorted(by_order)
        expected_orders = list(range(1, len(unique_orders) + 1))
        if unique_orders != expected_orders:
            first_record = group[0]
            findings.append(
                _finding(
                    "RELATIONSHIP_ORDER_GAP",
                    first_record["path"],
                    "/payload/orden",
                    first_record["contract_id"],
                    expected_orders,
                    unique_orders,
                    "Keep ordered relationship groups contiguous from 1 with no gaps.",
                    root,
                )
            )


def _validate_resolver_output_relationship_refs(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    relationship_records: list[dict[str, Any]],
    findings: list[Finding],
) -> None:
    support_targets = {
        record["dest_id"]
        for record in relationship_records
        if record["kind"] == "instance"
        and record["origin_family"] == "resolver"
        and record["relation_type"] == "usa"
        and record["dest_family"] == "relacion"
        and isinstance(record["dest_id"], str)
        and record["data"].get("status") not in RELATIONSHIP_RETIRED_STATUSES
    }

    for record in relationship_records:
        if (
            record["kind"] == "instance"
            and record["origin_family"] == "resolver"
            and record["relation_type"] == "usa"
            and record["dest_family"] == "relacion"
        ):
            target_id = record["dest_id"]
            if not isinstance(target_id, str) or not _is_active_relationship_instance_ref(target_id, contract_index):
                findings.append(
                    _finding(
                        "RELATIONSHIP_SUPPORT_LINK_TARGET_INVALID",
                        record["path"],
                        "/payload/destino_id",
                        record["contract_id"],
                        "active relationship instance target",
                        target_id,
                        "Resolver-to-Relación support links must target active relationship instance contracts, not placeholders, type refs, missing refs, deprecated refs, or retired refs.",
                        root,
                    )
                )

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "entity" or data.get("entity_family") != "resolver_output":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        selected_refs = payload.get("selected_relacion_refs")
        if not isinstance(selected_refs, list):
            continue
        for index, ref in enumerate(selected_refs):
            pointer = f"/payload/selected_relacion_refs/{index}"
            if not isinstance(ref, str):
                continue
            target = contract_index.get(ref)
            if _is_placeholder_relationship_ref(ref, target):
                findings.append(
                    _finding(
                        "RELATIONSHIP_SELECTED_REF_PLACEHOLDER",
                        path,
                        pointer,
                        _contract_id(data),
                        "relationship instance ref",
                        ref,
                        "ResolverOutput selected_relacion_refs must not select the placeholder relationship.",
                        root,
                    )
                )
                continue
            if isinstance(target, dict) and target.get("status") in RELATIONSHIP_RETIRED_STATUSES:
                findings.append(
                    _finding(
                        "RELATIONSHIP_SELECTED_REF_DEPRECATED",
                        path,
                        pointer,
                        _contract_id(data),
                        "active relationship instance ref",
                        ref,
                        "ResolverOutput selected_relacion_refs must not select deprecated or retired relationship refs.",
                        root,
                    )
                )
                continue
            if isinstance(target, dict) and not _is_relationship_instance_contract(target):
                findings.append(
                    _finding(
                        "RELATIONSHIP_SELECTED_REF_NOT_INSTANCE",
                        path,
                        pointer,
                        _contract_id(data),
                        "relationship instance ref",
                        ref,
                        "ResolverOutput selected_relacion_refs must select relationship instance refs, not relationship type refs.",
                        root,
                    )
                )
                continue
            if ref in contract_index and ref not in support_targets:
                findings.append(
                    _finding(
                        "RELATIONSHIP_SUPPORT_LINK_MISSING",
                        path,
                        pointer,
                        _contract_id(data),
                        "matching resolver.usa.relacion support link",
                        ref,
                        "Every accepted selected_relacion_refs entry must have a Resolver-to-Relación support link.",
                        root,
                    )
                )


def _relationship_order_group_key(record: dict[str, Any]) -> tuple[Any, ...]:
    type_tuple = (record["origin_family"], record["relation_type"], record["dest_family"])
    if type_tuple == ("fuente", "informa", "estado"):
        return type_tuple
    return (record["origin_id"], record["relation_type"], record["dest_family"])


def _is_placeholder_relationship_ref(ref: str, target: Any) -> bool:
    if ref == "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1":
        return True
    if not isinstance(target, dict):
        return False
    if target.get("contract_kind") != "relationship" or target.get("entity_family") != "relacion":
        return False
    payload = target.get("payload")
    if not isinstance(payload, dict):
        return False
    values = [
        payload.get("origen_entidad"),
        payload.get("origen_id"),
        payload.get("destino_entidad"),
        payload.get("destino_id"),
        payload.get("tipo_relacion"),
        payload.get("cardinalidad"),
        payload.get("requerido"),
        payload.get("orden"),
    ]
    return all(value is None for value in values)


def _is_relationship_instance_contract(data: dict[str, Any]) -> bool:
    if data.get("contract_kind") != "relationship" or data.get("entity_family") != "relacion":
        return False
    payload = data.get("payload")
    return isinstance(payload, dict) and isinstance(payload.get("origen_id"), str) and isinstance(payload.get("destino_id"), str)


def _is_active_relationship_instance_ref(ref: str, contract_index: dict[str, Any]) -> bool:
    target = contract_index.get(ref)
    return isinstance(target, dict) and target.get("status") not in RELATIONSHIP_RETIRED_STATUSES and _is_relationship_instance_contract(target)


def _embedded_contract_id(contract_id: str) -> str:
    body = contract_id.removesuffix(".v1")
    family, _, slug = body.partition(".")
    if not slug:
        return body
    return family + "." + slug.replace(".", "_")


def _validate_support_bundle_semantics(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    path_by_id: dict[str, Path],
    findings: list[Finding],
) -> None:
    support_records = _collect_support_records(contract_files, parsed)
    manifests = support_records.get("manifest", [])
    indexes = support_records.get("index", [])
    policies = support_records.get("reference_bundle", [])
    selectors = support_records.get("selector", [])

    for records in support_records.values():
        for record in records:
            _validate_support_boundary_claims(root, record["path"], record["data"], findings)

    manifest = manifests[0] if manifests else None
    index = indexes[0] if indexes else None
    policy = policies[0] if policies else None
    selector = selectors[0] if selectors else None

    if manifest and index:
        _validate_manifest_index_parity(root, manifest, index, contract_index, path_by_id, findings)
    if manifest and index and policy and selector:
        _validate_policy_static_data_refs(root, manifest, index, policy, selectors, findings)
    if index and selector:
        _validate_selector_output_and_dimension_parity(root, index, selector, findings)

    for record in indexes:
        _validate_index_active_support_refs(root, record, contract_index, findings)
    for record in policies:
        _validate_policy_active_support_refs(root, record, contract_index, findings)
    for record in selectors:
        _validate_selector_active_support_refs(root, record, contract_index, findings)

    if manifest or index or policy or selector:
        _validate_resolver_output_support_refs(root, contract_files, parsed, manifest, index, policy, selectors, contract_index, findings)


def _collect_support_records(contract_files: list[Path], parsed: dict[Path, Any]) -> dict[str, list[dict[str, Any]]]:
    records: dict[str, list[dict[str, Any]]] = {}
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        kind = data.get("contract_kind")
        if kind not in SUPPORT_KINDS:
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        records.setdefault(kind, []).append({"path": path, "data": data, "payload": payload})
    return records


def _validate_manifest_index_parity(
    root: Path,
    manifest: dict[str, Any],
    index: dict[str, Any],
    contract_index: dict[str, Any],
    path_by_id: dict[str, Path],
    findings: list[Finding],
) -> None:
    manifest_payload = manifest["payload"]
    index_payload = index["payload"]
    manifest_entries = {
        entry.get("contract_id"): entry
        for entry in manifest_payload.get("contract_entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("contract_id"), str)
    }

    by_contract = _support_lookup_group(index_payload, "by_contract_id")
    if by_contract is not None:
        group_index, group = by_contract
        entry_refs = _lookup_group_refs(group, "contract_refs")
        for contract_id in sorted(manifest_entries):
            if contract_id not in entry_refs.get(contract_id, set()):
                findings.append(
                    _finding(
                        "SUPPORT_MANIFEST_INDEX_PARITY_MISSING",
                        index["path"],
                        f"/payload/lookup_groups/{group_index}/entries",
                        _contract_id(index["data"]),
                        f"by_contract_id entry for {contract_id}",
                        sorted(entry_refs),
                        "Keep index by_contract_id entries in parity with manifest contract_entries.",
                        root,
                    )
                )
        for lookup_key, refs in entry_refs.items():
            for ref in refs:
                if ref not in manifest_entries:
                    findings.append(
                        _finding(
                            "SUPPORT_CROSS_BUNDLE_REF_DRIFT",
                            index["path"],
                            _lookup_entry_pointer(index_payload, "by_contract_id", lookup_key, "contract_refs"),
                            _contract_id(index["data"]),
                            "contract ref present in manifest contract_entries",
                            ref,
                            "Remove stale index refs or add the curated manifest entry in a scoped support issue.",
                            root,
                        )
                    )

    by_path = _support_lookup_group(index_payload, "by_path")
    if by_path is not None:
        group_index, group = by_path
        entry_refs = _lookup_group_refs(group, "contract_refs")
        expected_path_to_id = {
            entry.get("path"): contract_id
            for contract_id, entry in manifest_entries.items()
            if isinstance(entry.get("path"), str)
        }
        for entry_path, contract_id in sorted(expected_path_to_id.items()):
            if contract_id not in entry_refs.get(entry_path, set()):
                findings.append(
                    _finding(
                        "SUPPORT_MANIFEST_INDEX_PARITY_MISSING",
                        index["path"],
                        f"/payload/lookup_groups/{group_index}/entries",
                        _contract_id(index["data"]),
                        f"by_path entry for {entry_path} -> {contract_id}",
                        sorted(entry_refs),
                        "Keep index by_path entries in parity with manifest contract_entries paths.",
                        root,
                    )
                )

    for entry_index, entry in enumerate(manifest_payload.get("contract_entries", [])):
        if not isinstance(entry, dict):
            continue
        contract_id = entry.get("contract_id")
        path_value = entry.get("path")
        if isinstance(contract_id, str) and contract_id in contract_index:
            target = contract_index[contract_id]
            if entry.get("status") != target.get("status"):
                findings.append(
                    _finding(
                        "SUPPORT_CROSS_BUNDLE_REF_DRIFT",
                        manifest["path"],
                        f"/payload/contract_entries/{entry_index}/status",
                        _contract_id(manifest["data"]),
                        target.get("status"),
                        entry.get("status"),
                        "Keep manifest curated entry status aligned with the referenced contract.",
                        root,
                    )
                )
        if isinstance(contract_id, str) and isinstance(path_value, str) and contract_id in path_by_id:
            expected_path = _rel(root, path_by_id[contract_id])
            if path_value != expected_path:
                findings.append(
                    _finding(
                        "SUPPORT_CROSS_BUNDLE_REF_DRIFT",
                        manifest["path"],
                        f"/payload/contract_entries/{entry_index}/path",
                        _contract_id(manifest["data"]),
                        expected_path,
                        path_value,
                        "Keep manifest curated entry path aligned with the referenced contract.",
                        root,
                    )
                )


def _validate_policy_static_data_refs(
    root: Path,
    manifest: dict[str, Any],
    index: dict[str, Any],
    policy: dict[str, Any],
    selectors: list[dict[str, Any]],
    findings: list[Finding],
) -> None:
    payload = policy["payload"]
    static_refs = payload.get("static_data_refs")
    if not isinstance(static_refs, dict):
        return

    expected_manifest_ref = _contract_id(manifest["data"])
    expected_index_ref = _contract_id(index["data"])
    expected_selector_refs = {_contract_id(selector["data"]) for selector in selectors}
    expected_selector_refs.discard(None)

    if static_refs.get("manifest_ref") != expected_manifest_ref:
        _support_static_drift(root, policy, "/payload/static_data_refs/manifest_ref", expected_manifest_ref, static_refs.get("manifest_ref"), findings)
    if static_refs.get("index_ref") != expected_index_ref:
        _support_static_drift(root, policy, "/payload/static_data_refs/index_ref", expected_index_ref, static_refs.get("index_ref"), findings)
    actual_selector_refs = set(static_refs.get("selector_refs", [])) if isinstance(static_refs.get("selector_refs"), list) else set()
    if actual_selector_refs != expected_selector_refs:
        _support_static_drift(root, policy, "/payload/static_data_refs/selector_refs", sorted(expected_selector_refs), sorted(actual_selector_refs), findings)

    manifest_payload = manifest["payload"]
    index_payload = index["payload"]
    if expected_index_ref not in set(manifest_payload.get("index_refs", [])):
        _support_static_drift(root, manifest, "/payload/index_refs", f"include {expected_index_ref}", manifest_payload.get("index_refs"), findings)
    if _contract_id(policy["data"]) not in set(manifest_payload.get("policy_bundle_refs", [])):
        _support_static_drift(root, manifest, "/payload/policy_bundle_refs", f"include {_contract_id(policy['data'])}", manifest_payload.get("policy_bundle_refs"), findings)
    if expected_manifest_ref != index_payload.get("manifest_ref"):
        _support_static_drift(root, index, "/payload/manifest_ref", expected_manifest_ref, index_payload.get("manifest_ref"), findings)
    if _contract_id(policy["data"]) != index_payload.get("policy_ref"):
        _support_static_drift(root, index, "/payload/policy_ref", _contract_id(policy["data"]), index_payload.get("policy_ref"), findings)


def _support_static_drift(
    root: Path,
    record: dict[str, Any],
    pointer: str,
    expected: Any,
    actual: Any,
    findings: list[Finding],
) -> None:
    findings.append(
        _finding(
            "SUPPORT_STATIC_DATA_REF_DRIFT",
            record["path"],
            pointer,
            _contract_id(record["data"]),
            expected,
            actual,
            "Keep policy static_data_refs and active support bundle refs aligned across manifest, index, policy, and selector.",
            root,
        )
    )


def _validate_selector_output_and_dimension_parity(
    root: Path,
    index: dict[str, Any],
    selector: dict[str, Any],
    findings: list[Finding],
) -> None:
    payload = selector["payload"]
    output_groups = payload.get("output_ref_groups", [])
    output_group_set = set(output_groups) if isinstance(output_groups, list) else set()
    for group_index, group in enumerate(output_groups if isinstance(output_groups, list) else []):
        if not isinstance(group, str):
            continue
        if group not in RESOLVER_OUTPUT_SELECTOR_GROUPS:
            findings.append(
                _finding(
                    "SELECTOR_OUTPUT_GROUP_UNKNOWN",
                    selector["path"],
                    f"/payload/output_ref_groups/{group_index}",
                    _contract_id(selector["data"]),
                    sorted(RESOLVER_OUTPUT_SELECTOR_GROUPS),
                    group,
                    "Selector output groups must align with ResolverOutput ref-bearing payload fields.",
                    root,
                )
            )

    selector_entries = payload.get("selector_entries", [])
    for entry_index, entry in enumerate(selector_entries if isinstance(selector_entries, list) else []):
        if not isinstance(entry, dict):
            continue
        for group_index, group in enumerate(entry.get("candidate_output_ref_groups", []) if isinstance(entry.get("candidate_output_ref_groups"), list) else []):
            if not isinstance(group, str):
                continue
            if group not in RESOLVER_OUTPUT_SELECTOR_GROUPS:
                findings.append(
                    _finding(
                        "SELECTOR_OUTPUT_GROUP_UNKNOWN",
                        selector["path"],
                        f"/payload/selector_entries/{entry_index}/candidate_output_ref_groups/{group_index}",
                        _contract_id(selector["data"]),
                        sorted(RESOLVER_OUTPUT_SELECTOR_GROUPS),
                        group,
                        "Selector entry output groups must align with ResolverOutput ref-bearing payload fields.",
                        root,
                    )
                )
            elif group not in output_group_set:
                findings.append(
                    _finding(
                        "SELECTOR_OUTPUT_GROUP_MISSING",
                        selector["path"],
                        f"/payload/selector_entries/{entry_index}/candidate_output_ref_groups/{group_index}",
                        _contract_id(selector["data"]),
                        "candidate output group also listed in output_ref_groups",
                        group,
                        "List every selector entry output group in selector.output_ref_groups.",
                        root,
                    )
                )

    dimension_map = payload.get("dimension_contract_family_map")
    allowed_dimensions = payload.get("allowed_dimensions")
    if isinstance(dimension_map, dict) and isinstance(allowed_dimensions, list):
        if set(allowed_dimensions) != set(dimension_map):
            findings.append(
                _finding(
                    "SELECTOR_DIMENSION_PARITY_DRIFT",
                    selector["path"],
                    "/payload/allowed_dimensions",
                    _contract_id(selector["data"]),
                    sorted(dimension_map),
                    sorted(allowed_dimensions),
                    "Keep selector allowed_dimensions in parity with dimension_contract_family_map.",
                    root,
                )
            )

    entry_dimensions = {
        entry.get("dimension"): set(entry.get("candidate_contract_family_refs", []))
        for entry in selector_entries
        if isinstance(entry, dict) and isinstance(entry.get("dimension"), str) and isinstance(entry.get("candidate_contract_family_refs"), list)
    }
    if isinstance(dimension_map, dict):
        for dimension, family_refs in dimension_map.items():
            if entry_dimensions.get(dimension) != set(family_refs):
                findings.append(
                    _finding(
                        "SELECTOR_DIMENSION_PARITY_DRIFT",
                        selector["path"],
                        "/payload/selector_entries",
                        _contract_id(selector["data"]),
                        {dimension: family_refs},
                        {dimension: sorted(entry_dimensions.get(dimension, set()))},
                        "Keep selector entries in parity with dimension_contract_family_map.",
                        root,
                    )
                )

    by_selector_dimension = _support_lookup_group(index["payload"], "by_selector_dimension")
    if by_selector_dimension is None or not isinstance(dimension_map, dict):
        return
    group_index, group = by_selector_dimension
    index_dimension_refs = _lookup_group_refs(group, "contract_family_refs")
    for dimension, family_refs in dimension_map.items():
        if set(family_refs) != index_dimension_refs.get(dimension, set()):
            findings.append(
                _finding(
                    "SELECTOR_DIMENSION_PARITY_DRIFT",
                    index["path"],
                    f"/payload/lookup_groups/{group_index}/entries",
                    _contract_id(index["data"]),
                    {dimension: sorted(family_refs)},
                    {dimension: sorted(index_dimension_refs.get(dimension, set()))},
                    "Keep index by_selector_dimension entries in parity with selector dimension_contract_family_map.",
                    root,
                )
            )


def _validate_index_active_support_refs(
    root: Path,
    record: dict[str, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    payload = record["payload"]
    _validate_active_support_ref(root, record, "/payload/manifest_ref", payload.get("manifest_ref"), "manifest", contract_index, findings)
    _validate_active_support_ref(root, record, "/payload/policy_ref", payload.get("policy_ref"), "policy", contract_index, findings)
    for index, ref in enumerate(payload.get("selector_refs", []) if isinstance(payload.get("selector_refs"), list) else []):
        _validate_active_support_ref(root, record, f"/payload/selector_refs/{index}", ref, "selector", contract_index, findings)
    for index, ref in enumerate(payload.get("resolver_refs", []) if isinstance(payload.get("resolver_refs"), list) else []):
        _validate_active_support_ref(root, record, f"/payload/resolver_refs/{index}", ref, "resolver", contract_index, findings)


def _validate_policy_active_support_refs(
    root: Path,
    record: dict[str, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    payload = record["payload"]
    active_array_fields = {
        "allowed_actor_refs": "actor",
        "applies_to_resolver_refs": "resolver",
        "evidence_category_refs": "evidencia",
        "limit_refs": "limite",
        "relationship_type_refs": "relacion",
        "rule_refs": "regla",
        "source_authority_refs": "fuente",
        "state_refs": "estado",
        "tooling_gate_refs": None,
    }
    for key, expected_family in active_array_fields.items():
        values = payload.get(key, [])
        if not isinstance(values, list):
            continue
        for index, ref in enumerate(values):
            relationship_kind = "type" if key == "relationship_type_refs" else None
            _validate_active_support_ref(
                root,
                record,
                f"/payload/{key}/{index}",
                ref,
                expected_family,
                contract_index,
                findings,
                relationship_kind=relationship_kind,
            )

    relationship_instances = payload.get("relationship_instance_refs")
    if isinstance(relationship_instances, dict):
        for group_key, values in relationship_instances.items():
            if not isinstance(values, list):
                continue
            for index, ref in enumerate(values):
                _validate_active_support_ref(
                    root,
                    record,
                    f"/payload/relationship_instance_refs/{escape_pointer_token(str(group_key))}/{index}",
                    ref,
                    "relacion",
                    contract_index,
                    findings,
                    relationship_kind="instance",
                )

    _validate_policy_fallback_estado_ref(root, record, contract_index, findings)


def _validate_policy_fallback_estado_ref(
    root: Path,
    record: dict[str, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    payload = record["payload"]
    fallback = payload.get("fallback_estado_ref")
    state_refs = set(payload.get("state_refs", [])) if isinstance(payload.get("state_refs"), list) else set()
    target = contract_index.get(fallback) if isinstance(fallback, str) else None
    valid = (
        isinstance(fallback, str)
        and fallback in state_refs
        and isinstance(target, dict)
        and fallback.startswith("estado.")
        and target.get("status") in SUPPORT_ACTIVE_STATUSES
    )
    if not valid:
        findings.append(
            _finding(
                "POLICY_FALLBACK_ESTADO_INVALID",
                record["path"],
                "/payload/fallback_estado_ref",
                _contract_id(record["data"]),
                "active estado ref also present in policy state_refs",
                fallback,
                "Policy fallback_estado_ref must resolve to an active Estado included in state_refs.",
                root,
            )
        )


def _validate_selector_active_support_refs(
    root: Path,
    record: dict[str, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    payload = record["payload"]
    for key, expected_family in {
        "index_ref": "index",
        "manifest_ref": "manifest",
        "policy_ref": "policy",
        "resolver_ref": "resolver",
    }.items():
        _validate_active_support_ref(root, record, f"/payload/{key}", payload.get(key), expected_family, contract_index, findings)


def _validate_resolver_output_support_refs(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    manifest: dict[str, Any] | None,
    index: dict[str, Any] | None,
    policy: dict[str, Any] | None,
    selectors: list[dict[str, Any]],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    expected = {
        "manifest_ref": _contract_id(manifest["data"]) if manifest else None,
        "index_ref": _contract_id(index["data"]) if index else None,
        "policy_ref": _contract_id(policy["data"]) if policy else None,
    }
    expected_selector_refs = {_contract_id(selector["data"]) for selector in selectors}
    expected_selector_refs.discard(None)

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "entity" or data.get("entity_family") != "resolver_output":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        record = {"path": path, "data": data, "payload": payload}
        for key, expected_ref in expected.items():
            actual = payload.get(key)
            if expected_ref is not None and actual != expected_ref:
                findings.append(
                    _finding(
                        "RESOLVER_OUTPUT_SUPPORT_LINK_MISSING",
                        path,
                        f"/payload/{key}",
                        _contract_id(data),
                        expected_ref,
                        actual,
                        "ResolverOutput support refs must point to the active support manifest, index, and policy bundles.",
                        root,
                    )
                )
            _validate_active_support_ref(root, record, f"/payload/{key}", actual, key.removesuffix("_ref"), contract_index, findings)

        selector_refs = payload.get("selector_refs")
        actual_selector_refs = set(selector_refs) if isinstance(selector_refs, list) else set()
        if expected_selector_refs and actual_selector_refs != expected_selector_refs:
            findings.append(
                _finding(
                    "RESOLVER_OUTPUT_SUPPORT_LINK_MISSING",
                    path,
                    "/payload/selector_refs",
                    _contract_id(data),
                    sorted(expected_selector_refs),
                    sorted(actual_selector_refs),
                    "ResolverOutput selector_refs must point to active support selector bundles.",
                    root,
                )
            )
        for index_value, ref in enumerate(selector_refs if isinstance(selector_refs, list) else []):
            _validate_active_support_ref(root, record, f"/payload/selector_refs/{index_value}", ref, "selector", contract_index, findings)


def _validate_active_support_ref(
    root: Path,
    record: dict[str, Any],
    pointer: str,
    ref: Any,
    expected_family: str | None,
    contract_index: dict[str, Any],
    findings: list[Finding],
    *,
    relationship_kind: str | None = None,
) -> None:
    if not isinstance(ref, str):
        return
    if expected_family is not None and ref.split(".", 1)[0] != expected_family:
        findings.append(
            _finding(
                "SUPPORT_REF_FAMILY_MISMATCH",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                f"{expected_family} ref",
                ref,
                "Keep active support refs aligned with the expected contract family.",
                root,
            )
        )
        return
    target = contract_index.get(ref)
    if not isinstance(target, dict):
        findings.append(
            _finding(
                "SUPPORT_CROSS_BUNDLE_REF_DRIFT",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                "existing active support contract ref",
                ref,
                "Every active support ref must resolve to an existing contract record.",
                root,
            )
        )
        return
    status = target.get("status")
    if status == "deprecated":
        findings.append(
            _finding(
                "SUPPORT_REF_DEPRECATED_ACTIVE",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                "active non-deprecated support ref",
                ref,
                "Deprecated refs may remain provenance-only but must not be active support candidates.",
                root,
            )
        )
        return
    if status == "retired":
        findings.append(
            _finding(
                "SUPPORT_REF_RETIRED_ACTIVE",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                "active non-retired support ref",
                ref,
                "Retired refs must not be active support candidates.",
                root,
            )
        )
        return
    if status not in SUPPORT_ACTIVE_STATUSES:
        findings.append(
            _finding(
                "SUPPORT_REF_STATUS_INVALID",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                sorted(SUPPORT_ACTIVE_STATUSES),
                status,
                "Active support refs must point to active or draft records for Base v0.1.",
                root,
            )
        )
    if _is_placeholder_relationship_ref(ref, target):
        findings.append(
            _finding(
                "SUPPORT_REF_PLACEHOLDER_FORBIDDEN",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                "non-placeholder active support ref",
                ref,
                "Placeholder relationship refs are allowed only as explicitly inactive/provenance-safe placeholders, not active support candidates.",
                root,
            )
        )
        return
    if relationship_kind == "type" and _is_relationship_instance_contract(target):
        findings.append(
            _finding(
                "SUPPORT_REF_FAMILY_MISMATCH",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                "relationship type ref",
                ref,
                "Policy relationship_type_refs must point to relationship type records.",
                root,
            )
        )
    if relationship_kind == "instance" and not _is_relationship_instance_contract(target):
        findings.append(
            _finding(
                "SUPPORT_REF_FAMILY_MISMATCH",
                record["path"],
                pointer,
                _contract_id(record["data"]),
                "relationship instance ref",
                ref,
                "Policy relationship_instance_refs must point to relationship instance records.",
                root,
            )
        )


def _validate_support_boundary_claims(
    root: Path,
    path: Path,
    data: dict[str, Any],
    findings: list[Finding],
) -> None:
    kind = data.get("contract_kind")
    for pointer, key, value in _walk_key_values(data):
        raw_key = key.lower()
        normalized_key = _normalize_claim_text(key)
        if kind == "manifest" and key in {"complete_inventory", "generated"} and value is not False:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_GENERATED_INVENTORY_CLAIM", value, findings)
        if kind == "index" and key in {"generated", *SUPPORT_GENERATED_INDEX_KEYS} and value not in {False, None}:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_GENERATED_INDEX_CLAIM", value, findings)
        if key == "loader_behavior" and value is not False:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_LOADER_CLAIM", value, findings)
        if key == "runtime_behavior" and value is not False:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_RUNTIME_CLAIM", value, findings)
        if key == "resolver_behavior" and value is not False:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_RESOLVER_RUNTIME_CLAIM", value, findings)
        if key == "selector_runtime_behavior" and value is not False:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_SELECTOR_RUNTIME_CLAIM", value, findings)
        if key == "write_authorization_behavior" and value is not False:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_WRITE_AUTHORIZATION_FORBIDDEN", value, findings)
        if key in SUPPORT_BODY_COPY_KEYS or key in RELATIONSHIP_OWNED_KEYS:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_OUTPUT_BODY_FORBIDDEN", key, findings)
        if raw_key in SUPPORT_TEMPLATE_EXECUTION_KEYS:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_TEMPLATE_EXECUTION_CLAIM", key, findings)
        if raw_key in SUPPORT_COMMAND_KEYS:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_COMMAND_EXECUTION_CLAIM", key, findings)
        if raw_key in SUPPORT_PERMISSION_KEYS and value is not False and value is not None and value != []:
            _support_boundary_finding(root, path, data, pointer, "SUPPORT_WRITE_AUTHORIZATION_FORBIDDEN", key, findings)
        if isinstance(value, str):
            normalized_value = _normalize_claim_text(value)
            if _is_negative_claim(normalized_value):
                continue
            if kind == "manifest" and SUPPORT_GENERATED_INVENTORY_CLAIM_RE.search(normalized_value):
                _support_boundary_finding(root, path, data, pointer, "SUPPORT_GENERATED_INVENTORY_CLAIM", value, findings)
            if kind == "index" and SUPPORT_GENERATED_INDEX_CLAIM_RE.search(normalized_value):
                _support_boundary_finding(root, path, data, pointer, "SUPPORT_GENERATED_INDEX_CLAIM", value, findings)
            if SUPPORT_TEMPLATE_CLAIM_RE.search(normalized_value):
                _support_boundary_finding(root, path, data, pointer, "SUPPORT_TEMPLATE_EXECUTION_CLAIM", value, findings)
            if SUPPORT_COMMAND_CLAIM_RE.search(normalized_value):
                _support_boundary_finding(root, path, data, pointer, "SUPPORT_COMMAND_EXECUTION_CLAIM", value, findings)
            if SUPPORT_PERMISSION_CLAIM_RE.search(normalized_value):
                code = "SUPPORT_WRITE_AUTHORIZATION_FORBIDDEN" if "write" in normalized_value else "SUPPORT_PERMISSION_GRANT_FORBIDDEN"
                _support_boundary_finding(root, path, data, pointer, code, value, findings)


def _support_boundary_finding(
    root: Path,
    path: Path,
    data: dict[str, Any],
    pointer: str,
    code: str,
    actual: Any,
    findings: list[Finding],
) -> None:
    findings.append(
        _finding(
            code,
            path,
            pointer,
            _contract_id(data),
            "curated static reference-only support bundle with no generated, runtime, execution, body, command, permission, or write behavior",
            actual,
            "Keep support bundles as curated static references only; move behavior or copied payload claims out of durable support JSON.",
            root,
        )
    )


def _support_lookup_group(payload: dict[str, Any], lookup_group: str) -> tuple[int, dict[str, Any]] | None:
    groups = payload.get("lookup_groups")
    if not isinstance(groups, list):
        return None
    for index, group in enumerate(groups):
        if isinstance(group, dict) and group.get("lookup_group") == lookup_group:
            return index, group
    return None


def _lookup_group_refs(group: dict[str, Any], ref_key: str) -> dict[str, set[str]]:
    refs_by_lookup: dict[str, set[str]] = {}
    entries = group.get("entries")
    if not isinstance(entries, list):
        return refs_by_lookup
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("lookup_key"), str):
            continue
        refs = entry.get(ref_key)
        if isinstance(refs, list):
            refs_by_lookup[entry["lookup_key"]] = {ref for ref in refs if isinstance(ref, str)}
    return refs_by_lookup


def _lookup_entry_pointer(payload: dict[str, Any], lookup_group: str, lookup_key: str, field: str) -> str:
    groups = payload.get("lookup_groups")
    if not isinstance(groups, list):
        return "/payload/lookup_groups"
    for group_index, group in enumerate(groups):
        if not isinstance(group, dict) or group.get("lookup_group") != lookup_group:
            continue
        entries = group.get("entries")
        if not isinstance(entries, list):
            return f"/payload/lookup_groups/{group_index}/entries"
        for entry_index, entry in enumerate(entries):
            if isinstance(entry, dict) and entry.get("lookup_key") == lookup_key:
                return f"/payload/lookup_groups/{group_index}/entries/{entry_index}/{field}"
    return "/payload/lookup_groups"


def _validate_support_boundaries(
    root: Path,
    schema_files: list[Path],
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        if data.get("contract_kind") not in SUPPORT_KINDS:
            continue
        if data.get("classification") != "non_entity_static_reference_bundle":
            findings.append(
                _finding(
                    "SUPPORT_CLASSIFICATION_INVALID",
                    path,
                    "/classification",
                    _contract_id(data),
                    "non_entity_static_reference_bundle",
                    data.get("classification"),
                    "Support bundles must remain non-entity static reference bundles.",
                    root,
                )
            )
        _validate_boundary_flags(root, path, data, data, findings)

    for path in schema_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        _validate_positive_behavior_claims(root, path, data, data, findings)


def _validate_boundary_flags(
    root: Path,
    path: Path,
    data: Any,
    source_data: dict[str, Any],
    findings: list[Finding],
    pointer: str = "",
) -> None:
    for child_pointer, key, value in _walk_key_values(data, pointer or "/"):
        if key in FORBIDDEN_TRUE_FIELDS and value is not False:
            findings.append(
                _finding(
                    "SUPPORT_BOUNDARY_FLAG_INVALID",
                    path,
                    child_pointer,
                    _contract_id(source_data),
                    False,
                    value,
                    "Keep support bundles curated/read-only and non-runtime by setting boundary flags to false.",
                    root,
                )
            )
        if key in STATIC_TRUE_FIELDS and value is not True:
            findings.append(
                _finding(
                    "SUPPORT_CURATED_FLAG_INVALID",
                    path,
                    child_pointer,
                    _contract_id(source_data),
                    True,
                    value,
                    "Keep curated support-discovery flags true where the bundle declares them.",
                    root,
                )
            )
        if key == "generator_ref" and value is not None:
            findings.append(
                _finding(
                    "SUPPORT_GENERATOR_REF_INVALID",
                    path,
                    child_pointer,
                    _contract_id(source_data),
                    None,
                    value,
                    "Support bundles must not claim generated-index behavior in R1.10.",
                    root,
                )
            )
        if isinstance(value, str):
            _check_positive_behavior_string(root, path, source_data, child_pointer, value, findings)


def _validate_positive_behavior_claims(
    root: Path,
    path: Path,
    data: Any,
    source_data: dict[str, Any],
    findings: list[Finding],
) -> None:
    for pointer, _key, value in _walk_key_values(data):
        if isinstance(value, str):
            _check_positive_behavior_string(root, path, source_data, pointer, value, findings)


def _check_positive_behavior_string(
    root: Path,
    path: Path,
    source_data: dict[str, Any],
    pointer: str,
    value: str,
    findings: list[Finding],
) -> None:
    lowered = _normalize_claim_text(value)
    if _is_negative_claim(lowered):
        return
    behavior_words = (
        "command execution",
        "contract loader",
        "loader behavior",
        "resolver behavior",
        "resolver runtime",
        "runtime behavior",
        "selector behavior",
        "selector runtime",
        "write authorization",
        "write permission",
    )
    action_words = ("authorize", "create", "execute", "grant", "implement", "load", "select")
    if any(word in lowered for word in behavior_words) and any(word in lowered for word in action_words):
        findings.append(
            _finding(
                "BEHAVIOR_CLAIM_FORBIDDEN",
                path,
                pointer,
                _contract_id(source_data),
                "read-only/static denial language",
                value,
                "Schemas and support bundles must not claim runtime, loader, Resolver, selector, or write-authorization behavior.",
                root,
            )
        )


def _validate_deprecated_relationships(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    deprecated_refs: set[str] = set()
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        for pointer, key, value in _walk_key_values(data):
            if key == "deprecated_reserved_relationship_refs" and isinstance(value, list):
                for index, entry in enumerate(value):
                    if not isinstance(entry, dict):
                        continue
                    ref = entry.get("relationship_type_ref")
                    entry_pointer = f"{pointer}/{index}"
                    if isinstance(ref, str):
                        deprecated_refs.add(ref)
                        if ref not in contract_index:
                            findings.append(
                                _finding(
                                    "DEPRECATED_RELATIONSHIP_REF_NOT_FOUND",
                                    path,
                                    entry_pointer + "/relationship_type_ref",
                                    _contract_id(data),
                                    "existing deprecated relationship type",
                                    ref,
                                    "Reference an existing deprecated relationship type contract.",
                                    root,
                                )
                            )
                        elif contract_index[ref].get("status") != "deprecated":
                            findings.append(
                                _finding(
                                    "DEPRECATED_RELATIONSHIP_STATUS_INVALID",
                                    path,
                                    entry_pointer + "/relationship_type_ref",
                                    _contract_id(data),
                                    "relationship contract with status deprecated",
                                    contract_index[ref].get("status"),
                                    "Mark deprecated reserved relationship type contracts as deprecated.",
                                    root,
                                )
                            )
                    if entry.get("active_resolver_candidate") is not False:
                        findings.append(
                            _finding(
                                "DEPRECATED_ACTIVE_CANDIDATE_INVALID",
                                path,
                                entry_pointer + "/active_resolver_candidate",
                                _contract_id(data),
                                False,
                                entry.get("active_resolver_candidate"),
                                "Deprecated relationship refs must not be active resolver candidates.",
                                root,
                            )
                        )
                    if entry.get("provenance_discoverable_only") is not True:
                        findings.append(
                            _finding(
                                "DEPRECATED_PROVENANCE_FLAG_INVALID",
                                path,
                                entry_pointer + "/provenance_discoverable_only",
                                _contract_id(data),
                                True,
                                entry.get("provenance_discoverable_only"),
                                "Deprecated relationship refs must remain provenance-discoverable only.",
                                root,
                            )
                        )
                    replacement = entry.get("canonical_replacement_ref")
                    if isinstance(replacement, str) and replacement not in contract_index:
                        findings.append(
                            _finding(
                                "DEPRECATED_REPLACEMENT_NOT_FOUND",
                                path,
                                entry_pointer + "/canonical_replacement_ref",
                                _contract_id(data),
                                "existing canonical replacement relationship type",
                                replacement,
                                "Reference an existing canonical replacement relationship type.",
                                root,
                            )
                        )

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        contract_id = data.get("id")
        if contract_id in deprecated_refs:
            if data.get("status") != "deprecated":
                findings.append(
                    _finding(
                        "DEPRECATED_RELATIONSHIP_STATUS_INVALID",
                        path,
                        "/status",
                        _contract_id(data),
                        "deprecated",
                        data.get("status"),
                        "Deprecated reserved relationship contracts must have deprecated status.",
                        root,
                    )
                )
            for pointer, key, value in _walk_key_values(data):
                if key == "active_resolver_candidate" and value is not False:
                    findings.append(
                        _finding(
                            "DEPRECATED_ACTIVE_CANDIDATE_INVALID",
                            path,
                            pointer,
                            _contract_id(data),
                            False,
                            value,
                            "Deprecated relationship contracts must not be active resolver candidates.",
                            root,
                        )
                    )


def _validate_entity_payload_ownership(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "entity":
            continue
        family = data.get("entity_family")
        payload = data.get("payload")
        if not isinstance(family, str) or family not in ENTITY_PAYLOAD_ALLOWED_KEYS or not isinstance(payload, dict):
            continue
        contract_id = _contract_id(data)
        allowed_keys = ENTITY_PAYLOAD_ALLOWED_KEYS[family]

        for key, value in payload.items():
            pointer = "/payload/" + escape_pointer_token(key)
            if key not in allowed_keys:
                findings.append(
                    _finding(
                        "ENTITY_PAYLOAD_FIELD_NOT_OWNED",
                        path,
                        pointer,
                        contract_id,
                        sorted(allowed_keys),
                        key,
                        "Keep entity payloads to their normalized entity-owned fields; move relationship, ownership, or support facts to their owning contract family.",
                        root,
                    )
                )
            if key in RELATIONSHIP_OWNED_KEYS:
                findings.append(
                    _finding(
                        "RELATIONSHIP_FACT_OUTSIDE_RELACION",
                        path,
                        pointer,
                        contract_id,
                        "relationship fact stored in a relacion contract payload",
                        key,
                        "Move origen/destino/tipo/cardinality relationship facts into contracts/relacion records.",
                        root,
                    )
                )

            exception_keys = ENTITY_CROSS_FAMILY_REF_EXCEPTIONS.get(family, set())
            if key in exception_keys:
                continue
            for value_pointer, stable_id in _iter_stable_ref_values(value, pointer):
                ref_family = stable_id.split(".", 1)[0]
                if ref_family == family:
                    continue
                findings.append(
                    _finding(
                        "ENTITY_PAYLOAD_CROSS_FAMILY_FACT",
                        path,
                        value_pointer,
                        contract_id,
                        f"{family}-owned scalar or same-family ref only",
                        stable_id,
                        "Do not reintroduce cross-family facts into entity payloads; represent cross-family facts as relacion contracts or curated support refs.",
                        root,
                    )
                )


def _validate_relationship_ownership(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        contract_kind = data.get("contract_kind")
        entity_family = data.get("entity_family")
        contract_id = _contract_id(data)
        is_relationship_owner = contract_kind == "relationship" and entity_family == "relacion"

        if contract_kind == "relationship" and entity_family != "relacion":
            findings.append(
                _finding(
                    "RELATIONSHIP_OWNER_INVALID",
                    path,
                    "/entity_family",
                    contract_id,
                    "relacion",
                    entity_family,
                    "Relationship contracts must be owned by the relacion family.",
                    root,
                )
            )
        if entity_family == "relacion" and contract_kind != "relationship":
            findings.append(
                _finding(
                    "RELATIONSHIP_OWNER_INVALID",
                    path,
                    "/contract_kind",
                    contract_id,
                    "relationship",
                    contract_kind,
                    "Relación family records must remain relationship contracts.",
                    root,
                )
            )

        if is_relationship_owner:
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        for pointer, key, _value in _walk_key_values(payload, "/payload"):
            if key not in RELATIONSHIP_OWNED_KEYS:
                continue
            findings.append(
                _finding(
                    "RELATIONSHIP_FACT_OUTSIDE_RELACION",
                    path,
                    pointer,
                    contract_id,
                    "relationship fact stored in a relacion contract payload",
                    key,
                    "Keep relationship endpoint, type, cardinality, required, and order facts inside contracts/relacion records only.",
                    root,
                )
            )


def _validate_support_reference_only_ownership(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") not in SUPPORT_KINDS:
            continue
        contract_kind = data["contract_kind"]
        contract_id = _contract_id(data)
        payload = data.get("payload")

        expected_path = _expected_support_owner_path(contract_kind)
        if not _support_owner_path_matches(root, path, contract_kind):
            findings.append(
                _finding(
                    "SUPPORT_OWNER_PATH_DRIFT",
                    path,
                    "/contract_kind",
                    contract_id,
                    expected_path,
                    _rel(root, path),
                    "Keep manifest, index, selector, and policy/reference bundle ownership aligned with their canonical support paths.",
                    root,
                )
            )

        if not isinstance(payload, dict):
            continue
        allowed_keys = SUPPORT_PAYLOAD_ALLOWED_KEYS[contract_kind]
        required_keys = SUPPORT_REQUIRED_OWNER_KEYS[contract_kind]
        for key in payload:
            if key in allowed_keys:
                continue
            findings.append(
                _finding(
                    "SUPPORT_OWNERSHIP_DRIFT",
                    path,
                    "/payload/" + escape_pointer_token(key),
                    contract_id,
                    sorted(allowed_keys),
                    key,
                    "Keep support-bundle data under its owning manifest, index, selector, or policy field set.",
                    root,
                )
            )
        for key in sorted(required_keys):
            if key in payload:
                continue
            findings.append(
                _finding(
                    "SUPPORT_OWNER_KEY_MISSING",
                    path,
                    "/payload/" + escape_pointer_token(key),
                    contract_id,
                    "support owner key present",
                    "missing",
                    "Keep each support bundle's owner-defining fields present.",
                    root,
                )
            )

        for pointer, key, value in _walk_key_values(payload, "/payload"):
            if key in SUPPORT_BODY_COPY_KEYS:
                findings.append(
                    _finding(
                        "SUPPORT_REFERENCE_ONLY_VIOLATION",
                        path,
                        pointer,
                        contract_id,
                        "curated references only; no copied contract bodies, payloads, content, or generated output",
                        key,
                        "Replace copied bodies or generated content with contract ids, paths, and curated reference metadata only.",
                        root,
                    )
                )
            if key == "body_inclusion_policy" and isinstance(value, str) and not _is_reference_only_policy(value):
                findings.append(
                    _finding(
                        "SUPPORT_BODY_INCLUSION_POLICY_INVALID",
                        path,
                        pointer,
                        contract_id,
                        "reference-only body inclusion policy",
                        value,
                        "Support bundles must explicitly preserve reference-only/no-body/no-payload inclusion semantics.",
                        root,
                    )
                )


def _validate_durable_live_state_boundary(
    root: Path,
    schema_files: list[Path],
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in [*schema_files, *contract_files]:
        data = parsed.get(path)
        if data is None:
            continue
        source_data = data if isinstance(data, dict) else {}
        for pointer, key, value in _walk_key_values(data):
            if _is_under_source_refs(pointer):
                continue
            if key in LIVE_STATE_KEYS:
                findings.append(
                    _finding(
                        "DURABLE_LIVE_STATE_FIELD_FORBIDDEN",
                        path,
                        pointer,
                        _contract_id(source_data),
                        "durable reference metadata without live GitHub/review/validation/branch/release state fields",
                        key,
                        "Keep mutable GitHub truth, validation output, review verdicts, branch state, issue/PR state, closure state, and release state as external evidence.",
                        root,
                    )
                )
            if isinstance(value, str) and _looks_like_live_state_literal(value):
                findings.append(
                    _finding(
                        "DURABLE_LIVE_STATE_VALUE_FORBIDDEN",
                        path,
                        pointer,
                        _contract_id(source_data),
                        "external live evidence reference, not copied live state value",
                        value,
                        "Replace copied live GitHub URLs, commit SHAs, or mutable evidence values with abstract source/resource/evidence references.",
                        root,
                    )
                )


def _validate_actor_hard_limit_duplication(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "entity":
            continue
        if data.get("entity_family") == "limite":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        entity_family = data.get("entity_family")
        for pointer, key, _value in _walk_key_values(payload, "/payload"):
            if _is_resolver_output_limite_reference_field(entity_family, pointer, key):
                continue
            if not _is_actor_hard_limit_duplication_key(key):
                continue
            findings.append(
                _finding(
                    "ACTOR_HARD_LIMIT_DUPLICATED",
                    path,
                    pointer,
                    _contract_id(data),
                    "actor hard limits represented as limite entities plus relacion.actor.*.tiene.limite records",
                    key,
                    "Do not duplicate actor hard-limit lists or boundary actions into entity payloads or lower-layer contracts.",
                    root,
                )
            )


def _validate_workflow_step_rule_ownership(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    active_role_regla_destinations: set[str] = set()

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "relationship":
            continue
        if data.get("status") != "active":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        if (
            payload.get("origen_entidad") == "rol"
            and payload.get("destino_entidad") == "regla"
            and payload.get("tipo_relacion") == "aplica"
        ):
            destino_id = payload.get("destino_id")
            if isinstance(destino_id, str):
                active_role_regla_destinations.add(destino_id)

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "relationship":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        if (
            payload.get("origen_entidad") != "workflow_step"
            or payload.get("destino_entidad") != "regla"
            or payload.get("tipo_relacion") != "aplica"
        ):
            continue

        destino_id = payload.get("destino_id")
        if not isinstance(destino_id, str):
            continue

        if WORKFLOW_STEP_REGLA_ID_RE.fullmatch(destino_id) is None:
            findings.append(
                _finding(
                    "WORKFLOW_STEP_REGLA_ID_PATTERN_MISMATCH",
                    path,
                    "/payload/destino_id",
                    _contract_id(data),
                    "workflow_step-prefixed regla id matching /^regla\\.workflow_step_[a-z0-9_]+_.*\\.v1$/",
                    destino_id,
                    "Use the WorkflowStep-owned regla id prefix and naming pattern under contracts/regla.",
                    root,
                )
            )
            continue

        if data.get("status") == "active" and destino_id in active_role_regla_destinations:
            findings.append(
                _finding(
                    "WORKFLOW_STEP_REGLA_DUPLICATES_ACTIVE_ROLE_RULE_DESTINATION",
                    path,
                    "/payload/destino_id",
                    _contract_id(data),
                    "a destination id not used by active rol.aplica.regla relationships",
                    destino_id,
                    "Choose WorkflowStep-owned rule IDs that do not duplicate active role-owned destination IDs.",
                    root,
                )
            )


def _validate_role_permission_boundary(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") != "entity" or data.get("entity_family") != "rol":
            continue
        payload = data.get("payload")
        if not isinstance(payload, dict):
            continue
        contract_id = _contract_id(data)
        for pointer, key, value in _walk_key_values(payload, "/payload"):
            if _is_role_permission_key(key):
                findings.append(
                    _finding(
                        "ROLE_PERMISSION_GRANT_FORBIDDEN",
                        path,
                        pointer,
                        contract_id,
                        "role lens metadata only; no permission, authority, write, merge, close, commit, or push grants",
                        key,
                        "Role contracts are professional lenses only and must not grant permissions.",
                        root,
                    )
                )
            if isinstance(value, str) and _is_positive_role_permission_claim(value):
                findings.append(
                    _finding(
                        "ROLE_PERMISSION_GRANT_FORBIDDEN",
                        path,
                        pointer,
                        contract_id,
                        "role lens metadata only; no permission, authority, write, merge, close, commit, or push grants",
                        value,
                        "Replace permission-grant language with non-authorizing role lens metadata.",
                        root,
                    )
                )


def _validate_deprecated_relationship_active_candidates(
    root: Path,
    contract_files: list[Path],
    parsed: dict[Path, Any],
    contract_index: dict[str, Any],
    findings: list[Finding],
) -> None:
    deprecated_relationship_ids = {
        contract_id
        for contract_id, data in contract_index.items()
        if isinstance(data, dict) and data.get("contract_kind") == "relationship" and data.get("status") == "deprecated"
    }
    if not deprecated_relationship_ids:
        return

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        contract_id = _contract_id(data)
        if contract_id in deprecated_relationship_ids:
            for pointer, key, value in _walk_key_values(data):
                if key == "active_resolver_candidate" and value is not False:
                    findings.append(
                        _finding(
                            "DEPRECATED_ACTIVE_CANDIDATE_INVALID",
                            path,
                            pointer,
                            contract_id,
                            False,
                            value,
                            "Deprecated relationship type contracts must not be active Resolver candidates.",
                            root,
                        )
                    )

        for object_pointer, obj in _walk_objects(data):
            ref = obj.get("relationship_type_ref")
            if ref not in deprecated_relationship_ids:
                continue
            if "active_resolver_candidate" not in obj:
                continue
            if obj.get("active_resolver_candidate") is False:
                continue
            findings.append(
                _finding(
                    "DEPRECATED_ACTIVE_CANDIDATE_INVALID",
                    path,
                    join_pointer(object_pointer, "active_resolver_candidate"),
                    contract_id,
                    False,
                    obj.get("active_resolver_candidate", "missing"),
                    "Deprecated relationship type refs must not be presented as active Resolver candidates.",
                    root,
                )
            )


def _validate_behavior_claim_boundaries(
    root: Path,
    schema_files: list[Path],
    contract_files: list[Path],
    parsed: dict[Path, Any],
    findings: list[Finding],
) -> None:
    for path in schema_files:
        data = parsed.get(path)
        if not isinstance(data, dict):
            continue
        _validate_schema_behavior_field_denials(root, path, data, findings)
        _validate_positive_behavior_claims(root, path, data, data, findings)

    for path in contract_files:
        data = parsed.get(path)
        if not isinstance(data, dict) or data.get("contract_kind") not in SUPPORT_KINDS:
            continue
        _validate_boundary_flags(root, path, data, data, findings)


def _validate_schema_behavior_field_denials(
    root: Path,
    path: Path,
    data: dict[str, Any],
    findings: list[Finding],
) -> None:
    for pointer, key, value in _walk_key_values(data):
        if key not in BEHAVIOR_SCHEMA_DENIAL_FIELDS or not isinstance(value, dict):
            continue
        if value.get("const") is False:
            continue
        findings.append(
            _finding(
                "SCHEMA_BEHAVIOR_FIELD_NOT_DENIED",
                path,
                pointer,
                None,
                {"const": False},
                value,
                "Schemas may define boundary flags only when they deny runtime, loader, Resolver, selector, command execution, generated output, or write-authorization behavior.",
                root,
            )
        )


def _walk_key_values(value: Any, pointer: str = "") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = join_pointer(pointer or "/", key)
            yield child_pointer, key, child
            yield from _walk_key_values(child, child_pointer)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_key_values(child, join_pointer(pointer or "/", index))


def _walk_objects(value: Any, pointer: str = "") -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        current_pointer = pointer or "/"
        yield current_pointer, value
        for key, child in value.items():
            yield from _walk_objects(child, join_pointer(current_pointer, key))
    elif isinstance(value, list):
        current_pointer = pointer or "/"
        for index, child in enumerate(value):
            yield from _walk_objects(child, join_pointer(current_pointer, index))


def _iter_stable_ref_values(value: Any, pointer: str) -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        if STABLE_ID_RE.fullmatch(value) is not None:
            yield pointer, value
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_stable_ref_values(item, join_pointer(pointer, index))
        return
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _iter_stable_ref_values(item, join_pointer(pointer, key))


def _expected_support_owner_path(contract_kind: str) -> str:
    if contract_kind == "manifest":
        return "contracts/manifest.json"
    if contract_kind == "index":
        return "contracts/index.json"
    if contract_kind == "reference_bundle":
        return "contracts/policy/*.json"
    if contract_kind == "selector":
        return "contracts/selector/*.json"
    return "canonical support path"


def _support_owner_path_matches(root: Path, path: Path, contract_kind: str) -> bool:
    rel = _rel(root, path)
    if contract_kind == "manifest":
        return rel == "contracts/manifest.json"
    if contract_kind == "index":
        return rel == "contracts/index.json"
    if contract_kind == "reference_bundle":
        return rel.startswith("contracts/policy/") and rel.endswith(".json")
    if contract_kind == "selector":
        return rel.startswith("contracts/selector/") and rel.endswith(".json")
    return False


def _is_reference_only_policy(value: str) -> bool:
    normalized = _normalize_claim_text(value)
    return "reference" in normalized and "only" in normalized and "no" in normalized


def _is_under_source_refs(pointer: str) -> bool:
    return pointer == "/source_refs" or pointer.startswith("/source_refs/")


def _looks_like_live_state_literal(value: str) -> bool:
    return any(pattern.search(value) is not None for pattern in LIVE_STATE_VALUE_PATTERNS)


def _is_actor_hard_limit_duplication_key(key: str) -> bool:
    normalized = key.lower()
    return (
        normalized in ACTOR_HARD_LIMIT_DUPLICATION_KEYS
        or normalized.endswith("_limit_refs")
        or normalized.endswith("_limite_refs")
        or "hard_limit" in normalized
    )


def _is_resolver_output_limite_reference_field(entity_family: Any, pointer: str, key: str) -> bool:
    return (
        entity_family == "resolver_output"
        and pointer == f"/payload/{key}"
        and key in RESOLVER_OUTPUT_LIMITE_REF_REFERENCE_KEYS
    )


def _is_role_permission_key(key: str) -> bool:
    normalized = key.lower()
    return (
        normalized in ROLE_PERMISSION_KEYS
        or normalized.startswith("can_")
        or "permission" in normalized
        or "write_authorization" in normalized
        or "write_permission" in normalized
    )


def _is_positive_role_permission_claim(value: str) -> bool:
    normalized = _normalize_claim_text(value)
    if _is_negative_claim(normalized):
        return False
    return ROLE_PERMISSION_VALUE_RE.search(normalized) is not None


def _normalize_claim_text(value: str) -> str:
    return re.sub(r"[-_]+", " ", value.lower())


def _is_negative_claim(normalized: str) -> bool:
    padded = f" {normalized} "
    return (
        " does not " in padded
        or " do not " in padded
        or " not " in padded
        or " no " in padded
        or normalized.startswith("no ")
        or " without " in padded
        or " deny " in padded
        or " denies " in padded
        or " denied " in padded
        or " non " in padded
        or normalized.startswith("non ")
        or "reference only" in normalized
        or "data shape only" in normalized
        or "shape only" in normalized
    )


def _contract_id(data: Any) -> str | None:
    if isinstance(data, dict) and isinstance(data.get("id"), str):
        return data["id"]
    return None


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _finding(
    code: str,
    path: Path,
    pointer: str,
    contract_id: str | None,
    expected: Any,
    actual: Any,
    hint: str,
    root: Path,
) -> Finding:
    return Finding(
        code=code,
        severity="error",
        file=_rel(root, path),
        pointer=pointer or "/",
        contract_id=contract_id,
        expected=expected,
        actual=actual,
        hint=hint,
    )
