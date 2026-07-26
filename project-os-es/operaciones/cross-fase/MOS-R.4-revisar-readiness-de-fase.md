# MOS-R.4 — Revisar readiness de fase

Operación MOSDLC `review-phase-readiness` · Transversal · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (review advisory; no cambia de fase)

**Hace:** Revisa readiness advisory antes de mover trabajo entre fases MOSDLC.
**Para:** Identificar evidencia, blockers y decisiones faltantes antes de avanzar.
**Cómo:** Contrasta fase actual, fase objetivo y estado vivo sin ejecutar transición.

**Variables**
- Requeridas: ninguna
- Opcionales: TARGET_PHASE, READINESS_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** la fase actual, el repositorio, el issue, el PR y el
roadmap son metadata derivada. `TARGET_PHASE` permanece como input porque es
una decisión humana: declara a qué fase quiere mover el PM el trabajo y la
evidencia viva no puede sustituirla. `READINESS_SOURCE` es el único locator
primario y se pide solo cuando la invocación actual no identifica ya la fuente;
desde él se reconstruyen la fase actual y las relaciones verificables.

**Entrega:** output.status_result. Ante evidencia de fase faltante o transición ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cierre o revisión de una fase. Después: operación segura de la fase objetivo; MOS-R.3 si falta decisión PM; MOS-R.2 si falta routing. Recomendada: operación segura de la fase objetivo cuando esté lista.
