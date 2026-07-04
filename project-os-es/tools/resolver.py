"""Resolver de la superficie Project OS en espanol.

Hidrata el contrato JSON del kernel en espanol (project-os-es/kernel/) por
(actor, mode, workflow) siguiendo la resolution_sequence del manifest activo.
Por decision PM (PR #399), evidence y salidas hidratan solo desde las
referencias del workflow resuelto (required_evidence, allowed_outputs); el
mode gobierna unicamente acciones permitidas/prohibidas, fallback y
compatibilidad con el actor, y mode_key en evidencia/salidas no selecciona
registros. Lee el kernel JSON en runtime y no duplica data del kernel; no
lee estado vivo de GitHub/git y no muta archivos ni target alguno.

El output publico (PR #399, correccion QA) expone top-level exactamente
estado, resuelto, autorizacion y errores; resuelto expone exactamente
manifest, reglas_operativas, actor, limites, mode, workflow y
estados_permitidos. workflow.required_evidence y workflow.allowed_outputs
llevan el contenido hidratado (no ids crudos) y ningun registro publico
expone workflow_key ni mode_key. Los registros crudos del kernel se
proyectan a este subconjunto publico mediante un shaping helper privado;
internamente el resolver sigue usando los registros crudos.

El output hidratado es guia operativa y nunca concede permisos
(rule.no_autorizacion, boundary.output_not_permission). Toda falla resuelve
cerrada con output estructurado (rule.resolucion_fail_closed).

Importable como funcion o ejecutable como comando desde cualquier cwd:

    python /ruta/a/project-os-es/tools/resolver.py \
        --actor actor.browser_chat --mode mode.review_only \
        --workflow workflow.review_only [--kernel-dir DIR]

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
    "estados": ("estados.json", "statuses"),
}

MODE_FALLBACK = "mode.review_only"

AUTORIZACION = (
    "La autorización de acciones depende de el modo de ejecución recibido; "
    "esta resolución no concede permisos por sí sola."
)

# Reglas de diseno interno del resolver (emision, hidratacion): guian la
# implementacion pero no son operativas para el agente que consume la
# resolucion, asi que el shaping publico las excluye de reglas_operativas.
_REGLAS_INTERNAS_EXCLUIDAS = {"rule.emision_resolver", "rule.hidratacion"}

_GUIA_MANIFEST_PUBLICA = [
    "Lee esta resolución",
    "Es tu guía operativa obligatoria",
    "Debes respetar las reglas_operativas obligatoriamente.",
    "Debes respetar los limites obligatorios y el contexto de tu superficie de actuación.",
    "Debes respetar las acciones disponibles y prohibidas de tu modo de ejecución obligatoriamente.",
    "Debes ejecutar exclusivamente el workflow resuelto.",
    "Debes respetar las evidencias y salidas del workflow resuelto obligatoriamente.",
    "Debes respetar los estados resueltos obligatoriamente.",
]

_CLAVES_REGLA = (
    "key", "manifest_key", "resolution_sequence", "on_violation", "priority", "active",
)
_CLAVES_ACTOR = ("key", "surface", "context", "allowed_modes", "active")
_CLAVES_LIMITE = ("key", "actor_key", "rule", "on_violation", "blocking", "active")
_CLAVES_MODE = ("key", "allowed_actions", "prohibited_actions", "fallback", "active")
_CLAVES_EVIDENCIA = ("key", "satisfied_by", "missing_status", "required", "active")
_CLAVES_SALIDA = ("key", "use_for", "status_key", "must_include", "active")
_CLAVES_ESTADO = ("key", "meaning", "type", "active")


def _campos_publicos(registro: dict[str, Any], claves: tuple[str, ...]) -> dict[str, Any]:
    """Proyecta un registro crudo del kernel a su subconjunto publico exacto."""
    return {clave: registro.get(clave) for clave in claves}


def _manifest_publico(manifest: dict[str, Any]) -> dict[str, Any]:
    """Manifest publico: campos del kernel mas guia operativa fija (no la
    resolution_sequence interna del loader)."""
    publico = {
        clave: manifest.get(clave) for clave in ("key", "version", "language", "objetivo")
    }
    publico["resolution_sequence"] = list(_GUIA_MANIFEST_PUBLICA)
    publico["active"] = manifest.get("active")
    return publico


def _workflow_publico(
    workflow: dict[str, Any],
    evidencia: dict[str, dict[str, Any]],
    salidas: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Workflow publico con required_evidence/allowed_outputs hidratados
    (contenido, no ids), sin workflow_key ni mode_key."""
    publico = _campos_publicos(workflow, ("key", "use_for", "required_behavior"))
    publico["required_evidence"] = [
        _campos_publicos(evidencia[key], _CLAVES_EVIDENCIA)
        for key in workflow.get("required_evidence", [])
    ]
    publico["allowed_outputs"] = [
        _campos_publicos(salidas[key], _CLAVES_SALIDA)
        for key in workflow.get("allowed_outputs", [])
    ]
    publico["active"] = workflow.get("active")
    return publico


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


def resolver(
    actor: str | None,
    mode: str | None = None,
    workflow: str | None = None,
    kernel_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Resuelve (actor, mode, workflow) contra el kernel es en runtime.

    Devuelve siempre un dict estructurado: estado status.resolved con el
    contrato hidratado y la guia operativa, o fail-closed con estado
    status.blocked y errores explicitos. Mode faltante cae a
    mode.review_only; mode invalido nunca cae, falla cerrado.
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

    return {
        "estado": "status.resolved",
        "resuelto": {
            "manifest": _manifest_publico(manifest),
            "reglas_operativas": [
                _campos_publicos(regla, _CLAVES_REGLA)
                for regla in reglas
                if regla.get("key") not in _REGLAS_INTERNAS_EXCLUIDAS
            ],
            "actor": _campos_publicos(registro_actor, _CLAVES_ACTOR),
            "limites": [_campos_publicos(limite, _CLAVES_LIMITE) for limite in limites],
            "mode": _campos_publicos(registro_mode, _CLAVES_MODE),
            "workflow": _workflow_publico(registro_workflow, evidencia, salidas),
            "estados_permitidos": [
                _campos_publicos(estado, _CLAVES_ESTADO) for estado in estados.values()
            ],
        },
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
            "project-os-es/kernel/ por (actor, mode, workflow). El output es "
            "guia operativa y nunca concede permisos."
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
    args = parser.parse_args(argv)

    try:
        resultado = resolver(
            args.actor, args.mode, args.workflow, kernel_dir=args.kernel_dir
        )
    except Exception as exc:
        error = _fail_closed([f"error de tooling inesperado: {exc}"])
        print(json.dumps(error, indent=2, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    return 0 if resultado.get("estado") == "status.resolved" else 1


if __name__ == "__main__":
    raise SystemExit(main())
