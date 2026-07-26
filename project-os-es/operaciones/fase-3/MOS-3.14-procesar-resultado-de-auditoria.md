# MOS-3.14 — Procesar el resultado de una auditoría

<!-- project-os-operation
canonical_code: MOS-3.14
operation_id: process-audit-result
aliases: MOS-6.11
deprecation: none
compatibility_reason: MOS-6.11 conserva su entrypoint histórico de mejoras de código y resuelve este contrato canónico para cualquier auditoría o revisión referida por REVIEW_SOURCE.
-->

Operación MOSDLC `process-audit-result` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.pm_command_bundle, output.status_result)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado de cualquier auditoría o revisión (trazabilidad,
disciplina, análisis de mantenimiento u otra) y clasifica la ruta segura.
**Para:** Convertir hallazgos en acciones concretas sin fragmentar el
procesamiento por tipo de revisión de origen.
**Cómo:** Clasifica cada hallazgo con su disposición verificable y lo deriva a
corrección (`blocking-correction` → MOS-3.5), follow-up (`non-blocking-follow-up`
→ MOS-3.3) o no-op (`preference`, `accepted-risk`, `invalid-finding`); una
clasificación resuelta entrega el route prompt o el command bundle que
corresponda. El origen viaja como referencia viva en `REVIEW_SOURCE`; la
operación no depende del tipo de revisión de origen.

**Variables**
- Requeridas: REVIEW_SOURCE
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** el issue o unidad relacionada, el PR, la rama, el roadmap
y las demás relaciones verificables se reconstruyen desde `REVIEW_SOURCE` y se
muestran resueltas en la salida para que el receptor las verifique; no son
inputs manuales ni campos que el PM copie desde GitHub, y nunca se inventan.
Solo una fuente ausente, no verificable o materialmente ambigua —varias fuentes
incompatibles igualmente vigentes o una relación material no reconstruible—
devuelve `status.needs_context` o `status.needs_pm_decision`; que el PM no haya
reescrito un identificador reconstruible nunca falla cerrado.

**Entrega:** output.route_prompt (+output.pm_command_bundle, output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.13, MOS-3.24 u otra auditoría. Después: MOS-3.5 o MOS-3.3. Recomendada: MOS-3.3 para lo no bloqueante.
