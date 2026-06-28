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
| `templates/operations/00-activar-sesion-browser-chat.md` | Establecer el contexto de sesión draft-only del PM en browser chat. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `PM_QUESTION` | No |
| `templates/operations/01-adoptar-project-os-en-target-existente.md` | Preparar un repositorio existente para operar con Project OS (adaptadores + checklist). | `browser_chat` → `terminal_agent` | `target_adoption` | `delegated_commit_pr` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / — | Sí |
| `templates/operations/02-iniciar-bootstrap-nuevo-proyecto.md` | Draftear la estructura de adopción inicial y un issue de roadmap fundacional para un repo nuevo. | `browser_chat` | `target_adoption` | `review_only` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / `DESCRIPTION` | No |
| `templates/operations/03-verificar-adopcion-en-repositorio-target.md` | Auditar read-only que la adopción existe, es correcta y referencia al kernel actual. | `browser_chat` / `terminal_agent` | `target_adoption` | `review_only` | `status_result` | `target_adoption` | `TARGET_REPOSITORY` / — | No |
| `templates/operations/04-draftear-comando-crear-issue-desde-descripcion.md` | Convertir una descripción del PM en un bundle `gh issue create` con formato Project OS. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis` | `DESCRIPTION` / — | No |
| `templates/operations/05-revisar-estado-del-proyecto-y-desalineaciones.md` | Usar decisiones PM y docs fijos como verdad principal para hallar desalineaciones de roadmap/issues/código. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `PM_QUESTION` | No |
| `templates/operations/06-draftear-comando-crear-siguiente-issue-desde-trazabilidad.md` | Inferir el próximo outcome real desde la trazabilidad viva y draftear su `gh issue create`. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis`, `repo_state` | — / `ROADMAP_ISSUE` | No |
| `templates/operations/07-draftear-route-prompt-para-implementar-issue.md` | Draftear un route-prompt para delegar la implementación de un issue a un terminal agent. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis`, `repo_state` | `ISSUE_NUMBER` / `ROADMAP_ISSUE` | No |
| `templates/operations/08-draftear-route-prompt-para-correcciones-de-review.md` | Encapsular feedback humano en un route-prompt de corrección sin expandir el scope. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis`, `repo_state` | `ISSUE_NUMBER`, `FEEDBACK_PM_HUMANO` / — | No |
| `templates/operations/09-revisar-pr-antes-de-cierre-y-draftear-paquete.md` | Comparar la implementación del PR contra el issue vinculado y, solo si resuelve, draftear el cierre. | `browser_chat` | `review_before_close` | `review_only` | `review_result` (+`pm_command_bundle`) | `issue_scope`, `pr_diff`, `validation_output` | `PR_NUMBER` / — | No |
| `templates/operations/10-draftear-comando-cierre-de-pr-y-limpieza.md` | Draftear el paquete común de cierre de PR/issue según el estado vivo. | `browser_chat` → Humano PM | `review_before_close` | `review_only` | `pm_command_bundle` | `issue_scope`, `pr_diff`, `validation_output` | `PR_NUMBER`, `ISSUE_NUMBER` / — | No |
| `templates/operations/11-verificar-estado-post-merge.md` | Comprobar read-only que la rama principal quedó saludable y el issue se resolvió tras el merge. | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `PR_NUMBER` / — | No |
| `templates/operations/12-analizar-readiness-para-release-o-tag.md` | Evaluar si el estado, los outcomes merged y la validación justifican un tag/release. | `browser_chat` | `release_readiness` | `review_only` | `status_result` | `repo_state`, `validation_output` | — / `TAG_NAME` | No |
| `templates/operations/13-draftear-comando-para-crear-release-tag.md` | Draftear el bundle `git tag` + `git push --tags` basado en el readiness. | `browser_chat` → Humano PM | `release_readiness` | `review_only` | `pm_command_bundle` | `repo_state`, `validation_output` | — / `TAG_NAME` | Sí |
| `templates/operations/14-auditar-adaptadores-en-target.md` | Detectar drift o modificaciones invasivas de adaptadores vs el modelo canónico (read-only). | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `TARGET_REPOSITORY` / — | No |
| `templates/operations/15-auditar-trazabilidad-de-issues-y-prs.md` | Verificar evidencia de cierre y trazabilidad completa de un issue (read-only). | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `ISSUE_NUMBER` / — | No |
| `templates/operations/16-analizar-idea-como-feature-del-sistema.md` | Evaluar la viabilidad de una idea como feature del sistema y proponer pasos. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | `IDEA` / — | No |
| `templates/operations/17-draftear-paquete-de-handoff-para-nueva-sesion.md` | Empaquetar contexto vivo y decisiones PM para transferir a una sesión nueva. | `browser_chat` | `handoff` | `review_only` | `handoff_packet` | `repo_state` | — / — | No |
| `templates/operations/18-draftear-checklist-de-qa-humano.md` | Extraer requerimientos no automatizables a un checklist para un QA humano (no actor). | `browser_chat` → QA externo | `review_only` | `review_only` | `status_result` | `repo_state` | `ISSUE_NUMBER` / — | No |
| `templates/operations/19-solicitar-assets-de-diseno-externos.md` | Draftear un asset prompt para un destinatario de diseño (recipiente, no actor). | `browser_chat` → diseño externo | `design_asset` | `review_only` | `asset_prompt` | `repo_state`, `source_basis` | `DESCRIPTION` / — | No |
| `templates/operations/20-solicitar-revision-de-seguridad-owasp.md` | Draftear un prompt de revisión OWASP con redacción obligatoria (recipiente, no actor). | `browser_chat` → seguridad externa | `security_revision` | `review_only` | `security_review_prompt` | `repo_state`, `source_basis` | `PR_NUMBER` / — | No |
| `templates/operations/21-draftear-comando-crear-follow-up-desde-review.md` | Aislar findings no bloqueantes de un review en un issue follow-up diferido. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis` | `PR_NUMBER` / — | No |
| `templates/operations/22-registrar-decision-adr.md` | Draftear contenido ADR y, si se escribe el archivo, un route-prompt que delega su creación. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis` | `DECISION` / — | Sí (escritura del archivo) |
| `templates/operations/23-actualizar-adopcion-de-kernel-en-target.md` | Refrescar adaptadores de un target ya adoptado a una versión de kernel más reciente. | `browser_chat` → `terminal_agent` | `target_adoption` | `delegated_commit_pr` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / — | Sí |
| `templates/operations/24-draftear-comando-crear-release-github.md` | Draftear el bundle `gh release create` (objeto Release: notas + tag), distinto del tag simple. | `browser_chat` → Humano PM | `release_readiness` | `review_only` | `pm_command_bundle` | `repo_state`, `validation_output` | — / `TAG_NAME` | Sí |

