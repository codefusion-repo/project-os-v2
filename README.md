# project-os-v2

**Project OS es un kernel operativo compacto y portable para dirigir proyectos
de software con agentes de IA sin perder el control.** Un set pequeño de
archivos JSON resolubles por agentes define **cómo comportarse** — actores,
modos, workflows, límites, evidencia, salidas y estados — mientras **todo el
estado vivo del proyecto queda en GitHub** y se lee al momento de la tarea.
Cualquier agente puede retomar un proyecto en frío resolviendo el kernel y
leyendo GitHub; nada depende de la memoria de un chat previo.

Hay dos superficies activas y semánticamente equivalentes:
**`project-os-es/`** (español, default) y **`project-os-en/`** (inglés,
selección explícita). Omitir el path de kernel siempre conserva español.

**English version:** [README.en.md](README.en.md).

## Qué es y qué no es

Project OS es un **sistema operativo humano-dirigido** para construir
productos reales con agentes de IA, preservando contexto, calidad,
trazabilidad y control: un operating layer de proceso, GitHub-native, anclado
en workflows concretos — issues, PRs, evidencia, validación proporcional,
review-before-close y decisiones PM exactas.

Qué **no** es:

- No es un agente de coding automático y no deja agentes trabajando sin
  supervisión: el humano conserva scope, aprobaciones, merge, cierre y
  release.
- No es un runtime, un runner hosteado ni un workflow engine.
- No es una API con capacidad de escritura ni una consola de operaciones.
- No reemplaza OpenAI Agents SDK, LangGraph/Deep Agents, AutoGen/Microsoft
  Agent Framework, Claude Code, Codex ni GitHub: es la capa de proceso bajo la
  cual esas herramientas ejecutan.

## Para quién

- **Personas aprendiendo o haciendo vibe coding.** Entender qué cambió y por
  qué; detectar errores que un agente de implementación omitió; revisar,
  ajustar scope y draftear correcciones desde browser chat; aprender debugging
  y QA desde evidencia concreta; continuar un trabajo sin depender de la
  memoria del chat anterior. Project OS es un complemento estructurado a cómo
  ya trabajas.
- **Developers y equipos con experiencia.** Scope y transiciones explícitos;
  review independiente entre implementación y closeout; resúmenes claros de
  cambios, riesgos y validación; trazabilidad GitHub-native; validación
  proporcional; autorización explícita; libertad para alternar agentes y
  proveedores sin perder el contexto del proyecto en una sola herramienta o
  ventana.

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
| `project-os-es/kernel/*.json` | Kernel operativo en español: actores, modos, workflows, límites, evidencia, salidas, estados, artefactos y skills | **Activa (default)** |
| `project-os-en/kernel/*.json` | Kernel operativo paralelo en inglés, con los mismos IDs, gates y relaciones | **Activa (explícita)** |
| `tools/project_os_resolve.py` | Único resolver determinista principal: default ES o EN mediante path explícito, sin conceder permisos | **Activa** |
| `project-os-es/docs/` | Docs PM-facing: `project-os-es/docs/empezar.md`, `project-os-es/docs/reglas.md`, `project-os-es/docs/ritmo.md`, `project-os-es/docs/benchmark-contexto.md` | **Activa** |
| `project-os-es/operaciones/` | Catálogo MOSDLC compacto en español, por fase | **Activa** |
| `project-os-es/adapters/` | Adapter templates `*.target.md` para adoptar Project OS en un target | **Activa** |
| `project-os-es/templates/` + `project-os-es/habilidades/` | Formas de artefactos y skills opcionales referenciados por el kernel | **Activa** |
| `project-os-en/docs/`, `operations/`, `adapters/`, `templates/`, `skills/` | Capas PM-facing inglesas paralelas | **Activa (explícita)** |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Adapters propios de este repo (corre sobre su propio kernel) | Adapter (self) |
| `docs/decisions/` | ADRs de este repositorio | Decisiones del repo |
| `tools/` + `tests/` | Resolver y validador del kernel activo, guards focalizados y diagnósticos read-only secundarios | Infraestructura activa |
La superficie anterior no forma parte del árbol actual. Cuando una auditoría
histórica la necesite, se recupera exclusivamente desde el historial git; no
es una ruta operativa ni una fuente activa.

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

