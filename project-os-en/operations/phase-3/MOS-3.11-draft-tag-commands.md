# MOS-3.11 — Draft tag commands

MOSDLC operation `draft-tag-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.validation_output
- PM approval: Yes (the Human PM authorizes and runs the tag)

**Does:** Draft the git tag creation bundle for GitHub.
**For:** Publish a simple tag when readiness justifies it.
**How:** Bundle copy-safe; the Human PM executes tag and push.

**Variables**
- Required: — (none)
- Optional: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.10. Next: Human PM executes; then MOS-3.9 or MOS-3.12. Recommended: MOS-3.12 if applicable Release.
