# MOS-3.5 — Draftear el route prompt de corrección

Operación MOSDLC `draft-correction-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el route-prompt de corrección de un PR/issue desde findings
con disposición `blocking-correction`.
**Para:** Corregir solo incumplimientos materiales sin expandir el scope original.
**Cómo:** Encapsula únicamente los findings `blocking-correction` en una ruta de
corrección delegada; los `non-blocking-follow-up` se difieren a MOS-3.3 y
`preference`, `accepted-risk` e `invalid-finding` no fuerzan cambios. El browser chat
puede recomendar un skill opcional e infiere
`RECOMMENDED_TERMINAL_AGENT_FAMILY` según el trabajo. La recomendación es
advisory, no autoriza nada y el feedback explícito del PM puede reemplazarla.

**Variables**
- Requeridas: ISSUE_NUMBER
- Opcionales: PR_NUMBER, OPTIONAL_SKILL, HYDRATION_LEVEL, PM_FEEDBACK_HUMANO,
  PM_QUESTION_HUMANO (el skill, el nivel, el feedback y la pregunta del PM son
  contexto; nunca autorizan nada). `HYDRATION_LEVEL` acepta `minimal`,
  `compact` (valor predeterminado) o `full/debug`; controla el contenido
  hidratado del resolver y aplica la visibilidad PM-facing contractual del
  recibo sin alterar el recibo interno ni `context_plan`. El wizard pide `PM_AUTHORIZATION_STATUS` de forma requerida y
  precarga `HYDRATION_LEVEL=compact` antes de generar este route-prompt.

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.25 o MOS-4.4, solo con findings
`blocking-correction`. Después: MOS-3.7. Recomendada: MOS-3.7.
