# MOS-4.6 — Procesar el checklist de production readiness

Operación MOSDLC `process-production-readiness-checklist` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado del checklist humano de production readiness.
**Para:** Decidir si el proyecto avanza hacia despliegue.
**Cómo:** Conserva unidad, criterios, ref, entorno y disposiciones del QA
verificable según MOS-4.4 y el contrato común. QA pendiente/fallido conserva su
gate; no se convierte en PASS ni en permiso de producción. Con evidencia
suficiente consume MOS-R.11 para el entorno objetivo ya reconstruido, con su
workflow resuelto, sin otra selección de fase ni locator. Renueva solo lo que
requiera ese entorno/ref/riesgo y entrega el siguiente draft o gate pendiente.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.3. Después: MOS-4.4 para disposiciones QA o MOS-R.11 para readiness del entorno objetivo. Recomendada: siguiente salida segura en la misma unidad; nunca producción por inferencia.
