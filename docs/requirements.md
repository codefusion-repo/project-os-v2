# Requisitos de producto y metodología de Project OS

Esta es la especificación canónica de **qué debe lograr Project OS en su
siguiente etapa**: facilitar su uso, aprovechar prudentemente nuevas
capacidades de IA, acelerar el recorrido desde prototipo hasta producción y
completar outcomes end-to-end con menos fragmentación en issues. La validación
y la autoridad humana forman parte del resultado exigido.

Su alcance es producto y metodología. El kernel conserva el comportamiento
operativo; los ADRs conservan las decisiones durables; GitHub y git conservan
el estado vivo. Este documento no modifica contratos, concede permisos ni
registra avance, aprobaciones, mediciones o planificación. Los requisitos son
resultados exigidos a la evolución posterior, no afirmaciones de que ya estén
implementados ni un roadmap de soluciones.

## Fuentes y criterio de lectura

- [README](../README.md): identidad, públicos, fuentes de verdad y superficies
  de Project OS.
- [Beneficios](../project-os-es/docs/beneficios.md) y
  [ritmo de trabajo](../project-os-es/docs/ritmo.md): capacidades verificables,
  continuidad, proporcionalidad y ciclo humano-dirigido.
- [Kernel](../project-os-es/kernel/manifest.json),
  [reglas](../project-os-es/docs/reglas.md) y
  [catálogo MOSDLC](../project-os-es/operaciones/README.md): comportamiento,
  límites y operaciones aplicables.
