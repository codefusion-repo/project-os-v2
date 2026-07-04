# 07 — Capas operativas

Responsabilidad: ubicar reglas que el kernel referencia pero no debe duplicar.
La fuente de layering es `docs/decisions/0002-pre-377-validation-fastpath-audit.md`.

## Ownership

- `kernel/manifest.json`: entrada unica, orden de carga, estrategia de
  resolucion, fuente de verdad y no-autorizacion canonica.
- `kernel/*.json`: actores, modos, workflows, evidencia, outputs, estados y
  limites estables.
- `tools/project_os_resolve.py`: expande la resolucion en terminal y emite
  guia operativa/trazabilidad sin consultar GitHub/git ni autorizar acciones.
- `docs/TRACEABILITY_PROTOCOL.md`: reglas de reconstruccion viva.
- `docs/VALIDATION_POLICY.md`: categorias de validacion, lista obligatoria y
  criterios para tests.
- `docs/CONTEXT_ECONOMY.md`: clases de contexto y disciplina de subagentes.
- `templates/route-prompt.md`: forma del route prompt PM-facing.
- `templates/pm-command-bundle.md`: forma copy-safe del command bundle.
- `project-os-es/operaciones/`: prompts compactos de operacion; cada operacion
  aporta contexto task-specific y referencia estas capas.

## Trazabilidad viva

Antes de trabajo no trivial:

- lee issue/PR, comentarios, reviews, branches, commits y validacion desde
  GitHub/git;
- lee el roadmap canonico y ADRs relevantes cuando son source basis;
- trata PR bodies, comentarios y reportes como claims hasta verificar diff,
  checks y archivos finales;
- no uses memoria interna ni archivos durables como estado vivo.

## Validacion proporcional

Clasifica la validacion como:

- agent-run obligatoria;
- comandos PM-run drafteados;
- validacion manual PM;
- sin validacion automatica, con justificacion.

La validacion agent-run es obligatoria cuando cambia comportamiento
deterministico o de alto riesgo: kernel JSON, resolver/tooling, command safety,
trazabilidad, autorizacion, seguridad/privacidad, despliegue, secretos,
produccion, migraciones, billing, storage, auth, payments, route prompts o
contratos estables.

## Operaciones compactas

Las operaciones en `project-os-es/operaciones/` deben:

- resolver kernel antes de actuar;
- mantener el detalle vivo en issues/PRs;
- preservar variables PM-facing como contexto, no autorizacion;
- fallar cerrado ante evidencia o autoridad faltante;
- no guardar estado vivo;
- no pedir ni exponer secretos;
- apuntar a la capa duena en vez de repetir reglas largas.
