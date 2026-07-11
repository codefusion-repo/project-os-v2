# Getting started

## Choose the language surface

Spanish is the default: omit `--kernel-dir` or select `project-os-es/kernel`. Select English only by passing `--kernel-dir project-os-en/kernel`. This is an explicit tooling path, not a persisted preference or productized language selector.

## Resolve before acting

Read `project-os-en/kernel/manifest.json` and follow `resolution_sequence`. In a terminal checkout:

```sh
python tools/project_os_resolve.py --actor <actor> --workflow <workflow>   --mode <mode> --kernel-dir project-os-en/kernel [--skill skill.<id>]
```

The resolver accelerates a canonical manifest read. Its output never grants permission or reads GitHub/git on your behalf. Browser chat does not run local Python; it reads the manifest through available sources and stays read-only and draft-only.

### Hydration level

The resolver accepts `--hydration-level minimal|compact|full/debug`. When
omitted, it uses `compact`: the practical execution view without dumping the
whole contract. `minimal` retains the IDs, boundaries, evidence, outputs,
statuses, non-authorization, and secret safety needed to stop prohibited work.
`compact` adds concise mandatory guidance, the selected actor/workflow/mode,
and resolvable references. `full/debug` expands selected-resolution metadata
for review, debugging, or audit; it is not the normal mode and does not replace
the canonical manifest.

The response declares `hydration_level` and has these deterministic shapes:

- `minimal`: manifest/actor/mode/workflow identity, every applicable boundary,
  prohibited actions, required evidence, allowed outputs, and referenced statuses.
- `compact`: all of `minimal` plus concise mandatory rules, selected operating
  context, and artifact/template/skill references.
- `full/debug`: all of `compact` plus complete selected-resolution metadata,
  including active flags and internal audit links.

```sh
python tools/project_os_resolve.py --actor actor.terminal_agent \
  --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
  --kernel-dir project-os-en/kernel --hydration-level full/debug
```

The level changes returned content only: it does not read GitHub/git, invent
state, or grant permission. Unknown values fail closed. The canonical Python
parameter is `hydration_level`; `compact` remains a compatibility alias. The
pre-existing `--compact` flag only controls JSON indentation.

## Adopt a target

Use `../adapters/AGENTS.target.md` as the only complete terminal bootloader. Claude and Gemini files are shims. Use `BROWSER_CHAT.target.md` separately for browser chat. Preserve metadata order and put only stable target-owned commands, paths, domain/security constraints, language, and escalation notes in the target section.

## Start operating

Open `../operations/README.md`, choose the operation matching the real lifecycle outcome, fill its variables, and gather the declared live evidence. Optional local prompt generation may call `tools.operation_prompt_wizard.discover_operations(Path("project-os-en/operations"))`; this does not execute the operation or choose a global language.

Stop with the resolved status if the kernel, scope, authority, evidence, or validation is missing or ambiguous.
