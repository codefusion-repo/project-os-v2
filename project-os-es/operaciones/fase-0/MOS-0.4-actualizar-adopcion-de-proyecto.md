# MOS-0.4 — Actualizar la adopción de un proyecto

<!-- project-os-operation
canonical_code: MOS-0.4
operation_id: update-project-adoption
aliases: MOS-R.10
deprecation: none
compatibility_reason: MOS-R.10 conserva resolución histórica compatible sin duplicar este contrato operativo.
-->

Operación MOSDLC `update-project-adoption` · Fase 0 — Adaptación · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.route_prompt, +output.status_result)
- Evidencia: evidence.target_adoption
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM del route prompt con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode`
  puede satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea la actualización browser-first de un target ya adoptado a la versión vigente de kernel/catálogo.
**Para:** Mantener la adopción alineada al kernel actual.
**Cómo:** Igual que la adopción: draft browser-first en `mode.review_only` más escritura delegada por route prompt cuando hay drift terminal confirmado.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PROJECT_NAME, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Adapter browser primero:** Draftea una actualización completa de `BROWSER_CHAT.md` cuando exista drift respecto al adapter canónico; preserva sus límites read-only y draft-only y no lo exige como archivo del repo.

**Drift terminal y route prompt:** Reporta `terminal_adoption_state` y rutea únicamente el drift terminal confirmado. Draftea un route prompt que delega la actualización de adapters repo-owned al terminal agent en `mode.delegated_commit_pr`, con branch preflight, validación y aprobación PM exacta. La unidad viva es la adopción acotada del target —`TARGET_REPOSITORY`, scope exacto de adapters, rama y `evidence.target_adoption`— y no requiere un roadmap ni un issue de adopción previos; conserva las notas y constraints target-owned y nunca inventes la unidad de trabajo ni el scope.

**Entrega:** output.adoption_packet (+output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.5 o MOS-R.5. Después: MOS-0.5. Recomendada: MOS-0.5.
