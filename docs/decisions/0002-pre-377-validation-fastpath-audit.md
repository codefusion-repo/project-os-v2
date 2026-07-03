# ADR 0002 — Pre-#377 audit: proportional-validation and fast-path source-of-truth layering is safe

- Status: accepted (resolves issue #387; no code/docs correction required).
- Scope: audits the #380 proportional-validation implementation (PR #384) and
  the #378 fast-path/source-of-truth implementation (PR #381) as the
  prerequisite gate for #377.
- Source basis: roadmap #274; issue #387; issue #380 / PR #384; issue #378 /
  PR #381; issue #385 / PR #386 (Fase 6 migration, the trigger that made #377
  eligible); `kernel/manifest.json`; `tools/project_os_resolve.py`;
  `docs/TRACEABILITY_PROTOCOL.md`; `docs/VALIDATION_POLICY.md`;
  `docs/CONTEXT_ECONOMY.md`; `templates/route-prompt.md`;
  `templates/pm-command-bundle.md`; `docs/MOSDLC_TEMPLATE_STANDARD.md`;
  `docs/PM_OPERATIONS.md`; `docs/OPERATION_FLOWS.md`; `tests/test_resolver.py`;
  `tests/test_validation_policy.py`.
- Non-authorization: this ADR documents a decision and an audit finding; it
  grants no write permission, merge, closure, or settings authority
  (`boundary.output_not_permission`). Authority comes only from exact scoped
  PM approval plus the kernel-resolved gates for the specific action.

## Context

#377 will compact migrated MOSDLC operation prompts and audit which repeated
responsibilities the resolver/kernel layer should own instead of individual
templates. The PM asked for a prerequisite audit of #380 and #378 first: if
either left unclear layering, duplicated rules, weak source-of-truth
boundaries, or missing tests, #377 could compact the wrong content or move a
responsibility to the wrong layer.

This audit re-read the current (post-#384, post-#381, post-#386) state of the
validation-policy and fast-path/traceability implementation directly from the
repository, not from PR bodies or prior reports, and checked it against #380's
and #378's own acceptance criteria.

## Decision

**#380 (proportional validation) is coherent, centralized, and safe for #377
to rely on.**

- `docs/VALIDATION_POLICY.md` is the single canonical home for validation
  categories (agent-run required, PM-run drafted, manual PM, no automated
  validation), the mandatory agent-run list, test add/remove criteria,
  target-repository behavior, and review-before-close acceptance.
- `boundary.validation_discipline` states the hard floor and points to
  `docs/VALIDATION_POLICY.md` for detail via its `notes` field; it does not
  restate or compete with the policy doc.
- `templates/route-prompt.md`, `docs/MOSDLC_TEMPLATE_STANDARD.md`,
  `docs/PM_OPERATIONS.md`, `docs/OPERATION_FLOWS.md`, `AGENTS.md`, and
  `adapters/*.target.md` reference the policy doc and classify validation
  (agent-run / PM-run / manual / none) instead of defaulting to a full suite
  or new tests per change.
- `tests/test_validation_policy.py` guards the categories, the mandatory-list
  wording, route/review-prompt classification without blanket defaults,
  target-adapter non-imposition of Project OS-specific tests, and removal of
  the "a new MOSDLC phase always needs a new test file" assumption.

**#378 (fast-path / resolver source-of-truth) is coherent, operational,
non-authorizing, and safe for #377 to rely on.**

- `tools/project_os_resolve.py` emits `operative_guidance` (states the
  resolved actor/workflow/mode/evidence/boundaries/output entries are
  operative task guidance, not mere context) and `live_traceability` (a
  compact, evidence- and workflow-derived live-read checklist with an
  explicit `resolver_role: emit_obligations_only_no_github_or_git_fetch`) on
  every resolution, plus a standing `non_authorization` notice. It performs no
  GitHub or git I/O; it only reads kernel JSON under `--kernel-dir`.
- This matches `kernel/manifest.json`'s `resolution_strategy`,
  `resolution_sequence`, and `source_of_truth` block, and expands
  `docs/TRACEABILITY_PROTOCOL.md`'s seven rules without overriding them.
- `tests/test_resolver.py` covers the three workflows #378's acceptance
  criteria named — `workflow.issue_implementation` with
  `mode.delegated_commit_pr`, `workflow.review_before_close` with
  `mode.review_only`, and `workflow.pm_intake` with `mode.review_only` —
  asserting the non-authorization notice, the `operative_guidance` shape, and
  the `live_traceability` reads all survive resolution.

**The layering #377 must respect is:**

- `kernel/manifest.json` owns load order, `resolution_strategy`,
  `resolution_sequence`, `source_of_truth` pointers, and the canonical
  non-authorization statement.
- `tools/project_os_resolve.py` (the resolver) owns turning that manifest into
  a per-task `operative_guidance` / `live_traceability` packet from kernel
  JSON only; it never fetches GitHub/git state and never becomes a workflow
  engine.
- `docs/TRACEABILITY_PROTOCOL.md` owns the seven live-reconstruction rules the
  resolver's `live_traceability` packet expands from.
- `docs/VALIDATION_POLICY.md` owns validation categories, the mandatory
  agent-run list, and test add/remove criteria.
- `docs/CONTEXT_ECONOMY.md` owns context classes and subagent discipline.
- `templates/route-prompt.md` and `templates/pm-command-bundle.md` own the
  PM-facing route-prompt/command-bundle shape and variants, citing the docs
  above instead of restating them.
- `templates/mosdlc/operations/fase-<n>/` and the numbered `templates/operations/`
  catalog (`00`-`37`) own task-specific operation prompts: each resolves
  `kernel/manifest.json` and cites `docs/VALIDATION_POLICY.md`'s categories
  instead of defaulting to a full suite or new tests.
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `adapters/*.target.md` stay
  compact bootloaders that point back to `kernel/manifest.json` and the
  canonical docs above; they store no live issue/PR/branch/validation state.

**No narrow correction is required.** The audit found no duplicated or
conflicting source-of-truth statements between these layers, no stale
full-suite/new-test defaults, no resolver GitHub/git fetch, and no gap against
#380's or #378's own acceptance criteria.

#377 may proceed. It should use the layering map above when deciding which
repeated MOSDLC template block to reference compactly instead of restate, and
it does not need to reopen #380 or #378 to do so.

## Consequences

- #377 can compact repeated MOSDLC boilerplate by pointing to the owning layer
  identified above, instead of re-deriving or re-litigating #380/#378.
- This ADR changes no kernel, resolver, or test behavior; validation was kept
  proportional to a docs-only, no-op audit finding: `git status --short
  --branch` and `git diff --check` only. `python3 -m tools.validate_kernel`
  and the full test suite were run as read-only audit evidence (kernel valid,
  0 findings; 356 passed) and are not re-required by this change since no
  kernel JSON, resolver, or test file changed.
- Rollback is deleting this ADR file; it records a decision, not a behavior
  change, so reverting has no functional effect on the kernel, resolver, or
  tests.
