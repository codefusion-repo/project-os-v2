# MOS-6.1 — Revisar seguridad para production readiness

Operación MOSDLC `review-security-production-readiness` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/20-request-owasp-security-review.md, templates/operations/25-audit-implementation-discipline-gaps.md`
- Aprobación PM: No (read-only)

**Hace:** Revisa la seguridad del proyecto para production readiness.
**Para:** Detectar riesgos de seguridad antes de producción.
**Cómo:** Revisión read-only OWASP y 8 dominios sobre el estado actual.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.6. Después: MOS-6.7. Recomendada: MOS-6.7.
