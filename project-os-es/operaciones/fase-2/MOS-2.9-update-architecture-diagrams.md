# MOS-2.9 — Actualizar diagramas de arquitectura

Operación MOSDLC `update-architecture-diagrams` · Fase 2 — Diseño · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidencia: evidence.source_basis
- Compatibilidad: `templates/operations/26-draft-docs-from-conversation.md, templates/operations/28-draft-docs-from-description.md`
- Aprobación PM: Sí (exacta solo para la escritura del archivo)

**Hace:** Actualiza o crea diagramas de arquitectura desde la documentación existente y la Fase 1.
**Para:** Sostener la Fase 2 con documentación de diseño estable.
**Cómo:** Browser chat draftea; la escritura la aplica un terminal agent con aprobación exacta.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: SOURCE_DOCS, DOC_TARGET, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt (+output.draft_issue, output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-2.8. Después: MOS-2.14. Recomendada: MOS-2.14.
