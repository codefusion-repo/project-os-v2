# Adapters compactos en español

Estos archivos son bootloaders para adoptar Project OS en repos target. Su
responsabilidad es apuntar al kernel, a la evidencia viva y a las constraints
del target; no duplican comportamiento del kernel ni guardan estado vivo.

- `project-os-es/adapters/AGENTS.target.md`: adapter terminal/repo-wide.
- `project-os-es/adapters/BROWSER_CHAT.target.md`: adapter draft-only para browser chat.
- `project-os-es/adapters/CLAUDE.target.md`: puntero compacto a `AGENTS.md` para Claude.
- `project-os-es/adapters/GEMINI.target.md`: puntero compacto a `AGENTS.md` para Gemini.

Todo permiso de escritura exige aprobacion PM exacta, evidencia viva, preflight
cuando aplique y validacion proporcional. Estos adapters nunca autorizan por si
solos.
