# MOS-3.10 — Analyze release readiness

MOSDLC operation `analyze-release-readiness` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result (+output.pm_command_bundle)
- Evidence: evidence.repo_state, evidence.validation_output, evidence.exact_ref
- PM approval: No (read-only)

**Does:** Analyze release-on-tag readiness and draft creation commands if ready.
**For:** To decide tag/release with merged evidence and validation.
**How:** Reconstruct the unit, current QA, and review through the common
QA → release → deployment continuity contract. Verify the actual merge and its
resulting ref; GO or CI on the previous head does not prove validation of that
ref. Reuse still-applicable criteria and evidence; renew what depends on ref,
environment, or risk. Expose each gap and the exact tag/Release gate, separately
from closeout. With sufficient readiness and applicable exact approvals, consume
MOS-3.11 or MOS-3.12 in the same response without another selection or locator.
Missing merge, validation, or decision yields status and the next safe step,
without claiming readiness or creating a release unit.

**Variables**
- Required: — (none)
- Optional: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: QA and closeout through MOS-3.7, with verified merge for release readiness. Next: MOS-3.11 or MOS-3.12 in the same response when their gates are satisfied; then intended environment readiness via MOS-R.11 when applicable. Recommended: the same unit's next pending action.
