# MOS-R.15 — Draftear comandos de rollback

Operación MOSDLC `draft-rollback-commands` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No para draftear; rollback exige aprobación exacta por target, entorno y acción

**Hace:** Draftea comandos o ruta de rollback para un despliegue fallido.
**Para:** Volver a un estado seguro sin improvisar bajo presión.
**Cómo:** Usa solo rutas de rollback target-owned y conserva advertencias fuera de bloques ejecutables.

**Variables**
- Requeridas: TARGET_REPOSITORY, TARGET_ENVIRONMENT
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- No inventes comandos ni ejecutes rollback; si la ruta es faltante, conflictiva, no probada o ambigua, fail-closed.
- Redacta secretos; nunca imprimas valores de entorno ni pidas credenciales.
- Internal-only/pre-release-convert: remover, ocultar, deshabilitar o convertir antes de cualquier release público del catálogo operativo.

**Entrega:** output.pm_command_bundle. Ante rutas de rollback insuficientes o aprobación faltante para ejecución: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-R.14 con rollback elegido. Después: ejecución PM del bundle; luego MOS-R.16. Recomendada: MOS-R.16 tras ejecutar.
