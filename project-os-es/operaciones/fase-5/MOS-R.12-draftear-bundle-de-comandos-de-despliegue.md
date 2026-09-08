# MOS-R.12 — Draftear bundle de comandos de despliegue

Operación MOSDLC `draft-deploy-command-bundle` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis, evidence.deployment_readiness, evidence.validation_output, evidence.exact_ref
- Aprobación PM: No para draftear; ejecución exige aprobación exacta por target, entorno y acción

**Hace:** Draftea un bundle copy-safe de comandos de despliegue para un entorno.
**Para:** Unificar drafteo por entorno sin perder claridad PM.
**Cómo:** Consume readiness suficiente de MOS-R.11 para la misma unidad,
target, ref exacta y entorno. Una entrada directa reconstruye esa evidencia;
no exige volver a invocar readiness si sigue vigente. Aplica la reutilización
del contrato común y la forma de `project-os-es/templates/pm-command-bundle.md`:
comandos target-owned revisados, gate/responsable, evidencia renovada/reutilizada,
riesgo, rollback y postcondiciones fuera de los bloques ejecutables.

El draft identifica aprobación exacta vigente o pendiente para ese target,
entorno, acción y ref; no confunde capacidad del target ni readiness con permiso.
No junta configuración, release, varios entornos o rollback como una cadena
ejecutable con gates pendientes. Si falta evidencia material, falla cerrado.
Local/staging pueden pasar a MOS-5.11/MOS-5.13 solo bajo la autorización y
resolución delegadas propias; producción queda en MOS-5.15 para Humano PM.
MOS-5.10/5.12/5.14 son entradas que delegan aquí; no las reinvoques desde este bundle.
La siguiente verificación MOS-R.13 conserva la unidad y se exige tras ejecutar.

**Variables**
- Requeridas: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- No inventes comandos ni ejecutes el bundle; el Humano PM decide y ejecuta.
- Redacta secretos como `[REDACTED]`; no pidas valores ni vuelques entorno/config.
- Internal-only/pre-release-convert: remover, ocultar, deshabilitar o convertir antes de cualquier release público del catálogo operativo.

**Entrega:** output.pm_command_bundle. Ante comandos target-owned faltantes, ambiguos o secret-sensitive sin redacción: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.11. Después: ejecución PM del bundle o la operación de ejecución del entorno con aprobación exacta; luego MOS-R.13. Recomendada: MOS-R.13 tras ejecutar.
