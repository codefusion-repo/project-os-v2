# Route prompts (browser chat → terminal agent)

One template for every route. Fill the variable block, delete unused lines, add
the one-line instruction for the variant you need, and paste into the terminal
agent. Everything not stated resolves from the kernel.

Keep route prompts compact and issue-referential: never paste a full issue body;
the terminal agent reads the issue live. Authorization travels separately as
exact scoped PM approval (`kernel/execution_modes.json` `approval_note`); this
prompt grants no permission. Copy-safe: plain text, at most one fenced block.

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
VALIDATION_REQUIRED = {{exact commands}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{granted for this exact scope and mode | pending}}
recommended_effort: {{medium | high | xhigh}} — {{1-2 line rationale}}
~~~

When `PM_AUTHORIZATION_STATUS` is granted for this exact scope and mode, proceed
without re-requesting approval unless the `approval_note` rule applies. Agent
disagreement with a PM decision is reported as risk or accepted exception, not as
`status.needs_pm_decision` or `status.blocked` by itself.

## Variants

Set the workflow/mode/output as shown, then add the instruction line.

- **Implement an issue** — `WORKFLOW = workflow.issue_implementation`;
  `EXECUTION_MODE = mode.local_implementation | mode.delegated_commit_push | mode.delegated_commit_pr`;
  `OUTPUT_CONTRACT = output.execution_report`;
  `EVIDENCE_REQUIRED = evidence.issue_scope, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output`.
  *Instruction:* "Implement ISSUE_OR_PR in REPOSITORY_NAME. Resolve the kernel,
  run branch preflight, work only inside SCOPE on BRANCH_NAME, validate, and
  report per OUTPUT_CONTRACT." (Target-adapter adoption is this variant: SCOPE =
  repoint the target's `AGENTS.md`/`CLAUDE.md` to the kernel using
  KERNEL_REPOSITORY's `adapters/AGENTS.target.md` and
  `adapters/CLAUDE.target.md`; keep target product truth in the target.)

- **Review a PR before merge/close** — `WORKFLOW = workflow.review_before_close`;
  `EXECUTION_MODE = mode.review_only`; `OUTPUT_CONTRACT = output.review_result`;
  `TARGET_ACTOR_TYPE = actor.terminal_agent | actor.browser_chat` (choose one
  existing surface; do not invent a reviewer actor);
  `EVIDENCE_REQUIRED = evidence.issue_scope, evidence.pr_diff, evidence.validation_output`.
  *Instruction:* "Review PR ISSUE_OR_PR against its linked issue. Read the real
  diff and validation live. Check scope, correctness, boundaries preserved, and
  risks. Do not merge or close; report a verdict with findings by file:line."

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
