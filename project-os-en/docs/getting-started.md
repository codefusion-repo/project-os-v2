# Getting started

## Choose the language surface

Spanish is the default: omit `--kernel-dir` or select `project-os-es/kernel`. Select English only by passing `--kernel-dir project-os-en/kernel`. This is an explicit tooling path, not a persisted preference or productized language selector.

## Resolve before acting

Read `project-os-en/kernel/manifest.json` and follow `resolution_sequence`. In a terminal checkout:

```sh
python tools/project_os_resolve.py --actor <actor> --workflow <workflow>   --mode <mode> --kernel-dir project-os-en/kernel [--skill skill.<id>]
```

The resolver accelerates a canonical manifest read. Its output never grants permission or reads GitHub/git on your behalf. Browser chat does not run local Python; it reads the manifest through available sources and stays read-only and draft-only.

## Adopt a target

Use `../adapters/AGENTS.target.md` as the only complete terminal bootloader. Claude and Gemini files are shims. Use `BROWSER_CHAT.target.md` separately for browser chat. Preserve metadata order and put only stable target-owned commands, paths, domain/security constraints, language, and escalation notes in the target section.

## Start operating

Open `../operations/README.md`, choose the operation matching the real lifecycle outcome, fill its variables, and gather the declared live evidence. Optional local prompt generation may call `tools.operation_prompt_wizard.discover_operations(Path("project-os-en/operations"))`; this does not execute the operation or choose a global language.

Stop with the resolved status if the kernel, scope, authority, evidence, or validation is missing or ambiguous.
