# MOS-R.7 — Review licensing publication readiness

MOSDLC operation `review-licensing-publication-readiness` · Phase 3 — Implementation · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (advisory review; publication stays with the PM)

**Does:** Review licensing, support posture, secrets hygiene, and documentation quality for publication readiness of the target project.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only review of publication readiness: licensing completeness and compatibility, support posture, secrets hygiene, and documentation quality against the target's publication criteria.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Report secret risks only by path, variable, or type; never by value.
- Do not assume every target publishes packages, releases, or public distributions.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.10. Next: MOS-R.22. Recommended: MOS-R.22.
