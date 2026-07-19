# MOS-0.2 — Iniciar un proyecto nuevo

Operación MOSDLC `bootstrap-new-project` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.pm_command_bundle, +output.route_prompt, +output.status_result)
- Evidencia: evidence.target_adoption
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM del route prompt con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode`
  puede satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea el bootstrap browser-first de un repo nuevo: primero un adapter browser completo, luego la creación del roadmap y la ruta terminal cuando existan.
**Para:** Iniciar un proyecto nuevo bajo Project OS sin bloquear el arranque en la falta de roadmap.
**Cómo:** Browser chat resuelve el kernel en `mode.review_only` y draftea; el Humano PM aplica el adapter browser, crea el roadmap y entrega el route prompt.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PROJECT_NAME, DESCRIPTION, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, ADOPTION_ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Adapter browser primero:** Produce siempre un draft completo de `BROWSER_CHAT.md` aplicable por el PM aunque el proyecto no tenga roadmap. Es un artefacto PM-applied y no tiene por qué guardarse dentro del repo target. Conserva sus límites read-only y draft-only y separa `browser_adoption_state` de `terminal_adoption_state`.

**Roadmap y ruta terminal:** Declara `roadmap_state`. Cuando no exista un roadmap canónico, declara `roadmap_state=missing`, draftea un `output.pm_command_bundle` copy-safe para crearlo, no inventes su número y no rellenes `{{#ROADMAP_ISSUE}}` con placeholders durables; no generes todavía un route prompt terminal ejecutable. Después de que exista el roadmap vivo, usa su número verificado y una unidad de trabajo viva (`ADOPTION_ISSUE_NUMBER`) para draftear el route prompt que delega la escritura de adapters repo-owned al terminal agent en `mode.delegated_commit_pr`, con branch preflight, validación y aprobación PM exacta; el route prompt referencia la unidad viva y no restata el cuerpo del issue, y nunca inventes la unidad de trabajo.

**Entrega:** output.adoption_packet (+output.pm_command_bundle, +output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.1. Después: MOS-0.5. Recomendada: MOS-0.5.
