# MOS-R.3 — Procesar una decisión PM pendiente

Operación MOSDLC `process-needs-pm-decision` · Transversal · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle, output.draft_issue)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (clasifica la decisión; no ejecuta ni autoaprueba)

**Hace:** Procesa una decisión PM pendiente desde evidencia viva hacia una salida segura.
**Para:** Resolver decisiones PM pendientes con variables claras y target-agnostic.
**Cómo:** Reconstruye el punto pendiente desde `DECISION_SOURCE`, deriva de ahí el issue, el PR y sus relaciones, y aplica `rule.precedencia_decision_pm`: valida la decisión vigente o presenta opciones con impacto, tradeoffs, recomendación y la pregunta exacta.

**Variables**
- Requeridas: DECISION_SOURCE, PM_DECISION_ALREADY_MADE
- Opcionales: DECISION_OPTIONS, PM_DECISION

**Cuida**
- `DECISION_SOURCE` es el único locator primario. El issue, el PR y sus relaciones son metadata derivada: reconstrúyelos desde esa fuente y la evidencia viva, muéstralos resueltos en la salida y devuelve `status.needs_context` solo si no puedes derivarlos inequívocamente durante la ejecución.
- Cuando la fuente identifique un issue y un PR, verifica que pertenezcan a un flujo relacionado; si no están relacionados, falla cerrado en vez de inventar la relación.
- `PM_DECISION_ALREADY_MADE` es `true` o `false`: con `true`, `PM_DECISION` es obligatoria; con `false`, debe quedar vacía.
- Si `PM_DECISION_ALREADY_MADE=false`, usa `DECISION_OPTIONS` cuando existan o deriva un conjunto acotado desde evidencia viva; entrega impacto, tradeoffs, riesgos, reversibilidad, recomendación y la pregunta exacta.
- Forma una `decision_key` material con proyecto o target, unidad de trabajo, acción material y alcance exacto. Verifica fuente y orden temporal como evidencia separada de cada decisión; solo compara decisiones de la misma clave material. Una aprobación de Release no autoriza cierre, settings, publicación, transición ni otra acción separada.
- Una decisión posterior, explícita, exacta y aplicable de fuente viva verificable se vuelve `current_pm_decision`; conserva como `superseded_decision` únicamente la decisión anterior más reciente que también sea exacta y suficiente. Si varias candidatas anteriores exactas y suficientes empatan en el mayor orden cronológico elegible, no elijas por orden de entrada: deja `superseded_decision` sin resolver, conserva la `current_pm_decision` ya resuelta y devuelve `status.needs_pm_decision`.
- Ante drift con evidencia durable anterior, identifica la fuente contradictoria en `required_traceability_follow_up` sin reescribir la historia. Ese drift no bloquea por sí solo una acción cuyos `remaining_gates` estén satisfechos.
- Entrega siempre `decision_key`, `superseded_decision`, `current_pm_decision`, `required_traceability_follow_up`, `remaining_gates`, `resulting_status` y `safe_return_operation`.
- Conserva `superseded_decision` y `current_pm_decision` cuando una decisión vigente ya se resolvió aunque un `remaining_gate` independiente produzca bloqueo. Usa `status.resolved` solo con decisión vigente exacta, supersesión inequívoca cuando aplique, salida soportada y demás gates satisfechos. Usa `status.needs_pm_decision` si la vigencia, clave material o selección de `superseded_decision` es ambigua; `status.needs_context` si falta fuente, procedencia, orden o relación verificable; y `status.blocked` para mutación con aprobación no verificable o exacta insuficiente, actor/mode/superficie/permisos incompatibles, secretos, validación fallida, límite no delegable o extensión a otra acción.
- `PM_DECISION` decide solo el punto explícito; nunca autoriza escrituras, implementación, merge, cierre, tag, release, deploy, rutas futuras ni otras mutaciones, y nunca relaja límites no delegables ni aprobaciones separadas.
- Si la evidencia contiene secretos o valores con pinta de secreto, fail-closed a `status.blocked` y pide una base redactada.
- No ejecutes rutas, no edites archivos/GitHub y no cruces los límites de la operación origen.

**Entrega:** output.status_result con la forma canónica de resolución de decisión; route prompt solo para corrección acotada y draft issue/bundle solo para follow-up de trazabilidad. Si la decisión vigente y los gates bastan, vuelve a la operación origen; si faltan opciones, presenta la recomendación sin ejecutar ni autoaprobar ninguna.

**Conexiones:** Antes: cualquier operación con `status.needs_pm_decision`. Después: vuelve a DECISION_SOURCE si basta; MOS-3.5 para corrección; MOS-3.3 para follow-up; MOS-R.2 si solo falta routing. Recomendada: volver a DECISION_SOURCE cuando sea seguro.
