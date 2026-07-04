# MOS-6.6 — Auditar código muerto

Operación MOSDLC `audit-dead-code` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Busca código huérfano, legacy, variables sin uso, funciones obsoletas y código inútil.
**Para:** Reducir superficie muerta y deuda técnica.
**Cómo:** Auditoría read-only con evidencia de archivos y líneas.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: mantenimiento periódico. Después: MOS-6.12. Recomendada: MOS-6.12.
