# MOS-3.30 — Draftear un plan de implementación manual

Operación MOSDLC `draft-manual-implementation-plan` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.issue_implementation_manual · mode.review_only · output.manual_implementation_plan
- Evidencia: evidence.issue_scope, evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only; el humano aplica y valida)

**Hace:** Draftea el paso a paso humano-ejecutable para implementar un issue sin escribir archivos.
**Para:** Implementar cuando no hay terminal agent disponible o apropiado.
**Cómo:** Plan detallado por archivo y anclas; nunca afirma haber editado código.

**Variables**
- Requeridas: ISSUE_NUMBER
- Opcionales: TARGET_REPOSITORY, PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.manual_implementation_plan. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.1 o MOS-3.4 no disponible. Después: MOS-3.31. Recomendada: MOS-3.31.
