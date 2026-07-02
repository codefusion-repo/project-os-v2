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

Arquitectura final de docs de operaciones:

- `docs/PM_OPERATIONS.md` es el índice canónico, matriz de variables y referencia
  técnica de templates.
- `docs/OPERATION_FLOWS.md` es el manual PM-facing de fase SDLC: cuándo usar cada
  operación, qué evidencia requiere, qué output emite, cómo falla cerrado, qué
  aprobación PM aplica y cuál es la siguiente operación segura.
- `docs/MOSDLC_OPERATION_MAP.md` es el mapa objetivo MOSDLC (MOSDLC.0): clasifica
  cada operación PM-written y recomendada aceptada respecto a este catálogo sin
  renumerar ni eliminar templates. Este catálogo `00`–`37` sigue siendo el
  canónico vigente hasta que cada lote de migración MOSDLC se apruebe por issue
  separado.

La división evita duplicar la tabla canónica de templates dentro de un manual de
flujo más largo. Ambos docs apuntan a las mismas operaciones `00`–`37`; ninguno
renumera, autoriza escritura ni guarda estado vivo.

## Migracion MOSDLC

El estandar de migracion vive en `docs/MOSDLC_TEMPLATE_STANDARD.md`.
Los templates MOSDLC migrados se agregan bajo
`templates/mosdlc/operations/fase-<n>/`; el catalogo `00`-`37` permanece usable
como fuente de reemplazo y compatibilidad. La migracion de una fase agrega
templates, docs y tests; no agrega ids de kernel ni cambia autorizacion por si
misma.

Fase 0, Fase 1, Fase 2 y Fase 3 son los lotes migrados. Sus templates son prompts
ejecutables con la misma disciplina de bloques (`MOSDLC`, `OPERATION`, `INPUT`,
`KERNEL`, `COMPATIBILITY_SOURCE`, `LIVE_STATE`, `DO`, `OUTPUT`, `LIMITS`,
`RECOMMENDED_NEXT_OPERATION`) y todos incluyen `PM_FEEDBACK_HUMANO` y
`PM_QUESTION_HUMANO` como contexto opcional. El wizard local sigue leyendo
`templates/operations/` como catalogo interactivo vigente hasta que otro issue
apruebe cambios de wizard o catalogo interactivo.

