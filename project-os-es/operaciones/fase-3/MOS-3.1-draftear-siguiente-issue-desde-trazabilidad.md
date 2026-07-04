# MOS-3.1 — Draftear el siguiente issue desde trazabilidad

Operación MOSDLC `draft-next-issue-from-traceability` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Compatibilidad: `templates/operations/06-draft-create-next-issue-command-from-traceability.md`
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Infiere el próximo outcome real desde trazabilidad viva y roadmap y draftea su creación.
**Para:** Crear el siguiente issue único sin perder el hilo del roadmap.
**Cómo:** Lee estado vivo y draftea el bundle de creación para el Humano PM.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.6 o MOS-3.9. Después: MOS-3.4. Recomendada: MOS-3.4.
