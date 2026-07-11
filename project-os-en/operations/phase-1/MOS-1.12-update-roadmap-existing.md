# MOS-1.12 — Update roadmap existing

MOSDLC operation `update-roadmap-existing` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: Yes (only the bundled GitHub write, run by the Human PM)

**Does:** Draft or update the general roadmap for an existing project from requirements documentation and live repository context.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft a roadmap body or update text that reflects the existing project's requirements, current state, not-now scope, risks, and validation expectations.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: SOURCE_DOCS, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.draft_issue (+output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.11. Next: MOS-3.1. Recommended: MOS-3.1.
