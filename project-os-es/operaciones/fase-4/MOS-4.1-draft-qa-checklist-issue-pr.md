# MOS-4.1 — Draftear el checklist QA de un issue/PR

Operación MOSDLC `draft-qa-checklist-issue-pr` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/18-draft-human-qa-checklist.md`
- Aprobación PM: No (read-only)

**Hace:** Draftea el checklist humano de QA enfocado en un issue/PR.
**Para:** Cubrir lo no automatizable con QA humano dirigido.
**Cómo:** Extrae criterios del issue/PR a pasos verificables por un humano.

**Variables**
- Requeridas: ISSUE_NUMBER
- Opcionales: PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7. Después: MOS-4.4. Recomendada: MOS-4.4.
