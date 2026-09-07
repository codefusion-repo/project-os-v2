# MOS-3.4 — Draftear el route prompt de implementación

Operación MOSDLC `draft-implementation-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No para draftear. Un draft no autoriza escritura; una entrega
  PM con `PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode` puede
  satisfacer la aprobación PM exacta solo para lo declarado.

**Hace:** Draftea el route-prompt para delegar la implementación de una unidad
viva a un terminal agent.
**Para:** Rutear implementación con unidad, clase, scope, modo y evidencia correctos.
**Cómo:** Usa un bootloader compacto referenciado a la unidad viva: el detalle
permanece en la unidad y sus registros (issue o PR y comentarios cuando el
target usa GitHub; change request, registro del target o instrucción PM exacta
cuando no), no en el route prompt. Los inputs humanos son `WORK_UNIT` cuando el
contexto no identifica ya la unidad, `OPTIONAL_SKILL`, feedback o preguntas del
PM, el override explícito `/hydration` y la autorización exacta aplicable; no
son metadata derivada ni autorizan nada. El resto de la metadata se reconstruye
desde la evidencia viva y se muestra resuelta para inspección, no se vuelve a
pedir.
Cuando la invocación actual ya identifica esa unidad inequívocamente —por
ejemplo la unidad identificada por MOS-R.2 o el issue creado por el Humano PM
con el bundle de MOS-3.1, MOS-3.2 o MOS-3.8 en esta sesión— no vuelvas a pedir
su locator. Un draft de issue todavía no satisface la unidad formal exigida:
verifica la creación antes de continuar. Browser chat lee la unidad y sus
relaciones, reconstruye la `CHANGE_CLASS` desde el scope, el riesgo y las
superficies afectadas según el contrato `proportionality.change_class` y
resuelve el roadmap relacionado, el PR existente cuando aplique y la rama scoped
`work/<unidad>-<slug>`. Para un `change_class.small` admitido por la política
del target, la instrucción PM exacta puede ser la unidad viva sin issue; para
una clase que exige unidad formal, resuelve la unidad viva verificable o falla
cerrado, nunca la sustituyas por metadata inventada. Al derivar `SCOPE` y
`OUT_OF_SCOPE` interpreta la unidad por intención: solo autorización, identidad,
hard constraints, scope, out of scope y seguridad son literales; ejemplos,
nombres tentativos y propuestas de implementación son advisory. El browser chat
puede recomendar un skill opcional e infiere
`RECOMMENDED_TERMINAL_AGENT_FAMILY` según el trabajo. La recomendación es
advisory, no autoriza nada y el feedback explícito del PM puede reemplazarla.

**Variables**
- Requeridas: ninguna
- Opcionales: WORK_UNIT, OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO
  (`WORK_UNIT` es el único locator primario y se pide solo cuando el contexto de
  ejecución no identifica ya la unidad viva; `OPTIONAL_SKILL`, el feedback y la
  pregunta son inputs humanos opcionales; ninguno autoriza nada)

**Metadata derivada:** `CHANGE_CLASS`, `ROADMAP_ISSUE`,
`BRANCH_NAME`, el PR existente y las demás relaciones verificables no son inputs
manuales del wizard ni campos que el PM copie desde GitHub: browser chat los
reconstruye desde la evidencia viva y los muestra resueltos en el route prompt
para verificación del receptor; nunca los inventa. La `CHANGE_CLASS` pertenece a
la unidad y se conserva en intake, implementación, review, closeout y
verificación; gobierna los gates materiales y la densidad del execution report,
nunca la hidratación del resolver. `HYDRATION_LEVEL` no se deriva de la clase:
el resolver aplica `compact` por defecto para cualquier clase, así que sin
override la variable se omite. Controla únicamente el contenido hidratado del
resolver: ningún nivel cambia gates, densidad del reporte ni autoridad. El wizard captura
los inputs humanos declarados y asiste `PM_AUTHORIZATION_STATUS`; no solicita la
clase, la hidratación, el roadmap ni la rama cuando pueden derivarse u omitirse.
La hidratación conserva una única ruta de override: una decisión PM explícita
—`/hydration <nivel>` en el wizard, que
la escribe como `HYDRATION_LEVEL` en el bloque INPUT— puede elegir cualquiera de
los tres niveles, sin ranking derivado de la clase. No es una pregunta rutinaria:
sin ese override explícito la variable no se pide ni viaja. Solo una
ambigüedad material real
—unidad formal ausente para una clase que la exige, scope que no permite
determinar la clase con confianza, relaciones no verificables o conflicto entre
la evidencia viva y una decisión PM posterior— devuelve `status.needs_context` o
`status.needs_pm_decision`.

**Recomendación inferida:** `RECOMMENDED_TERMINAL_AGENT_FAMILY` es consejo de
browser chat basado en el trabajo; se muestra para inspección, no se solicita al
PM y nunca autoriza una herramienta o acción.

**Contrato de autorización:** El browser chat solo draftea y nunca puede
autoasignar, completar, cambiar ni inferir `granted`. Un route prompt en draft,
no entregado por el PM o con `PM_AUTHORIZATION_STATUS` en `pending` no autoriza
escrituras. Cuando el PM entrega el route prompt con
`PM_AUTHORIZATION_STATUS` en `granted for this exact scope and mode`, esa entrega
satisface `evidence.pm_approval` únicamente para el repositorio, workflow,
modo, rama y scope declarados. El agente receptor debe verificar esa
coincidencia y la evidencia restante; un estado ausente, desconocido o
inferido falla cerrado. No se exige un comentario adicional de GitHub como
condición universal, y la aprobación no cubre merge, cierre, tags, releases,
deploys, settings ni otra acción fuera del modo declarado.

**Comprobación de conformidad:** Antes de entregar, compara la salida con
`project-os-es/templates/route-prompt.md`. Comprímela si repite detalle de la
unidad viva o sus registros; conserva una referencia a la evidencia viva en vez
de copiar cuerpos, acceptance criteria, source basis, checklists o pasos de
implementación. Entrega solo un bloque estándar de variables, `SCOPE` de 1-3
líneas y una única instrucción concreta posterior. Si no puede producir esa
forma, falla cerrado con `output.status_result`.

**QA manual reproducible:** Usa una unidad viva con registros extensos. Verifica
que el route prompt conserva solo metadata, referencia viva, clase y densidad
reconstruidas, scope breve, out-of-scope breve y una instrucción concreta; que
`SCOPE` tiene 1-3 líneas; que no hay secciones copiadas; que no se pidió al PM
ningún valor derivable; y que instruye al agente receptor a leer evidencia
viva.

**Entrega:** output.route_prompt. Ante evidencia, alcance, aprobación o forma conforme faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-1.7, MOS-3.1, MOS-3.2 o MOS-3.8, o una instrucción
PM exacta como unidad viva de un `change_class.small`. Después: MOS-3.7 tras el
PR. Recomendada: MOS-3.7.
