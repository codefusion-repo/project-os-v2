# MOS-0.2 — Bootstrap new project

MOSDLC operation `bootstrap-new-project` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet
- Evidence: evidence.target_adoption
- PM approval: No (draft-only)

**Does:** Draft the initial adoption structure and foundational roadmap of a new repo.
**For:** Start a new project under Project OS.
**How:** Browser chat drafts adoption package; the Human PM applies or delegates it.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: DESCRIPTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.1. Next: MOS-0.5. Recommended: MOS-0.5.
