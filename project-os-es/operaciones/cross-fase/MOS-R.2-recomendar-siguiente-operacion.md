# MOS-R.2 — Recomendar la siguiente operación

Operación MOSDLC `recommend-next-operation` · Transversal · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (solo recomienda; no ejecuta ni autoriza)

**Hace:** Recomienda exactamente una siguiente operación MOSDLC desde trazabilidad viva.
**Para:** Elegir ruta de ciclo de vida sin razonamiento ad hoc.
**Cómo:** Lee estado vivo, justifica la recomendación y muestra alternativas seguras si hay ambigüedad.

**Variables**
- Requeridas: ninguna
- Opcionales: TARGET_REPOSITORY, ISSUE_NUMBER, PR_NUMBER, ROADMAP_ISSUE, CURRENT_STATUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante trazabilidad insuficiente o ilegible: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier operación que necesite routing. Después: la operación recomendada, invocada por el Humano PM. Recomendada: la operación recomendada.
