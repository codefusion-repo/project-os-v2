# Issue

Responsabilidad: draftear una unidad de trabajo verificable, una outcome por
issue.

Interpretación: el ejecutor lee la unidad por intención según
`boundary.implementation_discipline`. Objetivo, scope, out of scope,
acceptance criteria y las decisiones de `Decisiones incluidas` son
vinculantes; los ejemplos, esquemas ilustrativos y propuestas de
implementación del cuerpo son advisory.

```markdown
## Por que existe

{{1-3 frases del problema real.}}

## Objetivo

{{Resultado observable al cerrar.}}

## Source basis

- {{Roadmap, issues, PRs, ADRs o decisiones fuente.}}

## Scope

- {{Incluido. Maximo practico y verificable.}}

## Out of scope

- {{Solo errores plausibles que el agente podria intentar.}}

## Decisiones incluidas

{{Decisiones PM vinculantes si existen; omitir si no aplica.}}

## Acceptance criteria

- {{Criterios observables.}}

## Validacion

- {{Agent-run, PM-run, manual PM o sin automatizada con razon.}}

## Riesgo y rollback

{{Riesgo breve. Rollback: revertir el PR cuando aplique.}}

## Degradacion segura (solo si aplica)

- verified_evidence: {{Evidencia verificada.}}
- unavailable_evidence: {{Fuente no disponible.}}
- materiality: auxiliary
- decision_impact: {{Por que no cambia autoridad, scope ni decision material.}}
- equivalent_source_used: {{Fuente equivalente registrada o none.}}
- revalidation_required_before_write: true
```

No guardes estado vivo ni valores secretos.
