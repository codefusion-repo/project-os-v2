# GitHub Access Guidance

## Principios Actuales para Project OS
El uso actual de Project OS asume interacción mediante el GitHub CLI (`gh`)
autenticado localmente en el entorno del Humano PM. Esta guía documenta el uso
local de `gh` y las expectativas de acceso de mínimo privilegio.

### Herramienta Primaria: GitHub CLI (`gh`)
- Las acciones de GitHub se rutean normalmente vía comandos generados para `gh` (e.g. `gh issue create`, `gh pr merge`).
- La sesión usa la autenticación local (vía `gh auth login`).

### Acceso Recomendado por Superficie
- **Browser Chat**: Solo debe solicitar contexto u observar repositorios en modo lectura. Está acordonado para actuar en modo *draft-only*, sin importar las capacidades técnicas de la superficie. Para operaciones normales debe poder leer el repo Project OS (`codefusion-repo/project-os-v2`) y el `TARGET_REPOSITORY` relevante, incluyendo issues, PRs, diffs, docs, templates, adapters y kernel files cuando la operación los requiera. Si no puede leer una fuente requerida, devuelve `status.needs_context` y nombra exactamente qué falta.
- **Terminal Agent**: Posee privilegios mínimos necesarios (`least-privilege`). Generalmente escritura sobre código, creación de Pull Requests, e Issues (para reportes de trazabilidad). Nunca debe usarse una cuenta administradora para roles de edición simple.
- **Human PM**: Conserva y ejerce las autoridades destructivas y críticas: merge, cierre final, alteración de configuraciones (settings), etiquetas (labels/milestones), creaciones de tags o releases y cualquier alteración de visibilidad de repositorio.

### Secret-Safety
- Es estrictamente prohibido imprimir, pegar en chats, hacer commit, subir, resumir, citar, o exponer *tokens*, credenciales o archivos `.env`.
- Prefiera siempre acceso "least privilege" configurado repositorio-a-repositorio, por encima de permisos de organización general (org access).
