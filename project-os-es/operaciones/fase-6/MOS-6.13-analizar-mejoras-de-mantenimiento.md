# MOS-6.13 — Analizar mejoras de mantenimiento

<!-- project-os-operation
shared_contract: maintenance-analysis
-->

**Hace:** Analiza y recomienda mejoras de mantenimiento para un único foco.
**Para:** Priorizar mejoras fundamentadas sin mezclar rendimiento, producto y calidad de código.
**Cómo:** Análisis read-only de `FOCUS_AREA`, entregado como hallazgos con referencia,
disposición verificable, recomendación, riesgos y áreas no revisadas. Un foco ausente,
inválido o materialmente ambiguo falla cerrado con `output.status_result`.
