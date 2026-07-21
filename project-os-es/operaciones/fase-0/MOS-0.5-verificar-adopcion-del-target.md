# MOS-0.5 — Verificar la adopción del target

Operación MOSDLC `verify-target-adoption` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.status_result (+output.adoption_packet, +output.route_prompt)
- Evidencia: evidence.target_adoption
- Aprobación PM: No (read-only/draft-only)

**Hace:** Audita read-only la adopción del target separando readiness browser y terminal, y draftea reparación cuando corresponde.
**Para:** Confirmar que el target puede operar con seguridad.
**Cómo:** Lee adapters y evidencia del target sin escribir; audita browser y terminal por separado.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Auditoría separada:** Reporta `browser_adoption_state` y `terminal_adoption_state` de forma independiente. Cuando no se suministre el contenido del adapter browser, no declares su readiness: márcalo como no suministrado y devuelve `status.needs_context`. Devuelve GO global solo cuando ambas superficies aplicables estén listas.

**Reparación:** Cuando la auditoría detecte que el adapter browser falta o está desactualizado, incluye un draft corregido en el adoption packet. Cuando los findings requieran una corrección terminal, draftea un route prompt que delega la reparación de adapters repo-owned al terminal agent en `mode.delegated_commit_pr`, con branch preflight, validación y aprobación PM exacta. La unidad viva es la adopción acotada del target —`TARGET_REPOSITORY`, scope exacto de adapters, rama y `evidence.target_adoption`— y no requiere un roadmap ni un issue de adopción previos; nunca inventes la unidad de trabajo ni el scope.

**Entrega:** output.status_result (+output.adoption_packet, +output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.2, MOS-0.3 o MOS-0.4. Después: MOS-1.1 o MOS-1.10 según el proyecto. Recomendada: MOS-R.2.
