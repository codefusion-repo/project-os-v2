# Route prompt

Responsabilidad: rutear trabajo scoped a otra superficie como bootloader compacto
e issue-referential, sin pegar el issue, PR o comentarios completos ni conceder
permisos. El detalle de implementacion permanece en la evidencia viva.

El bloque siguiente es el route prompt completo: contiene un unico bloque
estandar de variables y una unica instruccion concreta al final.

```text
PROJECT_NAME = {{nombre}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{org/repo si difiere}}
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{ruta a kernel}}
ISSUE_OR_PR = {{#N}}
TARGET_ACTOR_TYPE = {{actor id}}
WORKFLOW = {{workflow id}}
EXECUTION_MODE = {{mode id}}
OUTPUT_CONTRACT = {{output id}}
OPTIONAL_SKILL = {{skill.<id> | none}}
HYDRATION_LEVEL = {{minimal | compact | full/debug}}
RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}
SCOPE = {{1-3 lineas; no restatar issue, PR, cuerpos, comentarios, acceptance criteria, source basis ni checklists}}
OUT_OF_SCOPE = {{errores plausibles a evitar}}
EVIDENCE_REQUIRED = {{evidence ids requeridas}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none con razon}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium|high|xhigh}} - {{razon breve}}

{{Una unica instruccion concreta: re-resuelve el kernel, lee la evidencia viva requerida y verifica la entrega PM, PM_AUTHORIZATION_STATUS y la coincidencia exacta de repositorio, workflow, modo, rama y scope; falla cerrado para draft, falta de entrega, `pending` o valores ausentes, desconocidos o inferidos, e implementa, revisa, audita o draftea solo el scope.}}
```

Al draftear, lee el issue o PR vivo y sus comentarios, y referencia ese detalle
en vez de copiarlo. No agregues encabezados, secciones, listas, checklists ni
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
y no fuerzan herramienta. `HYDRATION_LEVEL` controla cuánto contrato ya
resuelto devuelve el resolver y selecciona la visibilidad PM-facing contractual
del recibo: `compact` es el valor predeterminado práctico, `minimal` conserva
los límites obligatorios, ambos ocultan solo esa representación, y `full/debug`
la muestra completa para revisión, debugging o auditoría. Ningún nivel cambia
el recibo interno ni `context_plan`, lee estado vivo, inventa estado o cambia autorización.
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
