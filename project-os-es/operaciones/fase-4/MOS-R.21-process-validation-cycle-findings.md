# MOS-R.21 — Procesar hallazgos de ciclo de validación

Operación MOSDLC `process-validation-cycle-findings` · Fase 4 — QA y verificación humana · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (clasifica y draftea; no crea ni ejecuta follow-ups)

**Hace:** Procesa hallazgos de un ciclo de validación y los convierte en follow-ups acotados.
**Para:** Capturar fricción real del target como trabajo trazable.
**Cómo:** Clasifica findings por evidencia, impacto y ruta: corrección, follow-up, decisión PM o no-op.

**Variables**
- Requeridas: VALIDATION_FINDINGS
- Opcionales: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Los hallazgos pueden venir de QA, UAT, beta, TestFlight, playtest, integración, piloto u otro ciclo target-owned.
- Si un hallazgo cambia alcance o dirección de producto, devuelve `status.needs_pm_decision`.

**Entrega:** output.status_result (+drafts si aplica). Ante findings ilegibles o sin base de evidencia: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.20 al cierre del ciclo. Después: MOS-3.3 por finding. Recomendada: MOS-3.3.
