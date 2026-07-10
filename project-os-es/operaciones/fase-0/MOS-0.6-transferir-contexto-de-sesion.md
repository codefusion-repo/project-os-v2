# MOS-0.6 — Transferir el contexto de sesión

Operación MOSDLC `handoff-session-context` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.handoff · mode.review_only · output.handoff_packet
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Empaqueta contexto vivo y decisiones PM para transferir a una sesión nueva.
**Para:** Continuar el trabajo sin perder trazabilidad.
**Cómo:** Draftea un handoff packet reconstruible desde GitHub.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.handoff_packet. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-0.1 en la nueva sesión. Recomendada: MOS-0.1 en la nueva sesión.
