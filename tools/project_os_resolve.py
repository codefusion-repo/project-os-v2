"""Principal deterministic resolver for the allowed Project OS kernels.

The resolver defaults to ``project-os-es/kernel`` and may explicitly resolve
``project-os-en/kernel``. It hydrates one ``(actor, mode, workflow)`` selection
and fails closed for every other path.

The resulting JSON is operative guidance only.  It never reads GitHub or git,
mutates files, grants permission, or replaces exact PM approval and the
kernel-resolved gates.
"""

from __future__ import annotations

import argparse
import json
import sys
from enum import Enum
from pathlib import Path
from typing import Any

try:
    from tools.project_os_surfaces import (
        DEFAULT_KERNEL_DIR,
        DEFAULT_SURFACE,
        ProjectOSSurface,
        select_surface,
    )
except ModuleNotFoundError:  # Direct ``python tools/project_os_resolve.py`` execution.
    from project_os_surfaces import (  # type: ignore[no-redef]
        DEFAULT_KERNEL_DIR,
        DEFAULT_SURFACE,
        ProjectOSSurface,
        select_surface,
    )

MODE_FALLBACK = "mode.review_only"
AUTHORIZATION_NOTICE = DEFAULT_SURFACE.authorization_notice


class DensityLevel(str, Enum):
    """Safe internal names for the public density vocabulary.

    Two independent axes read these values: the hydration level, which selects
    how much resolved contract the agent receives, and the report density, which
    selects one output's ``must_include`` obligation. Sharing the vocabulary
    never couples the axes.
    """

    MINIMAL = "minimal"
    COMPACT = "compact"
    FULL_DEBUG = "full/debug"


# Hydration is a deliberate view over the resolved contract, never a function of
# risk: every resolution defaults to compact and only an explicit override asks
# for the minimal projection or the full/debug one used to audit or debug.
DEFAULT_HYDRATION_LEVEL = DensityLevel.COMPACT
HYDRATION_LEVEL_VALUES = tuple(level.value for level in DensityLevel)

# The report density stays proportional to risk and is read from its single
# canonical source, the class's ``output_density``. A resolution without a
# declared class never mutates, so it keeps the same practical default.
DEFAULT_REPORT_DENSITY = DensityLevel.COMPACT

# Gates the resolver only shapes; they must be enforced with actor capability,
# live evidence, and exact PM approval, not by this deterministic resolution.
REMAINING_GATE_SOURCES = {
    "formal_unit_required": "live_work_unit_or_exact_pm_decision",
    "pr_required": "delegated_mode_capability_and_target_policy",
    "review_level": "review_before_close_at_the_class_level",
    "validation_level": "agent_or_ci_validation_output",
    "prior_docs": "durable_docs_or_adr_before_implementation",
}


