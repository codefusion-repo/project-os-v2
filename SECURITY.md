# Política de seguridad

Esta política define cómo reportar vulnerabilidades de Project OS de forma
responsable. CodeFusion SpA es propietaria y responsable final de esta
política; los mantenedores designados por CodeFusion SpA la administran y
aplican, y solo personas autorizadas por CodeFusion SpA emiten decisiones
oficiales de seguridad.

## Versiones y superficies soportadas

- Antes del primer release público, solo el `main` vigente de este
  repositorio recibe soporte de seguridad best-effort.
- Después del primer release público, se soportarán `main` y la última
  versión pública. No se garantizan backports ni soporte para versiones
  anteriores.
- Se consideran activas las superficies vigentes `project-os-es/` y
  `project-os-en/`, junto con el kernel, el resolver, las operaciones, los
  templates, los adapters, el tooling y la documentación presentes en el
  árbol actual.
- No se soportan superficies retiradas, ramas históricas, tags internos ni
  contenido recuperable únicamente desde el historial git.
- CLI, API, bridge, MCP, GPT action y tooling downstream no se consideran
  soportados mientras no existan oficialmente.

## Cómo reportar una vulnerabilidad

- Envía el reporte de forma **privada** por email a `support@codefusion.cl`.
  Asunto recomendado: `[Project OS Security]`.
- **No publiques** vulnerabilidades, secretos, tokens, datos personales ni
  detalles explotables en issues, pull requests o comentarios.
- Cuando exista un repositorio público y el setting se habilite mediante una
  aprobación separada, el private vulnerability reporting de GitHub será el
  canal estructurado recomendado, y el email quedará como canal secundario.
  Esta política no habilita ese setting ni ningún otro.

## Qué incluir en un reporte

Incluye solo información segura:

- superficie o ruta afectada, y el commit o versión donde se observa;
- tipo de impacto (por ejemplo: exposición de datos, escalada de permisos,
  ejecución no prevista);
- pasos de reproducción **sin valores sensibles**: redacta secretos, tokens y
  datos personales como `[REDACTED]`, reportando solo rutas, nombres de
  variables y tipo de riesgo;
- mitigación o workaround conocido, si existe.

Nunca incluyas secretos, credenciales, tokens, claves, datos personales de
terceros ni exploits listos para usar.

## Expectativas de respuesta

- Objetivo best-effort de acuse inicial dentro de cinco días hábiles.
- No existe SLA ni plazo garantizado de corrección, merge, release o
  publicación.
- La prioridad depende de severidad, impacto, reproducibilidad y capacidad
  disponible.

## Relación con soporte y conducta

- El soporte general (bugs no de seguridad, preguntas, propuestas) se rige
  por [SUPPORT.md](SUPPORT.md) y **no** usa el canal de seguridad.
- Los reportes de conducta se rigen por
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Mantenimiento de esta política

Esta política se revisará antes de cada release público, cuando cambien los
canales o las superficies soportadas y, como mínimo, una vez al año.
