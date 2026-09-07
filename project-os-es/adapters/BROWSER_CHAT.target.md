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

## Entrada intent-first

La ruta normal para el PM es describir su intención —el target o referencia
relevante cuando no se derive ya del contexto, el outcome que busca y sus
constraints— sin seleccionar antes un código MOS. Aplica directamente la
capacidad canónica de
`project-os-es/operaciones/cross-fase/MOS-R.2-recomendar-siguiente-operacion.md`:
reutiliza la fuente inequívoca ya presente, pide como máximo un locator
primario cuando falte, reconstruye el resto desde evidencia viva y selecciona
exactamente una operación cuando la intención y la evidencia son inequívocas.
Explica en una frase breve por qué eligió esa operación y devuelve la decisión
al PM con `status.needs_context` o `status.needs_pm_decision` solo ante
ambigüedad material real, nunca eligiendo por orden de catálogo o coincidencia
superficial. Sigue la continuación intent-first de MOS-R.2 hasta la siguiente
salida útil bajo la resolución propia de la operación seleccionada; no exijas
otra invocación PM solo para aplicar la ruta ya resuelta. No repitas aquí el
contrato de MOS-R.2; consúltalo resuelto.

La selección explícita —código MOS, workflow, mode, path, o un override de
hidratación— sigue disponible y tiene precedencia cuando el PM la declara
directamente. Ninguna de las dos rutas infiere autorización PM, aprobación,
merge, cierre, labels, tags, releases, deploys ni cambios de secretos desde la
intención.

## Notas propias del target

Añade únicamente restricciones estables de dominio, seguridad, idioma PM-facing
o escalación. No guardes issues, PRs, ramas, commits, reviews ni validación en
este adapter.
