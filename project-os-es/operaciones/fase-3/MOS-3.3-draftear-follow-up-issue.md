# MOS-3.3 — Draftear un follow-up issue

Operación MOSDLC `draft-follow-up-issue` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea un follow-up desde cualquier fuente viva: un issue
incompleto, un review, una auditoría de disciplina o una revisión de seguridad.
**Para:** Diferir con trazabilidad trabajo pendiente y hallazgos no bloqueantes.
**Cómo:** Aísla lo faltante o diferido en un follow-up con scope propio; la
fuente viva queda referenciada, no copiada.

**Variables**
- Requeridas: FOLLOW_UP_SOURCE (issue incompleto, review, resultado de
  auditoría o de revisión de seguridad, u otro registro vivo)
- Opcionales: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO
  (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.14, MOS-3.25 o MOS-3.31.
Después: MOS-3.4 cuando se priorice. Recomendada: MOS-3.4.
