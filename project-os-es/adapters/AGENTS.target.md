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
KERNEL_LOCAL_PATH = {{ruta absoluta a project-os-v2/kernel}}
KERNEL_VERSION_ADOPTED = {{version adoptada o "tracks latest"}}

## Resolucion del kernel

Antes de trabajo no trivial, resuelve desde `KERNEL_LOCAL_PATH` siguiendo
`manifest.json` exactamente. En terminal usa el fast path desde el checkout de
Project OS, no desde el target:

```sh
PROJECT_OS_LOCAL_PATH="${KERNEL_LOCAL_PATH%/}"
PROJECT_OS_LOCAL_PATH="${PROJECT_OS_LOCAL_PATH%/kernel}"
cd "$PROJECT_OS_LOCAL_PATH"
if [ -d .venv ]; then . .venv/bin/activate; fi
python -m tools.project_os_resolve --actor <actor> --workflow <workflow> --mode <mode> --kernel-dir "$KERNEL_LOCAL_PATH"
cd "$REPOSITORY_LOCAL_PATH"
```

La resolucion manual de `kernel/manifest.json` es el fallback canonico. La
resolucion da forma operativa y nunca concede permisos.

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
- Valida proporcionalmente segun `docs/VALIDATION_POLICY.md` del kernel:
  comandos agent-run cuando el riesgo lo exige, comandos PM-run cuando
  corresponda, validacion manual PM para claridad/UX/copy, o ausencia
  justificada.
