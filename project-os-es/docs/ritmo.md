# Ritmo: el ciclo de trabajo día a día

**Este es el pulso de Project OS: clasificar el trabajo por riesgo, usar solo
el proceso que ese riesgo justifica e implementar la solución completa que
mejor satisface el outcome. El ciclo central de abajo es la ruta del cambio
estándar, no un peaje universal.**

## Proporcionalidad: cuatro niveles de trabajo

Antes de elegir operación, clasifica el trabajo; la clase gobierna unidad,
PR, review, validación y densidad del reporte:

- **Nivel 0 — Lectura o análisis.** Respuesta directa con evidencia
  suficiente. Sin issue, sin roadmap, sin branch, sin tests, sin artefacto
  durable.
- **Nivel 1 — Cambio pequeño y reversible.** Una instrucción PM exacta y
  verificable puede ser la unidad viva cuando el target lo permite. Preflight,
  rama scoped, solución completa que mejor satisface el outcome, validación
  mínima suficiente y reporte `minimal`. No requiere por defecto issue,
  roadmap, ADR, tests nuevos ni tooling nuevo.
- **Nivel 2 — Cambio estándar.** El ciclo central de abajo: unidad viva,
  route prompt, implementación con validación, draft PR, review y closeout.
- **Nivel 3 — Cambio crítico o difícil de revertir.** Kernel, autorización,
  seguridad, migraciones, deployment, releases, contratos públicos:
  unidad formal, PR, review independiente, rollback y validación amplia.

Issues, PRs, branches y GitHub son adapters disponibles, no requisitos
universales del modelo: otro tracker o registro del target puede representar
la unidad viva.

