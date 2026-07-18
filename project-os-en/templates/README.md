# Non-operational templates

Compact English templates for artifacts that Project OS may draft, create,
trace, or document. They are shape contracts: they do not contain workflow
logic, read live state, or grant permission. Skills live separately as optional
agent capabilities under `project-os-en/skills/`; they are not templates or
artifacts.

The `project-os-en/kernel/artifacts.json` catalog links each artifact to
exactly one `required_template`. The resolver exposes those references
without copying template contents.

Every output references `context_receipt.minimum_read_surface`. The agent keeps
the internal receipt intact with the canonical kernel fields and applies
`pm_facing_visibility`: it omits the marked block from PM-facing Markdown in
`minimal` and `compact`, and shows it in full in the `full/debug` envelope. The
`context-receipt:*` comments are control syntax: always remove them and never
include them in PM-facing Markdown. The
receipt records repository-relative paths or live identifiers and reasons,
never absolute machine paths, bodies, secrets, or durable live state. When an
artifact requires an exact body—such as a route prompt—the receipt remains
outside that body and does not alter it.

## Operating bridge

- PM-facing map: `project-os-en/docs/README.md`.
- Action entry point: `project-os-en/operations/README.md`.
- Adoption bootloaders: `project-os-en/adapters/README.md`.
- Artifact catalog: `project-os-en/kernel/artifacts.json`.
- Optional skill catalog: `project-os-en/kernel/skills.json`.
- Compact skill files: `project-os-en/skills/`.
- `required_template` hydration: `tools/project_os_resolve.py`.

## Catalog

- `project-os-en/templates/route-prompt.md`: scoped routing to another
  surface; may recommend an optional skill and terminal-agent family without
  making either binding.
- `project-os-en/templates/pm-command-bundle.md`: the single canonical source
  for copy-safe PM command shape and style.
- `project-os-en/templates/issue.md`: issue body.
- `project-os-en/templates/pull-request.md`: PR body.
- `project-os-en/templates/closure-comment.md`: closure comment and
  reconstruction.
- `project-os-en/templates/adr.md`: durable decision.
- `project-os-en/templates/roadmap.md`: canonical roadmap.
- `project-os-en/templates/execution-report.md`: execution report.
- `project-os-en/templates/review-result.md`: review result.
- `project-os-en/templates/status-result.md`: unresolved status.
- `project-os-en/templates/manual-implementation-plan.md`: human-executable
  plan.
- `project-os-en/templates/asset-prompt.md`: asset request for an external
  recipient.
- `project-os-en/templates/security-review-prompt.md`: OWASP review request.
- `project-os-en/templates/handoff-packet.md`: session-to-session transfer.
- `project-os-en/templates/adoption-packet.md`: target adoption report.
