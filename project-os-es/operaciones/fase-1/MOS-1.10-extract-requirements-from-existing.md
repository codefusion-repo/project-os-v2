# MOS-1.10 — Extraer requisitos de un proyecto existente

Operación MOSDLC `extract-requirements-from-existing` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption
- Aprobación PM: No (read-only)

**Hace:** Identifica requisitos reales desde el código y docs de un proyecto existente.
**Para:** Adoptar proyectos que nunca tuvieron Fase 1 formal.
**Cómo:** Lee el repo target y reconstruye requisitos observables.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.3. Después: MOS-1.11. Recomendada: MOS-1.11.
