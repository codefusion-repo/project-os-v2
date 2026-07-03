# MOS-6.5 — Analizar gaps de calidad de código

Operación MOSDLC `analyze-code-quality-gaps` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/25-audit-implementation-discipline-gaps.md`
- Aprobación PM: No (read-only)

**Hace:** Analiza y recomienda mejoras de normalización de código o gaps de clean code.
**Para:** Mantener el código consistente con los estándares de la Fase 2.
**Cómo:** Análisis read-only contra estándares documentados.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: mantenimiento periódico. Después: MOS-6.11. Recomendada: MOS-6.11.
