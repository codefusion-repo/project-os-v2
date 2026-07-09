# MOS-3.10 — Analizar readiness de release

Operación MOSDLC `analyze-release-readiness` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result (+output.pm_command_bundle)
- Evidencia: evidence.repo_state, evidence.validation_output
- Compatibilidad: `legacy-project-os/templates/operations/12-analyze-release-or-tag-readiness.md, legacy-project-os/templates/operations/13-draft-create-release-tag-command.md`
- Aprobación PM: No (read-only)

**Hace:** Analiza readiness de release-on-tag y draftea los comandos de creación si está listo.
**Para:** Decidir tag/release con evidencia merged y validación.
**Cómo:** Evalúa readiness y encadena el drafteo del bundle solo si procede.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.9. Después: MOS-3.11 o MOS-3.12. Recomendada: MOS-3.11.
