# Getting Started (Primeros Pasos con Project OS)

Project OS facilita la planificación, revisión y delegación segura hacia agentes de IA usando **GitHub como la única memoria viva compartida**. No depende de la memoria de las sesiones de chat.

## 1. Adopción en Target Existente
1. Copia `adapters/AGENTS.target.md` hacia tu repositorio y nómbralo `AGENTS.md`.
2. Completa los placeholders de `TARGET_REPOSITORY` y `KERNEL_LOCAL_PATH`.
3. (Opcional) Adapta/copia `CLAUDE.md` o `GEMINI.md` según el LLM principal.

## 2. Iniciar un Nuevo Proyecto (Bootstrap)
Si no existe el repositorio:
1. Inicia un nuevo repositorio en blanco.
2. Invoca la operación `templates/operations/02-iniciar-bootstrap-nuevo-proyecto.md` desde tu Browser Chat.
3. El sistema sugerirá la estructura inicial y el roadmap de fundación. Adopta el kernel como se indica arriba.

## 3. Uso en Browser Chat (Compañero PM)
Browser Chat es tu **compañero de revisión y redacción (draft-only)**:
- Empieza pasando `templates/operations/00-activar-sesion-browser-chat.md` al LLM en el navegador.
- Pide revisiones de PRs, redactar route-prompts, o buscar desalineaciones.
- Browser Chat **no escribe código**, pero prepara comandos o delegaciones exactas.

## 4. Uso de Terminal Agents (Ejecutores)
Los Terminal Agents **ejecutan trabajo ruteado**:
- **No hay una operación aislada "setup terminal agent" para el PM**. El setup real es el archivo `AGENTS.md` subido en tu repo.
- El agente lee el kernel automáticamente desde su sistema de archivos local y recibe un "route-prompt" (ej. redactado por `templates/operations/07-draftear-route-prompt-para-implementar-issue.md`).
- Ejecutará el código solo bajo autorización (ej. `PM_AUTHORIZATION_STATUS`).

Para instrucciones de seguridad de Github, lee `docs/GITHUB_ACCESS.md`.
