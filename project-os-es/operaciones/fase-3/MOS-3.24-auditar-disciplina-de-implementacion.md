# MOS-3.24 — Auditar disciplina de implementación

Operación MOSDLC `audit-implementation-discipline` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.implementation_discipline_audit · mode.review_only · output.review_result (+output.draft_issue)
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Audita gaps de disciplina de implementación contra boundary.implementation_discipline.
**Para:** Detectar deuda de disciplina con evidencia de archivos y líneas.
**Cómo:** Auditoría read-only con findings y drafts de follow-up.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PATH_SCOPE, FOCUS, AUDIT_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** `TARGET_REPOSITORY`, `PATH_SCOPE`, `FOCUS` y
`AUDIT_SCOPE` representan niveles distintos de scope, así que su precedencia es
explícita: (1) usa la fuente que la invocación actual ya seleccionó; (2) si
falta, un único locator primario proporcionado —`AUDIT_SCOPE` acepta el issue o
el PR que acota la auditoría; (3) deriva desde él el resto de la metadata y del
scope; (4) devuelve la decisión al PM solo cuando varias interpretaciones
materiales sean igualmente válidas. `TARGET_REPOSITORY` se conserva porque una
auditoría deliberadamente repo-wide no tiene otra fuente de alcance; el issue y
el PR nunca se piden juntos.

**Entrega:** output.review_result (+output.draft_issue). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-3.14. Recomendada: MOS-3.14.
