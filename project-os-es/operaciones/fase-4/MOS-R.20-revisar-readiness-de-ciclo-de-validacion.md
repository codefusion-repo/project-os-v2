# MOS-R.20 — Revisar readiness de ciclo de validación

Operación MOSDLC `review-validation-cycle-readiness` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/37-review-phase-readiness.md`
- Aprobación PM: No (review advisory; el PM inicia o cierra el ciclo)

**Hace:** Revisa readiness para iniciar o cerrar un ciclo de validación del target.
**Para:** Entrar y salir de validación con criterios claros.
**Cómo:** Evalúa criterios de entrada o salida, evidencia faltante, blockers y decisiones PM pendientes.

**Variables**
- Requeridas: ninguna
- Opcionales: TARGET_REPOSITORY, VALIDATION_CYCLE_TYPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante criterios o evidencia ilegible, o decisión de inicio/cierre pendiente: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.19 o ciclo en curso. Después: MOS-R.21 al cerrar el ciclo. Recomendada: MOS-R.21 cuando existan hallazgos.
