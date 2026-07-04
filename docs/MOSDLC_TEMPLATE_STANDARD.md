# MOSDLC Template Migration Standard

Este documento define el estandar durable para migrar templates de operaciones
MOSDLC. El mapa fuente para la migracion es `docs/MOSDLC_OPERATION_MAP.md`.

## Ubicacion

Los templates MOSDLC migrados viven fuera del catalogo numerado de
compatibilidad:

- Catalogo vigente de compatibilidad: templates numerados `00`-`37` bajo `templates/operations/`.
- Templates MOSDLC migrados: `templates/mosdlc/operations/fase-<n>/`.
- Operaciones recomendadas aceptadas migradas: bajo la fase que corresponda en
  `templates/mosdlc/operations/fase-<n>/`, o bajo
  `templates/mosdlc/operations/cross-fase/` cuando son transversales.

Las fases migradas usan `templates/mosdlc/operations/fase-<n>/` y conservan
los templates numerados `00`-`37` como fuentes de reemplazo o referencias de
compatibilidad. Ningun template numerado `00`-`37` se elimina, renombra o
renumera por una migracion MOSDLC.

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
  actual, salvo candidatos documentados en el mapa MOSDLC. Las fases migradas
  no introducen candidatos de kernel.
- Un template MOSDLC no autoriza escrituras por si mismo. La escritura terminal
  requiere aprobacion PM exacta, evidence requerido, branch preflight,
  validacion proporcional y review-before-close cuando aplique.
- La validacion sigue `docs/VALIDATION_POLICY.md`: los templates clasifican
  validacion agent-run, comandos PM-run, validacion manual PM o ausencia
  justificada de validacion automatizada. Una fase MOSDLC nueva no implica por
  si misma un archivo de tests nuevo.
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

