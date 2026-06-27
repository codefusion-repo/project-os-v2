# Public Usage Model (Modelo de Uso Público)

## ¿Qué es Project OS?
Project OS se comporta como un pequeño kernel de sistema operativo. Posee archivos de reglas (`kernel/*.json`) inmutables en tiempo de ejecución.

## Actores y Superficies
1. **Human PM**: El originador de prioridades, alcances y autoridad. Único que debe realizar comandos peligrosos (mezclar, configurar secretos, lanzar tags).
2. **Browser Chat** (`actor.browser_chat`): Entorno de charla, efímero. Lee GitHub para recuperar la historia. Sirve de acompañante analítico y prepara *drafts* (borradores de comandos o de prompts).
3. **Terminal Agent** (`actor.terminal_agent`): Agente local con acceso a consola. Recibe `route-prompts` (órdenes de trabajo estructuradas) para resolver issues específicos. Ejecuta escrituras de código y pull requests, nunca cambia prioridades sin autorización.

## La Memoria (Source of Truth)
- **NO** se confía en la retentiva del chat (`.txt` locales de historial, variables de contexto pasadas).
- La memoria a largo plazo es 100% trazable en **GitHub** (Issues, PRs, Comments).
- Si el chat falla o se vuelve incoherente, invoca `templates/operations/17-draftear-paquete-de-handoff-para-nueva-sesion.md` para empaquetar lo inmediato y abrir una nueva sesión basada puramente en el estado de GitHub.

## Operaciones / Templates
Las operaciones de la carpeta `templates/operations/` dictan instrucciones estándar y predecibles, pero no portan autorización ni estado vivo.

## Aprobación
Los `route-prompts` a terminal agents no deben asumir permisos. Deben contener un `PM_AUTHORIZATION_STATUS` explícito.
