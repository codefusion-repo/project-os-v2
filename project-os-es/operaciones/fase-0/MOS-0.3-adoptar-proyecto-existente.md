# MOS-0.3 — Adoptar un proyecto existente

Operación MOSDLC `adopt-existing-project` · Fase 0 — Adaptación · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.route_prompt, +output.status_result)
- Evidencia: evidence.target_adoption
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM del route prompt con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode`
  puede satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea la adopción browser-first de un repo existente: adapter browser completo y auditoría del estado terminal.
**Para:** Adoptar un proyecto existente como target.
**Cómo:** Browser chat resuelve el kernel en `mode.review_only`, draftea el adapter browser y audita los adapters terminal; la escritura la delega el route prompt.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PROJECT_NAME, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, ADOPTION_ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Adapter browser primero:** Produce siempre un draft completo de `BROWSER_CHAT.md` aplicable por el PM. Es PM-applied y no tiene por qué guardarse dentro del repo target; conserva sus límites read-only y draft-only.

**Adoption packet y route prompt:** Reporta por separado `browser_adoption_state` y `terminal_adoption_state`. Produce el adoption packet draft-only y, cuando exista una unidad de trabajo viva (`ADOPTION_ISSUE_NUMBER`), un route prompt que delega el bootstrap de adapters repo-owned al terminal agent en `mode.delegated_commit_pr`, con branch preflight, validación y aprobación PM exacta. El route prompt referencia la unidad viva y no restata el cuerpo del issue; nunca inventes la unidad de trabajo.

**Entrega:** output.adoption_packet (+output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.1. Después: MOS-0.5. Recomendada: MOS-0.5.
