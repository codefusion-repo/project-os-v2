# Pull request

Responsabilidad: documentar claims, scope y validacion de un PR draft. No es
prueba de completitud hasta review contra diff/archivos finales.

Trazabilidad PM-facing: `Validation` y el scope declarado son la representación
canónica. No agregues un bloque de recibo; la procedencia detallada se entrega
solo cuando el PM la solicita para auditoría, debugging, revisión de seguridad o
autorización, o investigación de una resolución incorrecta.

```markdown
## Summary

- {{Que cambia en terminos de comportamiento.}}

## Scope / Boundaries

- {{Superficies tocadas.}}
- {{Fuera de scope preservado.}}
- Merge y cierre no se solicitan por este PR.

## Validation

- `{{comando}}` - {{resultado real}}
- {{Validacion manual PM o excepcion aceptada si aplica.}}

## Security / Privacy

- {{Manejo de datos sensibles o "sin superficies sensibles tocadas".}}

Related to #{{issue}}.
```
