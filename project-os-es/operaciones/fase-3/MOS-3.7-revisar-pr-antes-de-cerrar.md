# MOS-3.7 — Revisar el PR antes de cerrar

Operación MOSDLC `review-pr-before-close` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_before_close · mode.review_only · output.review_result (+output.pm_command_bundle)
- Evidencia: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- Aprobación PM: No (no mergea ni cierra; draftea cierre solo si el review resuelve)

**Hace:** Revisa el cambio contra su unidad viva, clasifica cada hallazgo por
disposición y, con veredicto GO, entrega el closeout en la misma respuesta.
**Para:** Gate de calidad previo a todo cierre, sin turnos redundantes.
**Cómo:** Compara diff, validación y scope; consume execution reports como
evidence leads. Los findings se leen por intención: el incumplimiento material
es vinculante, la propuesta de solución es advisory. Clasifica cada hallazgo
como `blocking-correction`, `non-blocking-follow-up`, `preference`,
`accepted-risk` o `invalid-finding`; solo `blocking-correction` vuelve a
corrección por MOS-3.5. Toda corrección de este PR se registra como un
correction report append-only —review fuente, head anterior, head corregido,
findings abordados y validación— sin editar el body ni comentarios previos, y
alimenta un nuevo MOS-3.7 sobre el head corregido. Con GO, draftea en la misma
respuesta el bundle completo de closeout y su verificación final read-only. Si
ese bundle se pierde, queda obsoleto o el cierre falla, vuelve a ejecutar esta
operación sobre la evidencia vigente para regenerarlo; una verificación
posterior independiente de postcondiciones usa MOS-3.27.

**Variables**
- Requeridas: PR_NUMBER
- Opcionales: EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.review_result (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.4 o MOS-3.5. Después: con GO, el closeout y su
verificación van en la misma respuesta; MOS-3.5 solo con findings
`blocking-correction`; follow-ups no bloqueantes a MOS-3.3; verificación
posterior independiente con MOS-3.27. Recomendada: MOS-3.5 solo si hay
`blocking-correction`.
