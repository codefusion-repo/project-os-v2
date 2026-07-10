# GEMINI.md (adapter Gemini para target)

Copia este archivo al repo target como `GEMINI.md` despues de copiar
`project-os-es/adapters/AGENTS.target.md` como `AGENTS.md`. Reemplaza
`{{PLACEHOLDERS}}` y elimina este bloque inicial.

---

# GEMINI.md

GEMINI.md es un bootloader compacto para Gemini en `{{ORG/REPO}}`.

Usa el adapter terminal basado en `project-os-es/adapters/AGENTS.target.md`
como bootloader principal del target. Alli estan la identidad del repo,
`KERNEL_LOCAL_PATH` apuntando a `project-os-es/kernel`, el fast path con
`tools/project_os_resolve.py` y las reglas de estado vivo. Resuelve
comportamiento desde la superficie espanola y estado del target desde
GitHub/git al momento de la tarea.

GEMINI.md no concede permisos y no guarda estado vivo. Falla cerrado ante
kernel faltante, evidencia faltante, autoridad ambigua o validacion requerida
fallida. Usa validacion proporcional desde `project-os-es/docs/reglas.md` y el
kernel espanol resuelto; no impongas tests Project OS al target salvo que el
riesgo del issue lo justifique.
