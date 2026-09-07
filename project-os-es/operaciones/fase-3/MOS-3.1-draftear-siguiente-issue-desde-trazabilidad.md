# MOS-3.1 — Draftear el siguiente issue desde trazabilidad

Operación MOSDLC `draft-next-issue-from-traceability` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Infiere el próximo outcome real desde trazabilidad viva y roadmap y draftea su creación.
**Para:** Crear el siguiente issue único sin perder el hilo del roadmap.
**Cómo:** Lee estado vivo y draftea el bundle de creación para el Humano PM.

Si llega desde MOS-R.2, reutiliza intención, constraints y source basis para
draftear una sola unidad; no pidas al PM que los capture otra vez. La creación
sigue con el Humano PM. Para una intención de implementación, cuando el
resultado de creación se pueda verificar en vivo, continúa a MOS-3.4 según
MOS-R.2 sin otra selección MOS ni locator redundante.

Antes de draftear, verifica si ya existe una unidad para el outcome y
reutilízala; no crees otra por planificación o handoff. En un roadmap secuencial,
identifica si existe predecessor; cuando exista, verifica su completitud
material desde scope, criterios, PR, review/QA, validación y cierre vivos: un GO, un PR integrado o un
issue cerrado aislados no prueban el outcome. Si sigue materialmente abierto,
conserva esa unidad y reporta el siguiente paso seguro con `output.status_result`,
sin draftear la fase siguiente. Si falta evidencia, falla cerrado. Una vez
completo, infiere y draftea una única unidad para el siguiente outcome real,
reutilizando una existente si la hay; nunca un set anticipado por enumeración
del roadmap. Una prioridad material ambigua vuelve al PM.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.6 o el cierre GO de MOS-3.7. Después: MOS-3.4. Recomendada: MOS-3.4.
