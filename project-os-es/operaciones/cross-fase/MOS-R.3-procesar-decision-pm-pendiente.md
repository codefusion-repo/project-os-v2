# MOS-R.3 — Procesar una decisión PM pendiente

Operación MOSDLC `process-needs-pm-decision` · Transversal · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/36-process-needs-pm-decision.md`
- Aprobación PM: No (clasifica la decisión; no ejecuta ni autoaprueba)

**Hace:** Procesa un `status.needs_pm_decision` de una operación origen hacia una salida segura.
**Para:** Resolver decisiones PM pendientes con variables claras y target-agnostic.
**Cómo:** Clasifica entre contexto faltante, elegir ruta, aprobar corrección, crear follow-up, detener/no-op, volver a origen o pedir más evidencia.

**Variables**
- Requeridas: DECISION_SOURCE, DECISION_CONTEXT, DECISION_QUESTION, DECISION_OPTIONS
- Opcionales: OPTIONS_IMPACT, PM_DECISION, PM_CLARIFICATION, ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- `PM_DECISION` decide solo el punto explícito; nunca autoriza escrituras, rutas futuras ni mutaciones.
- `PM_CLARIFICATION` y `PM_QUESTION_HUMANO` pueden acotar la pregunta, pero no reemplazan evidencia requerida.
- Si la evidencia contiene secretos o valores con pinta de secreto, fail-closed a `status.blocked` y pide una base redactada.
- No ejecutes rutas, no edites archivos/GitHub y no cruces los límites de la operación origen.

**Entrega:** output.status_result, con route prompt solo para corrección acotada y draft issue/bundle solo para follow-up. Ante evidencia, alcance o decisión ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier operación con `status.needs_pm_decision`. Después: vuelve a DECISION_SOURCE si basta; MOS-3.5 para corrección; MOS-3.3 para follow-up; MOS-R.2 si solo falta routing. Recomendada: volver a DECISION_SOURCE cuando sea seguro.
