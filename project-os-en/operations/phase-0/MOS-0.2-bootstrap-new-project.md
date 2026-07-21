# MOS-0.2 — Bootstrap new project

MOSDLC operation `bootstrap-new-project` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.pm_command_bundle, +output.route_prompt, +output.status_result)
- Evidence: evidence.target_adoption
- PM approval: No for drafting. A draft does not authorize writing; a PM
  delivery of the route prompt with `PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`
  can satisfy exact PM approval only for what it declares.

**Does:** Draft the browser-first bootstrap of a new repo: first a complete browser adapter, then the delegated terminal route for the repo-owned adapters.
**For:** To start a new project under Project OS without requiring a prior roadmap or issue.
**How:** Browser chat resolves the kernel in `mode.review_only` and drafts; the Human PM applies the browser adapter and delivers the route prompt.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PROJECT_NAME, DESCRIPTION, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Browser adapter first:** Always produce a complete PM-applicable `BROWSER_CHAT.md` draft even when the project has no roadmap. It is a PM-applied artifact and need not be stored inside the target repo. Keep its read-only and draft-only boundaries and separate `browser_adoption_state` from `terminal_adoption_state`.

**Work unit and terminal route:** The live unit of `workflow.target_adoption` is the bounded target adoption: `TARGET_REPOSITORY`, the exact repo-owned adapter scope, the work branch, `evidence.target_adoption`, branch preflight, validation, and PM delivery with exact approval. It requires no roadmap and no adoption issue created beforehand. Draft the route prompt that delegates repo-owned adapter writes to the terminal agent in `mode.delegated_commit_pr` under those gates; never invent the work unit or the scope.

**Roadmap as optional evidence:** Declare `roadmap_state`. When a live canonical roadmap exists, use it as evidence and context; when it is missing, declare `roadmap_state=missing` and draft a copy-safe `output.pm_command_bundle` to create it, but do not invent its number and do not block adoption or the terminal route on it. Do not store roadmap, issue, PR, branch, commit, or validation numbers as durable adapter configuration.

**Deliver:** output.adoption_packet (+output.pm_command_bundle, +output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.1. Next: MOS-0.5. Recommended: MOS-0.5.
