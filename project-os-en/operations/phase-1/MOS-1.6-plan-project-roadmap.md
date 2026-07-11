# MOS-1.6 — Plan project roadmap

MOSDLC operation `plan-project-roadmap` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: Yes (only the bundled GitHub write, run by the Human PM)

**Does:** Draft the general project roadmap from stable requirements documentation and live repository context.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Convert stable requirements into a roadmap issue body with phases, outcomes, not-now scope, risks, and validation expectations.

**Variables**
- Required: SOURCE_DOCS
- Optional: TARGET_REPOSITORY, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.draft_issue (+output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.5. Next: MOS-3.1, MOS-3.2. Recommended: MOS-3.1.
