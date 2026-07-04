# MOS-6.7 — Procesar resultados de seguridad de producción

Operación MOSDLC `process-security-production-results` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/31-process-security-review-results.md`
- Aprobación PM: No (draft-only)

**Hace:** Procesa los resultados de seguridad para production readiness.
**Para:** Convertir riesgos detectados en acciones concretas.
**Cómo:** Clasifica bloqueantes y diferibles sin ejecutar nada.

**Variables**
- Requeridas: SECURITY_REVIEW_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-6.1. Después: MOS-3.5 o MOS-3.3. Recomendada: MOS-3.5 para bloqueantes.
