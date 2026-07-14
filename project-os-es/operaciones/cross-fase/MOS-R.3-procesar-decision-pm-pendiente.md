# MOS-R.3 — Procesar una decisión PM pendiente

Operación MOSDLC `process-needs-pm-decision` · Transversal · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (clasifica la decisión; no ejecuta ni autoaprueba)

**Hace:** Procesa una decisión PM pendiente desde evidencia viva hacia una salida segura.
**Para:** Resolver decisiones PM pendientes con variables claras y target-agnostic.
**Cómo:** Lee el issue y/o PR identificado por sus números, reconstruye el punto pendiente desde `DECISION_SOURCE` y valida una decisión ya tomada o presenta opciones con impacto, tradeoffs, recomendación y la pregunta exacta.

**Variables**
- Requeridas: DECISION_SOURCE, PM_DECISION_ALREADY_MADE
- Opcionales: ISSUE_NUMBER, PR_NUMBER, DECISION_OPTIONS, PM_DECISION

**Cuida**
- `ISSUE_NUMBER` y `PR_NUMBER` reciben solo números positivos; al menos una debe estar presente. Si ambas faltan, devuelve `status.needs_context`.
- Pueden estar presentes ambas referencias cuando pertenecen a un flujo relacionado verificable; si no están relacionadas, falla cerrado.
- `PM_DECISION_ALREADY_MADE` es `true` o `false`: con `true`, `PM_DECISION` es obligatoria; con `false`, debe quedar vacía.
- Si `PM_DECISION_ALREADY_MADE=false`, usa `DECISION_OPTIONS` cuando existan o deriva un conjunto acotado desde evidencia viva; entrega impacto, tradeoffs, riesgos, reversibilidad, recomendación y la pregunta exacta.
- `PM_DECISION` decide solo el punto explícito; nunca autoriza escrituras, implementación, merge, cierre, tag, release, deploy, rutas futuras ni otras mutaciones.
- Ante decisión ambigua, evidencia faltante o contradicción con evidencia durable, falla cerrado con `status.needs_pm_decision` o `status.needs_context`, según corresponda.
- Si la evidencia contiene secretos o valores con pinta de secreto, fail-closed a `status.blocked` y pide una base redactada.
- No ejecutes rutas, no edites archivos/GitHub y no cruces los límites de la operación origen.

**Entrega:** output.status_result, con route prompt solo para corrección acotada y draft issue/bundle solo para follow-up. Si la decisión ya tomada es suficiente, vuelve a la operación origen; si faltan opciones, presenta la recomendación sin ejecutar ni autoaprobar ninguna.

**Conexiones:** Antes: cualquier operación con `status.needs_pm_decision`. Después: vuelve a DECISION_SOURCE si basta; MOS-3.5 para corrección; MOS-3.3 para follow-up; MOS-R.2 si solo falta routing. Recomendada: volver a DECISION_SOURCE cuando sea seguro.
