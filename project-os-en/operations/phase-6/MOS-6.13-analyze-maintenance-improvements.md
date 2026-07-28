# MOS-6.13 — Analyze maintenance improvements

<!-- project-os-operation
canonical_code: MOS-6.13
operation_id: analyze-maintenance-improvements
aliases: MOS-6.3,MOS-6.4,MOS-6.5
deprecation: none
compatibility_reason: MOS-6.3, MOS-6.4, and MOS-6.5 retain their historical entry points and resolve this one contract with their focus bound.
-->

MOSDLC operation `analyze-maintenance-improvements` · Phase 6 — Maintenance and improvements · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.review_result (+output.status_result)
- Evidence: evidence.repo_state
- PM approval: No (read-only)

**Does:** Analyze and recommend maintenance improvements for one focus area.
**For:** Prioritize evidence-based improvements without mixing performance, product, and code quality.
**How:** Read-only analysis of `FOCUS_AREA`, delivered as findings with their reference,
verifiable disposition, recommendation, risks, and areas not reviewed. A missing,
invalid, or materially ambiguous focus fails closed with `output.status_result`.

**Variables**
- Required: TARGET_REPOSITORY, FOCUS_AREA
- Optional: PATH_SCOPE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

INPUT:
  TARGET_REPOSITORY=<owner/repository>
  FOCUS_AREA=<performance|product|code_quality>
  PATH_SCOPE=<path scope> optional
  PM_FEEDBACK_HUMANO=<human feedback> optional
  PM_QUESTION_HUMANO=<human question> optional

**Deliver:** output.review_result (+output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: periodic maintenance. Next: MOS-6.9, MOS-6.10, or MOS-3.14 according to `FOCUS_AREA`. Recommended: MOS-6.9 for `performance`, MOS-6.10 for `product`, and MOS-3.14 for `code_quality`.
