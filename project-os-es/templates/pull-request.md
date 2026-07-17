# Pull request

Responsabilidad: documentar claims, scope y validacion de un PR draft. No es
prueba de completitud hasta review contra diff/archivos finales.

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

## Source Receipt

- project_os_sources_read: {{Lista de source + reason, o [].}}
- target_sources_read: {{Lista de source + reason, o [].}}
- live_evidence_sources: {{Lista de source + reason, o [].}}
- resolved_template: project-os-es/templates/pull-request.md
- requested_skills: {{Lista de key + source, o [].}}
- tool_internal_sources: {{Lista de source + reason, o [].}}
- resolver_projected_metadata: {{Lista de source + reason, o [].}}
- model_context_sources: {{Lista de source + incorporation, o [].}}
- additional_context_reason: {{Valor permitido o none.}}

Closes #{{issue}} (on PM merge decision).
```
