# MOS-3.22 — Procesar la entrega de un asset de video

Operación MOSDLC `process-video-asset-delivery` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/32-process-design-asset-delivery.md`
- Aprobación PM: No (draft-only)

**Hace:** Procesa la entrega de un asset de video y la mapea a tareas técnicas o drafts.
**Para:** Integrar assets recibidos al ciclo de desarrollo.
**Cómo:** Clasifica la entrega hacia issue, corrección o follow-up.

**Variables**
- Requeridas: DESIGN_DELIVERY
- Opcionales: ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.18. Después: MOS-3.4, MOS-3.5 o MOS-3.3. Recomendada: MOS-3.4.
