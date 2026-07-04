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
5. **Formas PM-facing.** Los outputs drafteables usan los artefactos resueltos
   desde `project-os-es/kernel/artefactos.json`: cada artefacto apunta a un
   `required_template` en `project-os-es/templates/`. Los templates raíz quedan
   como fuente de compatibilidad cuando haga falta; los outputs siguen siendo
   no autorizantes.
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
vida: `project-os-es/operaciones/cross-fase/`,
`project-os-es/operaciones/fase-0/`, `project-os-es/operaciones/fase-2/`,
`project-os-es/operaciones/fase-3/`, `project-os-es/operaciones/fase-4/`,
`project-os-es/operaciones/fase-5/` y `project-os-es/operaciones/fase-6/`.

## Índice

### Transversales — Operaciones recomendadas aceptadas

- [MOS-R.2 — Recomendar la siguiente operación](cross-fase/MOS-R.2-recomendar-siguiente-operacion.md)
- [MOS-R.3 — Procesar una decisión PM pendiente](cross-fase/MOS-R.3-procesar-decision-pm-pendiente.md)
- [MOS-R.4 — Revisar readiness de fase](cross-fase/MOS-R.4-revisar-readiness-de-fase.md)

### Fase 0 — Adaptación

- [MOS-0.1 — Activar la sesión de browser chat](fase-0/MOS-0.1-activar-sesion-browser-chat.md)
- [MOS-0.2 — Iniciar un proyecto nuevo](fase-0/MOS-0.2-iniciar-proyecto-nuevo.md)
- [MOS-0.3 — Adoptar un proyecto existente](fase-0/MOS-0.3-adoptar-proyecto-existente.md)
- [MOS-0.4 — Actualizar la adopción de un proyecto](fase-0/MOS-0.4-actualizar-adopcion-de-proyecto.md)
- [MOS-0.5 — Verificar la adopción del target](fase-0/MOS-0.5-verificar-adopcion-del-target.md)
- [MOS-0.6 — Transferir el contexto de sesión](fase-0/MOS-0.6-transferir-contexto-de-sesion.md)
- [MOS-R.5 — Auditar adopción de targets en lote](fase-0/MOS-R.5-auditar-adopcion-de-targets-en-lote.md)
- [MOS-R.10 — Actualizar catálogo de adapters del target](fase-0/MOS-R.10-actualizar-catalogo-de-adapters-del-target.md)

### Fase 1 — Requerimientos, planificación y viabilidad

- [MOS-1.1 — Entrevistar requisitos](fase-1/MOS-1.1-entrevistar-requisitos.md)
- [MOS-1.2 — Resumir los requisitos identificados](fase-1/MOS-1.2-resumir-requisitos-identificados.md)
- [MOS-1.3 — Verificar la viabilidad de los requisitos](fase-1/MOS-1.3-verificar-viabilidad-de-requisitos.md)
- [MOS-1.4 — Draftear la documentación de requisitos](fase-1/MOS-1.4-draftear-documentacion-de-requisitos.md)
- [MOS-1.5 — Validar la documentación de requisitos](fase-1/MOS-1.5-validar-documentacion-de-requisitos.md)
- [MOS-1.6 — Planificar el roadmap del proyecto](fase-1/MOS-1.6-planificar-roadmap-del-proyecto.md)
- [MOS-1.7 — Revisar la viabilidad de una idea](fase-1/MOS-1.7-revisar-viabilidad-de-idea.md)
- [MOS-1.8 — Actualizar docs y roadmap con un requerimiento](fase-1/MOS-1.8-actualizar-docs-y-roadmap-con-requerimiento.md)
- [MOS-1.9 — Revisar la eliminación de un requerimiento](fase-1/MOS-1.9-revisar-eliminacion-de-requerimiento.md)
- [MOS-1.10 — Extraer requisitos de un proyecto existente](fase-1/MOS-1.10-extraer-requisitos-de-proyecto-existente.md)
- [MOS-1.11 — Actualizar docs de requisitos de un proyecto existente](fase-1/MOS-1.11-actualizar-docs-de-requisitos-de-proyecto-existente.md)
- [MOS-1.12 — Actualizar el roadmap de un proyecto existente](fase-1/MOS-1.12-actualizar-roadmap-de-proyecto-existente.md)

### Fase 2 — Diseño

