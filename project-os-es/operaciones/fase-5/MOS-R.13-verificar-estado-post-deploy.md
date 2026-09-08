# MOS-R.13 — Verificar estado post-deploy

Operación MOSDLC `verify-post-deploy-state` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.validation_output, evidence.exact_ref
- Aprobación PM: No (verificación read-only)

**Hace:** Verifica el estado post-deploy del entorno objetivo.
**Para:** Confirmar que el despliegue quedó saludable con evidencia de salud o smoke.
**Cómo:** Reconstruye unidad, target, entorno, ref esperado y ref realmente
desplegado desde fuentes verificables; compara identidad y postcondiciones con
readiness y el resultado de ejecución. Usa solo checks read-only target-owned
del despliegue actual, con fuente, alcance y resultados redactados. Exit code
exitoso, QA previo o salud de otro entorno no prueban éxito post-deploy.
Ref discrepante o checks fallidos bloquean; evidencia ilegible no es PASS.
Entrega el resultado a MOS-R.14 sin recaptura y sin iniciar otro entorno;
cuando MOS-R.16 consume esta comprobación para un rollback, devuelve allí la
evidencia de recuperación en vez de reiniciar el procesamiento de deployment.

**Variables**
- Requeridas: TARGET_ENVIRONMENT
- Opcionales: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Falla cerrado si el target no tiene ese entorno o checks target-owned.
- Reporta endpoints por nombre, check names y resultados; nunca valores de entorno, tokens ni connection strings.
- No redespliegues, reinicies servicios, edites config ni ejecutes correcciones.

**Entrega:** output.status_result. Ante checks ilegibles: `status.needs_context`; ante deploy no saludable: `status.blocked`.

**Conexiones:** Antes: MOS-5.11, MOS-5.13, ejecución PM de MOS-R.12 o despliegue aprobado. Después: MOS-R.14. Recomendada: MOS-R.14.
