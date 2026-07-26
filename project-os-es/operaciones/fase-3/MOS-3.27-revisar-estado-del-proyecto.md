# MOS-3.27 — Revisar estado y verificar postcondiciones

Operación MOSDLC `review-project-state` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Revisa el estado del proyecto dentro de una referencia acotada y,
cuando se declara una acción ejecutada con sus postcondiciones esperadas, las
verifica una a una contra la evidencia viva.
**Para:** Detectar drift entre docs, roadmap y realidad del repo dentro de esa
referencia, y confirmar que una acción declarada (merge, tag, cierre, deploy)
dejó el estado esperado.
**Cómo:** Reconstruye y conserva la `CHANGE_CLASS` de la unidad viva al
verificar, sin pedirla como input manual al PM: una unidad crítica se verifica
como `change_class.critical`, `review.independent`, `validation.broad`
y la densidad crítica del reporte, mientras su hidratación normal es
`compact` y solo cambia mediante un override explícito. `REVIEWED_REFERENCE` es
el único locator primario y acota ambos modos de revisión. Sin
`ACTION_EXECUTED`, usa `REVIEWED_REFERENCE` para acotar qué decisiones PM y
docs fijos contrastar contra la evidencia viva, y reporta drift únicamente
dentro de esa referencia. `ACTION_EXECUTED` y `EXPECTED_POSTCONDITIONS` activan
el modo de verificación de postcondiciones, cuyo scope proviene de
`REVIEWED_REFERENCE` explícita o de una fuente inequívoca ya presente en el
contexto; verifica cada postcondición contra la evidencia viva correspondiente
—merge efectivo, SHA final de la rama principal, correspondencia con el head
revisado, checks post-merge, cierre de la unidad, eliminación de la rama
remota y limpieza local— y reporta el estado de cada una. `ACTION_EXECUTED`
y `EXPECTED_POSTCONDITIONS` seleccionan y acotan el modo de verificación; nunca
son locators adicionales ni amplían la superficie revisada. No ejecuta ninguna
mutación; una postcondición no satisfecha o no verificable falla cerrado.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: ACTION_EXECUTED, REVIEWED_REFERENCE, EXPECTED_POSTCONDITIONS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (`ACTION_EXECUTED` y `EXPECTED_POSTCONDITIONS` activan la verificación de postcondiciones, cuyo scope proviene de `REVIEWED_REFERENCE` explícita o de una fuente inequívoca ya presente; el feedback y la pregunta del PM son contexto humano y nunca autorizan nada)

**Locator único y constraints humanos:** `REVIEWED_REFERENCE` es el único
locator primario de MOS-3.27 en ambos modos y nunca se combina con otro
locator en la captura rutinaria. Primero reutiliza una fuente inequívoca ya
seleccionada en el contexto de ejecución; en ese caso `REVIEWED_REFERENCE`
puede quedar vacío. Sin contexto suficiente, recibe exactamente una referencia
viva verificable —unidad de trabajo, PR, roadmap o registro equivalente— y
deriva desde ella el repositorio y las demás relaciones verificables; un
repositorio completo solo es la referencia cuando el PM o una unidad viva lo
selecciona explícitamente, nunca por omisión. `ACTION_EXECUTED` y
`EXPECTED_POSTCONDITIONS` solo seleccionan y acotan el modo de verificación;
nunca sustituyen ni amplían `REVIEWED_REFERENCE`. Sin `REVIEWED_REFERENCE` ni
una fuente inequívoca en contexto, o si su formato no es verificable, falla
cerrado con `status.needs_context` en vez de revisar todo el repositorio, sus
issues o su historial. Dos referencias vigentes materialmente incompatibles
devuelven `status.needs_context` o, ante decisiones PM en conflicto
verificable, `status.needs_pm_decision`; nunca elige una ni mezcla evidencia
de ambas.

**Entrega:** output.review_result (+output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase; MOS-3.7, MOS-3.11 o un deploy para verificar sus postcondiciones. Después: MOS-3.1, MOS-3.3 o MOS-R.9. Recomendada: MOS-R.9 si el drift es documental.
