# Route prompt

Responsabilidad: rutear trabajo scoped a otra superficie como bootloader compacto
referenciado a una unidad viva, sin pegar la unidad, sus registros o comentarios
completos ni conceder permisos. El detalle de implementacion permanece en la
evidencia viva.

El bloque siguiente es el route prompt completo: contiene un unico bloque
estandar de variables y una unica instruccion concreta al final.

```text
PROJECT_NAME = {{nombre}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{org/repo si difiere}}
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{ruta a kernel}}
WORK_UNIT = {{referencia viva de la unidad: issue #N o PR #N cuando el target usa GitHub; si no, el change request, registro del target o instruccion PM exacta equivalente}}
CHANGE_CLASS = {{change_class.read | change_class.small | change_class.standard | change_class.critical}}
TARGET_ACTOR_TYPE = {{actor id}}
WORKFLOW = {{workflow id}}
EXECUTION_MODE = {{mode id}}
OUTPUT_CONTRACT = {{output id}}
OPTIONAL_SKILL = {{skill.<id> | none}}
HYDRATION_LEVEL = {{opcional; omitir salvo override explícito: minimal | compact | full/debug}}
RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}
SCOPE = {{1-3 lineas; no restatar la unidad viva, sus cuerpos, comentarios, acceptance criteria, source basis ni checklists}}
OUT_OF_SCOPE = {{errores plausibles a evitar}}
EVIDENCE_REQUIRED = {{evidence ids requeridas}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none con razon}}
BRANCH_NAME = work/{{unidad}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium|high|xhigh}} - {{razon breve}}

{{Una unica instruccion concreta: re-resuelve el kernel con la CHANGE_CLASS declarada, lee la evidencia viva requerida y verifica la entrega PM, PM_AUTHORIZATION_STATUS y la coincidencia exacta de repositorio, workflow, modo, rama y scope; falla cerrado para draft, falta de entrega, `pending` o valores ausentes, desconocidos o inferidos, e implementa, revisa, audita o draftea solo el scope.}}
```

`WORK_UNIT` nombra la unidad viva del workflow resuelto. Cuando el target usa
GitHub suele ser un issue o PR vivo; cuando no, transporta la referencia viva
equivalente: un change request, un registro del target o, para un
`change_class.small` admitido por la politica del target, la instruccion PM
exacta y verificable. En todos los casos la referencia debe ser verificable
viva y desde ella deben poder leerse objetivo, scope, out of scope, acceptance
criteria y resultado observable; nunca se completa con un numero inventado ni
con un placeholder durable.

`CHANGE_CLASS` declara la clase del contrato `proportionality.change_class`
del kernel. El agente receptor la pasa al resolver (`--change-class`), que
falla cerrado cuando la clase es desconocida o incompatible con el workflow o el
mode. La clase gobierna los gates materiales —unidad formal, PR, nivel de
review, validación y documentación previa— y la densidad del execution report;
nunca selecciona `HYDRATION_LEVEL`, que es un eje independiente. La clase
pertenece a la unidad y se conserva en intake, implementación, review, closeout
y verificación. La clase nunca autoriza nada.

El PM aporta decisiones, constraints y autoridad; browser chat aporta la
metadata. Los **inputs humanos** son el locator primario cuando hace falta,
`OPTIONAL_SKILL`, `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO`, el override
explícito `/hydration <nivel>` y `PM_AUTHORIZATION_STATUS`; no son metadata
derivada y nunca autorizan por sí mismos. La **metadata derivada** comprende
`CHANGE_CLASS`, `BRANCH_NAME`, el PR existente, el roadmap y las demás relaciones verificables
desde la unidad y sus registros. Esos valores se muestran ya resueltos para que
el receptor los verifique, nunca se inventan. La **recomendación inferida**
`RECOMMENDED_TERMINAL_AGENT_FAMILY` es consejo de browser chat, no un input ni
una autorización. Browser chat usa como máximo un locator primario por cadena de
evidencia y no lo vuelve a pedir cuando la invocación actual ya identifica la
fuente; solo devuelve `status.needs_context` o
`status.needs_pm_decision` ante ambigüedad material real —fuentes incompatibles
igualmente vigentes, relaciones no verificables, scope que no permite determinar
la clase, unidad formal ausente para una clase que la exige, o conflicto entre
evidencia viva y una decisión PM posterior—, nunca porque el PM no haya
reescrito un identificador, una clase, una rama o un nivel reconstruibles.
Ningún valor derivado concede permisos.

Cuando el route prompt corrige un PR ya revisado (MOS-3.5), el bloque agrega
`SOURCE_REVIEW` con la referencia exacta al review o comentario fuente y
`PR_NUMBER`, reconstruidos igual que el resto de la metadata. La
instrucción final exige publicar exactamente un correction report append-only en
ese PR con head anterior, head corregido, mapa de `blocking-correction` y
confirmación de que no hubo merge ni cierre, sin editar el body ni ningún
comentario previo.

Al draftear, lee la unidad viva y sus registros (el issue o PR y sus
comentarios cuando el target usa GitHub; la evidencia viva equivalente cuando
no) y referencia ese detalle en vez de copiarlo.
No agregues encabezados, secciones, listas, checklists ni
planes de implementacion antes o despues del bloque: fuera de las variables, el
unico contenido permitido es la instruccion concreta final. El agente receptor
re-resuelve el kernel, lee evidencia viva y falla cerrado si falta contexto,
autoridad o validacion. El browser chat infiere
`RECOMMENDED_TERMINAL_AGENT_FAMILY` como consejo no vinculante: Codex para
implementación de código, tooling Python, migraciones, refactors y tests;
Claude para síntesis documental, revisión de arquitectura o prosa de contexto
largo; Gemini para trabajo multimodal o de ecosistema Google con ventaja clara;
`none` si no hay ventaja significativa o falta evidencia. El feedback explícito
del PM puede reemplazar esa recomendación. `OPTIONAL_SKILL`, `HYDRATION_LEVEL`
y la familia recomendada no eligen permisos, no reemplazan aprobacion PM exacta
y no fuerzan herramienta. `HYDRATION_LEVEL` controla únicamente cuánto contrato
ya resuelto devuelve el resolver: `compact` es el valor predeterminado global
para cualquier clase, `minimal` es el opt-in que conserva los límites
obligatorios y `full/debug` es el opt-in para auditoría del kernel, debugging
del resolver o inspección detallada explícitamente solicitada. Ninguna clase
activa `full/debug` y ningún nivel cambia gates, densidad del reporte,
autoridad ni acciones permitidas. Ningún nivel devuelve `context_plan`, agrega
un bloque de recibo ni obliga a releer manualmente el kernel que el resolver ya
procesó; la procedencia detallada requiere una solicitud explícita
(`--context-provenance <razón>`). Ningún nivel lee estado vivo, inventa estado
o cambia autorización.
La plantilla y el wizard no conceden permisos por sí mismos. Un route prompt en
draft, no entregado por el PM o con `PM_AUTHORIZATION_STATUS=pending` no
autoriza escrituras. Cuando el PM entrega el route prompt con
`PM_AUTHORIZATION_STATUS=granted for this exact scope and mode`, esa entrega
satisface `evidence.pm_approval` únicamente para el repositorio, workflow,
modo, rama y scope declarados. El agente receptor debe verificar esa
coincidencia y la evidencia restante; un estado ausente, desconocido o
inferido falla cerrado. No se exige un comentario adicional de GitHub como
condición universal. El agente nunca puede completar, cambiar ni inferir
`granted`, y esa aprobación no cubre merge, cierre, tags, releases, deploys,
settings ni otra acción fuera del modo declarado.
