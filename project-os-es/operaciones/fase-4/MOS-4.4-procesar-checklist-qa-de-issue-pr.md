# MOS-4.4 — Procesar el checklist QA de un issue/PR

Operación MOSDLC `process-qa-checklist-issue-pr` · Fase 4 — QA y verificación humana · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidencia: evidence.source_basis, evidence.repo_state
- Aprobación PM: No (draft-only)

**Hace:** Procesa el resultado del checklist humano de issue/PR.
**Para:** Convertir QA humano en corrección, follow-up o avance.
**Cómo:** Aplica el gate de materialidad y las disposiciones de MOS-3.7 al
resultado QA de la misma unidad: `blocking-correction` consume MOS-3.5;
`non-blocking-follow-up` consume MOS-3.3, con agrupación e independencia;
`preference`, `accepted-risk` e `invalid-finding` no crean trabajo. Entrega la
salida canónica aplicable en la misma respuesta sin otra selección ni locator.
No ejecutes mutaciones. QA requerido pendiente o fallido impide GO; QA
satisfecho permite volver a MOS-3.7 con su evidencia, sin crear unidad ni
sustituir review o autorización de closeout.

Entrega esa evidencia con criterios/disposiciones, ref y entorno cubiertos y
lo reutilizado o pendiente de renovar según el contrato común. Cuando el
outcome incluye release o deployment, reconstruye su siguiente gate: MOS-3.7
si falta review, MOS-3.10 tras merge verificado si requiere release, o MOS-R.11
para el entorno objetivo cuando sus prerrequisitos estén satisfechos. Compón
la siguiente salida segura con su kernel resuelto sin otro selector ni locator;
QA PASS no autoriza merge, Release ni ningún entorno.

**Variables**
- Requeridas: QA_RESULT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Metadata derivada:** el issue o unidad relacionada, el PR, la rama y las
demás relaciones verificables se reconstruyen desde `QA_RESULT` y se muestran
resueltas en la salida para que el receptor las verifique; no son inputs
manuales ni campos que el PM copie desde GitHub, y nunca se inventan. Solo una
ambigüedad material real —varias fuentes incompatibles igualmente vigentes o
una relación no verificable— devuelve `status.needs_context` o
`status.needs_pm_decision`; que el PM no haya reescrito un identificador
reconstruible nunca falla cerrado.

**Entrega:** output.status_result (+output.route_prompt, output.pm_command_bundle). Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.1. Después: MOS-3.5 para blocking-correction, MOS-3.3 para follow-up, MOS-3.7 si falta review, MOS-3.10 si corresponde release tras merge o MOS-R.11 para el entorno pendiente. MOS-4.8/MOS-4.7 conservan entradas QA compatibles. Recomendada: siguiente salida segura de la misma unidad.
