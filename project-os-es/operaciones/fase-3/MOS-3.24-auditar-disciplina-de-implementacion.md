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
- Requeridas: — (ninguna)
- Opcionales: TARGET_REPOSITORY, AUDIT_SCOPE, PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Locators alternativos y constraints humanos:** `TARGET_REPOSITORY` y
`AUDIT_SCOPE` son locators alternativos, nunca requisitos acumulativos. Primero
reutiliza una fuente inequívoca ya seleccionada. Sin ella, una auditoría
deliberadamente repo-wide pide `TARGET_REPOSITORY`; una auditoría acotada pide
`AUDIT_SCOPE` —issue o PR— y deriva desde esa fuente el repositorio y las demás
relaciones verificables. `PATH_SCOPE` y `FOCUS` son constraints humanos
opcionales, no metadata derivada. Si no existe fuente suficiente, o ambos
locators se declaran y resuelven targets incompatibles, falla cerrado con
`status.needs_context`; nunca elige un target ni mezcla evidencias.

**Entrega:** output.review_result (+output.draft_issue). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-3.14. Recomendada: MOS-3.14.
