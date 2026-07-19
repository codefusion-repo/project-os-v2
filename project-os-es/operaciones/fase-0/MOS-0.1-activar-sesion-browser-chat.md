# MOS-0.1 — Activar la sesión de browser chat

Operación MOSDLC `activate-browser-session` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Establece la sesión draft-only del PM en browser chat resolviendo el manifest del kernel contra el target declarado en `TARGET_REPOSITORY`.
**Para:** Arrancar cualquier ciclo MOSDLC con un target inequívoco, boundaries y contexto correctos.
**Cómo:** Solicita el target, resuelve el kernel, reconstruye `evidence.repo_state` exclusivamente contra `TARGET_REPOSITORY` y emite el status inicial identificando explícitamente el target revisado.

**Variables**
- Requeridas: TARGET_REPOSITORY (formato canónico `owner/repo`; nombra el repositorio target cuyo estado inicial se reconstruye)
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Devuelve `status.needs_context` nombrando la evidencia faltante cuando `TARGET_REPOSITORY` está ausente, no tiene formato `owner/repo`, no puede resolverse o leerse mediante las fuentes conectadas, o la evidencia disponible corresponde a otro repositorio; nunca usa silenciosamente otro repositorio conectado y la sesión permanece read-only y draft-only. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: —. Después: MOS-0.2, MOS-0.3, MOS-0.5. Recomendada: MOS-0.5 si hay target adoptado; MOS-0.2 o MOS-0.3 si no.
