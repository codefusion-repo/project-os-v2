# MOS-3.4 — Draft implementation route prompt

MOSDLC operation `draft-implementation-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No for drafting. A draft does not authorize writing; a PM
  delivery with `PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`
  can satisfy exact PM approval only for what it declares.

**Does:** Draft the route-prompt to delegate the implementation of an issue to a terminal agent.
**For:** To route implementation with correct scope, mode and evidence.
**How:** Use a compact, issue-referential bootloader: the live issue or PR and
its comments retain detail instead of the route prompt. Browser chat may
recommend an optional skill and infer `RECOMMENDED_TERMINAL_AGENT_FAMILY` from
the work. The recommendation is advisory, authorizes nothing, and may be
overridden by explicit PM feedback.

**Variables**
- Required: — (none)
- Optional: ISSUE_NUMBER, ROADMAP_ISSUE, OPTIONAL_SKILL, HYDRATION_LEVEL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (the skill, level, PM feedback, and PM questions are context only and never authorize an action). `HYDRATION_LEVEL` accepts `minimal`, `compact` (default), or `full/debug` and controls only the resolver's hydrated content. The wizard requires `PM_AUTHORIZATION_STATUS` and preloads `HYDRATION_LEVEL=compact` before generating this route prompt.

**Authorization contract:** Browser chat only drafts and can never self-assign,
complete, change, or infer `granted`. A route prompt that is a draft, was not
delivered by the PM, or has `PM_AUTHORIZATION_STATUS` set to `pending` does not
authorize writing. When the PM delivers the route prompt with
`PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`, that delivery
satisfies `evidence.pm_approval` only for the declared repository, workflow,
mode, branch, and scope. The receiving agent must verify that match and the
remaining evidence; an absent, unknown, or inferred status fails closed. No additional GitHub comment is universally required, and the approval does not
cover merge, closure, tags, releases, deploys, settings, or any action outside
the declared mode.

**Conformance check:** Before delivery, compare the output with
`project-os-en/templates/route-prompt.md`. Compress it when it repeats issue,
PR, or comment detail; keep a live-evidence reference instead of copying bodies,
acceptance criteria, source basis, checklists, or implementation steps. Deliver
only one standard variable block, a 1-3 line `SCOPE`, and one following concrete
instruction. If that shape cannot be produced, fail closed with
`output.status_result`.

**Reproducible manual QA:** Use a long issue with extensive comments. Verify that
the route prompt keeps only metadata, a brief scope, brief out-of-scope, and one
concrete instruction; that `SCOPE` has 1-3 lines; that it has no copied sections;
and that it instructs the receiving agent to read live evidence.

**Deliver:** output.route_prompt. If evidence, scope, approval, or a conforming shape is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.1, MOS-3.2 or MOS-3.8. Next: MOS-3.7 after the PR. Recommended: MOS-3.7.
