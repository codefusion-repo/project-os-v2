# MOS-0.2 — Bootstrap new project

MOSDLC operation `bootstrap-new-project` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet
- Evidence: evidence.target_adoption
- PM approval: No (draft-only)

**Does:** Draft the initial Project OS adoption package for a new target repository.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft an adoption packet with adapter drafts, a foundational roadmap draft, and a PM checklist.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.1. Next: MOS-0.5. Recommended: MOS-0.5.
