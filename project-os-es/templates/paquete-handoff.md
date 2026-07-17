# Paquete de handoff

Responsabilidad: transferir contexto apuntando a evidencia viva, no guardar
estado durable.

```markdown
## Estado actual

{{Referencias vivas a issue/PR/rama/checks; no SHAs salvo que el output vivo lo
requiera para la tarea inmediata.}}

## Verificado vs asumido

- Verificado: {{evidencia leida vivo.}}
- Asumido: {{claims no verificados o ninguno.}}

## Proximos pasos

- {{Paso con source basis.}}

## Decisiones abiertas para PM

- {{Decision y opciones si aplica.}}

## Limites activos

- {{No-live-state, no-autorizacion, secret safety, validacion, etc.}}

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```
