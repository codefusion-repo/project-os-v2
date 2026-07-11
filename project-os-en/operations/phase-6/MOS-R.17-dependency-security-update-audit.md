# MOS-R.17 — Dependency security update audit

MOSDLC operation `dependency-security-update-audit` · Phase 6 — Maintenance and improvements · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only audit)

**Does:** Audit dependencies and pending security updates.
**For:** To reduce risk of dependencies without blindly executing upgrades.
**How:** Read manifests, lockfiles and advisories; classifies severity and proposes a prioritized route.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not run upgrades or installs, pin versions, or edit manifests.
- Redact credentials or secret-looking values as `[REDACTED]`; report the path, variable, and risk type.

**Deliver:** output.status_result. In case of unreadable manifests or advisories, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.1 or maintenance. Next: MOS-3.8 for prioritized upgrades; MOS-3.3 for non-urgent follow-ups. Recommended: MOS-3.8 for priority findings.
