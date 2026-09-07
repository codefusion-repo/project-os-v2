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
evidence leads. Reconstruye la `CHANGE_CLASS` de la unidad viva desde su
evidencia —no la pide como input manual al PM— y resuelve el review a esa clase:
una unidad crítica conserva `change_class.critical`, `review.independent`,
`validation.broad` y la densidad crítica del reporte, mientras su
hidratación normal es `compact` y solo cambia mediante un override
explícito. Los findings se leen por intención: el incumplimiento material
es vinculante, la propuesta de solución es advisory.
Antes de tratar una observación como hallazgo aplica el gate de materialidad de
`rule.economia_de_contexto`: exige un estado actual verificable, un outcome,
contrato, riesgo o capacidad insatisfecho, una acción concreta de mejora material
y valor durable; lo meramente histórico, informativo, confirmatorio, ya resuelto
por el curso normal o duplicado no es un hallazgo y se omite, o `invalid-finding`
sin routing si ya fue elevado. Solo entonces clasifica cada hallazgo como
`blocking-correction`, `non-blocking-follow-up`, `preference`, `accepted-risk` o
`invalid-finding`; un `non-blocking-follow-up` exige un gap vigente, durable y
accionable con scope independiente y razón para diferirlo, y solo
`blocking-correction` vuelve a corrección por MOS-3.5. Toda corrección de este PR
se registra como un correction report append-only —review fuente, head anterior,
head corregido, findings abordados y validación— sin editar el body ni
comentarios previos, y alimenta un nuevo MOS-3.7 sobre el head corregido. Con GO,
draftea en la misma respuesta el bundle completo de closeout y su verificación
final read-only. Si ese bundle se pierde, queda obsoleto o el cierre falla,
vuelve a ejecutar esta operación sobre la evidencia vigente para regenerarlo; una
verificación posterior independiente de postcondiciones usa MOS-3.27.

Reconstruye la misma unidad primaria y PR al recibir review, QA o un
correction report. QA manual requerido pendiente o fallido impide GO: usa
MOS-4.1/MOS-4.4 para completarlo dentro de esa unidad. El closeout no crea otra
unidad ni permite omitir findings bloqueantes o validar un head anterior.

**Variables**
- Requeridas: PR_NUMBER
- Opcionales: EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.review_result (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.4 o MOS-3.5. Después: con GO, el closeout y su
verificación van en la misma respuesta; MOS-3.5 solo con findings
`blocking-correction`; follow-ups no bloqueantes a MOS-3.3; verificación
posterior independiente con MOS-3.27. Recomendada: MOS-3.5 solo si hay
`blocking-correction`.
