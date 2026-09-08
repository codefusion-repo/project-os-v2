# MOS-3.10 — Analizar readiness de release

Operación MOSDLC `analyze-release-readiness` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result (+output.pm_command_bundle)
- Evidencia: evidence.repo_state, evidence.validation_output, evidence.exact_ref
- Aprobación PM: No (read-only)

**Hace:** Analiza readiness de release-on-tag y draftea los comandos de creación si está listo.
**Para:** Decidir tag/release con evidencia merged y validación.
**Cómo:** Reconstruye la unidad, QA y review vigentes por el contrato común de
continuidad QA → release → deployment. Verifica el merge real y su ref
resultante; un GO o CI del head previo no prueba validación de ese ref. Reutiliza
criterios y evidencia aún aplicables; renueva lo dependiente de ref, entorno o
riesgo. Expone cada gap y el gate exacto de tag/Release, separado del closeout.
Con readiness suficiente y aprobaciones exactas aplicables, consume MOS-3.11 o
MOS-3.12 en la misma respuesta, sin pedir otra selección ni locator. Si falta
merge, validación o decisión, entrega el estado y siguiente paso seguro, sin
declarar readiness ni crear una unidad de release.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result (+output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: QA y closeout por MOS-3.7, con merge verificado para readiness de release. Después: MOS-3.11 o MOS-3.12 en la misma respuesta si sus gates están satisfechos; luego readiness del entorno objetivo por MOS-R.11 cuando aplique. Recomendada: la siguiente acción pendiente de la misma unidad.
