# MOS-R.8 — Process incident hotfix

MOSDLC operation `process-incident-hotfix` · Phase 3 — Implementation · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.draft_issue, output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only triage; hotfixes and commands have separate gates)

**Does:** Process a critical incident or bug by severity, hotfix, and postmortem path.
**For:** Give an explicit route to incidents without improvising under pressure.
**How:** Confirm live evidence, classify severity and draft issue/route/bundle only when applicable.

**Variables**
- Required: INCIDENT_DESCRIPTION
- Optional: TARGET_REPOSITORY, PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Do not run hotfixes, rollbacks, or commands; outputs are non-authorizing or PM-executed.
- Redact secrets and request a redacted source basis when the incident includes credentials or sensitive values.

**Deliver:** output.status_result (+drafts if applicable). In case of non-confirmable incident or ambiguous severity/path, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: incident report or MOS-R.16. Next: MOS-3.4 for hotfix; MOS-3.3 for postmortem. Recommended: MOS-3.4 if the hotfix is ​​warranted.
