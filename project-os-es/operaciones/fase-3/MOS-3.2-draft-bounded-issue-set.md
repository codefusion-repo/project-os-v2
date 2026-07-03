# MOS-3.2 — Draftear un set acotado de issues

Operación MOSDLC `draft-bounded-issue-set` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/29-draft-bounded-roadmap-issues-command.md`
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea un conjunto acotado de issues desde trazabilidad viva y roadmap.
**Para:** Planificar lotes de trabajo con límite explícito.
**Cómo:** Exige un límite y draftea un bundle por outcome.

**Variables**
- Requeridas: ROADMAP_ISSUE
- Opcionales: ISSUE_COUNT_LIMIT, SCOPE_LIMIT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.6. Después: MOS-3.4 por cada issue aprobado. Recomendada: MOS-3.4.
