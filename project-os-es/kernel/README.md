# Kernel Project OS — superficie compacta en español

Esta carpeta es una superficie PM/agent-readable en español para entender el
kernel actual de Project OS. No reemplaza `kernel/*.json`, no es runtime y no
autoriza acciones.

Fuente canonica:

- Comportamiento estable: `kernel/*.json`.
- Resolucion terminal: `tools/project_os_resolve.py`.
- Trazabilidad viva: `docs/TRACEABILITY_PROTOCOL.md`.
- Validacion proporcional: `docs/VALIDATION_POLICY.md`.
- Economia de contexto: `docs/CONTEXT_ECONOMY.md`.
- Capas y ownership: `docs/decisions/0002-pre-377-validation-fastpath-audit.md`.
- Operaciones compactas: `project-os-es/operaciones/`.

## Contrato de uso

1. Resuelve primero `kernel/manifest.json`. En terminal, usa el fast path del
   resolver cuando exista checkout local.
2. Trata esta carpeta como espejo compacto en español, no como fuente de verdad
   ejecutable.
3. Lee estado vivo desde GitHub/git al momento de trabajar. Nunca lo guardes en
   archivos durables.
4. No inventes issues, PRs, ramas, commits, validaciones, aprobaciones ni
   revisiones.
5. Recuerda la regla base: outputs, templates, prompts, roles y variables dan
   forma; nunca dan permiso.
6. Browser chat queda draft-only. Terminal escribe solo con aprobacion PM exacta
   mas gates resueltos.
7. Ante evidencia faltante, autoridad ambigua, kernel faltante o validacion
   fallida: fail-closed con `output.status_result`.
8. Nunca pidas, copies, registres ni resumas secretos o valores con pinta de
   secreto. Redacta como `[REDACTED]`.

## Indice

- `00-resolucion-y-fuentes.md`: manifiesto, fuentes de verdad, resolver y
  no-autorizacion.
- `01-actores.md`: superficies de ejecucion.
- `02-modos.md`: alcance de accion de un terminal agent.
- `03-workflows.md`: perfiles de trabajo.
- `04-evidencia.md`: evidencia viva requerida.
- `05-salidas-y-estados.md`: contratos de salida y estados.
- `06-limites.md`: boundaries que siempre aplican.
- `07-capas-operativas.md`: trazabilidad, validacion, contexto y operaciones.
