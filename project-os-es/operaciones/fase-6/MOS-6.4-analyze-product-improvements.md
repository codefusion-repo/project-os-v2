# MOS-6.4 — Analizar mejoras de producto

Operación MOSDLC `analyze-product-improvements` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Analiza y recomienda mejoras de producto.
**Para:** Alimentar el roadmap con mejoras fundadas.
**Cómo:** Análisis read-only de producto contra uso y docs.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: mantenimiento periódico. Después: MOS-6.10. Recomendada: MOS-6.10.