def _fail_closed(
    errors: list[str],
    surface: ProjectOSSurface = DEFAULT_SURFACE,
    hydration_level: DensityLevel | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {"estado": "status.blocked"}
    if hydration_level is not None:
        result["hydration_level"] = hydration_level.value
    result.update(
        {
            "resuelto": None,
            "autorizacion": surface.authorization_notice,
            "errores": errors,
        }
    )
    return result


def _parse_hydration_level(
    hydration_level: str | DensityLevel | None,
    compact: str | DensityLevel | None,
) -> tuple[DensityLevel | None, list[str]]:
    """Validate one explicit level without silently falling back.

    ``compact`` is a Python compatibility alias. The command-line ``--compact``
    flag remains reserved for compact JSON formatting, so ``--hydration-level``
    is the unambiguous CLI spelling.
    """

    if hydration_level is not None and compact is not None:
        return None, ["hydration_level and compact cannot be supplied together"]
    value = hydration_level if hydration_level is not None else compact
    if value is None:
        return DEFAULT_HYDRATION_LEVEL, []
    try:
        return DensityLevel(value), []
    except (TypeError, ValueError):
        return None, [
            "unknown hydration level; expected exactly one of: "
            + ", ".join(HYDRATION_LEVEL_VALUES)
        ]


def _load(
    kernel_dir: Path, surface: ProjectOSSurface
) -> tuple[dict[str, Any], list[str]]:
    data: dict[str, Any] = {}
    errors: list[str] = []
    for family, (filename, collection) in surface.kernel_files.items():
        path = kernel_dir / filename
        if not path.is_file():
            errors.append(f"{surface.messages['missing_file']}: {path}")
            continue
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{surface.messages['invalid_file']}: {filename}: {exc}")
            continue
        entries = content.get(collection) if isinstance(content, dict) else None
        if not isinstance(entries, list):
            errors.append(f"{filename} {surface.messages['missing_collection']} '{collection}'")
            continue
        data[family] = [entry for entry in entries if isinstance(entry, dict) and entry.get("active")]
        contract_fields = {
            "evidence": ("materiality_contract",),
            "workflows": ("proportionality_contract",),
            "outputs": ("safe_degradation_contract", "context_receipt_contract"),
        }.get(family, ())
        for contract_field in contract_fields:
            contract = content.get(contract_field)
            if not isinstance(contract, dict):
                errors.append(f"{filename} {surface.messages['missing_collection']} '{contract_field}'")
            else:
                data[contract_field] = contract
    return data, errors


def _index(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {entry["key"]: entry for entry in entries if isinstance(entry.get("key"), str)}


def _resolve_change_class(
    change_class: str | None,
    contract: Any,
    workflow_key: str,
    surface: ProjectOSSurface,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Resolve one declared change class against the structured contract.

    The class never grants authority: it selects the proportionality contract
    (unit, PR, review, validation, density) and must be coherent with the
    selected workflow, or the resolution fails closed.
    """

    if change_class is None:
        return None, []
    classes = contract.get("classes") if isinstance(contract, dict) else None
    entries = {
        entry["key"]: entry
        for entry in (classes if isinstance(classes, list) else [])
        if isinstance(entry, dict) and isinstance(entry.get("key"), str)
    }
    entry = entries.get(change_class)
    if entry is None:
        return None, [
            f"{surface.messages['unknown_change_class']}: {change_class!r} "
            f"({surface.messages['known']}: {sorted(entries)})"
        ]
    if workflow_key not in entry.get("allowed_workflows", []):
        return None, [
            f"{surface.messages['incompatible_change_class']}: "
            f"{change_class!r} -> {workflow_key!r}"
        ]
    return entry, []


def _remaining_gates(change_class: dict[str, Any]) -> list[dict[str, Any]]:
    """Surface the class gates the resolver cannot verify as enforceable obligations.

    The class selects unit, PR, review, validation, and prior-docs requirements,
    but the resolver reads no live evidence, so these remain to be enforced by the
    actor's real capability, live evidence, and exact PM approval. They are listed
    as gates, never as descriptive metadata that could be silently skipped.
    """

    return [
        {"gate": gate, "required": change_class.get(gate), "enforced_by": source}
        for gate, source in REMAINING_GATE_SOURCES.items()
    ]


def _projected_must_include(item: dict[str, Any], density: DensityLevel) -> Any:
    """Project the single applicable must_include list for one report density.

    The density comes from the declared class, so a critical unit keeps its
    detailed report obligation even when the agent asked for a compact
    resolution.
    """

    by_density = item.get("must_include_by_density")
    if isinstance(by_density, dict):
        return by_density.get(density.value)
    return item.get("must_include")


def _fields(entry: dict[str, Any], *names: str) -> dict[str, Any]:
    return {name: entry.get(name) for name in names}


def _project_root(kernel_dir: Path) -> Path:
    return kernel_dir.parent.parent


def _valid_project_path(path_value: Any, prefix: tuple[str, ...], kernel_dir: Path) -> bool:
    if not isinstance(path_value, str):
        return False
    path = Path(path_value)
    return (
        not path.is_absolute()
        and path.parts[: len(prefix)] == prefix
        and path.suffix == ".md"
        and (_project_root(kernel_dir) / path).is_file()
    )


def _hydrate(
    keys: list[str],
    index: dict[str, dict[str, Any]],
    kind: str,
    surface: ProjectOSSurface,
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    hydrated: dict[str, dict[str, Any]] = {}
    for key in keys:
        entry = index.get(key)
        if entry is None:
            message = (
                f"{kind} required by the workflow was not found"
                if surface.language == "en"
                else f"{kind} requerida por el workflow no encontrada"
            )
            errors.append(f"{message}: {key}")
        else:
            hydrated[key] = entry
    return hydrated


def _resolve_artifacts(
    workflow: dict[str, Any],
    outputs: dict[str, dict[str, Any]],
    artifacts: list[dict[str, Any]],
    kernel_dir: Path,
    surface: ProjectOSSurface,
    errors: list[str],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for artifact in artifacts:
        if workflow["key"] not in artifact.get("workflow_key", []):
            continue
        if artifact.get("output_key") not in (None, *outputs):
            continue
        template = artifact.get("required_template")
        if not _valid_project_path(template, surface.templates_prefix, kernel_dir):
            errors.append(f"{surface.messages['missing_template']}: {artifact.get('key')}: {template}")
            continue
        resolved.append(
            {
                **_fields(artifact, "key", "output_key"),
                "responsabilidad": artifact.get("responsabilidad", artifact.get("responsibility")),
                **_fields(artifact, "required_template", "active"),
            }
        )
    return resolved


def _resolve_skills(
    requested: list[str],
    skills: dict[str, dict[str, Any]],
    kernel_dir: Path,
    surface: ProjectOSSurface,
    errors: list[str],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for key in dict.fromkeys(requested):
        skill = skills.get(key)
        if skill is None:
            errors.append(
                f"{surface.messages['unknown_skill']}: {key!r} "
                f"({surface.messages['known']}: {sorted(skills)})"
            )
            continue
        required_skill = skill.get("required_skill")
        if not _valid_project_path(required_skill, surface.skills_prefix, kernel_dir):
            errors.append(f"{surface.messages['missing_skill_file']}: {key}: {required_skill}")
            continue
        resolved.append(
            {
                "key": skill.get("key"),
                "nombre": skill.get("nombre", skill.get("name")),
                "responsabilidad": skill.get("responsabilidad", skill.get("responsibility")),
                **_fields(skill, "required_skill", "use_for", "non_authorization", "active"),
            }
        )
    return resolved


def _safety_limits(limits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep every applicable limit and its blocking meaning at every level."""

    return [
        _fields(limit, "key", "rule", "on_violation", "blocking")
        for limit in limits
    ]


def _required_evidence(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the complete required-evidence contract at every level."""

    return [
        _fields(
            item,
            "key",
            "satisfied_by",
            "missing_status",
            "required",
            "materiality",
            "hard_gate",
            "source",
            "revalidation_required_before_write",
        )
        for item in evidence
    ]


def _allowed_outputs(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep allowed-output constraints rather than only their identifiers.

    ``must_include`` is already the single density projection applied while
    building the complete resolution, so every level carries one obligation.
    """

    return [
        _fields(
            item,
            "key",
            "use_for",
            "status_key",
            "action_class",
            "allows_non_material_gaps",
            "safe_degradation_key",
            "context_receipt_key",
            "must_include",
        )
        for item in outputs
    ]


def _referenced_statuses(statuses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep referenced status meanings, not only status identifiers."""

    return [_fields(status, "key", "meaning", "type") for status in statuses]


def _minimal_requested_skills(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep a requested capability's identity and non-authorizing boundary."""

    return [
        _fields(skill, "key", "required_skill", "non_authorization")
        for skill in skills
    ]


def _compact_requested_skills(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep concise, usable requested-skill references for normal execution."""

    return [
        _fields(
            skill,
            "key",
            "nombre",
            "responsabilidad",
            "required_skill",
            "use_for",
            "non_authorization",
        )
        for skill in skills
    ]


def _minimal_resolution(resolved: dict[str, Any]) -> dict[str, Any]:
    """Project the explicit non-omittable safety contract for minimal output."""

    workflow = resolved["workflow"]
    projected: dict[str, Any] = {
        "manifest": _fields(resolved["manifest"], "key", "version", "language"),
        "actor": _fields(resolved["actor"], "key"),
        "limites": _safety_limits(resolved["limites"]),
        "mode": _fields(resolved["mode"], "key", "prohibited_actions", "fallback"),
        "workflow": {
            "key": workflow["key"],
            "materiality_contract": workflow["materiality_contract"],
            "safe_degradation_contract": workflow["safe_degradation_contract"],
            "context_receipt_contract": workflow["context_receipt_contract"],
            "required_evidence": _required_evidence(workflow["required_evidence"]),
            "minimum_evidence": _required_evidence(workflow["minimum_evidence"]),
            "allowed_outputs": _allowed_outputs(workflow["allowed_outputs"]),
        },
        "estados_permitidos": _referenced_statuses(resolved["estados_permitidos"]),
    }
    if "change_class" in resolved:
        projected["change_class"] = resolved["change_class"]
    if "requested_skills" in resolved:
        projected["requested_skills"] = _minimal_requested_skills(resolved["requested_skills"])
    return projected


def _compact_resolution(resolved: dict[str, Any]) -> dict[str, Any]:
    """Project concise mandatory guidance for ordinary agent execution."""

    workflow = resolved["workflow"]
    projected: dict[str, Any] = {
        "manifest": _fields(
            resolved["manifest"],
            "key",
            "version",
            "language",
            "objetivo",
            "resolution_sequence",
        ),
        "reglas_operativas": [
            _fields(rule, "key", "resolution_sequence", "on_violation", "priority")
            for rule in resolved["reglas_operativas"]
        ],
        "actor": _fields(resolved["actor"], "key", "surface", "context", "allowed_modes"),
        "limites": _safety_limits(resolved["limites"]),
        "mode": _fields(
            resolved["mode"],
            "key",
            "allowed_actions",
            "prohibited_actions",
            "fallback",
        ),
        "workflow": {
            "key": workflow["key"],
            "use_for": workflow["use_for"],
            "required_behavior": workflow["required_behavior"],
            "materiality_contract": workflow["materiality_contract"],
            "safe_degradation_contract": workflow["safe_degradation_contract"],
            "context_receipt_contract": workflow["context_receipt_contract"],
            "required_evidence": _required_evidence(workflow["required_evidence"]),
            "minimum_evidence": _required_evidence(workflow["minimum_evidence"]),
            "allowed_outputs": _allowed_outputs(workflow["allowed_outputs"]),
            "artefactos": [
                _fields(
                    artifact,
                    "key",
                    "output_key",
                    "responsabilidad",
                    "required_template",
                )
                for artifact in workflow["artefactos"]
            ],
        },
        "estados_permitidos": _referenced_statuses(resolved["estados_permitidos"]),
    }
    if "change_class" in resolved:
        projected["change_class"] = resolved["change_class"]
    if "requested_skills" in resolved:
        projected["requested_skills"] = _compact_requested_skills(resolved["requested_skills"])
    return projected


def _project_resolution(
    resolved: dict[str, Any], hydration_level: DensityLevel
) -> dict[str, Any]:
    """Apply one explicit view after resolving the complete internal contract.

    This selects only how much contract is returned. It never decides an
    output's ``must_include``, which the report density already resolved.
    """

    if hydration_level is DensityLevel.MINIMAL:
        return _minimal_resolution(resolved)
    if hydration_level is DensityLevel.COMPACT:
        return _compact_resolution(resolved)
    return resolved


def _context_plan(
    resolved: dict[str, Any],
    projected: dict[str, Any],
    provenance_reason: str,
    surface: ProjectOSSurface,
) -> dict[str, Any]:
    """Report resolver-observable provenance for one explicit audit or debugging request.

    This is never part of a normal resolution: the caller must ask for it with an
    allowed reason. It carries only what the resolver alone observes; anything the
    resolution already states (contract key, hydration level, normal read surface,
    executor-reported fields, external-access flag) is read from the resolved
    contract instead of being duplicated here.
    """

    kernel_sources = {
        "manifest": ("manifest",),
        "reglas_operativas": ("operational_rules",),
        "actor": ("actors",),
        "limites": ("limits",),
        "mode": ("modes",),
        "workflow": ("workflows", "evidence", "outputs", "artifacts"),
        "change_class": ("workflows",),
        "estados_permitidos": ("statuses",),
        "requested_skills": ("skills",),
    }

    def kernel_path(family: str) -> str:
        filename = surface.kernel_files[family][0]
        return f"{surface.root_name}/kernel/{filename}"

    projected_metadata: dict[str, list[str]] = {}
    for field in projected:
        families = kernel_sources.get(field, ())
        if families:
            projected_metadata[f"resuelto.{field}"] = [
                kernel_path(family) for family in families
            ]

    return {
        "provenance_reason": provenance_reason,
        "tool_internal_sources": [
            kernel_path(family) for family in surface.kernel_files
        ],
        "resolver_projected_metadata": projected_metadata,
        "resolved_templates": [
            {
                "artifact": artifact["key"],
                "output": artifact["output_key"],
                "source": artifact["required_template"],
            }
            for artifact in resolved["workflow"]["artefactos"]
        ],
        "requested_skills": [
            {
                "key": skill["key"],
                "source": skill["required_skill"],
            }
            for skill in resolved.get("requested_skills", [])
        ],
        "model_context_observation": "executor_report_required",
    }


def resolver(
    actor: str | None,
    mode: str | None = None,
    workflow: str | None = None,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
    hydration_level: str | DensityLevel | None = None,
    compact: str | DensityLevel | None = None,
    change_class: str | None = None,
    context_provenance: str | None = None,
) -> dict[str, Any]:
    """Resolve an allowed kernel, defaulting to compact Spanish guidance.

    The complete selected contract is built first and then projected into one
    hydration level, which always defaults to compact and only changes through
    an explicit override. A declared ``change_class`` must be coherent with the
    selected workflow; it selects the proportional gates and the report density,
    never the hydration level. ``context_provenance`` is the only way to obtain
    ``context_plan``: a normal resolution never carries it, at any hydration
    level. Neither the level, the density, the class, the provenance request,
    nor this result grants authority.
    """
    surface, directory = select_surface(kernel_dir)
    selected_hydration_level, hydration_errors = _parse_hydration_level(
        hydration_level, compact
    )
    selected_surface = surface or DEFAULT_SURFACE
    if hydration_errors:
        return _fail_closed(hydration_errors, selected_surface)
    assert selected_hydration_level is not None
    if surface is None:
        return _fail_closed(
            [f"{DEFAULT_SURFACE.messages['invalid_kernel_dir']}: {directory}"],
            DEFAULT_SURFACE,
            selected_hydration_level,
        )
    if not directory.is_dir():
        return _fail_closed(
            [f"{surface.messages['missing_kernel_dir']}: {directory}"],
            surface,
            selected_hydration_level,
        )
    data, errors = _load(directory, surface)
    if errors:
        return _fail_closed(errors, surface, selected_hydration_level)

    # The receipt contract owns the allowed reasons, so an unknown one fails
    # closed instead of silently downgrading to a normal resolution.
    allowed_reasons = data["context_receipt_contract"].get("detailed_provenance_reasons", [])
    if context_provenance is not None and context_provenance not in allowed_reasons:
        return _fail_closed(
            [
                f"{surface.messages['unknown_provenance_reason']}: {context_provenance!r} "
                f"({surface.messages['known']}: {sorted(allowed_reasons)})"
            ],
            surface,
            selected_hydration_level,
        )

    manifests = data["manifest"]
    if len(manifests) != 1:
        message = (
            f"the kernel must have exactly one active manifest; found {len(manifests)}"
            if surface.language == "en"
            else f"el kernel debe tener exactamente un manifest activo; hay {len(manifests)}"
        )
        return _fail_closed([message], surface, selected_hydration_level)
    manifest = manifests[0]
    rules = sorted(
        (rule for rule in data["operational_rules"] if rule.get("manifest_key") == manifest.get("key")),
        key=lambda rule: rule.get("priority", 0),
    )
    if not rules:
        message = (
            f"no active operational_rules for {manifest.get('key')}"
            if surface.language == "en"
            else f"sin operational_rules activas para {manifest.get('key')}"
        )
        return _fail_closed([message], surface, selected_hydration_level)

    actors = _index(data["actors"])
    modes = _index(data["modes"])
    workflows = _index(data["workflows"])
    actor_entry = actors.get(actor or "")
    mode_key = mode or MODE_FALLBACK
    mode_entry = modes.get(mode_key)
    workflow_entry = workflows.get(workflow or "")
    if actor_entry is None:
        errors.append(f"{surface.messages['unknown_actor']}: {actor!r} ({surface.messages['known']}: {sorted(actors)})")
    if mode_entry is None:
        errors.append(f"{surface.messages['unknown_mode']}: {mode_key!r} ({surface.messages['known']}: {sorted(modes)})")
    if workflow_entry is None:
        errors.append(f"{surface.messages['unknown_workflow']}: {workflow!r} ({surface.messages['known']}: {sorted(workflows)})")
    if errors:
        return _fail_closed(errors, surface, selected_hydration_level)
    assert actor_entry is not None and mode_entry is not None and workflow_entry is not None
    if mode_key not in actor_entry.get("allowed_modes", []):
        message = (
            f"{surface.messages['incompatible_mode']}: {mode_key!r} is not in "
            f"allowed_modes for {actor_entry['key']!r}"
            if surface.language == "en"
            else f"mode incompatible: {mode_key!r} no esta en allowed_modes de {actor_entry['key']!r}"
        )
        return _fail_closed([message], surface, selected_hydration_level)

    selected_class, class_errors = _resolve_change_class(
        change_class, data["proportionality_contract"], workflow_entry["key"], surface
    )
    if class_errors:
        return _fail_closed(class_errors, surface, selected_hydration_level)

    evidence_index = _index(data["evidence"])
    evidence = _hydrate(
        workflow_entry.get("required_evidence", []),
        evidence_index,
        "evidence",
        surface,
        errors,
    )
    minimum_evidence = _hydrate(
        workflow_entry.get("minimum_evidence", []),
        evidence_index,
        "minimum evidence",
        surface,
        errors,
    )
    outputs = _hydrate(
        workflow_entry.get("allowed_outputs", []),
        _index(data["outputs"]),
        "output",
        surface,
        errors,
    )
    artifacts = _resolve_artifacts(workflow_entry, outputs, data["artifacts"], directory, surface, errors)
    requested = [skill] if isinstance(skill, str) else list(skill or [])
    requested_skills = _resolve_skills(requested, _index(data["skills"]), directory, surface, errors)
    if errors:
        return _fail_closed(errors, surface, selected_hydration_level)

    # A resolution mutates only when a write-capable mode meets a workflow that
    # can emit a mutable output; the read-only mode never mutates, so the same
    # workflow (e.g. target_adoption) may draft read-only without a class. Every
    # actual mutation must declare a change class (no silent omission).
    mutable_output = any(
        item.get("action_class") == "action.mutable" for item in outputs.values()
    )
    mutating = mutable_output and mode_key != MODE_FALLBACK
    if mutating and selected_class is None:
        return _fail_closed(
            [f"{surface.messages['change_class_required_for_mutation']}: {workflow_entry['key']} + {mode_key}"],
            surface,
            selected_hydration_level,
        )

    # The class owns the report density and the material gates; it never selects
    # how much contract the agent receives, so a critical unit resolves at the
    # compact default while keeping its detailed report and every gate.
    report_density = DEFAULT_REPORT_DENSITY
    remaining_gates: list[dict[str, Any]] | None = None
    if selected_class is not None:
        try:
            report_density = DensityLevel(selected_class.get("output_density"))
        except ValueError:
            return _fail_closed(
                [f"{surface.messages['unknown_change_class']}: {change_class!r} output_density"],
                surface,
                selected_hydration_level,
            )
        remaining_gates = _remaining_gates(selected_class)

    statuses = _index(data["statuses"])
    status_refs = [limit.get("on_violation") for limit in data["limits"] if limit.get("actor_key") in (None, actor_entry["key"])]
    status_refs += [item.get("missing_status") for item in evidence.values()]
    status_refs += [item.get("status_key") for item in outputs.values()]
    status_refs.append(data["safe_degradation_contract"].get("status_key"))
    selected_statuses: list[dict[str, Any]] = []
    for status_key in dict.fromkeys(ref for ref in status_refs if ref):
        status = statuses.get(status_key)
        if status is None:
            errors.append(
                f"{'referenced status not found' if surface.language == 'en' else 'status referenciado no encontrado'}: {status_key}"
            )
        else:
            selected_statuses.append(_fields(status, "key", "meaning", "type", "active"))
    if errors:
        return _fail_closed(errors, surface, selected_hydration_level)

    resolved: dict[str, Any] = {
        "manifest": {
            **_fields(manifest, "key", "version", "language"),
            "objetivo": manifest.get("objetivo", manifest.get("objective")),
            **_fields(manifest, "resolution_sequence", "active"),
        },
        "reglas_operativas": [_fields(rule, "key", "manifest_key", "resolution_sequence", "on_violation", "priority", "active") for rule in rules],
        "actor": _fields(actor_entry, "key", "surface", "context", "allowed_modes", "active"),
        "limites": [_fields(limit, "key", "actor_key", "rule", "on_violation", "blocking", "active") for limit in data["limits"] if limit.get("actor_key") in (None, actor_entry["key"])],
        "mode": _fields(mode_entry, "key", "allowed_actions", "prohibited_actions", "fallback", "active"),
        "workflow": {
            **_fields(workflow_entry, "key", "use_for", "required_behavior", "active"),
            "materiality_contract": data["materiality_contract"],
            "proportionality_contract": data["proportionality_contract"],
            "safe_degradation_contract": data["safe_degradation_contract"],
            "context_receipt_contract": data["context_receipt_contract"],
            "required_evidence": [
                _fields(
                    item,
                    "key",
                    "satisfied_by",
                    "missing_status",
                    "required",
                    "materiality",
                    "hard_gate",
                    "source",
                    "revalidation_required_before_write",
                    "active",
                )
                for item in evidence.values()
            ],
            "minimum_evidence": [
                _fields(
                    item,
                    "key",
                    "satisfied_by",
                    "missing_status",
                    "required",
                    "materiality",
                    "hard_gate",
                    "source",
                    "revalidation_required_before_write",
                    "active",
                )
                for item in minimum_evidence.values()
            ],
            "allowed_outputs": [
                {
                    **_fields(
                        item,
                        "key",
                        "use_for",
                        "status_key",
                        "action_class",
                        "allows_non_material_gaps",
                        "safe_degradation_key",
                        "context_receipt_key",
                    ),
                    "must_include": _projected_must_include(item, report_density),
                    "active": item.get("active"),
                }
                for item in outputs.values()
            ],
            "artefactos": artifacts,
        },
        "estados_permitidos": selected_statuses,
    }
    if selected_class is not None:
        resolved["change_class"] = {
            "contract_key": data["proportionality_contract"].get("key"),
            **selected_class,
            "remaining_gates": remaining_gates,
        }
    if requested_skills:
        resolved["requested_skills"] = requested_skills
    projected = _project_resolution(resolved, selected_hydration_level)
    result: dict[str, Any] = {
        "estado": "status.resolved",
        "hydration_level": selected_hydration_level.value,
        "resuelto": projected,
        "autorizacion": surface.authorization_notice,
        "errores": [],
    }
    if context_provenance is not None:
        result["context_plan"] = _context_plan(
            resolved, projected, context_provenance, surface
        )
    return result


def resolve(
    actor_id: str,
    workflow_id: str,
    mode_id: str,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
    hydration_level: str | DensityLevel | None = None,
    compact: str | DensityLevel | None = None,
    change_class: str | None = None,
    context_provenance: str | None = None,
) -> dict[str, Any]:
    """Compatibility import; Spanish remains the default surface."""
    return resolver(
        actor_id,
        mode_id,
        workflow_id,
        kernel_dir=kernel_dir,
        skill=skill,
        hydration_level=hydration_level,
        compact=compact,
        change_class=change_class,
        context_provenance=context_provenance,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Principal deterministic resolver for project-os-es (default) or explicit project-os-en; output never grants permission."
    )
    parser.add_argument("--actor", required=True, help="e.g. actor.terminal_agent")
    parser.add_argument("--workflow", required=True, help="e.g. workflow.issue_implementation")
    parser.add_argument("--mode", default=None, help="e.g. mode.delegated_commit_pr; omitted falls back to mode.review_only")
    parser.add_argument("--kernel-dir", default=None, help="kernel directory (default: ./project-os-es/kernel)")
    parser.add_argument("--skill", action="append", default=None, help="optional skill selector; repeatable")
    parser.add_argument(
        "--change-class",
        default=None,
        metavar="CLASS",
        help=(
            "declared change class, e.g. change_class.small; must be coherent "
            "with the workflow and selects the proportional gates and the "
            "report density, never the hydration level"
        ),
    )
    parser.add_argument(
        "--hydration-level",
        default=None,
        metavar="LEVEL",
        help=(
            "minimal, compact (default for every class), or full/debug for "
            "auditing or debugging the resolver; changes returned guidance only"
        ),
    )
    parser.add_argument(
        "--context-provenance",
        default=None,
        metavar="REASON",
        help=(
            "explicitly request detailed resolver provenance (context_plan) for one "
            "allowed reason: audit, debugging, security_or_authorization_review, or "
            "incorrect_resolution_investigation; omitted, no provenance is returned"
        ),
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="omit JSON indentation; legacy formatting flag, not a hydration selector",
    )
    args = parser.parse_args(argv)
    try:
        result = resolver(
            args.actor,
            args.mode,
            args.workflow,
            args.kernel_dir,
            args.skill,
            hydration_level=args.hydration_level,
            change_class=args.change_class,
            context_provenance=args.context_provenance,
        )
    except Exception as exc:
        surface, _ = select_surface(args.kernel_dir)
        selected = surface or DEFAULT_SURFACE
        result = _fail_closed([f"{selected.messages['unexpected_error']}: {exc}"], selected)
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=None if args.compact else 2, ensure_ascii=False))
    return 0 if result["estado"] == "status.resolved" else 1


if __name__ == "__main__":
    raise SystemExit(main())
