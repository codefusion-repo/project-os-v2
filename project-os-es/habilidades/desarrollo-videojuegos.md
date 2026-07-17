# Skill: desarrollo de videojuegos

Lente de calidad para trabajo de videojuegos dentro de una tarea Project OS ya
resuelta. No prescribe un engine ni cómo operar Project OS: aporta criterio para
que gameplay, simulación y contenido se mantengan correctos dentro de budgets de
frame, memoria, hardware y experiencia jugable verificables.

## Responsabilidad

Aplicar juicio de ingeniería sobre game loop, input, estados y escenas, física,
memoria, assets, guardado, audio, networking, plataformas, profiling,
accesibilidad y QA de gameplay, alineado a las mecánicas y dispositivos que el
producto realmente soporta.

## Cuándo conviene usarla

- El scope toca gameplay, simulación, render, animación, cámaras, UI in-game o
  transiciones entre escenas.
- Hay input de uno o más dispositivos, física, colisiones, tiempo o replay.
- Se agregan assets, audio, streaming, carga, save/load o compatibilidad de datos.
- Aparecen multiplayer, replicación, predicción o decisiones de autoridad.
- Se revisan performance por frame, memoria, plataformas, accesibilidad o QA en
  hardware real.

## Criterios de calidad

- **Game loop y frame budget.** Update, simulación, render, audio y trabajo
  asíncrono tienen responsabilidades y frecuencias claras. CPU, GPU y esperas se
  perfilan por separado contra un budget derivado del framerate objetivo; no se
  confunde promedio con estabilidad de frame pacing.
- **Tiempo y determinismo.** Movimiento y cooldowns usan la noción de tiempo
  apropiada. La simulación que necesita reproducibilidad define fixed steps,
  orden, seeds, precisión y fuentes de no determinismo; render puede interpolar
  sin cambiar el estado autoritativo.
- **Input y dispositivos.** Acciones de juego se separan de teclas o botones
  concretos. Remapeo, hot-plug, múltiples dispositivos, dead zones, métodos
  simultáneos y desconexión tienen estados definidos, con feedback coherente.
- **Estados, escenas y transiciones.** Gameplay, pausa, menús, cinemáticas,
  carga, derrota y reanudación tienen dueños y transiciones explícitas. Cambiar
  escena no deja listeners, timers o referencias a objetos destruidos.
- **Física.** Capas de colisión, unidades, timestep, triggers, teleports y
  autoridad se deciden conscientemente. Se toleran límites numéricos y orden de
  contactos; el determinismo no se asume entre plataformas o engines.
- **Memoria y pooling.** Allocations, lifetime y ownership de objetos/assets se
  observan por escena y sesión. Pooling se aplica a churn medido, con reset
  completo del estado; no conserva referencias o eventos obsoletos.
- **Asset pipeline y cargas.** Importación, compresión, variantes, dependencias,
  versionado y budgets de textura/malla/animación/audio son repetibles. La carga
  crítica tiene progreso honesto, cancelación y estrategia contra picos; no se
  hace I/O bloqueante en el loop principal.
- **Save/load y compatibilidad.** El formato tiene versión, validación, escritura
  atómica y recuperación ante corrupción. Se preserva compatibilidad o existe
  migración explícita; nunca se deserializa contenido no confiable como objetos
  ejecutables.
- **Audio.** Mezcla, prioridades, buses, voces simultáneas, spatialization,
  pausas, transiciones y pérdida de dispositivo tienen límites. Volumen,
  subtítulos y señales visuales apoyan accesibilidad sin depender solo del oído.
- **Networking y autoridad.** Cuando aplica, servidor, host o peer autoritativo
  se define por cada estado/acción. Tick rate, latencia, pérdida, orden,
  reconciliación, predicción y anti-cheat se diseñan juntos; el cliente no
  decide resultados competitivos por conveniencia.
- **Plataformas y hardware.** Resolución, aspect ratio, input, memoria, storage,
  CPU/GPU, shaders, suspensión y comportamiento térmico varían por target. Los
  quality tiers reducen costo sin romper legibilidad ni mecánicas.
- **Profiling representativo.** Se captura en builds y escenas representativas,
  con marcadores que atribuyen CPU, GPU, allocations, draw calls, streaming y
  red. Se comparan percentiles y spikes, no solo FPS promedio en el editor.
- **Accesibilidad.** Remapeo, alternativas a input sostenido/repetido, tamaño y
  contraste de UI, subtítulos, reducción de flashes/movimiento y opciones de
  dificultad se evalúan contra las mecánicas, sin prometer una solución única.
