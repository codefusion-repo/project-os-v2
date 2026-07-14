# Benefits, architecture, and scenarios

**What Project OS delivers, how it is built inside, and which concrete
situations it handles, with every claim anchored to a verifiable source in
the tree: a kernel key, a document, an operation, a template, or a test.**
This document compares against no external tool, promises no universal
savings, and grants no permission (`boundary.output_not_permission`): every
benefit is stated as a property of the system itself and is checked by
reading the cited source or running the indicated command.

Spanish version: [beneficios.md](../../project-os-es/docs/beneficios.md).
The technical appendix with measured sizes per hydration level is
[context-benchmark.md](context-benchmark.md).

The `rule.*`, `boundary.*`, `evidence.*`, and `output.*` keys cited below
live in [`../kernel/`](../kernel/manifest.json) and appear resolved when you
run the resolver (see [getting-started.md](getting-started.md)). The cited
tests run with `python3 -m pytest tests/ -q`.

## Verifiable benefits

1. **Human authority per action.** No text in the system authorizes
   anything: writing requires exact PM approval naming project, work unit,
   and action, and merge, close, labels, tags, releases, settings, and
   secrets each require their own separate approval. Source:
   `rule.no_autorizacion`, `boundary.separate_pm_approval`, and
   `evidence.pm_approval`; the PM-facing detail is in [rules.md](rules.md).
2. **GitHub as live project state.** Issues, PRs, branches, commits,
   reviews, and their checks are read live at task time; durable files never
   store that data, so they neither age nor contradict reality. Source:
   `rule.estado_vivo_no_durable`, `rule.trazabilidad_viva`, and
   `boundary.no_live_state_durable`.
3. **Cold-resume continuity.** Any new session rebuilds the project by
   resolving the kernel and reading GitHub: nothing depends on one previous
   chat's memory. Source: the `resolution_sequence` in the
   [manifest](../kernel/manifest.json) plus `rule.trazabilidad_viva`; guided
   transfer exists as
   [MOS-0.6](../operations/phase-0/MOS-0.6-handoff-session-context.md).
4. **Switching agents or providers without loss.** The contract is the same
   whichever agent resolves the kernel: switching tools means switching
   adapters, not process. Source: the
   [`AGENTS.target.md`, `CLAUDE.target.md`, `GEMINI.target.md`, and
   `BROWSER_CHAT.target.md`](../adapters/README.md) adapters boot different
   surfaces onto the same kernel; ES/EN equivalence is guarded by
   `tests/test_project_os_bilingual_parity.py`.
5. **Alignment with roadmap, issues, and ADRs.** Every work unit is born
   from existing traceability — the canonical roadmap or an issue — and
   durable decisions become ADRs. Source:
   [MOS-3.1](../operations/phase-3/MOS-3.1-draft-next-issue-from-traceability.md),
   [MOS-3.8](../operations/phase-3/MOS-3.8-draft-issue-from-description.md),
   [MOS-R.1](../operations/phase-2/MOS-R.1-record-adr-decision.md), and this
   repo's ADRs in
   [`docs/decisions/`](../../docs/decisions/0004-public-presentation-and-packaging.md).
6. **End-to-end traceability.** Work is tracked from issue to merge with
   scoped `work/<unit>-<slug>` branches and live records, and traceability
   itself is auditable as an operation. Source: `rule.trazabilidad_viva`,
   `rule.preflight`, and
   [MOS-3.13](../operations/phase-3/MOS-3.13-audit-traceability.md).
7. **Fail-closed by design.** On a missing kernel, ambiguous authority,
   missing required inputs, or failed checks, the agent stops with an
   unresolved status instead of guessing and continuing. Source:
   `rule.resolucion_fail_closed`, `boundary.fail_closed`, and the
   `status.blocked` / `status.needs_pm_decision` / `status.needs_context`
   statuses; the resolver itself fails closed on unknown values
   (`tests/test_project_os_bilingual_parity.py::test_unknown_skill_and_unallowed_kernel_paths_fail_closed`).
