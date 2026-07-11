# Route prompt

Responsabilidad: rutear trabajo scoped a otra superficie sin pegar el issue
completo ni conceder permisos.

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
SCOPE = {{1-3 lineas, no el cuerpo completo}}
OUT_OF_SCOPE = {{errores plausibles a evitar}}
EVIDENCE_REQUIRED = {{evidence ids requeridas}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none con razon}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium|high|xhigh}} - {{razon breve}}

{{Instruccion concreta: implementar, revisar, auditar o draftear solo el scope.}}
```

El agente receptor re-resuelve el kernel, lee evidencia viva y falla cerrado si
falta contexto, autoridad o validacion. El browser chat infiere
`RECOMMENDED_TERMINAL_AGENT_FAMILY` como consejo no vinculante: Codex para
implementación de código, tooling Python, migraciones, refactors y tests;
Claude para síntesis documental, revisión de arquitectura o prosa de contexto
largo; Gemini para trabajo multimodal o de ecosistema Google con ventaja clara;
`none` si no hay ventaja significativa o falta evidencia. El feedback explícito
del PM puede reemplazar esa recomendación. `OPTIONAL_SKILL`, `HYDRATION_LEVEL`
y la familia recomendada no eligen permisos, no reemplazan aprobacion PM exacta
y no fuerzan herramienta. `HYDRATION_LEVEL` controla solo cuánto contrato ya
resuelto devuelve el resolver: `compact` es el valor predeterminado práctico, `minimal`
conserva los límites obligatorios y `full/debug` sirve para revisión, debugging
o auditoría. Ningún nivel lee estado vivo, inventa estado ni cambia autorización.
Este prompt no autoriza escritura.
