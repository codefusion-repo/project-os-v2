# Empezar con Project OS

**Guía breve para arrancar bien: confirma lo externo, elige superficie,
configura el browser, prepara terminal solo si vas a delegar, abre la primera
sesión con evidencia real y opera el ciclo completo — delegar, revisar,
corregir y cerrar.**

## 1. Requisitos externos

Project OS no controla estos puntos. Tenlos listos antes de operar:

- **Repo target creado en GitHub.** Es el producto que vas a adoptar,
  implementar, revisar o auditar.
- **Cuenta GitHub conectada con acceso al repo target.** El acceso conectado
  requerido es al target: issues, PRs, diffs y docs según el flujo.
- **Browser chat con lectura GitHub/repo target en modo read-only.** Recomendado:
  ChatGPT con GitHub conectado. Otra superficie sirve si permite proyecto/chat
  con instrucciones y lectura del repo target.
- **Terminal/local con acceso GitHub al target si delegarás implementación.**
  Debe poder leer y escribir lo aprobado; si el flujo usa issues o PRs, también
  necesita acceso a issues/PRs del target.
- **Repo Project OS readable.** Úsalo como fuente pública o legible de kernel,
  operaciones, adapters y docs; no lo presentes como requisito privado ligado a
  una cuenta especial.
- **Sin secretos para empezar.** No necesitas `.env`, tokens, llaves privadas ni
  credenciales de producción para activar una sesión.

## 2. Superficies

La capacidad depende de la superficie, no del rol:

- **Humano PM.** Decide alcance, aprobaciones exactas, merge, cierre de issues,
  labels, tags, releases, settings, secretos y despliegues.
- **Browser chat.** Sirve para draft, revision, routing y analisis. Permanece
  read-only/draft-only aunque la herramienta conectada pudiera escribir.
- **Terminal agent.** Ejecuta implementación delegada: edita en scope, valida,
  hace commit/push y abre PR draft solo con evidencia viva, rama correcta y
  aprobación PM exacta.

Dos repos aparecen en casi todos los flujos:

- **Repo Project OS:** kernel, operaciones, adapters y docs.
- **Repo target:** producto donde se adopta o ejecuta el trabajo. En el
  desarrollo de Project OS, target y Project OS pueden ser el mismo repo.

Antes de pedir trabajo, nombra cuál repo cumple cada rol.

Además de la superficie de actuación, elige la superficie de idioma por path:
español es el default (`project-os-es/`); inglés es selección explícita
(`project-os-en/`, o `--kernel-dir project-os-en/kernel` en el resolver). No
existe selector global ni preferencia persistente de idioma.

## 3. Configuración browser

Haz esto en la superficie browser antes de usarla para draft o revisión:

1. Usa ChatGPT recomendado u otra superficie browser que permita proyecto/chat
   con instrucciones persistentes.
2. Carga las instrucciones de Project OS o el adapter del target cuando exista;
   para browser project/chat usa
   [`project-os-es/adapters/BROWSER_CHAT.target.md`](../adapters/BROWSER_CHAT.target.md)
   como bootloader.
3. Conecta o verifica GitHub en esa superficie.
4. Confirma que puede leer el repo target; cuando aplique, confirma también que
   puede leer el repo Project OS.
5. Si no puede leer una evidencia requerida, debe responder
   `status.needs_context` con lo que falta. No debe inventar estado de issues,
   PRs, ramas, diffs, validación ni roadmap.

## 4. Preparación terminal/local

Haz esto solo cuando vayas a delegar implementación a un terminal agent:

1. Ten el repo target clonado o el workspace local listo.
2. Verifica `gh auth status` para el repo target.
3. Confirma acceso a issues y PRs del target cuando el agente necesite leerlos,
   comentarlos o abrir PRs.
4. Ten Python disponible si usaras el resolver.
5. Adopta o revisa el adapter terminal del target con
   [`project-os-es/adapters/AGENTS.target.md`](../adapters/AGENTS.target.md) y
   conserva sus referencias portables y define localmente
   `PROJECT_OS_TARGET_ROOT` y `PROJECT_OS_KERNEL_DIR`, o usa paths absolutos
   literales en los dos campos para una adopción privada.

