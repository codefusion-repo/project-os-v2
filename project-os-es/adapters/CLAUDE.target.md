# CLAUDE.md (adapter Claude para target)

Copia este archivo al repo target como `CLAUDE.md` despues de `AGENTS.md`.
Reemplaza `{{PLACEHOLDERS}}` y elimina este bloque inicial.

---

# CLAUDE.md

CLAUDE.md es un bootloader compacto para Claude en `{{ORG/REPO}}`.

Usa `AGENTS.md` como adapter terminal principal. Alli estan la identidad del
repo, `KERNEL_LOCAL_PATH`, el fast path de resolucion y las reglas de estado
vivo. Resuelve comportamiento generico desde el kernel y estado del target
desde GitHub/git al momento de la tarea.

CLAUDE.md no concede permisos y no guarda estado vivo. Falla cerrado ante
kernel faltante, evidencia faltante, autoridad ambigua o validacion requerida
fallida. Usa validacion proporcional desde `docs/VALIDATION_POLICY.md`; no
impongas tests Project OS al target salvo que el riesgo del issue lo justifique.
