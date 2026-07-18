# MOS-3.4 — Draftear el route prompt de implementación

Operación MOSDLC `draft-implementation-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode` puede
  satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea el route-prompt para delegar la implementación de un issue a un terminal agent.
**Para:** Rutear implementación con scope, modo y evidencia correctos.
**Cómo:** Usa un bootloader compacto e issue-referential: el detalle permanece
en el issue o PR vivo y sus comentarios, no en el route prompt. El browser chat
puede recomendar un skill opcional e infiere `RECOMMENDED_TERMINAL_AGENT_FAMILY`
según el trabajo. La recomendación es advisory, no autoriza nada y el feedback
explícito del PM puede reemplazarla.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: ISSUE_NUMBER, ROADMAP_ISSUE, OPTIONAL_SKILL, HYDRATION_LEVEL,
  PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el skill, el nivel, el feedback y la
  pregunta del PM son contexto; nunca autorizan nada). `HYDRATION_LEVEL` acepta
  `minimal`, `compact` (valor predeterminado) o `full/debug`; controla el
  contenido hidratado del resolver y aplica la visibilidad PM-facing contractual
  del recibo sin alterar el recibo interno ni `context_plan`. El wizard pide `PM_AUTHORIZATION_STATUS` de forma
  requerida y precarga `HYDRATION_LEVEL=compact` antes de generar este
  route-prompt.

**Contrato de autorización:** El browser chat solo draftea y nunca puede
autoasignar, completar, cambiar ni inferir `granted`. Un route prompt en draft,
no entregado por el PM o con `PM_AUTHORIZATION_STATUS` en `pending` no autoriza
escrituras. Cuando el PM entrega el route prompt con
`PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode`, esa entrega
satisface `evidence.pm_approval` únicamente para el repositorio, workflow,
modo, rama y scope declarados. El agente receptor debe verificar esa
coincidencia y la evidencia restante; un estado ausente, desconocido o
inferido falla cerrado. No se exige un comentario adicional de GitHub como
condición universal, y la aprobación no cubre merge, cierre, tags, releases,
deploys, settings ni otra acción fuera del modo declarado.

**Comprobación de conformidad:** Antes de entregar, compara la salida con
`project-os-es/templates/route-prompt.md`. Comprímela si repite detalle del
issue, PR o comentarios; conserva una referencia a la evidencia viva en vez de
copiar cuerpos, acceptance criteria, source basis, checklists o pasos de
implementación. Entrega solo un bloque estándar de variables, `SCOPE` de 1-3
líneas y una única instrucción concreta posterior. Si no puede producir esa
forma, falla cerrado con `output.status_result`.

**QA manual reproducible:** Usa un issue largo con comentarios extensos. Verifica
que el route prompt conserva solo metadata, scope breve, out-of-scope breve y
una instrucción concreta; que `SCOPE` tiene 1-3 líneas; que no hay secciones
copiadas; y que instruye al agente receptor a leer evidencia viva.

**Entrega:** output.route_prompt. Ante evidencia, alcance, aprobación o forma conforme faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.1, MOS-3.2 o MOS-3.8. Después: MOS-3.7 tras el PR. Recomendada: MOS-3.7.
