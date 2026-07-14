# Readiness y paquete de handoff interno — issue #424

- Fecha de preparación: 2026-07-14
- Unidad de trabajo: issue #424; roadmap #274 (KOPS).
- Base de la decisión:
  [ADR 0005](../decisions/0005-public-repository-strategy.md) y su
  Amendment 1 (excepción acotada de tag interno de handoff, decisión PM
  Opción B registrada en issue #424).
- Commit base de preparación: `01aaad811ca7a4618ae008b1657b2a81df2451fc`
  (`main` al momento de preparar este documento). **Este no es el SHA del
  tag**: el SHA final se fija únicamente después del merge del PR de este
  issue y de confirmar la validación final (ver
  [Procedimiento para fijar el SHA](#procedimiento-para-fijar-el-sha)).
- Este documento no autoriza ninguna acción. La creación del tag, la
  creación de `agent-os-cli`, la transición de contenido, cualquier cambio
  de visibilidad o settings y el cierre de #424 o #274 requieren, cada uno,
  aprobación PM exacta y separada.

## Estado de readiness (al 2026-07-14)

- Stage 0 (public-readiness, #417 / PR #418): completado con veredicto
  `GO_WITH_BLOCKERS`; ver
  [PUBLIC_READINESS_REVIEW.md](../security/PUBLIC_READINESS_REVIEW.md).
- Blockers de Stage 0: B1 resuelto por #419 / PR #420; B2 y B3 resueltos por
  #421 / PR #425; B4 resuelto por #422 /
  [ADR 0005](../decisions/0005-public-repository-strategy.md) (estrategia de
  repositorio separado: este repositorio no se publica).
- Stage 1 documental (#423 / PR #427): completado; presentación pública y
  onboarding bilingüe preparados como material reusable por la futura
  superficie pública, sin publicar nada desde este repositorio.
- ADR 0005 Amendment 1: enmienda documental introducida por el PR de este
  issue; permite conceptualmente un único tag interno anotado de handoff sin
  autorizar su creación.
- Validación local del PR de este issue: registrada en el propio PR
  (kernel ES/EN, tests, `git diff --check`, links, barrido de secretos).
- Readiness final: se confirma sobre el head final de `main` después del
  merge, con GitHub Actions verdes sobre ese head y MOS-3.7 completado antes
  del merge. Hasta entonces el readiness es preparatorio, no definitivo.

## Inventario de refs y tags (2026-07-14, read-only)

Tags existentes (locales y remotos coinciden):

| Tag | Naturaleza |
| --- | --- |
| `project-os-lab-v0.1.0` … `project-os-lab-v0.1.4` | serie interna de laboratorio |
| `project-os-lab-v0.2.0`, `project-os-lab-v0.3.0` | serie interna de laboratorio |
| `target-dogfood-baseline-2026-06-16` | baseline interno de dogfood |
| `v2-min-dogfood.0` | baseline interno de dogfood |

Ramas: `main` (default), `work/422-public-repository-strategy` (histórica) y
la rama de trabajo de este issue.

GitHub Releases existentes (internos, en repositorio privado):
`project-os-lab-v0.1.2`, `project-os-lab-v0.1.3`, `project-os-lab-v0.1.4`
(marcado `Latest`) y `target-dogfood-baseline-2026-06-16`. Ninguno se mueve,
reutiliza ni elimina en esta unidad de trabajo, y el tag de handoff **no**
debe sumarse a esta lista: no tendrá GitHub Release asociado.

Conclusión: el nombre candidato no colisiona con ningún ref ni release
existente y no pertenece a ninguna serie previa.

## Propuesta de tag

### Nombre propuesto

`project-os-internal-handoff-v1`

- No colisiona con ningún tag, rama ni ref existente (inventario anterior).
- Contiene `internal-handoff`, que lo distingue inequívocamente de un
  release público y de la serie `project-os-lab-v*`.
- No sigue un esquema semver de producto (`vX.Y.Z`); el sufijo `v1` numera
  el marcador de handoff, no una versión publicable.
- Estado: **candidato**. El nombre exacto queda sujeto a aprobación PM
  exacta y separada junto con el mensaje y el SHA.

### Mensaje propuesto (tag anotado)

```text
Project OS internal handoff baseline (issue #424)

Marcador interno del baseline final del kernel de project-os-v2 antes de la
transicion unica hacia agent-os-cli (ADR 0005, Amendment 1).

No es un release publico ni un GitHub Release. No autoriza publicacion,
cambio de visibilidad, creacion de agent-os-cli, transicion de contenido ni
implementacion del CLI. Cada una de esas acciones requiere aprobacion PM
exacta y separada.
```

El tag debe ser **anotado** (`git tag -a`), nunca ligero, para que el
mensaje, el tagger y la fecha queden registrados en el objeto tag.

## Procedimiento para fijar el SHA

El SHA nunca se fija antes del merge. Secuencia:

1. Completar MOS-3.7 (review-before-close) sobre el PR de este issue.
2. El PM mergea el PR con su aprobación exacta y separada de merge.
3. Confirmar GitHub Actions verdes sobre el head final de `main`.
4. Fijar `SHA_FINAL_MAIN` con `git rev-parse main` actualizado; debe ser el
   merge commit del PR de este issue y coincidir con el estado validado.
5. Solicitar aprobación PM exacta y separada del trío nombre + mensaje +
   SHA antes de ejecutar el command bundle.

## Paquete de handoff

| Campo | Valor |
| --- | --- |
| Repositorio de origen | `codefusion-repo/project-os-v2` (privado, internal-only) |
| Tag | `project-os-internal-handoff-v1` (candidato; anotado, interno) |
| SHA | `<SHA_FINAL_MAIN>` — se fija después del merge, nunca antes |
| Fecha del tag | `<FECHA_TAG>` — la fecha en que el PM ejecute el bundle aprobado |
| Fecha de transición | `<FECHA_TRANSICION>` — se fija cuando la transición hacia `agent-os-cli` sea aprobada por separado |
| Nueva fuente de verdad | `agent-os-cli`, tras la transición única |

- Contenido transferible (ADR 0005 §2): la base funcional de Project OS —
  kernel ES/EN, operaciones, templates, adapters, tooling y documentación —
  junto con la base git y de contenido auditada.
- Contenido no transferible: issues, pull requests, comentarios, reviews y
  cualquier conversación histórica de GitHub de este repositorio.
- Riesgos aceptados (decisión PM en #422, registrada en ADR 0005): F-04
  (fixture sintético con forma de secreto en el historial), F-05 (nombre de
  proyecto interno en el historial), F-06 (nombre personal y emails en
  metadata de commits).
- Reglas de la transición: transición **única**; sin sincronización
  bidireccional; sin backports; este repositorio queda congelado como
  baseline interno de CodeFusion después de la transición.
- El tag y este paquete **no** son autorización para ejecutar la
  transición; solo registran procedencia y límites.

## PM command bundle (copy-safe)

Ejecutar solo después de la aprobación PM exacta y separada del nombre,
mensaje y SHA. Reemplazar `<SHA_FINAL_MAIN>` por el SHA fijado según el
procedimiento anterior. El bundle no crea GitHub Releases ni cambia
visibilidad o settings.

```sh
git fetch origin --prune
git checkout main
git pull --ff-only
git rev-parse main
# Debe imprimir exactamente <SHA_FINAL_MAIN>; si no coincide, detenerse.

git tag -a project-os-internal-handoff-v1 <SHA_FINAL_MAIN> \
  -m "Project OS internal handoff baseline (issue #424)" \
  -m "Marcador interno del baseline final del kernel de project-os-v2 antes de la transicion unica hacia agent-os-cli (ADR 0005, Amendment 1)." \
  -m "No es un release publico ni un GitHub Release. No autoriza publicacion, cambio de visibilidad, creacion de agent-os-cli, transicion de contenido ni implementacion del CLI. Cada una de esas acciones requiere aprobacion PM exacta y separada."

git push origin refs/tags/project-os-internal-handoff-v1
```

## Verificación post-tag (read-only)

Después de pushear el tag, verificar sin mutar nada:

```sh
git fetch origin --prune
git cat-file -t project-os-internal-handoff-v1
# Debe imprimir: tag  (objeto anotado, no lightweight)

git cat-file -p project-os-internal-handoff-v1
# Revisar: object = <SHA_FINAL_MAIN>, tagger y mensaje interno completo.

git ls-remote --tags origin project-os-internal-handoff-v1
# El tag debe existir en el remoto y apuntar al objeto tag esperado.

git branch --contains <SHA_FINAL_MAIN> --format='%(refname:short)'
# Debe incluir: main

gh release list --repo codefusion-repo/project-os-v2
# No debe listar project-os-internal-handoff-v1 ni ningún release nuevo.

gh repo view codefusion-repo/project-os-v2 --json visibility --jq .visibility
# Debe imprimir: PRIVATE
```

## Evidencia para considerar el cierre de roadmap #274

El cierre de #274 permanece como decisión PM posterior y separada. Estado
preparado por esta unidad de trabajo:

- Completado: Stage 0 y sus blockers B1–B4; ADR 0003, 0004 y 0005; Stage 1
  documental (#423 / PR #427); enmienda ADR 0005 Amendment 1 y este paquete
  de readiness/handoff (PR de #424).
- Pendiente antes de considerar el cierre: merge del PR de #424; CI verde
  sobre el head final; fijación del SHA; aprobación PM exacta del tag;
  creación y verificación post-tag del tag interno.
- Fuera de la secuencia de cierre: la creación de `agent-os-cli`, la
  transición de contenido y cualquier publicación ocurren **después** del
  cierre de #274 según la secuencia
  `#422 → #423 → #424 → cierre de #274 → nuevo repositorio y CLI`, cada una
  con su propia aprobación PM exacta.

## Trazabilidad

- Issue #424 (re-scoped: readiness, handoff y tag interno; decisión PM
  Opción B) — unidad de trabajo de este documento.
- Issue #423 / PR #427 — Stage 1 documental completado.
- Issue #422 / [ADR 0005](../decisions/0005-public-repository-strategy.md)
  — estrategia de repositorio separado y resolución de B4.
- [ADR 0004](../decisions/0004-public-presentation-and-packaging.md) —
  camino staged docs-first.
- [Revisión Stage 0](../security/PUBLIC_READINESS_REVIEW.md) — gate de
  public-readiness y findings F-04/F-05/F-06.
- Roadmap #274 — secuencia y cierre posterior.
