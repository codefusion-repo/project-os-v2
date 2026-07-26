# AGENTS.md

AGENTS.md es el bootloader terminal de `codefusion-repo/project-os-v2`.
No es fuente de verdad ni concede permisos. El comportamiento genérico vive en
`project-os-es/kernel/`; los hechos de producto, dominio e implementación se
reconstruyen desde la evidencia viva de este repositorio.

## Identidad del repositorio

Estas rutas y la versión adoptada son configuración de máquina/adopción, no
estado vivo. Conserva estos campos y orden al adaptar esta superficie. Las
referencias portables son exactamente `PROJECT_OS_TARGET_ROOT` para el checkout
target y `PROJECT_OS_KERNEL_DIR` para el kernel; sus valores absolutos viven
solo en el entorno local y nunca en este archivo.

PROJECT_NAME = project-os-v2
REPOSITORY_NAME = codefusion-repo/project-os-v2
REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR
KERNEL_VERSION_ADOPTED = tracks latest

## Resolución del kernel

Antes de trabajo no trivial, lee `project-os-es/kernel/manifest.json` y sigue
su `resolution_sequence`. En esta superficie terminal, cuando el checkout del
kernel esté disponible, usa este fast path. Localiza el `AGENTS.md` raíz
subiendo desde el directorio actual: valida cada candidato completo y sigue
subiendo cuando no sea el bootloader raíz coherente con el target resuelto, de
modo que un `AGENTS.md` intermedio de una subcarpeta no detenga la búsqueda.
Lee los dos campos persistidos, acepta solo la referencia portable exacta o un
literal absoluto y comprueba la identidad estructural del kernel antes del
resolver; no usa `eval`, no expande nombres arbitrarios y propaga sin alterar
cualquier código de salida no cero del resolver:

```sh
select_target_bootloader() {
  AGENTS_FILE=$1
  TARGET_REF=$(sed -n 's/^REPOSITORY_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
  KERNEL_REF=$(sed -n 's/^KERNEL_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
  case "$TARGET_REF" in
    '$PROJECT_OS_TARGET_ROOT'|'${PROJECT_OS_TARGET_ROOT}')
      test -n "${PROJECT_OS_TARGET_ROOT:-}" || return 1
      TARGET_ROOT="$PROJECT_OS_TARGET_ROOT"
      ;;
    /*) case "$TARGET_REF" in *'$'*) return 1 ;; esac; TARGET_ROOT="$TARGET_REF" ;;
    *) return 1 ;;
  esac
  case "$KERNEL_REF" in
    '$PROJECT_OS_KERNEL_DIR'|'${PROJECT_OS_KERNEL_DIR}')
      test -n "${PROJECT_OS_KERNEL_DIR:-}" || return 1
      KERNEL_DIR="$PROJECT_OS_KERNEL_DIR"
      ;;
    /*) case "$KERNEL_REF" in *'$'*) return 1 ;; esac; KERNEL_DIR="$KERNEL_REF" ;;
    *) return 1 ;;
  esac
  case "$TARGET_ROOT" in /*) ;; *) return 1 ;; esac
  case "$KERNEL_DIR" in /*) ;; *) return 1 ;; esac
  case "$KERNEL_DIR" in */project-os-es/kernel) ;; *) return 1 ;; esac
  PROJECT_OS_ROOT="${KERNEL_DIR%/project-os-es/kernel}"
  test -n "$PROJECT_OS_ROOT" || return 1
  test -d "$TARGET_ROOT" || return 1
  test "$AGENTS_FILE" -ef "$TARGET_ROOT/AGENTS.md" || return 1
  test -f "$KERNEL_DIR/manifest.json" || return 1
  test -f "$PROJECT_OS_ROOT/tools/project_os_resolve.py" || return 1
  python -c '
import json
import sys
try:
    payload = json.load(open(sys.argv[1], encoding="utf-8"))
    entries = payload.get("manifest") if isinstance(payload, dict) else None
    valid = (
        isinstance(entries, list) and len(entries) == 1
        and isinstance(entries[0], dict)
        and entries[0].get("key") == "manifest.kernel_es"
        and entries[0].get("language") == "es"
        and entries[0].get("active") is True
    )
except (OSError, UnicodeError, json.JSONDecodeError):
    valid = False
raise SystemExit(0 if valid else 1)
' "$KERNEL_DIR/manifest.json" || return 1
}
AGENTS_FILE=
probe=$(pwd)
while :; do
  if test -f "$probe/AGENTS.md" && select_target_bootloader "$probe/AGENTS.md"; then
    break
  fi
  AGENTS_FILE=
  test "$probe" = / && break
  probe=$(dirname "$probe")
done
test -n "$AGENTS_FILE" || {
  echo 'sin AGENTS.md raiz coherente con el target adoptado' >&2
  exit 1
}
python "$PROJECT_OS_ROOT/tools/project_os_resolve.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  --kernel-dir "$KERNEL_DIR" [--change-class change_class.<id>] [--skill skill.<id>] || exit $?
cd "$TARGET_ROOT" || exit 1
```

El alcance de esas comprobaciones es estructural y demostrable: exigen que el
`AGENTS.md` seleccionado sea el del target resuelto, rechazan referencias fuera
del allowlist, paths relativos, kernels ubicados en otra superficie y manifests
ilegibles, no activos o de otro idioma, y no invocan el resolver cuando ninguna
ruta ascendente las satisface. Continuar la búsqueda no relaja ninguna: un
candidato solo se acepta si él mismo las cumple todas, y el resolver se invoca
una sola vez sobre el candidato aceptado. No verifican procedencia del repositorio, commit, firma, hash ni
integridad del checkout, así que no son un trust anchor: un directorio local que
reproduzca esa estructura sigue siendo ejecutable. Si un código no cero del
resolver aborta el fast path, ningún paso posterior queda habilitado.

El resolver acelera la resolución; el manifest sigue siendo canónico. Ambos
solo dan forma y nunca autorizan una acción. Consulta artefactos, templates y
skills desde las referencias resueltas, sin copiar sus contratos aquí.

Abre después de resolver solo el template aplicable, las skills solicitadas y
las fuentes Project OS, target o evidencia viva exigidas por scope, validación
o source basis. La trazabilidad PM-facing es `Evidencia revisada` y su
equivalente por output. Una lectura adicional debe estar justificada por scope,
validación o source basis; no recorras recursivamente Project OS por defecto.

## Evidencia viva

Reconstruye el estado del trabajo desde GitHub, git, el roadmap canónico del
repositorio cuando exista y los ADRs de `docs/decisions/` cuando apliquen. No
guardes aquí sus números ni ninguna otra referencia viva.
Ante kernel, evidencia, autoridad o validación requerida faltantes o ambiguos,
falla cerrado según el kernel resuelto.

## Notas propias del repositorio

- Conserva solo comandos estables, paths protegidos, restricciones de dominio,
  seguridad o escalaciones específicas del repositorio.
- Para cambios web/API/user-facing, considera los riesgos OWASP relevantes.
- No expongas valores sensibles; reporta rutas, nombres de variables y tipo de
  riesgo con `[REDACTED]`.
- La política completa de seguridad, trazabilidad y validación vive en
  `project-os-es/docs/reglas.md` y el kernel resuelto.
