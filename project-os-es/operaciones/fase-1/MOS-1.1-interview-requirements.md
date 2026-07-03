# MOS-1.1 — Entrevistar requisitos

Operación MOSDLC `interview-requirements` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidencia: evidence.source_basis
- Aprobación PM: No (draft-only)

**Hace:** Conduce una entrevista guiada al PM para elicitar requisitos.
**Para:** Capturar requisitos funcionales y no funcionales desde el conocimiento del PM.
**Cómo:** Preguntas iterativas en chat; sintetiza hallazgos sin escribir archivos.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.5. Después: MOS-1.2. Recomendada: MOS-1.2.
