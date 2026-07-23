# Handoff interno — contrato final v3 y verificación

Este documento registra el contrato final del handoff interno definido por
[ADR 0005, Amendment 3](../../../docs/decisions/0005-public-repository-strategy.md#amendment-3--final-internal-handoff-marker-v3-issue-438)
sobre la historia registrada por
[Amendment 1](../../../docs/decisions/0005-public-repository-strategy.md#amendment-1--bounded-internal-handoff-tag-exception-issue-424)
y
[Amendment 2](../../../docs/decisions/0005-public-repository-strategy.md#amendment-2--exact-internal-github-release-for-the-fixed-handoff-baseline-issue-424).

- Este documento no autoriza ninguna acción. Mergear el PR documental de
  issue #438, crear y pushear el tag final, crear su GitHub Release interno,
  cerrar la unidad de trabajo o el roadmap, crear `agent-os-cli`,
  transicionar contenido, cambiar visibilidad o settings y publicar
  externamente requieren aprobaciones PM exactas y separadas.
- Este documento conserva decisiones e identidades históricas verificadas y
  el contrato final previsto; no guarda el head actual de `main`, readiness,
  resultados de CI o validación, permisos ni otro estado mutable. Esa
  evidencia se lee viva cuando una operación la necesita.
- No contiene comandos mutantes como autoridad durable: no incluye comandos
  para crear, recrear, mover, editar o eliminar tags o GitHub Releases. Los
  comandos mutantes del tag y del Release se draftean en el momento de la
  ejecución (MOS-3.11 y MOS-3.12) y quedan gateados por su aprobación PM
  exacta.

## Historia verificada: v1 y v2

`project-os-internal-handoff-v1` y `project-os-internal-handoff-v2` existen,
fueron verificados en vivo y se conservan como marcadores históricos de
etapas anteriores. Después de issue #438, ninguno de los dos representa el
baseline final: no se presentan como identidad final del handoff y no se
mueven, reutilizan, reemplazan, editan ni eliminan.

| Campo | v1 | v2 |
| --- | --- | --- |
| Tag anotado (objeto) | `901676d358d37423d8a64896f278075469deb2e8` | `e9bafbf1b088e9973bd0dc6e5781415ccc09e000` |
| Commit (peeled) | `8b01e9f45b1c2449c9cc799d51ee300b6793e9dc` | `57c6b5176cc43606191418faf884915888cd9202` |
| Título aprobado del Release interno | `Project OS internal handoff baseline` | `Project OS final internal handoff baseline` |
| Papel histórico | Baseline oficial fijado del handoff (Amendments 1 y 2) | Estado del repositorio inmediatamente después del merge de PR #437 |

Decisiones PM durables exactas, en orden cronológico verificado:

- aprobación tag-only de `v1`:
  [issuecomment-4976581909](https://github.com/codefusion-repo/project-os-v2/issues/424#issuecomment-4976581909)
  (`2026-07-15T03:30:23Z`);
- decisión posterior del Release interno de `v1`:
  [issuecomment-4987453334](https://github.com/codefusion-repo/project-os-v2/issues/424#issuecomment-4987453334)
  (`2026-07-16T02:14:10Z`);
- dirección y aprobación exacta de `v2`:
  [issuecomment-4987758661](https://github.com/codefusion-repo/project-os-v2/issues/424#issuecomment-4987758661)
  (`2026-07-16T03:08:14Z`) e
  [issuecomment-4987814297](https://github.com/codefusion-repo/project-os-v2/issues/424#issuecomment-4987814297)
  (`2026-07-16T03:19:20Z`).

Los SHAs anteriores identifican marcadores históricos fijados y no alias del
head permanentemente actual de `main`. Los tags no se mueven para incorporar
commits posteriores. El wording de las decisiones anteriores no se
reinterpreta retroactivamente; permanece como evidencia de cada etapa.

## Identidad final prevista: v3

| Campo | Identidad final prevista |
| --- | --- |
| Repositorio | `codefusion-repo/project-os-v2` (privado, internal-only) |
| Tag final | `project-os-internal-handoff-v3` |
| Tipo de tag | Anotado, nunca ligero |
| GitHub Release | Exactamente uno, interno, asociado al tag final |
| Título previsto | `Project OS final internal handoff baseline v3` |
| Draft | `false` |
| Prerelease | `false` |
| Commit final | Se obtiene únicamente del head remoto vivo de `main` después del merge del PR documental de issue #438 |

El commit final **no se almacena anticipadamente** en este documento, en el
ADR, en el issue, en los tests ni en el PR. Cualquier SHA que aparezca aquí
identifica exclusivamente historia verificada de `v1` y `v2`.

El `name` vivo del Release y el resto de su metadata mutable no se congelan
en este archivo: se releen en GitHub. Si el `name` vivo difiere del título
aprobado, la operación consumidora reporta drift y falla cerrada antes de
depender del Release; no reinterpreta la decisión ni edita la metadata.

## Orden obligatorio

La secuencia es estricta y no se reordena:

`documentación → validación → merge → SHA post-merge → tag → Release`

1. **Documentación**: el PR documental de issue #438 actualiza ADR 0005,
   este procedimiento y sus regresiones. No se crea `v3` en esta fase.
2. **Validación**: kernels ES/EN, tests focalizados, suite completa,
   links/anchors, revisión proporcional de secretos y PII y CI verde sobre
   el head revisado del PR.
3. **Merge**: requiere aprobación PM exacta del merge tras MOS-3.7.
4. **SHA post-merge**: solo después del merge se lee el head remoto de
   `main` directamente y se confirma que corresponde al merge del PR de
   issue #438 sin commits posteriores no revisados. Ese head validado es el
   único origen del commit de `v3`.
5. **Tag**: con aprobación PM exacta y separada, se crea y pushea el tag
   anotado `project-os-internal-handoff-v3` sobre ese SHA post-merge.
   Antes de crearlo se ejecuta el preflight local read-only de v3 (ver
   [Verificación read-only](#verificación-read-only)) con output real: el
   tag no debe existir local ni remotamente, el worktree debe estar limpio
   y el checkout local debe apuntar exactamente al SHA post-merge aprobado.
6. **Release**: con otra aprobación PM exacta y separada, se crea el único
   GitHub Release interno asociado al tag `v3`. Antes de crearlo se
   verifica que el Release no exista.

El tag anotado y el Release quedan asociados exactamente al mismo commit
post-merge. Crear `v3` antes del merge documental volvería a fijar un
baseline incompleto y está prohibido.

## Aprobaciones PM exactas y separadas

- La aprobación del merge del PR documental no autoriza el tag ni el
  Release.
- Crear y pushear el tag anotado `v3` requiere su propia aprobación PM
  exacta que nombre proyecto, unidad de trabajo (issue #438), acción, tag,
  mensaje y SHA post-merge validado.
- Crear el GitHub Release interno requiere otra aprobación PM exacta y
  separada que nombre el tag, el título y el estado draft/prerelease.
- Ninguna de esas aprobaciones queda implícita en este documento, en el
  ADR, en el issue ni en el merge.

## Invariantes de arquitectura

- `codefusion-repo/project-os-v2` permanece privado e internal-only y, tras
  la transición, congelado como baseline interno de CodeFusion.
- `v1`, `v2` y `v3` son marcadores internos de handoff. No son releases
  públicos ni versionan Project OS para una audiencia externa.
- Los artefactos anteriores no se mueven ni eliminan: `v1` y `v2` no se
  recrean, editan, reemplazan ni borran bajo este contrato. Una vez
  publicado, `v3` tampoco se mueve, reutiliza ni elimina; cualquier
  corrección remota requiere una decisión PM exacta dentro de issue #438
  mientras permanezca abierto.
- No habrá `v4` ni otro follow-up de finalización derivado de este flujo.
- `agent-os-cli` es la futura superficie pública y, tras la transición
  única, la única fuente de verdad de Project OS y del CLI. La transición
  es única: sin sincronización bidireccional y sin backports.
- El tag y el Release no autorizan ninguna acción posterior: publicación,
  visibilidad, settings, cierre, archivo del repositorio, creación de
  `agent-os-cli`, transición de contenido, implementación del CLI,
  sincronización o backports conservan sus gates.

## Gates aún separados

1. Merge del PR documental de issue #438.
2. Creación y push del tag anotado `v3` (aprobación PM exacta propia).
3. Creación del GitHub Release interno `v3` (aprobación PM exacta propia).
4. Cierre de issue #438, solo tras verificar toda la evidencia final.
5. Cierre de roadmap #274.
6. Archivo del repositorio o cambio de visibilidad o settings.
7. Creación de `agent-os-cli`, transición de contenido, implementación del
   CLI y cualquier publicación externa.

Cada gate requiere evidencia viva, aprobación PM exacta y separada,
capacidad real de la superficie y validación o review proporcional cuando
aplique.

## Verificación read-only

Todas las consultas siguientes leen estado sin mutarlo. Las consultas
`git ls-remote` leen las refs directamente desde el remoto: son
reproducibles en un clone sin tags hidratados y no dependen de
remote-tracking refs locales potencialmente obsoletas. No crean, actualizan
ni eliminan refs locales o remotas. No requiere tag local.

Historia (`v1` y `v2`):

```sh
git ls-remote --exit-code --tags origin \
  refs/tags/project-os-internal-handoff-v1 \
  'refs/tags/project-os-internal-handoff-v1^{}'
# Debe devolver el objeto tag 901676d358d37423d8a64896f278075469deb2e8
# y el peeled commit 8b01e9f45b1c2449c9cc799d51ee300b6793e9dc.

git ls-remote --exit-code --tags origin \
  refs/tags/project-os-internal-handoff-v2 \
  'refs/tags/project-os-internal-handoff-v2^{}'
# Debe devolver el objeto tag e9bafbf1b088e9973bd0dc6e5781415ccc09e000
# y el peeled commit 57c6b5176cc43606191418faf884915888cd9202.

gh release view project-os-internal-handoff-v1 \
  --repo codefusion-repo/project-os-v2 \
  --json tagName,name,isDraft,isPrerelease,publishedAt,url

gh release view project-os-internal-handoff-v2 \
  --repo codefusion-repo/project-os-v2 \
  --json tagName,name,isDraft,isPrerelease,publishedAt,url
# En cada caso tagName debe identificar el tag histórico esperado y name se
# compara con el título aprobado correspondiente.
```

Head remoto vivo y visibilidad:

```sh
git ls-remote --exit-code --heads origin refs/heads/main
# Reporta el head remoto vivo de main; después del merge del PR documental,
# ese head debe corresponder al merge de issue #438 y es el único origen
# del commit de v3.

gh repo view codefusion-repo/project-os-v2 \
  --json visibility,defaultBranchRef
# La visibilidad debe seguir siendo privada.
```

Ausencia previa de `v3` (obligatoria antes de crear el tag y el Release):

```sh
git ls-remote --exit-code --tags origin \
  refs/tags/project-os-internal-handoff-v3 \
  'refs/tags/project-os-internal-handoff-v3^{}'
# Antes de la creación debe FALLAR (exit code distinto de cero): el tag v3
# no debe existir local ni remotamente.

gh release view project-os-internal-handoff-v3 \
  --repo codefusion-repo/project-os-v2 \
  --json tagName,name,isDraft,isPrerelease,publishedAt,url
# Antes de la creación debe FALLAR: el Release v3 no debe existir.
# Después de la creación, ambas consultas verifican el tag anotado, su
# peeled commit igual al SHA post-merge validado, la asociación del Release
# al tag v3, el título previsto y draft=false, prerelease=false.
```

Preflight local de v3 (obligatorio antes de draftear el tag; los tres
comandos son read-only, no crean, actualizan ni eliminan refs, y su output
real se captura como evidencia):

```sh
git tag --list project-os-internal-handoff-v3
# Resultado esperado: salida vacía. El tag v3 no debe existir en el clone
# local. Cualquier salida no vacía es drift y la operación falla cerrada
# sin draftear el tag.

git status --short --branch
# Resultado esperado: únicamente la línea de rama (`## ...`), sin entradas
# de archivos. El worktree debe estar limpio: sin cambios staged, unstaged
# ni untracked. Cualquier entrada adicional falla cerrada.

git rev-parse HEAD
# Resultado esperado: exactamente el SHA post-merge aprobado, leído en vivo
# del head remoto de `main` en el paso 4 del orden obligatorio. Cualquier
# diferencia entre el checkout local y ese SHA falla cerrada antes de
# draftear el tag.
```

Si un tag histórico falta, no es anotado o resuelve a otro commit; si un
Release no está asociado al tag esperado o su `name` vivo difiere del título
aprobado; si `v3` existe antes de su aprobación —local o remotamente—; si
el head remoto no corresponde al merge esperado; si el worktree no está
limpio; si `git rev-parse HEAD` no coincide con el SHA post-merge aprobado;
o si el repositorio deja de ser privado, la operación consumidora reporta
drift y falla cerrada. Una diferencia entre el
head vivo de `main` y un marcador histórico se reporta explícitamente, pero
no mueve ni invalida por sí sola ningún tag.

## Paquete de handoff

- Contenido transferible (ADR 0005 §2): la base funcional de Project OS —
  kernel ES/EN, operaciones, templates, adapters, tooling y documentación —
  junto con la base git y de contenido auditada.
- Contenido no transferible: issues, pull requests, comentarios, reviews y
  cualquier conversación histórica de GitHub de este repositorio.
- Riesgos aceptados: los registrados por decisión PM en
  [ADR 0005](../../../docs/decisions/0005-public-repository-strategy.md) y en la
  [revisión Stage 0](../security/PUBLIC_READINESS_REVIEW.md)
  (F-04, F-05, F-06).
- El baseline y este paquete registran procedencia y límites; no autorizan
  la transición.

## Cierre y transición

- La evidencia final de `v3` se registra en issue #438, que se cierra solo
  después de verificar tag, Release, visibilidad y head remoto, sin crear
  otro follow-up de finalización.
- El cierre de roadmap #274 es una decisión PM posterior y separada,
  informada por la evidencia viva leída en ese momento.
- La creación de `agent-os-cli`, la transición de contenido y cualquier
  publicación ocurren después de ese cierre, cada una con su propia
  aprobación PM exacta, según ADR 0005 y los gates preservados de
  [ADR 0004](../../../docs/decisions/0004-public-presentation-and-packaging.md).
