# MOS-4.1 — Draftear el checklist QA de un issue/PR

Operación MOSDLC `draft-qa-checklist-issue-pr` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Draftea el checklist humano de QA enfocado en un issue/PR.
**Para:** Cubrir lo no automatizable con QA humano dirigido.
**Cómo:** Extrae criterios del issue/PR a pasos verificables por un humano.

**Variables**
- Requeridas: QA_SOURCE
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** `QA_SOURCE` es el único locator primario y acepta por
igual un issue o un PR: cualquiera sirve cuando contiene evidencia suficiente
para extraer los criterios. Desde él se reconstruyen el issue o PR relacionado,
el repositorio y las demás relaciones verificables, que se muestran resueltas
en la salida sin volver a pedirlas. Solo una relación no verificable o varias
fuentes incompatibles igualmente vigentes devuelven `status.needs_context`.

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7. Después: MOS-4.4. Recomendada: MOS-4.4.
