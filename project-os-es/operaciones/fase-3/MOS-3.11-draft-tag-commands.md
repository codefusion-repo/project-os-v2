# MOS-3.11 — Draftear comandos de tag

Operación MOSDLC `draft-tag-commands` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.validation_output
- Compatibilidad: `templates/operations/13-draft-create-release-tag-command.md`
- Aprobación PM: Sí (el Humano PM autoriza y ejecuta el tag)

**Hace:** Draftea el bundle de creación de tag git para GitHub.
**Para:** Publicar un tag simple cuando el readiness lo justifica.
**Cómo:** Bundle copy-safe; el Humano PM ejecuta tag y push.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.10. Después: el Humano PM ejecuta; luego MOS-3.9 o MOS-3.12. Recomendada: MOS-3.12 si corresponde Release.
