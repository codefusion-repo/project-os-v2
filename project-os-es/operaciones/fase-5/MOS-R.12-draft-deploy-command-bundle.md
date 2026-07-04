# MOS-R.12 — Draftear bundle de comandos de despliegue

Operación MOSDLC `draft-deploy-command-bundle` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No para draftear; ejecución exige aprobación exacta por target, entorno y acción

**Hace:** Draftea un bundle copy-safe de comandos de despliegue para un entorno.
**Para:** Unificar drafteo por entorno sin perder claridad PM.
**Cómo:** Usa solo comandos target-owned y mantiene riesgo, rollback y verificación fuera de bloques ejecutables.

**Variables**
- Requeridas: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- No inventes comandos ni ejecutes el bundle; el Humano PM decide y ejecuta.
- Redacta secretos como `[REDACTED]`; no pidas valores ni vuelques entorno/config.
- Internal-only/pre-release-convert: remover, ocultar, deshabilitar o convertir antes de cualquier release público del catálogo operativo.

**Entrega:** output.pm_command_bundle. Ante comandos target-owned faltantes, ambiguos o secret-sensitive sin redacción: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.11. Después: ejecución PM del bundle o la operación de ejecución del entorno con aprobación exacta; luego MOS-R.13. Recomendada: MOS-R.13 tras ejecutar.
