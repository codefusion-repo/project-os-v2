# MOS-0.2 — Iniciar un proyecto nuevo

Operación MOSDLC `bootstrap-new-project` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet
- Evidencia: evidence.target_adoption
- Compatibilidad: `templates/operations/02-bootstrap-new-project.md`
- Aprobación PM: No (draft-only)

**Hace:** Draftea la estructura de adopción inicial y el roadmap fundacional de un repo nuevo.
**Para:** Iniciar un proyecto nuevo bajo Project OS.
**Cómo:** Browser chat draftea el paquete de adopción; el Humano PM lo aplica o lo delega.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.adoption_packet. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.1. Después: MOS-0.5. Recomendada: MOS-0.5.
