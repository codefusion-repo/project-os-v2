# MOS-3.25 — Procesar la revisión de seguridad

Operación MOSDLC `process-security-review` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado de una revisión de seguridad y clasifica la ruta segura.
**Para:** Convertir findings de seguridad en corrección o follow-up.
**Cómo:** Clasifica bloqueantes y no bloqueantes sin ejecutar nada.

**Variables**
- Requeridas: SECURITY_REVIEW_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.

**Metadata derivada:** el issue o unidad relacionada, el PR, la rama y las
demás relaciones verificables se reconstruyen desde `SECURITY_REVIEW_RESULT` y
se muestran resueltas en la salida para que el receptor las verifique; no son
inputs manuales ni campos que el PM copie desde GitHub, y nunca se inventan.
Solo una ambigüedad material real —varias fuentes incompatibles igualmente
vigentes o una relación no verificable— devuelve `status.needs_context` o
`status.needs_pm_decision`; que el PM no haya reescrito un identificador
reconstruible nunca falla cerrado.

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.23. Después: MOS-3.5, MOS-3.3 o MOS-3.7. Recomendada: MOS-3.5 para bloqueantes.
