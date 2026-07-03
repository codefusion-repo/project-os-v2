# MOS-1.5 — Validar la documentación de requisitos

Operación MOSDLC `validate-requirements-docs` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Valida la documentación creada contra los requisitos identificados.
**Para:** Detectar huecos o contradicciones antes de planificar.
**Cómo:** Revisión read-only doc contra requisitos con hallazgos accionables.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.4. Después: MOS-1.6. Recomendada: MOS-1.6.
