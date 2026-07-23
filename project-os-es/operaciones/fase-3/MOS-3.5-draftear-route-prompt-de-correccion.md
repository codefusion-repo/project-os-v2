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
`preference`, `accepted-risk` e `invalid-finding` no fuerzan cambios. Completa
`WORK_UNIT` con la unidad viva corregida y conserva su `CHANGE_CLASS`. Transporta
la referencia exacta al review o comentario fuente (`SOURCE_REVIEW`) y, cuando la
unidad corrige un PR existente, su `PR_NUMBER`; ambos son obligatorios y nunca se
inventan. El route-prompt exige que el agente ejecutor publique exactamente un
correction report append-only en ese PR que referencie el review fuente, registre
el head anterior y el corregido, mapee cada `blocking-correction` con su resultado,
identifique commits o rango y la validación real, declare el trabajo restante y
confirme que no hubo merge ni cierre, sin editar el body ni ningún comentario
previo. Los findings se transportan por intención: el incumplimiento material y su
criterio observable son vinculantes; la redacción y las propuestas de solución del
reviewer son advisory. El browser chat puede recomendar un skill opcional e
infiere `RECOMMENDED_TERMINAL_AGENT_FAMILY` según el trabajo. La recomendación
es advisory, no autoriza nada y el feedback explícito del PM puede
reemplazarla.

**Variables**
- Requeridas: WORK_UNIT, SOURCE_REVIEW, PR_NUMBER, CHANGE_CLASS
- Opcionales: OPTIONAL_SKILL, HYDRATION_LEVEL, PM_FEEDBACK_HUMANO,
  PM_QUESTION_HUMANO (el skill, el nivel, el feedback y la pregunta del PM son
  contexto; nunca autorizan nada). `HYDRATION_LEVEL` acepta `minimal`,
  `compact` o `full/debug`; controla el contenido hidratado del resolver y aplica
  la visibilidad PM-facing contractual del recibo sin alterar el recibo interno ni
  `context_plan`. El wizard pide `PM_AUTHORIZATION_STATUS` de forma requerida y
  precarga `HYDRATION_LEVEL` con la densidad contractual de la `CHANGE_CLASS`
  declarada (`full/debug` para `change_class.critical`), nunca por debajo.

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.25 o MOS-4.4, solo con findings
`blocking-correction`. Después: MOS-3.7. Recomendada: MOS-3.7.