- [Dirección estratégica](https://github.com/codefusion-repo/project-os-v2/issues/274):
  calidad del kernel y las operaciones, lifecycle completo y herramientas
  subordinadas al valor de uso real.
- [Simplificación operativa](https://github.com/codefusion-repo/project-os-v2/issues/474)
  y su [decisión de cierre](https://github.com/codefusion-repo/project-os-v2/issues/474#issuecomment-5105952691):
  economía de contexto y complejidad, y derecho a abandonar una línea cuando
  su costo supera el valor. Sus fases y propuestas no se convierten en
  pendientes de esta especificación.
- [ADR 0003](decisions/0003-project-os-cli-adoption-model.md),
  [ADR 0004](decisions/0004-public-presentation-and-packaging.md) y
  [ADR 0005](decisions/0005-public-repository-strategy.md): diferimiento del
  CLI, posicionamiento, gates de publicación y separación interno/público.
- [Intención PM y alcance de origen](https://github.com/codefusion-repo/project-os-v2/issues/497):
  objetivos de experiencia, velocidad y menor fragmentación que esta
  especificación sintetiza.

Las referencias GitHub son fuentes que deben releerse al usar el documento,
no snapshots de su estado. Los roadmaps históricos explican intención y
restricciones; una propuesta en ellos no demuestra una capacidad actual. Los
ejemplos técnicos son orientativos salvo decisión PM expresamente vinculante.
Ante conflicto material, se aplica la resolución de decisiones y estados del
kernel; esta especificación nunca supersede una decisión por sí sola.

## Baseline de capacidades actuales

El baseline describe mecanismos y contratos verificables en las fuentes
citadas. Su existencia no demuestra todavía una reducción end-to-end del
tiempo, las decisiones o los issues; esa mejora debe evaluarse por separado.

| Capacidad actual | Source basis verificable | Límite de la afirmación |
| --- | --- | --- |
| Kernel compacto resoluble por actor, workflow y modo, con reglas, evidencia y estados | [Manifest](../project-os-es/kernel/manifest.json), [resolver](../tools/project_os_resolve.py) y [README](../README.md) | Resuelve forma operativa; no consulta por sí solo el estado del proyecto ni autoriza acciones. |
| Entrada por intención en browser chat y reconstrucción de metadata desde referencias vivas | [Adapter browser](../project-os-es/adapters/BROWSER_CHAT.target.md), [MOS-R.2](../project-os-es/operaciones/cross-fase/MOS-R.2-recomendar-siguiente-operacion.md) y [contrato de inputs](../project-os-es/operaciones/README.md) | Seleccionar la operación no la ejecuta ni infiere aprobación; los códigos MOS siguen disponibles. |
| Fast path terminal con una única entrada ejecutable y configuración local explícita | [Bootloader](../AGENTS.md) y [fast path](../tools/project_os_fast_path.py) | Acelera el arranque local; requiere referencias válidas y no constituye un instalador o runtime. |
| Operaciones por fase para planificación, implementación, QA, release, despliegue y mantenimiento | [Catálogo](../project-os-es/operaciones/README.md) y [ritmo](../project-os-es/docs/ritmo.md) | Es cobertura metodológica; no promete ejecución autónoma de todo el lifecycle. |
| Validación proporcional, corrección del PR y review-before-close | [Reglas](../project-os-es/docs/reglas.md), [ritmo](../project-os-es/docs/ritmo.md) y [límites](../project-os-es/kernel/limites.json) | Un reporte es un claim; el review necesita diff, archivos finales y resultados reales. |
| Continuidad en frío y cambio de agente apoyados en kernel y evidencia viva | [Beneficios](../project-os-es/docs/beneficios.md) y [reglas](../project-os-es/docs/reglas.md) | Depende de acceso verificable a las fuentes; no garantiza capacidades equivalentes de todas las herramientas ni un tiempo de resume. |
| Superficies española e inglesa y separación entre core, adapters y mantenimiento propio | [README](../README.md) y [reglas operativas](../project-os-es/kernel/reglas-operativas.json) | ES es default y EN explícito; paridad semántica no exige generar la prosa ni compartir toda su estructura. |

La evolución debe partir de estas capacidades y demostrar dónde queda fricción
real. No se presupone que haga falta reemplazar el kernel, añadir un actor o
reconstruir el catálogo para alcanzar los outcomes siguientes.

## Objetivos de producto

1. **Facilidad de uso.** El PM puede expresar intención, outcome y constraints
   para iniciar y continuar trabajo sin estudiar códigos MOS, workflows ni
   metadata reconstruible. Se reducen preguntas repetidas y pasos mecánicos;
   la siguiente acción segura es comprensible.
2. **Aprovechamiento prudente de IA.** Una capacidad nueva merece incorporarse
   cuando reduce fricción, tiempo o costo real con valor neto demostrado,
   conservando portabilidad, seguridad y autoridad. La novedad no es un
   criterio de adopción.
3. **Velocidad end-to-end.** Planificación, prototipado, implementación, QA,
   release y producción forman un recorrido explícito que reutiliza evidencia
   y decisiones verificables, y reduce esperas y trabajo repetido sin omitir
   gates humanos.
4. **Menor fragmentación.** Un outcome cohesivo puede completarse con una
   unidad primaria y las unidades independientes que materialmente requiera.
   Cambiar de fase o corregir el mismo PR no debe generar issues mecánicos.

Un **outcome** es un resultado observable con scope y criterios de aceptación
coherentes. Una **unidad primaria** reúne su trazabilidad de planificación,
implementación, revisión y closeout. No equivale a una autorización global ni
obliga a agrupar resultados independientes en un mega-issue. La forma de la
unidad y los gates siguen la clase de cambio y la política del target.

## Constraints durables

Estos límites preservan el contrato existente; su detalle operativo se
consulta en el kernel, las reglas y los ADRs citados.

- **Separación de fuentes.** En este repositorio, GitHub y git son la fuente
  de estado vivo; el kernel es la fuente de comportamiento estable. La
  configuración del target vive en sus adapters y entorno local; producto,
  dominio y validación específicos se reconstruyen desde el target. El core
  sigue agnóstico de proyectos y no convierte este adapter GitHub en un
  requisito universal de otros targets.
- **Autoridad humana exacta.** Scope, riesgo, aceptación y decisiones
  materiales siguen bajo control humano. Capacidad técnica, intención,
  routing, outputs y templates nunca equivalen a permiso. Merge, cierre,
  labels, tags, releases, settings, automatización y producción conservan sus
  aprobaciones exactas por acción. Una decisión puede enumerar acciones
  exactas, sin autorizar otras por inferencia ni saltar gates.
- **Límites de superficie.** Browser chat permanece read-only/draft-only
  incluso con herramientas conectadas. Las escrituras delegadas requieren
  actor y modo compatibles, autorización exacta y preflight de rama,
  worktree, HEAD y scope; se protege `main` y se trabaja en una rama scoped.
- **Fail-closed y secret safety.** Contexto o evidencia material ausentes,
  autoridad ambigua, conflictos sin resolver o validación requerida fallida
  impiden la acción afectada. No se inventa evidencia. Los gaps auxiliares
  solo siguen la degradación segura expresamente admitida por el kernel;
  nunca habilitan una mutación. No se exponen secretos, datos sensibles ni
  paths personales; solo referencias seguras y valores `[REDACTED]`.
- **Validación y revisión.** La velocidad no sustituye validación
  proporcional, QA humano, review-before-close, evidencia verificable ni
  rollback según el riesgo. Un cambio editorial no justifica tests de
  wording; los tests protegen comportamiento y contratos deterministas.
- **CLI y arquitectura diferidos.** ADR 0003 mantiene el CLI sin aceptación
  para implementación; ADR 0004 conserva su evaluación posterior basada en
  adopción y el posicionamiento de capa de proceso humano-dirigida. Reducir
  fricción no exige CLI, bridge, MCP, plugin system, runtime ni proveedor.
  Si una solución posterior necesita cambiar ese diferimiento, debe
  identificar la decisión a reconsiderar y obtener una decisión PM exacta;
  cumplir estos requisitos no la reemplaza.
- **Estrategia interna/pública.** Conforme a ADR 0005, este repositorio
  permanece privado e interno. `agent-os-cli` es la superficie futura separada
  definida por esa decisión, no una tecnología elegida por estos requisitos.
  Se conserva la transición única: después de ella, el nuevo repositorio es
  la única fuente de desarrollo futuro y el baseline interno queda congelado,
  sin sincronización bidireccional ni backports. No se trasladan las
  conversaciones históricas GitHub; se preserva la política de base git
  auditada. Creación, transición, publicación y cambios de visibilidad tienen
  sus propios gates, incluida la revisión de public-readiness de la nueva
  superficie y la confirmación PM de dogfood. Las excepciones internas de
  tags/releases del ADR no son permisos reutilizables.

Los requisitos no reabren líneas abandonadas ni eligen una nueva arquitectura
durable. Una reconsideración necesita evidencia nueva, decisión PM explícita y
trazable, y su propio scope; no se presenta como optimización ya autorizada.

## Requisitos funcionales

Cada requisito expresa un outcome objetivo. La comprobación describe evidencia
de aceptación futura; no afirma una validación ya realizada.

### RF-1. Entrada y routing por intención

La ruta normal debe aceptar intención PM, outcome y constraints, reutilizar la
referencia inequívoca disponible y reconstruir operación, metadata y relaciones
verificables. Solo debe pedir un locator primario por cadena cuando falte y
datos adicionales ante una ambigüedad material. El PM responde decisiones que
requieren su juicio —producto, scope, riesgo, aceptación y autorización—, no
preguntas sobre datos derivables. Los códigos MOS y selectores explícitos se
conservan como interfaz avanzada y sus overrides siguen el contrato vigente.

**Comprobación:** ante una intención y evidencia suficientes, se explica una
única ruta y la siguiente acción segura sin pedir al PM que seleccione un código
ni repita metadata. Si falta evidencia o una decisión humana, se identifica
exactamente el faltante y quién o qué fuente puede resolverlo, sin inventarlo.

### RF-2. Continuidad de una unidad a través del lifecycle

Un outcome cohesivo debe poder recorrer planificación, implementación, revisión
y closeout mediante una unidad primaria, conservando sus decisiones, criterios
y evidencias. Las transiciones mecánicas no deben exigir un issue nuevo. Una
corrección del mismo PR permanece en la misma unidad y vuelve a review sobre el
cambio corregido con trazabilidad del review fuente y de la validación real.

Solo se justifica otra unidad ante un outcome independiente, durable y
accionable. Los gaps relacionados se agrupan cuando tienen cohesión real;
reducir el conteo no permite expandir scope silenciosamente, ocultar riesgos ni
fusionar resultados que necesitan criterios de salida independientes.

**Comprobación:** al reconstruir un outcome completo, cada unidad adicional
tiene un resultado independiente y criterios propios; ninguna existe solo por
el paso a QA, un handoff o una corrección del mismo PR. Cada acción mantiene su
autorización y sus gates aunque comparta unidad.

### RF-3. Incorporación de capacidades de herramientas y agentes

Project OS debe poder aprovechar capacidades nuevas sin convertir a cada
proveedor en arquitectura del kernel. Una evaluación debe comparar la fricción
observada con el resultado de usar la capacidad, incluyendo costo de adopción,
mantenimiento, validación y abandono. Antes de proponer actores, workflows o
infraestructura adicional, debe justificar por qué no bastan adapters, skills,
conectores o tooling acotado ya disponibles.

La integración debe conservar acceso verificable a las fuentes, límites de la
superficie, secret safety y autoridad PM; ninguna herramienta externa se vuelve
fuente implícita de permiso. Debe ser posible cambiarla o retirarla sin perder
decisiones durables ni dejar la continuidad atada a memoria privada.

**Comprobación:** una evaluación posterior identifica el paso o costo que
reduce, presenta evidencia comparable de valor neto y límites, y demuestra
continuidad al cambiar o retirar la herramienta. Si no hay valor neto o se
requiere una decisión durable pendiente, se difiere o rechaza la adopción.

### RF-4. Cold-start y cambio de agente, modelo o proveedor

Una sesión nueva debe reconstruir el estado relevante desde el kernel y las
fuentes vivas del target, incluidas las decisiones durables aplicables. Cambiar
de agente, modelo o proveedor no debe exigir al PM transcribir decisiones ya
registradas ni depender del chat anterior. El contexto transportado debe
limitarse a lo necesario y remitir a fuentes verificables.

**Comprobación:** una sesión sin la conversación original identifica outcome,
scope, cambios, validación disponible, decisiones y siguiente acción segura
desde las fuentes. Si falta acceso material, declara el faltante y se detiene;
un handoff o resumen nunca sustituye la revalidación previa a una escritura.

### RF-5. Reviews, auditorías y evolución de la metodología

Los findings deben tener disposición explícita para no perder gaps materiales
en chat ni disparar una cascada automática de issues. Las correcciones
bloqueantes vuelven a la misma unidad; un follow-up requiere estado actual
verificable, gap material, acción concreta, valor durable independiente y razón
para diferirlo. Preferencias, observaciones históricas, duplicados y resultados
ya resueltos no justifican unidades nuevas.

La evolución grande debe poder distribuirse en pocas unidades con outcomes
independientes, dependencias justificadas y criterios de salida claros. Se
agrupa por resultado, no por cada requisito, archivo o transición. Una fase
puede detenerse cuando su costo o complejidad supera el valor demostrado; la
necesidad de completar un plan no justifica continuarla.

**Comprobación:** el review distingue corrección de follow-up y deja su
disposición en la fuente viva. Una propuesta posterior de roadmap explica el
valor y las dependencias de cada unidad y cómo evaluar continuidad o abandono,
sin crear unidades ni reactivar líneas descartadas automáticamente.

### RF-6. Prototipo, QA, release y producción con control humano

El camino desde prototipo funcional hasta producción debe ser explícito y
reutilizar el trabajo verificable: criterios, decisiones, cambios y evidencia.
Debe añadir o revalidar los gates proporcionales al entorno y riesgo, sin
reconstruir el outcome desde cero ni exigir issues por cada transición.

La automatización puede preparar, verificar o reducir trabajo mecánico dentro
de la autoridad concedida. El humano conserva las decisiones de scope, riesgo,
aceptación, merge, release y producción. Deben quedar identificados la
validación previa, el responsable de cada gate, la evidencia de autorización,
la verificación posterior y el rollback o recuperación según el riesgo.
Producción sigue con el Humano PM por defecto; esta especificación no amplía
la delegación.

**Comprobación:** un recorrido de prototipo a producción permite verificar qué
evidencia se reutiliza y cuál debe renovarse, quién acepta el riesgo y quién
autoriza cada acción sensible. No se ejecuta una acción pendiente de gate; se
conservan resultados de validación y evidencia de verificación o recuperación.

## Requisitos no funcionales

| Área | Resultado exigido | Forma de comprobarlo |
| --- | --- | --- |
| Usabilidad | La ruta normal no exige memorizar el catálogo; minimiza locators, variables, prompts redundantes y decisiones mecánicas. | QA humano recorre los casos de uso, explica la siguiente acción segura y distingue decisiones materiales de solicitudes derivables. |
| Velocidad | Reducir fricción y tiempo de principio a fin, incluidos pasos, handoffs y cold resume; la rapidez de generación aislada no basta. | Comparación reproducible por outcome con las métricas de este documento, validación equivalente y gates humanos preservados. |
| Economía de complejidad | Una optimización elimina más complejidad durable de la que añade y reutiliza capacidades antes de crear entidades. | Evaluación del cambio, consumidores, alternativas y costo de mantenimiento; no se añade workflow engine, runtime, daemon, registry, cache o capa intermedia sin necesidad material demostrada y decisión aplicable. |
| Portabilidad | Independencia de modelo o proveedor, kernel agnóstico de targets y equivalencia semántica ES/EN donde corresponda. | Continuación con otra herramienta compatible y review de mismos outcomes, contratos y límites entre superficies; sin exigir paridad textual ni una arquitectura de generación. |
| Seguridad y autoridad | Fail-closed, secret safety, outputs no autorizantes, límites del browser y aprobación PM exacta intactos. | Casos de falta de acceso, conflicto y aprobación insuficiente no producen la mutación; una herramienta conectada no amplía permisos. |
| Reconstrucción y calidad | Evidencia accesible, validación proporcional y review antes del cierre, sin memoria privada ni snapshots de estado en docs. | Cold resume y review sobre fuentes, diff, archivos finales y resultados verificables; los gaps se reportan y no se convierten en claims de completitud. |

## Casos de uso y salidas observables

| Caso | Recorrido esperado | Criterio de salida |
| --- | --- | --- |
| CU-1. Idea → prototipo funcional | El PM expresa una intención; se aclaran solo decisiones materiales, se delimita el outcome y se implementa y revisa bajo RF-1 y RF-2. | Prototipo que satisface sus criterios, validación y review trazables, y mínimo de unidades justificadas; sin aprobación implícita de producción. |
| CU-2. Prototipo → producción | Se retoma la evidencia y se añaden readiness, QA, decisiones de riesgo, release y gates del entorno según RF-6. | Resultado aceptado y verificado para el entorno autorizado, con evidencia y recuperación previstas; sin issues por transiciones mecánicas. |
| CU-3. Cambio de agente a mitad de un outcome | La sesión receptora resuelve el kernel y consulta GitHub, git y decisiones aplicables según RF-4. | Puede explicar scope y siguiente acción segura sin consultar el chat anterior ni pedir que se repitan decisiones durables. |
| CU-4. Nueva capacidad de IA | Se evalúa un gap real, se compara valor neto y se conserva una vía de retirada o cambio según RF-3. | Adopción, diferimiento o rechazo sustentado en evidencia y decisión aplicable; no se adopta una herramienta solo por estar disponible. |
| CU-5. Review con corrección | Un hallazgo bloqueante vuelve al mismo issue/PR, se corrige con autorización scoped, se valida y se revisa de nuevo según RF-2 y RF-5. | Corrección trazable al review fuente y review del cambio corregido, sin issue adicional ni reescritura de la historia. |
| CU-6. Hallazgo independiente | Se verifica materialidad e independencia, se explicita la razón para diferir y se prepara un follow-up según RF-5. | Propuesta trazable con outcome propio; su creación sigue la aprobación exacta y el scope actual se conserva. |
| CU-7. Actualización de metodología | Se agrupan gaps por outcomes en pocas unidades secuenciales cuando haya dependencia real, conforme a RF-5. | Propuesta con valor observable, criterios de salida y abandono; ni mega-issue indiscriminado ni un issue por requisito. |
| CU-8. Ambigüedad o falta de aprobación | Se identifica la fuente o decisión material faltante y se aplica fail-closed según RF-1 y los constraints. | Estado no resuelto con causa y siguiente paso seguro; ninguna acción dependiente ejecutada por inferencia. |

## Historias de usuario representativas

- **Como PM**, quiero describir el outcome sin estudiar previamente el
  catálogo para empezar correctamente. Se acepta con CU-1 y RF-1.
- **Como PM**, quiero llegar desde una idea hasta un resultado validado con
  el menor número razonable de decisiones e issues. Se acepta con CU-1,
  CU-2 y RF-2, sin reducir los gates materiales.
- **Como PM**, quiero que las automatizaciones reduzcan trabajo mecánico sin
  asumir mis decisiones. Se acepta con CU-4, CU-8, RF-3 y RF-6.
- **Como developer**, quiero cambiar de agente o modelo sin perder el
  contexto durable del trabajo. Se acepta con CU-3 y RF-4.
- **Como reviewer**, quiero distinguir correcciones bloqueantes de mejoras
  independientes para no fragmentar innecesariamente el trabajo. Se acepta
  con CU-5, CU-6 y RF-5.
- **Como mantenedor**, quiero que las mejoras futuras se conviertan en
  unidades trazables sin sobredimensionar el roadmap. Se acepta con CU-7 y
  RF-5.
- **Como responsable de producción**, quiero conservar un gate humano
  verificable antes de cambios irreversibles o sensibles. Se acepta con CU-2,
  CU-8 y RF-6.

## Métricas y evaluación reproducible

Primero se registra un baseline reproducible en evidencia viva. El roadmap
posterior podrá fijar objetivos cuantitativos cuando haya evidencia suficiente
y decisión PM; esta especificación no asigna cifras, porcentajes ni thresholds
arbitrarios, ni declara ahorros ya obtenidos.

| Métrica | Definición para la comparación | Lectura del resultado |
| --- | --- | --- |
| Decisiones PM-facing por outcome | Número de decisiones solicitadas; separar juicio material, autorización y preguntas mecánicas o repetidas. | Reducir lo mecánico sin contar la omisión de aprobaciones o aceptación humana como mejora. |
| Operaciones manuales por outcome | Acciones humanas para transportar contexto, completar metadata, elegir rutas o ejecutar pasos; declarar la unidad de conteo y separar QA y acciones sensibles. | Menos trabajo repetido con igual resultado y control. |
| Issues por outcome end-to-end | Total de unidades creadas para el mismo resultado, incluidas correcciones y follow-ups; justificar las materialmente independientes. | Menor fragmentación sin ocultar unidades, ampliar scope ni agrupar outcomes sin cohesión. |
| Handoffs browser / terminal / humano | Traspasos que requieren intervención o transporte de contexto; registrar causa y trabajo necesario para retomar. | Reducir traspasos evitables y su costo, conservando separación de superficies y review independiente. |
| Tiempo y fricción de cold resume | Tiempo desde sesión limpia y acceso a fuentes hasta reconstruir scope y siguiente acción segura; contar fuentes solicitadas, aclaraciones y decisiones retranscritas. | Continuidad verificable sin chat previo; las limitaciones de acceso se registran por separado. |
| Tiempo end-to-end | Tiempo desde intención scoped hasta resultado aceptado y verificado para el entorno objetivo; separar ejecución, espera humana, herramientas y retrabajo. | Evitar trasladar demoras a QA o producción para aparentar rapidez en implementación. |
| Contexto transportado, cuando sea material | Bytes, caracteres o tokens con herramienta y método declarados, separando contrato resuelto, evidencia viva y texto reenviado. | Reducción sin pérdida de evidencia o gates; nunca ahorro universal deducido de un tokenizer. |

El protocolo de evaluación debe:

1. Elegir casos de uso representativos y declarar outcome, scope, clase de
   cambio, criterios, entorno objetivo y gates. Comparar recorridos
   equivalentes; un prototipo no se compara con un resultado en producción.
2. Registrar en la unidad o evaluación viva las referencias exactas, fecha,
   herramientas y versiones relevantes, método de conteo, puntos de inicio y
   fin, resultados y limitaciones. No copiar mediciones ni estado a este
   documento ni crear un sistema persistente de métricas por defecto.
3. Medir el baseline antes de evaluar la alternativa y declarar repeticiones
   y variabilidad cuando las haya. Separar demoras de acceso, red, cuota o
   aprobación; si falta evidencia, reportar la limitación sin inventar datos.
4. Comparar con scope, calidad y validación equivalentes, incluyendo costo de
   adopción, mantenimiento, retrabajo y retirada. Una reducción local de
   pasos no demuestra valor neto end-to-end.
5. Someter la mejora a QA humano y review proporcional. Detener o re-scopear
   si debilita autoridad, trazabilidad o seguridad, añade más complejidad de
   la que elimina o no demuestra valor; no continuar solo para completar una
   fase.

## Uso como source basis y validación de la especificación

`docs/requirements.md` puede suministrarse como `SOURCE_DOCS` a
[MOS-1.12](../project-os-es/operaciones/fase-1/MOS-1.12-actualizar-roadmap-de-proyecto-existente.md).
La operación debe releer las fuentes vivas y decisiones aplicables y proponer
pocas unidades de alto valor, cada una con outcome verificable, scope, criterios
de salida y dependencias justificadas. La relación con RF-1 a RF-6 y los casos
de uso ayuda a evaluar cobertura; no impone un issue por identificador ni fija
secuencia, prioridades, tecnología o arquitectura.

La aceptación documental requiere comprobar que cada capacidad del baseline
tenga source basis, que los requisitos se distingan de capacidades existentes
y que los outcomes puedan evaluarse sin convertir hipótesis en decisiones.
La validación agent-run proporcional incluye referencias y links del documento,
`git diff --check` y revisión del diff, sin tests narrativos ni tooling nuevo.
La revisión independiente debe evaluar coherencia estratégica y economía de
complejidad. La QA manual PM debe confirmar fidelidad de los cuatro objetivos,
usabilidad y velocidad deseadas, y preservación de autoridad y validación
humana. Los resultados pertenecen a la evidencia viva de revisión.

## Fuera de alcance

Esta especificación no implementa optimizaciones ni modifica kernel,
workflows, outputs, evidence, actors, modes o contratos operativos. No elige
CLI, bridge, MCP, plugin system, runtime, proveedor o arquitectura, ni adopta
una herramienta sin evaluación posterior. No cambia autorización, validación
humana o estrategia de repositorio público; no modifica `agent-os-cli` ni
otros targets. Tampoco crea el roadmap posterior, nuevas unidades, métricas
ficticias o benchmarks para aparentar cumplimiento.
