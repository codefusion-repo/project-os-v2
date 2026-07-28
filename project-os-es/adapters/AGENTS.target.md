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

## Configuración local

La única ruta normal para configurar las referencias portables es un `.envrc`
local, no trackeado, con los valores absolutos de `PROJECT_OS_TARGET_ROOT` y
`PROJECT_OS_KERNEL_DIR`. Cárgalo manualmente y de forma explícita en tu
terminal; no requiere herramientas adicionales. El fast path nunca hace
`source`, `eval` ni carga `.envrc`; sin variables válidas falla cerrado antes
del resolver.

## Resolución del kernel

Antes de trabajo no trivial, lee `project-os-es/kernel/manifest.json` y sigue
su `resolution_sequence`. En terminal, cuando el checkout del kernel esté
disponible, la ruta normal es este comando corto. Es location-safe: funciona
igual desde la raíz del target o cualquier subdirectorio porque ubica el
script a partir de la referencia de kernel ya conocida, sin volver a
buscarla:

```sh
python "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  [--change-class change_class.<id>] [--skill skill.<id>]
```

Si tu `AGENTS.md` usa un path absoluto literal en `KERNEL_LOCAL_PATH` en vez
de la referencia portable, sustituye `$PROJECT_OS_KERNEL_DIR` por esa misma
ruta literal en el comando.

`tools/project_os_fast_path.py` es la única fuente ejecutable: falla cerrado
si no puede establecer una adopción estructuralmente coherente y delega
exactamente una vez en `tools/project_os_resolve.py`. Los bootloaders y
adapters son consumidores de esa entrada, no implementaciones alternativas.

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
