# MOS-3.3 — Draftear un follow-up issue

Operación MOSDLC `draft-follow-up-issue` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/21-draft-create-follow-up-from-review-command.md`
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea un issue de follow-up desde un issue incompleto.
**Para:** No perder trabajo pendiente cuando un issue cierra incompleto.
**Cómo:** Aísla lo faltante en un follow-up con scope propio.

**Variables**
- Requeridas: ISSUE_NUMBER
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.13 o MOS-3.31. Después: MOS-3.4. Recomendada: MOS-3.4.
