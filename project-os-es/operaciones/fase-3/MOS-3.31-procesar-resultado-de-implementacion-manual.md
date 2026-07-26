# MOS-3.31 — Procesar el resultado de implementación manual

Operación MOSDLC `process-manual-implementation-result` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado de la implementación manual aplicada por el humano.
**Para:** Clasificar la ruta segura tras aplicar un plan manual.
**Cómo:** Deriva a review de PR cuando existe PR; nunca duplica ese review.

**Variables**
- Requeridas: ISSUE_NUMBER, MANUAL_IMPLEMENTATION_RESULT
- Opcionales: MANUAL_IMPLEMENTATION_PLAN, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** el repositorio, el PR y la rama se reconstruyen desde el
issue y el resultado vivo; no se piden al PM. El issue se conserva como unidad
formal porque la clase del cambio la exige, y `MANUAL_IMPLEMENTATION_RESULT` es
contenido humano que ninguna evidencia viva puede sustituir. Cuando la relación
issue↔PR no sea verificable, falla cerrado en vez de inventarla.

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.30. Después: MOS-3.7 si hay PR; MOS-3.5 o MOS-3.3 si no. Recomendada: MOS-3.7 si hay PR.
