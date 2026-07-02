# Operation Flows by SDLC Phase

Este documento es el manual PM-facing de flujo por fase. La arquitectura final
de docs de operaciones queda dividida en dos artefactos estables:

- `docs/PM_OPERATIONS.md`: indice canonico, matriz de variables y referencia
  tecnica de templates.
- `docs/OPERATION_FLOWS.md`: manual PM-facing para elegir la operacion correcta
  por fase SDLC, trigger, evidencia, output, fail-closed y siguiente paso.

La division evita duplicar la tabla canonica de templates dentro de un manual de
flujo mas largo: `PM_OPERATIONS.md` responde "que template existe y que contrato
tiene"; `OPERATION_FLOWS.md` responde "cuando lo uso y que sigue". Ambos apuntan
a los mismos templates y este archivo no cambia la numeracion `00`-`37`.

El modelo objetivo de operaciones es MOSDLC y vive en
`docs/MOSDLC_OPERATION_MAP.md` (MOSDLC.0): mapea cada operacion PM-written y
recomendada aceptada contra este catalogo sin eliminar ni renumerar nada. Este
manual y el catalogo `00`-`37` siguen siendo los vigentes hasta que la
migracion MOSDLC se apruebe por issues separados.

Project OS no es un motor de workflow. Cada operacion lee evidencia viva desde
GitHub/git cuando corresponde, resuelve `kernel/manifest.json`, aplica los
boundaries del kernel y emite el output declarado. Los docs y templates no
guardan estado vivo: no issue, PR, branch, commit, validacion, release ni
planificacion viva. Browser chat permanece draft-only; GitHub permanece como
source of truth para issues, PRs, comentarios, reviews, branches, commits y
validacion.

## Entry Shape

Cada fila del mapa usa esta forma estandar:

- Phase: fase SDLC principal.
- Trigger: senal PM o evidencia viva que inicia la operacion.
- Operation/template: numero existente y archivo bajo `templates/operations/`.
- Required evidence: ids de `kernel/evidence.json` requeridos o usados por la
  operacion.
- Variables: variables requeridas y opcionales; las variables humanas
  `PM_FEEDBACK_HUMANO` y `PM_QUESTION_HUMANO` son contexto opcional.
- Output contract: ids de `kernel/outputs.json` que la operacion emite.
- Safe next operation: siguiente operacion segura cuando la evidencia alcanza.
- Fail-closed behavior: estado seguro cuando falta evidencia, hay ambiguedad o
  existe conflicto.
- PM approval behavior: si la operacion solo draftea, si requiere aprobacion PM
  exacta para escritura, o si deja la ejecucion al Humano PM.

## MOSDLC Migration Flow

La migracion MOSDLC empieza por Fase 0 y continua por Fase 1, Fase 2 y Fase 3,
documentadas en `docs/MOSDLC_TEMPLATE_STANDARD.md`. Los templates migrados viven en
`templates/mosdlc/operations/fase-<n>/`; los templates `00`-`37` siguen siendo
el catalogo de compatibilidad vigente, no se eliminan, no se renombran y no se
renumeran.

