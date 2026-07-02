# Getting Started (Primeros Pasos con Project OS)

Project OS facilita la planificación, revisión y delegación segura hacia agentes de IA usando **GitHub como la única memoria viva compartida**. No depende de la memoria de las sesiones de chat.

## Repositorios en Juego
La mayoría de las operaciones tienen dos repositorios:

- **Project OS repo / `KERNEL_REPOSITORY`**: contiene el kernel, adapters, templates, docs y contratos operativos. Hoy es `codefusion-repo/project-os-v2`.
- **Target repo / `TARGET_REPOSITORY`**: el producto o proyecto que se adopta, revisa, implementa o audita.

Browser Chat debe saber cuál es cuál. En desarrollo del propio Project OS,
ambos pueden ser `codefusion-repo/project-os-v2`. En adopción de un target,
normalmente son repos distintos.

## 1. Adopción en Target Existente
1. Copia `adapters/AGENTS.target.md` hacia tu repositorio y nómbralo `AGENTS.md`.
2. Completa los placeholders de `TARGET_REPOSITORY` y `KERNEL_LOCAL_PATH`.
3. (Opcional) Adapta/copia `CLAUDE.md` o `GEMINI.md` según el LLM principal.

## 2. Iniciar un Nuevo Proyecto (Bootstrap)
Si no existe el repositorio:
1. Inicia un nuevo repositorio en blanco.
2. Invoca la operación `templates/operations/02-bootstrap-new-project.md` desde tu Browser Chat.
3. El sistema sugerirá la estructura inicial y el roadmap de fundación. Adopta el kernel como se indica arriba.

## 3. Uso en Browser Chat (Compañero PM)
Browser Chat es tu **compañero de revisión y redacción (draft-only)**:
- Empieza pasando `templates/operations/00-browser-chat-activation.md` al LLM en el navegador.
- Pide revisiones de PRs, redactar route-prompts, o buscar desalineaciones.
- Browser Chat **no escribe código**, pero prepara comandos o delegaciones exactas.
- Para resolver estado vivo debe poder leer contexto GitHub: el repo Project OS,
  el repo target, issues, PRs, archivos cambiados/diffs, docs, templates,
  adapters y kernel files que requiera la operación.
- Si no puede acceder al repo Project OS o al target necesario, devuelve
  `status.needs_context` y nombra exactamente qué repo, issue, PR, diff o
  archivo falta. No inventa estado.
- Su acceso es de lectura, revisión y redacción. Aunque una superficie pueda
  técnicamente mutar GitHub, la frontera `actor.browser_chat` sigue siendo
  draft-only.

## 4. Uso de Terminal Agents (Ejecutores)
Los Terminal Agents **ejecutan trabajo ruteado**:
- **No hay una operación aislada de configuración del terminal agent para el PM**. La configuración real es el archivo `AGENTS.md` subido en tu repo.
- El agente resuelve el kernel desde su sistema de archivos local y recibe un "route-prompt" (ej. redactado por `templates/operations/07-draft-issue-implementation-route-prompt.md`).
- Con checkout del kernel y repo-local Python disponibles puede usar el fast
  path desde la raíz del repo:
  ```sh
  cd "$REPOSITORY_LOCAL_PATH"
  if [ -d .venv ]; then . .venv/bin/activate; fi
  python -m tools.project_os_resolve --actor <actor> --workflow <workflow> --mode <mode> --kernel-dir "$KERNEL_LOCAL_PATH"
  ```
  La resolución manual desde `kernel/manifest.json` siempre es el fallback
  canónico. La salida del resolver solo da forma al comportamiento y no otorga
  permisos.
- Ejecutará el código solo bajo autorización (ej. `PM_AUTHORIZATION_STATUS`).
- Necesita un checkout local del target, el adapter del repo (`AGENTS.md`,
  `CLAUDE.md` o `GEMINI.md` según superficie), acceso al kernel configurado por
  `KERNEL_LOCAL_PATH`, branch de trabajo y comandos de validación del proyecto.
- Ejecuta solo después de adopción, route-prompt, execution mode apropiado y
  autorización PM exacta.

## 5. Autoridad Humana
El Human PM conserva merge, cierre de issues, tags, releases, settings,
labels/milestones, secretos, deployment y cualquier decisión de alcance. Las
operaciones rutean trabajo y drafts; no transfieren autoridad.

Para instrucciones de seguridad de GitHub, lee `docs/GITHUB_ACCESS.md`.