La adopción es copy-based por diseño: copiar el adapter al target y ajustar sus
campos de identidad es la instalación completa. Las referencias persistidas
`$PROJECT_OS_TARGET_ROOT` y `$PROJECT_OS_KERNEL_DIR` permiten compartir el
adapter sin commitear paths personales. Define sus valores solo en el entorno
local, por ejemplo con `export`, y verifica la adopción con el auditor. Para un
adapter privado de una máquina también se admiten paths absolutos literales;
un mount neutral como `/workspace/...` es válido, pero no obligatorio. `$PWD`,
variables distintas, valores compuestos y placeholders fallan cerrado. No hay
installer, package ni CLI; cualquier tooling futuro tiene su propio gate y no
es requisito para operar hoy.

Fast path del resolver para el target ya adoptado:

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
  --kernel-dir "$KERNEL_DIR" [--skill skill.<id>] || exit $?
cd "$TARGET_ROOT" || exit 1
```

La misma resolución consume el campo persistido en modalidad portable o
literal, sin `eval` ni expansión de nombres arbitrarios, y funciona igual desde
la raíz del target o desde cualquiera de sus subcarpetas, incluidas las que
tienen su propio `AGENTS.md`: la búsqueda ascendente valida cada candidato y
continúa hasta el bootloader raíz coherente con el target. Las comprobaciones
previas son estructurales: exigen que el `AGENTS.md` seleccionado sea el del
target resuelto y rechazan referencias fuera del allowlist, paths relativos,
kernels de otra superficie y manifests ilegibles, no activos o de otro idioma.
Si ningún ancestro las satisface, el fast path falla cerrado sin invocar el
resolver. No verifican
procedencia, firma, hash ni integridad del checkout, así que no son un trust
anchor. Un código de salida no cero del resolver aborta el fast path con ese
mismo código y no habilita ningún paso posterior. La resolución manual de
`project-os-es/kernel/manifest.json` sigue siendo el fallback canónico para la
superficie en español.

### Nivel de hidratación

El resolver acepta `--hydration-level minimal|compact|full/debug`. Si se omite,
usa `compact`: es la vista práctica para ejecutar sin volcar todo el contrato.
`minimal` conserva IDs, límites, evidencia, outputs, statuses, no-autorización
y secret safety necesarios para detener acciones prohibidas. `compact` añade la
guía mandatoria, actor/workflow/mode y referencias resolubles. `full/debug`
amplía los metadatos de la resolución seleccionada para revisión, debugging o
auditoría; no es el modo normal ni reemplaza el manifest canónico.

La respuesta declara `hydration_level` y usa estos shapes deterministas:

- `minimal`: identidad de manifest/actor/mode/workflow, todos los límites
  aplicables, acciones prohibidas, evidencia, outputs y statuses referenciados.
- `compact`: todo `minimal` más reglas mandatorias concisas, el contexto
  operativo seleccionado y referencias de artifacts/templates/skills.
- `full/debug`: todo `compact` más los metadatos completos de la resolución
  seleccionada, incluidos flags de actividad y enlaces internos de auditoría.

Ningún nivel devuelve `context_plan`: la procedencia detallada del resolver es
una ruta explícita y aparte (`--context-provenance <razón>`). En la ejecución,
la trazabilidad PM-facing es la evidencia revisada del output y ningún nivel
agrega un bloque de recibo. `debug` aislado no es un alias válido.

```sh
python tools/project_os_resolve.py --actor actor.terminal_agent \
  --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
  --kernel-dir project-os-es/kernel --hydration-level compact
