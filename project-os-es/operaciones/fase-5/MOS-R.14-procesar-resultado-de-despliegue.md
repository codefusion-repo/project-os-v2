# MOS-R.14 — Procesar resultado de despliegue

Operación MOSDLC `process-deployment-result` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (clasifica; rollback/corrección requieren gates propios)

**Hace:** Procesa un despliegue exitoso, parcial o fallido hacia continuar, corregir o rollback.
**Para:** Decidir la ruta siguiente con evidencia, no con output de deploy sin verificar.
**Cómo:** Cruza DEPLOYMENT_RESULT con evidencia MOS-R.13 de la misma unidad,
target, ref y entorno. Éxito verificado permite reconstruir readiness del
entorno objetivo pendiente por MOS-R.11, renovando su evidencia específica y
mostrando su gate exacto; no implica promoción. Ante fallo, conserva la unidad,
clasifica corrección por la ruta aplicable o decisión PM de rollback por
MOS-R.15; follow-up solo con materialidad e independencia por MOS-3.3.
Entrega la salida segura en la misma respuesta y redacta cualquier dato sensible.

**Variables**
- Requeridas: DEPLOYMENT_RESULT, TARGET_ENVIRONMENT
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Rollback nunca es automático; el PM lo decide y MOS-R.15 lo draftea.
- Route prompts y bundles son no autorizantes o PM-executed; no ejecutes acciones de entorno.
- Redacta valores sensibles como `[REDACTED]` y reporta solo nombres de comando/check y tipos de riesgo.

**Entrega:** output.status_result (+drafts si aplica). Ante resultado o verificación ilegible, o elección continuar/rollback pendiente: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.13. Después: MOS-R.11 para entorno pendiente con éxito verificado; MOS-R.15 si el PM elige rollback; corrección de la unidad o MOS-3.3 solo para outcome independiente. Recomendada: la siguiente acción segura de la misma unidad, sin promoción automática.
