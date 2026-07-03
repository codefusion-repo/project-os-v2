# MOS-1.9 — Revisar la eliminación de un requerimiento

Operación MOSDLC `review-requirement-removal` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Revisa el impacto de eliminar un requerimiento del proyecto.
**Para:** Evitar remociones que rompan roadmap, docs o dependencias.
**Cómo:** Analiza impacto y devuelve decisión al PM; fail-closed a status.needs_pm_decision.

**Variables**
- Requeridas: DESCRIPTION
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.7. Después: MOS-1.8 si el PM confirma. Recomendada: MOS-1.8 si el PM confirma la eliminación.