## Fase 2 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-2.1 | `templates/mosdlc/operations/fase-2/MOS-2.1-draft-architecture-diagrams.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.2 | `templates/mosdlc/operations/fase-2/MOS-2.2-draft-uiux-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.3 | `templates/mosdlc/operations/fase-2/MOS-2.3-draft-data-algorithms-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.4 | `templates/mosdlc/operations/fase-2/MOS-2.4-draft-coding-standards-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.5 | `templates/mosdlc/operations/fase-2/MOS-2.5-draft-security-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.6 | `templates/mosdlc/operations/fase-2/MOS-2.6-validate-design-docs.md` | — |
| MOS-2.7 | `templates/mosdlc/operations/fase-2/MOS-2.7-inventory-design-docs.md` | — |
| MOS-2.8 | `templates/mosdlc/operations/fase-2/MOS-2.8-audit-design-doc-gaps.md` | `templates/operations/05-review-project-state-and-misalignment.md` |
| MOS-2.9 | `templates/mosdlc/operations/fase-2/MOS-2.9-update-architecture-diagrams.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.10 | `templates/mosdlc/operations/fase-2/MOS-2.10-update-uiux-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.11 | `templates/mosdlc/operations/fase-2/MOS-2.11-update-data-algorithms-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.12 | `templates/mosdlc/operations/fase-2/MOS-2.12-update-coding-standards-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.13 | `templates/mosdlc/operations/fase-2/MOS-2.13-update-security-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.14 | `templates/mosdlc/operations/fase-2/MOS-2.14-validate-updated-design-docs.md` | — |

## Fase 3 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-3.1 | `templates/mosdlc/operations/fase-3/MOS-3.1-draft-next-issue-from-traceability.md` | `templates/operations/06-draft-create-next-issue-command-from-traceability.md` |
| MOS-3.2 | `templates/mosdlc/operations/fase-3/MOS-3.2-draft-bounded-issue-set.md` | `templates/operations/29-draft-bounded-roadmap-issues-command.md` |
| MOS-3.3 | `templates/mosdlc/operations/fase-3/MOS-3.3-draft-follow-up-issue.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-3.4 | `templates/mosdlc/operations/fase-3/MOS-3.4-draft-implementation-route-prompt.md` | `templates/operations/07-draft-issue-implementation-route-prompt.md` |
| MOS-3.5 | `templates/mosdlc/operations/fase-3/MOS-3.5-draft-correction-route-prompt.md` | `templates/operations/08-draft-review-correction-route-prompt.md` |
| MOS-3.6 | `templates/mosdlc/operations/fase-3/MOS-3.6-draft-closeout-commands.md` | `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` |
| MOS-3.7 | `templates/mosdlc/operations/fase-3/MOS-3.7-review-pr-before-close.md` | `templates/operations/09-review-pr-before-close-and-draft-package.md` |
| MOS-3.8 | `templates/mosdlc/operations/fase-3/MOS-3.8-draft-issue-from-description.md` | `templates/operations/04-draft-create-issue-command-from-description.md` |
| MOS-3.9 | `templates/mosdlc/operations/fase-3/MOS-3.9-verify-post-merge.md` | `templates/operations/11-verify-post-merge-state.md` |
| MOS-3.10 | `templates/mosdlc/operations/fase-3/MOS-3.10-analyze-release-readiness.md` | `templates/operations/12-analyze-release-or-tag-readiness.md`, `templates/operations/13-draft-create-release-tag-command.md` |
| MOS-3.11 | `templates/mosdlc/operations/fase-3/MOS-3.11-draft-tag-commands.md` | `templates/operations/13-draft-create-release-tag-command.md` |
| MOS-3.12 | `templates/mosdlc/operations/fase-3/MOS-3.12-draft-release-commands.md` | `templates/operations/24-draft-create-github-release-command.md` |
| MOS-3.13 | `templates/mosdlc/operations/fase-3/MOS-3.13-audit-traceability.md` | `templates/operations/15-audit-issue-pr-traceability.md` |
| MOS-3.14 | `templates/mosdlc/operations/fase-3/MOS-3.14-process-traceability-audit.md` | — |
| MOS-3.15 | `templates/mosdlc/operations/fase-3/MOS-3.15-request-2d-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.16 | `templates/mosdlc/operations/fase-3/MOS-3.16-request-3d-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.17 | `templates/mosdlc/operations/fase-3/MOS-3.17-request-audio-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.18 | `templates/mosdlc/operations/fase-3/MOS-3.18-request-video-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.19 | `templates/mosdlc/operations/fase-3/MOS-3.19-process-2d-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.20 | `templates/mosdlc/operations/fase-3/MOS-3.20-process-3d-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.21 | `templates/mosdlc/operations/fase-3/MOS-3.21-process-audio-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.22 | `templates/mosdlc/operations/fase-3/MOS-3.22-process-video-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.23 | `templates/mosdlc/operations/fase-3/MOS-3.23-request-security-review.md` | `templates/operations/20-request-owasp-security-review.md` |
| MOS-3.24 | `templates/mosdlc/operations/fase-3/MOS-3.24-audit-implementation-discipline.md` | `templates/operations/25-audit-implementation-discipline-gaps.md` |
| MOS-3.25 | `templates/mosdlc/operations/fase-3/MOS-3.25-process-security-review.md` | `templates/operations/31-process-security-review-results.md` |
| MOS-3.26 | `templates/mosdlc/operations/fase-3/MOS-3.26-process-discipline-audit.md` | — |
| MOS-3.27 | `templates/mosdlc/operations/fase-3/MOS-3.27-review-project-state.md` | `templates/operations/05-review-project-state-and-misalignment.md` |
| MOS-3.28 | `templates/mosdlc/operations/fase-3/MOS-3.28-draft-follow-up-from-audit.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-3.29 | `templates/mosdlc/operations/fase-3/MOS-3.29-draft-follow-up-from-security.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-3.30 | `templates/mosdlc/operations/fase-3/MOS-3.30-draft-manual-implementation-plan.md` | `templates/operations/33-draft-manual-implementation-plan.md` |
| MOS-3.31 | `templates/mosdlc/operations/fase-3/MOS-3.31-process-manual-implementation-result.md` | `templates/operations/34-process-manual-implementation-result.md` |

