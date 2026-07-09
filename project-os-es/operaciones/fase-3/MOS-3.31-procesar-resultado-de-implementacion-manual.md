# MOS-3.31 — Procesar el resultado de implementación manual

Operación MOSDLC `process-manual-implementation-result` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/34-process-manual-implementation-result.md`
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado de la implementación manual aplicada por el humano.
**Para:** Clasificar la ruta segura tras aplicar un plan manual.
**Cómo:** Deriva a review de PR cuando existe PR; nunca duplica ese review.

**Variables**
- Requeridas: ISSUE_NUMBER, MANUAL_IMPLEMENTATION_RESULT
- Opcionales: MANUAL_IMPLEMENTATION_PLAN, PR_NUMBER, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.30. Después: MOS-3.7 si hay PR; MOS-3.5 o MOS-3.3 si no. Recomendada: MOS-3.7 si hay PR.
