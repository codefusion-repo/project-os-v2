# MOS-1.2 — Resumir los requisitos identificados

Operación MOSDLC `summarize-requirements` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidencia: evidence.source_basis
- Aprobación PM: No (draft-only)

**Hace:** Resume y estructura los requisitos identificados en la entrevista.
**Para:** Tener una base estable antes de documentar.
**Cómo:** Sintetiza la conversación en una lista verificable por el PM.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.1. Después: MOS-1.3. Recomendada: MOS-1.3.