| MOSDLC ID | Operacion | Template MOSDLC | Fuente 00-37 |
|---|---|---|---|
| MOS-0.1 | activate-browser-session | `templates/mosdlc/operations/fase-0/MOS-0.1-activate-browser-session.md` | `templates/operations/00-browser-chat-activation.md` |
| MOS-0.2 | bootstrap-new-project | `templates/mosdlc/operations/fase-0/MOS-0.2-bootstrap-new-project.md` | `templates/operations/02-bootstrap-new-project.md` |
| MOS-0.3 | adopt-existing-project | `templates/mosdlc/operations/fase-0/MOS-0.3-adopt-existing-project.md` | `templates/operations/01-adopt-project-os-in-existing-target.md` |
| MOS-0.4 | update-project-adoption | `templates/mosdlc/operations/fase-0/MOS-0.4-update-project-adoption.md` | `templates/operations/23-upgrade-kernel-adoption-in-target.md` |
| MOS-0.5 | verify-target-adoption | `templates/mosdlc/operations/fase-0/MOS-0.5-verify-target-adoption.md` | `templates/operations/03-verify-target-adoption.md` |
| MOS-0.6 | handoff-session-context | `templates/mosdlc/operations/fase-0/MOS-0.6-handoff-session-context.md` | `templates/operations/17-draft-handoff-package-for-new-session.md` |
| MOS-1.1 | interview-requirements | `templates/mosdlc/operations/fase-1/MOS-1.1-interview-requirements.md` | — |
| MOS-1.2 | summarize-requirements | `templates/mosdlc/operations/fase-1/MOS-1.2-summarize-requirements.md` | — |
| MOS-1.3 | verify-requirements-feasibility | `templates/mosdlc/operations/fase-1/MOS-1.3-verify-requirements-feasibility.md` | `templates/operations/16-review-idea-as-system-feature.md` |
| MOS-1.4 | draft-requirements-docs | `templates/mosdlc/operations/fase-1/MOS-1.4-draft-requirements-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-1.5 | validate-requirements-docs | `templates/mosdlc/operations/fase-1/MOS-1.5-validate-requirements-docs.md` | — |
| MOS-1.6 | plan-project-roadmap | `templates/mosdlc/operations/fase-1/MOS-1.6-plan-project-roadmap.md` | `templates/operations/27-draft-roadmap-from-docs.md` |
| MOS-1.7 | review-idea-feasibility | `templates/mosdlc/operations/fase-1/MOS-1.7-review-idea-feasibility.md` | `templates/operations/16-review-idea-as-system-feature.md` |
| MOS-1.8 | update-docs-roadmap-with-requirement | `templates/mosdlc/operations/fase-1/MOS-1.8-update-docs-roadmap-with-requirement.md` | `templates/operations/27-draft-roadmap-from-docs.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-1.9 | review-requirement-removal | `templates/mosdlc/operations/fase-1/MOS-1.9-review-requirement-removal.md` | — |
| MOS-1.10 | extract-requirements-from-existing | `templates/mosdlc/operations/fase-1/MOS-1.10-extract-requirements-from-existing.md` | — |
| MOS-1.11 | update-requirements-docs-existing | `templates/mosdlc/operations/fase-1/MOS-1.11-update-requirements-docs-existing.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-1.12 | update-roadmap-existing | `templates/mosdlc/operations/fase-1/MOS-1.12-update-roadmap-existing.md` | `templates/operations/27-draft-roadmap-from-docs.md` |
| MOS-2.1 | draft-architecture-diagrams | `templates/mosdlc/operations/fase-2/MOS-2.1-draft-architecture-diagrams.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.2 | draft-uiux-docs | `templates/mosdlc/operations/fase-2/MOS-2.2-draft-uiux-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.3 | draft-data-algorithms-docs | `templates/mosdlc/operations/fase-2/MOS-2.3-draft-data-algorithms-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.4 | draft-coding-standards-docs | `templates/mosdlc/operations/fase-2/MOS-2.4-draft-coding-standards-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.5 | draft-security-docs | `templates/mosdlc/operations/fase-2/MOS-2.5-draft-security-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.6 | validate-design-docs | `templates/mosdlc/operations/fase-2/MOS-2.6-validate-design-docs.md` | — |
| MOS-2.7 | inventory-design-docs | `templates/mosdlc/operations/fase-2/MOS-2.7-inventory-design-docs.md` | — |
| MOS-2.8 | audit-design-doc-gaps | `templates/mosdlc/operations/fase-2/MOS-2.8-audit-design-doc-gaps.md` | `templates/operations/05-review-project-state-and-misalignment.md` |
| MOS-2.9 | update-architecture-diagrams | `templates/mosdlc/operations/fase-2/MOS-2.9-update-architecture-diagrams.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.10 | update-uiux-docs | `templates/mosdlc/operations/fase-2/MOS-2.10-update-uiux-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.11 | update-data-algorithms-docs | `templates/mosdlc/operations/fase-2/MOS-2.11-update-data-algorithms-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.12 | update-coding-standards-docs | `templates/mosdlc/operations/fase-2/MOS-2.12-update-coding-standards-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.13 | update-security-docs | `templates/mosdlc/operations/fase-2/MOS-2.13-update-security-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` |
| MOS-2.14 | validate-updated-design-docs | `templates/mosdlc/operations/fase-2/MOS-2.14-validate-updated-design-docs.md` | — |
| MOS-3.1 | draft-next-issue-from-traceability | `templates/mosdlc/operations/fase-3/MOS-3.1-draft-next-issue-from-traceability.md` | `templates/operations/06-draft-create-next-issue-command-from-traceability.md` |
| MOS-3.2 | draft-bounded-issue-set | `templates/mosdlc/operations/fase-3/MOS-3.2-draft-bounded-issue-set.md` | `templates/operations/29-draft-bounded-roadmap-issues-command.md` |
| MOS-3.3 | draft-follow-up-issue | `templates/mosdlc/operations/fase-3/MOS-3.3-draft-follow-up-issue.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-3.4 | draft-implementation-route-prompt | `templates/mosdlc/operations/fase-3/MOS-3.4-draft-implementation-route-prompt.md` | `templates/operations/07-draft-issue-implementation-route-prompt.md` |
| MOS-3.5 | draft-correction-route-prompt | `templates/mosdlc/operations/fase-3/MOS-3.5-draft-correction-route-prompt.md` | `templates/operations/08-draft-review-correction-route-prompt.md` |
| MOS-3.6 | draft-closeout-commands | `templates/mosdlc/operations/fase-3/MOS-3.6-draft-closeout-commands.md` | `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` |
| MOS-3.7 | review-pr-before-close | `templates/mosdlc/operations/fase-3/MOS-3.7-review-pr-before-close.md` | `templates/operations/09-review-pr-before-close-and-draft-package.md` |
| MOS-3.8 | draft-issue-from-description | `templates/mosdlc/operations/fase-3/MOS-3.8-draft-issue-from-description.md` | `templates/operations/04-draft-create-issue-command-from-description.md` |
| MOS-3.9 | verify-post-merge | `templates/mosdlc/operations/fase-3/MOS-3.9-verify-post-merge.md` | `templates/operations/11-verify-post-merge-state.md` |
| MOS-3.10 | analyze-release-readiness | `templates/mosdlc/operations/fase-3/MOS-3.10-analyze-release-readiness.md` | `templates/operations/12-analyze-release-or-tag-readiness.md`, `templates/operations/13-draft-create-release-tag-command.md` |
| MOS-3.11 | draft-tag-commands | `templates/mosdlc/operations/fase-3/MOS-3.11-draft-tag-commands.md` | `templates/operations/13-draft-create-release-tag-command.md` |
| MOS-3.12 | draft-release-commands | `templates/mosdlc/operations/fase-3/MOS-3.12-draft-release-commands.md` | `templates/operations/24-draft-create-github-release-command.md` |
| MOS-3.13 | audit-traceability | `templates/mosdlc/operations/fase-3/MOS-3.13-audit-traceability.md` | `templates/operations/15-audit-issue-pr-traceability.md` |
| MOS-3.14 | process-traceability-audit | `templates/mosdlc/operations/fase-3/MOS-3.14-process-traceability-audit.md` | — |
| MOS-3.15 | request-2d-asset | `templates/mosdlc/operations/fase-3/MOS-3.15-request-2d-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.16 | request-3d-asset | `templates/mosdlc/operations/fase-3/MOS-3.16-request-3d-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.17 | request-audio-asset | `templates/mosdlc/operations/fase-3/MOS-3.17-request-audio-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.18 | request-video-asset | `templates/mosdlc/operations/fase-3/MOS-3.18-request-video-asset.md` | `templates/operations/19-request-external-design-assets.md` |
| MOS-3.19 | process-2d-asset-delivery | `templates/mosdlc/operations/fase-3/MOS-3.19-process-2d-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.20 | process-3d-asset-delivery | `templates/mosdlc/operations/fase-3/MOS-3.20-process-3d-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.21 | process-audio-asset-delivery | `templates/mosdlc/operations/fase-3/MOS-3.21-process-audio-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.22 | process-video-asset-delivery | `templates/mosdlc/operations/fase-3/MOS-3.22-process-video-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` |
| MOS-3.23 | request-security-review | `templates/mosdlc/operations/fase-3/MOS-3.23-request-security-review.md` | `templates/operations/20-request-owasp-security-review.md` |
| MOS-3.24 | audit-implementation-discipline | `templates/mosdlc/operations/fase-3/MOS-3.24-audit-implementation-discipline.md` | `templates/operations/25-audit-implementation-discipline-gaps.md` |
| MOS-3.25 | process-security-review | `templates/mosdlc/operations/fase-3/MOS-3.25-process-security-review.md` | `templates/operations/31-process-security-review-results.md` |
| MOS-3.26 | process-discipline-audit | `templates/mosdlc/operations/fase-3/MOS-3.26-process-discipline-audit.md` | — |
| MOS-3.27 | review-project-state | `templates/mosdlc/operations/fase-3/MOS-3.27-review-project-state.md` | `templates/operations/05-review-project-state-and-misalignment.md` |
| MOS-3.28 | draft-follow-up-from-audit | `templates/mosdlc/operations/fase-3/MOS-3.28-draft-follow-up-from-audit.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-3.29 | draft-follow-up-from-security | `templates/mosdlc/operations/fase-3/MOS-3.29-draft-follow-up-from-security.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` |
| MOS-3.30 | draft-manual-implementation-plan | `templates/mosdlc/operations/fase-3/MOS-3.30-draft-manual-implementation-plan.md` | `templates/operations/33-draft-manual-implementation-plan.md` |
| MOS-3.31 | process-manual-implementation-result | `templates/mosdlc/operations/fase-3/MOS-3.31-process-manual-implementation-result.md` | `templates/operations/34-process-manual-implementation-result.md` |

