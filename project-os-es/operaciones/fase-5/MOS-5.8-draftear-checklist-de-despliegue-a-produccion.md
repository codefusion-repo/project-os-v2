# MOS-5.8 — Draftear el checklist de despliegue a producción

Operación MOSDLC `draft-production-deploy-checklist` · Fase 5 — Despliegue local / staging / producción · Riesgo: medium.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result
- Evidencia: evidence.repo_state, evidence.target_adoption, evidence.source_basis
- Aprobación PM: No (draft-only; el Humano PM decide y ejecuta el bundle)

**Hace:** Draftea el checklist humano de despliegue de producción nombrando variables y pasos, nunca valores secretos.
**Para:** Guiar los pasos humanos del despliegue de producción.
**Cómo:** Consume los gaps humanos de MOS-R.11 para la misma unidad, ref y
entorno `production`. Conserva resultados aún válidos con sus fuentes y
draftea solo comprobaciones pendientes o que requieren renovación; nunca
omite QA o aceptación humana exigidos. Nombra variables, nunca secretos.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Cuida**
- Postura de seguridad estricta: describe superficies sensibles solo por nombre de variable, comando, ruta o tipo de riesgo; nunca expongas secretos, valores de `.env`, tokens ni credenciales.
- Depende de las `Project-specific notes` del adapter del target: usa solo comandos y rutas target-owned documentados ahí; si faltan o son ambiguos, fail-closed.

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-5.7. Después: MOS-5.9. Recomendada: MOS-5.9.
