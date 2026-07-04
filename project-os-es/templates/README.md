# Templates no operacionales

Templates compactos en español para artefactos que Project OS puede draftear,
crear, trazar o documentar. Son contratos de forma: no contienen logica de
workflow, no leen estado vivo y no conceden permisos.

El catalogo `project-os-es/kernel/artefactos.json` enlaza cada artefacto con
exactamente un `required_template`. El resolver debe exponer esas referencias,
no copiar el contenido del template.

## Catalogo

- `project-os-es/templates/route-prompt.md`: ruteo scoped hacia otra superficie.
- `project-os-es/templates/pm-command-bundle.md`: comandos PM copy-safe.
- `project-os-es/templates/issue.md`: cuerpo de issue.
- `project-os-es/templates/pull-request.md`: cuerpo de PR.
- `project-os-es/templates/comentario-cierre.md`: comentario de cierre/reconstruccion.
- `project-os-es/templates/adr.md`: decision durable.
- `project-os-es/templates/roadmap.md`: roadmap canonico.
- `project-os-es/templates/reporte-ejecucion.md`: execution report.
- `project-os-es/templates/resultado-revision.md`: review result.
- `project-os-es/templates/resultado-estado.md`: status no resuelto.
- `project-os-es/templates/plan-implementacion-manual.md`: plan humano-ejecutable.
- `project-os-es/templates/prompt-asset.md`: solicitud de asset a destinatario externo.
- `project-os-es/templates/prompt-revision-seguridad.md`: solicitud de revision OWASP.
- `project-os-es/templates/paquete-handoff.md`: traspaso entre sesiones.
- `project-os-es/templates/paquete-adopcion.md`: reporte de adopcion de target.
