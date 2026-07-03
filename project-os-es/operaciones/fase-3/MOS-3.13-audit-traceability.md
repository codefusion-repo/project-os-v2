# MOS-3.13 — Auditar trazabilidad

Operación MOSDLC `audit-traceability` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/15-audit-issue-pr-traceability.md`
- Aprobación PM: No (read-only)

**Hace:** Audita issue/PR y trazabilidad viva en GitHub.
**Para:** Verificar que el ciclo es reconstruible desde evidencia.
**Cómo:** Auditoría read-only de vínculos, evidencia de cierre y estado.

**Variables**
- Requeridas: ISSUE_NUMBER
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-3.14. Recomendada: MOS-3.14.
