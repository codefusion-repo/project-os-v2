# Route prompt: review a PR before merge/close

```text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
ISSUE_OR_PR = PR {{#N}} (issue {{#M}})
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = workflow.review_before_close
EXECUTION_MODE = mode.review_only
OUTPUT_CONTRACT = output.review_result
SCOPE = {{what the PR claims to deliver, 1-2 lines}}
EVIDENCE_REQUIRED = evidence.issue_scope, evidence.pr_diff, evidence.validation_output
EXPECTED_REPORT = verdict (approve / request changes) with findings by file:line

Review PR {{#N}} in REPOSITORY_NAME against its linked issue. Read the real
diff and validation evidence live. Check scope compliance, correctness,
boundaries preserved, and risks. Do not merge or close; report only.

recommended_effort: {{medium | high}}
rationale: {{1-2 lines}}
```
