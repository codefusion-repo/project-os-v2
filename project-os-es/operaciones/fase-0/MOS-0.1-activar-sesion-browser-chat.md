# MOS-0.1 — Activar la sesión de browser chat

Operación MOSDLC `activate-browser-session` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state (solo en la sesión vinculada; la desvinculada no
  tiene target y por eso no hay estado de repositorio en su alcance)
- Aprobación PM: No (read-only)

**Hace:** Establece la sesión draft-only del PM en browser chat resolviendo el manifest del kernel, con o sin un target seleccionado.
**Para:** Arrancar cualquier ciclo MOSDLC con boundaries y contexto correctos, y con un target inequívoco cuando ya exista.
**Cómo:** Resuelve el kernel y activa uno de dos estados de sesión explícitos
según `TARGET_REPOSITORY`, que es un locator primario opcional y no un requisito
para arrancar.

Con `TARGET_REPOSITORY`: activa la sesión vinculada al target exacto,
reconstruye `evidence.repo_state` exclusivamente contra él y emite el status
inicial nombrando el target revisado.

Sin `TARGET_REPOSITORY`: activa la sesión desvinculada, read-only y draft-only, y
declara explícitamente que todavía no hay target seleccionado. No lee, elige ni
infiere ningún repositorio conectado, no reconstruye estado de repositorio
—ninguno está en el alcance de esta activación— y no devuelve
`status.needs_context` solo por arrancar sin repositorio. La sesión desvinculada
no concede autoridad ni permite que una operación target-specific omita su
evidencia: antes de ejecutar cualquier operación que dependa realmente de estado
de repositorio, exige o deriva un target inequívoco, y falla cerrado con
`status.needs_context` cuando esa operación lo requiere y no puede
identificarlo.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO
  (`TARGET_REPOSITORY` es el locator primario en formato canónico `owner/repo` y
  se pide solo cuando el PM quiere vincular la sesión a un target; el feedback y
  la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Nombra siempre el estado de sesión activado —vinculado a un target exacto o explícitamente desvinculado—. Devuelve `status.needs_context` nombrando la evidencia faltante cuando el PM declara un `TARGET_REPOSITORY` que no tiene formato `owner/repo`, no puede resolverse o leerse mediante las fuentes conectadas, o cuya evidencia disponible corresponde a otro repositorio; nunca usa silenciosamente otro repositorio conectado y la sesión permanece read-only y draft-only en ambos estados. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: —. Después: MOS-0.2, MOS-0.3, MOS-0.5. Recomendada: MOS-0.5 si hay target adoptado; MOS-0.2 o MOS-0.3 si no.
