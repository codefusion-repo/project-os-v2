# AGENTS.md (adapter terminal para target)

Copia el bloque siguiente como `AGENTS.md` en el target, reemplaza los
`{{PLACEHOLDERS}}`, define las dos variables locales indicadas y elimina estas
instrucciones de copia. Para una adopción privada de una sola máquina, los dos
campos de path también aceptan paths absolutos literales.

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
disponible, usa este fast path. Falla cerrado si una variable falta o no es
absoluta; no usa `eval` ni expande nombres arbitrarios:

```sh
: "${PROJECT_OS_TARGET_ROOT:?define PROJECT_OS_TARGET_ROOT con el path absoluto del target}"
: "${PROJECT_OS_KERNEL_DIR:?define PROJECT_OS_KERNEL_DIR con el path absoluto del kernel}"
TARGET_ROOT="$PROJECT_OS_TARGET_ROOT"
KERNEL_DIR="$PROJECT_OS_KERNEL_DIR"
case "$TARGET_ROOT" in /*) ;; *) exit 1 ;; esac
case "$KERNEL_DIR" in /*) ;; *) exit 1 ;; esac
PROJECT_OS_ROOT="${KERNEL_DIR%/project-os-es/kernel}"
test "$PROJECT_OS_ROOT" != "$KERNEL_DIR"
test -f "$KERNEL_DIR/manifest.json"
python "$PROJECT_OS_ROOT/tools/project_os_resolve.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  --kernel-dir "$KERNEL_DIR" [--skill skill.<id>]
cd "$TARGET_ROOT"
```

El resolver acelera la resolución; el manifest sigue siendo canónico. Ambos
solo dan forma y nunca autorizan una acción. Consulta artefactos, templates y
skills desde las referencias resueltas, sin copiar sus contratos aquí. Usa
`context_plan` para distinguir archivos cargados internamente, metadata
proyectada, templates y skills referenciados; no lo trates como prueba del
contenido entregado al modelo.

Abre después de resolver solo el template aplicable, las skills solicitadas y
las fuentes Project OS, target o evidencia viva exigidas por scope, validación
o source basis. Reporta las lecturas reales en el recibo canónico de fuentes,
en el envelope del output junto al artefacto, con paths relativos al repositorio
o identificadores vivos y razones, nunca con cuerpos completos. Una lectura
adicional requiere una razón admitida por el contrato; no recorras
recursivamente Project OS por defecto.

## Evidencia viva

Reconstruye el estado desde GitHub, git, el roadmap canónico `{{#ROADMAP_ISSUE}}`
y los ADRs del target cuando apliquen. No lo guardes en este archivo. Ante
kernel, evidencia, autoridad o validación requerida faltantes o ambiguos, falla
cerrado según el kernel resuelto.

## Notas propias del target

Añade únicamente comandos estables de build/validación, paths protegidos,
restricciones de dominio o seguridad, idioma PM-facing y escalaciones
específicas. La política genérica de seguridad, trazabilidad y validación sigue
en `project-os-es/docs/reglas.md` y el kernel resuelto.
