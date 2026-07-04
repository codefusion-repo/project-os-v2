# MOS-0.3 — Adoptar un proyecto existente

Operación MOSDLC `adopt-existing-project` · Fase 0 — Adaptación · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidencia: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- Compatibilidad: `templates/operations/01-adopt-project-os-in-existing-target.md`
- Aprobación PM: Sí (exacta para escritura en el target)

**Hace:** Prepara un repositorio existente para operar con Project OS (adapters y checklist).
**Para:** Adoptar un proyecto existente como target.
**Cómo:** Browser chat draftea; el terminal agent escribe adapters solo con aprobación exacta.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.adoption_packet (+output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.1. Después: MOS-0.5. Recomendada: MOS-0.5.
