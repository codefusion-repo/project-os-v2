# Route prompt: audit (read-only)

For audits, architecture reviews, viability assessments, and roadmap reviews.

```text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{repos or paths under audit}}
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = workflow.review_only
EXECUTION_MODE = mode.review_only
OUTPUT_CONTRACT = output.review_result
SCOPE = {{the questions the audit must answer, as a short list}}
OUT_OF_SCOPE = edits, commits, GitHub mutations, fixes (report only)
EVIDENCE_REQUIRED = evidence.repo_state, evidence.source_basis
EXPECTED_REPORT = findings with file/issue references, verdict, and recommendation

Audit TARGET_REPOSITORY read-only. Cite concrete evidence (paths, issues,
PRs, history) for every claim, say what could not be verified, and do not
soften findings.

recommended_effort: xhigh
rationale: audits require broad evidence gathering and structural judgment.
```
