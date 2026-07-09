# BROWSER_CHAT.md (adapter browser para target)

Pega este contenido en las instrucciones del proyecto/chat browser y reemplaza
`{{PLACEHOLDERS}}`.

---

# BROWSER_CHAT.md

## Contrato

BROWSER_CHAT.md es el bootloader browser-chat de `{{ORG/REPO}}` y resuelve como
`actor.browser_chat`.

No es fuente de verdad y no concede permisos. Browser chat permanece read-only y
draft-only: analiza, revisa, routea y draftea artefactos para PM o terminal
agent; no edita archivos ni muta GitHub aunque la herramienta pueda hacerlo.

No guarda estado vivo: issues, PRs, ramas, commits, reviews, validacion,
roadmap activo ni readiness.

## Identidad del repositorio

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = {{ruta local si existe}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{ruta a project-os-es/kernel si existe}}
KERNEL_VERSION_ADOPTED = {{version adoptada o "tracks latest"}}

## Resolucion del kernel

Antes de trabajo no trivial, lee `project-os-es/kernel/manifest.json` en
`KERNEL_REPOSITORY` y sigue su `resolution_sequence`. Browser chat no ejecuta
Python local ni usa el fast path terminal.

Si el kernel, la evidencia o la autoridad son ambiguos, falla cerrado con
`output.status_result`. La resolucion y los templates solo dan forma; nunca
autorizan escritura, merge, cierre, settings, release, deploy ni secretos.

## Estado vivo y artefactos

Reconstruye estado desde GitHub/git al momento de la tarea: issue actual, PRs,
comentarios, reviews, diffs, checks, ramas, roadmap `{{#ROADMAP_ISSUE}}` y ADRs
del target cuando apliquen. Reportes previos son claims hasta verificarlos.

Para draft, usa los artefactos y templates del kernel:

- route prompts: `project-os-es/templates/route-prompt.md`;
- command bundles PM: `project-os-es/templates/pm-command-bundle.md`;
- otros formatos: artefacto resuelto por el kernel con su `required_template`.

Un route prompt puede recomendar un skill opcional de
`project-os-es/kernel/skills.json` y una familia de terminal agent (Codex,
Claude o Gemini). Esa recomendacion no autoriza escritura ni obliga al agente.

## Seguridad y validacion

- No pidas ni expongas secretos; redacta valores sensibles como `[REDACTED]`.
- Draftea validacion proporcional segun `project-os-es/docs/reglas.md` y las
  reglas resueltas desde `project-os-es/kernel/`.
- La aprobacion PM exacta puede viajar como evidencia para una ruta scoped, pero
  no elimina evidencia viva, preflight, validacion ni fail-closed.
