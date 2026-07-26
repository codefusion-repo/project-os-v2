# MOS-3.3 — Draftear un follow-up issue

Operación MOSDLC `draft-follow-up-issue` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea un follow-up desde cualquier fuente viva: un issue
incompleto, un review, una auditoría de disciplina o una revisión de seguridad.
**Para:** Diferir con trazabilidad trabajo pendiente y hallazgos no bloqueantes.
**Cómo:** Aísla lo faltante o diferido en un follow-up con scope propio; la
fuente viva queda referenciada, no copiada. Aplica primero el gate de
materialidad de `rule.economia_de_contexto`: solo draftea cuando la fuente
contiene un gap vigente, durable y accionable, con outcome observable, scope
independiente y razón para diferirlo en vez de descartarlo. Que una observación
sea técnicamente verdadera o pueda redactarse como issue no basta: una
observación histórica, informativa, confirmatoria, ya resuelta por el curso
normal o duplicada de evidencia viva no genera follow-up. Sin trabajo durable y
accionable, devuelve no-action con `output.status_result`. Usa como máximo un
locator primario: cuando la invocación actual ya identifica una fuente viva
inequívoca —el review, la auditoría, la revisión de seguridad o el issue que se
acaba de trabajar en esta sesión— no vuelvas a pedirla; cuando no exista, pide
solo `FOLLOW_UP_SOURCE` y reconstruye desde ahí sus relaciones.

**Variables**
- Requeridas: ninguna
- Opcionales: FOLLOW_UP_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO
  (`FOLLOW_UP_SOURCE` es el único locator primario —issue incompleto, review,
  resultado de auditoría o de revisión de seguridad, u otro registro vivo— y se
  pide solo cuando el contexto de ejecución no identifica ya una fuente
  inequívoca; el feedback y la pregunta del PM son contexto humano; nunca
  autorizan nada)

**Metadata derivada:** el issue o unidad relacionada, el PR, el review o
comentario fuente, la rama existente y las relaciones entre roadmap, unidad y
hallazgos se reconstruyen desde la fuente viva y se muestran resueltos en el
bundle para que el Humano PM los verifique; no son inputs manuales ni campos que
el PM copie desde GitHub, y nunca se inventan. Solo una ambigüedad material real
—varias fuentes incompatibles igualmente vigentes o una relación
unidad↔PR↔review no verificable— devuelve `status.needs_context` o
`status.needs_pm_decision`; que el PM no haya reescrito un identificador
reconstruible nunca falla cerrado.

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.14, MOS-3.25 o MOS-3.31.
Después: MOS-3.4 cuando se priorice. Recomendada: MOS-3.4.
