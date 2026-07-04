# MOS-R.18 — Auditar configuración de forma segura para secretos

Operación MOSDLC `secret-safe-config-audit` · Fase 6 — Mantenimiento y mejoras · Riesgo: high.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (auditoría read-only y redactada por diseño)

**Hace:** Audita riesgos de entorno/config sin exponer secretos.
**Para:** Detectar configuración insegura, defaults riesgosos o secretos comprometidos sin copiar valores.
**Cómo:** Revisa superficies de configuración del repo y reporta solo ruta, nombre de variable y tipo de riesgo.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Nunca abras, pegues, resumas ni reconstruyas valores secretos; usa siempre `[REDACTED]`.
- No ejecutes `env`, `printenv`, `set`, dumps de framework ni contextos de secretos CI.
- No rotes claves, no edites config, no modifiques secret stores ni toques secretos de despliegue.

**Entrega:** output.status_result. Ante superficies ilegibles: `status.needs_context`; ante secreto vivo expuesto: `status.blocked`.

**Conexiones:** Antes: MOS-6.1 o auditoría de mantenimiento. Después: MOS-3.3 por riesgo detectado. Recomendada: MOS-3.3.
