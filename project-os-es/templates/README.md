# Templates no operacionales

Templates compactos en español para artefactos que Project OS puede draftear,
crear, trazar o documentar. Son contratos de forma: no contienen logica de
workflow, no leen estado vivo y no conceden permisos. Los skills viven aparte:
son capacidades opcionales del agente bajo `project-os-es/habilidades/`, no
templates ni artefactos.

El catalogo `project-os-es/kernel/artefactos.json` enlaza cada artefacto con
exactamente un `required_template`. El resolver debe exponer esas referencias,
no copiar el contenido del template.

Todo output referencia `context_receipt.minimum_read_surface`. El agente lo
renderiza en el envelope del output, junto al artefacto, con los campos
canónicos del kernel. El recibo registra paths relativos al repositorio o
identificadores vivos y razones; nunca paths absolutos de máquina, cuerpos,
secretos ni estado vivo durable. Cuando un artefacto exige un cuerpo exacto
—por ejemplo un route prompt— el recibo queda fuera de ese cuerpo y no lo
altera.

## Puente operativo

- Mapa PM-facing: `project-os-es/docs/README.md`.
- Entrada de accion: `project-os-es/operaciones/README.md`.
- Bootloaders de adopcion: `project-os-es/adapters/README.md`.
- Catalogo de artefactos: `project-os-es/kernel/artefactos.json`.
- Catalogo de skills opcionales: `project-os-es/kernel/skills.json`.
- Archivos compactos de skills: `project-os-es/habilidades/`.
- Hidratador de `required_template`: `tools/project_os_resolve.py`.

## Catalogo

- `project-os-es/templates/route-prompt.md`: ruteo scoped hacia otra superficie;
  puede recomendar un skill opcional y una familia de terminal agent sin
  hacerlos vinculantes.
- `project-os-es/templates/pm-command-bundle.md`: única fuente canónica para
  la forma y estilo de comandos PM copy-safe.
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
