# MOS-R.2 — Recomendar la siguiente operación

Operación MOSDLC `recommend-next-operation` · Transversal · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (routing read-only; no autoriza la operación seleccionada)

**Hace:** Recomienda exactamente una siguiente operación MOSDLC desde trazabilidad viva.
**Para:** Elegir ruta de ciclo de vida sin razonamiento ad hoc.
**Cómo:** Lee estado vivo, justifica la recomendación y muestra alternativas seguras si hay ambigüedad.

**Variables**
- Requeridas: ninguna
- Opcionales: ROUTING_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** el repositorio, el issue, el PR, el roadmap y el estado
actual son metadata derivada, no inputs. Aplica la precedencia del contrato
común: reutiliza la fuente inequívoca que la invocación actual ya identifica;
si falta, pide un único `ROUTING_SOURCE` —repositorio, issue, PR, roadmap o
registro vivo equivalente— y reconstruye el resto desde él. Devuelve la
decisión al PM solo ante ambigüedad material real, nunca porque falte un
identificador reconstruible.

**Entrega:** output.status_result. Ante trazabilidad insuficiente o ilegible: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Continuación intent-first:** Si el PM busca un outcome y la ruta es
inequívoca, no termines en la recomendación: re-resuelve el kernel para la
operación seleccionada, conserva sus gates de actor, workflow, mode, evidencia
y validación, abre su template y produce su siguiente salida read-only o
draft-only en la misma respuesta. Esa salida pertenece a la operación
seleccionada, no al workflow de routing. Explica brevemente la ruta dentro de
la forma permitida por su template, sin pedir otra selección MOS, confirmación
mecánica ni metadata derivable. Si el PM pide únicamente recomendar o comparar
rutas, entrega la recomendación sin continuar.

Para implementar una unidad viva suficiente, continúa a MOS-3.4. Si la clase
exige una unidad formal que aún no existe, draftea exactamente una mediante
MOS-3.1 o MOS-3.8 según su source basis y detente en la creación humana; un
draft no es una unidad formal creada. Cuando el resultado de esa creación sea
verificable, retoma MOS-3.4 con la misma intención y referencia, sin pedir el
número otra vez ni crear otra unidad. No encadenes operaciones después del
siguiente artefacto útil ni atravieses una decisión material o un límite de
superficie. Cada continuación exige la evidencia de su propia operación: un
routing resuelto no demuestra que esa evidencia esté completa.

Usa las fuentes conectadas de lectura disponibles para verificar la referencia
y sus relaciones. Si no están disponibles, aplica el contrato común de fuentes
equivalentes y fail-closed; no inventes metadata ni pidas retranscribir datos
accesibles. Conserva intención, constraints y overrides explícitos en el
contexto de la cadena, sin persistir estado. La continuación nunca crea
autorización ni ejecuta writes; MOS-3.4 conserva su entrega PM exacta.

**Conexiones:** Antes: cualquier operación que necesite routing. Después: la operación seleccionada, re-resuelta bajo sus propios gates cuando procede la continuación. Recomendada: la operación seleccionada.
