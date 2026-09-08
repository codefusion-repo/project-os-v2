# MOSDLC operations — compact English surface

This directory is the English PM-facing MOSDLC (Modern AI SDLC Operations) catalog. Each file is a compact operation prompt defining its outcome, variables, evidence, output, and safe connections. Stable MOS codes, variables, and kernel references match the default Spanish catalog.

## Common contract

1. Resolve `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. The resolver provides guidance and never reads live state or grants permission.
2. Reconstruct issues, PRs, branches, commits, and validation from target systems of record at task time. Durable files never store live state.
3. Validate in proportion to risk: agent-run checks, drafted PM-run commands, manual PM validation, or a justified omission. Running validation is not creating tests or tooling, and the change class (reading, small, standard, critical) governs unit, PR, review, and output density.
4. Use only the context and subagents the scope needs without dropping evidence, validation, secret safety, or exact approval. Before creating a finding, follow-up, or unit, apply the materiality gate from `rule.economia_de_contexto`: require a verifiable current state, an unsatisfied outcome, contract, or risk, a concrete action, and durable independent value; anything historical, informational, already resolved, or duplicated is omitted.
5. Resolve artifacts and their `required_template` paths from `project-os-en/kernel/artifacts.json`.
6. Treat `project-os-en/kernel/skills.json` capabilities as optional and outside workflow logic.
7. Templates, outputs, variables, and route prompts never authorize. Browser chat stays draft-only.
8. Fail closed on missing or ambiguous kernel data, missing minimum or material evidence, unsatisfied hard gates, ambiguous authority, or missing or failed required validation. Missing auxiliary evidence does not block by itself: it follows the canonical gap contract only for declared read-only or draft-only outputs that allow safe degradation. Before any mutation, fully revalidate every gap and satisfy all material evidence, hard gates, authority, and required validation.
9. Never request or expose secrets; use `[REDACTED]` and report only names, paths, commands, and risk types.
10. `PM_FEEDBACK_HUMANO` and `PM_QUESTION_HUMANO` are optional PM context and never authorization.
11. PM-facing operations with `PM approval: Yes` consume
    `rule.precedencia_decision_pm` from the shared kernel: a later decision
    supersedes another only for the same `decision_key`; separate limits and
    gates remain in force.
12. Read PM instructions, units, and findings by intent per
    `boundary.implementation_discipline`: only authorization and allowed
    actions, target identity, hard constraints, scope and out of scope,
    security, and expressly binding decisions are literal; examples,
    hypotheses, preferences, tentative names, and implementation proposals are
    advisory and are never copied automatically into rules, fields, files, or
    tests.

## Primary work unit continuity

Reconstruct `WORK_UNIT` and its live relations before continuing: outcome,
scope, criteria, `CHANGE_CLASS`, existing PR and branch when applicable, and the
review or QA source. Planning, implementation, review, QA, correction,
re-review, handoff, and closeout retain that unit while completing the same
outcome. Changing phase, agent, or session, producing an output or checklist,
or correcting the same PR creates neither another unit nor another PR. Reuse
verifiable references without asking for reconstructible identifiers; a missing
or ambiguous material relation fails closed. Add no lifecycle registry or
durable state.

Continuity neither expands scope nor shares authorization: every material
action retains its exact approval, evidence, preflight, validation, and review.
A blocker for the same outcome retains unit, PR, class, and scope through
MOS-3.5, including its QA source; a follow-up from any origin consumes MOS-3.3.
QA and audit are not sufficient reasons to create work.

Before another unit, check materiality and independence through MOS-3.3 and
group findings sharing one outcome and exit criteria. Separate distinct
observable results with their own criteria, independent prioritization, or work
unnecessary to complete the current outcome; do not absorb work requiring a
separate material decision or a different authorization/security boundary.
Resolve that separate scope and its gates before acting. Fewer units never
justify mega-issues or scope creep. Separate permission for an action already
belonging to the same outcome does not itself create another unit.

## QA → release → deployment continuity

The same unit rule covers readiness, release, local deployment, staging,
production, rollback, and verification of the same outcome. Reconstruct the
unit even if its PR was merged or closed; closure does not prove that the target
environment was reached. Do not open another unit or PR for a transition. A gap
requiring code returns to the applicable correction route and its approval;
do not treat a closed PR as editable. An independent outcome follows MOS-3.3.

Start from the already identifiable QA, review, release, or deployment result
and follow its live relations. Retain verifiable outcome, criteria, class,
target, ref, and intended environment; ask only for a missing material decision
or source. Success in one environment does not select the next. Handoffs and
agent changes carry references, not a new transcription or readiness snapshot.

### Reusable evidence

Before each transition check the live source and its applicability to the
current action. In the existing output's evidence, state what is reused, what
is renewed and why, with verifiable source, ref, environment, and coverage when
applicable. Revalidating a source need not rerun a still-valid test.

| Existing evidence | Retain when | Renew or block when |
| --- | --- | --- |
| Scope and criteria (`evidence.issue_scope` / `evidence.source_basis`) | Outcome and criteria remain current in the same unit. | Scope changes or a verifiable material relation is missing. |
| Accepted QA and review dispositions | The source identifies covered criteria, ref, and environment; acceptance and dispositions still apply. | Coverage changes, risk increases, or a PM decision conflicts. Pending/failed QA never becomes PASS; an accepted risk retains its scope and exempts no hard gate. |
| `evidence.validation_output` | Verifiable result for the same exact SHA/ref and required coverage, with applicable environment/conditions. Equivalent CI meets the same limits. | New code/ref, environment, or risk requires affected tests; expired/unreadable sources or insufficient coverage prevent reuse. Validation of another head, including pre-merge, never certifies the current ref; validate the resulting ref. |
| `evidence.exact_ref` | Immutable identity remains verifiable from the target source. | Verify again for every action requiring it: a moving branch or tag does not prove the SHA; change or mismatch invalidates dependent claims. |
| `evidence.repo_state` | Reconstructed live for the action, including applicable relations, diff, merge, and checks. | A previous report replaces neither current state nor preflight before writes. |
| `evidence.target_adoption` | Adapter, `Project-specific notes`, commands, and constraints remain current for that target and environment. | Adoption, configuration, or commands change; target-owned paths are missing or ambiguous. Never inspect secret values to fill the gap. |
| Readiness / `evidence.deployment_readiness` | Its checks still cover the required target, ref, environment, risk, rollback, and postconditions. | Reassess when any of these or an applicable decision changes; staging health does not certify production, and post-deploy verification must cover the current deployment. |
| Applicable durable PM decisions and `evidence.pm_approval` | Source, temporal order, and exact `decision_key` still govern the action under the kernel. | A later conflicting decision needs PM resolution; permission for another action/target/environment/ref does not transfer. Evidence reuse never expands authority. |

Renew only affected evidence, with verifiable justification: retain stable
criteria and environment-independent tests of the same ref, but add checks for
the new environment and increased risk. If independence cannot be established,
renew before advancing. Add no cache, registry, persistent fields, or durable
lifecycle state to the existing contracts.

### Next action and gate

Show a short route to the intended environment in the applicable output, with
only actions the outcome needs. For every material action identify unit,
target, ref, environment when applicable, responsible party, evidence/validation,
current or pending exact authorization, rollback/recovery, and postconditions.
Use `not applicable` with a reason where appropriate. This map is execution
evidence, not a new artifact or durable plan.

| Action | Existing contract and gate | Recovery and verification |
| --- | --- | --- |
| Merge | MOS-3.7: class-level review and required QA on the current head; GO delivers closeout under its contract, executed by Human PM. Outside that contract retain exact merge approval. | Target-specific reversal; verify merge and resulting ref. GO authorizes no tag, Release, or deploy. |
| Tag | MOS-3.10 → MOS-3.11: readiness of the resulting ref and exact PM approval for tag and push; Human PM executes. | Verify tag/ref identity; never move or delete it as implicit recovery. |
| GitHub Release | MOS-3.10 → MOS-3.12: verified tag/ref, notes, and exact Release approval; Human PM executes. | Verify object and tag; editing/deleting artifacts needs its own decision. |
| Configuration/settings | Existing target route, exact approval for that write, and compatible surface; secret and production limits remain. | Target-owned recovery and configuration checks without sensitive values. |
| Local deploy | MOS-R.11 → MOS-R.12; MOS-5.11 only with supported target, owned commands, and exact local authorization. | Applicable rollback and MOS-R.13 on the deployed ref. |
| Staging deploy | MOS-R.11 → MOS-R.12; MOS-5.13 only with supported target and exact staging authorization, without inheriting local permission. | Staging rollback and MOS-R.13 with environment-specific checks. |
| Production deploy | MOS-5.7/5.8/5.9 → MOS-5.14 → MOS-5.15: production readiness and required human checks; exact approval and execution by Human PM. | Prepared production rollback and MOS-R.13 verification; staging PASS grants neither permission nor production readiness. |
| Rollback | MOS-R.14 → MOS-R.15: decision and exact approval for target/environment/action/recovery ref; Human PM executes. | Tested target-owned route; MOS-R.16 verifies restored ref and health. Never automatic. |
| Post-deploy verification | MOS-R.13, read-only, target-owned checks of observed target/environment/ref; authorizes no corrections. | On failure MOS-R.14 determines the route; no recovery runs by inference. |

Compose these operations in the same response when evidence and decisions
suffice, resolving each output's workflow/actor/mode before using it. Ask for no
additional MOS selection or reconstructible locator. MOS-R.11 owns the shared
environment review; MOS-R.12 owns shared drafting. MOS-5.* entry points delegate
to them and retain human checklists when checks are actually missing. QA and
release retain MOS-4.4, MOS-3.7, and MOS-3.10–MOS-3.12; release is not mandatory
if the target does not require it.

This does not chain writes: stop at the first pending material authorization,
failed readiness, unverifiable ref, failed/missing required validation,
missing environment evidence or missing/ambiguous commands, undefined mandatory
rollback, or unresolved secret/configuration boundary. Report the gate and next
safe action with `output.status_result`; do not combine actions separated by a
pending gate in an executable block. A permitted draft clearly identifies its
pending execution approval. Local/staging require resolving `workflow.deployment` /
`mode.delegated_deploy_execution`, preflight, and exact approval before executing
one environment at a time. Production remains Human PM; browser chat only reads
or drafts. Passing one gate neither executes nor authorizes the next.

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

## Canonical operations and aliases

Each canonical operation keeps its complete prompt and stable operational
identity in its own Markdown file. When compatible historical codes exist, the
canonical file's `project-os-operation` metadata declares `canonical_code`,
`operation_id`, `aliases`, `deprecation`, and `compatibility_reason`. A
maintenance alias that binds its historical focus also declares
`alias_focus_area`. An alias
file is only a stub pointing through `alias_of`; it never repeats workflows,
modes, outputs, evidence, approval, variables, or connections. The canonical
Markdown is therefore the single source of operational semantics.

The confirmed pairs are `MOS-0.4` (canonical) / `MOS-R.10` (supported,
non-deprecated historical alias) and `MOS-3.14` (canonical for every audit) /
`MOS-6.11` (compatible historical code-improvement entry point). Normal wizard
views show only canonicals, but an explicit alias selection by code, filename, or
path reports the canonical code and renders exactly its contract and variables.

`MOS-6.13` is the canonical maintenance-improvement analysis operation. Its
supported aliases `MOS-6.3`, `MOS-6.4`, and `MOS-6.5` bind
`FOCUS_AREA=performance`, `product`, and `code_quality` respectively, without
duplicating the contract or asking for that focus again.

The initial audit classified the asset request/delivery families
(`MOS-3.15`–`MOS-3.22`), environment-specific deploy flows (`MOS-5.*`), and the
draft/update or analysis/processing pairs in requirements, design, and
maintenance as related but materially distinct. Their purposes, inputs,
artifacts, or environments differ, so they are not aliases. Catalog guards
reject dangling, ambiguous, or cyclic aliases,
copied contracts in stubs, ES/EN drift, and two canonicals for one identity. An
additional undeclared contractual match returns `status.needs_pm_decision` and
is never merged automatically.

## PM-facing inputs and derived metadata

An operation asks only for what the AI cannot reconstruct unambiguously. Every
active variable is classified into one of these categories before it is kept,
made optional, derived, or removed:

1. **Human decision or constraint.** Exact PM authorization, product decisions,
   scope or constraints absent from live evidence, and explicit overrides
   admitted by the contract. These always need the human: live evidence cannot
   substitute for them.
2. **Primary locator.** At most one live reference per evidence chain, and only
   when the current invocation does not already identify the source. The live
   unit, the live result —audit, QA, security review, design delivery,
   checklist, manual implementation, deployment— or the equivalent target record
   all serve equally: when an operation accepts an issue or a PR, either one is a
   sufficient primary locator if it carries enough evidence.
3. **Derived metadata.** The repository, the related issue or unit, the PR, the
   source review or comment, the roadmap, the existing or derivable scoped
   branch, `CHANGE_CLASS`, and any other identifier or
   relation verifiable from the locator. It is never a manual input: browser chat
   reconstructs it from live evidence and shows it already resolved in the route
   prompt, bundle, or report whenever the receiver must verify it.
4. **Optional human context.** `PM_FEEDBACK_HUMANO`, `PM_QUESTION_HUMANO`,
   `OPTIONAL_SKILL`, and other non-authorizing preferences. They are human
   choices, not derivable metadata, which is why they stay inputs.
5. **Over-required input.** Data an operation demands without needing it to
   start or safely complete its basic behavior. It is removed or made optional;
   its absence must never block a safe scenario.

Precedence when resolving any of those variables:

1. Reuse an unambiguous source already present in the execution context.
2. If none exists, ask for at most one primary locator per evidence chain.
3. Reconstruct from it the repository, issue, PR, roadmap, branch, class, and
   verifiable relations.
4. Show the derived values in the output whenever the receiver must inspect them.
5. Ask for extra data only on real material ambiguity.
6. Never derive or self-assign PM authorization.

`CHANGE_CLASS` is a reconstructible property of the unit —derived from its scope,
risk, and affected surfaces, and preserved across intake, implementation, review,
closeout, and verification— that governs the material gates and the execution
report density; `HYDRATION_LEVEL` is not derived from it. The resolver applies
`compact` by default for every class. That is why the wizard for `MOS-3.4` and
`MOS-3.5` captures only human inputs: the locator when
needed, `OPTIONAL_SKILL`, PM feedback or questions,
`PM_AUTHORIZATION_STATUS`, and, only on an `output.route_prompt` path, the
explicit override. Hydration keeps a single category-1 override route:
`/hydration <level>` in the wizard records an exact PM decision and writes it as
`HYDRATION_LEVEL` in the INPUT block only when an `output.route_prompt` is
confirmed. That override may select any of the three levels with no ranking
derived from the class, changes no gate or authority, and it is not a routine
question: without it the variable is neither asked for nor carried.
`RECOMMENDED_TERMINAL_AGENT_FAMILY` is inferred as separate advice, never asked
of the PM, and never authorizes a tool or action.

No derived value grants permission and authorization is never inferred. The
decision returns to the PM with `status.needs_context` or
`status.needs_pm_decision` only on real material ambiguity —incompatible sources
equally active, unverifiable relations, a scope that does not allow determining
the class, a missing formal unit for a class that requires one, a conflict between
live evidence and a later PM decision, or authorization that is absent, pending,
or out of scope—, never because the PM did not retype a reconstructible
identifier, class, branch, or density.

A repo-wide locator is kept whenever it is the only source of scope: audits,
adoptions, readiness checks, and cycles that are deliberately repo-wide keep
declaring `TARGET_REPOSITORY` because no other evidence identifies their reach.

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
  - Compatible alias: [MOS-R.10](phase-0/MOS-R.10-update-target-adapters-catalog.md)
- [MOS-0.5 — Verify target adoption](phase-0/MOS-0.5-verify-target-adoption.md)
- [MOS-0.6 — Handoff session context](phase-0/MOS-0.6-handoff-session-context.md)
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
- [MOS-3.14 — Process audit result](phase-3/MOS-3.14-process-audit-result.md)
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
- [MOS-3.27 — Review project state and verify postconditions](phase-3/MOS-3.27-review-project-state.md)
- [MOS-3.3 — Draft a follow-up](phase-3/MOS-3.3-draft-follow-up-issue.md)
- [MOS-3.30 — Draft manual implementation plan](phase-3/MOS-3.30-draft-manual-implementation-plan.md)
- [MOS-3.31 — Process manual implementation result](phase-3/MOS-3.31-process-manual-implementation-result.md)
- [MOS-3.4 — Draft implementation route prompt](phase-3/MOS-3.4-draft-implementation-route-prompt.md)
- [MOS-3.5 — Draft correction route prompt](phase-3/MOS-3.5-draft-correction-route-prompt.md)
- [MOS-3.7 — Review PR before close](phase-3/MOS-3.7-review-pr-before-close.md)
- [MOS-3.8 — Draft issue from description](phase-3/MOS-3.8-draft-issue-from-description.md)
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
- [MOS-5.15 — Production deploy (Human PM)](phase-5/MOS-5.15-execute-production-deploy.md)
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
- [MOS-6.11 — Compatible alias of MOS-3.14](phase-6/MOS-6.11-process-code-improvements.md)
- [MOS-6.12 — Process dead code cleanup](phase-6/MOS-6.12-process-dead-code-cleanup.md)
- [MOS-6.2 — Review feature gaps production](phase-6/MOS-6.2-review-feature-gaps-production.md)
- [MOS-6.3 — Performance-analysis alias](phase-6/MOS-6.3-analyze-performance-improvements.md)
- [MOS-6.4 — Product-analysis alias](phase-6/MOS-6.4-analyze-product-improvements.md)
- [MOS-6.5 — Code-quality-analysis alias](phase-6/MOS-6.5-analyze-code-quality-gaps.md)
- [MOS-6.6 — Audit dead code](phase-6/MOS-6.6-audit-dead-code.md)
- [MOS-6.7 — Process security production results](phase-6/MOS-6.7-process-security-production-results.md)
- [MOS-6.8 — Process feature gap results](phase-6/MOS-6.8-process-feature-gap-results.md)
- [MOS-6.9 — Process performance improvements](phase-6/MOS-6.9-process-performance-improvements.md)
- [MOS-6.13 — Analyze maintenance improvements](phase-6/MOS-6.13-analyze-maintenance-improvements.md)
- [MOS-R.17 — Dependency security update audit](phase-6/MOS-R.17-dependency-security-update-audit.md)
- [MOS-R.18 — Secret safe config audit](phase-6/MOS-R.18-secret-safe-config-audit.md)
