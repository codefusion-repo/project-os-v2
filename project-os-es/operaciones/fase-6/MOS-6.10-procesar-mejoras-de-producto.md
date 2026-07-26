# MOS-6.10 — Procesar mejoras de producto

Operación MOSDLC `process-product-improvements` · Fase 6 — Mantenimiento y mejoras · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.pm_command_bundle, output.status_result)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa las mejoras de producto recomendadas.
**Para:** Alimentar roadmap y backlog con decisiones PM.
**Cómo:** Lee la revisión viva referida por `REVIEW_SOURCE` y clasifica cada
mejora hacia roadmap, issues o no-op; una clasificación resuelta entrega el
route prompt o el command bundle que corresponda.

**Variables**
- Requeridas: REVIEW_SOURCE
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** el issue o unidad relacionada, el PR, la rama, el roadmap
y las demás relaciones verificables se reconstruyen desde `REVIEW_SOURCE` y se
muestran resueltas en la salida; no son inputs manuales y nunca se inventan.
Solo una fuente ausente, no verificable o materialmente ambigua —varias fuentes
incompatibles igualmente vigentes o una relación material no reconstruible—
falla cerrado con output.status_result.

**Entrega:** output.route_prompt (+output.pm_command_bundle, output.status_result). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-6.4. Después: MOS-1.8 o MOS-3.8. Recomendada: MOS-1.8 si toca el roadmap.