La [continuidad de unidad](../operaciones/README.md#continuidad-de-la-unidad-primaria)
se conserva durante planificación, implementación, review, QA, corrección,
handoff y closeout. QA requerido precede al GO: MOS-4.1 → MOS-4.4 reutiliza
MOS-3.5 para corrección del mismo PR y MOS-3.3 para follow-ups materiales e
independientes, agrupados por outcome. MOS-4.8/MOS-4.7 mantienen entradas QA
compatibles que consumen esos contratos en la misma respuesta. En roadmaps
secuenciales, MOS-3.1 verifica completitud del predecessor antes de draftear una
única unidad siguiente; otra fase o una aprobación separada no crean unidades.

## El ciclo central

1. **Elige el siguiente outcome.** Desde el roadmap canónico y la
   trazabilidad viva ([MOS-3.1](../operaciones/fase-3/MOS-3.1-draftear-siguiente-issue-desde-trazabilidad.md))
   o desde una descripción tuya
   ([MOS-3.8](../operaciones/fase-3/MOS-3.8-draftear-issue-desde-descripcion.md)).
   Una unidad viva por outcome, con scope y criterios propios; para cambios
   estándar y críticos suele ser un issue, para cambios pequeños basta la
   instrucción PM exacta.
2. **Rutea la implementación.** Browser chat draftea el route prompt
   ([MOS-3.4](../operaciones/fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md));
   tú lo revisas y lo entregas al terminal agent con
   `PM_AUTHORIZATION_STATUS` explícito. Sin terminal agent disponible, usa el
   plan manual ([MOS-3.30](../operaciones/fase-3/MOS-3.30-draftear-plan-de-implementacion-manual.md)).
3. **El agente implementa y abre un PR en draft**, con validación proporcional
   y execution report.
4. **Revisa antes de cerrar.**
   [MOS-3.7](../operaciones/fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md)
   compara el PR contra la unidad viva con evidencia; el execution report es un
   claim, no prueba. Cada hallazgo recibe una disposición: solo
   `blocking-correction` vuelve por
   [MOS-3.5](../operaciones/fase-3/MOS-3.5-draftear-route-prompt-de-correccion.md);
   los `non-blocking-follow-up` se difieren
   ([MOS-3.3](../operaciones/fase-3/MOS-3.3-draftear-follow-up-issue.md)) y
   `preference`, `accepted-risk` e `invalid-finding` no fuerzan cambios. Cada
   corrección del PR se registra como un correction report append-only (review
   fuente, head anterior, head corregido, findings y validación), sin editar el
   body ni comentarios previos, y vuelve a MOS-3.7 sobre el head corregido.
5. **Cierra tú.** Con GO, MOS-3.7 entrega en la misma respuesta el bundle de
   closeout y su verificación final; tú lo ejecutas. Si el bundle se pierde,
   queda obsoleto o el cierre falla, vuelve a ejecutar MOS-3.7 sobre la
   evidencia vigente; una verificación posterior independiente de postcondiciones
   (merge, SHA final, cierre, limpieza) usa
   [MOS-3.27](../operaciones/fase-3/MOS-3.27-revisar-estado-del-proyecto.md).
   El cierre deja evidencia de reconstrucción en la unidad viva.

## Las fases, de un vistazo

El catálogo completo, con un prompt compacto por operación, está en
[`project-os-es/operaciones/README.md`](../operaciones/README.md):

- **Fase 0 — Adaptación:** activar sesiones, adoptar/verificar targets,
  transferir contexto.
- **Fase 1 — Requerimientos:** entrevistar, resumir, validar viabilidad,
  planificar roadmap.
- **Fase 2 — Diseño:** arquitectura, UI/UX, datos, estándares, seguridad,
  ADRs.
- **Fase 3 — Implementación:** el ciclo central de arriba, más releases,
  tags, assets y auditorías.
- **Fase 4 — QA humano:** checklists de QA y production readiness, y su
  procesamiento.
- **Fase 5 — Despliegue:** readiness, checklists y comandos por entorno.
  Local y staging pueden ejecutarse por agente con aprobación exacta
  (internal-only); **producción queda con el Humano PM por defecto**.
- **Fase 6 — Mantenimiento:** análisis read-only de seguridad, rendimiento,
  producto y calidad, procesados en draft-only.

¿No sabes qué sigue? Pide una recomendación con
[MOS-R.2](../operaciones/cross-fase/MOS-R.2-recomendar-siguiente-operacion.md)
o revisa readiness de fase con
[MOS-R.4](../operaciones/cross-fase/MOS-R.4-revisar-readiness-de-fase.md).
Cuando una operación devuelve `status.needs_pm_decision`, procésala con
[MOS-R.3](../operaciones/cross-fase/MOS-R.3-procesar-decision-pm-pendiente.md).

## Rutas frecuentes

El ciclo central es la ruta más común, no la única. Estas son las rutas
típicas, solo como navegación (cada operación conserva sus propios gates;
el prompt de cada una vive en el catálogo):

- **Nuevo proyecto desde cero:** MOS-0.2 browser-first (adapter browser
  primero y ruta terminal acotada por target, sin roadmap ni issue previos) →
  requerimientos (fase 1) → roadmap → ciclo central.
- **Repo target existente:** adopción browser-first (MOS-0.3 → MOS-0.5, con
  readiness browser y terminal por separado) → primer issue (MOS-3.1) → ciclo
  central.
- **Unidad lista con terminal agent:** route prompt (MOS-3.4) →
  implementación delegada → PR en draft → review (MOS-3.7) → closeout con el
  GO en la misma respuesta.
- **Sin terminal agent:** plan de implementación manual (MOS-3.30) →
  ejecución PM/humana → procesar resultado (MOS-3.31) → review normal.
- **QA humano:** checklist (MOS-4.1) → tú lo ejecutas → procesar resultado
  (MOS-4.4) → corrección (MOS-3.5) o follow-up (MOS-3.3), en la misma unidad
  mientras el outcome sea el mismo.
- **Seguridad / auditoría read-only:** solicitar revisión (MOS-3.23) →
  procesar hallazgos (MOS-3.25) → follow-ups (MOS-3.3) o correcciones
  (MOS-3.5).
- **Release / deploy readiness:** análisis (MOS-3.10 o MOS-R.11) → comandos
  drafteados y PM-gated (MOS-3.11, MOS-3.12 o fase 5 por entorno).
- **Sesión agotada:** transferir contexto (MOS-0.6) → sesión nueva
  reconstruida solo desde el estado de GitHub.

## Variables PM

Las variables son selectores de contexto, **no fronteras de autorización**.
Se escriben como `<NOMBRE>` en placeholders y `NOMBRE=VALOR` al invocar; las
explícitas del PM tienen prioridad sobre lo inferido de GitHub, y si falta una
requerida o conflictúa con la realidad, la operación falla cerrada.

- `PM_FEEDBACK_HUMANO` — tu contexto o criterio adicional. Opcional; nunca
  reemplaza evidencia viva.
- `PM_QUESTION_HUMANO` — tu pregunta de interpretación, ruteo o priorización.
  Opcional; nunca autoriza nada. (`PM_QUESTION` no existe.)
- `PM_AUTHORIZATION_STATUS` — la única variable de autorización. Solo dos
  valores autorizan estado: `pending` y
  `granted for this exact scope and mode`.

Las variables jamás portan secretos; todo valor sensible se redacta como
`[REDACTED]`.

## Siguiente paso

Abre el [catálogo de operaciones](../operaciones/README.md), ubica tu fase y
copia el prompt de la operación que toca. Si estás arrancando de cero,
vuelve a [empezar.md](empezar.md).
