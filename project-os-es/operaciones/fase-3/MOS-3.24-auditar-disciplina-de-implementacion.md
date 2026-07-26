# MOS-3.24 — Auditar disciplina de implementación

Operación MOSDLC `audit-implementation-discipline` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.review_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Audita disciplina de implementación con foco explícito en las tres
boundaries vigentes: boundary.implementation_discipline,
boundary.primary_path_discipline y boundary.validation_discipline.
**Para:** Detectar deuda de disciplina con evidencia de archivos y líneas, sin
un workflow especializado propio.
**Cómo:** Auditoría read-only sobre `workflow.review_only` que entrega
findings con su disposición verificable; el procesamiento posterior vive en
MOS-3.14, nunca en una entrega directa de issue.

**Variables**
- Requeridas: — (ninguna)
- Opcionales: AUDIT_SCOPE, PATH_SCOPE, FOCUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Locator único y constraints humanos:** `AUDIT_SCOPE` es el único locator
primario y nunca se combina con otro locator en la captura rutinaria. Primero
reutiliza una fuente inequívoca ya seleccionada; en ese caso `AUDIT_SCOPE` puede
quedar vacío. Sin contexto suficiente, recibe exactamente una referencia
verificable: `owner/repo` para una auditoría repo-wide, o issue o PR para una
auditoría acotada. Deriva desde esa fuente o desde el contexto el repositorio y
las demás relaciones verificables. `PATH_SCOPE` es un constraint humano opcional
que acota superficie, no metadata derivada. `FOCUS` solo puede estrechar el
análisis dentro de las tres boundaries de disciplina; nunca amplía el scope ni
selecciona otro workflow. Si falta locator y contexto suficiente, el formato no
es verificable, o la evidencia resuelve fuentes incompatibles, falla cerrado con
`status.needs_context`; nunca elige un target ni mezcla evidencias.

**Entrega:** output.review_result. Los findings no se entregan como issue
directo: MOS-3.14 los clasifica y deriva a corrección, follow-up o no-op. Ante
evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con
output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: MOS-3.14. Recomendada: MOS-3.14.
