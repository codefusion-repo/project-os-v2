# Route prompts (browser chat → terminal agent)

One template for every route. Fill the variable block, delete unused lines, add
the one-line instruction for the variant you need, and paste into the terminal
agent. Everything not stated resolves from the kernel.

Keep route prompts compact and issue-referential per `boundary.context_economy`
(docs/CONTEXT_ECONOMY.md): never paste a full issue body, full diff, full log,
or prior report — the executing agent reads live evidence at task time.
Authorization travels separately as exact scoped PM approval
(`kernel/execution_modes.json` `approval_note`); this prompt grants no
permission. Copy-safe: plain text, at most one fenced block.

How the executing agent resolves the kernel is owned by `kernel/manifest.json`
(its `resolution_sequence` and surface-aware `resolution_strategy`); the route
prompt routes work and never restates resolver strategy, issue bodies, or
kernel rules, on any surface. Resolver output is operative task guidance, not
mere context and not authorization; the executing agent still reconstructs live
traceability, confirms exact PM approval where required, and fails closed on
missing evidence.

Validation is proportional for every route and target repository
(`boundary.validation_discipline`, `docs/VALIDATION_POLICY.md`). The route
prompt states scoped validation expectations; it does not default to a full
suite or new tests. Use `VALIDATION_REQUIRED` to distinguish agent-run required
commands, PM-run drafted commands, manual PM validation, or justified no
automated validation.

## Variable block (omit lines that do not apply)

