# MOS-2.6 — Validar la documentación de diseño

Operación MOSDLC `validate-design-docs` · Fase 2 — Diseño · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Valida la documentación de diseño contra la Fase 1.
**Para:** Asegurar que el diseño responde a los requisitos.
**Cómo:** Revisión read-only con gaps y contradicciones accionables.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-2.1 a MOS-2.5. Después: MOS-R.4 y MOS-3.1. Recomendada: MOS-R.4.
