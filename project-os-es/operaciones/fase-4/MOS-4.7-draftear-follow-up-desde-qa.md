# MOS-4.7 — Draftear un follow-up desde QA

Operación MOSDLC `draft-follow-up-from-qa` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea follow-up desde resultados de QA.
**Para:** Diferir hallazgos de QA no bloqueantes con trazabilidad.
**Cómo:** Usa MOS-3.3 como único contrato de follow-up: `QA_RESULT` es su
`FOLLOW_UP_SOURCE` ya disponible. Lee y aplica ese contrato en esta misma
respuesta, incluidos materialidad, independencia, agrupación, reutilización de
unidad y no-action. No pidas otro locator ni conviertas cada finding QA en un
issue. Conserva esta entrada compatible; no es otra semántica ni un handoff
obligatorio.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** el issue o unidad relacionada, el PR, la rama y las
demás relaciones verificables se reconstruyen desde `QA_RESULT` y se muestran
resueltas en la salida para que el receptor las verifique; no son inputs
manuales ni campos que el PM copie desde GitHub, y nunca se inventan. Solo una
ambigüedad material real —varias fuentes incompatibles igualmente vigentes o
una relación no verificable— devuelve `status.needs_context` o
`status.needs_pm_decision`; que el PM no haya reescrito un identificador
reconstruible nunca falla cerrado.

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.4, MOS-4.5 o MOS-4.6. Después: MOS-3.4 cuando se priorice. Recomendada: MOS-3.4.
