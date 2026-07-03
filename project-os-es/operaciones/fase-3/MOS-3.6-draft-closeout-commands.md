# MOS-3.6 — Draftear comandos de closeout

Operación MOSDLC `draft-closeout-commands` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.review_before_close · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- Compatibilidad: `templates/operations/10-draft-pr-closeout-and-cleanup-command.md`
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea el paquete de cierre y limpieza de issue/PR según estado vivo.
**Para:** Cerrar con evidencia completa y sin escritura del agente.
**Cómo:** Bundle copy-safe que ejecuta el Humano PM.

**Variables**
- Requeridas: PR_NUMBER, ISSUE_NUMBER
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7. Después: MOS-3.9. Recomendada: MOS-3.9.
