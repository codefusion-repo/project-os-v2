# MOS-R.11 — Revisar readiness de despliegue por entorno

Operación MOSDLC `deployment-readiness-review` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis, evidence.validation_output, evidence.exact_ref
- Aprobación PM: No (readiness read-only)

**Hace:** Revisa readiness de despliegue para un `TARGET_ENVIRONMENT`.
**Para:** Unificar análisis local/staging/producción sin borrar las operaciones PM-facing por entorno.
**Cómo:** Aplica la continuidad y reutilización de evidencia del contrato común
a la unidad y el entorno objetivo reconstruidos. Verifica ref exacta,
validación aplicable, QA/disposiciones vigentes y prerrequisitos del target
(incluidos merge/release o entorno previo solo cuando sean exigidos). Revisa
adopción y `Project-specific notes` en vivo: configuración por nombres seguros,
comandos/rutas de deploy, rollback probado cuando obligatorio y checks
post-deploy propios de ese entorno. Identifica responsable y autorización de
cada acción, sin tratar el éxito anterior como readiness o permiso del siguiente.

Declara evidencia reutilizada, renovada y faltante con fuente/ref/entorno y
razón; readiness solo es suficiente si cubre todas las comprobaciones exigidas.
Si faltan pasos humanos, consume MOS-5.2, MOS-5.5 o MOS-5.8 para draftear solo
los pendientes en la misma respuesta, conservando los resultados válidos.
Si están satisfechos, consume MOS-R.12 bajo su workflow resuelto y entrega el
draft sin otro checklist, selector ni locator mecánico. La aprobación de
ejecución sigue siendo un gate separado; no ejecutes el bundle.

Falta de ref, validación, comandos, evidencia de entorno o rollback obligatorio
impide declarar readiness y entregar comandos de ejecución. No inventes rutas
ni amplíes autoridad para resolver configuración; informa el faltante exacto y
la siguiente acción segura.

**Variables**
- Requeridas: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia faltante, entorno inexistente o decisión PM requerida: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: QA/release o verificación del entorno previo cuando el target lo exige; MOS-5.1/5.4/5.7 delegan esta revisión. Después: MOS-R.12 si hay readiness; checklist del entorno solo para comprobaciones humanas pendientes. Recomendada: entregar la siguiente salida segura en la misma respuesta.
