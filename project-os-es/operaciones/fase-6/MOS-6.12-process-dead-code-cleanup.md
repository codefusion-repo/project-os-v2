# MOS-6.12 — Procesar limpieza de código muerto

Operación MOSDLC `process-dead-code-cleanup` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa la limpieza de código inútil detectado.
**Para:** Ejecutar la limpieza con scope acotado y seguro.
**Cómo:** Draftea la ruta de limpieza delegada por lotes acotados.

**Variables**
- Requeridas: AUDIT_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-6.6. Después: MOS-3.8 o MOS-3.3. Recomendada: MOS-3.8.
