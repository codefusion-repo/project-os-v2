# Route prompt: implement an issue (browser chat → terminal agent)

Fill the variables, delete unused lines, paste into the terminal agent.
Everything not stated here is resolved by the agent from the kernel.

Keep the prompt compact and issue-referential: never duplicate the full
issue body. Detailed scope, acceptance criteria, validation, risks, and
rollback live in the GitHub issue (created from `templates/issue.md`),
and the terminal agent reads the issue body live.

~~~text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
ISSUE_OR_PR = {{#N}}
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = workflow.issue_implementation
EXECUTION_MODE = {{mode.local_implementation | mode.delegated_commit_push | mode.delegated_commit_pr}}
OUTPUT_CONTRACT = output.execution_report
SCOPE = {{1-3 line summary, never the full issue body}}
OUT_OF_SCOPE = {{1-3 lines, only plausible mistakes}}
EVIDENCE_REQUIRED = evidence.issue_scope, evidence.branch_preflight, evidence.validation_output
VALIDATION_REQUIRED = {{exact commands}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = granted for this exact scope and mode

Implement ISSUE_OR_PR in REPOSITORY_NAME. Resolve the kernel first, run
branch preflight, work only inside SCOPE on BRANCH_NAME, validate, and
report per OUTPUT_CONTRACT. This prompt grants no permission beyond
PM_AUTHORIZATION_STATUS. When PM_AUTHORIZATION_STATUS is granted for this
exact scope and mode, proceed without re-requesting approval unless scope,
actor, write type, target, risk, or evidence changes materially.

recommended_effort: {{medium | high | xhigh}}
rationale: {{1-2 lines}}
~~~
