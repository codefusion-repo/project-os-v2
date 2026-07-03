# MOS-4.3 — Draftear el checklist de production readiness

Operación MOSDLC `draft-production-readiness-checklist` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Compatibilidad: `templates/operations/18-draft-human-qa-checklist.md`
- Aprobación PM: No (read-only)

**Hace:** Draftea el checklist humano de QA de production readiness.
**Para:** Verificar preparación real antes de considerar producción.
**Cómo:** Checklist transversal de readiness verificable por un humano.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.4. Después: MOS-4.6. Recomendada: MOS-4.6.
