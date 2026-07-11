# Adapters compactos en español

Los adapters son bootloaders copiables: conservan metadata de adopción,
punteros al kernel y constraints estables del target. El kernel, resolver, docs
y templates son dueños del comportamiento genérico; un adapter nunca autoriza
una acción ni guarda estado vivo.

- `AGENTS.target.md` es el único bootloader terminal completo.
- `CLAUDE.target.md` y `GEMINI.target.md` son shims hacia `AGENTS.md`.
- `BROWSER_CHAT.target.md` es el bootloader separado de `actor.browser_chat`:
  read-only, draft-only y sin fast path local.

Para adoptar un target, copia el adapter de la superficie, reemplaza los
placeholders y conserva el bloque estándar de metadata en el mismo orden. Usa
`Notas propias del target` solo para comandos estables, paths protegidos,
restricciones de dominio o seguridad, idioma PM-facing y escalaciones. No
copies contratos de actores, modos, workflows, límites, evidencia, outputs,
estados o políticas completas: el manifest y sus referencias canónicas los
resuelven cuando se necesitan.
