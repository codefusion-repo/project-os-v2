# Reporte de ejecucion

Responsabilidad: reportar trabajo ejecutado, evidencia y validacion sin pedir
merge/cierre.

Densidad PM-facing: el resolver proyecta como `must_include` exactamente la
lista de `output.execution_report.must_include_by_density` para el nivel de
hidratación resuelto. Usa solo el bloque del nivel resuelto; no combines
niveles. La visibilidad del recibo sigue
`context_receipt_contract.pm_facing_visibility` (`minimal` y `compact` lo
ocultan; `full/debug` lo muestra); conserva siempre el recibo interno íntegro
en todos los niveles.

## Nivel minimal

```markdown
## Resultado

{{Que quedo hecho, en 1-3 lineas.}}

## Archivos o superficie

- {{Rutas exactas o superficie tocada.}}

## Validacion

- `{{comando}}` - {{resultado real}}

## Referencia

{{Unidad viva, commit o PR.}}
```

## Nivel compact

```markdown
## Scope

{{Scope implementado y out of scope respetado, en 2-4 lineas.}}

## Cambios

- {{Cambios materiales con rutas exactas.}}

## Validacion

- `{{comando}}` - {{resultado real}}
- No ejecutada: {{razon si aplica}}
- Manual PM requerida: {{si aplica}}

## Riesgos

{{Riesgos restantes y excepciones aceptadas, o ninguno.}}
```

## Nivel full/debug

```markdown
## Issue o PR

{{Unidad de trabajo.}}

## Repositorio

{{Repo target.}}

## Rama

{{Rama de trabajo.}}

## Evidencia revisada

- {{Issue/PR/roadmap/ADR/diff/comentarios leidos vivo.}}

## Archivos cambiados

- {{Rutas exactas.}}

## Validacion

- `{{comando}}` - {{resultado real}}
- No ejecutada: {{razon si aplica}}
- Manual PM requerida: {{claridad/copy/UX/producto si aplica}}

## Riesgos y limitaciones

{{Riesgos restantes, out-of-scope respetado y excepciones aceptadas.}}

## Commit o PR

{{Referencia si aplica.}}

## Trabajo restante

{{Follow-ups o ninguno.}}

## Correction report (solo al corregir un PR revisado)

{{Publicar como comentario append-only en el PR, sin editar el body ni ningun
comentario o review previo.}}

- Review o comentario fuente: {{referencia exacta al review o comentario}}
- Head anterior: {{sha revisado}}
- Head corregido: {{sha nuevo}}
- Findings abordados: {{cada blocking-correction con el cambio y su resultado}}
- Commits o rango: {{referencia}}
- Sin merge ni cierre: {{confirmacion de que no hubo merge ni cierre}}

<!-- context-receipt:pm-facing-conditional -->
## Recibo de fuentes

- project_os_sources_read: {{Lista de source + reason, o [].}}
- target_sources_read: {{Lista de source + reason, o [].}}
- live_evidence_sources: {{Lista de source + reason, o [].}}
- resolved_template: {{Path exacto o none.}}
- requested_skills: {{Lista de key + source, o [].}}
- tool_internal_sources: {{Lista de source + reason, o [].}}
- resolver_projected_metadata: {{Lista de source + reason, o [].}}
- model_context_sources: {{Lista de source + incorporation, o [].}}
- additional_context_reason: {{Valor permitido o none.}}
<!-- /context-receipt -->
```
