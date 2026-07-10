# MOS-3.5 — Draftear el route prompt de corrección

Operación MOSDLC `draft-correction-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el route-prompt de corrección de un PR/issue desde feedback accionable.
**Para:** Corregir sin expandir el scope original.
**Cómo:** Encapsula findings en una ruta de corrección delegada; el browser chat
puede recomendar un skill opcional e infiere
`RECOMMENDED_TERMINAL_AGENT_FAMILY` según el trabajo. La recomendación es
advisory, no autoriza nada y el feedback explícito del PM puede reemplazarla.

**Variables**
- Requeridas: ISSUE_NUMBER
- Opcionales: PR_NUMBER, OPTIONAL_SKILL, PM_FEEDBACK_HUMANO,
  PM_QUESTION_HUMANO (el skill, el feedback y la pregunta del PM son contexto;
  nunca autorizan nada). El wizard pide `PM_AUTHORIZATION_STATUS` de forma
  requerida antes de generar este route-prompt.

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.25 o MOS-4.4. Después: MOS-3.7. Recomendada: MOS-3.7.
