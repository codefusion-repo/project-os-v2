# MOS-6.13 — Analyze maintenance improvements

<!-- project-os-operation
shared_contract: maintenance-analysis
-->

**Does:** Analyze and recommend maintenance improvements for one focus area.
**For:** Prioritize evidence-based improvements without mixing performance, product, and code quality.
**How:** Read-only analysis of `FOCUS_AREA`, delivered as findings with their reference,
verifiable disposition, recommendation, risks, and areas not reviewed. A missing,
invalid, or materially ambiguous focus fails closed with `output.status_result`.
