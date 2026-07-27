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
disponible, la ruta normal es este comando corto:

```sh
python tools/project_os_fast_path.py \
  --actor <actor> --workflow <workflow> --mode <mode> \
  [--change-class change_class.<id>] [--skill skill.<id>]
```

`tools/project_os_fast_path.py` es la única fuente ejecutable de esta lógica:
localiza el `AGENTS.md` raíz subiendo desde el directorio actual, valida cada
candidato completo y sigue subiendo cuando no sea el bootloader raíz coherente
con el target resuelto, de modo que un `AGENTS.md` intermedio de una subcarpeta
no detiene la búsqueda. Lee los dos campos persistidos, acepta solo la
referencia portable exacta o un literal absoluto y comprueba la identidad
estructural del kernel antes del resolver; no usa `eval`, no expande nombres
arbitrarios e invoca `tools/project_os_resolve.py` exactamente una vez, propagando sin alterar
cualquier código de salida no cero.

El siguiente bloque es documentación de implementación y depuración, no la
interfaz diaria: reproduce la misma búsqueda ascendente delegando cada
candidato a `project_os_fast_path.py --agents-file`, útil cuando el comando
corto no es alcanzable por ruta relativa desde el directorio actual o para
auditar el mecanismo paso a paso:

```sh
select_target_bootloader() {
  AGENTS_FILE=$1
  KERNEL_REF=$(sed -n 's/^KERNEL_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
  case "$KERNEL_REF" in
    '$PROJECT_OS_KERNEL_DIR'|'${PROJECT_OS_KERNEL_DIR}') KERNEL_DIR="${PROJECT_OS_KERNEL_DIR:-}" ;;
    /*) case "$KERNEL_REF" in *'$'*) KERNEL_DIR= ;; *) KERNEL_DIR="$KERNEL_REF" ;; esac ;;
    *) KERNEL_DIR= ;;
  esac
  test -n "$KERNEL_DIR" || return 111
  PROJECT_OS_ROOT=$(dirname "$(dirname "$KERNEL_DIR")")
  test -f "$PROJECT_OS_ROOT/tools/project_os_fast_path.py" || return 111
  python "$PROJECT_OS_ROOT/tools/project_os_fast_path.py" --agents-file "$AGENTS_FILE" \
    --actor <actor> --workflow <workflow> --mode <mode> \
    [--change-class change_class.<id>] [--skill skill.<id>]
}
probe=$(pwd)
rc=111
while test "$rc" -eq 111; do
  if test -f "$probe/AGENTS.md"; then
    select_target_bootloader "$probe/AGENTS.md"
    rc=$?
  fi
  if test "$rc" -eq 111; then
    test "$probe" = / && { echo 'sin AGENTS.md raiz coherente con el target adoptado' >&2; exit 1; }
    probe=$(dirname "$probe")
  fi
done
test "$rc" -eq 0 || exit "$rc"
cd "$probe" || exit 1
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
