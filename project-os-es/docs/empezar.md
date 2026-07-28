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
   [`project-os-es/adapters/AGENTS.target.md`](../adapters/AGENTS.target.md).
   Configura sus dos referencias portables en un `.envrc` local no trackeado
   y actívalo explícitamente en la terminal.

La adopción es copy-based por diseño: copiar el adapter al target y ajustar sus
campos de identidad es la instalación completa. Las referencias persistidas
`$PROJECT_OS_TARGET_ROOT` y `$PROJECT_OS_KERNEL_DIR` permiten compartir el
adapter sin commitear paths personales. La única ruta normal es crear un
`.envrc` local no trackeado que contenga solamente las dos exportaciones con
paths absolutos y cargarlo manualmente con `. ./.envrc` desde el directorio del
target. Carga solo un archivo que controles y hayas revisado: es código de
shell local, aunque el fast path nunca lo lee. No requiere herramientas
adicionales. Ninguna ruta carga el archivo de forma implícita y el fast path
nunca hace `source` ni `eval`. Por eso una terminal sin variables válidas falla
cerrado antes del resolver. El archivo reúne las dos configuraciones en un
único paso explícito por terminal. Para un adapter privado de una máquina aún
se admiten paths absolutos literales, pero no son la ruta normal compartida; un
mount neutral como `/workspace/...` es válido, pero no obligatorio. `$PWD`,
variables distintas, valores compuestos y placeholders fallan cerrado. No hay
installer, package ni CLI; cualquier tooling futuro tiene su propio gate y no
es requisito para operar hoy.

Fast path del resolver para el target ya adoptado. La ruta normal es este
comando corto. Es location-safe: funciona igual desde la raíz del target o
cualquier subdirectorio porque ubica el script a partir de la referencia de
kernel ya conocida, sin volver a buscarla:

```sh
python "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py" \
  --actor <actor> --workflow <workflow> --mode <mode> [--skill skill.<id>]
```

Si tu `AGENTS.md` usa un path absoluto literal en `KERNEL_LOCAL_PATH` en vez
de la referencia portable, sustituye `$PROJECT_OS_KERNEL_DIR` por esa misma
ruta literal en el comando.

`tools/project_os_fast_path.py` es la única fuente ejecutable que localiza el
`AGENTS.md` raíz subiendo desde el directorio actual, valida el candidato y
solo entonces invoca `tools/project_os_resolve.py`, exactamente una vez.
Ningún bootloader, adapter ni doc reimplementa esta búsqueda ni la
validación: todos son consumidores de este mismo módulo. Como referencia de
depuración no ejecutable, `--agents-file` valida un único candidato puntual
sin recorrer el árbol: `python tools/project_os_fast_path.py --agents-file
RUTA/AGENTS.md --actor <actor> --workflow <workflow> --mode <mode>` devuelve
el código reservado 111 cuando ese archivo por sí solo no es un candidato
coherente, distinto de cualquier veredicto real del resolver.

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
usa `compact` para cualquier `--change-class`: es la vista práctica para
ejecutar sin volcar todo el contrato, y la clase declarada nunca la cambia.
`minimal` conserva IDs, límites, evidencia, outputs, statuses, no-autorización
y secret safety necesarios para detener acciones prohibidas. `compact` añade la
guía mandatoria, actor/workflow/mode y referencias resolubles. `full/debug`
amplía los metadatos de la resolución seleccionada y es un opt-in para auditar
el kernel, debuggear el resolver o investigar una resolución incorrecta; no es
el modo normal, no lo exige ninguna clase ni ninguna revisión de seguridad o
autorización por sí sola, no implica procedencia detallada ni obliga a releer
manualmente los archivos que el resolver ya procesó, y no reemplaza el manifest
canónico.

La hidratación y la `CHANGE_CLASS` son ejes independientes. La clase gobierna
los gates materiales —unidad formal, PR, nivel de review, validación y
documentación previa— y la densidad del execution report; un cambio crítico
resuelto en `compact` conserva íntegros esos gates y su reporte detallado.

La respuesta declara `hydration_level` y usa estos shapes deterministas:

- `minimal`: identidad de manifest/actor/mode/workflow, todos los límites
  aplicables, acciones prohibidas, evidencia, outputs y statuses referenciados.
- `compact`: todo `minimal` más reglas mandatorias concisas, el contexto
  operativo seleccionado y referencias de artifacts/templates/skills.
- `full/debug`: todo `compact` más los metadatos completos de la resolución
  seleccionada, incluidos flags de actividad y enlaces internos de auditoría.

En la ejecución, la trazabilidad PM-facing es la evidencia revisada del output.
`debug` aislado no es un alias válido.

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
   [MOS-0.1](../operaciones/fase-0/MOS-0.1-activar-sesion-browser-chat.md).**
   `TARGET_REPOSITORY` es opcional: declararlo en formato `owner/repo` activa la
   sesión vinculada a ese target exacto y reconstruye `evidence.repo_state` solo
   contra él; omitirlo activa una sesión desvinculada, read-only y draft-only,
   que resuelve el kernel y declara que aún no hay target seleccionado sin elegir
   silenciosamente ningún repositorio conectado. Arrancar sin repositorio no es
   un error; solo devuelve `status.needs_context` cuando el target declarado es
   inválido o ilegible, o cuando una operación posterior depende realmente de
   estado de repositorio y no puede identificar un target inequívoco.
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
5. **Expresa tu intención.** Describe en browser chat el target o referencia
   relevante, el outcome que buscas y tus constraints; la ruta normal
   reutiliza [MOS-R.2](../operaciones/cross-fase/MOS-R.2-recomendar-siguiente-operacion.md)
   para reconstruir desde evidencia viva y recomendar exactamente una
   operación aplicable. Para elegir explícitamente por fase o código MOS, usa
   el catálogo [`operaciones/README.md`](../operaciones/README.md) (incluye
   una tabla de casos frecuentes en [docs/README.md](README.md)) y el ciclo
   día a día de [ritmo.md](ritmo.md).
6. **Genera prompts locales opcionalmente** con
   `python tools/operation_prompt_wizard.py --language es` (o responde su
   pregunta única `es/en`; español sigue siendo el default). Describe tu
   intención en el primer paso del wizard para que la transporte hacia
   MOS-R.2, o selecciona explícitamente por índice, código MOS, filename,
   stem o path. La selección es solo de sesión, no ejecuta la operación y
   nunca adopta un idioma para el target.

## 6. Delegar, revisar, corregir y cerrar

El ciclo completo de una unidad de trabajo, una vez activa la sesión:

1. **Delegar la implementación.** Draftea el route prompt con
   [MOS-3.4](../operaciones/fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md)
   (el wizard solo pide la unidad viva y la autorización; browser chat deriva
   clase, densidad, rama y relaciones desde la evidencia viva) y entrégalo
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
