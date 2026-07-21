# MOS-0.2 — Iniciar un proyecto nuevo

Operación MOSDLC `bootstrap-new-project` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.pm_command_bundle, +output.route_prompt, +output.status_result)
- Evidencia: evidence.target_adoption
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM del route prompt con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode`
  puede satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea el bootstrap browser-first de un repo nuevo: primero un adapter browser completo, luego la ruta terminal delegada de los adapters repo-owned.
**Para:** Iniciar un proyecto nuevo bajo Project OS sin exigir un roadmap ni un issue previos.
**Cómo:** Browser chat resuelve el kernel en `mode.review_only` y draftea; el Humano PM aplica el adapter browser y entrega el route prompt.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PROJECT_NAME, DESCRIPTION, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Adapter browser primero:** Produce siempre un draft completo de `BROWSER_CHAT.md` aplicable por el PM aunque el proyecto no tenga roadmap. Es un artefacto PM-applied y no tiene por qué guardarse dentro del repo target. Conserva sus límites read-only y draft-only y separa `browser_adoption_state` de `terminal_adoption_state`.

**Unidad de trabajo y ruta terminal:** La unidad viva de `workflow.target_adoption` es la adopción acotada del target: `TARGET_REPOSITORY`, el scope exacto de adapters repo-owned, la rama de trabajo, `evidence.target_adoption`, branch preflight, validación y la entrega PM con aprobación exacta. No exige crear antes un roadmap ni un issue de adopción. Draftea el route prompt que delega la escritura de adapters repo-owned al terminal agent en `mode.delegated_commit_pr` con esos gates; nunca inventes la unidad de trabajo ni el scope.

**Roadmap como evidencia opcional:** Declara `roadmap_state`. Cuando exista un roadmap canónico vivo, úsalo como evidencia y contexto; cuando falte, declara `roadmap_state=missing` y draftea un `output.pm_command_bundle` copy-safe para crearlo, pero no inventes su número y no bloquees por ello la adopción ni la ruta terminal. No almacenes números de roadmap, issue, PR, ramas, commits ni validaciones como configuración durable de los adapters.

**Entrega:** output.adoption_packet (+output.pm_command_bundle, +output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.1. Después: MOS-0.5. Recomendada: MOS-0.5.
