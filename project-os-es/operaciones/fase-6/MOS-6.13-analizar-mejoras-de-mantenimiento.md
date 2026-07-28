# MOS-6.13 — Analizar mejoras de mantenimiento

<!-- project-os-operation
shared_contract: maintenance-analysis
-->

**Compatibilidad:** MOS-6.3, MOS-6.4 y MOS-6.5 conservan sus entrypoints históricos y resuelven este único contrato con su foco ligado.
**Contrato común:** `project-os-es/operaciones/README.md` (resolución de kernel, estado vivo, validación, no-autorización, fail-closed y secretos).

**Hace:** Analiza y recomienda mejoras de mantenimiento para un único foco.
**Para:** Priorizar mejoras fundamentadas sin mezclar rendimiento, producto y calidad de código.
**Cómo:** Análisis read-only de `FOCUS_AREA`, entregado como hallazgos con referencia,
disposición verificable, recomendación, riesgos y áreas no revisadas. Un foco ausente,
inválido o materialmente ambiguo falla cerrado con `output.status_result`.

**Entrega y límites:** La entrega incluye hallazgos y un resultado de estado; ante evidencia, alcance o aprobación faltante o ambigua, falla cerrado y devuelve la decisión al PM.
