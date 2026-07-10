# PM command bundle — contrato canónico

Esta es la única fuente canónica de forma y estilo para
`output.pm_command_bundle`. Los demás artefactos solo la referencian; no
repiten ni crean reglas alternativas para comandos PM-facing. No guarda estado
vivo ni autoriza acciones: antes de redactar, lee en vivo repositorio, issue,
PR, rama, paths y el head SHA revisado.

## Forma por defecto

El bundle por defecto es una secuencia corta, lineal y legible que el PM puede
copiar y ejecutar de arriba abajo. Declara scope, condiciones manuales, riesgo
y rollback en prosa, fuera de los bloques ejecutables. Entrega uno o, como
máximo, pocos bloques nativos `bash` o `sh`, en orden. Cada bloque debe poder
copiarse completo con su botón de copia y conservar bytes shell válidos,
incluidos saltos de línea, barras invertidas y heredocs.

Usa targets exactos ya revisados: `--repo`, número de PR/issue, rama, paths y,
si aplica, head SHA. Usa solamente campos `gh --json` confirmados como
soportados. Termina con verificación read-only del estado final.

No entregues shell en writing blocks, blockquotes, listas indentadas, texto
inline ni otras superficies que puedan transformar saltos, barras invertidas o
heredocs; tampoco uses fences anidados.

## Prohibido por defecto

- Cadenas extensas unidas con `&&` o `||`, command substitutions como guards y
  `test` encadenados que aborten el resto.
- `exit`, `set -e`, `set -u`, `set -o pipefail` o equivalentes.
- Bloques grandes `if`, `case`, loops o funciones shell, y guards que corten o
  corrompan la sesión.
- Preflights repetidos después de un `workflow.review_before_close` resuelto.
- `gh pr view --comments` si una consulta más acotada evita dependencias
  GraphQL o warnings innecesarios.

Un bundle defensivo o preflight-heavy solo se permite si el PM lo solicita
explícitamente, o si la evidencia falta, está obsoleta, entra en conflicto o
aún no fue revisada. En ese caso, sepáralo por fases y explica en prosa qué
debe comprobar el PM entre bloques; nunca lo conviertas en un programa shell
que se autoaborta.

## Ejemplos compactos

Los valores angulares son valores exactos leídos en vivo al redactar, no datos
que el PM deba descubrir ejecutando el bundle.

Comentario mediante body file. Scope y rollback: publica solo el comentario
revisado; el rollback humano es una corrección posterior.

```sh
cat > /tmp/pr-comment.md <<'PR_COMMENT_END'
<cuerpo Markdown revisado>
PR_COMMENT_END

gh pr comment <pr-number> --repo <owner/repo> --body-file /tmp/pr-comment.md
```

Marcar un draft como ready. Solo incluirlo si la evidencia confirma que sigue
draft y existe aprobación PM exacta para esa transición.

```sh
gh pr ready <pr-number> --repo <owner/repo>
```

Merge de un head revisado. Riesgo: el merge es irreversible por repetición;
rollback: revertir el commit de merge si corresponde.

```bash
gh pr merge <pr-number> --repo <owner/repo> --merge --delete-branch \
  --match-head-commit <reviewed-head-sha> --body "Closes #<issue-number>."
```

Cierre de issue mediante body file. Solo incluirlo con aprobación exacta para
cierre; no lo presupone el merge.

```sh
cat > /tmp/issue-close.md <<'ISSUE_CLOSE_END'
<evidencia de cierre revisada>
ISSUE_CLOSE_END

gh issue comment <issue-number> --repo <owner/repo> --body-file /tmp/issue-close.md
gh issue close <issue-number> --repo <owner/repo>
```

Actualización y limpieza local. Solo incluirla tras un merge confirmado y con
el path y rama exactos revisados.

```sh
git -C <local-path> switch main
git -C <local-path> pull --ff-only origin main
git -C <local-path> branch -D <work-branch>
git -C <local-path> fetch --prune origin
```

Verificación final read-only: este debe ser el último bloque del bundle.

```sh
gh pr view <pr-number> --repo <owner/repo> --json state,mergedAt,headRefOid
gh issue view <issue-number> --repo <owner/repo> --json state,closedAt
git -C <local-path> status --short --branch
```
