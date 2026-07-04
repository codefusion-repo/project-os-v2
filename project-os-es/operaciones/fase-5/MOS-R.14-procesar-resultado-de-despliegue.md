# MOS-R.14 — Procesar resultado de despliegue

Operación MOSDLC `process-deployment-result` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (clasifica; rollback/corrección requieren gates propios)

**Hace:** Procesa un despliegue exitoso, parcial o fallido hacia continuar, corregir o rollback.
**Para:** Decidir la ruta siguiente con evidencia, no con output de deploy sin verificar.
**Cómo:** Cruza DEPLOYMENT_RESULT con evidencia MOS-R.13 y redacta cualquier salida sensible.

**Variables**
- Requeridas: DEPLOYMENT_RESULT, TARGET_ENVIRONMENT
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Rollback nunca es automático; el PM lo decide y MOS-R.15 lo draftea.
- Route prompts y bundles son no autorizantes o PM-executed; no ejecutes acciones de entorno.
- Redacta valores sensibles como `[REDACTED]` y reporta solo nombres de comando/check y tipos de riesgo.

**Entrega:** output.status_result (+drafts si aplica). Ante resultado o verificación ilegible, o elección continuar/rollback pendiente: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.13. Después: MOS-R.15 si falló y el PM elige rollback; MOS-3.3 para follow-ups. Recomendada: MOS-R.15 solo si rollback fue elegido.
