# PM Operations Catalog

This document maps every public operation to the canonical kernel components (workflow, output, evidence) and the required/optional PM variables.

| Operation | Workflow | Mode | Output Contract | Evidence | Required Variables | Optional Variables |
| --- | --- | --- | --- | --- | --- | --- |
| `templates/operations/00-browser-chat-activation.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | none | `PM_QUESTION` |
| `templates/operations/01-terminal-agent-setup.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | none | none |
| `templates/operations/02-adopt-existing-target.md` | `workflow.target_adoption` | `mode.delegated_commit_pr` | `output.adoption_packet` | `evidence.target_adoption` | `TARGET_REPOSITORY` | none |
| `templates/operations/03-bootstrap-new-project.md` | `workflow.target_adoption` | `mode.delegated_commit_pr` | `output.adoption_packet` | `evidence.target_adoption` | `TARGET_REPOSITORY` | none |
| `templates/operations/04-verify-target-adoption.md` | `workflow.target_adoption` | `mode.review_only` | `output.status_result` | `evidence.target_adoption` | `TARGET_REPOSITORY` | none |
| `templates/operations/05-upgrade-kernel-adoption.md` | `workflow.target_adoption` | `mode.delegated_commit_pr` | `output.adoption_packet` | `evidence.target_adoption` | `TARGET_REPOSITORY` | none |
| `templates/operations/06-create-issue-from-description.md` | `workflow.pm_intake` | `mode.review_only` | `output.pm_command_bundle` | `evidence.repo_state` | `DESCRIPTION` | none |
| `templates/operations/07-review-project-state.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | none | `PM_QUESTION` |
| `templates/operations/08-create-next-issue-from-live-state.md` | `workflow.pm_intake` | `mode.review_only` | `output.pm_command_bundle` | `evidence.repo_state` | none | none |
| `templates/operations/09-route-issue-implementation.md` | `workflow.pm_intake` | `mode.review_only` | `output.route_prompt` | `evidence.repo_state` | `ISSUE_NUMBER` | none |
| `templates/operations/10-route-review-corrections.md` | `workflow.pm_intake` | `mode.review_only` | `output.route_prompt` | `evidence.repo_state` | `ISSUE_NUMBER`, `FEEDBACK_PM_HUMANO` | none |
| `templates/operations/11-review-pr-before-close.md` | `workflow.review_before_close` | `mode.review_only` | `output.closure_comment` | `evidence.pr_diff`, `evidence.review_evidence` | `PR_NUMBER` | none |
| `templates/operations/12-closeout-pr-issue.md` | `workflow.review_before_close` | `mode.review_only` | `output.closure_comment` | `evidence.closure_evidence` | `PR_NUMBER`, `ISSUE_NUMBER` | none |
| `templates/operations/13-post-merge-verification.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | `PR_NUMBER` | none |
| `templates/operations/14-release-readiness.md` | `workflow.release_readiness` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | none | none |
| `templates/operations/15-create-release-tag.md` | `workflow.release_readiness` | `mode.review_only` | `output.pm_command_bundle` | `evidence.repo_state` | none | `TAG_NAME` |
| `templates/operations/16-github-release-object.md` | `workflow.release_readiness` | `mode.review_only` | `output.pm_command_bundle` | `evidence.repo_state` | none | `TAG_NAME` |
| `templates/operations/17-target-adapter-audit.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | `TARGET_REPOSITORY` | none |
| `templates/operations/18-traceability-audit.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | none | `ISSUE_NUMBER` |
| `templates/operations/19-idea-feedback.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | `IDEA` | none |
| `templates/operations/20-draft-handoff.md` | `workflow.handoff` | `mode.review_only` | `output.handoff_packet` | `evidence.repo_state` | none | none |
| `templates/operations/21-human-qa-checklist.md` | `workflow.review_only` | `mode.review_only` | `output.status_result` | `evidence.repo_state` | `ISSUE_NUMBER` | none |
| `templates/operations/22-design-asset-request.md` | `workflow.pm_intake` | `mode.review_only` | `output.asset_prompt` | `evidence.repo_state` | `DESCRIPTION` | none |
| `templates/operations/23-security-review-request.md` | `workflow.pm_intake` | `mode.review_only` | `output.security_review_prompt` | `evidence.repo_state` | `ISSUE_NUMBER` | none |
| `templates/operations/24-create-follow-up-from-review.md` | `workflow.pm_intake` | `mode.review_only` | `output.pm_command_bundle` | `evidence.repo_state` | `PR_NUMBER` | none |
| `templates/operations/25-record-adr-decision.md` | `workflow.pm_intake` | `mode.delegated_commit_pr` | `output.status_result` | `evidence.repo_state` | `DECISION` | none |