La superficie inglesa se selecciona solo reemplazando el path por
`--kernel-dir project-os-en/kernel`. No existe preferencia persistente ni
selector global de idioma.

El resolver acepta `--hydration-level minimal|compact|full/debug`; `compact`
es el valor predeterminado práctico. El nivel solo proyecta cuánto contrato ya resuelto se
devuelve, nunca cambia autoridad ni lee estado vivo. `full/debug` es para
revisión, debugging o auditoría. El flag existente `--compact` continúa siendo
solo formato JSON sin indentación. Los tamaños por nivel, medidos con
metodología, tokenizer y fecha declarados, están en
[`project-os-es/docs/benchmark-contexto.md`](project-os-es/docs/benchmark-contexto.md).

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
4. **Genera un prompt local opcionalmente**: ejecuta
   `python tools/operation_prompt_wizard.py`. Al iniciar sin selección
   explícita, el wizard pregunta una sola vez
   `Elige idioma / Choose language [es/en]` (Enter mantiene español) y carga el
   bundle coherente de esa superficie: operaciones, skills y kernel
   orientativo. `--language es|en` selecciona lo mismo sin preguntar. La
   selección vive solo en la sesión del wizard y nunca adopta, instala ni
   configura un target. El wizard lista de forma
   recursiva las operaciones activas del catálogo seleccionado
   (por defecto `project-os-es/operaciones/`). Puedes
   mantener la lista enumerada, usar `/phases` para agruparla por `cross-fase`
   y `fase-*`, filtrar por título/path/fase, o seleccionar por índice, código
   MOS (`MOS-3.5`), filename, stem o path relativo. Solo escribe el artefacto
   local que confirmes.

## Validación

```sh
python3 -m tools.validate_kernel --kernel-dir project-os-es/kernel
python3 -m tools.validate_kernel --kernel-dir project-os-en/kernel
python3 -m pytest tests/ -q
```

`tests/test_active_project_os_resolver.py` guarda la resolución del kernel
español activo y evita referencias activas al resolver eliminado.
`tests/test_project_os_bilingual_parity.py` guarda la paridad estructural ES/EN,
los contratos MOS, adapters, paths y selección fail-closed.
`tools.validate_kernel` valida la superficie permitida seleccionada; español
sigue siendo su default cuando se omite `--kernel-dir`.

`tools.audit_target_adapters` y `tools.audit_traceability` siguen siendo
diagnósticos read-only manuales. CI (`.github/workflows/validate.yml`) ejecuta
solo la validación y la suite de tests: no hace writes y no automatiza ninguna
autoridad PM.

## Background

Este repo sostuvo antes una arquitectura de contract-graph (781 contratos),
reducida al kernel mínimo inglés tras una auditoría de uso real en 2026-06, y
luego consolidada en la superficie en español `project-os-es` como base
primaria (ADR 0003, `docs/decisions/0003-project-os-cli-adoption-model.md`).
La historia y el racional de superficies retiradas son recuperables desde git;
el árbol actual conserva español como default y su traducción inglesa paralela.

Por decisión durable (ADR 0005,
`docs/decisions/0005-public-repository-strategy.md`), este repositorio
permanece privado como baseline interno de CodeFusion; la futura superficie
pública de Project OS es un repositorio separado con su propio gate de
public-readiness. La documentación y el onboarding de este árbol se mantienen
reutilizables por esa superficie.

## Seguridad, contribuciones, soporte y conducta

- [SECURITY.md](SECURITY.md) — reporte responsable de vulnerabilidades,
  siempre por canal privado.
- [CONTRIBUTING.md](CONTRIBUTING.md) — proceso de contribución issue-first,
  en español o inglés, inbound=outbound bajo Apache-2.0.
- [SUPPORT.md](SUPPORT.md) — soporte best-effort, sin SLA.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Contributor Covenant 3.0.

## Licencia

Copyright 2026 CodeFusion SpA.

Este repositorio se distribuye bajo la [Apache License 2.0](LICENSE)
(SPDX: `Apache-2.0`). La licencia cubre el código, el kernel JSON, los
templates, las operaciones y la documentación del árbol.

La licencia no autoriza por sí misma nada más: publicación, visibilidad,
soporte, contribuciones y releases siguen sujetos a sus propios gates y
decisiones PM (ver `docs/security/PUBLIC_READINESS_REVIEW.md`).
