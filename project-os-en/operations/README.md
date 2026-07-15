# MOSDLC operations — compact English surface

This directory is the English PM-facing MOSDLC (Modern AI SDLC Operations) catalog. Each file is a compact operation prompt defining its outcome, variables, evidence, output, and safe connections. Stable MOS codes, variables, and kernel references match the default Spanish catalog.

## Common contract

1. Resolve `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. The resolver provides guidance and never reads live state or grants permission.
2. Reconstruct issues, PRs, branches, commits, and validation from target systems of record at task time. Durable files never store live state.
3. Validate in proportion to risk: agent-run checks, drafted PM-run commands, manual PM validation, or a justified omission.
4. Use only the context and subagents the scope needs without dropping evidence, validation, secret safety, or exact approval.
5. Resolve artifacts and their `required_template` paths from `project-os-en/kernel/artifacts.json`.
6. Treat `project-os-en/kernel/skills.json` capabilities as optional and outside workflow logic.
7. Templates, outputs, variables, and route prompts never authorize. Browser chat stays draft-only.
8. Fail closed on missing kernel data, evidence, authority, or required validation.
9. Never request or expose secrets; use `[REDACTED]` and report only names, paths, commands, and risk types.
10. `PM_FEEDBACK_HUMANO` and `PM_QUESTION_HUMANO` are optional PM context and never authorization.
11. PM-facing operations with `PM approval: Yes` consume
    `rule.precedencia_decision_pm` from the shared kernel: a later decision
    supersedes another only for the same `decision_key`; separate limits and
    gates remain in force.

Explicit resolver example:

```sh
python tools/project_os_resolve.py --actor <actor> --workflow <workflow> \
  --mode <mode> --kernel-dir project-os-en/kernel [--skill skill.<id>]
