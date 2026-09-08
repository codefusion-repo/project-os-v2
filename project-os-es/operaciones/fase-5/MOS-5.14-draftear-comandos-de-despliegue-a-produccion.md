# MOS-5.14 — Draftear comandos de despliegue a producción

Operación MOSDLC `draft-production-deploy-commands` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea el bundle de comandos de despliegue de producción desde los comandos target-owned de Project-specific notes.
**Para:** Preparar la ejecución del despliegue de producción sin inventar comandos.
**Cómo:** Delega el bundle en MOS-R.12 con `TARGET_ENVIRONMENT=production`
y la evidencia vigente de la misma unidad. Consume sus gates de readiness,
ref exacta, comandos target-owned, aprobación, rollback y verificación;
entrega el draft en esta respuesta, sin otra selección ni locator.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Depende de las `Project-specific notes` del adapter del target: usa solo comandos y rutas target-owned documentados ahí; si faltan o son ambiguos, fail-closed.
- Internal-only (uso CodeFusion): esta operación debe removerse, ocultarse, deshabilitarse o convertirse antes de cualquier release público de Project OS.

**Entrega:** output.pm_command_bundle. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-5.7/MOS-R.11 o MOS-5.9 con readiness suficiente. Después: MOS-5.15, ejecución por Humano PM; luego MOS-R.13. Recomendada: gate humano exacto de producción.
