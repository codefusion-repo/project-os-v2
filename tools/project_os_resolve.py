"""Principal deterministic resolver for the active Project OS kernel.

The resolver reads ``project-os-es/kernel`` at runtime and hydrates one
``(actor, mode, workflow)`` selection.  It is deliberately a repository tool,
not a multilingual abstraction: the canonical Spanish kernel is the only
repository surface it resolves by default or by explicit ``--kernel-dir``.

The resulting JSON is operative guidance only.  It never reads GitHub or git,
mutates files, grants permission, or replaces exact PM approval and the
kernel-resolved gates.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KERNEL_DIR = REPO_ROOT / "project-os-es" / "kernel"
MODE_FALLBACK = "mode.review_only"
AUTHORIZATION_NOTICE = (
    "Esta resolucion da forma operativa y nunca concede permisos; la autoridad "
    "requiere aprobacion PM exacta y los gates del kernel."
)

KERNEL_FILES = {
    "manifest": ("manifest.json", "manifest"),
    "reglas_operativas": ("reglas-operativas.json", "operational_rules"),
    "actores": ("actores.json", "actors"),
    "modos": ("modos.json", "modes"),
    "workflows": ("workflows.json", "workflows"),
    "limites": ("limites.json", "limits"),
    "evidencia": ("evidencia.json", "evidence"),
    "salidas": ("salidas.json", "outputs"),
    "artefactos": ("artefactos.json", "artefactos"),
    "skills": ("skills.json", "skills"),
    "estados": ("estados.json", "statuses"),
}


def _fail_closed(errors: list[str]) -> dict[str, Any]:
    return {
        "estado": "status.blocked",
        "resuelto": None,
        "autorizacion": AUTHORIZATION_NOTICE,
        "errores": errors,
    }


def _load(kernel_dir: Path) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    data: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []
    for family, (filename, collection) in KERNEL_FILES.items():
        path = kernel_dir / filename
        if not path.is_file():
            errors.append(f"archivo del kernel faltante: {path}")
            continue
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"archivo del kernel ilegible o invalido: {filename}: {exc}")
            continue
        entries = content.get(collection) if isinstance(content, dict) else None
        if not isinstance(entries, list):
            errors.append(f"{filename} no contiene la lista '{collection}'")
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
    keys: list[str], index: dict[str, dict[str, Any]], kind: str, errors: list[str]
) -> dict[str, dict[str, Any]]:
    hydrated: dict[str, dict[str, Any]] = {}
    for key in keys:
        entry = index.get(key)
        if entry is None:
            errors.append(f"{kind} requerida por el workflow no encontrada: {key}")
        else:
            hydrated[key] = entry
    return hydrated


def _resolve_artifacts(
    workflow: dict[str, Any],
    outputs: dict[str, dict[str, Any]],
    artifacts: list[dict[str, Any]],
    kernel_dir: Path,
    errors: list[str],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for artifact in artifacts:
        if workflow["key"] not in artifact.get("workflow_key", []):
            continue
        if artifact.get("output_key") not in (None, *outputs):
            continue
        template = artifact.get("required_template")
        if not _valid_project_path(template, ("project-os-es", "templates"), kernel_dir):
            errors.append(f"template requerido por artefacto no encontrado: {artifact.get('key')}: {template}")
            continue
        resolved.append(
            _fields(artifact, "key", "output_key", "responsabilidad", "required_template", "active")
        )
    return resolved


def _resolve_skills(
    requested: list[str], skills: dict[str, dict[str, Any]], kernel_dir: Path, errors: list[str]
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for key in dict.fromkeys(requested):
        skill = skills.get(key)
        if skill is None:
            errors.append(f"skill desconocido: {key!r} (conocidos: {sorted(skills)})")
            continue
        required_skill = skill.get("required_skill")
        if not _valid_project_path(required_skill, ("project-os-es", "habilidades"), kernel_dir):
            errors.append(f"skill requerido no encontrado: {key}: {required_skill}")
            continue
        resolved.append(
            _fields(skill, "key", "nombre", "responsabilidad", "required_skill", "use_for", "non_authorization", "active")
        )
    return resolved


def resolver(
    actor: str | None,
    mode: str | None = None,
    workflow: str | None = None,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Resolve the active Spanish kernel, failing closed for every bad selector."""
    directory = DEFAULT_KERNEL_DIR if kernel_dir is None else Path(kernel_dir)
    if not directory.is_dir():
        return _fail_closed([f"directorio del kernel no encontrado: {directory}"])
    data, errors = _load(directory)
    if errors:
        return _fail_closed(errors)

    manifests = data["manifest"]
    if len(manifests) != 1:
        return _fail_closed([f"el kernel debe tener exactamente un manifest activo; hay {len(manifests)}"])
    manifest = manifests[0]
    rules = sorted(
        (rule for rule in data["reglas_operativas"] if rule.get("manifest_key") == manifest.get("key")),
        key=lambda rule: rule.get("priority", 0),
    )
    if not rules:
        return _fail_closed([f"sin operational_rules activas para {manifest.get('key')}"])

    actors = _index(data["actores"])
    modes = _index(data["modos"])
    workflows = _index(data["workflows"])
    actor_entry = actors.get(actor or "")
    mode_key = mode or MODE_FALLBACK
    mode_entry = modes.get(mode_key)
    workflow_entry = workflows.get(workflow or "")
    if actor_entry is None:
        errors.append(f"actor desconocido: {actor!r} (conocidos: {sorted(actors)})")
    if mode_entry is None:
        errors.append(f"mode desconocido: {mode_key!r} (conocidos: {sorted(modes)})")
    if workflow_entry is None:
        errors.append(f"workflow desconocido: {workflow!r} (conocidos: {sorted(workflows)})")
    if errors:
        return _fail_closed(errors)
    assert actor_entry is not None and mode_entry is not None and workflow_entry is not None
    if mode_key not in actor_entry.get("allowed_modes", []):
        return _fail_closed([f"mode incompatible: {mode_key!r} no esta en allowed_modes de {actor_entry['key']!r}"])

    evidence = _hydrate(workflow_entry.get("required_evidence", []), _index(data["evidencia"]), "evidence", errors)
    outputs = _hydrate(workflow_entry.get("allowed_outputs", []), _index(data["salidas"]), "output", errors)
    artifacts = _resolve_artifacts(workflow_entry, outputs, data["artefactos"], directory, errors)
    requested = [skill] if isinstance(skill, str) else list(skill or [])
    requested_skills = _resolve_skills(requested, _index(data["skills"]), directory, errors)
    if errors:
        return _fail_closed(errors)

    statuses = _index(data["estados"])
    status_refs = [limit.get("on_violation") for limit in data["limites"] if limit.get("actor_key") in (None, actor_entry["key"])]
    status_refs += [item.get("missing_status") for item in evidence.values()]
    status_refs += [item.get("status_key") for item in outputs.values()]
    selected_statuses: list[dict[str, Any]] = []
    for status_key in dict.fromkeys(ref for ref in status_refs if ref):
        status = statuses.get(status_key)
        if status is None:
            errors.append(f"status referenciado no encontrado: {status_key}")
        else:
            selected_statuses.append(_fields(status, "key", "meaning", "type", "active"))
    if errors:
        return _fail_closed(errors)

    resolved: dict[str, Any] = {
        "manifest": _fields(manifest, "key", "version", "language", "objetivo", "resolution_sequence", "active"),
        "reglas_operativas": [_fields(rule, "key", "manifest_key", "resolution_sequence", "on_violation", "priority", "active") for rule in rules],
        "actor": _fields(actor_entry, "key", "surface", "context", "allowed_modes", "active"),
        "limites": [_fields(limit, "key", "actor_key", "rule", "on_violation", "blocking", "active") for limit in data["limites"] if limit.get("actor_key") in (None, actor_entry["key"])],
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
    return {"estado": "status.resolved", "resuelto": resolved, "autorizacion": AUTHORIZATION_NOTICE, "errores": []}


def resolve(
    actor_id: str,
    workflow_id: str,
    mode_id: str,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Compatibility import for root tools; resolves the active Spanish kernel."""
    return resolver(actor_id, mode_id, workflow_id, kernel_dir=kernel_dir, skill=skill)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Principal deterministic resolver for the active project-os-es kernel; output never grants permission."
    )
    parser.add_argument("--actor", required=True, help="e.g. actor.terminal_agent")
    parser.add_argument("--workflow", required=True, help="e.g. workflow.issue_implementation")
    parser.add_argument("--mode", default=None, help="e.g. mode.delegated_commit_pr; omitted falls back to mode.review_only")
    parser.add_argument("--kernel-dir", default=None, help="kernel directory (default: ./project-os-es/kernel)")
    parser.add_argument("--skill", action="append", default=None, help="optional skill selector; repeatable")
    parser.add_argument("--compact", action="store_true", help="omit JSON indentation")
    args = parser.parse_args(argv)
    try:
        result = resolver(args.actor, args.mode, args.workflow, args.kernel_dir, args.skill)
    except Exception as exc:
        result = _fail_closed([f"error de tooling inesperado: {exc}"])
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=None if args.compact else 2, ensure_ascii=False))
    return 0 if result["estado"] == "status.resolved" else 1


if __name__ == "__main__":
    raise SystemExit(main())
