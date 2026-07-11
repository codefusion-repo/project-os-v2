# MOS-R.22 — Public packaging safety review

MOSDLC operation `public-packaging-safety-review` · Phase 3 — Implementation · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.source_basis
- PM approval: No (read-only review; conversion and publication are separate)

**Does:** Review the safety of packaging the target project for public use, read-only.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only safety review before public packaging: secrets hygiene, internal-only surfaces that must be removed/hidden/disabled/converted before release, documentation exposure, and unsafe defaults.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Report secret hygiene by path, variable, or risk type; never report values.
- Keep wording target-agnostic: do not assume Project OS, dogfooding, public packages, or GitHub releases.
- Return `status.needs_pm_decision` when exposure requires a PM choice.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.7. Next: MOS-R.23. Recommended: MOS-R.23.
