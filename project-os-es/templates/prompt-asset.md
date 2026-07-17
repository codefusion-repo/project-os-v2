# Prompt de asset

Responsabilidad: pedir un asset a un destinatario real de diseno sin convertirlo
en actor Project OS.

```markdown
## Contexto leido vivo

{{Issue/repo/evidencia de producto.}}

## Objetivo del asset

{{Uso y resultado esperado.}}

## Destinatario

{{Persona/equipo/herramienta receptora; no actor kernel.}}

## Tipo, formato y entrega

{{2D/3D/audio/video, dimensiones, formato, cantidad y naming.}}

## Constraints de producto y marca

{{Fuente en target o evidencia PM.}}

## Accesibilidad

{{Contraste, legibilidad, alternativas, motion/audio safe.}}

## Acceptance criteria

- {{Criterios observables.}}

## Out of scope y autoridad

{{No editar target, no crear assets desde Project OS salvo scope separado.}}

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```
