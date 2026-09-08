# MOS-3.11 — Draftear comandos de tag

Operación MOSDLC `draft-tag-commands` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.validation_output, evidence.exact_ref
- Aprobación PM: Sí (el Humano PM autoriza y ejecuta el tag)

**Hace:** Draftea el bundle de creación de tag git para GitHub.
**Para:** Publicar un tag simple cuando el readiness lo justifica.
**Cómo:** Consume la evidencia vigente de MOS-3.10 y la continuidad del contrato
común, sin recapturar unidad, criterios ni validación aún válida. Verifica ref
exacta y aprobación de crear/pushear ese tag; no heredes permiso del merge.
El bundle copy-safe nombra tag, ref, responsable, recuperación y verificación
de identidad. El Humano PM ejecuta tag y push; tag aprobado no autoriza Release.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.10. Después: el Humano PM ejecuta; luego MOS-3.12, o MOS-3.27 para verificación independiente. Recomendada: MOS-3.12 si corresponde Release.
