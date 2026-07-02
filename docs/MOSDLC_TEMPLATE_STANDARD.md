# MOSDLC Template Migration Standard

Este documento define el estandar durable para migrar templates de operaciones
MOSDLC. El mapa fuente para la migracion es `docs/MOSDLC_OPERATION_MAP.md`.

## Ubicacion

Los templates MOSDLC migrados viven fuera del catalogo numerado de
compatibilidad:

- Catalogo vigente de compatibilidad: templates numerados `00`-`37` bajo `templates/operations/`.
- Templates MOSDLC migrados: `templates/mosdlc/operations/fase-<n>/`.

La Fase 0 usa `templates/mosdlc/operations/fase-0/` y conserva los templates
numerados `00`, `01`, `02`, `03`, `17` y `23` como fuentes de reemplazo o
referencias de compatibilidad. Ningun template numerado `00`-`37` se elimina,
renombra o renumera por una migracion MOSDLC.

## Forma Obligatoria

Cada template MOSDLC es un prompt ejecutable para IA y usa esta forma:

1. Titulo Markdown con el id MOSDLC y el nombre corto.
2. Bloque `MOSDLC:` con id, fase, superficie, fuente de compatibilidad,
   clasificacion, workflow, mode, output y evidence.
3. Bloque `OPERATION:` con el objetivo operativo.
4. Bloque `INPUT:` con variables requeridas y opcionales. Todas las operaciones
   PM-facing incluyen `PM_FEEDBACK_HUMANO` y `PM_QUESTION_HUMANO` como contexto
   opcional.
5. Bloque `KERNEL:` con ids reales del kernel y la regla de resolver
   `kernel/manifest.json` antes de actuar.
6. Bloque `COMPATIBILITY_SOURCE:` que apunta al template `00`-`37` usado como
   fuente de reemplazo o compatibilidad.
7. Bloque `LIVE_STATE:` que exige reconstruir estado desde GitHub/git al
   momento de ejecutar y prohibe guardar estado vivo durable.
8. Bloques `DO:`, `OUTPUT:`, `LIMITS:` y `RECOMMENDED_NEXT_OPERATION:`.

## Reglas

- Los ids de workflow, mode, output y evidence deben existir en el kernel
  actual, salvo candidatos documentados en el mapa MOSDLC. La Fase 0 no
  introduce candidatos de kernel.
- Un template MOSDLC no autoriza escrituras por si mismo. La escritura terminal
  requiere aprobacion PM exacta, evidence requerido, branch preflight,
  validacion y review-before-close cuando aplique.
- Cada template debe declarar `Template authority: none` en `LIMITS`.
- Browser chat permanece draft-only.
- Los templates no guardan URLs vivas de issues/PRs, ramas de trabajo, SHAs,
  resultados de validacion, readiness de release/deploy ni planning vivo.
- `PM_FEEDBACK_HUMANO` y `PM_QUESTION_HUMANO` nunca reemplazan evidencia viva
  requerida ni autorizan mutaciones.
- La migracion de una fase no implica crecimiento del kernel. Cualquier nuevo
  workflow, mode, output, evidence, boundary o status necesita gap probado y
  aprobacion PM exacta separada.

## Fase 0 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-0.1 | `templates/mosdlc/operations/fase-0/MOS-0.1-activate-browser-session.md` | `templates/operations/00-browser-chat-activation.md` |
| MOS-0.2 | `templates/mosdlc/operations/fase-0/MOS-0.2-bootstrap-new-project.md` | `templates/operations/02-bootstrap-new-project.md` |
| MOS-0.3 | `templates/mosdlc/operations/fase-0/MOS-0.3-adopt-existing-project.md` | `templates/operations/01-adopt-project-os-in-existing-target.md` |
| MOS-0.4 | `templates/mosdlc/operations/fase-0/MOS-0.4-update-project-adoption.md` | `templates/operations/23-upgrade-kernel-adoption-in-target.md` |
| MOS-0.5 | `templates/mosdlc/operations/fase-0/MOS-0.5-verify-target-adoption.md` | `templates/operations/03-verify-target-adoption.md` |
| MOS-0.6 | `templates/mosdlc/operations/fase-0/MOS-0.6-handoff-session-context.md` | `templates/operations/17-draft-handoff-package-for-new-session.md` |

## Fase 1 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-1.1 | `templates/mosdlc/operations/fase-1/MOS-1.1-interview-requirements.md` | — |
| MOS-1.2 | `templates/mosdlc/operations/fase-1/MOS-1.2-summarize-requirements.md` | — |
| MOS-1.3 | `templates/mosdlc/operations/fase-1/MOS-1.3-verify-requirements-feasibility.md` | `templates/operations/16-review-idea-as-system-feature.md` |
| MOS-1.4 | `templates/mosdlc/operations/fase-1/MOS-1.4-draft-requirements-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-1.5 | `templates/mosdlc/operations/fase-1/MOS-1.5-validate-requirements-docs.md` | — |
| MOS-1.6 | `templates/mosdlc/operations/fase-1/MOS-1.6-plan-project-roadmap.md` | `templates/operations/27-draft-roadmap-from-docs.md` |
| MOS-1.7 | `templates/mosdlc/operations/fase-1/MOS-1.7-review-idea-feasibility.md` | `templates/operations/16-review-idea-as-system-feature.md` |
| MOS-1.8 | `templates/mosdlc/operations/fase-1/MOS-1.8-update-docs-roadmap-with-requirement.md` | `templates/operations/27-draft-roadmap-from-docs.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-1.9 | `templates/mosdlc/operations/fase-1/MOS-1.9-review-requirement-removal.md` | — |
| MOS-1.10 | `templates/mosdlc/operations/fase-1/MOS-1.10-extract-requirements-from-existing.md` | — |
| MOS-1.11 | `templates/mosdlc/operations/fase-1/MOS-1.11-update-requirements-docs-existing.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-1.12 | `templates/mosdlc/operations/fase-1/MOS-1.12-update-roadmap-existing.md` | `templates/operations/27-draft-roadmap-from-docs.md` |

El wizard local sigue leyendo `templates/operations/` como catalogo de
compatibilidad vigente. La exposicion PM de los templates MOSDLC migrados vive
en este documento, `docs/PM_OPERATIONS.md` y `docs/OPERATION_FLOWS.md` hasta
que un issue separado apruebe cambios de wizard o catalogo interactivo.