- [MOS-2.1 — Draftear diagramas de arquitectura](fase-2/MOS-2.1-draftear-diagramas-de-arquitectura.md)
- [MOS-2.2 — Draftear documentación UI/UX](fase-2/MOS-2.2-draftear-documentacion-uiux.md)
- [MOS-2.3 — Draftear docs de datos y algoritmos](fase-2/MOS-2.3-draftear-docs-de-datos-y-algoritmos.md)
- [MOS-2.4 — Draftear estándares de codificación](fase-2/MOS-2.4-draftear-estandares-de-codificacion.md)
- [MOS-2.5 — Draftear documentación de seguridad](fase-2/MOS-2.5-draftear-documentacion-de-seguridad.md)
- [MOS-2.6 — Validar la documentación de diseño](fase-2/MOS-2.6-validar-documentacion-de-diseno.md)
- [MOS-2.7 — Inventariar la documentación de diseño](fase-2/MOS-2.7-inventariar-documentacion-de-diseno.md)
- [MOS-2.8 — Auditar gaps de documentación de diseño](fase-2/MOS-2.8-auditar-gaps-de-documentacion-de-diseno.md)
- [MOS-2.9 — Actualizar diagramas de arquitectura](fase-2/MOS-2.9-actualizar-diagramas-de-arquitectura.md)
- [MOS-2.10 — Actualizar documentación UI/UX](fase-2/MOS-2.10-actualizar-documentacion-uiux.md)
- [MOS-2.11 — Actualizar docs de datos y algoritmos](fase-2/MOS-2.11-actualizar-docs-de-datos-y-algoritmos.md)
- [MOS-2.12 — Actualizar estándares de codificación](fase-2/MOS-2.12-actualizar-estandares-de-codificacion.md)
- [MOS-2.13 — Actualizar documentación de seguridad](fase-2/MOS-2.13-actualizar-documentacion-de-seguridad.md)
- [MOS-2.14 — Validar la documentación de diseño actualizada](fase-2/MOS-2.14-validar-documentacion-de-diseno-actualizada.md)
- [MOS-R.1 — Registrar una decisión ADR](fase-2/MOS-R.1-registrar-decision-adr.md)
- [MOS-R.6 — Crear o actualizar ADR desde diseño](fase-2/MOS-R.6-crear-o-actualizar-adr-desde-diseno.md)

### Fase 3 — Implementación

- [MOS-3.1 — Draftear el siguiente issue desde trazabilidad](fase-3/MOS-3.1-draftear-siguiente-issue-desde-trazabilidad.md)
- [MOS-3.2 — Draftear un set acotado de issues](fase-3/MOS-3.2-draftear-set-acotado-de-issues.md)
- [MOS-3.3 — Draftear un follow-up issue](fase-3/MOS-3.3-draftear-follow-up-issue.md)
- [MOS-3.4 — Draftear el route prompt de implementación](fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md)
- [MOS-3.5 — Draftear el route prompt de corrección](fase-3/MOS-3.5-draftear-route-prompt-de-correccion.md)
- [MOS-3.6 — Draftear comandos de closeout](fase-3/MOS-3.6-draftear-comandos-de-closeout.md)
- [MOS-3.7 — Revisar el PR antes de cerrar](fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md)
- [MOS-3.8 — Draftear un issue desde una descripción](fase-3/MOS-3.8-draftear-issue-desde-descripcion.md)
- [MOS-3.9 — Verificar el estado post-merge](fase-3/MOS-3.9-verificar-estado-post-merge.md)
- [MOS-3.10 — Analizar readiness de release](fase-3/MOS-3.10-analizar-readiness-de-release.md)
- [MOS-3.11 — Draftear comandos de tag](fase-3/MOS-3.11-draftear-comandos-de-tag.md)
- [MOS-3.12 — Draftear comandos de release](fase-3/MOS-3.12-draftear-comandos-de-release.md)
- [MOS-3.13 — Auditar trazabilidad](fase-3/MOS-3.13-auditar-trazabilidad.md)
- [MOS-3.14 — Procesar la auditoría de trazabilidad](fase-3/MOS-3.14-procesar-auditoria-de-trazabilidad.md)
- [MOS-3.15 — Solicitar un asset 2D](fase-3/MOS-3.15-solicitar-asset-2d.md)
- [MOS-3.16 — Solicitar un asset 3D](fase-3/MOS-3.16-solicitar-asset-3d.md)
- [MOS-3.17 — Solicitar un asset de audio](fase-3/MOS-3.17-solicitar-asset-de-audio.md)
- [MOS-3.18 — Solicitar un asset de video](fase-3/MOS-3.18-solicitar-asset-de-video.md)
- [MOS-3.19 — Procesar la entrega de un asset 2D](fase-3/MOS-3.19-procesar-entrega-de-asset-2d.md)
- [MOS-3.20 — Procesar la entrega de un asset 3D](fase-3/MOS-3.20-procesar-entrega-de-asset-3d.md)
- [MOS-3.21 — Procesar la entrega de un asset de audio](fase-3/MOS-3.21-procesar-entrega-de-asset-de-audio.md)
- [MOS-3.22 — Procesar la entrega de un asset de video](fase-3/MOS-3.22-procesar-entrega-de-asset-de-video.md)
- [MOS-3.23 — Solicitar revisión de seguridad](fase-3/MOS-3.23-solicitar-revision-de-seguridad.md)
- [MOS-3.24 — Auditar disciplina de implementación](fase-3/MOS-3.24-auditar-disciplina-de-implementacion.md)
- [MOS-3.25 — Procesar la revisión de seguridad](fase-3/MOS-3.25-procesar-revision-de-seguridad.md)
- [MOS-3.26 — Procesar la auditoría de disciplina](fase-3/MOS-3.26-procesar-auditoria-de-disciplina.md)
- [MOS-3.27 — Revisar el estado del proyecto](fase-3/MOS-3.27-revisar-estado-del-proyecto.md)
- [MOS-3.28 — Draftear un follow-up desde auditoría](fase-3/MOS-3.28-draftear-follow-up-desde-auditoria.md)
- [MOS-3.29 — Draftear un follow-up desde seguridad](fase-3/MOS-3.29-draftear-follow-up-desde-seguridad.md)
- [MOS-3.30 — Draftear un plan de implementación manual](fase-3/MOS-3.30-draftear-plan-de-implementacion-manual.md)
- [MOS-3.31 — Procesar el resultado de implementación manual](fase-3/MOS-3.31-procesar-resultado-de-implementacion-manual.md)
- [MOS-R.7 — Revisar readiness de licenciamiento y publicación](fase-3/MOS-R.7-revisar-readiness-de-licenciamiento-y-publicacion.md)
- [MOS-R.8 — Procesar incidente o hotfix](fase-3/MOS-R.8-procesar-incidente-o-hotfix.md)
- [MOS-R.9 — Auditar drift entre docs y producto](fase-3/MOS-R.9-auditar-drift-entre-docs-y-producto.md)
- [MOS-R.22 — Revisar seguridad de packaging público](fase-3/MOS-R.22-revisar-seguridad-de-packaging-publico.md)
- [MOS-R.23 — Convertir operaciones internas antes de release](fase-3/MOS-R.23-convertir-operaciones-internas-antes-de-release.md)

