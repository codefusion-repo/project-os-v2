# MOS-4.5 — Procesar el checklist QA de una feature

Operación MOSDLC `process-qa-checklist-feature` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado del checklist humano de descripción/feature.
**Para:** Cerrar el loop de QA de features sin issue ancla.
**Cómo:** Reconstruye si la feature ya pertenece a una unidad viva. Aplica
materialidad y disposiciones como MOS-4.4: corrección del mismo outcome por
MOS-3.5, follow-up por MOS-3.3 y demás disposiciones sin trabajo nuevo. Solo usa
MOS-3.8 si falta unidad y hay un outcome material con scope y criterios propios;
agrupa antes por outcome, nunca crees un issue solo por entrar a QA.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.2. Después: MOS-3.5, MOS-3.3 o MOS-3.8 según la clasificación; MOS-4.7 conserva la entrada QA compatible. Recomendada: MOS-3.8 si nace trabajo nuevo.
