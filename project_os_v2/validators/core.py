"""R1.10 schema and reference validators."""

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
        if all(value is None for value in payload_values):
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
        elif type_contract.get("status") == "deprecated":
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


def _embedded_contract_id(contract_id: str) -> str:
    body = contract_id.removesuffix(".v1")
    family, _, slug = body.partition(".")
    if not slug:
        return body
    return family + "." + slug.replace(".", "_")


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
    lowered = value.lower().replace("-", " ")
    if "does not" in lowered or " not " in f" {lowered} " or lowered.startswith("no_") or lowered.startswith("no "):
        return
    behavior_words = ("runtime", "loader", "resolver behavior", "selector runtime", "write authorization")
    action_words = ("implement", "create", "execute", "authorize", "load", "select")
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


def _walk_key_values(value: Any, pointer: str = "") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = join_pointer(pointer or "/", key)
            yield child_pointer, key, child
            yield from _walk_key_values(child, child_pointer)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_key_values(child, join_pointer(pointer or "/", index))


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
