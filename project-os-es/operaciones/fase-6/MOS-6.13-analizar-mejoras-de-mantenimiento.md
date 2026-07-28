# MOS-6.13 — Analizar mejoras de mantenimiento

<!-- project-os-operation
canonical_code: MOS-6.13
operation_id: analyze-maintenance-improvements
aliases: MOS-6.3,MOS-6.4,MOS-6.5
deprecation: none
compatibility_reason: MOS-6.3, MOS-6.4 y MOS-6.5 conservan sus entrypoints históricos y resuelven este único contrato con su foco ligado.
-->

Operación MOSDLC `analyze-maintenance-improvements` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Analiza y recomienda mejoras de mantenimiento para un único foco.
**Para:** Priorizar mejoras fundamentadas sin mezclar rendimiento, producto y calidad de código.
**Cómo:** Análisis read-only de `FOCUS_AREA`, entregado como hallazgos con referencia,
disposición verificable, recomendación, riesgos y áreas no revisadas. Un foco ausente,
inválido o materialmente ambiguo falla cerrado con `output.status_result`.

**Variables**
- Requeridas: TARGET_REPOSITORY, FOCUS_AREA
- Opcionales: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

INPUT:
  TARGET_REPOSITORY=<owner/repository>
  FOCUS_AREA=<performance|product|code_quality>
  PATH_SCOPE=<path scope> optional
  PM_FEEDBACK_HUMANO=<human feedback> optional
  PM_QUESTION_HUMANO=<human question> optional

**Entrega:** output.review_result (+output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: mantenimiento periódico. Después: MOS-6.9, MOS-6.10 o MOS-3.14 según `FOCUS_AREA`. Recomendada: MOS-6.9 para `performance`, MOS-6.10 para `product` y MOS-3.14 para `code_quality`.
