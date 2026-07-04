# MOS-5.15 — Despliegue a producción (Humano PM)

Operación MOSDLC `execute-production-deploy` · Fase 5 — Despliegue local / staging / producción · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: terminal_agent
- Kernel: workflow y mode siguen como candidatos, no aplicados (producción no se ejecuta por agente; Humano PM por defecto) · output.execution_report
- Evidencia: evidence.pm_approval, evidence.source_basis, evidence.target_adoption, evidence.validation_output, evidence.repo_state
- Aprobación PM: Sí (exacta por target, entorno y acción; nunca implícita)

**Hace:** Ejecuta el despliegue en producción por terminal agent solo si el target lo soporta.
**Para:** Cubrir el caso interno donde el PM delega producción explícitamente.
**Cómo:** Ejecuta solo comandos target-owned bajo aprobación exacta y reporta redactado; por defecto producción queda con el Humano PM.

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
