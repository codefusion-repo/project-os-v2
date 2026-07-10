# MOS-R.6 — Crear o actualizar ADR desde diseño

Operación MOSDLC `create-update-adr-from-design` · Fase 2 — Diseño · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis
- Aprobación PM: No para draftear; sí exacta para escribir o actualizar ADRs

**Hace:** Extrae decisiones estables de documentación de diseño o requisitos y draftea ADRs.
**Para:** Llevar a ADR las decisiones que deben sobrevivir a documentos e issues.
**Cómo:** Lee SOURCE_DOCS, identifica decisiones candidatas y deriva una ruta delegada por decisión.

**Variables**
- Requeridas: SOURCE_DOCS
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.route_prompt. Ante docs ilegibles, ausencia de decisiones estables o conflicto con ADR existente: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-2.6 o actualización de diseño. Después: MOS-R.1 por decisión extraída. Recomendada: MOS-R.1.
