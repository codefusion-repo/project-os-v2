# MOS-R.17 — Dependency security update audit

MOSDLC operation `dependency-security-update-audit` · Phase 6 — Production readiness and maintenance · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only audit)

**Does:** Audit dependencies and pending security updates for the target project, read-only, with severity and a proposed update route.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only audit of dependencies and pending security updates, classifying each finding by severity and proposing a prioritized update route without executing any upgrade.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not run upgrades or installs, pin versions, or edit manifests.
- Redact credentials or secret-looking values as `[REDACTED]`; report the path, variable, and risk type.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.1. Next: MOS-3.8, MOS-3.3. Recommended: MOS-3.8.
