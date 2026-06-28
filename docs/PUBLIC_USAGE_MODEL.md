# Public Usage Model (Modelo de Uso Público)

## ¿Qué es Project OS?
Project OS se comporta como un pequeño kernel de sistema operativo. Posee archivos de reglas (`kernel/*.json`) inmutables en tiempo de ejecución.

## Actores y Superficies
1. **Human PM**: El originador de prioridades, alcances y autoridad. Único que debe realizar comandos peligrosos (mezclar, configurar secretos, lanzar tags).
2. **Browser Chat** (`actor.browser_chat`): Entorno de charla, efímero. Lee GitHub para recuperar la historia. Sirve de acompañante analítico y prepara *drafts* (borradores de comandos o de prompts).
3. **Terminal Agent** (`actor.terminal_agent`): Agente local con acceso a consola. Recibe `route-prompts` (órdenes de trabajo estructuradas) para resolver issues específicos. Ejecuta escrituras de código y pull requests, nunca cambia prioridades sin autorización.

## Project OS Repo vs Target Repo
- **Project OS repo / `KERNEL_REPOSITORY`**: provee kernel, adapters,
  templates, docs y contratos. Para este proyecto público es
  `codefusion-repo/project-os-v2`.
- **Target repo / `TARGET_REPOSITORY`**: es el producto/proyecto adoptado,
  implementado, revisado o auditado.
- En desarrollo del propio Project OS, ambos pueden ser
  `codefusion-repo/project-os-v2`. En adopciones target, normalmente son
  repos distintos.
- Browser Chat debe saber cuál repo cumple cada rol antes de resolver una
  operación.

## La Memoria (Source of Truth)
- **NO** se confía en la retentiva del chat (`.txt` locales de historial, variables de contexto pasadas).
- La memoria a largo plazo es 100% trazable en **GitHub** (Issues, PRs, Comments).
- Si el chat falla o se vuelve incoherente, invoca `templates/operations/17-draft-handoff-package-for-new-session.md` para empaquetar lo inmediato y abrir una nueva sesión basada puramente en el estado de GitHub.
- Browser Chat necesita acceso de lectura al repo Project OS y al target cuando
  la operación lo requiera: issues, PRs, diffs, archivos cambiados, docs,
  templates, adapters y kernel files.
- Si falta acceso al repo Project OS, al target, o a evidencia concreta, devuelve
  `status.needs_context` y nombra exactamente lo faltante.

## Operaciones / Templates
Las operaciones de la carpeta `templates/operations/` dictan instrucciones estándar y predecibles, pero no portan autorización ni estado vivo.
Cada template mantiene bloques `OPERATION`, `INPUT`, `KERNEL`, `LIVE_STATE`,
`DO`, `IF`, `OUTPUT`, `LIMITS`; resuelve `kernel/manifest.json`, sigue
`resolution_sequence`, y falla cerrado ante evidencia, autoridad o estado
faltante, ambiguo o conflictivo.

## Aprobación
Los `route-prompts` a terminal agents no deben asumir permisos. Deben contener un `PM_AUTHORIZATION_STATUS` explícito.
Browser Chat sigue siendo draft-only aunque su método de acceso pueda técnicamente
mutar GitHub. El Human PM conserva merge, close, tag, release, settings,
labels/milestones, secretos y deployment. El Terminal Agent ejecuta solo tras
adopción, route-prompt, modo de ejecución correcto y autorización PM exacta.

## Future optimization / follow-up
Después de estabilizar el modelo público de operaciones, un issue futuro puede
explorar incrustar JSON estable seleccionado del kernel Project OS y templates
no operacionales en instrucciones de Browser Chat. El objetivo sería reducir
lecturas repetidas de GitHub y acelerar la resolución del kernel para Browser
Chat.

Esa optimización futura no debe almacenar estado vivo en instrucciones, no debe
reemplazar GitHub como fuente de verdad para issues, PRs, branches, diffs,
validación o estado del target, y no se implementa en este PR. Debe esperar hasta
después del issue #305 y de los follow-ups #307 y #308, si el PM todavía la
quiere.
