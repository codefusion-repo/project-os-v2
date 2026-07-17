# Skill: desarrollo mobile

Lente de calidad para trabajo mobile dentro de una tarea Project OS ya
resuelta. No prescribe un framework ni cómo operar Project OS: aporta criterio
para que una app siga siendo correcta cuando cambia de estado, pierde red,
interactúa con el dispositivo o corre bajo restricciones reales de plataforma.

## Responsabilidad

Aplicar juicio de ingeniería sobre lifecycle, navegación y estado, operación
offline, permisos, accesibilidad, recursos del dispositivo, APIs nativas,
persistencia local y entrega multiplataforma, dimensionado al producto y al
hardware que realmente soporta.

## Cuándo conviene usarla

- El scope toca una aplicación mobile, una vista nativa o una integración con
  hardware o APIs del sistema.
- Hay navegación, estado persistente, sincronización, conectividad intermitente
  o trabajo en background.
- Aparecen permisos, notificaciones, deep links, almacenamiento local o datos
  privados del dispositivo.
- Se revisa performance, consumo de memoria/batería, startup, accesibilidad o
  diferencias de comportamiento entre iOS y Android.
- La validación necesita emuladores y hardware físico, no solo tests aislados.

## Criterios de calidad

- **Lifecycle explícito.** Foreground, background, suspensión, reanudación,
  terminación por el sistema y recreación de la UI conservan invariantes. El
  código no asume que el proceso ni una vista seguirán vivos tras perder foco.
- **Navegación y propiedad del estado.** La ruta restaurable, el estado efímero
  de pantalla, el estado de sesión y los datos persistidos tienen dueños
  distintos. Back, deep links y restauración no crean pantallas imposibles ni
  duplican una operación.
- **Offline y conectividad intermitente.** Se define qué puede leerse o editarse
  sin red, cómo se representa pendiente/sincronizado/conflictivo y cómo se
  reconcilian reintentos. "Hay conexión" no equivale a "el servicio responde".
- **Permisos proporcionales.** Cada permiso se solicita en contexto, cuando la
  función lo necesita, con alternativa ante rechazo o restricción. Nunca se
  infiere autorización por haber obtenido acceso técnico al sensor o archivo.
- **Accesibilidad mobile.** Lectores de pantalla, orden de foco, escalado de
  texto, contraste, movimiento reducido, orientación y targets táctiles se
  validan con herramientas y uso real, no solo por apariencia.
- **Performance y recursos.** Startup frío/caliente, trabajo del hilo principal,
  memoria, batería, red y almacenamiento tienen budgets medibles. Listas,
  imágenes, sensores y tareas periódicas liberan o limitan recursos según el
  lifecycle.
- **Hardware y APIs nativas.** Cámara, ubicación, biometría, archivos, Bluetooth
  u otros dispositivos se tratan como capacidades opcionales que pueden faltar,
  fallar o cambiar mientras se usan. Los callbacks respetan cancelación y estado
  actual.
- **Diferencias iOS/Android.** Navegación del sistema, permisos, restricciones de
  background, formatos, notificaciones y disponibilidad de APIs se verifican
  por plataforma y versión soportada. Una abstracción compartida no borra esas
  diferencias.
- **Persistencia y migraciones locales.** El esquema local tiene versión,
  migración atómica o recuperable y compatibilidad con datos existentes. Se
  distingue caché descartable de datos del usuario que no pueden perderse.
- **Notificaciones y background.** Entrega duplicada, tardía o ausente es parte
  del contrato. Las tareas son idempotentes, acotadas y compatibles con las
  cuotas del sistema; no dependen de ejecución continua.
- **Privacidad del dispositivo.** Se minimizan datos, retención, logs y backups;
  se evita exponer contenido sensible en notificaciones, screenshots, clipboard
  o almacenamiento no apropiado. La telemetría describe eventos sin valores
  privados.
- **Stores y releases como gates separados.** Compatibilidad técnica no implica
  aprobación para firmar, publicar o distribuir. Stores, firma y releases
  requieren sus propias evidencias, autoridades y validaciones fuera de esta
  skill.
- **Validación representativa.** Unitarios cubren lógica; integración cubre
  persistencia y bridges; UI cubre flujos críticos. Emuladores amplían matrices,
  pero hardware físico valida sensores, memoria, batería, notificaciones,
  accesibilidad y comportamiento térmico.

