# MOS-R.23 — Convertir operaciones internas antes de release

Operación MOSDLC `convert-internal-operations-before-release` · Fase 3 — Implementación · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue)
- Evidencia: evidence.source_basis
- Aprobación PM: No para draftear; sí exacta para convertir, ocultar, remover o deshabilitar

**Hace:** Draftea la conversión de superficies internal-only antes de release público.
**Para:** Publicar sin exponer capacidades internas del target.
**Cómo:** Usa el inventario de exposición del target y produce una ruta delegada no autorizante.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Opciones seguras: remover, ocultar, deshabilitar o convertir; la elección concreta puede requerir PM.
- No implementes conversiones ni cambies packaging; esta operación solo draftea la ruta.
- Redacta secretos y no copies detalles internos sensibles fuera de su contexto.

**Entrega:** output.route_prompt (+output.draft_issue). Ante inventario ilegible, disposición ambigua o aprobación faltante para escritura: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.22. Después: MOS-R.7 para re-verificar publicación. Recomendada: MOS-R.7.
