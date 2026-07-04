# MOS-R.11 — Revisar readiness de despliegue por entorno

Operación MOSDLC `deployment-readiness-review` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No (readiness read-only)

**Hace:** Revisa readiness de despliegue para un `TARGET_ENVIRONMENT`.
**Para:** Unificar análisis local/staging/producción sin borrar las operaciones PM-facing por entorno.
**Cómo:** Verifica configuración, comandos target-owned, checklist pendiente y blockers del entorno.

**Variables**
- Requeridas: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia faltante, entorno inexistente o decisión PM requerida: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-5.1, MOS-5.4 o MOS-5.7. Después: MOS-R.12 si hay readiness; si no, checklist del entorno correspondiente. Recomendada: MOS-R.12 cuando readiness sea suficiente.
