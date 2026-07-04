# PM command bundle

Responsabilidad: draftear comandos lineales y copy-safe que el PM ejecuta de
forma manual.

## Scope

{{Que hace el bundle y sobre que repo/issue/PR/rama exactos. Prosa fuera del
bloque ejecutable.}}

## Comandos

```sh
{{comandos exactos en orden}}
```

Para cuerpos largos, escribe un body file con heredoc delimitado y pasalo con
`--body-file`. No uses `exit`, `set -euo pipefail`, control flow grande ni
campos `gh --json` no soportados.

## Verificacion esperada

```sh
{{comandos read-only de verificacion con campos soportados}}
```

## Riesgo y rollback

{{Riesgo de la accion y rollback humano.}}

Este template solo da forma; merge, cierre, tags, releases, settings,
deployments y secretos requieren aprobacion PM exacta separada.