Cuando una operación emite `route_prompt` o `pm_command_bundle`, la forma del
artefacto vive una sola vez en su template canónico (`templates/route-prompt.md`,
`templates/pm-command-bundle.md`); los templates de operación apuntan ahí y no
duplican esas reglas.

## Cobertura de operaciones

Este catálogo contiene **25 templates** (`00`–`24`). Cada uno es un prompt de
operación ejecutable; ninguno permanece en el formato de ficha descriptiva
(*Objetivo / Detalle / Superficie / Configuración / Variables*).

**Familias restauradas** (no fueron autorizadas para eliminarse):

- *Upgrade kernel adoption* → `templates/operations/23-actualizar-adopcion-de-kernel-en-target.md`.
  Actualiza un target ya adoptado a una versión de kernel más reciente, distinta
  de la verificación read-only de `03` y de la auditoría de drift de `14`.
- *GitHub release object* → `templates/operations/24-draftear-comando-crear-release-github.md`.
  Publica un objeto Release de GitHub (`gh release create`, notas + tag),
  distinto del tag de git simple de `13`.

**Cierre de PR/issue**: las operaciones `09` y `10` emiten `pm_command_bundle`
bajo `workflow.review_before_close` por decisión del PM; el paquete común de
cierre (comentarios faltantes, mark-ready, merge, cierre, limpieza remota/local)
es drafteo PM-facing, no ejecución del agente. El Humano PM ejecuta el bundle.

**Nota de operaciones eliminadas**: la operación ficticia de setup de terminal
agent fue removida y su guía vive en `docs/GETTING_STARTED.md`. Los terminal
agents se ejecutan a través de route-prompts post-adopción; no existe una
operación PM-facing de "setup" del agente.
