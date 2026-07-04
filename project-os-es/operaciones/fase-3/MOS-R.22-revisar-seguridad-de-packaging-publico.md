# MOS-R.22 — Revisar seguridad de packaging público

Operación MOSDLC `public-packaging-safety-review` · Fase 3 — Implementación · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.source_basis
- Aprobación PM: No (review read-only; conversiones y publicación son separadas)

**Hace:** Revisa si el target es seguro para empaquetado o uso público.
**Para:** Evitar publicar superficies internas, secretos, defaults inseguros o docs riesgosas.
**Cómo:** Inspecciona hygiene de secretos, exposición documental y superficies internal-only sin convertir nada.

**Variables**
- Requeridas: ninguna
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Reporta secrets hygiene por ruta, variable o tipo de riesgo; nunca valores.
- Mantén wording target-agnostic: no asumas Project OS, dogfood, paquetes públicos ni release GitHub.
- Si una exposición requiere elección PM, devuelve `status.needs_pm_decision`.

**Entrega:** output.status_result. Ante superficies de packaging ilegibles o exposición ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.7. Después: MOS-R.23. Recomendada: MOS-R.23.
