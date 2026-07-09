# MOS-1.8 — Actualizar docs y roadmap con un requerimiento

Operación MOSDLC `update-docs-roadmap-with-requirement` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/27-draft-roadmap-from-docs.md, legacy-project-os/templates/operations/28-draft-docs-from-description.md`
- Aprobación PM: Sí (exacta solo para la escritura del archivo)

**Hace:** Actualiza documentación y roadmap con un requerimiento aceptado.
**Para:** Mantener docs y roadmap como única verdad de alcance.
**Cómo:** Draftea cambios de docs y bundle de roadmap; escritura con aprobación exacta.

**Variables**
- Requeridas: DESCRIPTION
- Opcionales: ROADMAP_ISSUE, DOC_TARGET, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.7. Después: MOS-3.1. Recomendada: MOS-3.1.
