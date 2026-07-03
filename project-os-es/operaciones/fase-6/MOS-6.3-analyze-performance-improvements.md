# MOS-6.3 — Analizar mejoras de rendimiento

Operación MOSDLC `analyze-performance-improvements` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Analiza y recomienda mejoras de rendimiento.
**Para:** Priorizar optimizaciones con evidencia.
**Cómo:** Análisis read-only con recomendaciones accionables.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: mantenimiento periódico. Después: MOS-6.9. Recomendada: MOS-6.9.
