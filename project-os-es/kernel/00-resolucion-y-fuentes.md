# 00 — Resolucion y fuentes

Responsabilidad: explicar como se resuelve el kernel y que capa manda. La
fuente canonica sigue siendo `kernel/manifest.json`.

## Manifiesto

`kernel/manifest.json` es la unica entrada de resolucion. Define:

- `load_order`: carga `statuses`, `actors`, `execution_modes`, `boundaries`,
  `evidence`, `workflows` y `outputs`.
- `resolution_strategy`: ruta terminal con resolver; ruta manual para browser y
  otras superficies.
- `resolution_sequence`: actor, limites, modo, workflow, evidencia, output y
  estado final.
- `source_of_truth`: comportamiento estable en `kernel/*.json`; estado vivo en
  GitHub/git; adapters/templates/docs solo apuntan al manifiesto.

## Resolver

`tools/project_os_resolve.py` acelera la resolucion en terminal:

```sh
python -m tools.project_os_resolve --actor <actor> --workflow <workflow> --mode <mode> --kernel-dir <kernel-dir>
```

El resolver:

- lee JSON del kernel siguiendo el manifiesto;
- expande actor, workflow, modo, evidencia, limites y outputs;
- emite guia operativa y lecturas requeridas de trazabilidad;
- no consulta GitHub ni git;
- no es workflow engine;
- no autoriza nada.

## Secuencia compacta

1. Identifica la superficie y resuelve `actor.*`.
2. Carga estados y limites; los limites siempre aplican.
3. Toma el `mode.*` indicado por el PM; si falta, usa `mode.review_only`.
4. Selecciona un `workflow.*`.
5. Reune evidencia viva requerida por workflow y modo.
6. Selecciona el `output.*` permitido.
7. Devuelve exactamente un `status.*`; gana el mas estricto.

## No-autorizacion

Nada en el kernel, esta superficie, el resolver, los outputs, templates,
variables, route prompts o command bundles concede permiso de escritura, merge,
cierre, labels, tags, releases, settings, despliegue o automatizacion.

La autoridad para escribir requiere siempre:

- aprobacion PM exacta para el repositorio, issue/PR y accion;
- actor y modo compatibles;
- evidencia viva suficiente;
- branch preflight cuando hay repo writes;
- validacion proporcional requerida;
- limites del kernel respetados.
