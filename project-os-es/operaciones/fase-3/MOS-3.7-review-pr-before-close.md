# MOS-3.7 — Revisar el PR antes de cerrar

Operación MOSDLC `review-pr-before-close` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_before_close · mode.review_only · output.review_result (+output.pm_command_bundle)
- Evidencia: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- Compatibilidad: `templates/operations/09-review-pr-before-close-and-draft-package.md`
- Aprobación PM: No (no mergea ni cierra; draftea cierre solo si el review resuelve)

**Hace:** Revisa el PR contra el issue vinculado antes de draftear cierre y limpieza.
**Para:** Gate de calidad previo a todo cierre.
**Cómo:** Compara diff, validación y scope; consume execution reports como evidence leads.

**Variables**
- Requeridas: PR_NUMBER
- Opcionales: EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.review_result (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.4 o MOS-3.5. Después: MOS-3.6 si resuelve; MOS-3.5 si hay findings. Recomendada: MOS-3.6.
