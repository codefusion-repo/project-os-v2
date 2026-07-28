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
placeholders y conserva el bloque estándar de metadata en el mismo orden. El
adapter terminal compartido usa únicamente las referencias allowlisted
`$PROJECT_OS_TARGET_ROOT` y `$PROJECT_OS_KERNEL_DIR`; define sus valores como
paths absolutos en un `.envrc` local no trackeado y no los commitees. Esta es
la única ruta normal: cárgalo manual y explícitamente en la terminal, sin
herramientas adicionales. El fast path no hace `source`, `eval` ni carga
`.envrc`; sin variables válidas falla cerrado. Un adapter
privado puede conservar paths absolutos literales, incluidos mounts neutrales
como `/workspace/...`, pero no es la ruta normal compartida. No se admiten
`$PWD`, otras variables, composición de variables ni expansión shell
arbitraria. Usa
`Notas propias del target` solo para comandos estables, paths protegidos,
restricciones de dominio o seguridad, idioma PM-facing y escalaciones. No
copies contratos de actores, modos, workflows, límites, evidencia, outputs,
estados o políticas completas: el manifest y sus referencias canónicas los
resuelven cuando se necesitan.
