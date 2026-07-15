# Handoff interno — procedimiento del tag de baseline final

Este documento define el procedimiento estable para el único tag interno
anotado de handoff permitido conceptualmente por
[ADR 0005, Amendment 1](../decisions/0005-public-repository-strategy.md#amendment-1--bounded-internal-handoff-tag-exception-issue-424).

- Este documento no autoriza ninguna acción. Crear el tag, crear
  `agent-os-cli`, transicionar contenido, cambiar visibilidad o settings y
  cerrar la unidad de trabajo o el roadmap requieren, cada uno, aprobación
  PM exacta y separada.
- Este documento no guarda estado vivo. Readiness, inventarios de refs,
  resultados de CI o validación, SHAs, fechas y aprobaciones se leen vivos
  de sus fuentes de registro al momento de ejecutar cada paso.
- Los placeholders `<APPROVED_TAG_NAME>`, `<APPROVED_TAG_MESSAGE>`,
  `<APPROVED_MAIN_SHA>`, `<TAG_DATE>` y `<TRANSITION_DATE>` nunca se
  rellenan en este archivo y no constituyen autorización: sus valores
  exactos se fijan únicamente en la aprobación PM exacta correspondiente.

## Invariantes (ADR 0005)

- `codefusion-repo/project-os-v2` permanece privado e internal-only y, tras
  la transición, congelado como baseline interno de CodeFusion.
- `agent-os-cli` es la futura superficie pública y, tras la transición, la
  única fuente de verdad de Project OS y del CLI.
- La transición es única: sin sincronización bidireccional y sin backports.
- Se permite conceptualmente **exactamente un** tag interno anotado de
  handoff en este repositorio; no es público, no es un GitHub Release y no
  versiona Project OS para ninguna audiencia externa.
- Un tag pusheado no se mueve, reutiliza ni elimina; un error se corrige con
  un tag **nuevo** bajo una nueva aprobación PM exacta, y cualquier
  eliminación requiere su propia aprobación PM exacta y comunicación
  separada.
- El tag no autoriza ninguna acción posterior.

## Gates de aprobación PM exacta y separada

Cada uno de estos pasos requiere su propia aprobación PM exacta que nombre
proyecto, unidad de trabajo y acción; ninguno queda implícito en otro:

1. Merge del PR que integra la enmienda y este procedimiento.
2. Creación y push del tag, aprobando el trío exacto
   `<APPROVED_TAG_NAME>` + `<APPROVED_TAG_MESSAGE>` + `<APPROVED_MAIN_SHA>`.
3. Cierre de la unidad de trabajo y del roadmap.
4. Creación de `agent-os-cli`, transición de contenido, cambios de
   visibilidad o settings y cualquier publicación.

## Requisitos del tag

- El tag debe ser **anotado** (`git tag -a`), nunca ligero, para que
  mensaje, tagger y fecha queden registrados en el objeto tag.
- `<APPROVED_TAG_NAME>` no debe colisionar con ningún tag, rama ni ref
  existente (verificado vivo en el momento de aprobar), no debe parecer un
  release público ni pertenecer a una serie previa de tags del repositorio,
  y no debe seguir un esquema semver de producto.
- `<APPROVED_TAG_MESSAGE>` debe declarar inequívocamente que el tag es un
  marcador interno de handoff, que no es un release público ni un GitHub
  Release y que no autoriza publicación, cambio de visibilidad, creación de
  `agent-os-cli`, transición de contenido ni implementación del CLI.
- `<APPROVED_MAIN_SHA>` debe pertenecer a `main`, coincidir con el estado
  validado y fijarse únicamente según el procedimiento siguiente; nunca se
  fija por anticipado ni se guarda en este archivo.

## Procedimiento pre-tag

1. Completar review-before-close (MOS-3.7) sobre el PR que integra la
   enmienda y este procedimiento.
2. El PM mergea ese PR con su aprobación exacta y separada de merge.
3. Confirmar, en vivo, GitHub Actions verdes sobre el head final de `main`.
4. Inventariar en vivo tags, ramas, refs y GitHub Releases existentes y
   verificar que el nombre propuesto cumple los requisitos anteriores y no
   colisiona.
5. Fijar `<APPROVED_MAIN_SHA>` con `git rev-parse main` actualizado; debe
   ser el merge commit del PR anterior y coincidir con el estado validado.
6. Solicitar la aprobación PM exacta y separada del trío nombre + mensaje +
   SHA antes de ejecutar el command bundle.

## Paquete de handoff (template)

Los valores se fijan en la aprobación PM exacta y en el registro vivo de la
ejecución, nunca en este archivo.

| Campo | Valor |
| --- | --- |
| Repositorio de origen | `codefusion-repo/project-os-v2` (privado, internal-only) |
| Tag | `<APPROVED_TAG_NAME>` (anotado, interno) |
| SHA | `<APPROVED_MAIN_SHA>` — se fija después del merge, nunca antes |
| Fecha del tag | `<TAG_DATE>` — la fecha en que el PM ejecute el bundle aprobado |
| Fecha de transición | `<TRANSITION_DATE>` — se fija cuando la transición hacia `agent-os-cli` sea aprobada por separado |
| Nueva fuente de verdad | `agent-os-cli`, tras la transición única |

- Contenido transferible (ADR 0005 §2): la base funcional de Project OS —
  kernel ES/EN, operaciones, templates, adapters, tooling y documentación —
  junto con la base git y de contenido auditada.
- Contenido no transferible: issues, pull requests, comentarios, reviews y
  cualquier conversación histórica de GitHub de este repositorio.
- Riesgos aceptados: los registrados por decisión PM en
  [ADR 0005](../decisions/0005-public-repository-strategy.md) y en la
  [revisión Stage 0](../security/PUBLIC_READINESS_REVIEW.md)
  (F-04, F-05, F-06).
- El tag y este paquete **no** son autorización para ejecutar la
  transición; solo registran procedencia y límites.

## PM command bundle (copy-safe)

Ejecutar solo después de la aprobación PM exacta y separada del trío nombre
+ mensaje + SHA. Reemplazar cada placeholder por el valor exacto aprobado;
`<APPROVED_TAG_MESSAGE>` es el texto aprobado completo (puede repartirse en
varios `-m` conservando el contenido exacto). El bundle no crea GitHub
Releases ni cambia visibilidad o settings.

```sh
git fetch origin --prune
git checkout main
git pull --ff-only
git rev-parse main
# Debe imprimir exactamente <APPROVED_MAIN_SHA>; si no coincide, detenerse.

git tag -a <APPROVED_TAG_NAME> <APPROVED_MAIN_SHA> \
  -m "<APPROVED_TAG_MESSAGE>"

git push origin refs/tags/<APPROVED_TAG_NAME>
```

## Verificación post-tag (read-only)

Después de pushear el tag, verificar sin mutar nada:

```sh
git fetch origin --prune
git cat-file -t <APPROVED_TAG_NAME>
# Debe imprimir: tag  (objeto anotado, no lightweight)

git cat-file -p <APPROVED_TAG_NAME>
# Revisar: object = <APPROVED_MAIN_SHA>, tagger y mensaje aprobado completo.

git ls-remote --tags origin <APPROVED_TAG_NAME>
# El tag debe existir en el remoto y apuntar al objeto tag esperado.

git branch --contains <APPROVED_MAIN_SHA> --format='%(refname:short)'
# Debe incluir: main

gh release list --repo codefusion-repo/project-os-v2
# No debe listar <APPROVED_TAG_NAME> ni ningún release nuevo.

gh repo view codefusion-repo/project-os-v2 --json visibility --jq .visibility
# Debe imprimir: PRIVATE
```

## Cierre y transición

- El cierre de la unidad de trabajo que produjo este procedimiento y el
  cierre del roadmap son decisiones PM posteriores y separadas, informadas
  por la evidencia viva leída en ese momento (merge integrado, CI verde
  sobre el head final, tag creado y verificado).
- La creación de `agent-os-cli`, la transición de contenido y cualquier
  publicación ocurren después de ese cierre, cada una con su propia
  aprobación PM exacta, según ADR 0005 y los gates preservados de
  [ADR 0004](../decisions/0004-public-presentation-and-packaging.md).
