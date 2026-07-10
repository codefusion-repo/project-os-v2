# MOS-R.1 — Registrar una decisión ADR

Operación MOSDLC `record-adr-decision` · Fase 2 — Diseño · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis
- Aprobación PM: No para draftear; sí exacta para escribir el ADR

**Hace:** Draftea un ADR para registrar una decisión PM estable y la ruta delegada de escritura.
**Para:** Preservar decisiones que deben sobrevivir al issue actual.
**Cómo:** Convierte DECISION y su base en contenido ADR y route prompt no autorizante.

**Variables**
- Requeridas: DECISION
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt. Ante decisión faltante, ambigua, sin evidencia o con escritura no aprobada: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.6 o decisión PM estable. Después: MOS-3.1 cuando la decisión esté registrada. Recomendada: MOS-3.1.