### Fase 4 — QA y verificación humana

- [MOS-4.1 — Draftear el checklist QA de un issue/PR](fase-4/MOS-4.1-draftear-checklist-qa-de-issue-pr.md)
- [MOS-4.2 — Draftear un checklist QA desde una descripción](fase-4/MOS-4.2-draftear-checklist-qa-desde-descripcion.md)
- [MOS-4.3 — Draftear el checklist de production readiness](fase-4/MOS-4.3-draftear-checklist-de-production-readiness.md)
- [MOS-4.4 — Procesar el checklist QA de un issue/PR](fase-4/MOS-4.4-procesar-checklist-qa-de-issue-pr.md)
- [MOS-4.5 — Procesar el checklist QA de una feature](fase-4/MOS-4.5-procesar-checklist-qa-de-feature.md)
- [MOS-4.6 — Procesar el checklist de production readiness](fase-4/MOS-4.6-procesar-checklist-de-production-readiness.md)
- [MOS-4.7 — Draftear un follow-up desde QA](fase-4/MOS-4.7-draftear-follow-up-desde-qa.md)
- [MOS-4.8 — Draftear una corrección desde QA](fase-4/MOS-4.8-draftear-correccion-desde-qa.md)
- [MOS-R.19 — Planificar ciclo de validación](fase-4/MOS-R.19-planificar-ciclo-de-validacion.md)
- [MOS-R.20 — Revisar readiness de ciclo de validación](fase-4/MOS-R.20-revisar-readiness-de-ciclo-de-validacion.md)
- [MOS-R.21 — Procesar hallazgos de ciclo de validación](fase-4/MOS-R.21-procesar-hallazgos-de-ciclo-de-validacion.md)

### Fase 5 — Despliegue local / staging / producción

