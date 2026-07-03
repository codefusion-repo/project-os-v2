# MOS-3.18 — Solicitar un asset de video

Operación MOSDLC `request-video-asset` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → external_recipient
- Kernel: workflow.design_asset · mode.review_only · output.asset_prompt
- Evidencia: evidence.repo_state, evidence.source_basis
- Compatibilidad: `templates/operations/19-request-external-design-assets.md`
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el asset prompt para solicitar un asset de video a un destinatario externo.
**Para:** Obtener assets de video sin tratar al creador como actor kernel.
**Cómo:** Prompt PM-facing con objetivo, restricciones y formato de entrega.

**Variables**
- Requeridas: DESCRIPTION
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.asset_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: necesidad de asset detectada. Después: MOS-3.22 al llegar la entrega. Recomendada: MOS-3.22.
