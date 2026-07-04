"""Resolver de la superficie Project OS en espanol.

Hidrata el contrato JSON del kernel en espanol (project-os-es/kernel/) por
(actor, mode, workflow) a partir del manifest activo.
Evidence, salidas y artefactos hidratan desde el workflow resuelto
(required_evidence, allowed_outputs); los skills se exponen solo cuando se
solicitan explicitamente. El mode gobierna unicamente acciones
permitidas/prohibidas, fallback y compatibilidad con el actor, y mode_key en
evidencia/salidas no selecciona registros. Lee el kernel JSON en runtime y no
duplica data del kernel; no lee estado vivo de GitHub/git y no muta archivos
ni target alguno.

El resolver devuelve exactamente el contrato JSON operativo del (actor, mode,
workflow) resuelto: top-level estado, resuelto, autorizacion, errores;
resuelto expone manifest, reglas_operativas, actor, limites, mode, workflow y
estados_permitidos. Los campos required_evidence y allowed_outputs del
workflow llevan el contenido hidratado, no ids crudos, y ningun registro
expone workflow_key ni mode_key. Los artefactos exponen referencias de template
(`required_template`) y nunca contenido de templates. Los skills solicitados
exponen referencias de habilidad (`required_skill`) y nunca contenido markdown;
viven fuera de workflow como `requested_skills`, separados de artefactos y
templates.

El output hidratado es guia operativa y nunca concede permisos
(rule.no_autorizacion, boundary.output_not_permission). Toda falla resuelve
cerrada con el mismo contrato top-level y estado status.blocked
(rule.resolucion_fail_closed).

Importable como funcion o ejecutable como comando desde cualquier cwd:

    python /ruta/a/project-os-es/tools/resolver.py \
        --actor actor.browser_chat --mode mode.review_only \
        --workflow workflow.review_only [--kernel-dir DIR] [--skill skill.id]

Exit codes: 0 = status.resolved, 1 = fail-closed estructurado, 2 = error de
tooling inesperado.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_KERNEL_DIR_DEFAULT = Path(__file__).resolve().parent.parent / "kernel"

# alias -> (archivo, lista raiz dentro del JSON)
_ARCHIVOS_KERNEL = {
    "manifest": ("manifest.json", "manifest"),
    "reglas": ("reglas-operativas.json", "operational_rules"),
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

MODE_FALLBACK = "mode.review_only"

AUTORIZACION = (
    "La autorización de acciones depende de el modo de ejecución recibido; "
    "esta resolución no concede permisos por sí sola."
)

_CLAVES_MANIFEST = (
    "key", "version", "language", "objetivo", "resolution_sequence", "active",
)
_CLAVES_REGLA = (
    "key", "manifest_key", "resolution_sequence", "on_violation", "priority", "active",
)
_CLAVES_ACTOR = ("key", "surface", "context", "allowed_modes", "active")
_CLAVES_LIMITE = ("key", "actor_key", "rule", "on_violation", "blocking", "active")
_CLAVES_MODE = ("key", "allowed_actions", "prohibited_actions", "fallback", "active")
_CLAVES_EVIDENCIA = ("key", "satisfied_by", "missing_status", "required", "active")
_CLAVES_SALIDA = ("key", "use_for", "status_key", "must_include", "active")
_CLAVES_ARTEFACTO = (
    "key", "output_key", "responsabilidad", "required_template", "active",
)
_CLAVES_SKILL = (
    "key", "nombre", "responsabilidad", "required_skill", "use_for",
    "non_authorization", "active",
)
_CLAVES_ESTADO = ("key", "meaning", "type", "active")


def _campos(registro: dict[str, Any], claves: tuple[str, ...]) -> dict[str, Any]:
    """Selecciona del registro del kernel exactamente las claves dadas."""
    return {clave: registro.get(clave) for clave in claves}


def _workflow_resuelto(
    workflow: dict[str, Any],
    evidencia: dict[str, dict[str, Any]],
    salidas: dict[str, dict[str, Any]],
    artefactos: list[dict[str, Any]],
) -> dict[str, Any]:
    """Workflow del contrato con los campos required_evidence y
    allowed_outputs hidratados (contenido, no ids), mas artefactos
    operativamente relevantes por template reference, sin workflow_key ni
    mode_key."""
    resuelto = _campos(workflow, ("key", "use_for", "required_behavior"))
    resuelto["required_evidence"] = [
        _campos(evidencia[key], _CLAVES_EVIDENCIA)
        for key in workflow.get("required_evidence", [])
    ]
    resuelto["allowed_outputs"] = [
        _campos(salidas[key], _CLAVES_SALIDA)
        for key in workflow.get("allowed_outputs", [])
    ]
    resuelto["artefactos"] = [
        _campos(artefacto, _CLAVES_ARTEFACTO) for artefacto in artefactos
    ]
    resuelto["active"] = workflow.get("active")
    return resuelto


def _fail_closed(errores: list[str]) -> dict[str, Any]:
    return {
        "estado": "status.blocked",
        "resuelto": None,
        "autorizacion": AUTORIZACION,
        "errores": errores,
    }


def _cargar_kernel(kernel_dir: Path) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    """Carga los archivos del kernel es; solo registros dict con active true."""
    data: dict[str, list[dict[str, Any]]] = {}
    errores: list[str] = []
    for alias, (nombre, familia) in _ARCHIVOS_KERNEL.items():
        ruta = kernel_dir / nombre
        if not ruta.is_file():
            errores.append(f"archivo del kernel faltante: {ruta}")
            continue
        try:
            contenido = json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errores.append(f"archivo del kernel ilegible o invalido: {nombre}: {exc}")
            continue
        registros = contenido.get(familia) if isinstance(contenido, dict) else None
        if not isinstance(registros, list):
            errores.append(f"{nombre} no contiene la lista '{familia}'")
            continue
        data[alias] = [r for r in registros if isinstance(r, dict) and r.get("active")]
    return data, errores


def _indexar(registros: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {r["key"]: r for r in registros if isinstance(r.get("key"), str)}


def _hidratar_nombrados(
    nombrados: list[str],
    indice: dict[str, dict[str, Any]],
    error_no_encontrado: str,
    faltantes: list[str],
) -> dict[str, dict[str, Any]]:
    """Hidrata los registros nombrados por el workflow; falla cerrado si faltan."""
    hidratados: dict[str, dict[str, Any]] = {}
    for key in nombrados:
        registro = indice.get(key)
        if registro is None:
            faltantes.append(f"{error_no_encontrado}: {key}")
        else:
            hidratados[key] = registro
    return hidratados


def _template_existe(required_template: str, kernel_dir: Path) -> bool:
    """Valida referencias .md sin leer ni incrustar el contenido del template."""
    candidates = [
        kernel_dir.parent / required_template,
        kernel_dir.parent.parent / required_template,
    ]
    return any(candidate.is_file() for candidate in candidates)


def _skill_file_existe(required_skill: str, kernel_dir: Path) -> bool:
    """Valida referencias .md bajo project-os-es/habilidades/ sin leer contenido."""
    ruta = Path(required_skill)
    if ruta.is_absolute() or ruta.parts[:2] != ("project-os-es", "habilidades"):
        return False
    if len(ruta.parts) != 3 or ruta.suffix != ".md":
        return False
    return (kernel_dir.parent.parent / ruta).is_file()


def _artefactos_resueltos(
    workflow: dict[str, Any],
    salidas: dict[str, dict[str, Any]],
    artefactos: list[dict[str, Any]],
    kernel_dir: Path,
    faltantes: list[str],
) -> list[dict[str, Any]]:
    """Selecciona artefactos por workflow/output y valida required_template."""
    workflow_key = workflow.get("key")
    output_keys = set(salidas)
    resueltos: list[dict[str, Any]] = []
    for artefacto in artefactos:
        workflows = artefacto.get("workflow_key", [])
        output_key = artefacto.get("output_key")
        if workflow_key not in workflows:
            continue
        if output_key is not None and output_key not in output_keys:
            continue
        required_template = artefacto.get("required_template")
        if not isinstance(required_template, str) or not required_template.endswith(".md"):
            faltantes.append(
                f"artefacto sin required_template .md valido: {artefacto.get('key')}"
            )
            continue
        if not _template_existe(required_template, kernel_dir):
            faltantes.append(
                f"template requerido por artefacto no encontrado: "
                f"{artefacto.get('key')}: {required_template}"
            )
            continue
        resueltos.append(artefacto)
    return resueltos


def _skill_keys_solicitadas(
    skill: str | list[str] | tuple[str, ...] | None,
) -> list[str]:
    if skill is None:
        return []
    if isinstance(skill, str):
        return [skill]
    return list(skill)


def _skills_solicitados(
    skill_keys: list[str],
    skills: dict[str, dict[str, Any]],
    kernel_dir: Path,
    faltantes: list[str],
) -> list[dict[str, Any]]:
    """Hidrata skills pedidos explicitamente y valida su referencia compacta."""
    resueltos: list[dict[str, Any]] = []
    vistos: set[str] = set()
    for key in skill_keys:
        if key in vistos:
            continue
        vistos.add(key)
        registro = skills.get(key)
        if registro is None:
            faltantes.append(f"skill desconocido: {key!r} (conocidos: {sorted(skills)})")
            continue
        required_skill = registro.get("required_skill")
        if not isinstance(required_skill, str) or not required_skill.endswith(".md"):
            faltantes.append(f"skill sin required_skill .md valido: {key}")
            continue
        if not _skill_file_existe(required_skill, kernel_dir):
            faltantes.append(
                f"skill requerido no encontrado o fuera de project-os-es/habilidades: "
                f"{key}: {required_skill}"
            )
            continue
        resueltos.append(_campos(registro, _CLAVES_SKILL))
    return resueltos


def resolver(
    actor: str | None,
    mode: str | None = None,
    workflow: str | None = None,
    kernel_dir: Path | str | None = None,
    skill: str | list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Resuelve (actor, mode, workflow) contra el kernel es en runtime.

    Devuelve siempre un dict estructurado: estado status.resolved con el
    contrato hidratado y la guia operativa, o fail-closed con estado
    status.blocked y errores explicitos. Mode faltante cae a
    mode.review_only; mode invalido nunca cae, falla cerrado. Skill faltante no
    cambia el output; skill desconocido falla cerrado.
    """
    dir_kernel = Path(kernel_dir) if kernel_dir is not None else _KERNEL_DIR_DEFAULT
    if not dir_kernel.is_dir():
        return _fail_closed([f"directorio del kernel no encontrado: {dir_kernel}"])

    data, errores = _cargar_kernel(dir_kernel)
    if errores:
        return _fail_closed(errores)

    manifests = data["manifest"]
    if len(manifests) != 1:
        return _fail_closed(
            [f"el kernel debe tener exactamente un manifest activo; hay {len(manifests)}"]
        )
    manifest = manifests[0]

    reglas = sorted(
        (r for r in data["reglas"] if r.get("manifest_key") == manifest.get("key")),
        key=lambda r: r.get("priority", 0),
    )
    if not reglas:
        return _fail_closed(
            [f"sin operational_rules activas para {manifest.get('key')}"]
        )

    actores = _indexar(data["actores"])
    registro_actor = actores.get(actor or "")
    if registro_actor is None:
        return _fail_closed(
            [f"actor desconocido: {actor!r} (conocidos: {sorted(actores)})"]
        )

    # Limits aplicables antes de mode y workflow: globales mas los del actor.
    limites = [
        registro
        for registro in data["limites"]
        if registro.get("actor_key") in (None, registro_actor["key"])
    ]

    mode_efectivo = mode if mode else MODE_FALLBACK
    modos = _indexar(data["modos"])
    registro_mode = modos.get(mode_efectivo)
    if registro_mode is None:
        return _fail_closed(
            [f"mode desconocido: {mode_efectivo!r} (conocidos: {sorted(modos)})"]
        )

    allowed_modes = registro_actor.get("allowed_modes", [])
    if mode_efectivo not in allowed_modes:
        return _fail_closed(
            [
                f"mode incompatible: {mode_efectivo!r} no esta en allowed_modes "
                f"de {registro_actor['key']!r} (permitidos: {allowed_modes})"
            ]
        )

    workflows = _indexar(data["workflows"])
    registro_workflow = workflows.get(workflow or "")
    if registro_workflow is None:
        return _fail_closed(
            [f"workflow desconocido: {workflow!r} (conocidos: {sorted(workflows)})"]
        )

    # Decision PM (PR #399): evidence y salidas hidratan solo desde las
    # referencias del workflow resuelto; mode_key en estos registros no
    # selecciona ni excluye nada y el kernel es lo mantiene vacio.
    faltantes: list[str] = []

    evidencia = _hidratar_nombrados(
        registro_workflow.get("required_evidence", []),
        _indexar(data["evidencia"]),
        "evidence requerida por el workflow no encontrada",
        faltantes,
    )
    salidas = _hidratar_nombrados(
        registro_workflow.get("allowed_outputs", []),
        _indexar(data["salidas"]),
        "output permitido por el workflow no encontrado",
        faltantes,
    )

    artefactos = _artefactos_resueltos(
        registro_workflow, salidas, data["artefactos"], dir_kernel, faltantes
    )
    requested_skills = _skills_solicitados(
        _skill_keys_solicitadas(skill), _indexar(data["skills"]), dir_kernel, faltantes
    )

    if faltantes:
        return _fail_closed(faltantes)

    # Statuses referenciados por limits, evidence y output.
    estados_idx = _indexar(data["estados"])
    referencias_estado = (
        [registro.get("on_violation") for registro in limites]
        + [registro.get("missing_status") for registro in evidencia.values()]
        + [registro.get("status_key") for registro in salidas.values()]
    )
    estados: dict[str, dict[str, Any]] = {}
    for key in referencias_estado:
        if not key or key in estados:
            continue
        registro = estados_idx.get(key)
        if registro is None:
            faltantes.append(f"status referenciado no encontrado: {key}")
        else:
            estados[key] = registro
    if faltantes:
        return _fail_closed(faltantes)

    resuelto: dict[str, Any] = {
        "manifest": _campos(manifest, _CLAVES_MANIFEST),
        "reglas_operativas": [_campos(regla, _CLAVES_REGLA) for regla in reglas],
        "actor": _campos(registro_actor, _CLAVES_ACTOR),
        "limites": [_campos(limite, _CLAVES_LIMITE) for limite in limites],
        "mode": _campos(registro_mode, _CLAVES_MODE),
        "workflow": _workflow_resuelto(
            registro_workflow, evidencia, salidas, artefactos
        ),
        "estados_permitidos": [
            _campos(estado, _CLAVES_ESTADO) for estado in estados.values()
        ],
    }
    if requested_skills:
        resuelto["requested_skills"] = requested_skills

    return {
        "estado": "status.resolved",
        "resuelto": resuelto,
        "autorizacion": AUTORIZACION,
        "errores": [],
    }


