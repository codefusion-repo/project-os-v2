# Project OS en 5 segundos

**Project OS es un kernel operativo para dirigir proyectos de software con
agentes de IA sin perder el control.** Tú decides; GitHub recuerda; los agentes
ejecutan solo lo que apruebas.

Tres verdades sostienen todo el sistema:

1. **GitHub es la memoria viva.** Issues, PRs, comentarios, reviews, ramas,
   commits y evidencia de validación se leen en vivo, nunca de la memoria de un
   chat.
2. **El kernel es el comportamiento estable.** `kernel/*.json` (en la raíz del
   repo) define actores, modos, workflows, límites, evidencia y estados. La
   carpeta `project-os-es/kernel/` es la superficie compacta en español; el
   kernel raíz sigue siendo la fuente canónica de comportamiento.
3. **Ningún texto otorga permisos.** Docs, templates, prompts y salidas de
   resolver solo dan forma al trabajo. Escribir, mergear, cerrar o desplegar
   exige aprobación PM exacta más los gates del kernel.

## Mapa de esta carpeta

| Documento | Responde | Léelo cuando |
|---|---|---|
| [empezar.md](empezar.md) | Quién hace qué y cómo se adopta Project OS. | Arrancas un proyecto o una sesión nueva. |
| [reglas.md](reglas.md) | Las reglas de seguridad y verdad que nunca se negocian. | Antes de delegar escritura a un agente. |
| [ritmo.md](ritmo.md) | El ciclo de trabajo día a día y las variables PM. | Operas el proyecto y necesitas el siguiente paso. |
| [adapters](../adapters/README.md) | Bootloaders compactos para targets. | Adoptas Project OS en un repo. |
| [templates](../templates/README.md) | Formas no operacionales enlazadas por artefactos. | Drafteas route prompts, bundles, reports o documentos. |

El catálogo de operaciones en español vive en
[`project-os-es/operaciones/README.md`](../operaciones/README.md): un prompt
compacto por operación, organizado por fase.

## Cómo se conectan las piezas

1. [Docs](README.md) orienta al PM y a la persona usuaria.
2. [Operaciones](../operaciones/README.md) elige la acción concreta.
3. [Adapters](../adapters/README.md) bootloadean el target o la superficie.
4. [Kernel](../kernel/manifest.json) y resolver hidratan comportamiento y
   artefactos.
5. Los artefactos enlazan un `required_template`; los
   [templates](../templates/README.md) dan forma al output sin autorizar nada.

## Siguiente paso

¿Primera vez? Lee [empezar.md](empezar.md). ¿Ya operando? Abre
[ritmo.md](ritmo.md) y elige la operación de tu fase.

### Casos frecuentes

| Si quieres… | Empieza por |
|---|---|
| Empezar con Project OS por primera vez | [empezar.md](empezar.md) |
| Adoptar un repo target existente | [MOS-0.3](../operaciones/fase-0/MOS-0.3-adoptar-proyecto-existente.md), verificando con [MOS-0.5](../operaciones/fase-0/MOS-0.5-verificar-adopcion-del-target.md) |
| Activar una sesión de browser chat | [MOS-0.1](../operaciones/fase-0/MOS-0.1-activar-sesion-browser-chat.md) |
| Rescatar una sesión incoherente o agotada | [MOS-0.6](../operaciones/fase-0/MOS-0.6-transferir-contexto-de-sesion.md) |
| Crear o derivar el siguiente issue | [MOS-3.1](../operaciones/fase-3/MOS-3.1-draftear-siguiente-issue-desde-trazabilidad.md) o [MOS-3.8](../operaciones/fase-3/MOS-3.8-draftear-issue-desde-descripcion.md) |
| Routear una implementación al terminal agent | [MOS-3.4](../operaciones/fase-3/MOS-3.4-draftear-route-prompt-de-implementacion.md) |
| Trabajar sin terminal agent (plan manual) | [MOS-3.30](../operaciones/fase-3/MOS-3.30-draftear-plan-de-implementacion-manual.md), procesando el resultado con [MOS-3.31](../operaciones/fase-3/MOS-3.31-procesar-resultado-de-implementacion-manual.md) |
| Revisar un PR antes de cerrarlo | [MOS-3.7](../operaciones/fase-3/MOS-3.7-revisar-pr-antes-de-cerrar.md) |
| Cerrar un PR/issue con evidencia | [MOS-3.6](../operaciones/fase-3/MOS-3.6-draftear-comandos-de-closeout.md) y [MOS-3.9](../operaciones/fase-3/MOS-3.9-verificar-estado-post-merge.md) |
| Procesar QA humano | [MOS-4.4](../operaciones/fase-4/MOS-4.4-procesar-checklist-qa-de-issue-pr.md) o [MOS-4.5](../operaciones/fase-4/MOS-4.5-procesar-checklist-qa-de-feature.md) |
| Revisar seguridad o auditar | [MOS-3.23](../operaciones/fase-3/MOS-3.23-solicitar-revision-de-seguridad.md) o [MOS-3.13](../operaciones/fase-3/MOS-3.13-auditar-trazabilidad.md) |
| Preparar release o deploy | [MOS-3.10](../operaciones/fase-3/MOS-3.10-analizar-readiness-de-release.md) o [MOS-R.11](../operaciones/fase-5/MOS-R.11-revisar-readiness-de-despliegue-por-entorno.md) |
