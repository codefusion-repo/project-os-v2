# MOS-1.4 — Draftear la documentación de requisitos

Operación MOSDLC `draft-requirements-docs` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue, output.status_result)
- Evidencia: evidence.source_basis
- Compatibilidad: `templates/operations/26-draft-docs-from-conversation.md, templates/operations/28-draft-docs-from-description.md`
- Aprobación PM: Sí (exacta solo para la escritura del archivo)

**Hace:** Draftea documentación de requisitos funcionales y no funcionales, casos de uso e historias de usuario.
**Para:** Fijar la base documental de la Fase 1.
**Cómo:** Browser chat draftea; la escritura la aplica un terminal agent con aprobación exacta.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: DOC_TARGET, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt (+output.draft_issue, output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.2, MOS-1.3. Después: MOS-1.5. Recomendada: MOS-1.5.
