# MOS-3.5 — Draftear el route prompt de corrección

Operación MOSDLC `draft-correction-route-prompt` · Fase 3 — Implementación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (el route-prompt no autoriza; la escritura exige aprobación PM exacta)

**Hace:** Draftea el route-prompt de corrección de una unidad viva desde
findings con disposición `blocking-correction`.
**Para:** Corregir solo incumplimientos materiales sin expandir el scope original.
**Cómo:** Encapsula únicamente los findings `blocking-correction` en una ruta de
corrección delegada; los `non-blocking-follow-up` se difieren a MOS-3.3 y
`preference`, `accepted-risk` e `invalid-finding` no fuerzan cambios. Los inputs
humanos son `WORK_UNIT`, `OPTIONAL_SKILL`, feedback o preguntas del PM, el
override explícito `/hydration` y la autorización exacta aplicable; no son
metadata derivada ni autorizan nada. El resto de la metadata se reconstruye desde
la evidencia viva y se muestra resuelta para inspección, no se vuelve a pedir.
Browser chat lee la unidad viva y sus relaciones, localiza el PR
existente cuando aplique, lee su conversación completa, selecciona el último review
vigente (técnico o QA humano) con `blocking-correction` sin resolver e incorpora
sus addenda PM posteriores como parte del mismo source basis, reconstruye o conserva la
`CHANGE_CLASS` de la unidad. Con esos valores resueltos completa `WORK_UNIT`,
`SOURCE_REVIEW`, `PR_NUMBER` y `CHANGE_CLASS` en el route-prompt
para que el receptor terminal verifique el contrato; nunca los inventa. Cuando
existe un único review vigente con `blocking-correction` sin resolver, lo selecciona
automáticamente; solo devuelve `status.needs_pm_decision` o `status.needs_context`
ante ambigüedad material real —dos reviews incompatibles igualmente vigentes,
relación unidad↔PR no verificable, comentarios materialmente truncados, evidencia
insuficiente para determinar la clase o contradicción real entre el review y una
decisión PM posterior—, nunca porque el PM no haya reescrito un ID, una clase o un
nivel reconstruibles. El route-prompt exige que el agente ejecutor publique
exactamente un correction report append-only en ese PR que referencie el review
fuente, registre el head anterior y el corregido, mapee cada `blocking-correction`
con su resultado, identifique commits o rango y la validación real, declare el
trabajo restante y confirme que no hubo merge ni cierre, sin editar el body ni
ningún comentario previo. Los findings se transportan por intención: el
incumplimiento material y su criterio observable son vinculantes; la redacción y
las propuestas de solución del reviewer son advisory. El browser chat puede
recomendar un skill opcional e infiere `RECOMMENDED_TERMINAL_AGENT_FAMILY` según el
trabajo. La recomendación es advisory, no autoriza nada y el feedback explícito del
PM puede reemplazarla.

La corrección conserva la unidad primaria, PR, rama existente, clase y scope
originales; no crea issue ni PR de corrección. Una fuente QA se procesa con este
mismo contrato: reconstruye desde `QA_RESULT` la relación con `WORK_UNIT` y el
PR y usa `SOURCE_REVIEW` para referenciar el review humano o comentario QA exacto
que contiene los `blocking-correction` vigentes. Lee también los reviews y
addenda aplicables; no sustituyas un blocking vigente por otro ni inventes un
review técnico para aceptar QA. Fuente insuficiente o conflicto material falla
cerrado. No fuerces un PR si la clase y política del target admiten la unidad sin
él; conserva en su registro equivalente la fuente y validación, sin inferir
permiso para publicarlas. Toda corrección del PR vuelve a MOS-3.7 sobre el head
corregido, con el correction report append-only exigido arriba. La autorización
exacta y la forma compacta se verifican como en MOS-3.4; compartir unidad no
reutiliza automáticamente un grant anterior.

**Variables**
- Requeridas: WORK_UNIT
- Opcionales: OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el skill, el
  feedback y la pregunta del PM son inputs humanos opcionales; nunca autorizan
  nada)

**Metadata derivada:** `SOURCE_REVIEW`, `PR_NUMBER` y `CHANGE_CLASS` no son inputs
manuales del wizard ni campos que el PM copie desde
GitHub: browser chat los reconstruye desde la evidencia viva y los muestra
resueltos en el route-prompt para verificación del receptor. `HYDRATION_LEVEL` no
se deriva de la `CHANGE_CLASS`: el resolver aplica `compact` por defecto para
cualquier clase, así que sin override la variable se omite; controla solo el
contenido hidratado del resolver y ningún nivel cambia gates, densidad del
reporte ni autoridad. El wizard captura los inputs humanos declarados y asiste
`PM_AUTHORIZATION_STATUS`; no solicita `SOURCE_REVIEW`, `PR_NUMBER`,
`CHANGE_CLASS` ni la hidratación cuando pueden derivarse u omitirse. Igual que en
MOS-3.4, la hidratación conserva una única ruta de override explícito
—`/hydration <nivel>` en
el wizard, escrito como `HYDRATION_LEVEL` en el bloque INPUT— que puede elegir
cualquiera de los tres niveles y que no se pregunta de forma rutinaria.

**Recomendación inferida:** `RECOMMENDED_TERMINAL_AGENT_FAMILY` es consejo de
browser chat basado en el trabajo; se muestra para inspección, no se solicita al
PM y nunca autoriza una herramienta o acción.

**Entrega:** output.route_prompt. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-3.7, MOS-3.25 o MOS-4.4, solo con findings
`blocking-correction`. Después: MOS-3.7. Recomendada: MOS-3.7.
