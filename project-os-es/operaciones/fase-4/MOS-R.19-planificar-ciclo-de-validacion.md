# MOS-R.19 — Planificar ciclo de validación

Operación MOSDLC `plan-validation-cycle` · Fase 4 — QA y verificación humana · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (planifica; inicio del ciclo queda con el PM)

**Hace:** Planifica un ciclo de validación real para el target según su tipo.
**Para:** Probar end-to-end con evidencia antes de ampliar o publicar.
**Cómo:** Draftea plan e issues acotados para QA, UAT, beta, TestFlight, playtest, integración, piloto u otra superficie aplicable.

**Variables**
- Requeridas: ninguna
- Opcionales: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Mantén wording target-agnostic: web, móvil, juegos, librerías/herramientas e internos pueden tener ciclos distintos.
- Falla cerrado si el target no tiene superficie de validación aplicable o si el PM debe escoger entre superficies.

**Entrega:** output.draft_issue (+output.pm_command_bundle). Ante superficie de validación faltante o elección PM necesaria: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.1, MOS-4.2 o preparación de validación. Después: MOS-R.20. Recomendada: MOS-R.20.
