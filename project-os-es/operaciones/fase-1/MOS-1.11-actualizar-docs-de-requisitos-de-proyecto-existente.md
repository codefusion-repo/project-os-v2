# MOS-1.11 — Actualizar docs de requisitos de un proyecto existente

Operación MOSDLC `update-requirements-docs-existing` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidencia: evidence.source_basis
- Aprobación PM: Sí (exacta solo para la escritura del archivo)

**Hace:** Actualiza o crea la documentación de requisitos de un proyecto existente.
**Para:** Cerrar el gap documental de proyectos adoptados.
**Cómo:** Igual que MOS-1.4 pero partiendo de requisitos extraídos del proyecto.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: DOC_TARGET, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt (+output.draft_issue, output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.10. Después: MOS-1.12. Recomendada: MOS-1.12.
