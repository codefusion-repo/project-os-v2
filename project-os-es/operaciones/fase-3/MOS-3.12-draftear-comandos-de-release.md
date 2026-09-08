# MOS-3.12 — Draftear comandos de release

Operación MOSDLC `draft-release-commands` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.validation_output, evidence.exact_ref
- Aprobación PM: Sí (el Humano PM autoriza y ejecuta el release)

**Hace:** Draftea el bundle de creación del objeto Release de GitHub (notas y tag).
**Para:** Publicar releases con notas trazables.
**Cómo:** Consume MOS-3.10 y el contrato común de continuidad. Verifica en vivo
tag y ref resultante, validación y notas para la misma unidad. La aprobación
exacta de Release no se infiere del tag ni del closeout; si crear el Release
también crearía un tag ausente, aplica primero MOS-3.11 y su gate propio.
El bundle copy-safe conserva recuperación y verificación del objeto y su ref;
ejecuta el Humano PM. Tras verificar el resultado, continúa con readiness del
entorno objetivo pendiente usando las mismas fuentes, sin unidad de transición.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.10 y tag verificado. Después: ejecución y verificación PM; MOS-R.11 para el entorno pendiente del mismo outcome, o MOS-0.6 para handoff. MOS-3.1 solo cuando corresponde un outcome siguiente. Recomendada: readiness del entorno pendiente, sin inferir deploy.
