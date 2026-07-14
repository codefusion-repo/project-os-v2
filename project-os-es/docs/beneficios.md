# Beneficios, arquitectura y escenarios

**Qué aporta Project OS, cómo está construido por dentro y qué situaciones
concretas resuelve, con cada afirmación anclada a una fuente verificable del
árbol: una clave del kernel, un documento, una operación, un template o un
test.** Este documento no compara contra herramientas externas, no promete
ahorros universales y no otorga permisos
(`boundary.output_not_permission`): cada beneficio se enuncia como propiedad
del propio sistema y se comprueba leyendo la fuente citada o ejecutando el
comando indicado.

Versión inglesa: [benefits.md](../../project-os-en/docs/benefits.md). El
apéndice técnico con los tamaños medidos por nivel de hidratación es
[benchmark-contexto.md](benchmark-contexto.md).

Las claves `rule.*`, `boundary.*`, `evidence.*` y `output.*` citadas abajo
viven en [`../kernel/`](../kernel/manifest.json) y se ven resueltas
ejecutando el resolver (ver [empezar.md](empezar.md)). Los tests citados
corren con `python3 -m pytest tests/ -q`.

## Beneficios verificables

1. **Autoridad humana por acción.** Ningún texto del sistema autoriza nada:
   escribir exige aprobación PM exacta que nombra proyecto, unidad de trabajo
   y acción, y merge, cierre, labels, tags, releases, settings y secretos
   exigen cada uno una aprobación separada. Fuente: `rule.no_autorizacion`,
   `boundary.separate_pm_approval` y `evidence.pm_approval`; el detalle PM
   está en [reglas.md](reglas.md).
2. **GitHub como estado vivo.** Issues, PRs, ramas, commits, reviews y
   validación se leen en vivo al momento de la tarea; los archivos durables
   nunca guardan ese estado, así que no envejecen ni contradicen la realidad.
   Fuente: `rule.estado_vivo_no_durable`, `rule.trazabilidad_viva` y
   `boundary.no_live_state_durable`.
3. **Continuidad cold-resume.** Cualquier sesión nueva reconstruye el
   proyecto resolviendo el kernel y leyendo GitHub: nada depende de la
   memoria de un chat anterior. Fuente: la `resolution_sequence` del
   [manifest](../kernel/manifest.json) más `rule.trazabilidad_viva`; el
   traspaso guiado existe como
   [MOS-0.6](../operaciones/fase-0/MOS-0.6-transferir-contexto-de-sesion.md).
4. **Cambio de agente o proveedor sin pérdida.** El contrato es el mismo para
   cualquier agente que resuelva el kernel: cambiar de herramienta es cambiar
   de adapter, no de proceso. Fuente: los adapters
   [`AGENTS.target.md`, `CLAUDE.target.md`, `GEMINI.target.md` y
   `BROWSER_CHAT.target.md`](../adapters/README.md) bootean superficies
   distintas hacia el mismo kernel; la equivalencia ES/EN la guarda
   `tests/test_project_os_bilingual_parity.py`.
5. **Alineación con roadmap, issues y ADRs.** Cada unidad de trabajo nace de
   la trazabilidad existente — del roadmap canónico o de un issue — y las
   decisiones durables quedan como ADRs. Fuente:
   [MOS-3.1](../operaciones/fase-3/MOS-3.1-draftear-siguiente-issue-desde-trazabilidad.md),
   [MOS-3.8](../operaciones/fase-3/MOS-3.8-draftear-issue-desde-descripcion.md),
   [MOS-R.1](../operaciones/fase-2/MOS-R.1-registrar-decision-adr.md) y los
   ADRs de este repo en
   [`docs/decisions/`](../../docs/decisions/0004-public-presentation-and-packaging.md).
6. **Trazabilidad de punta a punta.** El trabajo se rastrea desde el issue
   hasta el merge con ramas scoped `work/<unidad>-<slug>` y evidencia viva; la
   trazabilidad además se puede auditar como operación. Fuente:
   `rule.trazabilidad_viva`, `rule.preflight` y
   [MOS-3.13](../operaciones/fase-3/MOS-3.13-auditar-trazabilidad.md).
7. **Fail-closed por diseño.** Ante kernel faltante, autoridad ambigua,
   evidencia faltante o validación fallida, el agente se detiene con un
   estado no resuelto en lugar de adivinar y seguir. Fuente:
   `rule.resolucion_fail_closed`, `boundary.fail_closed` y los estados
   `status.blocked` / `status.needs_pm_decision` / `status.needs_context`;
   el resolver mismo falla cerrado ante valores desconocidos
   (`tests/test_project_os_bilingual_parity.py::test_unknown_skill_and_unallowed_kernel_paths_fail_closed`).
