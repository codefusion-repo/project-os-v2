# MOS-1.7 — Revisar la viabilidad de una idea

Operación MOSDLC `review-idea-feasibility` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/16-review-idea-as-system-feature.md`
- Aprobación PM: No (read-only)

**Hace:** Evalúa una idea nueva como posible requerimiento del proyecto.
**Para:** Decidir si la idea entra al roadmap.
**Cómo:** Analiza la idea contra estado vivo y documentación y recomienda ruta.

**Variables**
- Requeridas: IDEA
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-1.8 si procede. Recomendada: MOS-1.8.
