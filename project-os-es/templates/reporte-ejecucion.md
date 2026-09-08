# Reporte de ejecucion

Responsabilidad: reportar trabajo ejecutado, evidencia y validacion sin pedir
merge/cierre.

Densidad PM-facing: el resolver proyecta como `must_include` exactamente la
lista de `output.execution_report.must_include_by_density` para la densidad de
reporte de la `CHANGE_CLASS` declarada. Esa densidad es independiente del
`HYDRATION_LEVEL` recibido: una unidad crítica resuelta en `compact` conserva el
bloque `full/debug` de este template. Usa solo el bloque de la densidad
resuelta; no combines densidades. La trazabilidad PM-facing vive en el propio
bloque —en `full/debug`, `Evidencia revisada`—; ninguna densidad agrega un
bloque de recibo.

Para deployment, usa las secciones de evidencia, validación, riesgos y trabajo
restante de la densidad resuelta para conservar unidad, target, entorno, acción,
ref esperado/observado, aprobación exacta y evidencia reutilizada/renovada con
fuente y razón. Distingue ejecución de verificación post-deploy, registra
rollback aplicable y siguiente gate; no declares éxito sin postcondiciones
verificadas ni autorización de otro entorno por continuidad.

## Densidad minimal

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

## Densidad compact

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

## Densidad full/debug

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
```
