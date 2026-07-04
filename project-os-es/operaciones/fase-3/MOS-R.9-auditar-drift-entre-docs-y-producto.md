# MOS-R.9 — Auditar drift entre docs y producto

Operación MOSDLC `audit-docs-product-drift` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.source_basis
- Compatibilidad: `templates/operations/05-review-project-state-and-misalignment.md`
- Aprobación PM: No (auditoría read-only)

**Hace:** Audita drift entre documentación y producto real.
**Para:** Mantener docs como verdad usable del producto.
**Cómo:** Contrasta docs, código y estado vivo; lista drift accionable con evidencia.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante docs, código o estado vivo ilegible: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.27 o revisión de estado. Después: MOS-1.8 si el drift es documental; MOS-3.3 para follow-ups de producto. Recomendada: MOS-1.8 cuando el drift sea documental.
