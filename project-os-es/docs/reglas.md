# Reglas: verdad, permisos y seguridad

**Estas son las reglas que nunca se negocian. Si una operación y una regla
chocan, gana la regla y el sistema se detiene (fail-closed).**

## Fuentes de verdad

Cada tipo de información tiene exactamente un dueño:

- **Estado vivo → GitHub.** Issues, PRs, comentarios, reviews, ramas, commits
  y evidencia de validación se reconstruyen desde GitHub y git al momento de
  la tarea. La memoria del chat, los reportes previos y los archivos durables
  no son evidencia: son claims hasta verificarlos.
- **Comportamiento estable → kernel español.** `project-os-es/kernel/*.json`
  define actores, modos, workflows, límites, evidencia, salidas y estados para
  esta superficie, y se resuelve vía `project-os-es/kernel/manifest.json` antes
  de trabajo no trivial.
- **Verdad del producto → repo target.** Dominio, runtime, build y validación
  del target viven en el target, nunca en el kernel.
- **Decisiones que sobreviven a un issue → ADRs** en `docs/decisions/` del
  repo dueño de la decisión. **Qué sigue y por qué → un único roadmap issue
  canónico** por proyecto, que se supersede, no se muta.

Dos prohibiciones protegen esto: **nada de estado vivo en archivos durables**
(ni números de issue/PR como estado, ni SHAs, ni readiness) y **nada de estado
inventado** (lo que no se puede leer en vivo, falta; se reporta como faltante).

## Permisos: el texto nunca autoriza

Ningún doc, template, prompt, adapter ni salida de resolver otorga permiso
(`boundary.output_not_permission`). La escritura del terminal agent exige
estas cinco condiciones, todas a la vez:

1. aprobación PM exacta que nombra repo, issue/PR y acción aprobada;
2. el modo de ejecución correcto resuelto del kernel;
3. branch preflight real (rama, worktree y HEAD capturados antes de editar);
4. trabajo en rama `work/<issue>-<slug>`, nunca directo a main;
5. validación proporcional con resultados reales.

Merge, cierre, labels, tags, releases, settings y producción quedan con el
Humano PM salvo aprobación separada y exacta. Ante kernel faltante, evidencia
faltante, autoridad ambigua o validación fallida: detenerse y devolver
`status.needs_context`, `status.needs_pm_decision` o `status.blocked`.

Los skills opcionales tampoco autorizan. Solo describen una capacidad o metodo
que el agente puede aplicar si el PM lo pide o un route prompt lo recomienda;
no cambian workflow, mode, scope, preflight, validacion ni review-before-close.

## Trazabilidad: todo se puede reconstruir en frío

Cualquier agente debe poder retomar el proyecto solo desde GitHub:

- Cada **issue** carga su propio contexto: por qué existe, objetivo, base
  fuente, scope, fuera de scope, criterios de aceptación y validación.
- Cada **PR** documenta su propia verificación: resumen, límites, comandos de
  validación con resultados y notas de seguridad.
- Cada **cierre** deja un paquete de reconstrucción: evidencia de completitud
  y validación, límites preservados y referencias de commit/PR.
- Las ramas `work/<issue>-<slug>` atan el código a su issue.

## Validación proporcional

La validación es evidencia para el riesgo del cambio, no un ritual. Clasifica
siempre en una de cuatro categorías: **agent-run requerida** (obligatoria si
el cambio toca kernel, resolver, comandos, autorización, trazabilidad,
seguridad, secretos, deploy o contratos deterministas), **comandos PM-run
drafteados**, **validación manual PM** (claridad de docs, wording, UX) o
**sin validación automatizada, con justificación**. Nunca se asume full suite
ni tests nuevos por defecto; esta superficie usa este resumen y
`project-os-es/kernel/reglas-operativas.json` como ruta operativa.

## Economía de contexto

El costo en tokens y subagentes se mantiene proporcional a la tarea, pero la
economía está subordinada a la seguridad: ningún atajo elimina un gate. Lee el
estado vivo en vez de pegarlo; cita ubicaciones (`issue #`, `archivo:línea`)
en vez de repetir cuerpos completos; usa subagentes solo con razón acotada y
verifica su salida contra evidencia viva. El detalle operativo de esta
superficie vive en `project-os-es/kernel/reglas-operativas.json`.

## Secretos

Prohibido imprimir, pegar, commitear, citar o resumir secretos: `.env`,
tokens, credenciales, cookies, JWTs, URLs de base de datos, claves privadas,
llaves de pago o cualquier valor con pinta de secreto — incluso en tests,
logs, PRs y reportes. Se redacta como `[REDACTED]` reportando solo nombre de
variable, ruta y tipo de riesgo. Nada de dumps amplios de entorno (`env`,
`printenv`, `set`) sin diagnóstico redactado y acotado por el PM.

## Evolución planificada: materialidad de evidencia y degradación segura

**Esta sección documenta un requerimiento planificado, no comportamiento
implementado.** Mientras esta evolución no exista en el kernel, el
comportamiento vigente descrito arriba permanece sin cambios: ante evidencia
requerida faltante o ambigua, el sistema se detiene fail-closed.

**Objetivo.** Distinguir en una evolución futura la evidencia que sostiene un
hard gate de la evidencia auxiliar de contexto, para que la indisponibilidad
parcial de esta última pueda degradar de forma segura, explícita y trazable en
vez de forzar siempre un bloqueo total, sin debilitar ningún gate material.

- **Hard gates vs. evidencia auxiliar (distinción futura).** La aprobación PM
  exacta, el branch preflight, la validación requerida, la identidad del
  target, la SHA/ref exacta y la seguridad de secretos seguirán fallando
  cerrado sin excepción. La distinción planificada aplicaría únicamente a
  evidencia auxiliar de contexto, nunca a un hard gate.
- **Fuentes equivalentes.** Cuando la fuente primaria de una evidencia
  auxiliar no esté disponible, una fuente equivalente verificable podría
  satisfacer el mismo requerimiento, registrando qué fuente se usó y por qué.
- **Fallos de conectores.** Un fallo de conector, API o red al leer evidencia
  auxiliar debería degradar de forma explícita, nunca silenciosa: el resultado
  nombra qué no pudo leerse y confirma qué gates permanecen intactos.
- **Drafts con revalidación diferida.** Un draft podría avanzar con evidencia
  auxiliar incompleta solo si queda marcado para revalidación diferida, y esa
  revalidación debe completarse antes de cualquier acción material.
- **Gaps explícitos.** Toda degradación deja gaps nombrados y visibles en el
  output correspondiente, dentro de los estados existentes del kernel; nunca
  se declara completitud ocultando un gap.

**Criterios de aceptación para la implementación futura:**

1. Ningún hard gate vigente se debilita ni se vuelve degradable.
2. La clasificación material/auxiliar de cada evidencia queda definida en el
   kernel de forma determinista y protegida por tests.
3. Toda degradación es explícita, trazable y revalidable; los fallos
   silenciosos siguen prohibidos.
4. Hasta que exista esa implementación aprobada, el fail-closed total vigente
   se conserva íntegro.

## Siguiente paso

Con las reglas claras, opera el ciclo día a día con [ritmo.md](ritmo.md).
