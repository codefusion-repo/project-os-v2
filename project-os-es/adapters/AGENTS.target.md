# AGENTS.md (adapter terminal para target)

Copia el bloque siguiente como `AGENTS.md` en el target, reemplaza los
`{{PLACEHOLDERS}}` y elimina estas instrucciones de copia. Conserva las
referencias portables o reemplázalas por paths absolutos literales en una
adopción privada de una sola máquina.

---

# AGENTS.md

AGENTS.md es el bootloader terminal de `{{ORG/REPO}}`. No es fuente de verdad
ni concede permisos: el comportamiento genérico vive en `project-os-es/kernel/`
y los hechos del target se reconstruyen desde su evidencia viva.

## Identidad del repositorio

Estas rutas y la versión adoptada son configuración de máquina/adopción, no
estado vivo. Conserva estos campos y orden. Las referencias portables son
exactamente `PROJECT_OS_TARGET_ROOT` para el checkout target y
`PROJECT_OS_KERNEL_DIR` para el kernel; sus valores absolutos viven solo en el
entorno local y nunca en este archivo.

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR
KERNEL_VERSION_ADOPTED = {{version adoptada o "tracks latest"}}

## Resolución del kernel

Antes de trabajo no trivial, lee `project-os-es/kernel/manifest.json` y sigue
su `resolution_sequence`. En terminal, cuando el checkout del kernel esté
disponible, usa este fast path. Localiza el `AGENTS.md` raíz subiendo desde el
directorio actual: valida cada candidato completo y sigue subiendo cuando no sea
el bootloader raíz coherente con el target resuelto, de modo que un `AGENTS.md`
intermedio de una subcarpeta no detenga la búsqueda. Lee los dos campos
persistidos, acepta solo la referencia portable exacta o un literal absoluto y
comprueba la identidad estructural del kernel antes del resolver; no usa `eval`,
no expande nombres arbitrarios y propaga sin alterar cualquier código de salida
no cero del resolver:

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
skills desde las referencias resueltas, sin copiar sus contratos aquí. Usa
`context_plan` para distinguir archivos cargados internamente, metadata
proyectada, templates y skills referenciados; no lo trates como prueba del
contenido entregado al modelo.

Abre después de resolver solo el template aplicable, las skills solicitadas y
las fuentes Project OS, target o evidencia viva exigidas por scope, validación
o source basis. Conserva íntegros `context_plan` y el recibo canónico interno
con las lecturas reales. Aplica `pm_facing_visibility` del contrato resuelto:
omite únicamente la representación del recibo en `minimal` y `compact`, y
muéstralo completo en el envelope PM-facing de `full/debug`, con paths relativos
al repositorio o identificadores vivos y razones, nunca con cuerpos completos.
Una lectura adicional requiere una razón admitida por el contrato; no recorras
recursivamente Project OS por defecto.

## Evidencia viva

Reconstruye el estado desde GitHub, git, el roadmap canónico del target cuando
exista y los ADRs del target cuando apliquen. No guardes aquí sus números ni
ninguna otra referencia viva. Ante
kernel, evidencia, autoridad o validación requerida faltantes o ambiguos, falla
cerrado según el kernel resuelto.

## Notas propias del target

Añade únicamente comandos estables de build/validación, paths protegidos,
restricciones de dominio o seguridad, idioma PM-facing y escalaciones
específicas. La política genérica de seguridad, trazabilidad y validación sigue
en `project-os-es/docs/reglas.md` y el kernel resuelto.
