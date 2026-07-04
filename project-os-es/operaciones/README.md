# Operaciones MOSDLC — superficie compacta en español

Esta carpeta es la superficie PM-facing en español de las operaciones MOSDLC
(**Modern AI SDLC Operations**). Cada archivo es un prompt de operación
compacto: qué hace, qué variables necesita, qué evidencia exige, qué entrega y
cuál es la siguiente operación segura.

Fuentes de esta superficie (issue #377): `docs/MOSDLC_OPERATION_MAP.md` (mapa
canónico) y los templates migrados en `templates/mosdlc/operations/fase-*`.
Los templates raíz (`templates/mosdlc/operations/` y
`templates/operations/` 00-37) siguen disponibles como fuente de reemplazo y
referencia de compatibilidad; esta carpeta no los reemplaza ni los renumera.

## Contrato común

Toda operación de esta carpeta opera bajo este contrato. Cada regla vive en su
capa dueña (ver `docs/decisions/0002-pre-377-validation-fastpath-audit.md`);
aquí solo se referencia, no se redefine.

1. **Kernel primero.** Resuelve `kernel/manifest.json` siguiendo su
   `resolution_sequence` antes de actuar. En terminal usa el fast path
   `python -m tools.project_os_resolve --actor <actor> --workflow <workflow>
   --mode <mode> --kernel-dir <KERNEL_LOCAL_PATH>`; el resolver emite guía
   operativa y lecturas de trazabilidad, y nunca consulta GitHub/git por ti.
2. **Estado vivo, siempre vivo.** Reconstruye issues, PRs, ramas, commits y
   validaciones desde GitHub/git al momento de ejecutar, según
   `docs/TRACEABILITY_PROTOCOL.md`. Nada de estado vivo en archivos durables y
   nada de estado inventado: reportes y comentarios son claims hasta
   verificarlos.
3. **Validación proporcional.** Clasifica la validación según
   `docs/VALIDATION_POLICY.md`: agent-run obligatoria, comandos PM-run
   drafteados, validación manual PM, o ausencia justificada. Nunca asumas full
   suite ni tests nuevos por defecto.
4. **Economía de contexto.** Aplica `docs/CONTEXT_ECONOMY.md` para clases de
   contexto y disciplina de subagentes.
5. **Formas PM-facing.** Los route prompts y command bundles siguen
   `templates/route-prompt.md` y `templates/pm-command-bundle.md`; son outputs
   no autorizantes que el PM revisa y ejecuta.
6. **Ningún template autoriza nada.** Template authority: none
   (`boundary.output_not_permission`). Escritura, merge, cierre, labels,
   settings, release y despliegue exigen aprobación PM exacta separada más los
   gates resueltos del kernel para esa acción específica. Browser chat
   permanece draft-only.
7. **Fail-closed.** Ante kernel faltante, evidencia faltante, autoridad
   ambigua o validación fallida: detente y entrega `output.status_result` con
   la decisión que el PM debe tomar (`status.needs_pm_decision`,
   `status.needs_context` o `status.blocked` según corresponda).
8. **Secretos.** Nunca pidas, expongas ni registres secretos, valores de
   `.env`, credenciales, tokens, cookies, JWTs, URLs de base de datos, claves
   privadas ni valores con pinta de secreto; redacta como `[REDACTED]` y
   referencia solo nombres de variables, comandos, rutas y tipos de riesgo.
9. **Contexto humano opcional.** `PM_FEEDBACK_HUMANO` y `PM_QUESTION_HUMANO`
   están disponibles en toda operación como contexto del PM; nunca reemplazan
   evidencia viva requerida ni autorizan mutaciones.

## Cómo usar una operación

Copia el archivo de la operación como prompt, completa sus variables y
ejecútalo en la superficie que indica (`browser_chat`, `terminal_agent`,
`human_pm` o destinatario externo). El bloque **Conexiones** de cada operación
indica la operación previa, las siguientes seguras y la recomendada.

Las operaciones `MOS-R.*` son las recomendadas aceptadas del mapa MOSDLC y
también tienen prompts compactos en esta carpeta, colocados por rol de ciclo de
vida: `cross-fase/`, `fase-0/`, `fase-2/`, `fase-3/`, `fase-4/`, `fase-5/` y
`fase-6/`.

