# GitHub Access Guidance

## Principios Actuales para Project OS
El uso actual de Project OS asume interacción mediante herramientas y permisos locales que el Humano PM posee en su entorno.

### Herramienta Primaria: GitHub CLI (`gh`)
- Las acciones de GitHub se rutean normalmente vía comandos generados para `gh` (e.g. `gh issue create`, `gh pr merge`).
- **No se requiere** configurar GitHub Apps, OAuth Apps, integraciones customizadas, o dar automatizaciones en la nube.
- La sesión usa la autenticación local (vía `gh auth login`).

### Acceso Recomendado por Superficie
- **Browser Chat**: Solo debe solicitar contexto u observar repositorios de lectura/lectura amplia. Está acordonado para actuar en modo *draft-only*, incluso si un conector técnico pudiese editar algo.
- **Terminal Agent**: Posee privilegios mínimos necesarios (`least-privilege`). Generalmente escritura sobre código, creación de Pull Requests, e Issues (para reportes de trazabilidad). Nunca debe usarse una cuenta administradora para roles de edición simple.
- **Human PM**: Conserva y ejerce las autoridades destructivas y críticas: merge, cierre final, alteración de configuraciones (settings), etiquetas (labels/milestones), creaciones de tags o releases y cualquier alteración de visibilidad de repositorio.

### Secret-Safety
- Es estrictamente prohibido imprimir, pegar en chats, hacer commit, subir, resumir, citar, o exponer *tokens*, credenciales o archivos `.env`.
- Prefiera siempre acceso "least privilege" configurado repositorio-a-repositorio, por encima de permisos de organización general (org access).