8. **Seguridad y secret safety.** Prohibido pedir, imprimir, commitear o
   registrar secretos y datos sensibles; los valores se redactan como
   `[REDACTED]` y solo se reportan rutas, nombres de variables y tipo de
   riesgo. Fuente: `rule.secret_safety` y `boundary.security_privacy`; el
   reporte responsable vive en [SECURITY.md](../../SECURITY.md).
9. **Validación proporcional al riesgo.** La validación crece con el riesgo
   del cambio (kernel, seguridad, deployment exigen validación agent-run;
   claridad y producto quedan como validación manual PM) y nada se declara
   done sin reportarla. Fuente: `rule.validacion_proporcional`,
   `boundary.validation_discipline` y `evidence.validation_output`.
10. **Review-before-close.** Cerrar exige comparar la unidad de trabajo
    contra el diff, los archivos finales, la validación y los riesgos; el
    body de un PR es un claim, no prueba. Fuente:
    `boundary.review_before_close` y
    [MOS-3.7](../operaciones/fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md).
11. **QA humano desde el browser.** Una persona sin terminal draftea y
    procesa checklists de QA desde browser chat, con superficie read-only y
    draft-only. Fuente:
    [MOS-4.1](../operaciones/fase-4/MOS-4.1-draftear-checklist-qa-de-issue-pr.md),
    [MOS-4.4](../operaciones/fase-4/MOS-4.4-procesar-checklist-qa-de-issue-pr.md),
    [MOS-4.5](../operaciones/fase-4/MOS-4.5-procesar-checklist-qa-de-feature.md)
    y el adapter [BROWSER_CHAT.target.md](../adapters/BROWSER_CHAT.target.md).
12. **Summaries estándar.** Los reportes de ejecución, estados y PRs siguen
    templates fijos, así que el PM lee siempre la misma forma: qué cambió,
    qué se validó, qué falta y qué riesgo queda. Fuente:
    `output.execution_report` y `output.status_result` con sus templates
    [reporte-ejecucion.md](../templates/reporte-ejecucion.md),
    [resultado-estado.md](../templates/resultado-estado.md) y
    [pull-request.md](../templates/pull-request.md).
13. **Gobernanza reusable entre proyectos.** El kernel es agnóstico al
    proyecto: el mismo contrato se adopta por copia en otro repositorio sin
    reescribirlo, y lo específico del repo queda en su bootloader. Fuente: el
    objetivo del [manifest](../kernel/manifest.json), la adopción copy-based
    de [empezar.md](empezar.md) y
    [MOS-0.3](../operaciones/fase-0/MOS-0.3-adoptar-proyecto-existente.md).

## Arquitectura modular

Cada pieza tiene una responsabilidad y se puede leer por separado:

- **Kernel por tupla + resolver determinista.** Un set pequeño de JSON define
  actores, modos, workflows, reglas, límites, evidencia, outputs y estados;
  el resolver hidrata solo la tupla `(actor, workflow, mode)` pedida, en
  niveles `minimal` / `compact` / `full/debug`, sin conceder permisos. Los
  niveles nunca pierden límites ni secret safety
  (`tests/test_project_os_hydration_levels.py`); los tamaños medidos están en
  el apéndice [benchmark-contexto.md](benchmark-contexto.md).
- **Shims jerárquicos.** Los shims por herramienta (`CLAUDE.md`, `GEMINI.md`)
  son mínimos y delegan en un único bootloader terminal (`AGENTS.md`), que a
  su vez apunta al kernel: una sola cadena de arranque, sin duplicar
  contrato. Fuente: [CLAUDE.target.md](../adapters/CLAUDE.target.md) y
  [AGENTS.target.md](../adapters/AGENTS.target.md).
- **Adapters target-specific delgados.** El adapter de un target lleva solo
  identidad y configuración de máquina/adopción (paths, rama default, idioma
  PM) y punteros a la evidencia viva; nunca estado vivo ni copias del
  contrato. Fuente: [adapters/README.md](../adapters/README.md) y
  `tests/test_adapter_contract.py`.
- **Operaciones, templates y skills bajo demanda.** El catálogo MOSDLC, los
  templates de artefactos y los skills opcionales se cargan solo cuando se
  usan; el resolver los entrega como referencias resolubles, no inlineados.
  Fuente: [operaciones/README.md](../operaciones/README.md),
  [templates/README.md](../templates/README.md) y
  [`../kernel/skills.json`](../kernel/skills.json).
