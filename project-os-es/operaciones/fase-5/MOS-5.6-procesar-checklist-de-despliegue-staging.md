# MOS-5.6 — Procesar el checklist de despliegue staging

Operación MOSDLC `process-staging-deploy-checklist` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado de los pasos humanos del despliegue staging.
**Para:** Confirmar readiness o derivar gaps antes de continuar.
**Cómo:** Contrasta CHECKLIST_RESULT con la unidad, ref y entorno del
checklist y aplica MOS-R.11 sin recapturar evidencia válida. Si readiness
es suficiente, consume MOS-5.12 en esta respuesta; no exige otro
checklist ni selección. Resultado obsoleto o fallido conserva sus blockers;
la disposición y aprobación de corrección o rollback siguen sus rutas.
Solo un despliegue ya ejecutado pasa a verificación por MOS-R.13.

**Variables**
- Requeridas: CHECKLIST_RESULT
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Depende de las `Project-specific notes` del adapter del target: usa solo comandos y rutas target-owned documentados ahí; si faltan o son ambiguos, fail-closed.

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-5.5. Después: MOS-5.12 o MOS-R.13. Recomendada: MOS-5.12.