## Fase 4 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-4.1 | `templates/mosdlc/operations/fase-4/MOS-4.1-draft-qa-checklist-issue-pr.md` | `templates/operations/18-draft-human-qa-checklist.md` |
| MOS-4.2 | `templates/mosdlc/operations/fase-4/MOS-4.2-draft-qa-checklist-description.md` | `templates/operations/18-draft-human-qa-checklist.md` |
| MOS-4.3 | `templates/mosdlc/operations/fase-4/MOS-4.3-draft-production-readiness-checklist.md` | `templates/operations/18-draft-human-qa-checklist.md` |
| MOS-4.4 | `templates/mosdlc/operations/fase-4/MOS-4.4-process-qa-checklist-issue-pr.md` | `templates/operations/30-process-human-qa-results.md` |
| MOS-4.5 | `templates/mosdlc/operations/fase-4/MOS-4.5-process-qa-checklist-feature.md` | `templates/operations/30-process-human-qa-results.md` |
| MOS-4.6 | `templates/mosdlc/operations/fase-4/MOS-4.6-process-production-readiness-checklist.md` | `templates/operations/30-process-human-qa-results.md` |
| MOS-4.7 | `templates/mosdlc/operations/fase-4/MOS-4.7-draft-follow-up-from-qa.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-4.8 | `templates/mosdlc/operations/fase-4/MOS-4.8-draft-correction-from-qa.md` | `templates/operations/08-draft-review-correction-route-prompt.md` |

## Fase 5 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-5.1 | `templates/mosdlc/operations/fase-5/MOS-5.1-analyze-local-deploy-readiness.md` | — |
| MOS-5.2 | `templates/mosdlc/operations/fase-5/MOS-5.2-draft-local-deploy-checklist.md` | — |
| MOS-5.3 | `templates/mosdlc/operations/fase-5/MOS-5.3-process-local-deploy-checklist.md` | — |
| MOS-5.4 | `templates/mosdlc/operations/fase-5/MOS-5.4-analyze-staging-deploy-readiness.md` | — |
| MOS-5.5 | `templates/mosdlc/operations/fase-5/MOS-5.5-draft-staging-deploy-checklist.md` | — |
| MOS-5.6 | `templates/mosdlc/operations/fase-5/MOS-5.6-process-staging-deploy-checklist.md` | — |
| MOS-5.7 | `templates/mosdlc/operations/fase-5/MOS-5.7-analyze-production-deploy-readiness.md` | — |
| MOS-5.8 | `templates/mosdlc/operations/fase-5/MOS-5.8-draft-production-deploy-checklist.md` | — |
| MOS-5.9 | `templates/mosdlc/operations/fase-5/MOS-5.9-process-production-deploy-checklist.md` | — |
| MOS-5.10 | `templates/mosdlc/operations/fase-5/MOS-5.10-draft-local-deploy-commands.md` | — |
| MOS-5.11 | `templates/mosdlc/operations/fase-5/MOS-5.11-execute-local-deploy.md` | — |
| MOS-5.12 | `templates/mosdlc/operations/fase-5/MOS-5.12-draft-staging-deploy-commands.md` | — |
| MOS-5.13 | `templates/mosdlc/operations/fase-5/MOS-5.13-execute-staging-deploy.md` | — |
| MOS-5.14 | `templates/mosdlc/operations/fase-5/MOS-5.14-draft-production-deploy-commands.md` | — |
| MOS-5.15 | `templates/mosdlc/operations/fase-5/MOS-5.15-execute-production-deploy.md` | — |

Fase 5 conserva las distinciones local, staging y produccion. Los analisis de
readiness son read-only/draft-only; los checklists son Human PM-facing; los
bundles de comandos son `output.pm_command_bundle` ejecutados por el Humano PM
y derivados solo de comandos target-owned. El issue #376 (MOSDLC.6a) aplico
`workflow.deployment`, `mode.delegated_deploy_execution` y
`evidence.deployment_readiness` para ejecucion interna local y staging: MOS-5.11
y MOS-5.13 son operaciones reales gated, internal-only y target-owned, con
aprobacion PM exacta por target/entorno/accion y fail-closed. MOS-5.15
(produccion) preserva postura `kernel:candidate`, no se ejecuta por agente y
queda con el Humano PM por defecto. Los detalles viven en
`docs/decisions/0001-fase5-deploy-execution-fail-closed.md`.

## Fase 6 Migrada

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-6.1 | `templates/mosdlc/operations/fase-6/MOS-6.1-review-security-production-readiness.md` | `templates/operations/20-request-owasp-security-review.md`, `templates/operations/25-audit-implementation-discipline-gaps.md` |
| MOS-6.2 | `templates/mosdlc/operations/fase-6/MOS-6.2-review-feature-gaps-production.md` | — |
| MOS-6.3 | `templates/mosdlc/operations/fase-6/MOS-6.3-analyze-performance-improvements.md` | — |
| MOS-6.4 | `templates/mosdlc/operations/fase-6/MOS-6.4-analyze-product-improvements.md` | — |
| MOS-6.5 | `templates/mosdlc/operations/fase-6/MOS-6.5-analyze-code-quality-gaps.md` | `templates/operations/25-audit-implementation-discipline-gaps.md` |
| MOS-6.6 | `templates/mosdlc/operations/fase-6/MOS-6.6-audit-dead-code.md` | — |
| MOS-6.7 | `templates/mosdlc/operations/fase-6/MOS-6.7-process-security-production-results.md` | `templates/operations/31-process-security-review-results.md` |
| MOS-6.8 | `templates/mosdlc/operations/fase-6/MOS-6.8-process-feature-gap-results.md` | — |
| MOS-6.9 | `templates/mosdlc/operations/fase-6/MOS-6.9-process-performance-improvements.md` | — |
| MOS-6.10 | `templates/mosdlc/operations/fase-6/MOS-6.10-process-product-improvements.md` | — |
| MOS-6.11 | `templates/mosdlc/operations/fase-6/MOS-6.11-process-code-improvements.md` | — |
| MOS-6.12 | `templates/mosdlc/operations/fase-6/MOS-6.12-process-dead-code-cleanup.md` | — |

Fase 6 cubre mantenimiento y herramientas: analisis read-only de seguridad,
gaps funcionales, rendimiento, producto, calidad de codigo y codigo muerto
(MOS-6.1 a MOS-6.6), y su procesamiento draft-only hacia correccion, follow-up,
roadmap o PM decision (MOS-6.7 a MOS-6.12). Ninguna fila agrega ids de kernel;
todas resuelven `workflow.review_only` o `workflow.pm_intake` con
`mode.review_only` existentes. Los analisis nunca ejecutan cambios ni claman
completitud; el procesamiento nunca autoriza correcciones, limpieza o
despliegue por si mismo.

## Operaciones Recomendadas Migradas

| MOSDLC ID | Template MOSDLC | Fuente de compatibilidad |
|---|---|---|
| MOS-R.1 | `templates/mosdlc/operations/fase-2/MOS-R.1-record-adr-decision.md` | `templates/operations/22-record-adr-decision.md` |
| MOS-R.2 | `templates/mosdlc/operations/cross-fase/MOS-R.2-recommend-next-operation.md` | `templates/operations/35-recommend-next-lifecycle-operation.md` |
| MOS-R.3 | `templates/mosdlc/operations/cross-fase/MOS-R.3-process-needs-pm-decision.md` | `templates/operations/36-process-needs-pm-decision.md` |
| MOS-R.4 | `templates/mosdlc/operations/cross-fase/MOS-R.4-review-phase-readiness.md` | `templates/operations/37-review-phase-readiness.md` |
| MOS-R.5 | `templates/mosdlc/operations/fase-0/MOS-R.5-audit-target-adoption-batch.md` | `templates/operations/14-audit-target-adapters.md`, `templates/operations/03-verify-target-adoption.md` |
| MOS-R.6 | `templates/mosdlc/operations/fase-2/MOS-R.6-create-update-adr-from-design.md` | `templates/operations/22-record-adr-decision.md` |
| MOS-R.7 | `templates/mosdlc/operations/fase-3/MOS-R.7-review-licensing-publication-readiness.md` | `templates/operations/12-analyze-release-or-tag-readiness.md` |
| MOS-R.8 | `templates/mosdlc/operations/fase-3/MOS-R.8-process-incident-hotfix.md` | — |
| MOS-R.9 | `templates/mosdlc/operations/fase-3/MOS-R.9-audit-docs-product-drift.md` | `templates/operations/05-review-project-state-and-misalignment.md` |
| MOS-R.10 | `templates/mosdlc/operations/fase-0/MOS-R.10-update-target-adapters-catalog.md` | `templates/operations/23-upgrade-kernel-adoption-in-target.md` |
| MOS-R.11 | `templates/mosdlc/operations/fase-5/MOS-R.11-deployment-readiness-review.md` | — |
| MOS-R.12 | `templates/mosdlc/operations/fase-5/MOS-R.12-draft-deploy-command-bundle.md` | — |
| MOS-R.13 | `templates/mosdlc/operations/fase-5/MOS-R.13-verify-post-deploy-state.md` | `templates/operations/11-verify-post-merge-state.md` |
| MOS-R.14 | `templates/mosdlc/operations/fase-5/MOS-R.14-process-deployment-result.md` | — |
| MOS-R.15 | `templates/mosdlc/operations/fase-5/MOS-R.15-draft-rollback-commands.md` | — |
| MOS-R.16 | `templates/mosdlc/operations/fase-5/MOS-R.16-process-rollback-result.md` | — |
| MOS-R.17 | `templates/mosdlc/operations/fase-6/MOS-R.17-dependency-security-update-audit.md` | — |
| MOS-R.18 | `templates/mosdlc/operations/fase-6/MOS-R.18-secret-safe-config-audit.md` | — |
| MOS-R.19 | `templates/mosdlc/operations/fase-4/MOS-R.19-plan-validation-cycle.md` | — |
| MOS-R.20 | `templates/mosdlc/operations/fase-4/MOS-R.20-review-validation-cycle-readiness.md` | `templates/operations/37-review-phase-readiness.md` |
| MOS-R.21 | `templates/mosdlc/operations/fase-4/MOS-R.21-process-validation-cycle-findings.md` | — |
| MOS-R.22 | `templates/mosdlc/operations/fase-3/MOS-R.22-public-packaging-safety-review.md` | — |
| MOS-R.23 | `templates/mosdlc/operations/fase-3/MOS-R.23-convert-internal-operations-before-release.md` | — |

Las operaciones recomendadas aceptadas (MOS-R.1 a MOS-R.23) se ubican segun su
rol de ciclo de vida: MOS-R.2, MOS-R.3 y MOS-R.4 son transversales y viven en
`templates/mosdlc/operations/cross-fase/`; las demas viven en la carpeta de la
fase donde encajan por conexiones, fuente de compatibilidad y uso practico
(adopcion en Fase 0, ADR/diseno en Fase 2, implementacion/release en Fase 3,
validacion en Fase 4, despliegue en Fase 5 y mantenimiento/seguridad en Fase
6). MOS-R.3 clarifica las variables y categorias de decision del procesamiento
de status.needs_pm_decision y declara el mapeo de variables hacia el template
36 de compatibilidad. MOS-R.19 a MOS-R.21 son operaciones target-agnostic de
ciclo de validacion (QA interna, staging/UAT, beta, TestFlight/internal
testing, playtest, release-candidate trial o pilot rollout segun el tipo de
target).
Ninguna operacion recomendada es exclusiva de un proyecto ni asume que todo
target tiene dogfood, packaging publico, releases de GitHub, adapters, staging
o entornos de despliegue: cada dependencia de superficie se declara explicita
en `LIVE_STATE` y falla cerrado cuando no aplica. MOS-R.12 y MOS-R.15 son
internal-only con redaccion estricta, comandos target-owned, aprobacion PM
exacta y advertencia pre-release convert. Ningun template recomendado agrega
ids de kernel; todas las filas resuelven workflows, modes, outputs y evidence
existentes.

El wizard local sigue leyendo `templates/operations/` como catalogo de
compatibilidad vigente. La exposicion PM de los templates MOSDLC migrados vive
en este documento, `docs/PM_OPERATIONS.md` y `docs/OPERATION_FLOWS.md` hasta
que un issue separado apruebe cambios de wizard o catalogo interactivo.
