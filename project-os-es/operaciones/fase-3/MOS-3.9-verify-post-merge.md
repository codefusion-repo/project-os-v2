# MOS-3.9 — Verificar el estado post-merge

Operación MOSDLC `verify-post-merge` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/11-verify-post-merge-state.md`
- Aprobación PM: No (read-only)

**Hace:** Verifica que la rama principal quedó saludable y el issue resuelto tras el merge.
**Para:** Cerrar el loop de implementación con evidencia.
**Cómo:** Chequeo read-only de default branch, issue y checks.

**Variables**
- Requeridas: PR_NUMBER
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.6. Después: MOS-3.1 o MOS-3.10. Recomendada: MOS-3.1.
