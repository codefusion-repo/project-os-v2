# MOS-3.12 — Draftear comandos de release

Operación MOSDLC `draft-release-commands` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.validation_output
- Compatibilidad: `templates/operations/24-draft-create-github-release-command.md`
- Aprobación PM: Sí (el Humano PM autoriza y ejecuta el release)

**Hace:** Draftea el bundle de creación del objeto Release de GitHub (notas y tag).
**Para:** Publicar releases con notas trazables.
**Cómo:** Bundle copy-safe distinto del tag simple; ejecuta el Humano PM.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.10. Después: el Humano PM ejecuta; luego MOS-0.6 o MOS-3.1. Recomendada: MOS-3.1.
