# MOS-3.23 — Solicitar revisión de seguridad

Operación MOSDLC `request-security-review` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → external_recipient
- Kernel: workflow.security_revision · mode.review_only · output.security_review_prompt
- Evidencia: evidence.repo_state, evidence.source_basis
- Compatibilidad: `legacy-project-os/templates/operations/20-request-owasp-security-review.md`
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el prompt de revisión de seguridad OWASP y de los 8 dominios donde corresponda.
**Para:** Obtener un gate de seguridad externo con redacción obligatoria.
**Cómo:** Prompt con superficie sensible descrita sin exponer secretos.

**Variables**
- Requeridas: PR_NUMBER
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.

**Entrega:** output.security_review_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7 o MOS-6.1. Después: MOS-3.25 al llegar el resultado. Recomendada: MOS-3.25.
