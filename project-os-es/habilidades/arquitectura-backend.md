# Skill: arquitectura backend

Lente de calidad para trabajo backend dentro de una tarea Project OS ya
resuelta. No describe cómo operar Project OS: aporta el criterio técnico que
distingue una implementación correcta de una que solo parece funcionar.

## Responsabilidad

Aplicar juicio de ingeniería sobre modelo de dominio, datos, contratos de API,
autorización, migraciones, confiabilidad y observabilidad, dimensionado a la
madurez real del target y no a una escala imaginaria.

## Cuándo conviene usarla

- El scope toca modelos de datos, servicios, APIs, integraciones, colas o
  trabajos en segundo plano.
- Hay que cambiar un contrato o esquema que otros ya consumen.
- Aparecen dudas de consistencia, concurrencia, rollback o exposición de datos.
- Se revisa un PR backend y hace falta criterio más allá de "los tests pasan".

## Criterios de calidad

- **Dominio y propiedad del dato.** Cada dato tiene un dueño claro; nadie
  escribe en tablas de otro servicio por atajo. Las invariantes del dominio se
  imponen en el borde de escritura, no confiando en el llamador.
- **Contratos de API.** Entradas y salidas explícitas y versionables. Cambios
  compatibles hacia atrás salvo deprecación anunciada. Errores con semántica
  estable (código, forma, distinción cliente/servidor), no strings arbitrarios.
- **Idempotencia y reintentos.** Toda operación reintentable define su clave de
  idempotencia; escribir dos veces no duplica efectos.
- **Autorización y exposición.** La autorización se decide en el servidor por
  operación y por recurso, no en el cliente. La respuesta expone solo los
  campos que el actor puede ver; sin sobre-serializar entidades internas.
- **Migraciones.** Expand-and-contract: primero agregar, luego migrar datos,
  luego retirar. Índices para los patrones de consulta reales. Rollback pensado
  antes de tocar datos críticos.
- **Confiabilidad.** Cada llamada externa tiene timeout, política de reintento
  con backoff y un modo de fallo definido. Rate limits y degradación explícitos.
  Los jobs en segundo plano son reejecutables y observables.
- **Observabilidad.** Logs estructurados con id de correlación, métricas de
  latencia/errores/saturación y trazas en los saltos entre servicios. SLO
  proporcional a lo que el target realmente promete.

## Riesgos que debe detectar

- Cambios de esquema o contrato que rompen a consumidores existentes sin ruta
  de compatibilidad.
- Escrituras sin transacción o sin idempotencia que corrompen datos en carrera.
- Migraciones sin rollback, sin índice, o que bloquean tablas grandes en línea.
- Autorización ausente, evaluada en el cliente, o fuga de datos por respuestas
  demasiado amplias.
- Llamadas externas sin timeout que propagan caídas; reintentos sin límite que
  amplifican incidentes.
- Consultas N+1 o full scans escondidos tras un ORM.

## Decisiones que debe favorecer

- La arquitectura más simple que sostenga el dominio y la carga cercana; añadir
  complejidad solo cuando un requisito concreto lo justifica.
- Consistencia y corrección sobre micro-optimización prematura.
- Fronteras explícitas entre servicios/módulos sobre acoplamiento por base de
  datos compartida.
- Contratos y errores estables sobre la conveniencia de un solo llamador.

## Señales de alerta

- "Después lo indexamos / después le ponemos auth / después migramos".
- Un endpoint que devuelve el modelo entero "por si acaso".
- Reintentar un fallo sin saber si la operación es idempotente.
- Justificar microservicios, colas o caché por una escala que el target no tiene.
- Medir el éxito solo por cobertura de tests, sin observabilidad en producción.

## Output esperado de la skill

Juicio técnico accionable dentro del scope: riesgos backend concretos con su
consecuencia, la decisión de diseño recomendada y su porqué, y qué verificar
antes de dar el cambio por correcto. No produce artefactos ni templates;
alimenta la implementación o la review con criterio.

## Límites / no autorización

Skill opcional. No concede permisos ni reemplaza scope vivo, aprobación PM,
preflight de rama, validación, trazabilidad ni review-before-close: eso lo
gobierna Project OS. Aquí solo aporta criterio de calidad.
