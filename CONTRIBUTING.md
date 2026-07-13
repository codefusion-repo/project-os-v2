# Guía de contribución

Project OS acepta contribuciones comunitarias. Esta guía define el proceso
para que una contribución sea trazable, validada y revisable. CodeFusion SpA
es propietaria y responsable final de esta guía; los mantenedores designados
por CodeFusion SpA la administran y aplican.

## Idiomas

- Los issues y pull requests pueden presentarse en **español o inglés**. No
  se exige traducir cada conversación, y los mantenedores pueden responder en
  cualquiera de los dos idiomas.
- Español permanece como idioma PM-facing y superficie predeterminada del
  repositorio.
- Si tu contribución modifica documentación o contratos con contraparte
  ES/EN (`project-os-es/` ↔ `project-os-en/`), debe preservar la paridad
  semántica de ambas superficies. La paridad estructural está guardada por
  `tests/test_project_os_bilingual_parity.py`.

## Proceso issue-first

1. Toda contribución comienza con un **issue** que registre por qué existe,
   objetivo, source basis, scope, out of scope, criterios de aceptación y
   validación prevista. No abras pull requests sin issue asociado.
2. Espera la revisión del issue antes de implementar: el scope acordado en el
   issue es el contrato de la contribución. Los cambios fuera de ese scope
   pertenecen a otro issue.

## Ramas de trabajo

- Trabaja siempre en una rama `work/<issue>-<slug>` creada desde `main`;
  nunca directo a `main`. La rama ata el código a su issue.

## Validación proporcional

- Valida proporcional al riesgo del cambio y reporta los comandos ejecutados
  con sus resultados reales. La base mínima del repositorio es:

  ```sh
  python3 -m tools.validate_kernel --kernel-dir project-os-es/kernel
  python3 -m tools.validate_kernel --kernel-dir project-os-en/kernel
  python3 -m pytest tests/ -q
  git diff --check
  ```

- Agrega o cambia tests solo cuando protegen comportamiento determinista,
  regresión, seguridad o contratos estables; nunca por defecto para docs,
  prompts o templates.

## Pull requests

- Abre el pull request como **draft**, documentando resumen, scope, límites,
  validación con resultados y notas de seguridad. La forma de referencia es
  `project-os-es/templates/pull-request.md`.
- No incluyas secretos, credenciales, tokens ni datos personales en código,
  tests, logs, PRs ni comentarios; redacta cualquier valor sensible como
  `[REDACTED]`.
- El merge y el cierre son decisiones de los mantenedores
  (**review-before-close**): antes de cerrar, el PR se compara contra el
  issue, el diff, los archivos finales y la validación reportada. El body de
  un PR es un claim, no prueba de completitud.

## Feedback y correcciones

- El feedback de review se atiende en la misma rama y PR de la contribución,
  con commits adicionales y validación actualizada.
- Un PR puede devolverse o cerrarse sin merge si se sale del scope del issue,
  si la validación falla o si introduce riesgos de seguridad o privacidad.

## Licencia de las contribuciones

- Las contribuciones aceptadas son **inbound = outbound** bajo la
  [Apache License 2.0](LICENSE) del repositorio.
- Cada contributor debe tener derecho a enviar el contenido que propone.
- **No se adopta CLA ni DCO.** Un CLA o DCO solo podría adoptarse mediante
  una decisión PM posterior y separada.

## Conducta

- Este proyecto adopta el
  [Contributor Covenant 3.0](CODE_OF_CONDUCT.md) como código de conducta.
- Los reportes de conducta se envían de forma privada a
  `support@codefusion.cl` con el asunto `[Project OS Conduct]`; los
  incidentes de conducta no se publican en issues.

## Soporte y seguridad

- Soporte general y expectativas de respuesta: [SUPPORT.md](SUPPORT.md).
- Reporte responsable de vulnerabilidades: [SECURITY.md](SECURITY.md) —
  nunca mediante issues públicos.

## Mantenimiento de esta guía

Esta guía se revisará antes de cada release público, cuando cambien los
canales o las superficies soportadas y, como mínimo, una vez al año.
