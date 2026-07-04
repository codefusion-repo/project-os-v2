# MOS-R.16 — Procesar resultado de rollback

Operación MOSDLC `process-rollback-result` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (clasifica; incidentes/correcciones requieren gates propios)

**Hace:** Procesa el resultado de un rollback ejecutado hacia incidente, corrección o cierre.
**Para:** Cerrar el incidente de despliegue con trazabilidad y evidencia post-rollback.
**Cómo:** Clasifica ROLLBACK_RESULT como restaurado, parcial o fallido solo cuando la evidencia lo sostiene.

**Variables**
- Requeridas: ROLLBACK_RESULT, TARGET_ENVIRONMENT
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Si el entorno sigue inseguro, devuelve `status.blocked`.
- No redespliegues, no re-hagas rollback, no ejecutes correcciones ni autorices acciones de entorno.
- Redacta salidas sensibles y reporta solo comando/check/riesgo.

**Entrega:** output.status_result (+drafts si aplica). Ante evidencia ilegible o ruta siguiente con decisión pendiente: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: ejecución PM de MOS-R.15. Después: MOS-R.8 si hay incidente; MOS-3.3 para follow-ups. Recomendada: MOS-R.8 cuando el rollback expone incidente.
