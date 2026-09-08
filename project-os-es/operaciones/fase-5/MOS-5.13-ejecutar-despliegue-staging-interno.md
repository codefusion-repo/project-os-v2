# MOS-5.13 — Ejecutar el despliegue staging (interno)

Operación MOSDLC `execute-staging-deploy` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: terminal_agent
- Kernel: workflow.deployment · mode.delegated_deploy_execution · output.execution_report
- Evidencia: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.deployment_readiness, evidence.validation_output, evidence.repo_state, evidence.exact_ref
- Aprobación PM: Sí (exacta por target, entorno y acción; nunca implícita)

**Hace:** Ejecuta el despliegue en staging por terminal agent solo si el target lo soporta.
**Para:** Desplegar staging interno sin fricción cuando es seguro.
**Cómo:** Reconstruye la misma unidad y consume la evidencia de MOS-R.11/
MOS-R.12 para `staging` según la continuidad del contrato común.
Antes de ejecutar, revalida ref exacta, estado/preflight, adopción,
readiness, validación y aprobación exacta de target/entorno/acción/ref
bajo el workflow y mode delegados resueltos. Reutiliza pruebas aún
válidas; renueva las afectadas y bloquea ante cualquier gap material.
Ejecuta solo comandos target-owned aprobados, con rollback aplicable
preparado. Verifica post-deploy por MOS-R.13 antes de reportar éxito,
incluyendo ref esperado/observado y evidencia reutilizada/renovada.
No inicia otro entorno ni ejecuta rollback por inferencia.

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
