# MOS-1.7 — Revisar la viabilidad de una idea

Operación MOSDLC `review-idea-feasibility` · Fase 1 — Requerimientos, planificación y viabilidad · Riesgo: low.
Contrato común: `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed, secretos).

- Superficie: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidencia: evidence.repo_state
- Aprobación PM: No (read-only)

**Hace:** Evalúa una idea nueva y elige su ruta proporcional al riesgo.
**Para:** Decidir qué hacer con la idea: implementarla directamente, partirla en
slices, investigarla o prototiparla, registrarla como decisión durable,
actualizar solo el roadmap, o rechazarla o diferirla.
**Cómo:** Analiza la idea contra estado vivo y documentación y recomienda una
de esas rutas según riesgo y concreción; una idea concreta y acotada puede
derivar directamente a implementación sin pasar por documentación ni roadmap.

**Variables**
- Requeridas: IDEA
- Opcionales: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (el feedback y la pregunta del PM son contexto humano; nunca autorizan nada)

**Entrega:** output.status_result. Ante evidencia, alcance o aprobación faltante o ambigua: fail-closed — informa con output.status_result y devuelve la decisión al PM.

**Conexiones:** Antes: cualquier fase. Después: la ruta elegida — MOS-3.8 o
MOS-3.4 para implementar, MOS-3.2 para slices, MOS-R.1 para una decisión
durable, MOS-1.12 para solo roadmap, MOS-1.8 únicamente si docs o roadmap
quedaron obsoletos, o ninguna si se rechaza o difiere. Recomendada: la ruta
proporcional elegida.
