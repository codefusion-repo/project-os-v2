# MOS-1.12 — Actualizar el roadmap de un proyecto existente

Operación MOSDLC `update-roadmap-existing` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/27-draft-roadmap-from-docs.md`
- Aprobación PM: Sí (solo el GitHub write del bundle, ejecutado por el Humano PM)

**Hace:** Actualiza o planifica el roadmap general de un proyecto existente.
**Para:** Dar dirección por fases a proyectos adoptados.
**Cómo:** Draftea creación o actualización del roadmap issue para el Humano PM.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: SOURCE_DOCS, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.draft_issue (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.11. Después: MOS-3.1. Recomendada: MOS-3.1.
