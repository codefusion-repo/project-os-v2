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
falta contexto, autoridad o validacion. Este prompt no autoriza escritura.
