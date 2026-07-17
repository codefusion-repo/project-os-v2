# Prompt de revision de seguridad

Responsabilidad: pedir revision OWASP sin ejecutar scanners ni exponer secretos.

```markdown
## Contexto leido vivo

{{Issue/PR/repo/superficies.}}

## Objetivo de la revision

{{Que decision debe habilitar.}}

## Destinatario

{{Revisor real; no actor kernel.}}

## Superficies sensibles

- Auth/autorizacion/sesiones.
- Input validation, uploads, redirects.
- Dependencias, admin, logging, errores y config.

## Requisitos de secretos

No imprimir, pegar, subir, citar ni resumir secretos. Redactar valores como
`[REDACTED]`; reportar solo ruta, variable y tipo de riesgo.

## Evidencia a revisar

- {{Archivos, diffs, docs, checks.}}

## Formato de hallazgos

- {{severity}} - {{referencia}} - {{riesgo}} - {{remediacion esperada}}

## Out of scope

{{No fixes, no deploy/settings, no secret-store changes sin aprobacion separada.}}

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```
