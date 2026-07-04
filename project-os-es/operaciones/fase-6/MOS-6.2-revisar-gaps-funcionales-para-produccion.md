# MOS-6.2 — Revisar gaps funcionales para producción

Operación MOSDLC `review-feature-gaps-production` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.source_basis
- Aprobación PM: No (read-only)

**Hace:** Revisa gaps de funcionalidades para production readiness.
**Para:** Saber qué falta funcionalmente antes de producción.
**Cómo:** Contrasta features reales contra docs y requisitos.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.6. Después: MOS-6.8. Recomendada: MOS-6.8.
