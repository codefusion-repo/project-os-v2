# MOS-5.1 — Analizar readiness de despliegue local

Operación MOSDLC `analyze-local-deploy-readiness` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `../README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No (read-only)

**Hace:** Analiza readiness y configuración necesaria del despliegue local.
**Para:** Preparar un despliegue local seguro y reproducible.
**Cómo:** Analiza read-only desde target notes y repo; toda configuración con escritura va por ruta delegada aprobada.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Depende de las `Project-specific notes` del adapter del target: usa solo comandos y rutas target-owned documentados ahí; si faltan o son ambiguos, fail-closed.

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-4.6. Después: MOS-5.2, MOS-5.10. Recomendada: MOS-5.2.
