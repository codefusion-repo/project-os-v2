# MOS-4.5 — Procesar el checklist QA de una feature

Operación MOSDLC `process-qa-checklist-feature` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/30-process-human-qa-results.md`
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado del checklist humano de descripción/feature.
**Para:** Cerrar el loop de QA de features sin issue ancla.
**Cómo:** Clasifica hallazgos hacia issue nuevo, corrección o no-op.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.2. Después: MOS-3.8 o MOS-4.7. Recomendada: MOS-3.8 si nace trabajo nuevo.
