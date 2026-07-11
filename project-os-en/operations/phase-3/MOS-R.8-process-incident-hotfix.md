# MOS-R.8 — PRocess incident hotfix

MOSDLC operation `process-incident-hotfix` · Phase 3 — Implementation · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.draft_issue, output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only triage; hotfixes and commands have separate gates)

**Does:** Process an incident or critical bug: intake, triage, hotfix issue drafting, and postmortem follow-up, draft-only.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Triage the incident: classify severity and user impact only when evidence supports that route, and separate the blocking hotfix from non-blocking postmortem work.

**Variables**
- Required: INCIDENT_DESCRIPTION
- Optional: TARGET_REPOSITORY, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not run hotfixes, rollbacks, or commands; outputs are non-authorizing or PM-executed.
- Redact secrets and request a redacted source basis when the incident includes credentials or sensitive values.

**Deliver:** output.status_result (+drafts when applicable). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.16. Next: MOS-3.4, MOS-3.3. Recommended: MOS-3.4.