## Índice

### Transversales — Operaciones recomendadas aceptadas

- [MOS-R.2 — Recomendar la siguiente operación](cross-fase/MOS-R.2-recommend-next-operation.md)
- [MOS-R.3 — Procesar una decisión PM pendiente](cross-fase/MOS-R.3-process-needs-pm-decision.md)
- [MOS-R.4 — Revisar readiness de fase](cross-fase/MOS-R.4-review-phase-readiness.md)

### Fase 0 — Adaptación

- [MOS-0.1 — Activar la sesión de browser chat](fase-0/MOS-0.1-activate-browser-session.md)
- [MOS-0.2 — Iniciar un proyecto nuevo](fase-0/MOS-0.2-bootstrap-new-project.md)
- [MOS-0.3 — Adoptar un proyecto existente](fase-0/MOS-0.3-adopt-existing-project.md)
- [MOS-0.4 — Actualizar la adopción de un proyecto](fase-0/MOS-0.4-update-project-adoption.md)
- [MOS-0.5 — Verificar la adopción del target](fase-0/MOS-0.5-verify-target-adoption.md)
- [MOS-0.6 — Transferir el contexto de sesión](fase-0/MOS-0.6-handoff-session-context.md)
- [MOS-R.5 — Auditar adopción de targets en lote](fase-0/MOS-R.5-audit-target-adoption-batch.md)
- [MOS-R.10 — Actualizar catálogo de adapters del target](fase-0/MOS-R.10-update-target-adapters-catalog.md)

### Fase 1 — Requerimientos, planificación y viabilidad

- [MOS-1.1 — Entrevistar requisitos](fase-1/MOS-1.1-interview-requirements.md)
- [MOS-1.2 — Resumir los requisitos identificados](fase-1/MOS-1.2-summarize-requirements.md)
- [MOS-1.3 — Verificar la viabilidad de los requisitos](fase-1/MOS-1.3-verify-requirements-feasibility.md)
- [MOS-1.4 — Draftear la documentación de requisitos](fase-1/MOS-1.4-draft-requirements-docs.md)
- [MOS-1.5 — Validar la documentación de requisitos](fase-1/MOS-1.5-validate-requirements-docs.md)
- [MOS-1.6 — Planificar el roadmap del proyecto](fase-1/MOS-1.6-plan-project-roadmap.md)
- [MOS-1.7 — Revisar la viabilidad de una idea](fase-1/MOS-1.7-review-idea-feasibility.md)
- [MOS-1.8 — Actualizar docs y roadmap con un requerimiento](fase-1/MOS-1.8-update-docs-roadmap-with-requirement.md)
- [MOS-1.9 — Revisar la eliminación de un requerimiento](fase-1/MOS-1.9-review-requirement-removal.md)
- [MOS-1.10 — Extraer requisitos de un proyecto existente](fase-1/MOS-1.10-extract-requirements-from-existing.md)
- [MOS-1.11 — Actualizar docs de requisitos de un proyecto existente](fase-1/MOS-1.11-update-requirements-docs-existing.md)
- [MOS-1.12 — Actualizar el roadmap de un proyecto existente](fase-1/MOS-1.12-update-roadmap-existing.md)

### Fase 2 — Diseño