def main(argv: list[str] | None = None) -> int:
    """Entrypoint ejecutable minimo; imprime el resultado JSON en stdout.

    Exit codes: 0 = status.resolved, 1 = fail-closed estructurado,
    2 = error de tooling inesperado.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Resolver de la superficie Project OS en espanol: hidrata "
            "project-os-es/kernel/ por (actor, mode, workflow) y puede exponer "
            "skills opcionales solicitados. El output es guia operativa y "
            "nunca concede permisos."
        ),
    )
    parser.add_argument("--actor", required=True, help="ej. actor.browser_chat")
    parser.add_argument(
        "--mode",
        default=None,
        help="opcional; si falta cae a mode.review_only",
    )
    parser.add_argument("--workflow", required=True, help="ej. workflow.review_only")
    parser.add_argument(
        "--kernel-dir",
        default=None,
        help="directorio del kernel es (default: kernel/ junto a tools/)",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=None,
        help="skill opcional a exponer; se puede repetir. ej. skill.arquitectura_backend",
    )
    args = parser.parse_args(argv)

    try:
        resultado = resolver(
            args.actor,
            args.mode,
            args.workflow,
            kernel_dir=args.kernel_dir,
            skill=args.skill,
        )
    except Exception as exc:
        error = _fail_closed([f"error de tooling inesperado: {exc}"])
        print(json.dumps(error, indent=2, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    return 0 if resultado.get("estado") == "status.resolved" else 1


if __name__ == "__main__":
    raise SystemExit(main())
