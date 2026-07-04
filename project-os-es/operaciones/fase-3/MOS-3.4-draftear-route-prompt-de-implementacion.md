# MOS-3.4 — Draftear el route prompt de implementación

Operación MOSDLC `draft-implementation-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/07-draft-issue-implementation-route-prompt.md`
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el route-prompt para delegar la implementación de un issue a un terminal agent.
**Para:** Rutear implementación con scope, modo y evidencia correctos.
**Cómo:** Bootloader compacto; el detalle vive en el issue; nunca autoriza por sí mismo.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: ISSUE_NUMBER, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.1, MOS-3.2 o MOS-3.8. Después: MOS-3.7 tras el PR. Recomendada: MOS-3.7.