```

Dentro del resolver, el nivel cambia solo el contenido devuelto: no lee
GitHub/git, no inventa estado y nunca concede permisos. Los tamaños
medidos por nivel, con metodología y
fecha declaradas, están en [benchmark-contexto.md](benchmark-contexto.md). Los otros niveles se solicitan con el mismo flag; un
valor desconocido falla cerrado. En Python el parámetro canónico es
`hydration_level`; `compact` sigue disponible como alias de compatibilidad. El
flag preexistente `--compact` conserva exclusivamente su función de imprimir
JSON sin indentación.

Cuando draftees outputs, el resolver puede exponer artefactos con
`required_template`; usa ese template de
[`project-os-es/templates/`](../templates/README.md) como forma del output, no
como permiso. Si el PM pide un skill o un route prompt lo recomienda, pasalo
con `--skill`; el resolver lo devuelve como `requested_skills` separado de
artefactos/templates, referenciado por `required_skill` bajo
[`project-os-es/habilidades/`](../habilidades/), y sin autoridad extra.

## 5. Primera sesión

1. **Elige superficie.** Usa browser chat para draft, revisión y routing;
   terminal agent para implementación delegada; Humano PM para cierre, merge,
   settings, secretos y despliegues.
2. **Activa browser chat con
   [MOS-0.1](../operaciones/fase-0/MOS-0.1-activar-sesion-browser-chat.md),
   declarando `TARGET_REPOSITORY` en formato `owner/repo`.** MOS-0.1 solicita
   el target antes de resolver el estado inicial y reconstruye
   `evidence.repo_state` solo contra ese repositorio; si el target falta, es
   inválido o no puede leerse, devuelve `status.needs_context` sin usar otro
   repositorio conectado.
3. **Verifica adopción cuando haya target con
   [MOS-0.5](../operaciones/fase-0/MOS-0.5-verificar-adopcion-del-target.md),**
   que audita la readiness browser y terminal por separado y solo da GO global
   cuando ambas superficies aplicables están listas. Si el target aún no adoptó
   Project OS, usa
   [MOS-0.2](../operaciones/fase-0/MOS-0.2-iniciar-proyecto-nuevo.md) para
   proyecto nuevo o
   [MOS-0.3](../operaciones/fase-0/MOS-0.3-adoptar-proyecto-existente.md) para
   proyecto existente: ambas son browser-first y draftean primero un adapter
   browser aplicable por el PM (sin bloquear el arranque en la falta de
   roadmap), y luego rutean la escritura de adapters al terminal agent en
   `mode.delegated_commit_pr` mediante un route prompt con aprobación PM exacta.
4. **Usa
   [MOS-0.6](../operaciones/fase-0/MOS-0.6-transferir-contexto-de-sesion.md)
   solo si la sesión está incoherente, agotada o necesita traspaso.**
5. **Elige la siguiente operación por fase** desde el catálogo
   [`operaciones/README.md`](../operaciones/README.md) (incluye una tabla de
   casos frecuentes en [docs/README.md](README.md)) y el ciclo día a día de
   [ritmo.md](ritmo.md).
6. **Genera prompts locales opcionalmente** con
   `python tools/operation_prompt_wizard.py --language es` (o responde su
   pregunta única `es/en`; español sigue siendo el default). La selección es
   solo de sesión, no ejecuta la operación y nunca adopta un idioma para el
   target.

## 6. Delegar, revisar, corregir y cerrar

El ciclo completo de una unidad de trabajo, una vez activa la sesión:

1. **Delegar la implementación.** Draftea el route prompt con
   [MOS-3.4](../operaciones/fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md)
   (el wizard captura `HYDRATION_LEVEL`; `compact` es el default) y entrégalo
   al terminal agent. El agente re-resuelve el kernel, verifica preflight, scope
   vivo y aprobación PM exacta, implementa solo el scope, valida y abre un
   draft PR. El route prompt da forma y nunca autoriza por sí mismo.
2. **Revisar el PR antes de cerrar.** Usa
   [MOS-3.7](../operaciones/fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md):
   compara la unidad de trabajo contra el diff, los archivos finales, la
   validación reportada y los riesgos. Reportes y bodies son claims hasta
   verificarlos contra evidencia viva.
3. **Corregir dentro del mismo issue/PR.** Si el review encuentra gaps,
   draftea la corrección con
   [MOS-3.5](../operaciones/fase-3/MOS-3.5-draftear-route-prompt-de-correccion.md)
   sobre la misma rama y el mismo PR; no abras unidades nuevas para corregir
   scope vigente.
4. **Cerrar con el GO del review.** Merge y cierre son siempre del Humano PM:
   el GO de [MOS-3.7](../operaciones/fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md)
   entrega en la misma respuesta los comandos copy-safe de closeout y su
   verificación final read-only; si el bundle se pierde o el cierre falla,
   vuelve a ejecutar MOS-3.7 sobre la evidencia vigente.

**Siguiente paso:** lee [reglas.md](reglas.md) y luego [ritmo.md](ritmo.md).
