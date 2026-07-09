# MOS-R.10 — Actualizar catálogo de adapters del target

Operación MOSDLC `update-target-adapters-catalog` · Fase 0 — Adaptación · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidencia: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- Compatibilidad: `legacy-project-os/templates/operations/23-upgrade-kernel-adoption-in-target.md`
- Aprobación PM: Sí (exacta para escribir en el target)

**Hace:** Actualiza adapters de un target a una nueva versión de catálogo/kernel.
**Para:** Propagar upgrades de catálogo sin drift masivo.
**Cómo:** Draftea el paquete de adopción y la ruta delegada; la escritura exige aprobación exacta, preflight y validación proporcional.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.adoption_packet (+output.route_prompt). Ante adopción, versión, aprobación, preflight o validación faltante: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.5 o MOS-0.4. Después: MOS-0.5 por target actualizado. Recomendada: MOS-0.5.