- **Lifecycle MOSDLC.** Las operaciones cubren el ciclo completo por fase —
  adopción, requisitos, diseño, implementación, validación, release y
  operación — más operaciones cross-fase; el ritmo día a día está en
  [ritmo.md](ritmo.md).
- **Tres planos separados.** El **contrato** (kernel JSON versionado y
  testeado), la **configuración del target** (bootloader/adapters por repo) y
  el **estado de tarea** (GitHub, leído en vivo) nunca se mezclan: por eso el
  contrato es portable, el adapter es pequeño y el estado nunca envejece en
  un archivo. Fuente: `rule.fuente_canonica`, `rule.estado_vivo_no_durable` y
  [adapters/README.md](../adapters/README.md).

## Escenarios verificables

Cada escenario nombra la situación, lo que el sistema hace y cómo
comprobarlo en tu propio proyecto.

1. **Se perdió el chat.** La sesión anterior se cerró, expiró o se corrompió.
   Una sesión nueva re-resuelve el kernel y reconstruye el estado desde
   GitHub; si quedaba contexto útil, se transfiere con
   [MOS-0.6](../operaciones/fase-0/MOS-0.6-transferir-contexto-de-sesion.md).
   Comprobación: abre una sesión limpia y pide reconstruir un issue en curso;
   nada del resultado depende del chat perdido.
2. **Handoff a otra persona o sesión.** El trabajo queda documentado en el
   issue/PR con summaries estándar y el paquete de handoff tiene template
   ([paquete-handoff.md](../templates/paquete-handoff.md)); quien recibe
   repite el mismo arranque del escenario 1. Comprobación: la persona que
   recibe no necesita acceso a la conversación original.
3. **Cambio de agente o proveedor.** Se adopta el adapter de la nueva
   herramienta y esta resuelve el mismo kernel: mismas reglas, límites,
   evidencia y estados. Comprobación: resuelve la misma tupla con dos agentes
   distintos y compara el contrato hidratado; es el mismo JSON.
4. **Falta la aprobación PM.** Un agente con todo listo para escribir pero
   sin aprobación exacta debe detenerse: `evidence.pm_approval` es evidencia
   requerida con `missing_status: status.blocked`. Comprobación: pide una
   implementación sin conceder la aprobación; el output correcto es un
   estado bloqueado que nombra el gate, no un commit.
5. **Apareció un hallazgo fuera de scope.** El agente no lo corrige
   silenciosamente: `boundary.implementation_discipline` limita el cambio al
   scope vivo, y la corrección se routea trazable con
   [MOS-3.5](../operaciones/fase-3/MOS-3.5-draftear-route-prompt-de-correccion.md)
   o como follow-up con
   [MOS-3.3](../operaciones/fase-3/MOS-3.3-draftear-follow-up-issue.md).
   Comprobación: el diff del PR no contiene archivos ajenos al scope del
   issue.
6. **QA humano antes de cerrar.** El PM draftea el checklist de QA desde
   browser ([MOS-4.1](../operaciones/fase-4/MOS-4.1-draftear-checklist-qa-de-issue-pr.md)),
   lo ejecuta una persona, se procesa el resultado
   ([MOS-4.4](../operaciones/fase-4/MOS-4.4-procesar-checklist-qa-de-issue-pr.md))
   y las correcciones nacen de
   [MOS-4.8](../operaciones/fase-4/MOS-4.8-draftear-correccion-desde-qa.md);
   el PR además pasa review-before-close
   ([MOS-3.7](../operaciones/fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md))
   antes del merge. Comprobación: el issue/PR conserva el checklist y su
   resultado como evidencia viva.

## Capacidades actuales y CLI futuro

Todo lo descrito arriba existe hoy en este árbol y se opera así:

- **Adopción copy-based:** copiar los adapters del target
  ([empezar.md](empezar.md)); no hay installer ni package.
- **Terminal:** resolver Python repo-local
  (`tools/project_os_resolve.py`).
- **Browser chat:** resolución manual desde el
  [manifest](../kernel/manifest.json), siempre read-only/draft-only.

Un CLI de onboarding es trabajo futuro **diferido por decisión durable**
(ADR 0003,
[0003-project-os-cli-adoption-model.md](../../docs/decisions/0003-project-os-cli-adoption-model.md),
reafirmado por ADR 0004): solo se reconsidera con evidencia de adopción real,
como su propio issue de diseño. Este documento no lo presenta como capacidad
actual, y ninguna parte del sistema lo requiere para operar.
