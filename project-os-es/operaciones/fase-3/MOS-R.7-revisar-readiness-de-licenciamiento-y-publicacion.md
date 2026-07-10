# MOS-R.7 — Revisar readiness de licenciamiento y publicación

Operación MOSDLC `review-licensing-publication-readiness` · Fase 3 — Implementación · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.source_basis
- Aprobación PM: No (review advisory; publicación queda con el PM)

**Hace:** Revisa licenciamiento, soporte, secrets hygiene y calidad documental para publicación.
**Para:** Decidir publicación con evidencia real, no por intuición.
**Cómo:** Contrasta el repo y los criterios de publicación del target sin ejecutar acciones de release.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Reporta riesgos de secretos solo por ruta, variable o tipo; nunca valores.
- No asumas que todo target publica paquetes, releases o distribución pública.

**Entrega:** output.status_result. Ante criterios o evidencia ilegible, o decisión de publicación pendiente: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.10 o preparación de publicación. Después: MOS-R.22. Recomendada: MOS-R.22.
