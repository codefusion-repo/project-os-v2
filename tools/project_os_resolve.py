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


class HydrationLevel(str, Enum):
    """Safe internal names for the public hydration-level values."""

    MINIMAL = "minimal"
    COMPACT = "compact"
    FULL_DEBUG = "full/debug"


DEFAULT_HYDRATION_LEVEL = HydrationLevel.COMPACT
HYDRATION_LEVEL_VALUES = tuple(level.value for level in HydrationLevel)


def _fail_closed(
    errors: list[str],
    surface: ProjectOSSurface = DEFAULT_SURFACE,
    hydration_level: HydrationLevel | None = None,
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
    hydration_level: str | HydrationLevel | None,
    compact: str | HydrationLevel | None,
) -> tuple[HydrationLevel | None, list[str]]:
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
        return HydrationLevel(value), []
    except (TypeError, ValueError):
        return None, [
            "unknown hydration level; expected exactly one of: "
            + ", ".join(HYDRATION_LEVEL_VALUES)
        ]


def _load(
    kernel_dir: Path, surface: ProjectOSSurface
) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    data: dict[str, list[dict[str, Any]]] = {}
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
    return data, errors


def _index(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {entry["key"]: entry for entry in entries if isinstance(entry.get("key"), str)}


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
        _fields(item, "key", "satisfied_by", "missing_status", "required")
        for item in evidence
    ]


def _allowed_outputs(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep allowed-output constraints rather than only their identifiers."""

    return [
        _fields(item, "key", "use_for", "status_key", "must_include")
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
            "required_evidence": _required_evidence(workflow["required_evidence"]),
            "allowed_outputs": _allowed_outputs(workflow["allowed_outputs"]),
        },
        "estados_permitidos": _referenced_statuses(resolved["estados_permitidos"]),
    }
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
            "required_evidence": _required_evidence(workflow["required_evidence"]),
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
    if "requested_skills" in resolved:
        projected["requested_skills"] = _compact_requested_skills(resolved["requested_skills"])
    return projected


def _project_resolution(
    resolved: dict[str, Any], hydration_level: HydrationLevel
) -> dict[str, Any]:
    """Apply one explicit view after resolving the complete internal contract."""

    if hydration_level is HydrationLevel.MINIMAL:
        return _minimal_resolution(resolved)
    if hydration_level is HydrationLevel.COMPACT:
        return _compact_resolution(resolved)
    return resolved


def resolver(
    actor: str | None,
    mode: str | None = None,
    workflow: str | None = None,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
    hydration_level: str | HydrationLevel | None = None,
    compact: str | HydrationLevel | None = None,
) -> dict[str, Any]:
    """Resolve an allowed kernel, defaulting to compact Spanish guidance.

    The complete selected contract is built first and then projected into one
    hydration level. Neither the level nor this result grants authority.
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

    evidence = _hydrate(
        workflow_entry.get("required_evidence", []),
        _index(data["evidence"]),
        "evidence",
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

    statuses = _index(data["statuses"])
    status_refs = [limit.get("on_violation") for limit in data["limits"] if limit.get("actor_key") in (None, actor_entry["key"])]
    status_refs += [item.get("missing_status") for item in evidence.values()]
    status_refs += [item.get("status_key") for item in outputs.values()]
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
            "required_evidence": [_fields(item, "key", "satisfied_by", "missing_status", "required", "active") for item in evidence.values()],
            "allowed_outputs": [_fields(item, "key", "use_for", "status_key", "must_include", "active") for item in outputs.values()],
            "artefactos": artifacts,
        },
        "estados_permitidos": selected_statuses,
    }
    if requested_skills:
        resolved["requested_skills"] = requested_skills
    return {
        "estado": "status.resolved",
        "hydration_level": selected_hydration_level.value,
        "resuelto": _project_resolution(resolved, selected_hydration_level),
        "autorizacion": surface.authorization_notice,
        "errores": [],
    }


def resolve(
    actor_id: str,
    workflow_id: str,
    mode_id: str,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
    hydration_level: str | HydrationLevel | None = None,
    compact: str | HydrationLevel | None = None,
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
        "--hydration-level",
        default=None,
        metavar="LEVEL",
        help="minimal, compact (default), or full/debug; changes returned guidance only",
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