- **QA de gameplay.** Tests deterministas protegen reglas; soak y stress revelan
  acumulación; sesiones exploratorias cubren combinaciones emergentes. Hardware
  real valida controles, frame pacing, memoria, temperatura, audio, suspensión
  y experiencia, además de corrección funcional.

## Riesgos que debe detectar

- Trabajo no acotado por frame, spikes periódicos o stalls de CPU/GPU/I/O.
- Simulación dependiente del framerate o supuesto falso de determinismo.
- Input ligado a un dispositivo concreto, sin remapeo ni desconexión segura.
- Transiciones que duplican managers, listeners, audio o entidades persistentes.
- Pools que devuelven objetos con estado residual o esconden presión de memoria.
- Assets sin budgets, variantes incorrectas o dependencia circular que infla
  tiempos de carga y memoria.
- Saves parcialmente escritos, incompatibles o aceptados sin validación.
- Audio sin límites de voces o información crítica disponible solo por sonido.
- Cliente con autoridad sobre posición, daño, inventario o economía compartida.
- Optimización basada en el editor o en un PC potente, sin profiling del target.
- QA que confirma que "se puede terminar" pero no explora feel, exploits,
  fatiga, accesibilidad ni sesiones largas.

## Decisiones que debe favorecer

- Derivar budgets de objetivos de producto y medir antes de elegir optimizaciones.
- Separar simulación, presentación y efectos; usar fixed step solo donde aporta
  una invariante concreta.
- Mapear input a acciones y contextos con alternativas configurables.
- Modelar estados y ownership para que cada transición libere lo que crea.
- Optimizar lifetime y formatos de assets antes de aplicar pooling generalizado.
- Versionar saves desde el primer formato que deba sobrevivir a una release.
- Definir autoridad y modelo de red antes de construir mecánicas dependientes de
  baja latencia.
- Perfilar builds representativas en el hardware más débil soportado.
- Combinar tests automatizados con QA exploratorio y evaluación del gameplay.

## Señales de alerta

- "Con 60 FPS promedio estamos bien" sin percentiles ni frame pacing.
- Multiplicar movimiento por delta y asumir que toda simulación ya es estable.
- "El engine hace determinista la física" entre plataformas.
- Pooling de cada objeto sin medir allocation, lifetime ni costo de reset.
- Cargar todos los assets al inicio para evitar diseñar streaming.
- Guardar el grafo completo de objetos del runtime como formato de save.
- Confiar en el cliente porque "es solo un juego".
- Dar por validado un target porque funciona dentro del editor.

## Ejemplos de criterio

Contrastes compactos y portables. Son pseudocódigo conceptual, no código
productivo ni instrucciones específicas de Unity, Unreal u otro engine.

### Simulación separada del render

Problemático — reglas y render avanzan una vez por frame variable:

```text
eachFrame(delta):
  simulate(delta)
  render(world)
```

Mejor — la simulación crítica avanza con pasos acotados y el render interpola:

```text
eachFrame(delta):
  accumulator += clamp(delta)
  while accumulator >= fixedStep:
    simulate(fixedStep)
    accumulator -= fixedStep
  render(interpolate(previous, current, accumulator / fixedStep))
```

### Pooling con reset verificable

Problemático — recicla una entidad con listeners y daño anterior:

```text
pool.release(enemy)
pool.acquire() -> same enemy state
```

Mejor — el contrato de retorno y adquisición restaura todas las invariantes:

```text
release(entity): detachEvents + stopAudio + clearTargets + deactivate
acquire(config): resetTransform + resetHealth + bindEvents + activate
```

### Save versionado y atómico

Problemático — sobrescribe el único archivo con objetos del runtime:

```text
write("save", serialize(currentSceneObjects))
```

Mejor — valida datos, migra versiones y reemplaza solo tras completar la
escritura:

```text
payload = validateAndMigrate(read("save"), supportedVersions)
write("save.tmp", encode(version, stableData(payload)))
atomicReplace("save.tmp", "save")
```

## Output esperado de la skill

Juicio técnico accionable dentro del scope: riesgo de gameplay o plataforma con
su consecuencia, budget e invariante afectados, decisión recomendada y tradeoff,
perfil o evidencia que falta y una estrategia de validación que combine tests,
profiling, QA exploratorio y hardware real. No produce artefactos, workflows ni
manuales de engine.

## Límites / no autorización

Skill opcional. No concede permisos ni reemplaza scope vivo, aprobación PM,
preflight de rama, evidencia, validación, trazabilidad ni review-before-close.
No autoriza publicación, servicios online, cambios de economía, uso de assets o
acceso a plataformas: esos gates siguen gobernados por Project OS y por el
target.
