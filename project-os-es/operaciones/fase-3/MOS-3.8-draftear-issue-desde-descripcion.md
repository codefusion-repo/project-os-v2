# MOS-3.8 — Draftear un issue desde una descripción

Operación MOSDLC `draft-issue-from-description` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea un issue desde una descripción y verifica que no afecte roadmap ni documentación.
**Para:** Capturar trabajo nuevo sin romper la planificación vigente.
**Cómo:** Convierte la descripción en bundle y chequea impacto contra roadmap y docs.

**Variables**
- Requeridas: DESCRIPTION
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.7. Después: MOS-3.4. Recomendada: MOS-3.4.