- [MOS-2.1 — Draftear diagramas de arquitectura](fase-2/MOS-2.1-draft-architecture-diagrams.md)
- [MOS-2.2 — Draftear documentación UI/UX](fase-2/MOS-2.2-draft-uiux-docs.md)
- [MOS-2.3 — Draftear docs de datos y algoritmos](fase-2/MOS-2.3-draft-data-algorithms-docs.md)
- [MOS-2.4 — Draftear estándares de codificación](fase-2/MOS-2.4-draft-coding-standards-docs.md)
- [MOS-2.5 — Draftear documentación de seguridad](fase-2/MOS-2.5-draft-security-docs.md)
- [MOS-2.6 — Validar la documentación de diseño](fase-2/MOS-2.6-validate-design-docs.md)
- [MOS-2.7 — Inventariar la documentación de diseño](fase-2/MOS-2.7-inventory-design-docs.md)
- [MOS-2.8 — Auditar gaps de documentación de diseño](fase-2/MOS-2.8-audit-design-doc-gaps.md)
- [MOS-2.9 — Actualizar diagramas de arquitectura](fase-2/MOS-2.9-update-architecture-diagrams.md)
- [MOS-2.10 — Actualizar documentación UI/UX](fase-2/MOS-2.10-update-uiux-docs.md)
- [MOS-2.11 — Actualizar docs de datos y algoritmos](fase-2/MOS-2.11-update-data-algorithms-docs.md)
- [MOS-2.12 — Actualizar estándares de codificación](fase-2/MOS-2.12-update-coding-standards-docs.md)
- [MOS-2.13 — Actualizar documentación de seguridad](fase-2/MOS-2.13-update-security-docs.md)
- [MOS-2.14 — Validar la documentación de diseño actualizada](fase-2/MOS-2.14-validate-updated-design-docs.md)
- [MOS-R.1 — Registrar una decisión ADR](fase-2/MOS-R.1-record-adr-decision.md)
- [MOS-R.6 — Crear o actualizar ADR desde diseño](fase-2/MOS-R.6-create-update-adr-from-design.md)

### Fase 3 — Implementación

- [MOS-3.1 — Draftear el siguiente issue desde trazabilidad](fase-3/MOS-3.1-draft-next-issue-from-traceability.md)
- [MOS-3.2 — Draftear un set acotado de issues](fase-3/MOS-3.2-draft-bounded-issue-set.md)
- [MOS-3.3 — Draftear un follow-up issue](fase-3/MOS-3.3-draft-follow-up-issue.md)
- [MOS-3.4 — Draftear el route prompt de implementación](fase-3/MOS-3.4-draft-implementation-route-prompt.md)
- [MOS-3.5 — Draftear el route prompt de corrección](fase-3/MOS-3.5-draft-correction-route-prompt.md)
- [MOS-3.6 — Draftear comandos de closeout](fase-3/MOS-3.6-draft-closeout-commands.md)
- [MOS-3.7 — Revisar el PR antes de cerrar](fase-3/MOS-3.7-review-pr-before-close.md)
- [MOS-3.8 — Draftear un issue desde una descripción](fase-3/MOS-3.8-draft-issue-from-description.md)
- [MOS-3.9 — Verificar el estado post-merge](fase-3/MOS-3.9-verify-post-merge.md)
- [MOS-3.10 — Analizar readiness de release](fase-3/MOS-3.10-analyze-release-readiness.md)
- [MOS-3.11 — Draftear comandos de tag](fase-3/MOS-3.11-draft-tag-commands.md)
- [MOS-3.12 — Draftear comandos de release](fase-3/MOS-3.12-draft-release-commands.md)
- [MOS-3.13 — Auditar trazabilidad](fase-3/MOS-3.13-audit-traceability.md)
- [MOS-3.14 — Procesar la auditoría de trazabilidad](fase-3/MOS-3.14-process-traceability-audit.md)
- [MOS-3.15 — Solicitar un asset 2D](fase-3/MOS-3.15-request-2d-asset.md)
- [MOS-3.16 — Solicitar un asset 3D](fase-3/MOS-3.16-request-3d-asset.md)
- [MOS-3.17 — Solicitar un asset de audio](fase-3/MOS-3.17-request-audio-asset.md)
- [MOS-3.18 — Solicitar un asset de video](fase-3/MOS-3.18-request-video-asset.md)
- [MOS-3.19 — Procesar la entrega de un asset 2D](fase-3/MOS-3.19-process-2d-asset-delivery.md)
- [MOS-3.20 — Procesar la entrega de un asset 3D](fase-3/MOS-3.20-process-3d-asset-delivery.md)
- [MOS-3.21 — Procesar la entrega de un asset de audio](fase-3/MOS-3.21-process-audio-asset-delivery.md)
- [MOS-3.22 — Procesar la entrega de un asset de video](fase-3/MOS-3.22-process-video-asset-delivery.md)
- [MOS-3.23 — Solicitar revisión de seguridad](fase-3/MOS-3.23-request-security-review.md)
- [MOS-3.24 — Auditar disciplina de implementación](fase-3/MOS-3.24-audit-implementation-discipline.md)
- [MOS-3.25 — Procesar la revisión de seguridad](fase-3/MOS-3.25-process-security-review.md)
- [MOS-3.26 — Procesar la auditoría de disciplina](fase-3/MOS-3.26-process-discipline-audit.md)
- [MOS-3.27 — Revisar el estado del proyecto](fase-3/MOS-3.27-review-project-state.md)
- [MOS-3.28 — Draftear un follow-up desde auditoría](fase-3/MOS-3.28-draft-follow-up-from-audit.md)
- [MOS-3.29 — Draftear un follow-up desde seguridad](fase-3/MOS-3.29-draft-follow-up-from-security.md)
- [MOS-3.30 — Draftear un plan de implementación manual](fase-3/MOS-3.30-draft-manual-implementation-plan.md)
- [MOS-3.31 — Procesar el resultado de implementación manual](fase-3/MOS-3.31-process-manual-implementation-result.md)
- [MOS-R.7 — Revisar readiness de licenciamiento y publicación](fase-3/MOS-R.7-review-licensing-publication-readiness.md)
- [MOS-R.8 — Procesar incidente o hotfix](fase-3/MOS-R.8-process-incident-hotfix.md)
- [MOS-R.9 — Auditar drift entre docs y producto](fase-3/MOS-R.9-audit-docs-product-drift.md)
- [MOS-R.22 — Revisar seguridad de packaging público](fase-3/MOS-R.22-public-packaging-safety-review.md)
- [MOS-R.23 — Convertir operaciones internas antes de release](fase-3/MOS-R.23-convert-internal-operations-before-release.md)

