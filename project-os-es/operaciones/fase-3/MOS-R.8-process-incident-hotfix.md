# MOS-R.8 — Procesar incidente o hotfix

Operación MOSDLC `process-incident-hotfix` · Fase 3 — Implementación · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.draft_issue, output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (triage draft-only; hotfix y comandos requieren sus propios gates)

**Hace:** Procesa un incidente o bug crítico hacia severidad, hotfix y postmortem.
**Para:** Dar una ruta explícita a incidentes sin improvisar bajo presión.
**Cómo:** Confirma evidencia viva, clasifica severidad y draftea issue/ruta/bundle solo cuando corresponde.

**Variables**
- Requeridas: INCIDENT_DESCRIPTION
- Opcionales: TARGET_REPOSITORY, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- No ejecutes hotfixes, rollbacks ni comandos; los outputs son no autorizantes o PM-executed.
- Redacta secretos y pide base redactada si el incidente incluye credenciales o valores sensibles.

**Entrega:** output.status_result (+drafts si aplica). Ante incidente no confirmable o severidad/ruta ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: reporte de incidente o MOS-R.16. Después: MOS-3.4 para hotfix; MOS-3.3 para postmortem. Recomendada: MOS-3.4 si el hotfix está justificado.
