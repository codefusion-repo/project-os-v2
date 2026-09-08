# Execution report

Responsibility: report executed work, evidence and validation without asking
merge/close.

PM-facing density: the resolver projects as `must_include` exactly the
`output.execution_report.must_include_by_density` list for the declared
`CHANGE_CLASS`'s report density. That density is independent of the
`HYDRATION_LEVEL` received: a critical unit resolved at `compact` keeps this
template's `full/debug` block. Use only the block for the resolved density;
never combine densities. PM-facing traceability lives in the block itself — in
`full/debug`, `Reviewed evidence`; no density adds a receipt block.

For deployment, use the resolved density's evidence, validation, risk, and
remaining-work sections to retain unit, target, environment, action,
expected/observed ref, exact approval, and reused/renewed evidence with source
and reason. Distinguish execution from post-deploy verification, record
applicable rollback and the next gate; claim neither success without verified
postconditions nor another environment's authorization through continuity.

## Minimal density

```markdown
## Result

{{What got done, in 1-3 lines.}}

## Files or surface

- {{Exact routes or touched surface.}}

## Validation

- `{{command}}` - {{actual result}}

## Reference

{{Live work unit, commit, or PR.}}
```

## Compact density

```markdown
## Scope

{{Implemented scope and respected out of scope, in 2-4 lines.}}

## Changes

- {{Material changes with exact routes.}}

## Validation

- `{{command}}` - {{actual result}}
- Not executed: {{reason if applicable}}
- Manual PM required: {{if applicable}}

## Risks

{{Remaining risks and accepted exceptions, or none.}}
```

## Full/debug density

```markdown
## Issue or PR

{{Unit of work.}}

## Repository

{{Repo target.}}

## Branch

{{Work branch.}}

## Evidence reviewed

- {{Issue/PR/roadmap/ADR/diff/comments read live.}}

## Files changed

- {{Exact routes.}}

## Validation

- `{{command}}` - {{actual result}}
- Not executed: {{reason if applicable}}
- Manual PM required: {{clarity/copy/UX/product if applicable}}

## Risks and limitations

{{Remaining risks, out-of-scope respected and exceptions accepted.}}

## Commit or PR

{{Reference if applicable.}}

## Remaining work

{{Follow-ups or none.}}

## Correction report (only when correcting a reviewed PR)

{{Publish as an append-only comment on the PR, without editing the body or any
prior comment or review.}}

- Source review or comment: {{exact reference to the review or comment}}
- Previous head: {{reviewed sha}}
- Corrected head: {{new sha}}
- Findings addressed: {{each blocking-correction with the change and its outcome}}
- Commits or range: {{reference}}
- No merge or close: {{confirmation that no merge or close happened}}
```
