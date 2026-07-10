# MOS-1.6 — Planificar el roadmap del proyecto

Operación MOSDLC `plan-project-roadmap` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: Sí (solo el GitHub write del bundle, ejecutado por el Humano PM)

**Hace:** Planifica el roadmap general del proyecto desde la documentación estable.
**Para:** Ordenar el trabajo por fases y outcomes.
**Cómo:** Draftea el roadmap issue body o el bundle de creación para el Humano PM.

**Variables**
- Requeridas: SOURCE_DOCS
- Opcionales: TARGET_REPOSITORY, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.draft_issue (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.5. Después: MOS-3.1 o MOS-3.2. Recomendada: MOS-3.1.
