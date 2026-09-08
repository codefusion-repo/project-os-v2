# PM command bundle — contrato canónico

Esta es la única fuente canónica de forma y estilo para
`output.pm_command_bundle`. Los demás artefactos solo la referencian; no
repiten ni crean reglas alternativas para comandos PM-facing. No guarda estado
vivo ni autoriza acciones: antes de redactar, lee en vivo repositorio, issue,
PR, rama, paths y el head SHA revisado.

## Closeout tras GO

Cuando `workflow.review_before_close` queda resuelto con veredicto GO sobre la
unidad y el head vigentes, ese GO es el gate de closeout. Entrega directamente
en la misma respuesta el bundle completo: ready si el PR sigue draft, merge
del head revisado, evidencia y cierre de la unidad, cleanup de la rama y
verificación final read-only. No solicita una segunda ronda de aprobación PM
por cada acción ni retiene partes del bundle a la espera de ella.

El Humano PM ejecuta el bundle; `browser_chat` solo lo draftea y nunca ejecuta
ready, merge, cierre ni cleanup. El GO no delega ejecución al agente. Conserva
las condiciones operativas: targets exactos, head revisado y cleanup solo
tras confirmar el merge. Si la evidencia cambia o el bundle queda obsoleto,
vuelve a `workflow.review_before_close` antes de usarlo.

Esta regla de entrega es exclusiva de `workflow.review_before_close` con GO
resuelto. Los demás consumidores de `output.pm_command_bundle`, incluidos
`workflow.pm_intake`, `workflow.release_readiness` y `workflow.target_adoption`,
conservan sus aprobaciones exactas. No cambia la autoridad de implementación,
corrección, deploy, release, settings ni otros workflows.

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

Reemplazo body-only de un issue existente. Esta es la ruta predeterminada solo
cuando cambia el body completo; para labels, assignees, milestones u otras
propiedades, `gh issue edit` continúa permitido. Riesgo: un target incorrecto
reemplaza el body de otro issue; rollback: repetir la secuencia con el body
anterior revisado.

```sh
cat > /tmp/issue-body.md <<'ISSUE_BODY_END'
<cuerpo Markdown revisado>
ISSUE_BODY_END

gh api --method PATCH "repos/<owner>/<repo>/issues/<issue-number>" \
  -F "body=@/tmp/issue-body.md" --silent
gh api --method GET "repos/<owner>/<repo>/issues/<issue-number>" \
  --jq '{number,html_url,updated_at}'
```

Reemplazo body-only de un PR existente. Esta es la ruta predeterminada solo
cuando cambia el body completo; para reviewers, base branch u otras
propiedades, `gh pr edit` continúa permitido. Riesgo: un target incorrecto
reemplaza el body de otro PR; rollback: repetir la secuencia con el body
anterior revisado.

```sh
cat > /tmp/pr-body.md <<'PR_BODY_END'
<cuerpo Markdown revisado>
PR_BODY_END

gh api --method PATCH "repos/<owner>/<repo>/pulls/<pr-number>" \
  -F "body=@/tmp/pr-body.md" --silent
gh api --method GET "repos/<owner>/<repo>/pulls/<pr-number>" \
  --jq '{number,html_url,updated_at}'
```

Comentario mediante body file. Scope y rollback: publica solo el comentario
revisado; el rollback humano es una corrección posterior.

```sh
cat > /tmp/pr-comment.md <<'PR_COMMENT_END'
<cuerpo Markdown revisado>
PR_COMMENT_END

gh pr comment <pr-number> --repo <owner/repo> --body-file /tmp/pr-comment.md
```

Marcar un draft como ready. Solo incluirlo si la evidencia confirma que sigue
draft. En el closeout tras GO resuelto se incluye directamente; fuera de esa
ruta requiere aprobación PM exacta para la transición.

```sh
gh pr ready <pr-number> --repo <owner/repo>
```

Merge de un head revisado. Riesgo: el merge es irreversible por repetición;
rollback: revertir el commit de merge si corresponde.

```bash
gh pr merge <pr-number> --repo <owner/repo> --merge --delete-branch \
  --match-head-commit <reviewed-head-sha> --body "Closes #<issue-number>."
```

Cierre de issue mediante body file. En el closeout tras GO resuelto incluye
la evidencia y el cierre explícito si la unidad sigue abierta después del
merge. Fuera de esa ruta requiere aprobación exacta para cierre; no lo
presupone el merge.

```sh
cat > /tmp/issue-close.md <<'ISSUE_CLOSE_END'
<evidencia de cierre revisada>
ISSUE_CLOSE_END

gh issue comment <issue-number> --repo <owner/repo> --body-file /tmp/issue-close.md
gh issue close <issue-number> --repo <owner/repo>
```

Actualización y limpieza local. Inclúyela en el bundle de closeout tras GO con
el path y rama exactos revisados; el PM la ejecuta solo tras confirmar el merge.

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
