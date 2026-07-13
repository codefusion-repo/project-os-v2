# Política de soporte

El soporte de Project OS es **best-effort y sin SLA**. CodeFusion SpA es
propietaria y responsable final de esta política; los mantenedores designados
por CodeFusion SpA la administran y aplican.

## Qué esperar

- Los issues, pull requests y solicitudes generales se revisan según
  capacidad, sin tiempo garantizado de respuesta.
- No existe SLA ni plazo garantizado de corrección, merge, release o
  publicación.
- La prioridad depende de severidad, impacto, reproducibilidad y capacidad
  disponible.

## Versiones y superficies cubiertas

- Antes del primer release público, solo el `main` vigente recibe soporte
  best-effort. Después del primer release público, se soportarán `main` y la
  última versión pública; no se garantizan backports ni soporte para
  versiones anteriores.
- Se consideran activas las superficies vigentes `project-os-es/` y
  `project-os-en/`, junto con el kernel, el resolver, las operaciones, los
  templates, los adapters, el tooling y la documentación presentes en el
  árbol actual. No se soportan superficies retiradas, ramas históricas, tags
  internos ni contenido recuperable únicamente desde git.

## Canales adecuados

- **Issues del repositorio** para bugs, preguntas de uso y propuestas, en
  español o inglés.
- **Pull requests** para contribuciones, siguiendo
  [CONTRIBUTING.md](CONTRIBUTING.md).
- No existe canal de soporte en tiempo real ni soporte comercial
  comprometido.

## Qué queda fuera de alcance

- Desarrollo a medida, consultoría o features garantizadas bajo demanda.
- Garantías de tiempos de respuesta, corrección o release.
- Soporte de tooling que aún no existe oficialmente: CLI, API, bridge, MCP,
  GPT action y tooling downstream.
- Soporte de superficies retiradas o de contenido histórico de git.

## Qué no es soporte

- **Vulnerabilidades de seguridad:** repórtalas de forma privada según
  [SECURITY.md](SECURITY.md); nunca mediante issues públicos.
- **Incidentes de conducta:** repórtalos de forma privada según
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md); no se publican en issues.

## Mantenimiento de esta política

Esta política se revisará antes de cada release público, cuando cambien los
canales o las superficies soportadas y, como mínimo, una vez al año.
