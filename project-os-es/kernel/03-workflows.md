# 03 — Workflows

Responsabilidad: perfilar el tipo de trabajo. La fuente canonica es
`kernel/workflows.json`.

Selecciona exactamente un workflow por tarea. Sus pasos guian, pero no relajan
actores, modos, limites, evidencia ni outputs.

## Lectura y revision

### `workflow.review_only`

Uso: analisis, auditorias, preguntas y hallazgos sin cambios.

Evidencia: `evidence.repo_state`. Outputs: `output.review_result`,
`output.status_result`.

### `workflow.review_before_close`

Uso: revisar trabajo terminado antes de merge/cierre PM.

Debe comparar issue vivo, PR diff, changed files, archivos finales relevantes y
validacion. PR bodies y reportes son claims, no prueba. Si falta evidencia de
codigo, devuelve `status.needs_context`, no GO.

Evidencia: `evidence.issue_scope`, `evidence.pr_diff`,
`evidence.validation_output`. Outputs: review, closure draft, command bundle o
status.

### `workflow.implementation_discipline_audit`

Uso: auditoria read-only contra disciplina de implementacion.

Reporta hallazgos con evidencia archivo/linea cuando sea posible. No refactoriza
ni edita.

Evidencia: `evidence.repo_state`. Outputs: review, status o draft issue.

## Implementacion

### `workflow.issue_implementation`

Uso: implementar un issue GitHub acotado.

Secuencia: resolver kernel, leer issue vivo y source basis, branch preflight,
crear/switch a `work/<issue>-<slug>`, implementar solo dentro de scope, validar,
commit/push/PR solo si el modo lo permite, reportar.

Evidencia: issue scope, branch preflight, aprobacion PM y validacion. Outputs:
execution report o status.

### `workflow.issue_implementation_manual`

Uso: draftear instrucciones humano-ejecutables sin mutar repo ni GitHub.

Debe inspeccionar issue y contexto de codigo disponible, nombrar archivos y
anclas cuando sea posible, fallar cerrado si el contexto no alcanza y declarar
que no edito ni valido codigo.

Evidencia: issue scope, source basis y repo state. Outputs: manual
implementation plan o status.

## PM intake y rutas

### `workflow.pm_intake`

Uso: convertir input PM en issues, route prompts o decision requests.

No escribe. Entrega drafts y command bundles copy-safe.

Evidencia: `evidence.source_basis`. Outputs: draft issue, route prompt, command
bundle o status.

### `workflow.handoff`

Uso: transferir sesion o trabajo a otra superficie sin perder trazabilidad.

El estado transferible debe vivir en GitHub; el handoff apunta a evidencia viva
sin duplicarla como verdad durable.

Evidencia: `evidence.repo_state`. Outputs: handoff packet o status.

## Revision especializada y assets

### `workflow.design_asset`

Uso: preparar prompt para destinatario grafico/diseno.

El destinatario no es actor kernel. No genera assets ni edita archivos salvo
que otro workflow/modo/aprobacion lo permita.

Evidencia: repo state y source basis. Outputs: asset prompt o status.

### `workflow.security_revision`

Uso: preparar prompt de revision OWASP.

Debe cubrir superficies sensibles como auth, autorizacion, sesiones/cookies,
inputs, uploads, redirects, dependencias, admin, secretos, logs, errores y
deploy/config cuando aplique. Nunca pide exponer secretos.

Evidencia: repo state y source basis. Outputs: security review prompt o status.

## Release, adopcion y deploy

### `workflow.release_readiness`

Uso: evaluar si algo esta listo para tag/release.

Tags y releases requieren aprobacion PM separada. El workflow reporta gaps y se
detiene antes de crear nada.

Evidencia: repo state y validacion. Outputs: review, command bundle o status.

### `workflow.target_adoption`

Uso: auditar o bootstrappear un target sobre este kernel.

Audita adapters existentes contra templates/herramientas canonicas sin borrar
notas target-owned. Si falta adopcion y el modo/aprobacion permite, crea solo
adapters acotados y draft PR.

Evidencia: `evidence.target_adoption`. Outputs: adoption packet, execution
report o status.

### `workflow.deployment`

Uso: ejecutar deploy interno local/staging con comandos target-owned.

Requiere aprobacion exacta por repositorio, entorno y accion. Ejecuta solo
comandos documentados por el target; nunca inventa comandos, expone secretos ni
ejecuta produccion bajo este modo.

Evidencia: aprobacion PM, source basis, target adoption, deployment readiness,
validacion y repo state. Outputs: execution report o status.
