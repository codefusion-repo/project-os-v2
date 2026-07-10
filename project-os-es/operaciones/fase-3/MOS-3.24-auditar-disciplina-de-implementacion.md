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
- Opcionales: PATH_SCOPE, FOCUS, ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.review_result (+output.draft_issue). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-3.26. Recomendada: MOS-3.26.
