# MOS-5.15 — Despliegue a producción (Humano PM)

Operación MOSDLC `execute-production-deploy` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: human_pm
- Kernel: workflow y mode siguen como candidatos, no aplicados (producción no se ejecuta por agente; Humano PM por defecto) · output.execution_report
- Evidencia: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.deployment_readiness, evidence.validation_output, evidence.repo_state, evidence.exact_ref
- Aprobación PM: Sí (exacta por target, entorno y acción; nunca implícita)

**Hace:** El Humano PM ejecuta el despliegue de producción preparado en MOS-5.14.
**Para:** Completar el mismo outcome en producción bajo control humano.
**Cómo:** El PM verifica target, ref exacta, readiness de producción, checks
humanos requeridos, validación, rollback y aprobación exacta de esa acción antes
de ejecutar comandos target-owned. Conserva la unidad y evidencia aplicable
según el contrato común; staging PASS y su aprobación no satisfacen el gate
productivo. El agente solo prepara evidencia/drafts o verifica read-only bajo
los workflows existentes; no ejecuta producción aunque el target tenga comandos.
El resultado humano se contrasta con MOS-R.13 antes de declarar éxito.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Producción queda con el Humano PM por defecto: el agente no ejecuta esta operación; solo el Humano PM corre los comandos drafteados en MOS-5.14.
- Workflow y mode siguen siendo candidatos de kernel (ver el mapa MOSDLC): no apliques ids de kernel nuevos sin gap estricto probado y aprobación PM exacta separada.
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Internal-only (uso CodeFusion): esta operación debe removerse, ocultarse, deshabilitarse o convertirse antes de cualquier release público de Project OS.

**Entrega:** output.execution_report. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-5.14. Después: MOS-R.13. Recomendada: MOS-R.13.