### Fase 4 — QA y verificación humana

- [MOS-4.1 — Draftear el checklist QA de un issue/PR](fase-4/MOS-4.1-draft-qa-checklist-issue-pr.md)
- [MOS-4.2 — Draftear un checklist QA desde una descripción](fase-4/MOS-4.2-draft-qa-checklist-description.md)
- [MOS-4.3 — Draftear el checklist de production readiness](fase-4/MOS-4.3-draft-production-readiness-checklist.md)
- [MOS-4.4 — Procesar el checklist QA de un issue/PR](fase-4/MOS-4.4-process-qa-checklist-issue-pr.md)
- [MOS-4.5 — Procesar el checklist QA de una feature](fase-4/MOS-4.5-process-qa-checklist-feature.md)
- [MOS-4.6 — Procesar el checklist de production readiness](fase-4/MOS-4.6-process-production-readiness-checklist.md)
- [MOS-4.7 — Draftear un follow-up desde QA](fase-4/MOS-4.7-draft-follow-up-from-qa.md)
- [MOS-4.8 — Draftear una corrección desde QA](fase-4/MOS-4.8-draft-correction-from-qa.md)
- [MOS-R.19 — Planificar ciclo de validación](fase-4/MOS-R.19-plan-validation-cycle.md)
- [MOS-R.20 — Revisar readiness de ciclo de validación](fase-4/MOS-R.20-review-validation-cycle-readiness.md)
- [MOS-R.21 — Procesar hallazgos de ciclo de validación](fase-4/MOS-R.21-process-validation-cycle-findings.md)

### Fase 5 — Despliegue local / staging / producción

