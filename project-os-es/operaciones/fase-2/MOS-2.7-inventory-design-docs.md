# MOS-2.7 — Inventariar la documentación de diseño

Operación MOSDLC `inventory-design-docs` · Fase 2 — Diseño · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption
- Aprobación PM: No (read-only)

**Hace:** Identifica la documentación de diseño existente en un proyecto.
**Para:** Saber qué diseño ya existe antes de crear o actualizar.
**Cómo:** Inventario read-only de docs de diseño y su estado.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.12. Después: MOS-2.8. Recomendada: MOS-2.8.
