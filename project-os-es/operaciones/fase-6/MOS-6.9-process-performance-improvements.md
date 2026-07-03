# MOS-6.9 — Procesar mejoras de rendimiento

Operación MOSDLC `process-performance-improvements` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa las mejoras de rendimiento recomendadas.
**Para:** Convertir recomendaciones en trabajo priorizado.
**Cómo:** Clasifica mejoras hacia issues o follow-ups.

**Variables**
- Requeridas: AUDIT_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-6.3. Después: MOS-3.8 o MOS-3.3. Recomendada: MOS-3.3.