- [MOS-5.1 — Analizar readiness de despliegue local](fase-5/MOS-5.1-analizar-readiness-de-despliegue-local.md)
- [MOS-5.2 — Draftear el checklist de despliegue local](fase-5/MOS-5.2-draftear-checklist-de-despliegue-local.md)
- [MOS-5.3 — Procesar el checklist de despliegue local](fase-5/MOS-5.3-procesar-checklist-de-despliegue-local.md)
- [MOS-5.4 — Analizar readiness de despliegue staging](fase-5/MOS-5.4-analizar-readiness-de-despliegue-staging.md)
- [MOS-5.5 — Draftear el checklist de despliegue staging](fase-5/MOS-5.5-draftear-checklist-de-despliegue-staging.md)
- [MOS-5.6 — Procesar el checklist de despliegue staging](fase-5/MOS-5.6-procesar-checklist-de-despliegue-staging.md)
- [MOS-5.7 — Analizar readiness de despliegue a producción](fase-5/MOS-5.7-analizar-readiness-de-despliegue-a-produccion.md)
- [MOS-5.8 — Draftear el checklist de despliegue a producción](fase-5/MOS-5.8-draftear-checklist-de-despliegue-a-produccion.md)
- [MOS-5.9 — Procesar el checklist de despliegue a producción](fase-5/MOS-5.9-procesar-checklist-de-despliegue-a-produccion.md)
- [MOS-5.10 — Draftear comandos de despliegue local](fase-5/MOS-5.10-draftear-comandos-de-despliegue-local.md)
- [MOS-5.11 — Ejecutar el despliegue local (interno)](fase-5/MOS-5.11-ejecutar-despliegue-local-interno.md)
- [MOS-5.12 — Draftear comandos de despliegue staging](fase-5/MOS-5.12-draftear-comandos-de-despliegue-staging.md)
- [MOS-5.13 — Ejecutar el despliegue staging (interno)](fase-5/MOS-5.13-ejecutar-despliegue-staging-interno.md)
- [MOS-5.14 — Draftear comandos de despliegue a producción](fase-5/MOS-5.14-draftear-comandos-de-despliegue-a-produccion.md)
- [MOS-5.15 — Despliegue a producción (Humano PM)](fase-5/MOS-5.15-despliegue-a-produccion-humano-pm.md)
- [MOS-R.11 — Revisar readiness de despliegue por entorno](fase-5/MOS-R.11-revisar-readiness-de-despliegue-por-entorno.md)
- [MOS-R.12 — Draftear bundle de comandos de despliegue](fase-5/MOS-R.12-draftear-bundle-de-comandos-de-despliegue.md)
- [MOS-R.13 — Verificar estado post-deploy](fase-5/MOS-R.13-verificar-estado-post-deploy.md)
- [MOS-R.14 — Procesar resultado de despliegue](fase-5/MOS-R.14-procesar-resultado-de-despliegue.md)
- [MOS-R.15 — Draftear comandos de rollback](fase-5/MOS-R.15-draftear-comandos-de-rollback.md)
- [MOS-R.16 — Procesar resultado de rollback](fase-5/MOS-R.16-procesar-resultado-de-rollback.md)

### Fase 6 — Mantenimiento y mejoras

- [MOS-6.1 — Revisar seguridad para production readiness](fase-6/MOS-6.1-revisar-seguridad-para-production-readiness.md)
- [MOS-6.2 — Revisar gaps funcionales para producción](fase-6/MOS-6.2-revisar-gaps-funcionales-para-produccion.md)
- [MOS-6.3 — Analizar mejoras de rendimiento](fase-6/MOS-6.3-analizar-mejoras-de-rendimiento.md)
- [MOS-6.4 — Analizar mejoras de producto](fase-6/MOS-6.4-analizar-mejoras-de-producto.md)
- [MOS-6.5 — Analizar gaps de calidad de código](fase-6/MOS-6.5-analizar-gaps-de-calidad-de-codigo.md)
- [MOS-6.6 — Auditar código muerto](fase-6/MOS-6.6-auditar-codigo-muerto.md)
- [MOS-6.7 — Procesar resultados de seguridad de producción](fase-6/MOS-6.7-procesar-resultados-de-seguridad-de-produccion.md)
- [MOS-6.8 — Procesar resultados de gaps funcionales](fase-6/MOS-6.8-procesar-resultados-de-gaps-funcionales.md)
- [MOS-6.9 — Procesar mejoras de rendimiento](fase-6/MOS-6.9-procesar-mejoras-de-rendimiento.md)
- [MOS-6.10 — Procesar mejoras de producto](fase-6/MOS-6.10-procesar-mejoras-de-producto.md)
- [MOS-6.11 — Procesar mejoras de código](fase-6/MOS-6.11-procesar-mejoras-de-codigo.md)
- [MOS-6.12 — Procesar limpieza de código muerto](fase-6/MOS-6.12-procesar-limpieza-de-codigo-muerto.md)
- [MOS-R.17 — Auditar actualizaciones de seguridad de dependencias](fase-6/MOS-R.17-auditar-actualizaciones-de-seguridad-de-dependencias.md)
- [MOS-R.18 — Auditar configuración de forma segura para secretos](fase-6/MOS-R.18-auditar-configuracion-de-forma-segura-para-secretos.md)
