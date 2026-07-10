# MOS-0.5 — Verificar la adopción del target

Operación MOSDLC `verify-target-adoption` · Fase 0 — Adaptación · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat / terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.status_result
- Evidencia: evidence.target_adoption
- Aprobación PM: No (read-only)

**Hace:** Audita read-only que la adopción del target existe, es correcta y apunta al kernel actual.
**Para:** Confirmar que el target puede operar con seguridad.
**Cómo:** Lee adapters y evidencia del target sin escribir nada.

**Variables**
- Requeridas: TARGET_REPOSITORY
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: MOS-0.2, MOS-0.3 o MOS-0.4. Después: MOS-1.1 o MOS-1.10 según el proyecto. Recomendada: MOS-R.2.
