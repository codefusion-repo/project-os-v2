# MOS-6.13 — Analyze maintenance improvements

<!-- project-os-operation
shared_contract: maintenance-analysis
-->

**Compatibility:** MOS-6.3, MOS-6.4, and MOS-6.5 retain their historical entry points and resolve this one contract with their focus bound.
**Common contract:** `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

**Does:** Analyze and recommend maintenance improvements for one focus area.
**For:** Prioritize evidence-based improvements without mixing performance, product, and code quality.
**How:** Read-only analysis of `FOCUS_AREA`, delivered as findings with their reference,
verifiable disposition, recommendation, risks, and areas not reviewed. A missing,
invalid, or materially ambiguous focus fails closed with `output.status_result`.

**Delivery and limits:** Delivery includes findings and a status result; if evidence, scope, or approval is missing or ambiguous, it fails closed and returns the decision to the PM.