8. **Security and secret safety.** Requesting, printing, committing, or
   logging secrets and sensitive data is forbidden; values are redacted as
   `[REDACTED]` and only paths, variable names, and risk types are reported.
   Source: `rule.secret_safety` and `boundary.security_privacy`; responsible
   reporting lives in [SECURITY.md](../../SECURITY.md).
9. **Risk-proportional checking.** Verification grows with the risk of the
   change (kernel, secret handling, and deployment-shaped changes require
   agent-run checks; clarity and product judgment stay with the PM), and
   nothing is declared done without reporting it. Source:
   `rule.validacion_proporcional`, `boundary.validation_discipline`, and
   `evidence.validation_output`.
10. **Review-before-close.** Closing requires comparing the work unit
    against the diff, the final files, the check results, and the risks; a
    PR body is a claim, not proof. Source: `boundary.review_before_close`
    and [MOS-3.7](../operations/phase-3/MOS-3.7-review-pr-before-close.md).
11. **Human QA from the browser.** A person without a terminal drafts and
    processes QA checklists from browser chat, on a read-only, draft-only
    surface. Source:
    [MOS-4.1](../operations/phase-4/MOS-4.1-draft-qa-checklist-issue-pr.md),
    [MOS-4.4](../operations/phase-4/MOS-4.4-process-qa-checklist-issue-pr.md),
    [MOS-4.5](../operations/phase-4/MOS-4.5-process-qa-checklist-feature.md),
    and the [BROWSER_CHAT.target.md](../adapters/BROWSER_CHAT.target.md)
    adapter.
12. **Standard summaries.** Execution reports, status results, and PR bodies
    follow fixed templates, so the PM always reads the same shape: what
    changed, what was checked, what is missing, and what risk remains.
    Source: `output.execution_report` and `output.status_result` with their
    templates [execution-report.md](../templates/execution-report.md),
    [status-result.md](../templates/status-result.md), and
    [pull-request.md](../templates/pull-request.md).
13. **Reusable governance across projects.** The kernel is
    project-agnostic: the same contract is adopted by copy into another
    repository without rewriting it, and repository specifics stay in its
    bootloader. Source: the [manifest](../kernel/manifest.json) objective,
    copy-based adoption in [getting-started.md](getting-started.md), and
    [MOS-0.3](../operations/phase-0/MOS-0.3-adopt-existing-project.md).

## Modular architecture

Each piece has one responsibility and can be read on its own:

- **Per-tuple kernel + deterministic resolver.** A small JSON set defines
  actors, modes, workflows, rules, boundaries, required inputs, outputs, and
  statuses; the resolver hydrates only the requested
  `(actor, workflow, mode)` tuple, at `minimal` / `compact` / `full/debug`
  levels, granting no permission. No level drops boundaries or secret
  safety (`tests/test_project_os_hydration_levels.py`); measured sizes live
  in the [context-benchmark.md](context-benchmark.md) appendix.
- **Hierarchical shims.** Per-tool shims (`CLAUDE.md`, `GEMINI.md`) stay
  minimal and delegate to one terminal bootloader (`AGENTS.md`), which in
  turn points at the kernel: a single boot chain, with no duplicated
  contract. Source: [CLAUDE.target.md](../adapters/CLAUDE.target.md) and
  [AGENTS.target.md](../adapters/AGENTS.target.md).
- **Thin target-specific adapters.** A target's adapter carries only
  identity and machine/adoption configuration (paths, default branch, PM
  language) plus pointers to live sources; never live task data or contract
  copies. Source: [adapters/README.md](../adapters/README.md) and
  `tests/test_adapter_contract.py`.
- **On-demand operations, templates, and skills.** The MOSDLC catalog,
  artifact templates, and optional skills load only when used; the resolver
  returns them as resolvable references, not inlined. Source:
  [operations/README.md](../operations/README.md),
  [templates/README.md](../templates/README.md), and
  [`../kernel/skills.json`](../kernel/skills.json).
