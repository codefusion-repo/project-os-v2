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

El catálogo de operaciones en español vive en
[`../operaciones/README.md`](../operaciones/README.md): un prompt compacto por
operación, organizado por fase.

## Siguiente paso

¿Primera vez? Lee [empezar.md](empezar.md). ¿Ya operando? Abre
[ritmo.md](ritmo.md) y elige la operación de tu fase.
