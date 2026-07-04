# 02 — Modos de ejecucion

Responsabilidad: definir hasta donde puede llegar un terminal agent en una
tarea. La fuente canonica es `kernel/execution_modes.json`.

Un modo nunca supera un limite ni agrega capacidades al actor. El modo por
defecto es `mode.review_only`.

## `mode.review_only`

Lee, analiza, ejecuta comandos read-only y reporta.

Prohibe ediciones, commits, push, PR, comentarios y cualquier mutacion GitHub.
Requiere `evidence.issue_scope`.

## `mode.local_implementation`

Permite ediciones locales acotadas y validacion en una rama de trabajo.

Prohibe commit, push, PR, comentarios y cualquier mutacion GitHub. Requiere
`evidence.issue_scope`, `evidence.branch_preflight` y `evidence.pm_approval`.

## `mode.delegated_commit_push`

Permite ediciones acotadas, validacion, commit y push a la rama de trabajo.

Prohibe abrir PR, merge, cierre, comentarios fuera de scope y otras mutaciones
GitHub. Requiere issue scope, branch preflight, aprobacion PM y validacion.

## `mode.delegated_commit_pr`

Permite ediciones acotadas, validacion, commit, push y draft PR.

Prohibe merge, cierre de issue, labels, tags/releases y settings. Requiere
issue scope, branch preflight, aprobacion PM y validacion.

## `mode.delegated_deploy_execution`

Permite ejecutar comandos target-owned de despliegue interno para un unico
entorno aprobado: local o staging.

No permite editar repo, commit, push, PR, mutar GitHub, inventar comandos,
desplegar produccion, ejecutar sin aprobacion exacta por entorno, exponer
secretos, hacer dumps amplios de entorno/configuracion ni mutar secret stores,
DNS, hosting, pagos o bases de datos fuera de comandos target-owned.

Produccion queda con Human PM por defecto.

## Nota de aprobacion

Una decision PM explicita es evidencia para el punto decidido. No se re-pide
autorizacion solo por desacuerdo del agente. Se reporta el desacuerdo como
riesgo o excepcion aceptada, salvo que aparezca un limite nombrado, una accion
distinta, un cambio material de scope/riesgo/evidencia o una aprobacion nueva
requerida.