```

The local wizard works with one coherent surface per session. Without an
explicit selection it asks once, `Elige idioma / Choose language [es/en]
(default: es)`: Enter or `es` keeps Spanish (`project-os-es/operaciones` +
`project-os-es/kernel/skills.json`); `en` loads the full English bundle
(`project-os-en/operations` + `project-os-en/kernel/skills.json`). The
`--language es|en` option makes the same selection without asking and an
invalid value fails closed. The question is never repeated while generating
more prompts in the same session, and the session summary shows the language,
catalog, skills, reference kernel, and output directory. The selection lives
only in memory for the session: it does not modify adapters,
`PM_FACING_LANGUAGE`, or `KERNEL_LOCAL_PATH`, does not install or copy the
kernel, and the kernel shown is local orientation, not configuration applied
to the target. No selection grants permission.

Examples:

```sh
python tools/operation_prompt_wizard.py --language es
python tools/operation_prompt_wizard.py --language en
```

Advanced use: `--operations-dir` remains available for tests, development, and
custom catalogs. Precedence: when `--language` and `--operations-dir` do not
name the same surface, the wizard fails closed instead of mixing; an
`--operations-dir` that exactly matches a known surface derives the skills
catalog from that same surface; any other directory is a custom catalog that
keeps the existing programmatic API and is labeled neither es nor en.

When drafting `MOS-3.4` or `MOS-3.5`, the wizard also captures
`HYDRATION_LEVEL` for the terminal recipient: it accepts `minimal`, `compact`,
or `full/debug` and preloads `compact`. This assistance is local to those route
prompts; it does not make the level a canonical variable across the catalog or
authorize writing. The level controls only the resolver view returned.

## Index

### Cross-phase — Accepted recommended operations

- [MOS-R.2 — Recommend next operation](cross-phase/MOS-R.2-recommend-next-operation.md)
- [MOS-R.3 — Process a pending PM decision](cross-phase/MOS-R.3-process-needs-pm-decision.md)
- [MOS-R.4 — Review phase readiness](cross-phase/MOS-R.4-review-phase-readiness.md)

### Phase 0 — Adoption

- [MOS-0.1 — Activate browser session](phase-0/MOS-0.1-activate-browser-session.md)
- [MOS-0.2 — Bootstrap new project](phase-0/MOS-0.2-bootstrap-new-project.md)
- [MOS-0.3 — Adopt existing project](phase-0/MOS-0.3-adopt-existing-project.md)
- [MOS-0.4 — Update project adoption](phase-0/MOS-0.4-update-project-adoption.md)
- [MOS-0.5 — Verify target adoption](phase-0/MOS-0.5-verify-target-adoption.md)
- [MOS-0.6 — Handoff session context](phase-0/MOS-0.6-handoff-session-context.md)
- [MOS-R.10 — Update target adapters catalog](phase-0/MOS-R.10-update-target-adapters-catalog.md)
- [MOS-R.5 — Audit target adoption batch](phase-0/MOS-R.5-audit-target-adoption-batch.md)

### Phase 1 — Requirements, planning, and feasibility

- [MOS-1.1 — Interview requirements](phase-1/MOS-1.1-interview-requirements.md)
- [MOS-1.10 — Extract requirements from existing](phase-1/MOS-1.10-extract-requirements-from-existing.md)
- [MOS-1.11 — Update requirements docs existing](phase-1/MOS-1.11-update-requirements-docs-existing.md)
- [MOS-1.12 — Update roadmap existing](phase-1/MOS-1.12-update-roadmap-existing.md)
- [MOS-1.2 — Summarize requirements](phase-1/MOS-1.2-summarize-requirements.md)
- [MOS-1.3 — Verify requirements feasibility](phase-1/MOS-1.3-verify-requirements-feasibility.md)
- [MOS-1.4 — Draft requirements docs](phase-1/MOS-1.4-draft-requirements-docs.md)
- [MOS-1.5 — Validate requirements docs](phase-1/MOS-1.5-validate-requirements-docs.md)
- [MOS-1.6 — Plan project roadmap](phase-1/MOS-1.6-plan-project-roadmap.md)
- [MOS-1.7 — Review idea feasibility](phase-1/MOS-1.7-review-idea-feasibility.md)
- [MOS-1.8 — Update docs roadmap with requirement](phase-1/MOS-1.8-update-docs-roadmap-with-requirement.md)
- [MOS-1.9 — Review requirement removal](phase-1/MOS-1.9-review-requirement-removal.md)

### Phase 2 — Design

- [MOS-2.1 — Draft architecture diagrams](phase-2/MOS-2.1-draft-architecture-diagrams.md)
- [MOS-2.10 — Update ui/ux docs](phase-2/MOS-2.10-update-uiux-docs.md)
- [MOS-2.11 — Update data algorithms docs](phase-2/MOS-2.11-update-data-algorithms-docs.md)
- [MOS-2.12 — Update coding standards docs](phase-2/MOS-2.12-update-coding-standards-docs.md)
- [MOS-2.13 — Update security docs](phase-2/MOS-2.13-update-security-docs.md)
- [MOS-2.14 — Validate updated design docs](phase-2/MOS-2.14-validate-updated-design-docs.md)
- [MOS-2.2 — Draft ui/ux docs](phase-2/MOS-2.2-draft-uiux-docs.md)
- [MOS-2.3 — Draft data algorithms docs](phase-2/MOS-2.3-draft-data-algorithms-docs.md)
- [MOS-2.4 — Draft coding standards docs](phase-2/MOS-2.4-draft-coding-standards-docs.md)
- [MOS-2.5 — Draft security docs](phase-2/MOS-2.5-draft-security-docs.md)
- [MOS-2.6 — Validate design docs](phase-2/MOS-2.6-validate-design-docs.md)
- [MOS-2.7 — Inventory design docs](phase-2/MOS-2.7-inventory-design-docs.md)
- [MOS-2.8 — Audit design doc gaps](phase-2/MOS-2.8-audit-design-doc-gaps.md)
- [MOS-2.9 — Update architecture diagrams](phase-2/MOS-2.9-update-architecture-diagrams.md)
- [MOS-R.1 — Record an ADR decision](phase-2/MOS-R.1-record-adr-decision.md)
- [MOS-R.6 — Create or update an ADR from design](phase-2/MOS-R.6-create-update-adr-from-design.md)

### Phase 3 — Implementation

- [MOS-3.1 — Draft next issue from traceability](phase-3/MOS-3.1-draft-next-issue-from-traceability.md)
- [MOS-3.10 — Analyze release readiness](phase-3/MOS-3.10-analyze-release-readiness.md)
- [MOS-3.11 — Draft tag commands](phase-3/MOS-3.11-draft-tag-commands.md)
- [MOS-3.12 — Draft release commands](phase-3/MOS-3.12-draft-release-commands.md)
- [MOS-3.13 — Audit traceability](phase-3/MOS-3.13-audit-traceability.md)
- [MOS-3.14 — Process traceability audit](phase-3/MOS-3.14-process-traceability-audit.md)
- [MOS-3.15 — Request a 2D asset](phase-3/MOS-3.15-request-2d-asset.md)
- [MOS-3.16 — Request a 3D asset](phase-3/MOS-3.16-request-3d-asset.md)
- [MOS-3.17 — Request audio asset](phase-3/MOS-3.17-request-audio-asset.md)
- [MOS-3.18 — Request video asset](phase-3/MOS-3.18-request-video-asset.md)
- [MOS-3.19 — Process a 2D asset delivery](phase-3/MOS-3.19-process-2d-asset-delivery.md)
- [MOS-3.2 — Draft bounded issue set](phase-3/MOS-3.2-draft-bounded-issue-set.md)
- [MOS-3.20 — Process a 3D asset delivery](phase-3/MOS-3.20-process-3d-asset-delivery.md)
- [MOS-3.21 — Process audio asset delivery](phase-3/MOS-3.21-process-audio-asset-delivery.md)
- [MOS-3.22 — Process video asset delivery](phase-3/MOS-3.22-process-video-asset-delivery.md)
- [MOS-3.23 — Request security review](phase-3/MOS-3.23-request-security-review.md)
- [MOS-3.24 — Audit implementation discipline](phase-3/MOS-3.24-audit-implementation-discipline.md)
- [MOS-3.25 — Process security review](phase-3/MOS-3.25-process-security-review.md)
- [MOS-3.26 — Process discipline audit](phase-3/MOS-3.26-process-discipline-audit.md)
- [MOS-3.27 — Review PRoject state](phase-3/MOS-3.27-review-project-state.md)
- [MOS-3.28 — Draft follow up from audit](phase-3/MOS-3.28-draft-follow-up-from-audit.md)
- [MOS-3.29 — Draft follow up from security](phase-3/MOS-3.29-draft-follow-up-from-security.md)
- [MOS-3.3 — Draft follow up issue](phase-3/MOS-3.3-draft-follow-up-issue.md)
- [MOS-3.30 — Draft manual implementation plan](phase-3/MOS-3.30-draft-manual-implementation-plan.md)
- [MOS-3.31 — Process manual implementation result](phase-3/MOS-3.31-process-manual-implementation-result.md)
- [MOS-3.4 — Draft implementation route prompt](phase-3/MOS-3.4-draft-implementation-route-prompt.md)
- [MOS-3.5 — Draft correction route prompt](phase-3/MOS-3.5-draft-correction-route-prompt.md)
- [MOS-3.6 — Draft closeout commands](phase-3/MOS-3.6-draft-closeout-commands.md)
- [MOS-3.7 — Review PR before close](phase-3/MOS-3.7-review-pr-before-close.md)
- [MOS-3.8 — Draft issue from description](phase-3/MOS-3.8-draft-issue-from-description.md)
- [MOS-3.9 — Verify post merge](phase-3/MOS-3.9-verify-post-merge.md)
- [MOS-R.22 — Public packaging safety review](phase-3/MOS-R.22-public-packaging-safety-review.md)
- [MOS-R.23 — Convert internal operations before release](phase-3/MOS-R.23-convert-internal-operations-before-release.md)
- [MOS-R.7 — Review licensing publication readiness](phase-3/MOS-R.7-review-licensing-publication-readiness.md)
- [MOS-R.8 — Process incident hotfix](phase-3/MOS-R.8-process-incident-hotfix.md)
- [MOS-R.9 — Audit docs product drift](phase-3/MOS-R.9-audit-docs-product-drift.md)

### Phase 4 — QA and human verification

- [MOS-4.1 — Draft an issue/PR QA checklist](phase-4/MOS-4.1-draft-qa-checklist-issue-pr.md)
- [MOS-4.2 — Draft QA checklist description](phase-4/MOS-4.2-draft-qa-checklist-description.md)
- [MOS-4.3 — Draft production readiness checklist](phase-4/MOS-4.3-draft-production-readiness-checklist.md)
- [MOS-4.4 — Process an issue/PR QA checklist](phase-4/MOS-4.4-process-qa-checklist-issue-pr.md)
- [MOS-4.5 — Process QA checklist feature](phase-4/MOS-4.5-process-qa-checklist-feature.md)
- [MOS-4.6 — Process production readiness checklist](phase-4/MOS-4.6-process-production-readiness-checklist.md)
- [MOS-4.7 — Draft a follow-up from QA](phase-4/MOS-4.7-draft-follow-up-from-qa.md)
- [MOS-4.8 — Draft a correction from QA](phase-4/MOS-4.8-draft-correction-from-qa.md)
- [MOS-R.19 — Plan validation cycle](phase-4/MOS-R.19-plan-validation-cycle.md)
- [MOS-R.20 — Review validation cycle readiness](phase-4/MOS-R.20-review-validation-cycle-readiness.md)
- [MOS-R.21 — Process validation cycle findings](phase-4/MOS-R.21-process-validation-cycle-findings.md)

### Phase 5 — Local, staging, and production deployment

- [MOS-5.1 — Analyze local deploy readiness](phase-5/MOS-5.1-analyze-local-deploy-readiness.md)
- [MOS-5.10 — Draft local deploy commands](phase-5/MOS-5.10-draft-local-deploy-commands.md)
- [MOS-5.11 — Execute local deploy](phase-5/MOS-5.11-execute-local-deploy.md)
- [MOS-5.12 — Draft staging deploy commands](phase-5/MOS-5.12-draft-staging-deploy-commands.md)
- [MOS-5.13 — Execute staging deploy](phase-5/MOS-5.13-execute-staging-deploy.md)
- [MOS-5.14 — Draft production deploy commands](phase-5/MOS-5.14-draft-production-deploy-commands.md)
- [MOS-5.15 — Execute production deploy](phase-5/MOS-5.15-execute-production-deploy.md)
- [MOS-5.2 — Draft local deploy checklist](phase-5/MOS-5.2-draft-local-deploy-checklist.md)
- [MOS-5.3 — Process local deploy checklist](phase-5/MOS-5.3-process-local-deploy-checklist.md)
- [MOS-5.4 — Analyze staging deploy readiness](phase-5/MOS-5.4-analyze-staging-deploy-readiness.md)
- [MOS-5.5 — Draft staging deploy checklist](phase-5/MOS-5.5-draft-staging-deploy-checklist.md)
- [MOS-5.6 — Process staging deploy checklist](phase-5/MOS-5.6-process-staging-deploy-checklist.md)
- [MOS-5.7 — Analyze production deploy readiness](phase-5/MOS-5.7-analyze-production-deploy-readiness.md)
- [MOS-5.8 — Draft production deploy checklist](phase-5/MOS-5.8-draft-production-deploy-checklist.md)
- [MOS-5.9 — Process production deploy checklist](phase-5/MOS-5.9-process-production-deploy-checklist.md)
- [MOS-R.11 — Deployment readiness review](phase-5/MOS-R.11-deployment-readiness-review.md)
- [MOS-R.12 — Draft deploy command bundle](phase-5/MOS-R.12-draft-deploy-command-bundle.md)
- [MOS-R.13 — Verify post deploy state](phase-5/MOS-R.13-verify-post-deploy-state.md)
- [MOS-R.14 — Process deployment result](phase-5/MOS-R.14-process-deployment-result.md)
- [MOS-R.15 — Draft rollback commands](phase-5/MOS-R.15-draft-rollback-commands.md)
- [MOS-R.16 — Process rollback result](phase-5/MOS-R.16-process-rollback-result.md)

### Phase 6 — Production readiness and maintenance

- [MOS-6.1 — Review security production readiness](phase-6/MOS-6.1-review-security-production-readiness.md)
- [MOS-6.10 — Process product improvements](phase-6/MOS-6.10-process-product-improvements.md)
- [MOS-6.11 — Process code improvements](phase-6/MOS-6.11-process-code-improvements.md)
- [MOS-6.12 — Process dead code cleanup](phase-6/MOS-6.12-process-dead-code-cleanup.md)
- [MOS-6.2 — Review feature gaps production](phase-6/MOS-6.2-review-feature-gaps-production.md)
- [MOS-6.3 — Analyze performance improvements](phase-6/MOS-6.3-analyze-performance-improvements.md)
- [MOS-6.4 — Analyze product improvements](phase-6/MOS-6.4-analyze-product-improvements.md)
- [MOS-6.5 — Analyze code quality gaps](phase-6/MOS-6.5-analyze-code-quality-gaps.md)
- [MOS-6.6 — Audit dead code](phase-6/MOS-6.6-audit-dead-code.md)
- [MOS-6.7 — Process security production results](phase-6/MOS-6.7-process-security-production-results.md)
- [MOS-6.8 — Process feature gap results](phase-6/MOS-6.8-process-feature-gap-results.md)
- [MOS-6.9 — Process performance improvements](phase-6/MOS-6.9-process-performance-improvements.md)
- [MOS-R.17 — Dependency security update audit](phase-6/MOS-R.17-dependency-security-update-audit.md)
- [MOS-R.18 — Secret safe config audit](phase-6/MOS-R.18-secret-safe-config-audit.md)
