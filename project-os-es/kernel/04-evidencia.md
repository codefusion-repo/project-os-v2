# 04 — Evidencia

Responsabilidad: nombrar evidencia requerida y el estado que corresponde si
falta. La fuente canonica es `kernel/evidence.json`.

Toda evidencia se lee viva desde GitHub, git o output real de comandos en el
momento de la tarea.

## Evidencia base

- `evidence.issue_scope`: issue o PR actual con objetivo, scope, out of scope y
  acceptance criteria. Si falta: `status.needs_context`.
- `evidence.source_basis`: issues, PRs, ADRs o decisiones previas citadas o
  leidas vivas. Si falta: `status.needs_context`.
- `evidence.repo_state`: archivos, ramas, diffs, historia o estado GitHub/git
  del que depende la tarea. Si falta: `status.needs_context`.
- `evidence.pm_approval`: aprobacion PM exacta para repo, issue/PR y accion o
  command bundle. Si falta: `status.blocked`.

## Repo writes y validacion

- `evidence.branch_preflight`: output real con rama, worktree, HEAD, scope de
  rama y archivos sucios/untracked antes de editar. Si falta:
  `status.needs_context`.
- `evidence.validation_output`: comandos de validacion ejecutados y resultado
  real. Si falta: `status.needs_context`. Nunca se declara done sin reportarla.

## PR, review y cierre

- `evidence.pr_diff`: changed files y diff reales del PR, mas archivos finales
  cuando el diff no alcanza. PR body, comentarios y reportes son claims. Si
  falta: `status.needs_context`.
- `evidence.review_evidence`: hallazgos o veredicto de review en PR/issue. Si
  falta: `status.needs_context`.
- `evidence.closure_evidence`: comentario de cierre con completion evidence,
  validacion real, limites preservados y referencias commit/PR. Si falta:
  `status.needs_pm_decision`.

## Target y despliegue

- `evidence.target_adoption`: identidad del target, adapters, metadata, roadmap
  anchor, version/path de kernel, notas target-owned, validacion y riesgo de
  live-state durable. Si falta: `status.needs_context`.
- `evidence.deployment_readiness`: un entorno interno aprobado, comandos
  target-owned documentados, prerrequisitos validados y secret safety sin
  valores. Si falta o es ambiguo: `status.blocked`.
