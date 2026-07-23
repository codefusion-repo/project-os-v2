# MOS-3.27 — Revisar estado y verificar postcondiciones

Operación MOSDLC `review-project-state` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Revisa el estado del proyecto y, cuando se declara una acción
ejecutada con sus postcondiciones esperadas, las verifica una a una contra la
evidencia viva.
**Para:** Detectar drift entre docs, roadmap y realidad del repo, y confirmar
que una acción declarada (merge, tag, cierre, deploy) dejó el estado esperado.
**Cómo:** Sin `ACTION_EXECUTED`, usa decisiones PM y docs fijos como verdad
principal y reporta drift. Con `ACTION_EXECUTED`, `REVIEWED_REFERENCE` y
`EXPECTED_POSTCONDITIONS`, verifica cada postcondición contra la evidencia viva
correspondiente —merge efectivo, SHA final de la rama principal, correspondencia
con el head revisado, checks post-merge, cierre de la unidad, eliminación de la
rama remota y limpieza local— y reporta el estado de cada una. No ejecuta ninguna
mutación; una postcondición no satisfecha o no verificable falla cerrado.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: ACTION_EXECUTED, REVIEWED_REFERENCE, EXPECTED_POSTCONDITIONS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (declarar los tres primeros activa la verificación de postcondiciones; el feedback y la pregunta del PM son contexto humano y nunca autorizan nada)

**Entrega:** output.review_result (+output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase; MOS-3.7, MOS-3.11 o un deploy para verificar sus postcondiciones. Después: MOS-3.1, MOS-3.3 o MOS-R.9. Recomendada: MOS-R.9 si el drift es documental.
