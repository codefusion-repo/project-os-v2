# project-os-v2

**Project OS es un kernel operativo compacto y portable para dirigir proyectos
de software con agentes de IA sin perder el control.** Un set pequeño de
archivos JSON resolubles por agentes define **cómo comportarse** — actores,
modos, workflows, límites, evidencia, salidas y estados — mientras **todo el
estado vivo del proyecto queda en GitHub** y se lee al momento de la tarea.
Cualquier agente puede retomar un proyecto en frío resolviendo el kernel y
leyendo GitHub; nada depende de la memoria de un chat previo.

La superficie activa es la superficie en español: **`project-os-es/`**.

## Fuentes de verdad

- **Comportamiento estable** vive en `project-os-es/kernel/*.json` (versionado
  y guardado por tests).
- **Estado vivo del proyecto** (issues, PRs, ramas, commits, reviews) vive solo
  en GitHub y se reconstruye al momento de la tarea, según
  `project-os-es/docs/reglas.md`.
- Todo lo demás (adapters, operaciones, templates, docs) solo **bootea** un
  agente hacia esas dos fuentes y da forma a su output. La forma nunca otorga
  permisos (`boundary.output_not_permission`).

## Mapa del repositorio

| Ruta | Propósito | ¿Activa? |
| --- | --- | --- |
| `project-os-es/kernel/*.json` | El kernel operativo activo: actores, modos, workflows, límites, evidencia, salidas, estados, artefactos y skills | **Activa (canónica)** |
| `tools/project_os_resolve.py` | Resolver determinista principal: hidrata `project-os-es/kernel` por (actor, mode, workflow) sin conceder permisos | **Activa** |
| `project-os-es/docs/` | Docs PM-facing: `project-os-es/docs/empezar.md`, `project-os-es/docs/reglas.md`, `project-os-es/docs/ritmo.md` | **Activa** |
| `project-os-es/operaciones/` | Catálogo MOSDLC compacto en español, por fase | **Activa** |
| `project-os-es/adapters/` | Adapter templates `*.target.md` para adoptar Project OS en un target | **Activa** |
| `project-os-es/templates/` + `project-os-es/habilidades/` | Formas de artefactos y skills opcionales referenciados por el kernel | **Activa** |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Adapters propios de este repo (corre sobre su propio kernel) | Adapter (self) |
| `docs/decisions/` | ADRs de este repositorio | Decisiones del repo |
| `tools/` + `tests/` | Resolver y validador del kernel activo, guards focalizados y diagnósticos read-only secundarios | Infraestructura activa |
| `legacy-project-os/` | Source-basis histórico, cuando esté disponible explícitamente | **Archivo (no activa)** |

`legacy-project-os/` es source-basis histórico cuando se consulta de forma
explícita; ningún flujo activo se resuelve desde ahí.

## Cómo resuelve un agente el kernel

Lee `project-os-es/kernel/manifest.json` y sigue su `resolution_sequence`
exactamente. La resolución devuelve exactamente un estado —
`status.resolved`, `status.needs_context`, `status.needs_pm_decision` o
`status.blocked` — selecciona forma y gates, y **no otorga permiso** alguno.
Ante cualquier faltante o ambigüedad, falla cerrado.

En una superficie terminal con checkout local y Python, el fast path es el
resolver principal (los detalles de adopción viven en
`project-os-es/docs/empezar.md`):

```sh
python tools/project_os_resolve.py --actor <actor> --workflow <workflow> \
  --mode <mode> --kernel-dir project-os-es/kernel [--skill skill.<id>]
```

La resolución manual desde `project-os-es/kernel/manifest.json` sigue siendo
el fallback canónico. Las superficies browser/no terminales nunca ejecutan
repo-local Python: siempre resuelven manualmente desde el manifest. En ambos
casos el output resuelto solo da forma al comportamiento y no otorga permiso.

## Quick start

Project OS delega trabajo seguro a IA mediante operaciones compactas,
variables PM y trazabilidad viva en GitHub.

1. **Empieza por** `project-os-es/docs/empezar.md`: superficies, requisitos
   externos y primera sesión.
2. **Adopta el kernel en un target**: copia
   `project-os-es/adapters/AGENTS.target.md` a la raíz del repo target
   (terminal) o usa `project-os-es/adapters/BROWSER_CHAT.target.md` como
   bootloader de browser chat.
3. **Opera por fase**: el catálogo completo de operaciones está en
   `project-os-es/operaciones/README.md`; el ciclo día a día en
   `project-os-es/docs/ritmo.md`; las reglas no negociables en
   `project-os-es/docs/reglas.md`.

## Validación

```sh
python3 -m tools.validate_kernel   # valida project-os-es/kernel, el kernel activo
python3 -m pytest tests/ -q        # resolver principal y guards de rutas activas
```

`tests/test_active_project_os_resolver.py` guarda la resolución del kernel
español activo y evita referencias activas al resolver eliminado.
`tools.validate_kernel` valida `project-os-es/kernel/*.json`.

`tools.audit_target_adapters` y `tools.audit_traceability` siguen siendo
diagnósticos read-only manuales. CI (`.github/workflows/validate.yml`) ejecuta
solo la validación y la suite de tests: no hace writes y no automatiza ninguna
autoridad PM.

## Background

Este repo sostuvo antes una arquitectura de contract-graph (781 contratos),
reducida al kernel mínimo inglés tras una auditoría de uso real en 2026-06, y
luego consolidada en la superficie en español `project-os-es` como base
primaria (ADR 0003, `docs/decisions/0003-project-os-cli-adoption-model.md`).
La historia y el racional del kernel mínimo viven en
`legacy-project-os/docs/DESIGN.md`; el árbol anterior es recuperable desde el
historial de git.
