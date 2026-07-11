# MOS-3.12 — Draft release commands

MOSDLC operation `draft-release-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.validation_output
- PM approval: Yes (the Human PM authorizes and runs the release)

**Does:** Draft the GitHub Release object creation bundle (notes and tag).
**For:** To publish releases with traceable notes.
**How:** Provide a copy-safe bundle, distinct from a simple tag bundle, for the Human PM to run.

**Variables**
- Required: — (none)
- Optional: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.10. Next: Human PM executes; then MOS-0.6 or MOS-3.1. Recommended: MOS-3.1.