Estos templates no guardan estado vivo durable y no autorizan escritura. Browser
chat permanece draft-only; terminal agent escribe solo con aprobacion PM exacta,
evidence requerido, branch preflight, validacion y review-before-close cuando
aplique.

Las superficies (browser chat, terminal agent, Humano PM, destinatario externo)
aparecen en la columna **Superficie**. Las variables son selectores de contexto,
no autorización. En la tabla, los ids de workflow/mode/output/evidence se muestran
sin su prefijo de familia (`workflow.` / `mode.` / `output.` / `evidence.`); cada
uno resuelve a un id real del kernel.

| Template (`templates/operations/`) | Objetivo | Superficie | Workflow | Mode | Output | Evidence | Variables (Req / Opc) | Aprob. PM |
|---|---|---|---|---|---|---|---|---|
| `templates/operations/00-browser-chat-activation.md` | Establecer el contexto de sesión draft-only del PM en browser chat. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/01-adopt-project-os-in-existing-target.md` | Preparar un repositorio existente para operar con Project OS (adaptadores + checklist). | `browser_chat` → `terminal_agent` | `target_adoption` | `delegated_commit_pr` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí |
| `templates/operations/02-bootstrap-new-project.md` | Draftear la estructura de adopción inicial y un issue de roadmap fundacional para un repo nuevo. | `browser_chat` | `target_adoption` | `review_only` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / `DESCRIPTION`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/03-verify-target-adoption.md` | Auditar read-only que la adopción existe, es correcta y referencia al kernel actual. | `browser_chat` / `terminal_agent` | `target_adoption` | `review_only` | `status_result` | `target_adoption` | `TARGET_REPOSITORY` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/04-draft-create-issue-command-from-description.md` | Convertir una descripción del PM en un bundle `gh issue create` con formato Project OS. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis` | `DESCRIPTION` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/05-review-project-state-and-misalignment.md` | Usar decisiones PM y docs fijos como verdad principal para hallar desalineaciones de roadmap/issues/código. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/06-draft-create-next-issue-command-from-traceability.md` | Inferir el próximo outcome real desde la trazabilidad viva y draftear su `gh issue create`. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis`, `repo_state` | — / `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/07-draft-issue-implementation-route-prompt.md` | Draftear un route-prompt para delegar la implementación de un issue a un terminal agent. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis`, `repo_state` | — / `ISSUE_NUMBER`, `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/08-draft-review-correction-route-prompt.md` | Encapsular feedback humano en un route-prompt de corrección sin expandir el scope. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis`, `repo_state` | `ISSUE_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/09-review-pr-before-close-and-draft-package.md` | Comparar la implementación del PR contra el issue vinculado, consumir execution reports como evidence leads y, solo si resuelve, draftear el cierre. | `browser_chat` | `review_before_close` | `review_only` | `review_result` (+`pm_command_bundle`) | `issue_scope`, `pr_diff`, `validation_output` | `PR_NUMBER` / `EXECUTION_REPORT`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` | Draftear el paquete común de cierre de PR/issue según el estado vivo. | `browser_chat` → Humano PM | `review_before_close` | `review_only` | `pm_command_bundle` | `issue_scope`, `pr_diff`, `validation_output` | `PR_NUMBER`, `ISSUE_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/11-verify-post-merge-state.md` | Comprobar read-only que la rama principal quedó saludable y el issue se resolvió tras el merge. | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `PR_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/12-analyze-release-or-tag-readiness.md` | Evaluar si el estado, los outcomes merged y la validación justifican un tag/release. | `browser_chat` | `release_readiness` | `review_only` | `status_result` | `repo_state`, `validation_output` | — / `TAG_NAME`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/13-draft-create-release-tag-command.md` | Draftear el bundle `git tag` + `git push --tags` basado en el readiness. | `browser_chat` → Humano PM | `release_readiness` | `review_only` | `pm_command_bundle` | `repo_state`, `validation_output` | — / `TAG_NAME`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí |
| `templates/operations/14-audit-target-adapters.md` | Detectar drift o modificaciones invasivas de adaptadores vs el modelo canónico (read-only). | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `TARGET_REPOSITORY` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/15-audit-issue-pr-traceability.md` | Verificar evidencia de cierre y trazabilidad completa de un issue (read-only). | `browser_chat` / `terminal_agent` | `review_only` | `review_only` | `status_result` | `repo_state` | `ISSUE_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/16-review-idea-as-system-feature.md` | Evaluar la viabilidad de una idea como feature del sistema y proponer pasos. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | `IDEA` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/17-draft-handoff-package-for-new-session.md` | Empaquetar contexto vivo y decisiones PM para transferir a una sesión nueva. | `browser_chat` | `handoff` | `review_only` | `handoff_packet` | `repo_state` | — / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/18-draft-human-qa-checklist.md` | Extraer requerimientos no automatizables a un checklist para un QA humano (no actor). | `browser_chat` → QA externo | `review_only` | `review_only` | `status_result` | `repo_state` | `ISSUE_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/19-request-external-design-assets.md` | Draftear un asset prompt para un destinatario de diseño (recipiente, no actor). | `browser_chat` → diseño externo | `design_asset` | `review_only` | `asset_prompt` | `repo_state`, `source_basis` | `DESCRIPTION` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/20-request-owasp-security-review.md` | Draftear un prompt de revisión OWASP con redacción obligatoria (recipiente, no actor). | `browser_chat` → seguridad externa | `security_revision` | `review_only` | `security_review_prompt` | `repo_state`, `source_basis` | `PR_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/21-draft-create-follow-up-from-review-command.md` | Aislar findings no bloqueantes de un review en un issue follow-up diferido. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis` | `PR_NUMBER` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/22-record-adr-decision.md` | Draftear contenido ADR y, si se escribe el archivo, un route-prompt que delega su creación. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` | `source_basis` | `DECISION` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí (escritura del archivo) |
| `templates/operations/23-upgrade-kernel-adoption-in-target.md` | Refrescar adaptadores de un target ya adoptado a una versión de kernel más reciente. | `browser_chat` → `terminal_agent` | `target_adoption` | `delegated_commit_pr` | `adoption_packet` | `target_adoption` | `TARGET_REPOSITORY` / `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí |
| `templates/operations/24-draft-create-github-release-command.md` | Draftear el bundle `gh release create` (objeto Release: notas + tag), distinto del tag simple. | `browser_chat` → Humano PM | `release_readiness` | `review_only` | `pm_command_bundle` | `repo_state`, `validation_output` | — / `TAG_NAME`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí |
| `templates/operations/25-audit-implementation-discipline-gaps.md` | Auditar read-only brechas de implementación contra `boundary.implementation_discipline`. | `browser_chat` / `terminal_agent` | `implementation_discipline_audit` | `review_only` | `review_result` (+`draft_issue`) | `repo_state` | `TARGET_REPOSITORY` / `PATH_SCOPE`, `FOCUS`, `ISSUE_NUMBER`, `PR_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/26-draft-docs-from-conversation.md` | Convertir contexto conversacional del PM en contenido docs, issue draft o route-prompt de escritura exacta. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` (+`draft_issue`) | `source_basis` | `CONVERSATION_CONTEXT` / `DOC_TARGET`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí (solo escritura del archivo) |
| `templates/operations/27-draft-roadmap-from-docs.md` | Leer docs estables y draftear un roadmap issue body o bundle de creación/actualización. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `draft_issue` (+`pm_command_bundle`) | `source_basis`, `repo_state` | `SOURCE_DOCS` / `TARGET_REPOSITORY`, `ROADMAP_ACTION`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí (solo GitHub write) |
| `templates/operations/28-draft-docs-from-description.md` | Draftear documentación desde una descripción PM y routear creación de archivo solo con aprobación exacta. | `browser_chat` → `terminal_agent` | `pm_intake` | `review_only` | `route_prompt` (+`draft_issue`) | `source_basis` | `DESCRIPTION` / `DOC_TARGET`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | Sí (solo escritura del archivo) |
| `templates/operations/29-draft-bounded-roadmap-issues-command.md` | Draftear issues acotados desde roadmap con `ISSUE_COUNT_LIMIT` o `SCOPE_LIMIT`, uno por outcome. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `pm_command_bundle` | `source_basis`, `repo_state` | `ROADMAP_ISSUE` / `ISSUE_COUNT_LIMIT`, `SCOPE_LIMIT`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/30-process-human-qa-results.md` | Procesar resultados de ejecución de QA humano y draftear route-prompt de corrección o follow-up. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `route_prompt` (+`pm_command_bundle`, `status_result`) | `repo_state`, `source_basis` | `QA_RESULT` / `ISSUE_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/31-process-security-review-results.md` | Procesar resultados de revisión de seguridad y draftear route-prompt de corrección o follow-up. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `route_prompt` (+`pm_command_bundle`, `status_result`) | `repo_state`, `source_basis` | `SECURITY_REVIEW_RESULT` / `PR_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/32-process-design-asset-delivery.md` | Procesar entrega de assets o feedback de diseño y mapearlo a tareas técnicas o drafts. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `route_prompt` (+`pm_command_bundle`, `status_result`) | `repo_state`, `source_basis` | `DESIGN_DELIVERY` / `ISSUE_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/33-draft-manual-implementation-plan.md` | Draftear un plan de implementación humano-ejecutable para un issue scoped sin afirmar ejecución ni mutar repositorios. | `browser_chat` → Humano PM | `issue_implementation_manual` | `review_only` | `manual_implementation_plan` | `issue_scope`, `source_basis`, `repo_state` | `ISSUE_NUMBER` / `TARGET_REPOSITORY`, `PATH_SCOPE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/34-process-manual-implementation-result.md` | Clasificar el resultado de una implementación manual aplicada por humano y recomendar la ruta segura sin duplicar review de PR. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `status_result` (+`route_prompt`, `pm_command_bundle`) | `issue_scope`, `source_basis`, `repo_state` | `ISSUE_NUMBER`, `MANUAL_IMPLEMENTATION_RESULT` / `MANUAL_IMPLEMENTATION_PLAN`, `PR_NUMBER`, `TARGET_REPOSITORY`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/35-recommend-next-lifecycle-operation.md` | Recomendar la siguiente operación Project OS desde trazabilidad viva sin ejecutar ni draftear el siguiente paso. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `TARGET_REPOSITORY`, `ISSUE_NUMBER`, `PR_NUMBER`, `ROADMAP_ISSUE`, `CURRENT_STATUS`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/36-process-needs-pm-decision.md` | Procesar un `status.needs_pm_decision` desde la operación originaria y clasificar decisión PM, contexto faltante, corrección, follow-up, no-op o route prompt. | `browser_chat` → Humano PM | `pm_intake` | `review_only` | `status_result` (+`route_prompt`, `pm_command_bundle`, `draft_issue`) | `source_basis`, `repo_state` | `ORIGINATING_OPERATION`, `STATUS_CONTEXT`, `OPTIONS_TRADEOFFS` / `ISSUE_NUMBER`, `PR_NUMBER`, `TARGET_REPOSITORY`, `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |
| `templates/operations/37-review-phase-readiness.md` | Revisar readiness advisory antes de pasar a implementación, QA/security/design, closeout, release, dogfood o handoff. | `browser_chat` | `review_only` | `review_only` | `status_result` | `repo_state` | — / `CURRENT_PHASE`, `TARGET_PHASE`, `ISSUE_NUMBER`, `PR_NUMBER`, `TARGET_REPOSITORY`, `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | No |

Cuando una operación emite `route_prompt` o `pm_command_bundle`, la forma del
artefacto vive una sola vez en su template canónico (`templates/route-prompt.md`,
`templates/pm-command-bundle.md`); los templates de operación apuntan ahí y no
duplican esas reglas.


## Matriz de Variables de Operación (Operation-Variable Matrix)

Esta matriz detalla estrictamente las variables requeridas, opcionales (incluyendo discursivas) y la próxima operación recomendada para cada template, alineadas al catálogo.

| Template | Req Variables | Opt Variables | Discursive | Recommended Next Operation |
|----------|---------------|---------------|------------|----------------------------|
| 00 | (none) | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 01, 02, 05, or intake/audit |
| 01 | TARGET_REPOSITORY | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 03 |
| 02 | TARGET_REPOSITORY | DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 03 |
| 03 | TARGET_REPOSITORY | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 05, 06, or 14 |
| 04 | DESCRIPTION | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 07 |
| 05 | (none) | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 06, 29, or 21 |
| 06 | (none) | ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 07 |
| 07 | (none) | ISSUE_NUMBER, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 09 or 08 |
| 08 | ISSUE_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 09 |
| 09 | PR_NUMBER | EXECUTION_REPORT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 10 or 08 |
| 10 | PR_NUMBER, ISSUE_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 11 |
| 11 | PR_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 06 or 12 |
| 12 | (none) | TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 13 or 24 |
| 13 | (none) | TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | Human PM executes |
| 14 | TARGET_REPOSITORY | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 23 or manual correction |
| 15 | ISSUE_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 08 or 21 |
| 16 | IDEA | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 04 or 28 |
| 17 | (none) | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 00 |
| 18 | ISSUE_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 09 or 08 |
| 19 | DESCRIPTION | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 07 |
| 20 | PR_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 08 |
| 21 | PR_NUMBER | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 07 |
| 22 | DECISION | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 06 or 07 |
| 23 | TARGET_REPOSITORY | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 03 |
| 24 | (none) | TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | Human PM executes |
| 25 | TARGET_REPOSITORY | PATH_SCOPE, FOCUS, ISSUE_NUMBER, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 08 or 21 |
| 26 | CONVERSATION_CONTEXT | DOC_TARGET, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | Terminal Agent executes or 28 |
| 27 | SOURCE_DOCS | TARGET_REPOSITORY, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 06 or 29 |
| 28 | DESCRIPTION | DOC_TARGET, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | Terminal Agent executes, then 09 |
| 29 | ROADMAP_ISSUE | ISSUE_COUNT_LIMIT, SCOPE_LIMIT, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 07 |
| 30 | QA_RESULT | ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 08, 21, or 09 |
| 31 | SECURITY_REVIEW_RESULT | PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 08, 21, or 09 |
| 32 | DESIGN_DELIVERY | ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 07, 08, 04, or 21 |
| 33 | ISSUE_NUMBER | TARGET_REPOSITORY, PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 34, 09, 08, or 21 |
| 34 | ISSUE_NUMBER, MANUAL_IMPLEMENTATION_RESULT | MANUAL_IMPLEMENTATION_PLAN, PR_NUMBER, TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 09, 08, 21, 36, 37, or QA/security/design gates |
| 35 | (none) | TARGET_REPOSITORY, ISSUE_NUMBER, PR_NUMBER, ROADMAP_ISSUE, CURRENT_STATUS, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | Human PM invokes recommended operation |
| 36 | ORIGINATING_OPERATION, STATUS_CONTEXT, OPTIONS_TRADEOFFS | ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | Originating operation, 08, 21, 35, or stop |
| 37 | (none) | CURRENT_PHASE, TARGET_PHASE, ISSUE_NUMBER, PR_NUMBER, TARGET_REPOSITORY, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO | 36, 35, or target-phase operation |

## Cobertura de operaciones

Este catálogo contiene **38 templates** (`00`–`37`). Cada uno es un prompt de
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
- *Manual-result processing* → `templates/operations/34-process-manual-implementation-result.md`.
  Procesa solo evidencia PM/manual posterior a `33`, clasifica la ruta segura y
  deriva a `09` cuando existe PR; no afirma que browser chat aplico o valido cambios.
- *Next lifecycle operation recommendation* → `templates/operations/35-recommend-next-lifecycle-operation.md`.
  Recomienda la proxima operacion desde trazabilidad viva y se detiene; nunca
  ejecuta, autoriza ni draftea el siguiente paso.
- *PM-decision status processing* → `templates/operations/36-process-needs-pm-decision.md`.
  Procesa `status.needs_pm_decision` desde la operacion originaria y devuelve
  decision PM, contexto faltante, correccion, follow-up, no-op o route prompt
  sin auto-aprobar ni ejecutar nada.
- *Phase readiness review* → `templates/operations/37-review-phase-readiness.md`.
  Revisa readiness advisory antes de cambiar de fase, identifica evidencia o
  decisiones faltantes y recomienda la siguiente operacion segura sin ejecutarla.

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

Para elegir por fase, usar `docs/OPERATION_FLOWS.md` como manual operativo. Este
catálogo conserva la matriz canónica de templates/variables; el manual de flujos
describe trigger, evidencia, output, aprobación PM, fail-closed, gaps de ciclo
de vida y la guía de route-prompt y wizard debe distinguir
`PM_AUTHORIZATION_STATUS=pending` de `PM_AUTHORIZATION_STATUS=granted for this
exact scope and mode`; draft/read-only/planning son modo o postura, no valores
de autorización.

El ciclo abarca todas las fases del ciclo de vida del desarrollo de software (SDLC) de forma flexible, permitiendo encadenarlas mediante `RECOMMENDED_NEXT_OPERATION`:
1. **Idea Intake y Requirements**: Se evalúan ideas (16) y se transforman en issues (04, 06) o documentación (28, 26, 27).
2. **Docs y Design**: Decisiones de arquitectura (22), assets de diseño externo (19) o documentación estable se draftean sin mutar inmediatamente la rama principal.
3. **Implementation**: El PM delega trabajo al Terminal Agent (07) para ejecutar commits y PRs acotados, usa el plan manual (33) cuando browser chat debe producir instrucciones humano-ejecutables sin escribir archivos, clasifica resultados manuales aplicados con 34 cuando no corresponde saltar directo a review de PR, y usa 37 para revisar readiness antes de pasar de fase.
4. **QA y Security**: Revisión de PR (09), checklists manuales de QA (18), análisis OWASP (20), y procesamiento de resultados QA/seguridad (30, 31) proveen gates de calidad.
5. **Assets y Mantenimiento**: Solicitudes y entregas de assets de diseño (19, 32), correcciones menores (08), y hallazgos sistémicos (25, 14, 15, 23) mantienen la integridad del kernel y del repositorio.
6. **Release, Follow-up y Handoff**: El PR se cierra (10) y verifica (11), los hallazgos no bloqueantes se difieren (21), decisiones `status.needs_pm_decision` se procesan con 36, se generan tags y releases (12, 13, 24), el contexto se transfiere a una nueva sesión (17), y la siguiente operación se recomienda sin ejecutarla (35).

### Cobertura KOPS.3

El fit check KOPS.3 comparo Project OS contra un SDLC practico antes de agregar
templates. El resultado no requiere nuevos ids de kernel: el procesamiento de
resultado manual y `status.needs_pm_decision` usan `workflow.pm_intake`; la
recomendacion de proxima operacion y readiness de fase usan
`workflow.review_only`.

Las operaciones post-gate cubren los tres gates externos que ya existian como
operaciones de solicitud: QA humano (`18` → `30`), revision de seguridad
(`20` → `31`) y assets/diseno (`19` → `32`). KOPS.3 agrega solo lo que no
duplicaba rutas existentes: la implementacion manual se planifica con `33` y su
resultado aplicado por humano se clasifica con `34`; la proxima operacion se
recomienda con `35` sin ejecutar nada; `status.needs_pm_decision` se procesa con
`36` sin auto-aprobar ni ejecutar; readiness de fase se revisa con `37` como
advisory/read-only; reportes de terminal agent y PRs se revisan en `09` con
`EXECUTION_REPORT` como evidence lead opcional; findings de review se convierten
en correccion con `08` o follow-up con `21`; fallas de validacion bloqueantes
vuelven por `08`; readiness de cierre vive en `09`/`10`; post-merge y release
viven en `11`/`12`/`13`/`24`; handoff vive en `17`.

El unico candidato KOPS.3 no agregado como operacion nueva es un procesador
normal de execution report para PRs, porque duplicaria `09`. Un procesador de
execution report fuera de PR requiere una decision PM exacta y un caso no
duplicativo antes de agregarse.

### Justificación de Variables Discursivas
- `PM_QUESTION_HUMANO`: Es la única variable canónica para preguntas del PM. Es
  opcional en todas las operaciones PM-facing para permitir interpretación,
  ruteo, aclaración, priorización, ajuste de roadmap, juicio de revisión o
  soporte de decisión. Nunca reemplaza evidencia viva requerida ni otorga
  permiso de escritura.
- `PM_FEEDBACK_HUMANO`: Es contexto humano opcional en todas las operaciones
  PM-facing. Puede orientar interpretación, foco, severidad o ruta, incluida la
  operación `08`, pero no reemplaza issue/PR/docs/evidencia viva requerida y no
  autoriza mutaciones.
- `PM_QUESTION` no es alias ni variable legacy aceptada. Cualquier uso debe
  tratarse como entrada inválida y corregirse a `PM_QUESTION_HUMANO`.
- Variables de resultado post-gate: `QA_RESULT`,
  `SECURITY_REVIEW_RESULT` y `DESIGN_DELIVERY` son los nombres canónicos. No se
  mantienen alias plurales ni pares `ASSET_FEEDBACK`/`DESIGN_FEEDBACK`; si un
  resultado contiene feedback, va dentro de la variable canónica correspondiente.
