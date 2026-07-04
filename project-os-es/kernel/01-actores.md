# 01 — Actores

Responsabilidad: definir superficies de ejecucion. La fuente canonica es
`kernel/actors.json`.

No hay actores por rol. Reviewer, QA, asset creator y security reviewer son
focos de revision, gates, destinatarios o formas de issue; no son actores del
kernel salvo que exista una nueva superficie real y aprobada.

## `actor.human_pm`

Superficie: humano.

Puede decidir scope/prioridad y autorizar o ejecutar acciones que otros actores
no pueden asumir: merges, cierres, labels, tags, releases, settings y cambios
de autorizacion.

Limites activos: secretos/privacidad y no guardar estado vivo en durables.

## `actor.terminal_agent`

Superficie: terminal con checkout del repo.

Puede leer, analizar, editar archivos dentro del scope, validar, commitear,
pushear, abrir draft PR y comentar solo cuando el scope lo permita.

No puede: mergear, cerrar issues, aplicar labels, crear tags/releases, cambiar
settings, crear automatizaciones ni editar `main` directamente.

Modos permitidos:

- `mode.review_only`
- `mode.local_implementation`
- `mode.delegated_commit_push`
- `mode.delegated_commit_pr`
- `mode.delegated_deploy_execution`

## `actor.browser_chat`

Superficie: chat de navegador.

Es draft-only aunque el prompt tenga rol tecnico o mencione aprobacion PM.
Puede leer contexto provisto, analizar y draftear issues, prompts, reportes y
command bundles copy-safe.

No puede editar archivos, commitear, pushear, abrir PRs, mergear, cerrar issues
ni mutar GitHub o el repo. Si el trabajo requiere escritura, lo enruta a
terminal.

Modo permitido: `mode.review_only`.

## `actor.unknown`

Superficie: desconocida.

No tiene capacidad write-capable. Ante solicitudes de escritura devuelve
`status.blocked`; ante contexto insuficiente devuelve `status.needs_context`.
