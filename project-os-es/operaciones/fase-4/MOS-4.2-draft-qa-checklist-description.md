# MOS-4.2 — Draftear un checklist QA desde una descripción

Operación MOSDLC `draft-qa-checklist-description` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/18-draft-human-qa-checklist.md`
- Aprobación PM: No (read-only)

**Hace:** Draftea el checklist humano de QA desde una descripción o feature.
**Para:** Validar features descritas sin issue/PR ancla.
**Cómo:** Convierte la descripción en pasos verificables por un humano.

**Variables**
- Requeridas: DESCRIPTION
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: descripción de feature estable. Después: MOS-4.5. Recomendada: MOS-4.5.
