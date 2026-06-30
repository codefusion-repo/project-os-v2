# PM Operations Catalog (Catálogo de Operaciones PM)

Este documento es el **índice canónico** de las operaciones públicas. Cada fila
apunta a un template en `templates/operations/` y lo resuelve a ids reales del
kernel (`kernel/workflows.json`, `kernel/execution_modes.json`,
`kernel/outputs.json`, `kernel/evidence.json`).

Los archivos `templates/operations/*.md` **no** son fichas descriptivas
PM-facing: son **prompts de operación ejecutables para IA**. Cada uno usa bloques
en mayúscula (`OPERATION`, `INPUT`, `KERNEL`, `LIVE_STATE`, `DO`, `IF`, `OUTPUT`,
`LIMITS`) y empieza resolviendo `manifest.json` y siguiendo su
`resolution_sequence` antes de ejecutar. El template porta forma y scope; nunca
porta autorización ni estado vivo. La autoridad de escritura proviene de
aprobación PM exacta más los gates del kernel (`boundary.output_not_permission`).

Las superficies (browser chat, terminal agent, Humano PM, destinatario externo)
aparecen en la columna **Superficie**. Las variables son selectores de contexto,
no autorización. En la tabla, los ids de workflow/mode/output/evidence se muestran
sin su prefijo de familia (`workflow.` / `mode.` / `output.` / `evidence.`); cada
uno resuelve a un id real del kernel.