| MOSDLC ID | Fase | Template MOSDLC | Fuente de compatibilidad | Safe next operation |
|---|---|---|---|---|
| MOS-0.1 | Adaptation | `templates/mosdlc/operations/fase-0/MOS-0.1-activate-browser-session.md` | `templates/operations/00-browser-chat-activation.md` | MOS-0.2, MOS-0.3, MOS-0.5 o MOS-0.6 segun contexto. |
| MOS-0.2 | Adaptation | `templates/mosdlc/operations/fase-0/MOS-0.2-bootstrap-new-project.md` | `templates/operations/02-bootstrap-new-project.md` | MOS-0.5. |
| MOS-0.3 | Adaptation | `templates/mosdlc/operations/fase-0/MOS-0.3-adopt-existing-project.md` | `templates/operations/01-adopt-project-os-in-existing-target.md` | MOS-0.5. |
| MOS-0.4 | Adaptation | `templates/mosdlc/operations/fase-0/MOS-0.4-update-project-adoption.md` | `templates/operations/23-upgrade-kernel-adoption-in-target.md` | MOS-0.5. |
| MOS-0.5 | Adaptation | `templates/mosdlc/operations/fase-0/MOS-0.5-verify-target-adoption.md` | `templates/operations/03-verify-target-adoption.md` | MOS-0.4 si hay drift; si no, la siguiente operacion elegida por el PM. |
| MOS-0.6 | Adaptation | `templates/mosdlc/operations/fase-0/MOS-0.6-handoff-session-context.md` | `templates/operations/17-draft-handoff-package-for-new-session.md` | MOS-0.1 en la nueva sesion. |
| MOS-1.1 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.1-interview-requirements.md` | — | MOS-1.2. |
| MOS-1.2 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.2-summarize-requirements.md` | — | MOS-1.3. |
| MOS-1.3 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.3-verify-requirements-feasibility.md` | `templates/operations/16-review-idea-as-system-feature.md` | MOS-1.4. |
| MOS-1.4 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.4-draft-requirements-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-1.5. |
| MOS-1.5 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.5-validate-requirements-docs.md` | — | MOS-1.6. |
| MOS-1.6 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.6-plan-project-roadmap.md` | `templates/operations/27-draft-roadmap-from-docs.md` | MOS-3.1 o MOS-3.2. |
| MOS-1.7 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.7-review-idea-feasibility.md` | `templates/operations/16-review-idea-as-system-feature.md` | MOS-1.8 si procede. |
| MOS-1.8 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.8-update-docs-roadmap-with-requirement.md` | `templates/operations/27-draft-roadmap-from-docs.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-3.1. |
| MOS-1.9 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.9-review-requirement-removal.md` | — | MOS-1.8 si el PM confirma. |
| MOS-1.10 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.10-extract-requirements-from-existing.md` | — | MOS-1.11. |
| MOS-1.11 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.11-update-requirements-docs-existing.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-1.12. |
| MOS-1.12 | Requirements, planning, and feasibility | `templates/mosdlc/operations/fase-1/MOS-1.12-update-roadmap-existing.md` | `templates/operations/27-draft-roadmap-from-docs.md` | MOS-3.1. |
| MOS-2.1 | Design | `templates/mosdlc/operations/fase-2/MOS-2.1-draft-architecture-diagrams.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.6. |
| MOS-2.2 | Design | `templates/mosdlc/operations/fase-2/MOS-2.2-draft-uiux-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.6. |
| MOS-2.3 | Design | `templates/mosdlc/operations/fase-2/MOS-2.3-draft-data-algorithms-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.6. |
| MOS-2.4 | Design | `templates/mosdlc/operations/fase-2/MOS-2.4-draft-coding-standards-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.6. |
| MOS-2.5 | Design | `templates/mosdlc/operations/fase-2/MOS-2.5-draft-security-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.6. |
| MOS-2.6 | Design | `templates/mosdlc/operations/fase-2/MOS-2.6-validate-design-docs.md` | — | MOS-R.4 y MOS-3.1. |
| MOS-2.7 | Design | `templates/mosdlc/operations/fase-2/MOS-2.7-inventory-design-docs.md` | — | MOS-2.8. |
| MOS-2.8 | Design | `templates/mosdlc/operations/fase-2/MOS-2.8-audit-design-doc-gaps.md` | `templates/operations/05-review-project-state-and-misalignment.md` | MOS-2.9 a MOS-2.13 segun gap. |
| MOS-2.9 | Design | `templates/mosdlc/operations/fase-2/MOS-2.9-update-architecture-diagrams.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.14. |
| MOS-2.10 | Design | `templates/mosdlc/operations/fase-2/MOS-2.10-update-uiux-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.14. |
| MOS-2.11 | Design | `templates/mosdlc/operations/fase-2/MOS-2.11-update-data-algorithms-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.14. |
| MOS-2.12 | Design | `templates/mosdlc/operations/fase-2/MOS-2.12-update-coding-standards-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.14. |
| MOS-2.13 | Design | `templates/mosdlc/operations/fase-2/MOS-2.13-update-security-docs.md` | `templates/operations/26-draft-docs-from-conversation.md`, `templates/operations/28-draft-docs-from-description.md` | MOS-2.14. |
| MOS-2.14 | Design | `templates/mosdlc/operations/fase-2/MOS-2.14-validate-updated-design-docs.md` | — | MOS-R.4 y MOS-3.1. |
| MOS-3.1 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.1-draft-next-issue-from-traceability.md` | `templates/operations/06-draft-create-next-issue-command-from-traceability.md` | MOS-3.4. |
| MOS-3.2 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.2-draft-bounded-issue-set.md` | `templates/operations/29-draft-bounded-roadmap-issues-command.md` | MOS-3.4. |
| MOS-3.3 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.3-draft-follow-up-issue.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` | MOS-3.4. |
| MOS-3.4 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.4-draft-implementation-route-prompt.md` | `templates/operations/07-draft-issue-implementation-route-prompt.md` | MOS-3.7 si hay PR. |
| MOS-3.5 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.5-draft-correction-route-prompt.md` | `templates/operations/08-draft-review-correction-route-prompt.md` | MOS-3.7 si hay PR. |
| MOS-3.6 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.6-draft-closeout-commands.md` | `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` | MOS-3.9. |
| MOS-3.7 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.7-review-pr-before-close.md` | `templates/operations/09-review-pr-before-close-and-draft-package.md` | MOS-3.6 si resuelve. |
| MOS-3.8 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.8-draft-issue-from-description.md` | `templates/operations/04-draft-create-issue-command-from-description.md` | MOS-3.4. |
| MOS-3.9 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.9-verify-post-merge.md` | `templates/operations/11-verify-post-merge-state.md` | MOS-3.1. |
| MOS-3.10 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.10-analyze-release-readiness.md` | `templates/operations/12-analyze-release-or-tag-readiness.md`, `templates/operations/13-draft-create-release-tag-command.md` | MOS-3.11. |
| MOS-3.11 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.11-draft-tag-commands.md` | `templates/operations/13-draft-create-release-tag-command.md` | MOS-3.12 si corresponde Release. |
| MOS-3.12 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.12-draft-release-commands.md` | `templates/operations/24-draft-create-github-release-command.md` | MOS-3.1. |
| MOS-3.13 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.13-audit-traceability.md` | `templates/operations/15-audit-issue-pr-traceability.md` | MOS-3.14. |
| MOS-3.14 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.14-process-traceability-audit.md` | — | MOS-3.3. |
| MOS-3.15 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.15-request-2d-asset.md` | `templates/operations/19-request-external-design-assets.md` | MOS-3.19. |
| MOS-3.16 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.16-request-3d-asset.md` | `templates/operations/19-request-external-design-assets.md` | MOS-3.20. |
| MOS-3.17 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.17-request-audio-asset.md` | `templates/operations/19-request-external-design-assets.md` | MOS-3.21. |
| MOS-3.18 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.18-request-video-asset.md` | `templates/operations/19-request-external-design-assets.md` | MOS-3.22. |
| MOS-3.19 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.19-process-2d-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` | MOS-3.4. |
| MOS-3.20 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.20-process-3d-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` | MOS-3.4. |
| MOS-3.21 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.21-process-audio-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` | MOS-3.4. |
| MOS-3.22 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.22-process-video-asset-delivery.md` | `templates/operations/32-process-design-asset-delivery.md` | MOS-3.4. |
| MOS-3.23 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.23-request-security-review.md` | `templates/operations/20-request-owasp-security-review.md` | MOS-3.25. |
| MOS-3.24 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.24-audit-implementation-discipline.md` | `templates/operations/25-audit-implementation-discipline-gaps.md` | MOS-3.26. |
| MOS-3.25 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.25-process-security-review.md` | `templates/operations/31-process-security-review-results.md` | MOS-3.5 para bloqueantes. |
| MOS-3.26 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.26-process-discipline-audit.md` | — | MOS-3.28. |
| MOS-3.27 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.27-review-project-state.md` | `templates/operations/05-review-project-state-and-misalignment.md` | MOS-R.9 si el drift es documental. |
| MOS-3.28 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.28-draft-follow-up-from-audit.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` | MOS-3.4. |
| MOS-3.29 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.29-draft-follow-up-from-security.md` | `templates/operations/21-draft-create-follow-up-from-review-command.md` | MOS-3.4. |
| MOS-3.30 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.30-draft-manual-implementation-plan.md` | `templates/operations/33-draft-manual-implementation-plan.md` | MOS-3.31. |
| MOS-3.31 | Development / Implementation | `templates/mosdlc/operations/fase-3/MOS-3.31-process-manual-implementation-result.md` | `templates/operations/34-process-manual-implementation-result.md` | MOS-3.7 si hay PR. |

Estas filas son superficie PM-facing de activacion, no un motor de workflow.
Cada template debe resolver `kernel/manifest.json`, leer estado vivo solo al
momento de ejecutar, fallar cerrado cuando falte evidencia, y declarar que el
template no autoriza escrituras. Cualquier escritura terminal sigue requiriendo
aprobacion PM exacta, evidence requerido, branch preflight, validacion y review.

## SDLC Comparison and KOPS.3 Fit Check

KOPS.3 compara Project OS contra un SDLC practico antes de agregar operaciones.
La decision es conservar el kernel compacto y expresar los gaps reales en
templates/docs/tests usando workflows y outputs existentes.

| SDLC area | Current coverage | KOPS.3 fit decision |
|---|---|---|
| Intake/requirements | 16, 04, 26, 28 convierten ideas, descripcion y conversacion en issues o docs. | Cubierto; solo docs de orientacion. |
| Planning/design | 27, 06, 29, 22 y 19 cubren roadmap, issues acotados, ADRs y assets. | Cubierto; no kernel nuevo. |
| Implementation | 07 routea terminal agent; 33 draftea plan manual no-write. | Cubierto para rutas de entrada; 34 se agrega solo para clasificar resultado manual posterior. |
| Manual implementation result processing | 33 no procesa lo que el humano aplico; 09 solo aplica cuando hay PR. | Nuevo Operation 34 con workflow.pm_intake, recommendation/draft-only, y ruta a 09 si existe PR. |
| PM decision processing | Los statuses `status.needs_pm_decision` volvian a chat sin una operacion uniforme. | Nuevo Operation 36 procesa la decision desde la operacion originaria sin auto-aprobar ni ejecutar. |
| Testing/QA/security/design gates | 18, 20, 30, 31 y 32 cubren solicitud y procesamiento de gates externos. | Cubierto; 34 puede recomendar estos gates sin ejecutarlos. |
| PR review/acceptance | 09 es review-before-close y consume execution reports como evidence leads cuando hay PR. | Docs/template/test guard; no operacion duplicada para execution report normal. |
| Closeout/release | 10, 11, 12, 13 y 24 cubren cierre, verificacion, tags y releases. | Cubierto; sin cambios. |
| Maintenance/follow-up | 21, 25, 14, 15 y 23 cubren follow-ups, audits y upgrades. | Cubierto; 34 puede derivar no bloqueantes a 21. |
| Handoff/evaluation and phase readiness | 17 transfiere contexto; 05 revisa estado; readiness entre fases era ad hoc. | Nuevo Operation 35 recomienda la siguiente operacion y nuevo Operation 37 revisa readiness; ambos son read-only/advisory y nunca ejecutan transiciones. |

El PM pidio agregar ahora las operaciones faltantes no duplicativas. El unico
candidato que no se agrega como operacion nueva es el procesador normal de
execution report para PRs, porque duplicaria Operation 09. Cualquier procesador
de execution report fuera de PR requiere decision PM exacta y un caso no
duplicativo antes de agregarse.

## Phase Flow Map

| Op | Phase | Trigger | Template | Required evidence | Variables | Output contract | Safe next operation | Fail-closed behavior | PM approval behavior |
|---|---|---|---|---|---|---|---|---|---|
| 00 | Activation and state review | Nueva sesion PM en browser chat. | `templates/operations/00-browser-chat-activation.md` | `evidence.repo_state` | Req: none; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 01, 02, 05, o intake/audit segun evidencia. | Si la superficie no es browser chat o falta contexto necesario, devolver `status.needs_context` o `status.blocked`. | No aprueba escritura; establece contexto draft-only. |
| 01 | Activation and state review | Repo target existente necesita adopcion Project OS. | `templates/operations/01-adopt-project-os-in-existing-target.md` | `evidence.target_adoption`, `evidence.branch_preflight`, `evidence.pm_approval`, `evidence.validation_output` | Req: `TARGET_REPOSITORY`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.adoption_packet`, `output.route_prompt` | 03 para verificar adopcion. | Si identidad target, evidencia de adopcion o aprobacion de escritura faltan, devolver `status.needs_context` o `status.blocked`. | Browser chat draftea; terminal agent escribe solo con aprobacion PM exacta. |
| 02 | Activation and state review | Proyecto nuevo necesita estructura inicial de adopcion. | `templates/operations/02-bootstrap-new-project.md` | `evidence.target_adoption` | Req: `TARGET_REPOSITORY`; Opt: `DESCRIPTION`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.adoption_packet` | 03 para verificar adopcion. | Si target o base inicial faltan o son ambiguos, devolver `status.needs_context`. | Draft-only; no escritura. |
| 03 | Activation and state review | PM quiere comprobar que un target esta adoptado correctamente. | `templates/operations/03-verify-target-adoption.md` | `evidence.target_adoption` | Req: `TARGET_REPOSITORY`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 05, 06, 14, o 23 segun drift. | Si los adapters o evidencia target no pueden leerse, devolver `status.needs_context`. | No requiere aprobacion; read-only. |
| 05 | Activation and state review | PM necesita revisar estado, roadmap o desalineacion. | `templates/operations/05-review-project-state-and-misalignment.md` | `evidence.repo_state` | Req: none; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 06, 29, o 21 segun hallazgo. | Si no se puede leer estado vivo suficiente, devolver `status.needs_context`. | No requiere aprobacion; read-only. |
| 14 | Activation and state review | PM sospecha drift en adapters target. | `templates/operations/14-audit-target-adapters.md` | `evidence.repo_state` | Req: `TARGET_REPOSITORY`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 23 si hay upgrade/adopcion que aplicar; si no, 05 o 06. | Si adapters o modelo canonico no pueden leerse, devolver `status.needs_context`. | No requiere aprobacion; read-only. |
| 35 | Activation and state review | PM necesita elegir la siguiente operacion desde trazabilidad viva. | `templates/operations/35-recommend-next-lifecycle-operation.md` | `evidence.repo_state` | Req: none; Opt: `TARGET_REPOSITORY`, `ISSUE_NUMBER`, `PR_NUMBER`, `ROADMAP_ISSUE`, `CURRENT_STATUS`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | Humano PM invoca la operacion recomendada si decide seguir. | Si no hay ancla de ciclo o hay multiples rutas plausibles, devolver `status.needs_context` o `status.needs_pm_decision`. | Read-only y recommendation-only; nunca ejecuta, autoriza ni draftea el siguiente paso. |
| 36 | Activation and state review | Una operacion devolvio `status.needs_pm_decision` y el PM debe clasificar decision, contexto, correccion, follow-up, no-op o route prompt. | `templates/operations/36-process-needs-pm-decision.md` | `evidence.source_basis`, `evidence.repo_state` | Req: `ORIGINATING_OPERATION`, `STATUS_CONTEXT`, `OPTIONS_TRADEOFFS`; Opt: `ISSUE_NUMBER`, `PR_NUMBER`, `TARGET_REPOSITORY`, `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result`, `output.route_prompt`, `output.pm_command_bundle`, `output.draft_issue` | Volver a la operacion originaria, 08 para correccion, 21 para follow-up, 35 si falta routing, o stop. | Si origen/status/opciones o evidencia viva faltan, devolver `status.needs_context`; si la decision PM sigue abierta, devolver `status.needs_pm_decision`. | Draft-only; preserva autoridad PM y nunca auto-aprueba ni ejecuta. |
| 37 | Activation and state review | PM quiere revisar readiness antes de pasar a implementacion, manual implementation, QA/security/design, closeout, release, dogfood o handoff. | `templates/operations/37-review-phase-readiness.md` | `evidence.repo_state` | Req: none; Opt: `CURRENT_PHASE`, `TARGET_PHASE`, `ISSUE_NUMBER`, `PR_NUMBER`, `TARGET_REPOSITORY`, `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 36 si falta decision PM; 35 si falta elegir operacion; si no, la operacion segura de la fase target. | Si faltan scope, validacion, decision PM, blockers, branch/PR state o gate evidence, devolver `status.needs_context` o `status.needs_pm_decision`. | Advisory/read-only; recomienda pero no ejecuta, autoriza ni draftea la siguiente operacion. |
| 16 | Idea intake and requirements | PM tiene una idea y necesita decidir si es feature del sistema. | `templates/operations/16-review-idea-as-system-feature.md` | `evidence.repo_state` | Req: `IDEA`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 04 para issue, 28 para docs, o stop si no procede. | Si la idea o contexto base son insuficientes, devolver `status.needs_pm_decision` o `status.needs_context`. | No requiere aprobacion; analiza y recomienda. |
| 04 | Idea intake and requirements | PM entrega descripcion para convertirla en issue. | `templates/operations/04-draft-create-issue-command-from-description.md` | `evidence.source_basis` | Req: `DESCRIPTION`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle` | 07 cuando el issue exista y tenga scope estable. | Si la descripcion no alcanza para un issue accionable, devolver `status.needs_pm_decision`. | Browser chat draftea; Humano PM ejecuta el comando si decide crear el issue. |
| 26 | Idea intake and requirements | PM quiere convertir conversacion en docs, issue draft o ruta de escritura. | `templates/operations/26-draft-docs-from-conversation.md` | `evidence.source_basis` | Req: `CONVERSATION_CONTEXT`; Opt: `DOC_TARGET`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt`, `output.draft_issue`, `output.status_result` | Terminal agent escribe solo si se aprueba; si no, 28 o 04. | Si no se distinguen decisiones estables de discusion abierta, devolver `status.needs_pm_decision`. | Draft-only; escritura de archivo requiere aprobacion PM exacta y ruta delegada. |
| 28 | Idea intake and requirements | PM entrega descripcion para documentacion estable. | `templates/operations/28-draft-docs-from-description.md` | `evidence.source_basis` | Req: `DESCRIPTION`; Opt: `DOC_TARGET`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt`, `output.draft_issue`, `output.status_result` | Terminal agent escribe con aprobacion o 04 si debe ser issue. | Si falta target de doc o source basis, devolver `status.needs_pm_decision` o `status.needs_context`. | Draft-only; escritura de archivo requiere aprobacion PM exacta y ruta delegada. |
| 27 | Roadmap and issue planning | Docs estables deben convertirse en roadmap. | `templates/operations/27-draft-roadmap-from-docs.md` | `evidence.source_basis`, `evidence.repo_state` | Req: `SOURCE_DOCS`; Opt: `TARGET_REPOSITORY`, `ROADMAP_ACTION`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.draft_issue`, `output.pm_command_bundle`, `output.status_result` | 06 o 29 para derivar issues acotados. | Si docs, roadmap vivo o decision PM faltan/conflictuan, devolver `status.needs_pm_decision` o `status.needs_context`. | Draft-only; GitHub write lo ejecuta Humano PM con bundle. |
| 06 | Roadmap and issue planning | Hay roadmap/traceability y se necesita el proximo issue unico. | `templates/operations/06-draft-create-next-issue-command-from-traceability.md` | `evidence.source_basis`, `evidence.repo_state` | Req: none; Opt: `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle` | 07 cuando el PM crea el issue. | Si no hay un unico outcome derivable, devolver `status.needs_pm_decision`. | Browser chat draftea; Humano PM ejecuta el comando si decide crear el issue. |
| 29 | Roadmap and issue planning | Roadmap necesita issues acotados por limite explicito. | `templates/operations/29-draft-bounded-roadmap-issues-command.md` | `evidence.source_basis`, `evidence.repo_state` | Req: `ROADMAP_ISSUE`; Opt: `ISSUE_COUNT_LIMIT`, `SCOPE_LIMIT`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle`, `output.status_result` | 07 para cada issue aprobado. | Si falta limite explicito o trazabilidad suficiente, devolver `status.needs_pm_decision` o `status.needs_context`. | Browser chat draftea; Humano PM ejecuta los comandos si decide crear issues. |
| 22 | Roadmap and issue planning | PM tomo una decision que debe quedar como ADR. | `templates/operations/22-record-adr-decision.md` | `evidence.source_basis` | Req: `DECISION`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt` | 06 o 07 despues de registrar la decision. | Si decision o fuente son ambiguas, devolver `status.needs_context` o `status.needs_pm_decision`. | Draft-only; escritura del ADR requiere aprobacion PM exacta y ruta delegada. |
| 07 | Implementation routing | Issue scoped necesita implementacion por terminal agent. | `templates/operations/07-draft-issue-implementation-route-prompt.md` | `evidence.source_basis`, `evidence.repo_state` | Req: none; Opt: `ISSUE_NUMBER`, `ROADMAP_ISSUE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt` | 09 tras PR o 08 si hay correcciones. | Si no se puede derivar exactamente un issue, devolver `status.needs_context` o `status.needs_pm_decision`. | Route prompt no autoriza; `PM_AUTHORIZATION_STATUS` solo puede ser `pending` o `granted for this exact scope and mode`. Draft/read-only/planning describen modo o postura, no valores de autorizacion. Terminal agent solo escribe con aprobacion exacta, branch preflight y validacion. |
| 33 | Manual implementation planning | Terminal agent no esta disponible, no es apropiado, o se necesita un plan humano para un issue scoped. | `templates/operations/33-draft-manual-implementation-plan.md` | `evidence.issue_scope`, `evidence.source_basis`, `evidence.repo_state` | Req: `ISSUE_NUMBER`; Opt: `TARGET_REPOSITORY`, `PATH_SCOPE`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.manual_implementation_plan` | 34 si el resultado humano necesita clasificacion; 09 si ya existe PR; 08 o 21 segun hallazgos. | Si issue, repo/code anchors, source basis o expectativas de validacion no pueden inspeccionarse suficientemente, devolver `status.needs_context`; riesgo de secretos devuelve `status.blocked`. | Browser chat draftea solamente; el plan es humano-ejecutable y nunca afirma que browser chat edito codigo. |
| 34 | Manual implementation planning | Humano PM entrega evidencia de implementacion manual aplicada despues de 33. | `templates/operations/34-process-manual-implementation-result.md` | `evidence.issue_scope`, `evidence.source_basis`, `evidence.repo_state` | Req: `ISSUE_NUMBER`, `MANUAL_IMPLEMENTATION_RESULT`; Opt: `MANUAL_IMPLEMENTATION_PLAN`, `PR_NUMBER`, `TARGET_REPOSITORY`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result`, `output.route_prompt`, `output.pm_command_bundle` | 09 si existe PR; 08 para correcciones; 21 para follow-up; 36 si falta decision PM; 37 para readiness; gates QA/security/design cuando falte esa evidencia. | Si issue, resultado manual, plan, repo, PR o validacion no pueden inspeccionarse suficientemente, devolver `status.needs_context`; riesgo de secretos devuelve `status.blocked`. | Draft-only; no afirma que browser chat aplico o valido cambios y no reemplaza 09 cuando existe PR. |
| 23 | Implementation routing | Target adoptado necesita upgrade de kernel/adapters. | `templates/operations/23-upgrade-kernel-adoption-in-target.md` | `evidence.target_adoption`, `evidence.branch_preflight`, `evidence.pm_approval`, `evidence.validation_output` | Req: `TARGET_REPOSITORY`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.adoption_packet`, `output.route_prompt` | 03 para verificar upgrade. | Si target, adopcion o aprobacion de escritura faltan, devolver `status.needs_context` o `status.blocked`. | Browser chat draftea; terminal agent escribe solo con aprobacion PM exacta. |
| 08 | PR review and correction | Review, QA, seguridad, diseno o PM feedback requiere correccion. | `templates/operations/08-draft-review-correction-route-prompt.md` | `evidence.source_basis`, `evidence.repo_state` | Req: `ISSUE_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt` | 09 despues de aplicar correcciones. | Si falta issue/PR asociado o feedback accionable, devolver `status.needs_context`. | Draft-only; terminal agent corrige solo con aprobacion PM exacta. |
| 09 | PR review and correction | PR listo para review-before-close. | `templates/operations/09-review-pr-before-close-and-draft-package.md` | `evidence.issue_scope`, `evidence.pr_diff`, `evidence.validation_output` | Req: `PR_NUMBER`; Opt: `EXECUTION_REPORT`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.review_result`, `output.pm_command_bundle` | 10 si resuelto; 08 si hay findings. | Si no se puede inspeccionar codigo/diff/final files, devolver `status.needs_context`; no emitir GO, especialmente no basado solo en `EXECUTION_REPORT`. | No mergea ni cierra; consume execution reports como evidence leads cuando hay PR y solo draftea closeout para Humano PM cuando esta resuelto. |
| 15 | PR review and correction | PM necesita auditar trazabilidad issue/PR. | `templates/operations/15-audit-issue-pr-traceability.md` | `evidence.repo_state` | Req: `ISSUE_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 08 si falta correccion o 21 si hay follow-up. | Si historial del issue no puede leerse, devolver `status.needs_context`. | No requiere aprobacion; read-only. |
| 25 | PR review and correction | PM necesita auditar disciplina de implementacion. | `templates/operations/25-audit-implementation-discipline-gaps.md` | `evidence.repo_state` | Req: `TARGET_REPOSITORY`; Opt: `PATH_SCOPE`, `FOCUS`, `ISSUE_NUMBER`, `PR_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.review_result`, `output.draft_issue`, `output.status_result` | 08 para bloqueantes o 21 para follow-up. | Si evidencia de codigo no puede inspeccionarse, devolver `status.needs_context`. | No muta codigo ni GitHub; drafts de follow-up quedan para PM. |
| 18 | QA, security and design gates | PM necesita checklist de QA humano para una entrega. | `templates/operations/18-draft-human-qa-checklist.md` | `evidence.repo_state` | Req: `ISSUE_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 30 cuando existan resultados QA. | Si requisitos o criterios no pueden leerse, devolver `status.needs_context`. | Draft-only; QA externo no es actor kernel. |
| 19 | QA, security and design gates | PM necesita solicitar assets o insumos de diseno externos. | `templates/operations/19-request-external-design-assets.md` | `evidence.repo_state`, `evidence.source_basis` | Req: `DESCRIPTION`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.asset_prompt` | 32 cuando llegue la entrega. | Si objetivo o restricciones de assets son insuficientes, devolver `status.needs_pm_decision`. | Draft-only; destinatario de diseno no es actor kernel. |
| 20 | QA, security and design gates | PR necesita prompt de revision OWASP externa. | `templates/operations/20-request-owasp-security-review.md` | `evidence.repo_state`, `evidence.source_basis` | Req: `PR_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.security_review_prompt` | 31 cuando llegue el resultado. | Si PR o superficies sensibles no pueden leerse sin exponer secretos, devolver `status.needs_context` o `status.blocked`. | Draft-only; revision externa no es actor kernel. |
| 30 | QA, security and design gates | QA humano devuelve resultado. | `templates/operations/30-process-human-qa-results.md` | `evidence.repo_state`, `evidence.source_basis` | Req: `QA_RESULT`; Opt: `ISSUE_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt`, `output.pm_command_bundle`, `output.status_result` | 08 para bloqueantes, 21 para no bloqueantes, 09 si pasa. | Si no se puede derivar un issue unico, devolver `status.needs_context` o `status.needs_pm_decision`. | Draft-only; correcciones requieren ruta y aprobacion PM exacta. |
| 31 | QA, security and design gates | Revision de seguridad devuelve resultado. | `templates/operations/31-process-security-review-results.md` | `evidence.repo_state`, `evidence.source_basis` | Req: `SECURITY_REVIEW_RESULT`; Opt: `PR_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt`, `output.pm_command_bundle`, `output.status_result` | 08 para bloqueantes, 21 para no bloqueantes, 09 si pasa. | Si no se puede derivar un PR unico o hay riesgo de secretos, devolver `status.needs_context`, `status.needs_pm_decision` o `status.blocked`. | Draft-only; correcciones requieren ruta y aprobacion PM exacta. |
| 32 | QA, security and design gates | Llega entrega o feedback de diseno/assets. | `templates/operations/32-process-design-asset-delivery.md` | `evidence.repo_state`, `evidence.source_basis` | Req: `DESIGN_DELIVERY`; Opt: `ISSUE_NUMBER`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.route_prompt`, `output.pm_command_bundle`, `output.status_result` | 07, 08, 04, o 21 segun destino. | Si no se puede derivar un issue o ruta de producto unica, devolver `status.needs_context` o `status.needs_pm_decision`. | Draft-only; cambios requieren ruta y aprobacion PM exacta. |
| 21 | Follow-up and maintenance | Review detecta finding no bloqueante o diferible. | `templates/operations/21-draft-create-follow-up-from-review-command.md` | `evidence.source_basis` | Req: `PR_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle` | 07 cuando el follow-up exista y se priorice. | Si findings o fuente no pueden leerse, devolver `status.needs_context`. | Browser chat draftea; Humano PM decide si crea el issue. |
| 10 | Closeout and verification | Review-before-close resolvio y falta paquete de cierre. | `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` | `evidence.issue_scope`, `evidence.pr_diff`, `evidence.validation_output` | Req: `PR_NUMBER`, `ISSUE_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle` | 11 tras merge/cierre ejecutado por PM. | Si scope, diff, validacion o estado vivo faltan, devolver `status.needs_context`. | Draftea bundle; Humano PM mergea/cierra/limpia si decide. |
| 11 | Closeout and verification | PR fue mergeado/cerrado y PM quiere sanity check. | `templates/operations/11-verify-post-merge-state.md` | `evidence.repo_state` | Req: `PR_NUMBER`; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 06 para siguiente outcome o 12 para release readiness. | Si default branch, issue o checks no pueden leerse, devolver `status.needs_context`. | No requiere aprobacion; read-only. |
| 12 | Release and handoff | Estado merged podria justificar tag o release. | `templates/operations/12-analyze-release-or-tag-readiness.md` | `evidence.repo_state`, `evidence.validation_output` | Req: none; Opt: `TAG_NAME`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.status_result` | 13 para tag simple o 24 para GitHub Release. | Si evidencia merged o validacion faltan, devolver `status.needs_context`. | No publica; solo evalua readiness. |
| 13 | Release and handoff | Readiness justifica crear tag git. | `templates/operations/13-draft-create-release-tag-command.md` | `evidence.repo_state`, `evidence.validation_output` | Req: none; Opt: `TAG_NAME`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle` | Humano PM ejecuta o vuelve a 12 si falta version. | Si falta TAG_NAME final o hay colision, detener con `status.needs_pm_decision`. | Draftea bundle; Humano PM autoriza y ejecuta tag/push. |
| 24 | Release and handoff | Readiness justifica objeto GitHub Release. | `templates/operations/24-draft-create-github-release-command.md` | `evidence.repo_state`, `evidence.validation_output` | Req: none; Opt: `TAG_NAME`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.pm_command_bundle` | Humano PM ejecuta o vuelve a 12 si faltan notas/version. | Si faltan tag/notas o hay colision, detener con `status.needs_pm_decision`. | Draftea bundle; Humano PM autoriza y ejecuta release. |
| 17 | Release and handoff | PM necesita transferir contexto a nueva sesion. | `templates/operations/17-draft-handoff-package-for-new-session.md` | `evidence.repo_state` | Req: none; Opt: `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO` | `output.handoff_packet` | 00 en la nueva sesion. | Si no se puede reconstruir estado vivo suficiente, devolver `status.needs_context`. | Draft-only; no muta repo ni GitHub. |

## KOPS.3 Candidate Decisions

Cada candidato se resolvio contra el SDLC y los boundaries existentes antes de
agregar templates. Los cambios que sobreviven son no duplicativos, read-only o
draft-only, y no agregan workflows, outputs, evidence ids, statuses ni
boundaries.

| Candidate | Decision | Rationale | Durable change |
|---|---|---|---|
| Process terminal-agent execution report outside PR review | Clarified in Operation 09; no separate normal PR execution-report processor. | When a PR exists, Operation 09 is already the review-before-close path and consumes EXECUTION_REPORT as an evidence lead. A non-PR processor would need exact PM decision and a proven non-duplicative case. | Operation 09 INPUT/LIVE_STATE/DO/OUTPUT/LIMITS plus docs/tests state the standard path and guard against duplicate normal PR processing. |
| Process manual implementation result | New Operation 34. | After Operation 33, a human-applied result may need classification before PR review or when no PR exists. This is distinct from Operation 09 only until a PR exists. | `templates/operations/34-process-manual-implementation-result.md`, catalog/flow rows, and tests. |
| Process `status.needs_pm_decision` | New Operation 36. | PM requested a named operation instead of ad hoc chat handling. It must return to the originating operation or draft a safe route without becoming a workflow engine. | `templates/operations/36-process-needs-pm-decision.md`, catalog/flow rows, and tests. |
| Determine next lifecycle operation | New Operation 35. | The PM needs low-friction lifecycle routing, but it must remain read-only and recommendation-only. | `templates/operations/35-recommend-next-lifecycle-operation.md`, catalog/flow rows, and tests. |
| Phase readiness review | New Operation 37. | PM requested a named advisory readiness gate before implementation, QA/security/design, closeout, release, dogfood, or handoff. | `templates/operations/37-review-phase-readiness.md`, catalog/flow rows, and tests. |

Route-prompt authorization remains a two-option route-prompt/wizard-guided
status, not a kernel permission grant: `PM_AUTHORIZATION_STATUS` has exactly two
authorization-status values, `pending` and
`granted for this exact scope and mode`. Draft, read-only, and planning describe
execution mode or planning posture, not authorization-status values. The prompt
artifact itself never grants permission; permission comes only from exact scoped
PM approval plus the resolved kernel gates for the terminal agent action.

Manual implementation planning is covered by operation `33`, result
classification by operation `34`, recommendation-only lifecycle selection by
operation `35`, PM decision status processing by operation `36`, and advisory
phase readiness by operation `37`. None of these operations executes lifecycle
transitions automatically.

## KOPS.3 PM Decisions Needed

| Candidate not added as new operation | Why not added now | PM decision needed before adding |
|---|---|---|
| Separate normal PR execution-report processor | It would duplicate Operation 09, which is the standard review-before-close path when a PR exists. | A concrete non-PR or pre-review execution-report processing case that cannot be handled by 09, 08, 21, 35, 36, or 37. |

## Boundary Summary

- Browser chat: siempre draft-only; no edita archivos, no ejecuta git, no muta
  GitHub, no afirma que edito codigo y no convierte outputs en permiso.
- Terminal agent: puede escribir solo bajo modo de implementacion aprobado,
  branch preflight, evidencia requerida y validacion proporcional.
- Humano PM: ejecuta bundles de comandos y decide merge, cierre, labels, tags,
  releases, settings, automation y cualquier excepcion.
- GitHub/git: source of truth para estado vivo. Durable docs/templates guardan
  reglas, no hechos vivos.
- Fail closed: ante evidencia faltante, identidad ambigua, conflictos,
  aprobacion ausente, secretos o validacion fallida, devolver el status seguro
  y nombrar el proximo paso seguro.
