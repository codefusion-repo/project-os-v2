# MOS-4.7 — Draftear un follow-up desde QA

Operación MOSDLC `draft-follow-up-from-qa` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/21-draft-create-follow-up-from-review-command.md`
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea follow-up desde resultados de QA.
**Para:** Diferir hallazgos de QA no bloqueantes con trazabilidad.
**Cómo:** Bundle de creación de follow-up para el Humano PM.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.4, MOS-4.5 o MOS-4.6. Después: MOS-3.4 cuando se priorice. Recomendada: MOS-3.4.