- **MOSDLC lifecycle.** Operations cover the full cycle per phase —
  adoption, requirements, design, implementation, verification, release, and
  operation — plus cross-phase operations; the day-to-day cycle is in
  [rhythm.md](rhythm.md).
- **Three separate planes.** The **contract** (versioned, test-guarded
  kernel JSON), the **target configuration** (per-repo bootloader/adapters),
  and the **task state** (GitHub, read live) never mix: that is why the
  contract is portable, the adapter is small, and task state never ages
  inside a file. Source: `rule.fuente_canonica`,
  `rule.estado_vivo_no_durable`, and
  [adapters/README.md](../adapters/README.md).

## Verifiable scenarios

Each scenario names the situation, what the system does, and how to check it
on your own project.

1. **The chat was lost.** The previous session closed, expired, or broke. A
   new session re-resolves the kernel and rebuilds from GitHub; when useful
   context remains, it is transferred with
   [MOS-0.6](../operations/phase-0/MOS-0.6-handoff-session-context.md).
   Check: open a clean session and ask it to reconstruct an in-flight issue;
   nothing in the result depends on the lost chat.
2. **Handoff to another person or session.** The work is documented on the
   issue/PR with standard summaries, and the handoff packet has a template
   ([handoff-packet.md](../templates/handoff-packet.md)); the receiver
   repeats the same startup as scenario 1. Check: the receiver never needs
   access to the original conversation.
3. **Switching agents or providers.** Adopt the new tool's adapter and it
   resolves the same kernel: same rules, boundaries, required inputs, and
   statuses. Check: resolve the same tuple with two different agents and
   compare the hydrated contract; it is the same JSON.
4. **PM approval is missing.** An agent ready to write but without exact
   approval must stop: `evidence.pm_approval` is a required input with
   `missing_status: status.blocked`. Check: request an implementation
   without granting approval; the correct output is a blocked status naming
   the gate, not a commit.
5. **An out-of-scope finding appears.** The agent never fixes it silently:
   `boundary.implementation_discipline` keeps the change inside the live
   scope, and the fix is routed traceably with
   [MOS-3.5](../operations/phase-3/MOS-3.5-draft-correction-route-prompt.md)
   or as a follow-up with
   [MOS-3.3](../operations/phase-3/MOS-3.3-draft-follow-up-issue.md).
   Check: the PR diff contains no files outside the issue's scope.
6. **Human QA before closing.** The PM drafts the QA checklist from the
   browser
   ([MOS-4.1](../operations/phase-4/MOS-4.1-draft-qa-checklist-issue-pr.md)),
   a person runs it, the result is processed
   ([MOS-4.4](../operations/phase-4/MOS-4.4-process-qa-checklist-issue-pr.md)),
   and corrections come from
   [MOS-4.8](../operations/phase-4/MOS-4.8-draft-correction-from-qa.md); the
   PR also passes review-before-close
   ([MOS-3.7](../operations/phase-3/MOS-3.7-review-pr-before-close.md))
   ahead of the merge. Check: the issue/PR keeps the checklist and its
   result as live records.

## Current capabilities and the future CLI

Everything described above exists in this tree today and is operated like
this:

- **Copy-based adoption:** copy the target adapters
  ([getting-started.md](getting-started.md)); there is no installer or
  package.
- **Terminal:** repo-local Python resolver
  (`tools/project_os_resolve.py`).
- **Browser chat:** manual resolution from the
  [manifest](../kernel/manifest.json), always read-only/draft-only.

An onboarding CLI is future work **deferred by durable decision** (ADR 0003,
[0003-project-os-cli-adoption-model.md](../../docs/decisions/0003-project-os-cli-adoption-model.md),
reaffirmed by ADR 0004): it is only reconsidered with real adoption
signals, as its own design issue. This document does not present it as a
current capability, and no part of the system requires it to operate.
