# MOS-R.5 — Auditar adopción de targets en lote

Operación MOSDLC `audit-target-adoption-batch` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption
- Compatibilidad: `templates/operations/14-audit-target-adapters.md`, `templates/operations/03-verify-target-adoption.md`
- Aprobación PM: No (auditoría read-only)

**Hace:** Audita la adopción de varios repositorios target en una sola pasada.
**Para:** Mantener múltiples targets adoptados sin drift acumulado.
**Cómo:** Itera la verificación de adopción por target y consolida drift, adapters faltantes y adopción stale.

**Variables**
- Requeridas: TARGET_REPOSITORIES
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante lista vacía, target ilegible o evidencia de adopción faltante: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.5 o mantenimiento de adopción. Después: MOS-0.4 por target con drift. Recomendada: MOS-0.4 por target con drift.
