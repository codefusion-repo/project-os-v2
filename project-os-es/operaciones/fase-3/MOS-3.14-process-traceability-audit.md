# MOS-3.14 — Procesar la auditoría de trazabilidad

Operación MOSDLC `process-traceability-audit` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado de la auditoría de trazabilidad y clasifica la ruta segura.
**Para:** Convertir hallazgos de auditoría en acciones concretas.
**Cómo:** Clasifica cada hallazgo hacia corrección, follow-up o no-op.

**Variables**
- Requeridas: AUDIT_RESULT
- Opcionales: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.13. Después: MOS-3.5 o MOS-3.3. Recomendada: MOS-3.3 para lo no bloqueante.
