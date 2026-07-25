# MOS-3.5 — Draftear el route prompt de corrección

Operación MOSDLC `draft-correction-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el route-prompt de corrección de una unidad viva desde
findings con disposición `blocking-correction`.
**Para:** Corregir solo incumplimientos materiales sin expandir el scope original.
**Cómo:** Encapsula únicamente los findings `blocking-correction` en una ruta de
corrección delegada; los `non-blocking-follow-up` se difieren a MOS-3.3 y
`preference`, `accepted-risk` e `invalid-finding` no fuerzan cambios. El único
input humano normalmente necesario es `WORK_UNIT` —la unidad viva que el PM quiere
corregir— más la autorización exacta aplicable; el resto de la metadata se
reconstruye desde la evidencia viva y se muestra resuelta para inspección, no se
vuelve a pedir. Browser chat lee la unidad viva y sus relaciones, localiza el PR
existente cuando aplique, lee su conversación completa, selecciona el último review
vigente con `blocking-correction` sin resolver e incorpora sus addenda PM
posteriores como parte del mismo source basis, reconstruye o conserva la
`CHANGE_CLASS` de la unidad y deriva `HYDRATION_LEVEL` desde esa clase (`full/debug`
para `change_class.critical`). Con esos valores resueltos completa `WORK_UNIT`,
`SOURCE_REVIEW`, `PR_NUMBER`, `CHANGE_CLASS` y `HYDRATION_LEVEL` en el route-prompt
para que el receptor terminal verifique el contrato; nunca los inventa. Cuando
existe un único review vigente con `blocking-correction` sin resolver, lo selecciona
automáticamente; solo devuelve `status.needs_pm_decision` o `status.needs_context`
ante ambigüedad material real —dos reviews incompatibles igualmente vigentes,
relación unidad↔PR no verificable, comentarios materialmente truncados, evidencia
insuficiente para determinar la clase o contradicción real entre el review y una
decisión PM posterior—, nunca porque el PM no haya reescrito un ID, una clase o un
nivel reconstruibles. El route-prompt exige que el agente ejecutor publique
exactamente un correction report append-only en ese PR que referencie el review
fuente, registre el head anterior y el corregido, mapee cada `blocking-correction`
con su resultado, identifique commits o rango y la validación real, declare el
trabajo restante y confirme que no hubo merge ni cierre, sin editar el body ni
ningún comentario previo. Los findings se transportan por intención: el
incumplimiento material y su criterio observable son vinculantes; la redacción y
las propuestas de solución del reviewer son advisory. El browser chat puede
recomendar un skill opcional e infiere `RECOMMENDED_TERMINAL_AGENT_FAMILY` según el
trabajo. La recomendación es advisory, no autoriza nada y el feedback explícito del
PM puede reemplazarla.

**Variables**
- Requeridas: WORK_UNIT
- Opcionales: OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el skill, el
  feedback y la pregunta del PM son contexto; nunca autorizan nada)

**Metadata derivada:** `SOURCE_REVIEW`, `PR_NUMBER`, `CHANGE_CLASS` y
`HYDRATION_LEVEL` no son inputs manuales del wizard ni campos que el PM copie desde
GitHub: browser chat los reconstruye desde la evidencia viva y los muestra
resueltos en el route-prompt para verificación del receptor. `HYDRATION_LEVEL`
acepta `minimal`, `compact` o `full/debug`, se deriva de la `CHANGE_CLASS`
reconstruida y nunca queda por debajo de su densidad contractual; controla el
contenido hidratado del resolver y aplica la visibilidad PM-facing contractual del
recibo sin alterar el recibo interno ni `context_plan`. El wizard pide solo
`WORK_UNIT` y `PM_AUTHORIZATION_STATUS`; no solicita `SOURCE_REVIEW`, `PR_NUMBER`,
`CHANGE_CLASS` ni la densidad cuando pueden derivarse.

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.25 o MOS-4.4, solo con findings
`blocking-correction`. Después: MOS-3.7. Recomendada: MOS-3.7.
