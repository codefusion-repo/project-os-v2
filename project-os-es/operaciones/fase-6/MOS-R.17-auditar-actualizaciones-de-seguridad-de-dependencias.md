# MOS-R.17 — Auditar actualizaciones de seguridad de dependencias

Operación MOSDLC `dependency-security-update-audit` · Fase 6 — Mantenimiento y mejoras · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (auditoría read-only)

**Hace:** Audita dependencias y actualizaciones de seguridad pendientes.
**Para:** Reducir riesgo de dependencias sin ejecutar upgrades a ciegas.
**Cómo:** Lee manifests, lockfiles y advisories; clasifica severidad y propone ruta priorizada.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- No ejecutes upgrades, installs, pins ni ediciones de manifests.
- Redacta credenciales o valores con pinta de secreto como `[REDACTED]`; reporta ruta, variable y tipo de riesgo.

**Entrega:** output.status_result. Ante manifests o advisories ilegibles: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-6.1 o mantenimiento. Después: MOS-3.8 para upgrades priorizados; MOS-3.3 para follow-ups no urgentes. Recomendada: MOS-3.8 para findings prioritarios.
