# Reglas: verdad, permisos y seguridad

**Estas son las reglas que nunca se negocian. Si una operación y una regla
chocan, gana la regla y el sistema se detiene (fail-closed).**

## Fuentes de verdad

Cada tipo de información tiene exactamente un dueño:

- **Estado vivo → GitHub.** Issues, PRs, comentarios, reviews, ramas, commits
  y evidencia de validación se reconstruyen desde GitHub y git al momento de
  la tarea. La memoria del chat, los reportes previos y los archivos durables
  no son evidencia: son claims hasta verificarlos.
- **Comportamiento estable → kernel español.** `project-os-es/kernel/*.json`
  define actores, modos, workflows, límites, evidencia, salidas y estados para
  esta superficie, y se resuelve vía `project-os-es/kernel/manifest.json` antes
  de trabajo no trivial.
- **Verdad del producto → repo target.** Dominio, runtime, build y validación
  del target viven en el target, nunca en el kernel.
- **Decisiones que sobreviven a un issue → ADRs** en `docs/decisions/` del
  repo dueño de la decisión. **Qué sigue y por qué → un único roadmap issue
  canónico** por proyecto, que se supersede, no se muta.

Dos prohibiciones protegen esto: **nada de estado vivo en archivos durables**
(ni números de issue/PR como estado, ni SHAs, ni readiness) y **nada de estado
inventado** (lo que no se puede leer en vivo, falta; se reporta como faltante).

## Permisos: el texto nunca autoriza

Ningún doc, template, prompt, adapter ni salida de resolver otorga permiso
(`boundary.output_not_permission`). La escritura del terminal agent exige
estas cinco condiciones, todas a la vez:

1. aprobación PM exacta que nombra repo, issue/PR y acción aprobada;
2. el modo de ejecución correcto resuelto del kernel;
3. branch preflight real (rama, worktree y HEAD capturados antes de editar);
4. trabajo en rama `work/<issue>-<slug>`, nunca directo a main;
5. validación proporcional con resultados reales.

Merge, cierre, labels, tags, releases, settings y producción quedan con el
Humano PM salvo aprobación separada y exacta. Ante kernel faltante, evidencia
mínima o material faltante, autoridad ambigua o validación fallida: detenerse y devolver
`status.needs_context`, `status.needs_pm_decision` o `status.blocked`.

Los skills opcionales tampoco autorizan. Solo describen una capacidad o metodo
que el agente puede aplicar si el PM lo pide o un route prompt lo recomienda;
no cambian workflow, mode, scope, preflight, validacion ni review-before-close.

## Trazabilidad: todo se puede reconstruir en frío

Cualquier agente debe poder retomar el proyecto solo desde GitHub:

- Cada **issue** carga su propio contexto: por qué existe, objetivo, base
  fuente, scope, fuera de scope, criterios de aceptación y validación.
- Cada **PR** documenta su propia verificación: resumen, límites, comandos de
  validación con resultados y notas de seguridad.
- Cada **cierre** deja un paquete de reconstrucción: evidencia de completitud
  y validación, límites preservados y referencias de commit/PR.
- Las ramas `work/<issue>-<slug>` atan el código a su issue.

## Validación proporcional

La validación es evidencia para el riesgo del cambio, no un ritual. Clasifica
siempre en una de cuatro categorías: **agent-run requerida** (obligatoria si
el cambio toca kernel, resolver, comandos, autorización, trazabilidad,
seguridad, secretos, deploy o contratos deterministas), **comandos PM-run
drafteados**, **validación manual PM** (claridad de docs, wording, UX) o
**sin validación automatizada, con justificación**. Nunca se asume full suite
ni tests nuevos por defecto; esta superficie usa este resumen y
`project-os-es/kernel/reglas-operativas.json` como ruta operativa.

## Economía de contexto

