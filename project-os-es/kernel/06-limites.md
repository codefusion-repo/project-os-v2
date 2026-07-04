# 06 — Limites

Responsabilidad: resumir boundaries que siempre aplican. La fuente canonica es
`kernel/boundaries.json`.

Roles, workflows, modos, templates, prompts y outputs nunca relajan estos
limites.

## Autoridad y superficies

- `boundary.output_not_permission`: outputs, templates, roles, variables y
  route packets solo dan forma; nunca autorizan escritura.
- `boundary.draft_only_browser`: browser chat no edita ni muta GitHub/git. La
  aprobacion PM para escribir enruta a terminal; no expande browser.
- `boundary.separate_pm_approval`: merge, cierre, labels, tags, releases,
  settings, automatizacion y artefactos target requieren aprobacion PM exacta
  separada.
- `boundary.no_main_edits`: `main` es baseline limpio. Crea o cambia a rama
  scoped antes de editar.

## Evidencia y estado

- `boundary.branch_preflight`: antes de editar, commitear, pushear o abrir PR,
  verifica rama, worktree, HEAD, scope de rama y archivos ajenos.
- `boundary.no_live_state_durable`: archivos durables no guardan estado vivo:
  issues, PRs, ramas, commits, reviews, validaciones, release readiness ni
  planning state.
- `boundary.no_invented_state`: no inventes output git, estado repo/issue/PR,
  validacion, review ni aprobacion PM.
- `boundary.review_before_close`: cierre solo tras comparar issue, diff,
  changed files, archivos finales relevantes, validacion y riesgos.

## Seguridad y fail-closed

- `boundary.security_privacy`: nunca expongas ni guardes secretos, tokens,
  credenciales, keys, datos sensibles o detalles operativos confidenciales.
- `boundary.fail_closed`: ante autoridad ambigua, kernel/evidencia faltante,
  conflicto de fuentes, validacion fallida o aprobacion faltante, detente con
  el status correcto.

## Disciplina de implementacion

- `boundary.implementation_discipline`: completa el scope vivo sin rewrites
  ajenos, over-implementation, under-implementation ni abstraccion especulativa.
- `boundary.primary_path_discipline`: arregla la ruta principal; no agregues
  fallbacks para ocultar errores. Solo agrega fallback si el issue/evidencia lo
  requiere y queda validado.
- `boundary.validation_discipline`: valida proporcionalmente al riesgo; no
  agregues tests amplios, duplicados, fragiles o de confianza teatral.
- `boundary.code_clarity`: codigo autodocumentado; comenta solo intencion no
  obvia, invariantes, seguridad, APIs, migraciones, restricciones o tradeoffs.
- `boundary.context_economy`: usa solo contexto/subagentes necesarios, sin
  perder evidencia requerida, trazabilidad, validacion, secretos ni aprobacion.
- `boundary.copy_safe_commands`: command bundles PM-facing deben ser
  copy-safe, con targets exactos, cuerpos seguros y campos `gh` soportados.