- [MOS-5.1 — Analizar readiness de despliegue local](fase-5/MOS-5.1-analyze-local-deploy-readiness.md)
- [MOS-5.2 — Draftear el checklist de despliegue local](fase-5/MOS-5.2-draft-local-deploy-checklist.md)
- [MOS-5.3 — Procesar el checklist de despliegue local](fase-5/MOS-5.3-process-local-deploy-checklist.md)
- [MOS-5.4 — Analizar readiness de despliegue staging](fase-5/MOS-5.4-analyze-staging-deploy-readiness.md)
- [MOS-5.5 — Draftear el checklist de despliegue staging](fase-5/MOS-5.5-draft-staging-deploy-checklist.md)
- [MOS-5.6 — Procesar el checklist de despliegue staging](fase-5/MOS-5.6-process-staging-deploy-checklist.md)
- [MOS-5.7 — Analizar readiness de despliegue a producción](fase-5/MOS-5.7-analyze-production-deploy-readiness.md)
- [MOS-5.8 — Draftear el checklist de despliegue a producción](fase-5/MOS-5.8-draft-production-deploy-checklist.md)
- [MOS-5.9 — Procesar el checklist de despliegue a producción](fase-5/MOS-5.9-process-production-deploy-checklist.md)
- [MOS-5.10 — Draftear comandos de despliegue local](fase-5/MOS-5.10-draft-local-deploy-commands.md)
- [MOS-5.11 — Ejecutar el despliegue local (interno)](fase-5/MOS-5.11-execute-local-deploy.md)
- [MOS-5.12 — Draftear comandos de despliegue staging](fase-5/MOS-5.12-draft-staging-deploy-commands.md)
- [MOS-5.13 — Ejecutar el despliegue staging (interno)](fase-5/MOS-5.13-execute-staging-deploy.md)
- [MOS-5.14 — Draftear comandos de despliegue a producción](fase-5/MOS-5.14-draft-production-deploy-commands.md)
- [MOS-5.15 — Despliegue a producción (Humano PM)](fase-5/MOS-5.15-execute-production-deploy.md)
- [MOS-R.11 — Revisar readiness de despliegue por entorno](fase-5/MOS-R.11-deployment-readiness-review.md)
- [MOS-R.12 — Draftear bundle de comandos de despliegue](fase-5/MOS-R.12-draft-deploy-command-bundle.md)
- [MOS-R.13 — Verificar estado post-deploy](fase-5/MOS-R.13-verify-post-deploy-state.md)
- [MOS-R.14 — Procesar resultado de despliegue](fase-5/MOS-R.14-process-deployment-result.md)
- [MOS-R.15 — Draftear comandos de rollback](fase-5/MOS-R.15-draft-rollback-commands.md)
- [MOS-R.16 — Procesar resultado de rollback](fase-5/MOS-R.16-process-rollback-result.md)

### Fase 6 — Mantenimiento y mejoras

- [MOS-6.1 — Revisar seguridad para production readiness](fase-6/MOS-6.1-review-security-production-readiness.md)
- [MOS-6.2 — Revisar gaps funcionales para producción](fase-6/MOS-6.2-review-feature-gaps-production.md)
- [MOS-6.3 — Analizar mejoras de rendimiento](fase-6/MOS-6.3-analyze-performance-improvements.md)
- [MOS-6.4 — Analizar mejoras de producto](fase-6/MOS-6.4-analyze-product-improvements.md)
- [MOS-6.5 — Analizar gaps de calidad de código](fase-6/MOS-6.5-analyze-code-quality-gaps.md)
- [MOS-6.6 — Auditar código muerto](fase-6/MOS-6.6-audit-dead-code.md)
- [MOS-6.7 — Procesar resultados de seguridad de producción](fase-6/MOS-6.7-process-security-production-results.md)
- [MOS-6.8 — Procesar resultados de gaps funcionales](fase-6/MOS-6.8-process-feature-gap-results.md)
- [MOS-6.9 — Procesar mejoras de rendimiento](fase-6/MOS-6.9-process-performance-improvements.md)
- [MOS-6.10 — Procesar mejoras de producto](fase-6/MOS-6.10-process-product-improvements.md)
- [MOS-6.11 — Procesar mejoras de código](fase-6/MOS-6.11-process-code-improvements.md)
- [MOS-6.12 — Procesar limpieza de código muerto](fase-6/MOS-6.12-process-dead-code-cleanup.md)
- [MOS-R.17 — Auditar actualizaciones de seguridad de dependencias](fase-6/MOS-R.17-dependency-security-update-audit.md)
- [MOS-R.18 — Auditar configuración de forma segura para secretos](fase-6/MOS-R.18-secret-safe-config-audit.md)
