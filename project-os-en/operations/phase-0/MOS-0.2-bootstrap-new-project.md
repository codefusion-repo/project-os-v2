# MOS-0.2 — Bootstrap new project

MOSDLC operation `bootstrap-new-project` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.pm_command_bundle, +output.route_prompt, +output.status_result)
- Evidence: evidence.target_adoption
- PM approval: No for drafting. A draft does not authorize writing; a PM
  delivery of the route prompt with `PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`
  can satisfy exact PM approval only for what it declares.

**Does:** Draft the browser-first bootstrap of a new repo: first a complete browser adapter, then roadmap creation and the terminal route once they exist.
**For:** To start a new project under Project OS without blocking startup on a missing roadmap.
**How:** Browser chat resolves the kernel in `mode.review_only` and drafts; the Human PM applies the browser adapter, creates the roadmap, and delivers the route prompt.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PROJECT_NAME, DESCRIPTION, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, ADOPTION_ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Browser adapter first:** Always produce a complete PM-applicable `BROWSER_CHAT.md` draft even when the project has no roadmap. It is a PM-applied artifact and need not be stored inside the target repo. Keep its read-only and draft-only boundaries and separate `browser_adoption_state` from `terminal_adoption_state`.

**Roadmap and terminal route:** Declare `roadmap_state`. When no canonical roadmap exists, declare `roadmap_state=missing`, draft a copy-safe `output.pm_command_bundle` to create it, do not invent its number, and do not fill `{{#ROADMAP_ISSUE}}` with durable placeholders; do not yet generate an executable terminal route prompt. After the live roadmap exists, use its verified number and a live work unit (`ADOPTION_ISSUE_NUMBER`) to draft the route prompt that delegates repo-owned adapter writes to the terminal agent in `mode.delegated_commit_pr`, with branch preflight, validation, and exact PM approval; the route prompt references the live unit and does not restate the issue body, and never invent the work unit.

**Deliver:** output.adoption_packet (+output.pm_command_bundle, +output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.1. Next: MOS-0.5. Recommended: MOS-0.5.
