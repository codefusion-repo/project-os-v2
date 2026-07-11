# MOS-3.11 — Draft tag commands

MOSDLC operation `draft-tag-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.validation_output
- PM approval: Yes (the Human PM authorizes and runs the tag)

**Does:** Draft a copy-safe git tag command bundle for the Human PM to execute after readiness is established.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft a copy-safe git tag and push bundle with exact tag name, repository, verification, risk, and rollback prose.

**Variables**
- Required: — (none)
- Optional: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.10. Next: MOS-3.9, MOS-3.12. Recommended: MOS-3.12.
