# MOS-3.27 — Revisar el estado del proyecto

Operación MOSDLC `review-project-state` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/05-review-project-state-and-misalignment.md`
- Aprobación PM: No (read-only)

**Hace:** Revisa estado del proyecto y desalineaciones respecto a la documentación.
**Para:** Detectar drift entre docs, roadmap y realidad del repo.
**Cómo:** Usa decisiones PM y docs fijos como verdad principal.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-3.1, MOS-3.3 o MOS-R.9. Recomendada: MOS-R.9 si el drift es documental.
