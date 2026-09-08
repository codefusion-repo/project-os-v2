# MOS-3.12 — Draft release commands

MOSDLC operation `draft-release-commands` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.release_readiness · mode.review_only · output.pm_command_bundle
- Evidence: evidence.repo_state, evidence.validation_output, evidence.exact_ref
- PM approval: Yes (the Human PM authorizes and runs the release)

**Does:** Draft the GitHub Release object creation bundle (notes and tag).
**For:** To publish releases with traceable notes.
**How:** Consume MOS-3.10 and the common continuity contract. Verify the live
tag and resulting ref, validation, and notes for the same unit. Exact Release
approval is inferred from neither tag nor closeout; if creating the Release
would also create a missing tag, first apply MOS-3.11 and its own gate. The
copy-safe bundle retains recovery and verification of the object and ref;
Human PM executes. After verifying the result, continue to readiness of the
pending intended environment using the same sources, without a transition unit.

**Variables**
- Required: — (none)
- Optional: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.10 and verified tag. Next: PM execution and verification; MOS-R.11 for the same outcome's pending environment, or MOS-0.6 for handoff. MOS-3.1 only for a subsequent outcome. Recommended: pending environment readiness, without inferring deploy.
