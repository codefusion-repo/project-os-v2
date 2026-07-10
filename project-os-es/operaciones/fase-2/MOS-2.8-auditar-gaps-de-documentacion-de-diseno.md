# MOS-2.8 — Auditar gaps de documentación de diseño

Operación MOSDLC `audit-design-doc-gaps` · Fase 2 — Diseño · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.source_basis
- Aprobación PM: No (read-only)

**Hace:** Identifica gaps de la documentación existente respecto a la Fase 1.
**Para:** Priorizar qué diseño actualizar o crear.
**Cómo:** Contrasta inventario contra requisitos y lista gaps.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-2.7. Después: MOS-2.9 a MOS-2.13 según gap. Recomendada: la operación de actualización del gap principal.
