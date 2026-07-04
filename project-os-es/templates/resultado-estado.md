# Resultado de estado

Responsabilidad: devolver un estado no resuelto sin rellenar con reglas
repetidas.

```markdown
## Estado

{{status.needs_context | status.needs_pm_decision | status.blocked}}

## Falta, conflicto o bloqueo

{{Que falta o bloquea exactamente.}}

## Fuente o decision requerida

{{De donde debe venir o quien decide.}}

## Siguiente paso seguro

{{Paso minimo que preserva limites.}}
```
