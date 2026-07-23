# MOS-3.4 — Draftear el route prompt de implementación

Operación MOSDLC `draft-implementation-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode` puede
  satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea el route-prompt para delegar la implementación de una unidad
viva a un terminal agent.
**Para:** Rutear implementación con unidad, clase, scope, modo y evidencia correctos.
**Cómo:** Usa un bootloader compacto referenciado a la unidad viva: el detalle
permanece en la unidad y sus registros (issue o PR y comentarios cuando el
target usa GitHub; change request, registro del target o instrucción PM exacta
cuando no), no en el route prompt. Completa `WORK_UNIT` con esa referencia viva
y declara `CHANGE_CLASS` según el contrato `proportionality.change_class`: para
un `change_class.small` admitido por la política del target, la instrucción PM
exacta puede ser la unidad viva sin issue. Al derivar `SCOPE` y `OUT_OF_SCOPE`
interpreta la unidad por intención: solo autorización, identidad, hard
constraints, scope, out of scope y seguridad son literales; ejemplos, nombres
tentativos y propuestas de implementación son advisory. El browser chat puede
recomendar un skill opcional e infiere `RECOMMENDED_TERMINAL_AGENT_FAMILY`
según el trabajo. La recomendación es advisory, no autoriza nada y el feedback
explícito del PM puede reemplazarla.

**Variables**
- Requeridas: CHANGE_CLASS
- Opcionales: WORK_UNIT, ROADMAP_ISSUE, OPTIONAL_SKILL, HYDRATION_LEVEL,
  PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (la unidad, el skill, el nivel, el
  feedback y la pregunta del PM son contexto; nunca autorizan nada).
  `CHANGE_CLASS` declara la clase del contrato `proportionality.change_class`.
  `HYDRATION_LEVEL` acepta `minimal`, `compact` o `full/debug`; controla el
  contenido hidratado del resolver y aplica la visibilidad PM-facing contractual
  del recibo sin alterar el recibo interno ni `context_plan`. El wizard pide
  `PM_AUTHORIZATION_STATUS` de forma requerida y precarga `HYDRATION_LEVEL` con la
  densidad contractual de la `CHANGE_CLASS` declarada (`full/debug` para
  `change_class.critical`), nunca por debajo.

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
`project-os-es/templates/route-prompt.md`. Comprímela si repite detalle de la
unidad viva o sus registros; conserva una referencia a la evidencia viva en vez
de copiar cuerpos, acceptance criteria, source basis, checklists o pasos de
implementación. Entrega solo un bloque estándar de variables, `SCOPE` de 1-3
líneas y una única instrucción concreta posterior. Si no puede producir esa
forma, falla cerrado con `output.status_result`.

**QA manual reproducible:** Usa una unidad viva con registros extensos. Verifica
que el route prompt conserva solo metadata, referencia viva, clase declarada,
scope breve, out-of-scope breve y una instrucción concreta; que `SCOPE` tiene
1-3 líneas; que no hay secciones copiadas; y que instruye al agente receptor a
leer evidencia viva.

**Entrega:** output.route_prompt. Ante evidencia, alcance, aprobación o forma conforme faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.7, MOS-3.1, MOS-3.2 o MOS-3.8, o una instrucción
PM exacta como unidad viva de un `change_class.small`. Después: MOS-3.7 tras el
PR. Recomendada: MOS-3.7.