## Riesgos que debe detectar

- Pérdida o duplicación de acciones al suspender/reanudar o recrear una pantalla.
- Estado de navegación que contradice sesión, datos persistidos o deep links.
- Colas offline sin idempotencia, orden ni política de conflictos.
- Permisos pedidos al inicio, sin explicación ni alternativa ante rechazo.
- Trabajo pesado en el hilo principal, startup bloqueado, memory leaks o wakeups
  que degradan batería.
- Uso de una API nativa sin detectar disponibilidad, cancelación ni cambios de
  versión/plataforma.
- Migraciones locales destructivas o cachés tratadas como fuente durable.
- Notificaciones que filtran datos, se procesan dos veces o abren rutas inválidas.
- Claims de compatibilidad basados solo en un simulador o un dispositivo potente.

## Decisiones que debe favorecer

- Modelar transiciones de lifecycle y estados recuperables antes de sumar
  efectos secundarios.
- Separar estado efímero, persistente y sincronizado, con una fuente de verdad
  explícita para cada uno.
- Diseñar offline como un contrato de producto, no como reintentos invisibles.
- Pedir la capacidad mínima en el momento de uso y mantener un camino degradado.
- Medir en los dispositivos más débiles soportados antes de optimizar por intuición.
- Encapsular diferencias nativas en bordes verificables sin fingir paridad donde
  la plataforma no la ofrece.
- Hacer migraciones pequeñas y recuperables, conservando datos del usuario.
- Combinar automatización con sesiones en hardware físico y tecnologías de
  asistencia para los flujos de mayor riesgo.

## Señales de alerta

- "El framework maneja el lifecycle/offline por nosotros".
- "Si pidió el permiso una vez, siempre estará disponible".
- "Funciona en el simulador" como evidencia suficiente de compatibilidad.
- Guardar toda la navegación y todos los datos en un único store global.
- Una tarea background que necesita correr cada minuto para que el producto sea
  correcto.
- Borrar la base local ante cualquier error de migración.
- Tratar firma, publicación o acceso a stores como consecuencia automática de
  que el build compila.

## Ejemplos de criterio

Contrastes compactos y portables. Son pseudocódigo conceptual, no código
productivo ni instrucciones específicas de Flutter, Kotlin o Swift.

### Reanudación sin duplicar efectos

Problemático — cada foreground dispara otra escritura aunque ya esté en curso:

```text
onForeground:
  uploadDraft(currentDraft)
```

Mejor — el estado persistido identifica la operación y el reintento es
idempotente:

```text
onForeground:
  for operation in pendingOperations:
    syncOnce(operation.id, operation.version)
```

### Permiso denegado como estado soportado

Problemático — solicita cámara al arrancar y bloquea toda la app si se rechaza:

```text
onLaunch -> requestCamera -> denied -> fatalScreen
```

Mejor — solicita en contexto y conserva una alternativa proporcional:

```text
onScanAction -> explainPurpose -> requestCamera
granted -> scan
denied  -> manualEntry + settingsHelp
```

### Offline con conflicto explícito

Problemático — "última escritura gana" sobrescribe cambios remotos sin señal:

```text
reconnect -> upload(localDocument)
```

Mejor — sincroniza contra una versión conocida y presenta o aplica una política
de conflicto definida:

```text
reconnect -> compare(local.baseVersion, remote.version)
same      -> upload(localChange, operationId)
different -> resolveConflict(localChange, remoteChange)
```

## Output esperado de la skill

Juicio técnico accionable dentro del scope: transiciones y estados faltantes,
riesgos de plataforma o dispositivo con su consecuencia, decisión recomendada
y su porqué, budgets relevantes y una matriz de validación proporcional que
distinga automatización, emulador y hardware físico. No produce artefactos,
workflows ni instrucciones de publicación.

## Límites / no autorización

Skill opcional. No concede permisos ni reemplaza scope vivo, aprobación PM,
preflight de rama, evidencia, validación, trazabilidad ni review-before-close.
No autoriza firma, acceso a stores, releases, distribución ni uso de datos o
hardware: esos gates siguen gobernados por Project OS y por el target.
