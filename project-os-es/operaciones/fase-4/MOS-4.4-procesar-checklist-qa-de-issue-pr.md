# MOS-4.4 — Procesar el checklist QA de un issue/PR

Operación MOSDLC `process-qa-checklist-issue-pr` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/30-process-human-qa-results.md`
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado del checklist humano de issue/PR.
**Para:** Convertir QA humano en corrección, follow-up o avance.
**Cómo:** Clasifica bloqueantes y no bloqueantes sin ejecutar nada.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.1. Después: MOS-4.8, MOS-4.7 o MOS-3.7. Recomendada: MOS-4.8 para bloqueantes.
