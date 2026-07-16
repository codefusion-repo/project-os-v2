# Handoff interno — baseline oficial fijado y verificación

Este documento registra el contrato estable del handoff interno autorizado por
[ADR 0005, Amendment 1](../decisions/0005-public-repository-strategy.md#amendment-1--bounded-internal-handoff-tag-exception-issue-424)
y reconciliado por
[ADR 0005, Amendment 2](../decisions/0005-public-repository-strategy.md#amendment-2--exact-internal-github-release-for-the-fixed-handoff-baseline-issue-424).

- Este documento no autoriza ninguna acción. Mergear esta reconciliación,
  cerrar la unidad de trabajo o el roadmap, crear `agent-os-cli`, transicionar
  contenido, cambiar visibilidad o settings y publicar externamente requieren
  aprobaciones PM exactas y separadas.
- Este documento conserva decisiones e identidad estable del baseline; no
  guarda el head actual de `main`, readiness, inventarios actuales, resultados
  de CI o validación, permisos ni otro estado mutable. Esa evidencia se lee
  viva cuando una operación la necesita.
- No contiene comandos para recrear, mover, editar o eliminar el tag o el
  GitHub Release existentes.

## Decisión y supersesión

La decisión PM original de issue #424 permitió conceptualmente un único tag
interno anotado y excluyó un GitHub Release. La aprobación exacta posterior del
tag conservó esa exclusión en su mensaje, que forma parte del objeto tag y del
registro histórico.

Una decisión PM posterior, exacta y aplicable a la acción material de crear un
GitHub Release interno sobre ese tag supersedió **solo** esa exclusión. No
supersedió los límites sobre publicación, visibilidad, settings, cierre,
archivo del repositorio, creación de `agent-os-cli`, transición de contenido,
implementación del CLI, sincronización o backports.

El wording anterior no se reinterpreta como si siempre hubiera permitido el
Release: permanece como evidencia de la decisión previa. ADR 0005 Amendment 2
registra la decisión vigente y esta superficie documenta su efecto acotado.

## Identidad estable del baseline

| Campo | Identidad fijada |
| --- | --- |
| Repositorio de origen | `codefusion-repo/project-os-v2` (privado, internal-only) |
| Tag | `project-os-internal-handoff-v1` |
| Tipo de tag | Anotado, nunca ligero |
| Commit del baseline oficial | `8b01e9f45b1c2449c9cc799d51ee300b6793e9dc` |
| GitHub Release interno | `Project OS internal handoff baseline`, asociado al tag fijado |
| Nueva fuente de verdad | `agent-os-cli`, únicamente después de la transición separada |
| Fecha de transición | Se fija solo cuando esa transición sea aprobada y ejecutada |

El SHA anterior identifica el baseline oficial fijado para el handoff y no un
alias del head permanentemente actual de `main`. El tag no se mueve para
incorporar commits posteriores. Cualquier head actual, incluyendo commits
posteriores al baseline, se lee vivo y se describe por separado; nunca se
presenta como contenido del Release por mera pertenencia a `main`.

La metadata mutable del GitHub Release —por ejemplo su cuerpo, estado draft o
prerelease, assets y disponibilidad— tampoco se congela en este archivo. La
identidad estable es la asociación entre el Release interno, el tag anotado y
el commit fijado; su estado operativo se verifica en GitHub.

## Invariantes de arquitectura

- `codefusion-repo/project-os-v2` permanece privado e internal-only y, tras
  la transición, congelado como baseline interno de CodeFusion.
- El tag y el GitHub Release son marcadores internos de handoff. No son un
  release público ni versionan Project OS para una audiencia externa.
- `agent-os-cli` es la futura superficie pública y, tras la transición única,
  la única fuente de verdad de Project OS y del CLI.
- La transición es única: sin sincronización bidireccional y sin backports.
- El tag no se mueve, reutiliza ni elimina. El Release no se recrea, edita ni
  elimina bajo esta reconciliación. Cualquier acción remota posterior requiere
  una unidad de trabajo y aprobación PM exacta propias.
- El tag y el Release no autorizan ninguna acción posterior.

## Gates aún separados

Cada acción siguiente conserva su propio gate y ninguna queda implícita en la
decisión del tag, en la decisión del Release o en este documento:

1. Merge del PR que reconcilia ADR 0005 y este procedimiento.
2. Cierre de issue #424.
3. Cierre de roadmap #274.
4. Archivo del repositorio o cambio de visibilidad o settings.
5. Creación de `agent-os-cli`, transición de contenido, implementación del
   CLI y cualquier publicación externa.

Cada gate requiere evidencia viva, aprobación PM exacta y separada, capacidad
real de la superficie y validación o review proporcional cuando aplique.

## Paquete de handoff

- Contenido transferible (ADR 0005 §2): la base funcional de Project OS —
  kernel ES/EN, operaciones, templates, adapters, tooling y documentación —
  junto con la base git y de contenido auditada.
- Contenido no transferible: issues, pull requests, comentarios, reviews y
  cualquier conversación histórica de GitHub de este repositorio.
- Riesgos aceptados: los registrados por decisión PM en
  [ADR 0005](../decisions/0005-public-repository-strategy.md) y en la
  [revisión Stage 0](../security/PUBLIC_READINESS_REVIEW.md)
  (F-04, F-05, F-06).
- El baseline y este paquete registran procedencia y límites; no autorizan la
  transición.

## Verificación read-only

Antes de usar el baseline como evidencia, verificar sin mutar el repositorio:

```sh
git ls-remote --tags origin \
  refs/tags/project-os-internal-handoff-v1 \
  'refs/tags/project-os-internal-handoff-v1^{}'

git cat-file -t project-os-internal-handoff-v1
# Debe imprimir: tag

git rev-parse 'project-os-internal-handoff-v1^{}'
# Debe imprimir: 8b01e9f45b1c2449c9cc799d51ee300b6793e9dc

gh release view project-os-internal-handoff-v1 \
  --repo codefusion-repo/project-os-v2 \
  --json tagName,name,isDraft,isPrerelease,publishedAt,url

gh repo view codefusion-repo/project-os-v2 \
  --json visibility,defaultBranchRef

git rev-parse origin/main
# Se reporta como head vivo y puede diferir del baseline fijado.
```

Si el tag falta, no es anotado, resuelve a otro commit, el Release no está
asociado al tag esperado o el repositorio deja de ser privado, la operación
consumidora falla cerrada. Una diferencia entre el head vivo de `main` y el
baseline fijado se reporta explícitamente, pero no mueve ni invalida por sí
sola el tag.

## Cierre y transición

- El cierre de issue #424 y el cierre de roadmap #274 son decisiones PM
  posteriores y separadas, informadas por la evidencia viva leída en ese
  momento.
- La creación de `agent-os-cli`, la transición de contenido y cualquier
  publicación ocurren después de ese cierre, cada una con su propia
  aprobación PM exacta, según ADR 0005 y los gates preservados de
  [ADR 0004](../decisions/0004-public-presentation-and-packaging.md).
