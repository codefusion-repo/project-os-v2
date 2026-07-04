# AGENTS.md (adapter terminal para target)

Copia este archivo al repo target como `AGENTS.md`, reemplaza
`{{PLACEHOLDERS}}` y elimina este bloque inicial.

---

# AGENTS.md

## Contrato

AGENTS.md es el bootloader terminal de `{{ORG/REPO}}`.

No es fuente de verdad. El kernel Project OS define comportamiento generico
(actores, modos, workflows, limites, evidencia, salidas y estados). La verdad
de producto, dominio, runtime, validacion y decisiones PM vive en el target y
en su evidencia viva.

Debe permanecer compacto. No guarda estado vivo: issues, PRs, ramas, commits,
reviews, validacion, roadmap activo ni readiness.

## Identidad del repositorio

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = {{ruta absoluta al repo target}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{ruta absoluta a project-os-v2/project-os-es/kernel}}
KERNEL_VERSION_ADOPTED = {{version adoptada o "tracks latest"}}

## Resolucion del kernel

Antes de trabajo no trivial, resuelve desde `KERNEL_LOCAL_PATH` siguiendo
`project-os-es/kernel/manifest.json` exactamente. En terminal usa el resolver
de la superficie espanola:

```sh
PROJECT_OS_ES_LOCAL_PATH="${KERNEL_LOCAL_PATH%/}"
PROJECT_OS_ES_LOCAL_PATH="${PROJECT_OS_ES_LOCAL_PATH%/kernel}"
python "$PROJECT_OS_ES_LOCAL_PATH/tools/resolver.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  --kernel-dir "$KERNEL_LOCAL_PATH" [--skill skill.<id>]
```

La resolucion manual de `project-os-es/kernel/manifest.json` es el fallback
canonico para esta superficie. La resolucion da forma operativa y nunca concede
permisos.

`--skill` es opcional y solo expone una referencia de capacidad del agente; no
autoriza escritura ni reemplaza evidencia, aprobacion PM, preflight,
validacion, trazabilidad o review-before-close.

## Outputs y artefactos

Cuando produzcas reportes de ejecucion, cuerpos de PR, paquetes de handoff,
paquetes de adopcion u otros outputs, usa los artefactos/template references
resueltos desde `project-os-es` cuando apliquen. Los templates dan forma y nunca
autorizan.

Cuando el PM pida una capacidad o un route prompt la recomiende, usa el skill
resuelto como referencia a `project-os-es/habilidades/`. Los skills no son
artefactos ni templates.

El terminal agent sigue obligado por scope vivo, branch preflight, aprobacion PM
exacta, validacion proporcional y review-before-close. Ningun artefacto ni
template reemplaza esos gates.

## Estado vivo

Reconstruye estado para `REPOSITORY_NAME` desde GitHub y git al momento de la
tarea: issue actual, PRs vinculados, roadmap canonico `{{#ROADMAP_ISSUE}}` y
ADRs del target en `docs/decisions/` cuando existan. Si falta evidencia,
devuelve el estado no resuelto correspondiente; no inventes.

## Seguridad y validacion

- No imprimas, pegues, commitees ni resumas `.env`, tokens, credenciales,
  cookies, JWTs, URLs de base de datos, llaves privadas, secretos CI ni valores
  con pinta de secreto; redacta como `[REDACTED]`.
- No cambies secretos, settings, credenciales, produccion, pagos ni despliegues
  sin aprobacion PM exacta separada.
- Para web/API/user-facing, considera auth, autorizacion, sesiones, input
  validation, uploads, redirects, dependencias y superficies admin.
- Valida proporcionalmente segun `project-os-es/docs/reglas.md` y las reglas
  resueltas desde `project-os-es/kernel/`:
  comandos agent-run cuando el riesgo lo exige, comandos PM-run cuando
  corresponda, validacion manual PM para claridad/UX/copy, o ausencia
  justificada.
