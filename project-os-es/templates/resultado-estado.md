# Resultado de estado

Responsabilidad: devolver un estado y, cuando MOS-R.3 procesa una decisión PM,
su resolución canónica sin rellenar con reglas repetidas.

Trazabilidad PM-facing: `Fuente o decision requerida` es la representación
canónica. No agregues un bloque de recibo.

En QA/readiness/deployment, usa los bloques existentes para identificar la misma
unidad, target, ref y entorno; fuentes de evidencia reutilizada/renovada y razón;
gate pendiente, responsable, aprobación exacta, rollback y postcondiciones
aplicables. Sigue el contrato común de continuidad sin crear estado persistente
ni convertir un estado resuelto de lectura/draft en autorización de ejecución.

```markdown
## Estado

{{status.resolved | status.needs_context | status.needs_pm_decision | status.blocked}}

## Resolución de decisión PM (solo si aplica)

- decision_key: {{proyecto/target · unidad · acción material · alcance exacto}}
- superseded_decision: {{decisión anterior única más reciente, exacta y suficiente; ninguna si empata}}
- current_pm_decision: {{decisión vigente o ninguna}}
- required_traceability_follow_up: {{drift durable a reconciliar o ninguno}}
- remaining_gates: {{gates independientes y su estado}}
- resulting_status: {{estado seleccionado}}
- safe_return_operation: {{operación origen segura}}

## Falta, conflicto o bloqueo

{{Que falta o bloquea exactamente.}}

## Fuente o decision requerida

{{De donde debe venir o quien decide.}}

## Siguiente paso seguro

{{Paso minimo que preserva limites.}}
```