El costo en tokens y subagentes se mantiene proporcional a la tarea, pero la
economía está subordinada a la seguridad: ningún atajo elimina un gate. Lee el
estado vivo en vez de pegarlo; cita ubicaciones (`issue #`, `archivo:línea`)
en vez de repetir cuerpos completos; usa subagentes solo con razón acotada y
verifica su salida contra evidencia viva. El detalle operativo de esta
superficie vive en `project-os-es/kernel/reglas-operativas.json`.

La superficie normal de lectura parte en el manifest y se limita a la
resolución seleccionada, límites y evidencia, output y artefacto aplicables,
template exacto, skills solicitadas, evidencia viva mínima y fuentes del target
requeridas por scope, validación o source basis. Tooling interno, metadata
proyectada, contexto real del modelo y aperturas posteriores son categorías
distintas. Cada ejecución las conserva internamente mediante
`context_receipt.minimum_read_surface`, usando paths relativos al repositorio o
identificadores vivos y razones, nunca paths absolutos de máquina ni cuerpos
completos. `context_plan` y el recibo interno permanecen íntegros en todos los
niveles; `pm_facing_visibility` omite solo la representación Markdown del recibo
en `minimal` y `compact`, y la muestra completa en el envelope de `full/debug`.
Lecturas fuera de la superficie normal requieren `full/debug`, auditoría,
debugging, revisión de seguridad/autorización, arquitectura compleja o una
decisión PM concreta; ninguna razón sustituye evidencia ni gates.

## Secretos

Prohibido imprimir, pegar, commitear, citar o resumir secretos: `.env`,
tokens, credenciales, cookies, JWTs, URLs de base de datos, claves privadas,
llaves de pago o cualquier valor con pinta de secreto — incluso en tests,
logs, PRs y reportes. Se redacta como `[REDACTED]` reportando solo nombre de
variable, ruta y tipo de riesgo. Nada de dumps amplios de entorno (`env`,
`printenv`, `set`) sin diagnóstico redactado y acotado por el PM.

## Materialidad de evidencia y degradación segura

El contrato activo distingue evidencia `material` y `auxiliary`. Cada
workflow declara `required_evidence`, el conjunto que debe intentar obtener y
reportar, y `minimum_evidence`, el subconjunto material mínimo para su acción.
Cada output declara `action_class` y si admite gaps no materiales.

- **Hard gates no degradables.** Aprobación PM exacta, branch preflight,
  validación requerida, identidad del target, SHA/ref exacta, secret safety,
  privacidad, conflictos reales y cualquier evidencia material permanecen
  fail-closed. Un output mutable nunca admite gaps.
- **Representación única.** Solo un output `action.read_only` o
  `action.draft_only` que declare `allows_non_material_gaps: true` puede
  reutilizar `status.resolved`. Debe exponer `verified_evidence`,
  `unavailable_evidence`, `materiality`, `decision_impact`,
  `equivalent_source_used` y `revalidation_required_before_write`. Con gaps no
  puede reclamar completitud.
- **Fuentes equivalentes.** Una alternativa satisface evidencia solo si el
  contrato la declara, se verifica contra sus criterios y se registra la
  sustitución. CI solo es equivalente cuando cubre la misma SHA/ref exacta y
  el mismo alcance de validación; nunca se presume equivalente al merge real.
- **Indisponibilidad no es estado.** Errores de conector, API o red —incluidos
  404, 422 y 502— significan fuente no disponible; no demuestran ausencia,
  cierre, merge, fallo ni inexistencia del target.
- **Truncación material.** Una respuesta truncada bloquea cuando lo no
  recuperado puede cambiar autoridad, scope o la decisión. Si ese impacto no
  se puede clasificar, falla cerrado.
- **Revalidación antes de writes.** Todo gap, incluso auxiliar, debe
  revalidarse completamente antes de editar, commitear, hacer push, abrir PR,
  mergear, cerrar, etiquetar, desplegar o ejecutar cualquier otra mutación.

## Siguiente paso

Con las reglas claras, opera el ciclo día a día con [ritmo.md](ritmo.md).
