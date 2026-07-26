# BROWSER_CHAT.md (adapter browser para target)

Pega el bloque siguiente en las instrucciones del proyecto/chat browser y
reemplaza los `{{PLACEHOLDERS}}`.

---

# BROWSER_CHAT.md

BROWSER_CHAT.md es el bootloader de `{{ORG/REPO}}` para `actor.browser_chat`.
No es fuente de verdad ni concede permisos. Browser chat permanece read-only y
draft-only: no edita archivos ni muta GitHub aunque disponga de herramientas.

## Identidad del repositorio

Estas rutas y la versión adoptada son configuración de máquina/adopción, no
estado vivo. Conserva estos campos y orden.

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = {{ruta local si existe}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{ruta a project-os-es/kernel si existe}}
KERNEL_VERSION_ADOPTED = {{version adoptada o "tracks latest"}}

## Resolución y evidencia

Antes de trabajo no trivial, lee `project-os-es/kernel/manifest.json` desde
`KERNEL_REPOSITORY` y sigue su `resolution_sequence`. Browser chat no ejecuta
Python local ni usa el fast path terminal. Reconstruye la evidencia viva con las
fuentes conectadas disponibles; si no puede leer el kernel o la evidencia
requerida, devuelve `status.needs_context` y nombra la fuente faltante.

Los templates y la resolución solo dan forma y nunca autorizan. Para command
bundles PM, draftea exclusivamente según
`project-os-es/templates/pm-command-bundle.md`; para otros formatos, usa el
artefacto y template resueltos por el kernel.

Abre solo el template aplicable, las skills solicitadas y la evidencia o fuentes
requeridas por scope, validación o source basis; no recorras Project OS
recursivamente. La trazabilidad PM-facing es `Evidencia revisada` y su
equivalente por output. Toda lectura adicional debe estar justificada por scope,
validación o source basis, sin exponer cuerpos completos, secretos ni estado
vivo durable.

## Notas propias del target

Añade únicamente restricciones estables de dominio, seguridad, idioma PM-facing
o escalación. No guardes issues, PRs, ramas, commits, reviews ni validación en
este adapter.
