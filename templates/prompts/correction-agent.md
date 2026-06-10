# Route prompt: apply review corrections

For sending review findings back to a terminal agent on the same branch.

~~~text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
ISSUE_OR_PR = PR {{#N}} (issue {{#M}})
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = workflow.issue_implementation
EXECUTION_MODE = {{mode.delegated_commit_push | mode.delegated_commit_pr}}
OUTPUT_CONTRACT = output.execution_report
SCOPE = fix only the findings listed below; same branch, same issue scope
OUT_OF_SCOPE = refactors or improvements beyond the findings
EVIDENCE_REQUIRED = evidence.pr_diff, evidence.branch_preflight, evidence.validation_output
VALIDATION_REQUIRED = {{exact commands}}
BRANCH_NAME = {{existing work branch}}
PM_AUTHORIZATION_STATUS = granted for these findings only

Findings to fix:
1. {{file:line — finding}}
2. {{file:line — finding}}

Resolve the kernel, preflight on BRANCH_NAME, apply only these corrections,
validate, push per EXECUTION_MODE, and report per OUTPUT_CONTRACT.

recommended_effort: {{medium | high}}
rationale: {{1-2 lines}}
~~~
