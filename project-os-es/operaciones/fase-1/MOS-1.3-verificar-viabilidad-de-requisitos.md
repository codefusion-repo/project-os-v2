# MOS-1.3 — Verificar la viabilidad de los requisitos

Operación MOSDLC `verify-requirements-feasibility` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `legacy-project-os/templates/operations/16-review-idea-as-system-feature.md`
- Aprobación PM: No (read-only)

**Hace:** Evalúa viabilidad técnica y de alcance de los requisitos identificados.
**Para:** Evitar documentar o planificar requisitos inviables.
**Cómo:** Contrasta requisitos contra evidencia del repo y restricciones conocidas.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.2. Después: MOS-1.4. Recomendada: MOS-1.4.
