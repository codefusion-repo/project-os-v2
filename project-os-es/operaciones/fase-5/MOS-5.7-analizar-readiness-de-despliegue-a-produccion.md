# MOS-5.7 — Analizar readiness de despliegue a producción

Operación MOSDLC `analyze-production-deploy-readiness` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No (read-only)

**Hace:** Analiza readiness y configuración necesaria del despliegue de producción.
**Para:** Preparar un despliegue de producción seguro y reproducible.
**Cómo:** Delega la revisión en MOS-R.11 con `TARGET_ENVIRONMENT=production`
y las relaciones vivas ya reconstruidas; aplica su evidencia y gates.
Solo comprobaciones humanas pendientes consumen MOS-5.8; readiness
suficiente consume MOS-5.14 en la misma respuesta, sin recaptura.
Toda configuración con escritura conserva su aprobación y límites propios.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Depende de las `Project-specific notes` del adapter del target: usa solo comandos y rutas target-owned documentados ahí; si faltan o son ambiguos, fail-closed.

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: QA/release o entorno previo si el target lo exige. Después: MOS-5.8 solo para checks humanos pendientes; MOS-5.14 con readiness suficiente. Recomendada: la salida segura resuelta por MOS-R.11, sin otra selección.
