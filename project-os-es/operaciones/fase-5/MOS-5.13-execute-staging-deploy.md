# MOS-5.13 — Ejecutar el despliegue staging (interno)

Operación MOSDLC `execute-staging-deploy` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: terminal_agent
- Kernel: workflow.deployment · mode.delegated_deploy_execution · output.execution_report
- Evidencia: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.deployment_readiness, evidence.validation_output, evidence.repo_state
- Aprobación PM: Sí (exacta por target, entorno y acción; nunca implícita)

**Hace:** Ejecuta el despliegue en staging por terminal agent solo si el target lo soporta.
**Para:** Desplegar staging interno sin fricción cuando es seguro.
**Cómo:** Ejecuta solo comandos target-owned bajo aprobación exacta y reporta redactado.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Ejecuta solo los comandos target-owned aprobados para el entorno staging, un entorno a la vez; nunca inventes, adivines ni amplíes comandos de despliegue.
- Exige aprobación PM exacta por target, entorno y acción antes de cada comando; si falta comando target-owned, aprobación, readiness, adopción o validación: fail-closed a `status.blocked`.
- Redacta valores sensibles como `[REDACTED]`; no pidas secretos, no vuelques el entorno (`env`, `printenv`, `set`) y no declares éxito sin validación post-deploy.
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Internal-only (uso CodeFusion): esta operación debe removerse, ocultarse, deshabilitarse o convertirse antes de cualquier release público de Project OS.

**Entrega:** output.execution_report. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-5.12. Después: MOS-R.13. Recomendada: MOS-R.13.
