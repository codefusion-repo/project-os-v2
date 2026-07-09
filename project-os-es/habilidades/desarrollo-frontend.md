# Skill: desarrollo frontend

Lente de calidad para trabajo frontend dentro de una tarea Project OS ya
resuelta. No describe cómo operar Project OS: aporta el criterio que separa una
UI robusta de una que se ve bien solo en el camino feliz.

## Responsabilidad

Aplicar juicio de ingeniería sobre estados de UI, accesibilidad, fronteras de
componentes, propiedad del estado, integración con APIs y performance web,
alineado al framework y la madurez real del target.

## Cuándo conviene usarla

- El scope toca interfaces, componentes, estado de cliente o integración con
  APIs desde la UI.
- Hay formularios, acciones destructivas o flujos con errores y reintentos.
- Aparecen dudas de accesibilidad, responsive o performance percibida.
- Se revisa un PR frontend y hace falta criterio más allá de "se ve bien".

## Criterios de calidad

- **Todos los estados.** Cada vista contempla carga, vacío, error, éxito,
  deshabilitado y, si aplica, pendiente/optimista. El estado de error es
  recuperable y dice qué pasó, no una pantalla en blanco.
- **Accesibilidad real.** HTML semántico primero; ARIA solo cuando la semántica
  nativa no alcanza. Navegación por teclado, foco visible y orden de foco
  correcto, sobre todo en modales y menús.
- **Fronteras y propiedad del estado.** El estado vive en el nivel que lo
  necesita; se evita duplicarlo o subirlo de más. Distinción clara entre datos
  de servidor (cacheables, revalidables) y estado local de UI.
- **Integración con APIs.** Se manejan carga y error de cada request; los
  errores se muestran donde el usuario actúa. Reintentos y recuperación sin
  dejar la UI en estado inconsistente.
- **Responsive y bordes de layout.** Texto largo, listas vacías, contenido
  desbordado y viewports chicos no rompen el layout.
- **Formularios y acciones destructivas.** Validación con feedback claro y a
  tiempo; las acciones irreversibles piden confirmación y protegen contra el
  doble submit.
- **Performance percibida.** Tamaño de bundle bajo control, carga diferida de lo
  pesado y cuidado de Core Web Vitals (LCP/CLS/INP) donde el target los mide.

## Riesgos que debe detectar

- Vistas que solo cubren el éxito y truenan o quedan en blanco ante error o
  vacío.
- Spinners infinitos: request sin timeout ni estado de fallo.
- Componentes inaccesibles: divs clicables sin rol ni teclado, foco perdido al
  abrir o cerrar overlays.
- Estado de servidor tratado como estado local: datos obsoletos, doble fuente
  de verdad, condiciones de carrera entre requests.
- Doble submit o acción destructiva sin confirmación.
- Regresiones de layout en breakpoints o con contenido dinámico real.

## Decisiones que debe favorecer

- Cubrir bien los estados y la accesibilidad antes que el pulido visual.
- Semántica nativa sobre reimplementar controles con ARIA.
- Estado local simple y colocado cerca sobre store global prematuro.
- Manejar el error donde ocurre sobre asumir que el request siempre responde.

## Señales de alerta

- "Funciona en mi máquina / en Chrome" como criterio de terminado.
- Maquetar solo el happy path y dejar error y vacío "para después".
- Reemplazar `<button>` o `<a>` por divs con onClick.
- Meter todo el estado en un store global para "no pensarlo".
- Animaciones y estética que esconden que el flujo real está roto.

## Ejemplos de criterio

Contrastes compactos que ilustran el nivel de calidad esperado. Son snippets
genéricos (estilo React/JSX), no plantillas ni reglas de workflow.

### Todos los estados, no solo el éxito

Problemático — solo carga y éxito; error y vacío quedan en blanco:

```jsx
function Lista({ items, loading }) {
  if (loading) return <Spinner />;
  return <ul>{items.map(i => <li key={i.id}>{i.nombre}</li>)}</ul>;
}
```

Mejor — carga, error recuperable, vacío y éxito, cada uno explícito:

```jsx
function Lista({ items, loading, error, onRetry }) {
  if (loading) return <Spinner />;
  if (error) return <Aviso mensaje="No se pudo cargar la lista." accion={onRetry} />;
  if (items.length === 0) return <Vacio mensaje="Aún no hay elementos." />;
  return <ul>{items.map(i => <li key={i.id}>{i.nombre}</li>)}</ul>;
}
```

### Semántica nativa antes que div clicable

Problemático — invisible para teclado y lectores de pantalla:

```jsx
<div className="btn" onClick={guardar}>Guardar</div>
```

Mejor — control nativo con foco, teclado y estado deshabilitado gratis:

```jsx
<button type="button" onClick={guardar} disabled={enviando}>
  {enviando ? "Guardando…" : "Guardar"}
</button>
```

### Doble submit y acción destructiva

Problemático — permite doble envío y oculta el error:

```jsx
async function onSubmit() {
  await api.eliminarCuenta();  // sin confirmación, sin pending, error tragado
}
```

Mejor — confirmación, estado pendiente y error visible donde el usuario actúa:

```jsx
async function onSubmit() {
  if (!(await confirmar("Esta acción elimina la cuenta y no se puede deshacer."))) return;
  setEnviando(true);
  try {
    await api.eliminarCuenta();
  } catch {
    setError("No se pudo eliminar la cuenta. Intenta de nuevo.");
  } finally {
    setEnviando(false);  // el botón queda deshabilitado mientras enviando === true
  }
}
```

## Output esperado de la skill

Juicio técnico accionable dentro del scope: estados y bordes faltantes, riesgos
de accesibilidad e integración con su consecuencia, la decisión de UI
recomendada y su porqué, y qué verificar antes de dar la vista por terminada.
No produce artefactos ni templates; alimenta la implementación o la review.

## Límites / no autorización

Skill opcional. No concede permisos ni reemplaza scope vivo, aprobación PM,
preflight de rama, validación, trazabilidad ni review-before-close: eso lo
gobierna Project OS. Aquí solo aporta criterio de calidad.
