# Plan de implementacion manual

Responsabilidad: draftear instrucciones humano-ejecutables sin reclamar edits.

Trazabilidad PM-facing: `Archivos a inspeccionar` y el plan anclado son la
representación canónica. No agregues un bloque de recibo; la procedencia
detallada se entrega solo cuando el PM la solicita para auditoría, debugging,
revisión de seguridad o autorización, o investigación de una resolución
incorrecta.

```markdown
## Objetivo

{{Resultado esperado.}}

## Archivos a inspeccionar

- {{Ruta y razon.}}

## Archivos a modificar

- {{Ruta y ancla verificable.}}

## Plan de cambios

1. {{Cambio por archivo/ancla.}}

## Validacion

- `{{comando}}` - {{que debe probar}}

## QA manual

- {{Chequeo humano.}}

## Riesgos y rollback

{{Riesgos y como revertir.}}

## Siguiente operacion recomendada

{{Operacion Project OS.}}

## Declaracion de no escritura

Este plan no edito codigo, no ejecuto validacion y no concede permisos.

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```
