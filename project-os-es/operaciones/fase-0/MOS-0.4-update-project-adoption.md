# MOS-0.4 — Actualizar la adopción de un proyecto

Operación MOSDLC `update-project-adoption` · Fase 0 — Adaptación · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidencia: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- Compatibilidad: `templates/operations/23-upgrade-kernel-adoption-in-target.md`
- Aprobación PM: Sí (exacta para escritura en el target)

**Hace:** Refresca adapters de un target ya adoptado a la versión vigente de kernel/catálogo.
**Para:** Mantener la adopción alineada al kernel actual.
**Cómo:** Igual que la adopción: draft más escritura delegada con aprobación exacta.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.adoption_packet (+output.route_prompt). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.5 o MOS-R.5. Después: MOS-0.5. Recomendada: MOS-0.5.
