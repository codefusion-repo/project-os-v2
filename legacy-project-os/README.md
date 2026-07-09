# legacy-project-os — superficie archivada (no activa)

**Esta carpeta es archivo histórico. No es la superficie operativa de Project
OS y ningún flujo activo debe resolverse desde aquí.** (Archival only: this
folder is not the active Project OS surface.)

La superficie activa de Project OS vive en [`project-os-es/`](../project-os-es/)
y se resuelve desde `project-os-es/kernel/manifest.json` con el resolver
`project-os-es/tools/resolver.py`. Ver el mapa activo en
[`project-os-es/docs/README.md`](../project-os-es/docs/README.md).

## Qué contiene

Contenido movido desde la raíz del repositorio cuando `project-os-es` pasó a
ser la superficie primaria (issue de migración de la secuencia del ADR 0003,
`docs/decisions/0003-project-os-cli-adoption-model.md`):

| Carpeta | Contenido histórico |
| --- | --- |
| `kernel/` | Kernel inglés `project-os-v2-min` (source-basis del kernel español). |
| `adapters/` | Adapter templates ingleses `*.target.md` para adopción de targets. |
| `templates/` | Templates ingleses: artefactos, route prompt, command bundle, `templates/operations/` 00-37 y `templates/mosdlc/operations/`. |
| `docs/` | Docs ingleses de Project OS: diseño, políticas de validación/trazabilidad/economía de contexto, catálogo PM y mapa MOSDLC. |

## Reglas de esta carpeta

- Se conserva como referencia histórica y source-basis; se preserva por moves,
  no se reescribe.
- No es ruta activa: los adapters, docs y templates de la raíz y de
  `project-os-es/` no deben apuntar aquí como fuente operativa.
- Las rutas internas de estos archivos son las históricas (relativas a la raíz
  del repositorio antes de la migración); se leen en su contexto histórico.
- Nada aquí concede permisos (`boundary.output_not_permission`), y esta
  carpeta no guarda estado vivo.
