# Route prompt: implement an issue (browser chat → terminal agent)

Fill the variables, delete unused lines, paste into the terminal agent.
Everything not stated here is resolved by the agent from the kernel.

```text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
ISSUE_OR_PR = {{#N}}
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = workflow.issue_implementation
EXECUTION_MODE = {{mode.local_implementation | mode.delegated_commit_push | mode.delegated_commit_pr}}
OUTPUT_CONTRACT = output.execution_report
SCOPE = {{1-3 lines from the issue}}
OUT_OF_SCOPE = {{1-3 lines, only plausible mistakes}}
EVIDENCE_REQUIRED = evidence.issue_scope, evidence.branch_preflight, evidence.validation_output
VALIDATION_REQUIRED = {{exact commands}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = granted for this exact scope and mode

Implement ISSUE_OR_PR in REPOSITORY_NAME. Resolve the kernel first, run
branch preflight, work only inside SCOPE on BRANCH_NAME, validate, and
report per OUTPUT_CONTRACT. This prompt grants no permission beyond
PM_AUTHORIZATION_STATUS.

recommended_effort: {{medium | high | xhigh}}
rationale: {{1-2 lines}}
```
