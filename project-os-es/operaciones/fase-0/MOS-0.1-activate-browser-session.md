# MOS-0.1 — Activar la sesión de browser chat

Operación MOSDLC `activate-browser-session` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/00-browser-chat-activation.md`
- Aprobación PM: No (read-only)

**Hace:** Establece la sesión draft-only del PM en browser chat resolviendo el manifest del kernel.
**Para:** Arrancar cualquier ciclo MOSDLC con boundaries y contexto correctos.
**Cómo:** Resuelve el kernel, lee estado vivo mínimo y emite el status inicial.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: —. Después: MOS-0.2, MOS-0.3, MOS-0.5. Recomendada: MOS-0.5 si hay target adoptado; MOS-0.2 o MOS-0.3 si no.