~~~text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{org/repo, if work happens in a different repo}}
KERNEL_REPOSITORY = {{kernel owner/repo, normally codefusion-repo/project-os-v2}}
KERNEL_LOCAL_PATH = {{path to kernel/, or kernel when executing inside KERNEL_REPOSITORY}}
ISSUE_OR_PR = {{#N}}
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = {{canonical workflow id from kernel/workflows.json}}
EXECUTION_MODE = {{canonical mode id from kernel/execution_modes.json}}
OUTPUT_CONTRACT = {{canonical output id from kernel/outputs.json}}
SCOPE = {{1-3 lines, never the full issue body}}
OUT_OF_SCOPE = {{1-3 lines, only plausible mistakes}}
EVIDENCE_REQUIRED = {{canonical evidence ids from kernel/evidence.json}}
VALIDATION_REQUIRED = {{agent-run commands | PM-run draft commands | manual validation | no automated validation, with rationale}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium | high | xhigh}} — {{1-2 line rationale}}
~~~

When `PM_AUTHORIZATION_STATUS` is granted for this exact scope and mode, proceed
without re-requesting approval unless the `approval_note` rule applies. Agent
disagreement with a PM decision is reported as risk or accepted exception, not as
`status.needs_pm_decision` or `status.blocked` by itself.
That status does not bypass required evidence, branch preflight, validation, or
fail-closed behavior.

## Variants

Set the workflow/mode/output as shown, then add the instruction line.

- **Implement an issue** — `WORKFLOW = workflow.issue_implementation`;
  `EXECUTION_MODE = mode.local_implementation | mode.delegated_commit_push | mode.delegated_commit_pr`;
  `OUTPUT_CONTRACT = output.execution_report`;
  `EVIDENCE_REQUIRED = evidence.issue_scope, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output`.
  *Instruction:* "Implement ISSUE_OR_PR in REPOSITORY_NAME. Resolve the kernel,
  run branch preflight, work only inside SCOPE on BRANCH_NAME, validate, and
  report per OUTPUT_CONTRACT. Use proportional validation: run mandatory
  agent-side checks for deterministic, kernel, resolver, security,
  authorization, traceability, deployment, secret-sensitive,
  production-impacting, or other high-risk changes; otherwise draft PM-run
  commands or manual validation when that is the scoped evidence."

- **Adopt target repository** — `WORKFLOW = workflow.target_adoption`;
  `EXECUTION_MODE = mode.review_only | mode.delegated_commit_pr`;
  `OUTPUT_CONTRACT = output.adoption_packet | output.execution_report`;
  `TARGET_REPOSITORY = {{target org/repo}}`;
  `SCOPE = inspect target adoption; audit existing adapters; draft only under
  review-only; under delegated_commit_pr with exact PM approval create only
  AGENTS.md, CLAUDE.md, and GEMINI.md from KERNEL_REPOSITORY's canonical
  templates`;
  `OUT_OF_SCOPE = product code, CI/package/deploy/runtime config, .env,
  secrets, deployment settings, merge/closure/labels/releases/tags/settings`;
  `EVIDENCE_REQUIRED = evidence.target_adoption` for review-only;
  `EVIDENCE_REQUIRED = evidence.target_adoption, evidence.branch_preflight,
  evidence.pm_approval, evidence.validation_output` for delegated_commit_pr.
  *Instruction:* "Resolve the kernel and inspect TARGET_REPOSITORY first:
  whether `AGENTS.md` exists, whether `CLAUDE.md` exists, whether `GEMINI.md`
  exists, whether a browser-chat adapter was supplied, and whether metadata,
  roadmap anchor, kernel repo/path, kernel version, target notes, validation
  commands, and durable live-state risk are present. If adapters exist,
  audit/compare them against KERNEL_REPOSITORY's `adapters/*.target.md` and/or
  `tools.audit_target_adapters`; report drift and preserve target-owned notes,
  security/domain constraints, and validation commands. If adoption is missing,
  review-only drafts only; delegated_commit_pr with exact PM approval may create
  only `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` and open a draft PR. Browser
  chat remains draft-only. Do not merge, close, label,
  release, tag, change settings, deploy, or touch secrets."

- **Review a PR before merge/close** — `WORKFLOW = workflow.review_before_close`;
  `EXECUTION_MODE = mode.review_only`; `OUTPUT_CONTRACT = output.review_result`;
  `TARGET_ACTOR_TYPE = actor.terminal_agent | actor.browser_chat` (choose one
  existing surface; do not invent a reviewer actor);
  `EVIDENCE_REQUIRED = evidence.issue_scope, evidence.pr_diff, evidence.validation_output`.
  *Instruction:* "Review PR ISSUE_OR_PR against its linked issue. Read the real
  PR body/comments/reports only as claims, then inspect changed files, PR diff,
  and relevant final head files when the diff is insufficient. Compare
  implementation behavior against issue objective/scope/out-of-scope/acceptance
  criteria and validation against the issue's scoped validation expectations,
  including accepted PM-run or manual validation evidence when proportional.
  If code/diff/final file
  evidence cannot be inspected, return `status.needs_context`, not GO. Do not
  merge or close; report a verdict with findings by file:line and explicit
  not-reviewed gaps."

- **Design asset prompt** — `WORKFLOW = workflow.design_asset`;
  `EXECUTION_MODE = mode.review_only`; `OUTPUT_CONTRACT = output.asset_prompt`;
  `TARGET_ACTOR_TYPE = actor.terminal_agent | actor.browser_chat` (choose one
  existing surface; graphic/design specialist is a recipient, not an actor);
  `OUT_OF_SCOPE = target repo edits, binary assets, image generation automation,
  Figma/design-tool integration, product/design ownership claims`;
  `EVIDENCE_REQUIRED = evidence.repo_state, evidence.source_basis`.
  *Instruction:* "Read ISSUE_OR_PR, target repo context, and PM-provided design
  evidence live. Identify the needed assets and constraints: asset type, usage,
  dimensions, file format, style/brand/product truth, accessibility notes, and
  acceptance criteria where available. Draft a prompt/instructions packet for a
  real graphic/design recipient. Do not generate or commit assets, edit target
  files, or imply Project OS owns target product/design truth."

- **Security review prompt** — `WORKFLOW = workflow.security_revision`;
  `EXECUTION_MODE = mode.review_only`;
  `OUTPUT_CONTRACT = output.security_review_prompt`;
  `TARGET_ACTOR_TYPE = actor.terminal_agent | actor.browser_chat` (choose one
  existing surface; security specialist is a recipient/focus, not an actor);
  `OUT_OF_SCOPE = fixes, commits, SAST/DAST/dependency scanner runtime,
  secret-store changes, deployment/settings changes, printing or exposing
  secrets`;
  `EVIDENCE_REQUIRED = evidence.repo_state, evidence.source_basis`.
  *Instruction:* "Read ISSUE_OR_PR, repo context, and relevant evidence live
  without exposing secrets. Identify security-sensitive surfaces and draft an
  OWASP-based prompt for a real security-review recipient covering auth,
  authorization, sessions/cookies, input validation, file uploads, redirects,
  dependency risk, admin surfaces, secrets handling, logging, error exposure,
  and deployment/config risk where applicable. Require redaction; never ask
  anyone to print, paste, upload, quote, summarize, or expose `.env`, keys,
  tokens, credentials, JWT secrets, database URLs, cookies, session tokens,
  payment-provider keys, CI secrets, or hidden environment values."

- **Apply review corrections** — `WORKFLOW = workflow.issue_implementation`;
  `EXECUTION_MODE = mode.delegated_commit_push | mode.delegated_commit_pr`;
  `OUTPUT_CONTRACT = output.execution_report`;
  `SCOPE = fix only the findings listed below, same branch, same issue scope`;
  `EVIDENCE_REQUIRED = evidence.pr_diff, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output`.
  *Instruction:* "List findings as `file:line — finding`. Resolve the kernel,
  preflight on BRANCH_NAME, apply only these corrections, validate, push per
  EXECUTION_MODE, and report."

- **Audit (read-only)** — `WORKFLOW = workflow.review_only`;
  `EXECUTION_MODE = mode.review_only`; `OUTPUT_CONTRACT = output.review_result`;
  `OUT_OF_SCOPE = edits, commits, GitHub mutations, fixes (report only)`;
  `EVIDENCE_REQUIRED = evidence.repo_state, evidence.source_basis`.
  *Instruction:* "Audit TARGET_REPOSITORY read-only. Cite concrete evidence
  (paths, issues, PRs, history) for every claim, say what could not be verified,
  and do not soften findings." Typically `recommended_effort: xhigh`.
