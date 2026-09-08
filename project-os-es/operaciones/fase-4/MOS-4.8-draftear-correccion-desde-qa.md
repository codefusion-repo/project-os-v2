# MOS-4.8 — Draftear una corrección desde QA

Operación MOSDLC `draft-correction-from-qa` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el prompt de corrección desde resultados de QA.
**Para:** Corregir bloqueantes de QA sin expandir el scope.
**Cómo:** Lee y aplica MOS-3.5 como único contrato de corrección en esta misma
respuesta. Desde `QA_RESULT` reconstruye `WORK_UNIT`, `PR_NUMBER`,
`SOURCE_REVIEW`, clase y rama sin pedir otro locator. Solo transporta
`blocking-correction` del scope original: conserva unidad y PR, exige autorización
exacta, validación real, correction report append-only y re-review del head
corregido conforme a MOS-3.5. Usa su forma compacta de route prompt. Conserva
esta entrada compatible; no crea unidad, semántica ni handoff adicionales.

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

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.4. Después: MOS-3.7. Recomendada: MOS-3.7.
