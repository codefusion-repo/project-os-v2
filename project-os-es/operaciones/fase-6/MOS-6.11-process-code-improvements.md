# MOS-6.11 — Procesar mejoras de código

Operación MOSDLC `process-code-improvements` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa las mejoras de código recomendadas.
**Para:** Cerrar el loop de normalización de código.
**Cómo:** Clasifica mejoras hacia corrección o follow-up.

**Variables**
- Requeridas: AUDIT_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-6.5. Después: MOS-3.5 o MOS-3.3. Recomendada: MOS-3.3.