| Template (`templates/operations/`) | Objetivo | Superficie | Workflow | Mode | Output | Evidence | Variables (Req / Opc) | Aprob. PM |
|---|---|---|---|---|---|---|---|---|
| `templates/operations/00-browser-chat-activation.md` | Establecer el contexto de sesión draft-only del PM en browser chat. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `PM_QUESTION` | No |
| `templates/operations/01-adopt-project-os-in-existing-target.md` | Preparar un repositorio existente para operar con Project OS (adaptadores + checklist). | `browser_chat` → `terminal_agent` | `target_adoption` | `delegated_commit_pr` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / — | Sí |
| `templates/operations/02-bootstrap-new-project.md` | Draftear la estructura de adopción inicial y un issue de roadmap fundacional para un repo nuevo. | `browser_chat` | `target_adoption` | `review_only` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / `DESCRIPTION` | No |
| `templates/operations/03-verify-target-adoption.md` | Auditar read-only que la adopción existe, es correcta y referencia al kernel actual. | `browser_chat` / `terminal_agent` | `target_adoption` | `review_only` | `status_result` | `target_adoption` | `TARGET_REPOSITORY` / — | No |
| `templates/operations/04-draft-create-issue-command-from-description.md` | Convertir una descripción del PM en un bundle `gh issue create` con formato Project OS. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis` | `DESCRIPTION` / — | No |
| `templates/operations/05-review-project-state-and-misalignment.md` | Usar decisiones PM y docs fijos como verdad principal para hallar desalineaciones de roadmap/issues/código. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `PM_QUESTION` | No |
| `templates/operations/06-draft-create-next-issue-command-from-traceability.md` | Inferir el próximo outcome real desde la trazabilidad viva y draftear su `gh issue create`. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis`, `repo_state` | — / `ROADMAP_ISSUE` | No |
| `templates/operations/07-draft-issue-implementation-route-prompt.md` | Draftear un route-prompt para delegar la implementación de un issue a un terminal agent. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis`, `repo_state` | `ISSUE_NUMBER` / `ROADMAP_ISSUE` | No |
| `templates/operations/08-draft-review-correction-route-prompt.md` | Encapsular feedback humano en un route-prompt de corrección sin expandir el scope. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis`, `repo_state` | `ISSUE_NUMBER`, `FEEDBACK_PM_HUMANO` / — | No |
| `templates/operations/09-review-pr-before-close-and-draft-package.md` | Comparar la implementación del PR contra el issue vinculado y, solo si resuelve, draftear el cierre. | `browser_chat` | `review_before_close` | `review_only` | `review_result` (+`pm_command_bundle`) | `issue_scope`, `pr_diff`, `validation_output` | `PR_NUMBER` / — | No |
| `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` | Draftear el paquete común de cierre de PR/issue según el estado vivo. | `browser_chat` → Humano PM | `review_before_close` | `review_only` | `pm_command_bundle` | `issue_scope`, `pr_diff`, `validation_output` | `PR_NUMBER`, `ISSUE_NUMBER` / — | No |
| `templates/operations/11-verify-post-merge-state.md` | Comprobar read-only que la rama principal quedó saludable y el issue se resolvió tras el merge. | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `PR_NUMBER` / — | No |
| `templates/operations/12-analyze-release-or-tag-readiness.md` | Evaluar si el estado, los outcomes merged y la validación justifican un tag/release. | `browser_chat` | `release_readiness` | `review_only` | `status_result` | `repo_state`, `validation_output` | — / `TAG_NAME` | No |
| `templates/operations/13-draft-create-release-tag-command.md` | Draftear el bundle `git tag` + `git push --tags` basado en el readiness. | `browser_chat` → Humano PM | `release_readiness` | `review_only` | `pm_command_bundle` | `repo_state`, `validation_output` | — / `TAG_NAME` | Sí |
| `templates/operations/14-audit-target-adapters.md` | Detectar drift o modificaciones invasivas de adaptadores vs el modelo canónico (read-only). | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `TARGET_REPOSITORY` / — | No |
| `templates/operations/15-audit-issue-pr-traceability.md` | Verificar evidencia de cierre y trazabilidad completa de un issue (read-only). | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `ISSUE_NUMBER` / — | No |
| `templates/operations/16-review-idea-as-system-feature.md` | Evaluar la viabilidad de una idea como feature del sistema y proponer pasos. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | `IDEA` / — | No |
| `templates/operations/17-draft-handoff-package-for-new-session.md` | Empaquetar contexto vivo y decisiones PM para transferir a una sesión nueva. | `browser_chat` | `handoff` | `review_only` | `handoff_packet` | `repo_state` | — / — | No |
| `templates/operations/18-draft-human-qa-checklist.md` | Extraer requerimientos no automatizables a un checklist para un QA humano (no actor). | `browser_chat` → QA externo | `review_only` | `review_only` | `status_result` | `repo_state` | `ISSUE_NUMBER` / — | No |
| `templates/operations/19-request-external-design-assets.md` | Draftear un asset prompt para un destinatario de diseño (recipiente, no actor). | `browser_chat` → diseño externo | `design_asset` | `review_only` | `asset_prompt` | `repo_state`, `source_basis` | `DESCRIPTION` / — | No |
| `templates/operations/20-request-owasp-security-review.md` | Draftear un prompt de revisión OWASP con redacción obligatoria (recipiente, no actor). | `browser_chat` → seguridad externa | `security_revision` | `review_only` | `security_review_prompt` | `repo_state`, `source_basis` | `PR_NUMBER` / — | No |
| `templates/operations/21-draft-create-follow-up-from-review-command.md` | Aislar findings no bloqueantes de un review en un issue follow-up diferido. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis` | `PR_NUMBER` / — | No |
| `templates/operations/22-record-adr-decision.md` | Draftear contenido ADR y, si se escribe el archivo, un route-prompt que delega su creación. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis` | `DECISION` / — | Sí (escritura del archivo) |
| `templates/operations/23-upgrade-kernel-adoption-in-target.md` | Refrescar adaptadores de un target ya adoptado a una versión de kernel más reciente. | `browser_chat` → `terminal_agent` | `target_adoption` | `delegated_commit_pr` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / — | Sí |
| `templates/operations/24-draft-create-github-release-command.md` | Draftear el bundle `gh release create` (objeto Release: notas + tag), distinto del tag simple. | `browser_chat` → Humano PM | `release_readiness` | `review_only` | `pm_command_bundle` | `repo_state`, `validation_output` | — / `TAG_NAME` | Sí |
| `templates/operations/25-audit-implementation-discipline-gaps.md` | Auditar read-only brechas de implementación contra `boundary.implementation_discipline`. | `browser_chat` / `terminal_agent` | `implementation_discipline_audit` | `review_only` | `review_result` (+`draft_issue`) | `repo_state` | `TARGET_REPOSITORY` / `PATH_SCOPE`, `FOCUS`, `ISSUE_NUMBER`, `PR_NUMBER` | No |
| `templates/operations/26-draft-docs-from-conversation.md` | Convertir contexto conversacional del PM en contenido docs, issue draft o route-prompt de escritura exacta. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` (+`draft_issue`) | `source_basis` | `CONVERSATION_CONTEXT` / `DOC_TARGET` | Sí (solo escritura del archivo) |
| `templates/operations/27-draft-roadmap-from-docs.md` | Leer docs estables y draftear un roadmap issue body o bundle de creación/actualización. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `draft_issue` (+`pm_command_bundle`) | `source_basis`, `repo_state` | `SOURCE_DOCS` / `TARGET_REPOSITORY`, `ROADMAP_ACTION` | Sí (solo GitHub write) |
| `templates/operations/28-draft-docs-from-description.md` | Draftear documentación desde una descripción PM y routear creación de archivo solo con aprobación exacta. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` (+`draft_issue`) | `source_basis` | `DESCRIPTION` / `DOC_TARGET` | Sí (solo escritura del archivo) |
| `templates/operations/29-draft-bounded-roadmap-issues-command.md` | Draftear issues acotados desde roadmap con `ISSUE_COUNT_LIMIT` o `SCOPE_LIMIT`, uno por outcome. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis`, `repo_state` | `ROADMAP_ISSUE` + (`ISSUE_COUNT_LIMIT` o `SCOPE_LIMIT`) / — | No |

Cuando una operación emite `route_prompt` o `pm_command_bundle`, la forma del
artefacto vive una sola vez en su template canónico (`templates/route-prompt.md`,
`templates/pm-command-bundle.md`); los templates de operación apuntan ahí y no
duplican esas reglas.

## Cobertura de operaciones

Este catálogo contiene **30 templates** (`00`–`29`). Cada uno es un prompt de
operación ejecutable; ninguno permanece en el formato de ficha descriptiva
(*Objetivo / Detalle / Superficie / Configuración / Variables*).

**Transformaciones PM añadidas**:

- *Conversation-to-docs* → `templates/operations/26-draft-docs-from-conversation.md`.
  Extrae decisiones y contenido estable desde contexto conversacional y routea
  escritura de archivo solo cuando existe aprobación PM exacta.
- *Docs-to-roadmap* → `templates/operations/27-draft-roadmap-from-docs.md`.
  Convierte docs/source basis estables en roadmap issue body o bundle de
  creación/actualización PM-facing.
- *Docs-from-description* → `templates/operations/28-draft-docs-from-description.md`.
  Draftea documentación desde descripción del PM y usa route-prompt solo para
  escritura terminal aprobada.
- *Bounded roadmap-to-issues* → `templates/operations/29-draft-bounded-roadmap-issues-command.md`.
  Complementa `06` sin reemplazarlo: exige `ISSUE_COUNT_LIMIT` o `SCOPE_LIMIT`,
  y mantiene un issue por outcome.

**Familias restauradas** (no fueron autorizadas para eliminarse):

- *Upgrade kernel adoption* → `templates/operations/23-upgrade-kernel-adoption-in-target.md`.
  Actualiza un target ya adoptado a una versión de kernel más reciente, distinta
  de la verificación read-only de `03` y de la auditoría de drift de `14`.
- *GitHub release object* → `templates/operations/24-draft-create-github-release-command.md`.
  Publica un objeto Release de GitHub (`gh release create`, notas + tag),
  distinto del tag de git simple de `13`.
- *Implementation discipline audit* → `templates/operations/25-audit-implementation-discipline-gaps.md`.
  Revisa código o PRs contra `boundary.implementation_discipline` con evidencia
  de archivos/líneas y produce findings o drafts de follow-up sin mutar el target.

**Cierre de PR/issue**: las operaciones `09` y `10` emiten `pm_command_bundle`
bajo `workflow.review_before_close` por decisión del PM; el paquete común de
cierre (comentarios faltantes, mark-ready, merge, cierre, limpieza remota/local)
es drafteo PM-facing, no ejecución del agente. El Humano PM ejecuta el bundle.

**Nota de operaciones eliminadas**: la operación ficticia de configuración del
terminal agent fue removida y su guía vive en `docs/GETTING_STARTED.md`. Los terminal
agents se ejecutan a través de route-prompts post-adopción; no existe una
operación PM-facing de configuración del agente.

## Orientación de Flujo de Ciclo de Vida (Lifecycle Flow Guidance)

Project OS no es un runtime ni un motor de workflow enforcado por software. El flujo del ciclo de vida se basa en la lectura del estado vivo (GitHub/git) y se facilita a través del bloque `RECOMMENDED_NEXT_OPERATION` en cada template, permitiendo al Humano PM encadenar tareas lógicamente sin restricciones de máquina de estados.

El ciclo típico sigue este patrón:
1. **Intake y Planificación**: Las operaciones (04, 06, 29, 27) generan bundles de comandos para crear issues acotados en GitHub.
2. **Delegación**: A partir de un issue vivo, las operaciones (07, 22, 26, 28) emiten `route_prompt` para delegar el trabajo a un Terminal Agent.
3. **Revisión y Corrección**: El PR resultante es evaluado (09). Si hay faltantes, se emite una corrección (08); si se detectan problemas mayores, se audita (25) o se solicitan revisiones externas (20).
4. **Cierre**: Un PR validado produce un bundle de cierre (10) ejecutado por el PM, seguido de una verificación post-merge (11).
5. **Auditoría y Releases**: Finalmente, se evalúa la preparación (12) y se draftea el release o tag (13, 24).

### Justificación de Variables Discursivas
- `PM_QUESTION` (en 00, 05): Es estrictamente opcional. Su uso está justificado únicamente para contextualizar el draft-only analysis con base en el `repo_state` vivo y la evidencia. Nunca se utiliza para proveer directivas de implementación o saltar boundaries.
- `FEEDBACK_PM_HUMANO` (en 08): Es requerida para esta operación. Sirve exclusivamente para encapsular y documentar las correcciones solicitadas sobre un PR abierto sin expandir el scope original del issue. Garantiza trazabilidad entre el humano que revisa y el agente de terminal que aplica el fix.
