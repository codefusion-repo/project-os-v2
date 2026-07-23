# MOS-3.6 — Draft closeout commands

MOSDLC operation `draft-closeout-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.review_before_close · mode.review_only · output.pm_command_bundle
- Evidence: evidence.issue_scope, evidence.pr_diff, evidence.validation_output
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Regenerate the issue/PR closure and cleanup package when the bundle
delivered by the MOS-3.7 GO is unavailable or stale.
**For:** Exceptional closeout regeneration; the MOS-3.7 GO already delivers the
bundle and its verification in the same response.
**How:** Provide a copy-safe bundle for the Human PM to run, rebuilt from live status.

**Variables**
- Required: PR_NUMBER, ISSUE_NUMBER
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7 when its GO bundle was lost or became stale.
Next: MOS-3.9 only on a closure failure or a requested independent
verification. Recommended: MOS-3.9 only when closure fails.
