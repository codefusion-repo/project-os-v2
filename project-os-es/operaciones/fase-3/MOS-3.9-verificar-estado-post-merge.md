# MOS-3.9 — Verificar el estado post-merge

Operación MOSDLC `verify-post-merge` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Verifica que la rama principal quedó saludable y el issue resuelto tras el merge.
**Para:** Verificación posterior independiente cuando el cierre falló, una
auditoría la exige o el PM la solicita; no es un turno obligatorio después de
cada merge, porque el GO de MOS-3.7 ya incluye la verificación final.
**Cómo:** Chequeo read-only de default branch, issue y checks.

**Variables**
- Requeridas: PR_NUMBER
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: un cierre con fallo, una auditoría o una solicitud PM de
verificación independiente. Después: MOS-3.1 o MOS-3.10. Recomendada: MOS-3.1.
